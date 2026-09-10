"""Offline routing demonstration. Primary: ADRL-RTG-002.

Secondary: ADRL-RTG-003, ADRL-CAS-001/003/005.
Uses unchanged runtime classes with explicitly synthetic requests, observations,
gate outcomes and outcome events. No model calls, task execution or live policy changes.
The separate temporary ledger must never be imported as real learning evidence.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

REGISTER = Path(__file__).resolve().parents[3]
CORE = REGISTER.parent / "adrl-core"
sys.path[:0] = [str(CORE / "src"), str(CORE)]

import structlog

from adrl.cascade.controller import CascadeController
from adrl.cascade.sticky import MemoryStateProvider
from adrl.config.loaders import load_bundle
from adrl.config.settings import Settings
from adrl.core.enums import FailureType, OutcomeState, RequestClass, Rung
from adrl.core.types import PermittedSet
from adrl.ledger.facade import SqliteLedgerProvider
from adrl.ledger.store import LedgerStore
from adrl.routing.router import Router
from adrl.routing.rule_health import compute_rule_health
from tests.unit.routing.helpers import make_ctx, make_gate, make_obs, tool_turn, user_body


def looping_body(complete: bool) -> dict:
    extra = []
    for index in range(3):
        extra += tool_turn("Read", {"file_path": "a.py"}, "same", idx=index)
    if not complete:
        extra[-1] = {"role": "user", "content": []}
        extra.extend([
            {"role": "assistant", "content": [
                {"type": "tool_use", "id": "pending-1", "name": "Read", "input": {"file_path": "b.py"}},
                {"type": "tool_use", "id": "pending-2", "name": "Read", "input": {"file_path": "c.py"}},
            ]},
            {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "pending-1", "content": "b"}]},
        ])
    return user_body("Fix the typo in README.md", extra_messages=extra)


def record(router, decision) -> dict:
    return {"decision": decision.as_row(), "context": router.decision_context(decision)}


async def stress_matrix(bundle) -> dict:
    inputs_path = Path(__file__).with_name("stress-cases.json")
    inputs = json.loads(inputs_path.read_text())
    router = Router(bundle)
    rows = []
    issues = []
    counts = {r.value: 0 for r in Rung}
    invariant_failures = []
    for case in inputs["cases"]:
        cells = {}
        for variant in inputs["variants"]:
            body = user_body(case["prompt"])
            gate = make_gate()
            if variant == "previous_edit_failed":
                body["messages"].extend(tool_turn("Edit", {"file_path":"a.py"},
                    "String to replace not found in file", is_error=True))
            elif variant == "large_context":
                body["system"] = "x" * 100_000
            elif variant == "local_only":
                gate = make_gate(pinned=True)
            elif variant == "local_and_cheap_only":
                gate = make_gate(PermittedSet(frozenset({Rung.LOCAL, Rung.CHEAP_CLOUD})))
            traces = []
            for repeat in range(inputs["repeats"]):
                decision = await router.decide(make_ctx(body), gate, None)
                trace = record(router, decision)
                traces.append(trace)
                if decision.rung not in gate.permitted:
                    invariant_failures.append([case["id"], variant, "outside_permitted_set"])
                if variant == "local_only" and decision.rung is not Rung.LOCAL:
                    invariant_failures.append([case["id"], variant, "pin_ignored"])
            comparable = []
            for trace in traces:
                copied = json.loads(json.dumps(trace))
                copied["decision"].pop("route_id")
                comparable.append(copied)
            if any(c != comparable[0] for c in comparable[1:]):
                invariant_failures.append([case["id"], variant, "repeat_changed_semantics"])
            cells[variant] = traces[0]
        chosen = cells["ordinary"]["decision"]["decided_rung"]
        counts[chosen] += 1
        if case.get("review_expectation") == "not_local" and chosen == "local":
            issues.append({"case":case["id"], "hypothesis":case["review_hypothesis"],
                "observed":chosen, "status":"review_hypothesis_failed"})
        rows.append({**case, "variants":cells})
    return {"case_version":inputs["version"],
        "input_sha256":hashlib.sha256(inputs_path.read_bytes()).hexdigest(),
        "task_prompts":len(rows), "variants_per_prompt":len(inputs["variants"]),
        "repeats":inputs["repeats"], "decision_evaluations":len(rows)*len(inputs["variants"])*inputs["repeats"],
        "ordinary_choice_counts":counts, "invariant_failures":invariant_failures,
        "review_hypothesis_failures":issues, "rows":rows,
        "scope":"Routing component behavioural probes, not completed coding tasks or full gateway safety tests"}


async def demonstrate() -> dict:
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.CRITICAL))
    bundle = load_bundle(Settings(config_dir=CORE / "config"))
    router = Router(bundle)
    scenarios = []
    for name, text, pinned in [
        ("simple", "Fix the typo in README.md", False),
        ("complex", "Refactor the whole payments module", False),
        ("uncertain", "hmm can you look at the thing we discussed and sort it", False),
        ("private", "Refactor the whole payments module", True),
    ]:
        decision = await router.decide(make_ctx(user_body(text)), make_gate(pinned=pinned), None)
        scenarios.append({"id": name, "prompt": text, "synthetic_pin": pinned, **record(router, decision)})
    assert [s["decision"]["decided_rung"] for s in scenarios] == ["local", "frontier", "frontier", "local"]

    async def cascade_case(pinned: bool) -> dict:
        controller = CascadeController(bundle, MemoryStateProvider())
        gate = make_gate(pinned=pinned)
        ctx = make_ctx(user_body("Fix the typo in README.md"))
        decision = await router.decide(ctx, gate, None)
        first = await controller.plan(ctx, decision, gate, None)
        observed = await controller.observe(ctx, first, make_obs(rung=Rung.LOCAL))
        partial = make_ctx(looping_body(False), RequestClass.CONTINUATION)
        second = await controller.plan(partial, decision, gate, observed.sticky)
        loop = await controller.observe(partial, second, make_obs(rung=Rung.LOCAL))
        waiting = await controller.plan(partial, decision, gate, loop.sticky)
        boundary = make_ctx(looping_body(True), RequestClass.CONTINUATION)
        switched = await controller.plan(boundary, decision, gate, loop.sticky)
        assert first.rung is Rung.LOCAL and waiting.rung is Rung.LOCAL
        assert loop.fired and not waiting.escalated
        assert switched.escalated is (not pinned)
        assert switched.rung is (Rung.LOCAL if pinned else Rung.CHEAP_CLOUD)
        return {
            "synthetic_pin": pinned,
            "initial_rung": first.rung.value,
            "tripwires": list(loop.fired_wires),
            "escalation_pending": loop.escalation_pending,
            "while_tools_pending": {"rung": waiting.rung.value, "escalated": waiting.escalated},
            "at_complete_boundary": {"rung": switched.rung.value, "escalated": switched.escalated,
                "handoff_created": switched.handoff is not None, "block": str(switched.block) if switched.block else None},
        }

    cascades = [await cascade_case(False), await cascade_case(True)]

    # Supply invented outcome events through the real append-only store. These
    # are mechanism probes, not verified task results, calibration data or a trial.
    with TemporaryDirectory(prefix="adrl-synthetic-routing-") as directory:
        store = LedgerStore(Path(directory) / "synthetic.db")
        store.open()
        try:
            ledger = SqliteLedgerProvider(store)
            for index in range(20):
                ctx = make_ctx(user_body("Fix the typo in README.md"))
                decision = await router.decide(ctx, make_gate(), None)
                context = router.decision_context(decision,
                    session_hmac=ctx.session_hmac, lineage_hmac=ctx.lineage_hmac,
                    request_class="user_turn", content_bearing=True, evidence_kind="synthetic_only")
                assert await ledger.append_decision(decision, context)
                success = index < 12
                await store.write_through(LedgerStore.insert_event(
                    decision.route_id, OutcomeState.CLOSED_FINAL.value,
                    "synthetic-demo-only", 1,
                    {"verified": True, "success": success,
                     "failure_type": None if success else FailureType.TASK_CAPABILITY.value,
                     "evidence_kind": "synthetic_only", "learning_eligible": False},
                    "events-v1",
                ))
            health = compute_rule_health(store, threshold=bundle.policy.rule_precision_threshold)
            before = await router.decide(make_ctx(user_body()), make_gate(), None)
            # Explicit refresh in this demonstration. The service currently builds
            # its health snapshot at startup; no recurring refresh is wired there.
            router.set_rule_health(health)
            after = await router.decide(make_ctx(user_body()), make_gate(), None)
            pinned_after = await router.decide(make_ctx(user_body()), make_gate(pinned=True), None)
            assert before.rung is Rung.LOCAL and after.rung is Rung.FRONTIER
            assert pinned_after.rung is Rung.LOCAL
            correction = {
                "synthetic_successes": 12, "synthetic_outcomes": 20,
                "health": health.as_report(), "before": before.as_row(),
                "after_explicit_refresh": record(router, after),
                "pinned_after_explicit_refresh": pinned_after.as_row(),
                "automatic_service_refresh": False,
                "learned_model_used": False,
            }
        finally:
            store.close()

    stress = await stress_matrix(bundle)
    source_record = json.loads((REGISTER / "reports/research/adrl-w3-transport-receipts-2026-09-08.json").read_text())
    source = source_record["source_after"]
    mismatches = [p for p, meta in source.items() if hashlib.sha256((CORE / p).read_bytes()).hexdigest() != meta["sha256"]]
    assert not mismatches, mismatches
    return {
        "schema": "adrl-offline-routing-demonstration-v1", "generated_at": datetime.now(UTC).isoformat(),
        "scope": "Unchanged real routing/cascade/rule-health code, synthetic inputs and outcome events; no model or harness execution",
        "runtime_inputs_verified_unchanged": len(source), "config_versions": bundle.versions,
        "model_calls": 0, "new_paid_usage": 0, "task_quality_measured": False,
        "learning_eligible": False, "live_policy_changed": False, "maturity_promotions": 0,
        "scenarios": scenarios, "cascades": cascades, "rule_correction": correction,
        "stress_matrix":stress,
        "limitations": [
            "Gate outcomes are injected; this does not test secret detection, trust attestation or durable pins.",
            "Observations and completed outcomes are invented fixtures; no model completed any task.",
            "The rule-health refresh is explicitly invoked by this driver, not scheduled by the service.",
            "Current heuristic probabilities and config model aliases are not measured capability or availability claims.",
            "This is an offline decision demonstration, not an admitted learning dataset or routing-benefit benchmark.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = asyncio.run(demonstrate())
    payload = json.dumps(result, indent=2, default=str) + "\n"
    if args.output:
        args.output.write_text(payload)
    print(json.dumps({"scenarios": {s["id"]: s["decision"]["decided_rung"] for s in result["scenarios"]},
        "unrestricted_stuck_task": result["cascades"][0]["at_complete_boundary"],
        "rule_correction": {"before": result["rule_correction"]["before"]["decided_rung"],
            "after": result["rule_correction"]["after_explicit_refresh"]["decision"]["decided_rung"]},
        "stress_summary":{k:v for k,v in result["stress_matrix"].items() if k != "rows"},
        "model_calls": 0, "runtime_inputs_unchanged": result["runtime_inputs_verified_unchanged"]}, indent=2))
