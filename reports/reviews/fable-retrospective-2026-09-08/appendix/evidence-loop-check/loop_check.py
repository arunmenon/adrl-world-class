"""Bounded offline evidence-loop checks against the disposable runtime copy.

Synthetic inputs only. Writes only under the disposable directory. No network, no models.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

DISPOSABLE = Path(__file__).resolve().parent
RUNTIME = DISPOSABLE / "runtime"
OUT = DISPOSABLE / "loop-check-out"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(RUNTIME / "src"))
sys.path.insert(0, str(RUNTIME))
sys.path.insert(0, str(RUNTIME / "tools"))

import adrl  # noqa: E402

assert Path(adrl.__file__).resolve().is_relative_to(RUNTIME), adrl.__file__

results: dict[str, object] = {"adrl_import": adrl.__file__}


async def part_a_live_cascade_events() -> None:
    """Drive the real composition with the lab's synthetic endpoint; inspect the live ledger."""
    import httpx
    from starlette.applications import Starlette
    from starlette.routing import Route

    from tools.run_routing_lab import Case, SyntheticEndpoint, lab_settings, make_body
    from adrl.app import build_components
    from adrl.config.loaders import load_bundle
    from adrl.core.enums import OutcomeState, RoutingMode
    from adrl.gates.workload import HEADER_WORKLOAD_ASSERTION, RepoInventory, sign_assertion
    from adrl.ledger.labels import derive_label, outcome_state
    from adrl.ledger.events import read_stored_events
    from adrl.ledger.outcomes import Closer, routes_in_state
    from adrl.ledger.readiness import learning_readiness
    from adrl.learning.tiers import LedgerExampleReader
    from adrl.proxy.asgi import build_asgi

    endpoint = SyntheticEndpoint()
    app = Starlette(routes=[Route("/v1/messages", endpoint.messages, methods=["POST"])])
    directory = OUT / "lab-ledger"
    directory.mkdir(exist_ok=True)
    settings = lab_settings(directory)
    bundle = load_bundle(settings.model_copy(update={"routing_mode": RoutingMode.SHADOW}))
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://lab.invalid", trust_env=False
    ) as gateway:
        components = build_components(settings, bundle=bundle, gateway_client=gateway)
        try:
            inventory = RepoInventory(
                root=str(RUNTIME), remote=None, head="synthetic-only",
                fingerprint="e" * 64, tracked_files=1,
            )
            assertion = sign_assertion(inventory, components.keystore.hmac_key())
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=build_asgi(components.pipeline)),
                base_url="http://adrl.invalid", trust_env=False,
            ) as client:
                # Two user turns on one session so the first route reaches closed_turn.
                for turn in range(2):
                    case = Case(
                        id=f"turn-{turn}", family="synthetic", prompt="Fix the typo in README.md",
                        session="loop-check-session", context_chars=0, endpoint="reported",
                    )
                    endpoint.mode = case.endpoint
                    body = make_body(case)
                    response = await client.post(
                        "/v1/messages", content=json.dumps(body).encode(),
                        headers={
                            "content-type": "application/json",
                            "anthropic-version": "2023-06-01",
                            "x-claude-code-session-id": f"lab-{case.session}",
                            HEADER_WORKLOAD_ASSERTION: assertion,
                        },
                    )
                    results.setdefault("part_a_http", []).append(response.status_code)  # type: ignore[union-attr]
                await components.pipeline.drain()
            store = components.store
            types = store.read("SELECT event_type, COUNT(*) AS c FROM events GROUP BY event_type")
            results["part_a_event_types_written_by_live_pipeline"] = {
                str(r["event_type"]): int(r["c"]) for r in types
            }
            routes = [str(r["route_id"]) for r in store.read("SELECT route_id FROM decisions")]
            results["part_a_decisions"] = len(routes)
            results["part_a_routes_in_state_closed_turn_seen_by_closer"] = len(
                routes_in_state(store, OutcomeState.CLOSED_TURN)
            )
            results["part_a_outcome_state_per_route_as_seen_by_labels"] = {
                r: (outcome_state(read_stored_events(store, r)).value  # type: ignore[union-attr]
                    if outcome_state(read_stored_events(store, r)) else None)
                for r in routes
            }
            results["part_a_derived_labels"] = {
                r: derive_label(read_stored_events(store, r)).as_dict()["result"] for r in routes
            }
            closer = Closer(store, bundle.policy.close_rule)
            far_future = datetime.now(UTC) + timedelta(days=30)
            closed = await closer.scan(now=far_future)
            results["part_a_closer_scan_closed_routes_30_days_later"] = len(closed)
            results["part_a_learning_readiness"] = learning_readiness(store).as_dict()
            examples = LedgerExampleReader(store).read()
            results["part_a_learning_reader_examples"] = [
                {"outcome_state": e.outcome_state.value, "source": e.source,
                 "harness_reported_success": e.harness_reported_success,
                 "verification": e.verification, "features_version": e.features_version}
                for e in examples
            ]
        finally:
            await components.aclose()


