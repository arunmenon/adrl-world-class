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


async def stress_matrix(bundle, inputs_path) -> dict:
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


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['before','after','after-final'], required=True)
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.CRITICAL))
    bundle = load_bundle(Settings(config_dir=CORE / 'config'))
    result = {'phase':args.phase,'original':await stress_matrix(bundle, REGISTER / 'reports/research/routing-demonstration-2026-09-08/stress-cases.json'),
              'fresh':await stress_matrix(bundle, out / 'fresh-cases.json')}
    with (out / (args.phase+'.json')).open('x') as f: json.dump(result,f,indent=2)
    print({key:result[key]['review_hypothesis_failures'] for key in ['original','fresh']})

if __name__ == '__main__': asyncio.run(main())
