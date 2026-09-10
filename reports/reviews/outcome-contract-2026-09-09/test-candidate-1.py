"""ADRL-MEM-002: persisted cascade outcomes reach the canonical lifecycle consumers.

Synthetic ASGI transport only. The shared E2E fixture loads SHADOW configuration into
LIVE components; these tests do not qualify live configuration admission or real traffic.
"""

from datetime import UTC, datetime, timedelta

import pytest

from adrl.config.models import CloseRule
from adrl.core.enums import FailureType, OutcomeState
from adrl.core.ids import RouteId
from adrl.ledger.events import OUTCOME_EVENT, read_stored_events
from adrl.ledger.outcomes import Closer, read_projection, routes_in_state
from adrl.ledger.readiness import learning_readiness

from .conftest import E2E, user_turn_body


async def test_composed_outcomes_close_once_without_inventing_success(live: E2E) -> None:
    await live.send("user_turn", body=user_turn_body("Fix the typo in README.md"))
    first = RouteId(live.decisions()[0]["route_id"])
    await live.send("user_turn", body=user_turn_body("Fix another typo in README.md"))
    second = RouteId(live.decisions()[1]["route_id"])
    assert [e.route_id for e in routes_in_state(live.store, OutcomeState.CLOSED_TURN)] == [first]
    events = read_stored_events(live.store, first, OUTCOME_EVENT)
    assert [e.payload["state"] for e in events] == ["pending", "closed_turn"]
    assert all(
        e.event.producer == "cascade" and e.event.schema_version == "events-v1" for e in events
    )
    assert [e.event.producer_seq for e in events] == [1, 2]
    assert all(e.payload.get("harness_reported_success") is None for e in events)
    assert events[-1].payload["session_hmac"] == live.decisions()[0]["session_hmac"]
    assert read_projection(live.store, second).state is OutcomeState.PENDING
    closer = Closer(live.store, CloseRule())
    future = datetime.now(UTC) + timedelta(days=1)
    assert await closer.scan(now=future) == [(first, "idle")]
    assert await closer.scan(now=future) == []
    projected = read_projection(live.store, first)
    assert projected.state is OutcomeState.CLOSED_FINAL
    assert projected.label.failure_type is FailureType.UNVERIFIABLE
    assert projected.label.result == "excluded"
    assert len(live.store.read_events(first, "label")) == 1
    readiness = learning_readiness(live.store)
    assert readiness.closed_final_count == 1
    assert readiness.censored_count == 1
    assert readiness.capability_evidence_count == readiness.verified_success_count == 0
    assert readiness.window_blocked and "no_capability_evidence" in readiness.blockers


@pytest.mark.parametrize(
    "status,cause", [(503, FailureType.INFRASTRUCTURE), (400, FailureType.UNVERIFIABLE)]
)
async def test_terminal_cause_survives_next_turn_and_close(
    live: E2E, status: int, cause: FailureType
) -> None:
    live.gateway_state.status_code = status
    response = await live.send("user_turn")
    assert response.status_code == status
    first = RouteId(live.decisions()[0]["route_id"])
    assert read_projection(live.store, first).state is OutcomeState.CLOSED_TURN
    live.gateway_state.status_code = 200
    await live.send("user_turn", body=user_turn_body("Fix the typo in README.md"))
    closed = [
        e
        for e in read_stored_events(live.store, first, OUTCOME_EVENT)
        if e.payload["state"] == "closed_turn"
    ]
    assert len(closed) == 2
    assert closed[0].payload["failure_type"] == cause.value
    assert closed[-1].payload["reason"] == "next_user_turn"
    await Closer(live.store, CloseRule()).scan(now=datetime.now(UTC) + timedelta(days=1))
    label = read_projection(live.store, first).label
    assert label.result == "excluded" and label.failure_type is cause
    assert learning_readiness(live.store).capability_evidence_count == 0