async def part_b_correction_and_neighbour_and_tier() -> None:
    from adrl.config.loaders import load_bundle
    from adrl.core.enums import FailureType, OutcomeState, VerificationResult
    from adrl.core.ids import RouteId
    from adrl.ledger.events import (
        LABEL_CORRECTION_EVENT, LATE_EVIDENCE_EVENT, OUTCOME_EVENT, CauseCandidate,
        OutcomeFields, outcome_event, read_stored_events, verification_event,
    )
    from adrl.ledger.labels import derive_label
    from adrl.ledger.outcomes import append_late_evidence, ledger_event_to_write
    from adrl.ledger.store import LedgerStore
    from adrl.learning.dataset import LedgerNeighbourSource, build_frame, temporal_session_split
    from adrl.learning.tiers import (
        LedgerExampleReader, TieredDataset, VerifierPrecision, assign_tier,
    )
    from tools.run_routing_lab import lab_settings

    directory = OUT / "lib-ledger"
    directory.mkdir(exist_ok=True)
    store = LedgerStore(directory / "lib.db")
    store.open()
    settings = lab_settings(directory)
    from adrl.core.enums import RoutingMode
    bundle = load_bundle(settings.model_copy(update={"routing_mode": RoutingMode.SHADOW}))
    contract = bundle.learning_contract
    try:
        def decision_row(route: str, ts_offset_s: int, band: str = "clear-local") -> None:
            row = {
                "route_id": route, "permitted_set": ["local", "cheap_cloud", "frontier"],
                "decided_rung": "local", "estimator": "band-heuristic",
                "estimator_version": "v1", "policy_version": "p1", "objective_version": "o1",
                "cascade_feasible": True, "features": {"band_id": band, "request_class": "user_turn"},
                "features_version": contract.feature_schema_version,
            }
            ctx = {"session_hmac": "s-" + route[:3], "lineage_hmac": "l1",
                   "request_class": "user_turn", "content_bearing": True}
            store.submit(LedgerStore.insert_decision(row, ctx)).result(timeout=10)

        # B1: verified PASS then late human correction: does the label or the reader change?
        r1 = RouteId("r1-pass-then-corrected")
        decision_row(str(r1), 0)
        store.submit(ledger_event_to_write(outcome_event(
            r1, OutcomeState.CLOSED_FINAL, "closer", 1,
            OutcomeFields(harness_reported_success=True), rule_id="close-v1", trigger="idle",
        ))).result(timeout=10)
        store.submit(ledger_event_to_write(verification_event(
            r1, 7, verifier_version="verifier-v1", argv=[], protected_path_policy_version="p",
            tree_identity={}, result=VerificationResult.PASS, started_at="t", finished_at="t",
            tree_drift=False, checks=[],
        ))).result(timeout=10)
        before = derive_label(read_stored_events(store, r1)).as_dict()
        await append_late_evidence(
            store, r1, source="human_correction", detail={"kind": "revert"},
            causes=(CauseCandidate(FailureType.TASK_CAPABILITY, None, "human_correction"),),
        )
        events = read_stored_events(store, r1)
        after = derive_label(events).as_dict()
        results["part_b1_label_before_correction"] = before["result"]
        results["part_b1_label_after_human_revert"] = after["result"]
        results["part_b1_late_evidence_events"] = sum(
            1 for e in events if e.event_type == LATE_EVIDENCE_EVENT
        )
        results["part_b1_label_correction_events"] = sum(
            1 for e in events if e.event_type == LABEL_CORRECTION_EVENT
        )

        # B2: tripwire failure at closed_final, then late human correction that supersedes; does
        # the learning reader see the corrected label?
        r2 = RouteId("r2-failure-then-corrected")
        decision_row(str(r2), 0)
        store.submit(ledger_event_to_write(outcome_event(
            r2, OutcomeState.CLOSED_FINAL, "closer", 1,
            OutcomeFields(causes=(CauseCandidate(FailureType.INFRASTRUCTURE, 0, "cascade"),)),
            rule_id="close-v1", trigger="idle",
            label={"result": "excluded", "failure_type": "infrastructure"},
        ))).result(timeout=10)
        store.submit(LedgerStore.insert_event(
            str(r2), "label", "labeler", 5,
            {"result": "excluded", "failure_type": "infrastructure", "supersedes_seq": None},
            "events-v1",
        )).result(timeout=10)
        await append_late_evidence(
            store, r2, source="human_correction", detail={"kind": "re_edit"},
            causes=(CauseCandidate(FailureType.TASK_CAPABILITY, None, "human_correction"),),
        )
        ledger_label = derive_label(read_stored_events(store, r2)).as_dict()
        reader_example = [e for e in LedgerExampleReader(store).read() if str(e.route_id) == str(r2)][0]
        results["part_b2_ledger_label_failure_type"] = ledger_label["failure_type"]
        results["part_b2_learning_reader_failure_type"] = (
            reader_example.failure_type.value if reader_example.failure_type else None
        )
        results["part_b2_correction_events_present"] = sum(
            1 for e in read_stored_events(store, r2) if e.event_type == LABEL_CORRECTION_EVENT
        )

        # B2b: proxy success at closed_final, then a human revert. Ledger label vs learning reader.
        r2b = RouteId("r2b-proxy-success-then-revert")
        decision_row(str(r2b), 0)
        store.submit(ledger_event_to_write(outcome_event(
            r2b, OutcomeState.CLOSED_TURN, "cascade", 1, OutcomeFields(harness_reported_success=True),
        ))).result(timeout=10)
        pre_label = derive_label(read_stored_events(store, r2b))
        store.submit(ledger_event_to_write(outcome_event(
            r2b, OutcomeState.CLOSED_FINAL, "closer", 2, OutcomeFields(harness_reported_success=True),
            rule_id="close-v1", trigger="idle", label=pre_label.as_dict(),
        ))).result(timeout=10)
        store.submit(LedgerStore.insert_event(
            str(r2b), "label", "labeler", 5, {**pre_label.as_dict(), "supersedes_seq": None}, "events-v1",
        )).result(timeout=10)
        await append_late_evidence(
            store, r2b, source="human_correction", detail={"kind": "revert"},
            causes=(CauseCandidate(FailureType.TASK_CAPABILITY, None, "human_correction"),),
        )
        ev = read_stored_events(store, r2b)
        ledger_after = derive_label(ev).as_dict()
        reader_ex = [e for e in LedgerExampleReader(store).read() if str(e.route_id) == str(r2b)][0]
        results["part_b2b_ledger_label_after_revert"] = {
            "result": ledger_after["result"], "failure_type": ledger_after["failure_type"], "basis": ledger_after["basis"]}
        results["part_b2b_correction_events_present"] = sum(1 for e in ev if e.event_type == LABEL_CORRECTION_EVENT)
        results["part_b2b_learning_reader_label"] = {
            "label": reader_ex.label, "failure_type": reader_ex.failure_type.value if reader_ex.failure_type else None,
            "tier": assign_tier(reader_ex, contract).tier}

        # B3: LedgerNeighbourSource success attribution for a closer-written closed_final failure.
        r3 = RouteId("r3-verified-failure-neighbour")
        decision_row(str(r3), 0)
        store.submit(ledger_event_to_write(verification_event(
            r3, 9, verifier_version="verifier-v1", argv=[], protected_path_policy_version="p",
            tree_identity={}, result=VerificationResult.FAIL, started_at="t", finished_at="t",
            tree_drift=False, checks=[], causes=(CauseCandidate(FailureType.TASK_CAPABILITY, None, "verifier"),),
        ))).result(timeout=10)
        store.submit(ledger_event_to_write(outcome_event(
            r3, OutcomeState.CLOSED_FINAL, "closer", 1, OutcomeFields(),
            rule_id="close-v1", trigger="idle",
            label=derive_label(read_stored_events(store, r3)).as_dict(),
        ))).result(timeout=10)
        r4 = RouteId("r4-query")
        decision_row(str(r4), 0)
        neighbours = LedgerNeighbourSource(store).neighbours(r4, k=10)
        results["part_b3_ledger_label_of_r3"] = derive_label(read_stored_events(store, r3)).as_dict()["result"]
        results["part_b3_neighbour_records_seen_from_r4"] = [
            {"route": str(n.route_id), "success_as_seen_by_neighbour_source": n.success}
            for n in neighbours
        ]

        # B4: T1 reachable? Best possible organic example without / with a precision record.
        examples = LedgerExampleReader(store).read()
        r1_example = [e for e in examples if str(e.route_id) == str(r1)][0]
        results["part_b4_tier_without_precision_record"] = assign_tier(r1_example, contract).tier
        results["part_b4_tier_with_precision_record"] = assign_tier(
            r1_example, contract,
            {"verifier-v1": VerifierPrecision("verifier-v1", 1.0, 0.0, 0.0, 10)},
        ).tier
        results["part_b4_verifier_precision_producers_in_src"] = "none (grep)"

        # B5: features-v2 rows against the v1 contract.
        from adrl.routing.features import FEATURES_VERSION
        from dataclasses import replace
        try:
            build_frame(
                TieredDataset.build([replace(r1_example, features_version=FEATURES_VERSION)],
                                    contract, {"verifier-v1": VerifierPrecision("verifier-v1", 1.0, 0.0, 0.0, 10)}).examples,
                contract,
            )
            results["part_b5_features_v2_into_v1_contract"] = "accepted"
        except Exception as exc:  # noqa: BLE001
            results["part_b5_features_v2_into_v1_contract"] = f"{type(exc).__name__}: {exc}"
        results["part_b5_live_FEATURES_VERSION"] = FEATURES_VERSION
        results["part_b5_contract_feature_schema_version"] = contract.feature_schema_version
    finally:
        store.close()


async def main() -> None:
    try:
        await part_a_live_cascade_events()
    except Exception as exc:  # noqa: BLE001
        results["part_a_error"] = f"{type(exc).__name__}: {exc}"
    try:
        await part_b_correction_and_neighbour_and_tier()
    except Exception as exc:  # noqa: BLE001
        results["part_b_error"] = f"{type(exc).__name__}: {exc}"
    (OUT / "results.json").write_text(json.dumps(results, indent=2, default=str))
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    os.environ.setdefault("ADRL_CONFIG_DIR", str(RUNTIME / "config"))
    asyncio.run(main())
