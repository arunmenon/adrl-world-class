# ADRL-OPS-003: Endpoint inventory, rollout and change control

| Field | Value |
|---|---|
| Bucket | OPS; Platform, Runtime, Operations |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D0 Design; adrl-core generates a LiteLLM config from `rungs.yaml` and `gateway-endpoints.yaml` with rung-closed checks, but the inventory is unsigned and carries no trust zone, so a local group pointed at an external host passes every check (2026-09-03 external review, P0) |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 7 |
| Related decisions | FND-002, RTG-001, RTG-008, SAF-006, SAF-008, SAF-009, CAS-006, OPS-002, OPS-006 |
| Open questions | Q1, Q7 |

## Decision

Every model deployment ADRL may dispatch to is an entry in a signed endpoint inventory (`endpoint-inventory-v<N>`) carrying: deployment id, provider, model family, rung, trust zone (`on_host`, `private_network`, `public_cloud`), geography, data-use profile (training opt-out status), the gateway model group that fronts it, and an evidence reference for its rung boundary (RTG-001). The inventory is signed by the manifest key (OPS-002) and verified at startup; the LiteLLM config is generated from it and from nothing else; and CI checks that (1) every gateway model group maps to exactly one inventory entry, (2) no fallback group crosses a rung or a trust zone, (3) every `local` entry has trust zone `on_host` and an `api_base` on a loopback or Unix-socket address, (4) a `live` rung has an evidence reference. Adding a deployment requires a security co-sign for any entry outside `on_host`; changing a deployment's zone, geography or profile is a new inventory version. The served identity recorded on each response (OPS-006) is matched against the inventory, and a mismatch is an `infrastructure` event and a blocker (EVL-009).

## W0 execution baseline, 2026-09-07

Current-context correction: signed endpoint inventory, local-address/trust-zone checks and deployment-set enforcement already exist in the build, as recorded in the dated September 3 closure and exercised by the current TRU suite. The design-only wording in the earlier maturity row remains historical and is not a description of absent code. W0 rechecks configuration and records its declared-source hashes; production inventory, endpoint receipt qualification and release authority remain W6 work. This note adds evidence without silently promoting the whole decision.

See the [W0 packet](../../reports/waves/w0-baseline.md), [journey](../../reports/adrl-implementation-journey.md),
[check/source evidence](../../reports/research/adrl-w0-baseline-2026-09-07.json),
[maturity inventory](../../reports/research/adrl-maturity-baseline-2026-09-07.json) and
[engineering runner](/Users/arunmenon/projects/adrl-core/tools/check_all.py).
All 556 implementation tests and eleven engineering checks pass for the recorded build. This is
scoped local evidence; prior decision wording, status and maturity remain unchanged.

## Context and rationale

FND-002 made rung membership a shared versioned config; RTG-008 added the gateway leak contract. The 2026-09-03 external review showed the remaining hole: the rung is a logical label, and nothing binds "local" to a host boundary. Substituting an external HTTPS endpoint for the local group passed every config check. This decision makes the inventory the single source for dispatch targets and adds the two attributes the label lacked, trust zone and geography, with a mechanical check that `local` means on this host.

## Adversarial review (2026-09-03)

### Steelman
A signed inventory with trust zones is the deployment analogue of the signed repository manifest (SAF-008): policy constrains identities that were asserted by someone accountable, not strings in a YAML file.

### Attacks
1. **The gateway can still route to whatever it likes.** Answered: the inventory generates the gateway config and OPS-006 records what the gateway reports; a served identity outside the inventory is a detected breach, and FND-002's contract makes it the gateway team's incident.
2. **Loopback is not proof of locality; a local port can tunnel anywhere.** Answered: the check is necessary, not sufficient; the trust zone assertion is signed by a human who is accountable for it, and the egress ledger records the deployment id so an audit can ask.
3. **Inventory versioning slows down adding a model.** Answered: on-host entries need no co-sign; only entries that send data off the host do, which is the point.

### Evidence
- ADRL-FND-002 (amended); rung membership as shared versioned config; fallback groups rung-closed; local-only for pinned traffic.
- ADRL-RTG-008 (amended); gateway leak contract: served identity reported, membership shared.
- ADRL-SAF-008 (Proposed); residency-tagged lineages served only by deployments with matching tags; the attribute this inventory must carry.
- 2026-09-03 external review of adrl-core, finding P0-1; external endpoint substituted for the local group passed all config checks.

### Verdict
**PROPOSED.** The missing object behind the review's first P0. Needs security and the gateway team as joint owners.

## Follow-ups

- [ ] Replace `gateway-endpoints.yaml` with a signed `endpoint-inventory-v1.json`; add trust zone, geography, data-use profile; verify signature at startup.
- [ ] CI check: `local` entries must be `on_host` with loopback `api_base`; substituting an external host fails the check (regression test for the review's experiment).
- [ ] Match served identity (OPS-006) against the inventory on every response; mismatch is an `infrastructure` event and an EVL-009 blocker.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-07 | Recorded W0 baseline, repeatable checks and explicit remaining gates | Prior decision wording and evidence preserved; no architecture or maturity change |
| 2026-09-03 | Proposed (first capture of the OPS bucket) | (none) |
