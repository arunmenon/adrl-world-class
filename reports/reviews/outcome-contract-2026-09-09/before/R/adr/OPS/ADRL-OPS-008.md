# ADRL-OPS-008: Fail-open SLOs, alerting and bypass audit

| Field | Value |
|---|---|
| Bucket | OPS; Platform, Runtime, Operations |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D1 Code; adrl-core counts fail-open events by failure class and pin state and records bypass events, but thresholds are not pre-registered and no alert route exists |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8 |
| Related decisions | FND-004, SAF-001, SAF-004, SAF-009, MEM-006, EVL-008, EVL-009, OPS-007 |
| Open questions | Q7 |

## Decision

1. *SLIs.* Fail-open rate per failure class (`routing_path`, `gate_path`, `proxy_path`) and per pin state, computed over requests; `unscanned` share of forwarded requests; `memory_degraded` count; `ledger_degraded` count; gate latency p99 on continuations (SAF-003 budget); block rate per pinned lineage (SAF-005); `assumed_intended` share (OPS-006).
2. *SLOs.* Each SLI has a pre-registered threshold in `ops-slo-v1.json`. The fail-open thresholds are set per class because the classes carry different risk: `gate_path` on an unpinned lineage is the one that forwards unscanned content and has the tightest bound.
3. *Alerting.* Breach of any threshold over a declared window raises an alert to the named on-call owner and opens the corresponding EVL-009 blocker; alerts are recorded in the egress ledger so that the audit trail shows when the operator knew.
4. *Bypass audit.* The one-step operator bypass (FND-004: repoint the harness at the gateway) is recorded with actor, reason and duration; a bypass longer than a declared bound is an alert; a bypass never releases a pin (SAF-002) and the pinned lineages active during a bypass are listed in the incident record (OPS-007).
5. *Every fail-open is recorded* with its class, pin state and the request class it affected, and gate-internal fail-opens produce the same record as pipeline-level ones.

## Context and rationale

FND-004's replacement text requires that every automatic fail-open be recorded and that a sustained rate raise an alert; the review's SAF-001 amendment gave gate failures their semantics. What was missing is the operational side: which numbers, what thresholds, who is told, and how the operator bypass is audited. The 2026-09-03 conformance review of adrl-core also found that fail-open accounting was split across two label spellings and that gate-internal fail-opens were recorded differently from pipeline ones; clause 5 closes that class of drift.

## Adversarial review (2026-09-03)

### Steelman
Pre-registered thresholds with an alert route are the difference between a fail-open that is a design choice and a fail-open that is a silent policy change. Recording alerts in the egress ledger keeps the audit trail and the operational trail in one place.

### Attacks
1. **Thresholds set before any traffic will be wrong.** Answered: they are versioned; a change is recorded with its reason and the scorecard shows both.
2. **On-call for a developer-laptop proxy is theatre.** Answered: the on-call owner may be the developer; the point is that the alert is delivered and recorded, not who wears the pager.
3. **A long bypass is sometimes legitimate (gateway outage).** Answered: legitimate bypasses have a reason and an end; the alert asks for both.

### Evidence
- ADRL-FND-004 (replacement); every fail-open recorded with its class; sustained rate alerts; audited one-step bypass that cannot release a pin.
- ADRL-SAF-001 (amended); gate failure semantics by pin state; `unscanned` can never widen.
- ADRL-MEM-006 (amended); `memory_degraded` as an OPS health signal.
- 2026-09-02 conformance review of adrl-core, defect 10; inconsistent fail-open labels and records.

### Verdict
**PROPOSED.** The operational contract FND-004 assumed. Needs an owner and pre-registered values.

## Follow-ups

- [ ] Write `ops-slo-v1.json` with the SLIs, thresholds, windows and on-call owner.
- [ ] Alert route (terminal, file, or webhook) with the alert appended to the egress ledger.
- [ ] Golden test: a synthetic burst of `gate_path` fail-opens on unpinned lineages crosses the threshold and produces one alert record and one open blocker.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the OPS bucket) | (none) |
