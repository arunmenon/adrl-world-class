# ADRL-OPS-006: Record the served identity, not the intended one

| Field | Value |
|---|---|
| Bucket | OPS; Platform, Runtime, Operations |
| Status | Proposed 2026-09-03 (first capture; referenced by CAS-006, RTG-008, LRN-004, MEM-006 since 2026-08-27) |
| Maturity | D2 Tested; adrl-core records `served_rung`, `served_model`, `served_provider` and `served_source` from the gateway header, then `message_start.model`, else `assumed_intended`, under unit and end-to-end tests; no organic traffic yet, so D3 is not claimed (EVL-007) |
| Review verdict | PROPOSED (new) |
| Tenets | 7, 8 |
| Related decisions | CAS-006, RTG-008, RTG-009, LRN-004, MEM-006, SAF-009, OPS-003 |
| Open questions | Q7 |

## Decision

Every response is recorded with the identity that actually served it: deployment id (OPS-003), model, provider and, where the inventory carries them, trust zone and geography; plus a `served_source` of `gateway_reported`, `proxy_observed` or `assumed_intended`. The gateway reports identity on every response under the contract in RTG-008 (`gen_ai.response.model`, `gen_ai.provider.name`, or the equivalent header); the proxy observes `message_start.model` as the second source; `assumed_intended` is the last resort and marks the row so that (1) sticky state built on it is flagged, (2) failure types on it are `unverifiable`, and (3) the egress ledger records `destination_unconfirmed`. The share of `assumed_intended` rows is a scorecard metric with an EVL-009 blocker threshold. `served_rung` is deny-listed as a training feature (LRN-004).

## Context and rationale

CAS-006 says record what happened, not what you asked for, and RTG-008 gives the gateway contract. The 2026-09-03 external review pointed out that "left the machine" was being inferred from the intended rung name. This decision extends served identity to the deployment, so that the egress ledger's answer to "did this leave the machine" is derived from where the response actually came from, matched against the signed inventory, not from a label the router chose.

## Adversarial review (2026-09-03)

### Steelman
Recording the served identity is the detective control behind every preventive one in FND-002 and OPS-003. Extending it from rung to deployment costs one lookup and closes the review's residency finding on the audit side.

### Attacks
1. **The gateway header can lie.** Answered: it can; the contract makes that the gateway team's breach, and `proxy_observed` from the response body is the cross-check. A disagreement between the two is an `infrastructure` event.
2. **`assumed_intended` will dominate until the gateway contract lands.** Answered: then the scorecard shows it, and the blocker holds routing below D4 until it falls.
3. **Deployment-level identity leaks infrastructure detail into the ledger.** Answered: the ledger stores the inventory's deployment id, an opaque label; the inventory itself is the sensitive document and is access-controlled.

### Evidence
- ADRL-CAS-006 (amended); `served_rung`, `served_model`, `served_provider`, `served_source`; `assumed_intended` semantics.
- ADRL-RTG-008 (amended); gateway leak contract with served identity on every response.
- ADRL-LRN-004; `served_rung` deny-listed.
- 2026-09-03 external review of adrl-core, finding P0-1; `lineage_left_machine` infers from the rung name.

### Verdict
**PROPOSED.** Already implemented for rung and model in adrl-core; the deployment extension is the new content.

## Follow-ups

- [ ] Extend the served record with deployment id, trust zone and geography from the inventory; egress ledger derives `left_machine` from served trust zone, never from the rung name.
- [ ] Scorecard: share of `assumed_intended` rows per window with a pre-registered blocker threshold.
- [ ] Golden test: gateway header and `message_start.model` disagree yields an `infrastructure` event.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the OPS bucket) | (none) |
