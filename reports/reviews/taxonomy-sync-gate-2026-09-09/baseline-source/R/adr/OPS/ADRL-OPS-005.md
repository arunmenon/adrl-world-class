# ADRL-OPS-005: Shadow-mode semantics per subsystem

| Field | Value |
|---|---|
| Bucket | OPS; Platform, Runtime, Operations |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D1 Code; adrl-core has independent modes for gates, routing and fallback, but gate observe mode still writes durable pins and triggers suppression before the mode is consulted (2026-09-03 external review, P1) |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8, 9 |
| Related decisions | FND-004, SAF-001, SAF-002, SAF-003, MEM-005, MEM-010, RTG-006, CAS-005, EVL-005, EVL-007 |
| Open questions | Q6 |

## Decision

Each subsystem has its own mode, and the modes have defined meanings:

| Subsystem | Modes | Meaning |
|---|---|---|
| Gates | `enforce`, `observe` | In `observe`, every gate runs and every finding is recorded, but findings are written to a *shadow* namespace (`shadow_finding`, `shadow_pin`) that carries no authority: no block is returned, no pin is written to the authoritative namespace, no suppression or erasure is triggered, and no egress destination is constrained. Promotion of a shadow finding to an authoritative pin requires a recorded decision (a versioned rule or a human action), never a mode switch. |
| Routing | `off`, `shadow`, `live` | `off` forwards unchanged and records nothing but classification; `shadow` computes and records every decision and forwards to the harness-requested model; `live` dispatches to the decided rung. Gate enforcement is independent of routing mode: with gates in `enforce`, a pinned lineage goes local in every routing mode. |
| Fallback | `off`, `shadow`, `live` | Per FND-004; `shadow` records the resolution it would have applied. |

Mode changes are configuration versions recorded in the egress ledger with actor and reason. Shadow-namespace records are excluded from every organic count (EVL-004) and reported in the scorecard's exclusions (EVL-008). A finding recorded in `observe` mode is never retroactively treated as having pinned the lineage.

## Context and rationale

The register's posture is gates enforced and routing in shadow, and adrl-core built that split. The 2026-09-03 external review found that gate observe mode was irreversible: findings wrote durable pins and shredded embeddings before the mode was checked, so an observation could become an enforcement pin later. Observation that has side effects is not observation. This decision separates the shadow and authoritative namespaces so that observe mode can be used on a new detector or a new repository class without changing anything a later enforce mode will read.

## Adversarial review (2026-09-03)

### Steelman
Two namespaces is the standard shadow-deployment pattern: the candidate writes where it cannot be read as authority. It also gives SAF-003 its precision measurement for free, since shadow findings on live traffic are the labelled corpus.

### Attacks
1. **A secret seen in observe mode and not pinned has already left the machine.** Answered: yes, and that is what observe mode means; the register's rule is that observe mode is used before a detector is trusted, on traffic whose policy already permits cloud. It is never a mode for restricted repositories (SAF-008).
2. **Two namespaces double the pin logic.** Answered: the namespace is a column on the same events; the reader checks one flag.
3. **Promotion by a "versioned rule" can be an automatic mass pin.** Answered: promotion applies going forward only; it never rewrites which requests were pinned when they were forwarded, and the egress ledger records the truth.

### Evidence
- ADRL-FND-004 (replacement); fallback modes off, shadow, live.
- ADRL-SAF-003 (amended); shadow findings for uncorroborated generic detections; precision measured on representative traffic.
- ADRL-SAF-002 (amended); one-way pin; releases only by audited human action; the authority that observe mode must not exercise.
- 2026-09-03 external review of adrl-core, finding P1-6; observe mode writes durable pins and triggers erasure.

### Verdict
**PROPOSED.** Defines what every mode flag in the system means. Needs an owner.

## Follow-ups

- [ ] adrl-core: check `GateMode` before pin write and suppression; write shadow findings to a shadow namespace; golden test that observe mode leaves the authoritative pin state unchanged.
- [ ] Mode changes recorded in the egress ledger with actor and reason.
- [ ] Scorecard exclusions section counts shadow-namespace findings separately.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the OPS bucket) | (none) |
