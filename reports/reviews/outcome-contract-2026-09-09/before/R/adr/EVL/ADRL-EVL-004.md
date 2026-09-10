# ADRL-EVL-004: Label quantity and quality gate for retrieval and learned authority

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture; referenced by MEM-002, MEM-004, MEM-008, LRN-001 since 2026-08-27) |
| Maturity | D1 Code; adrl-core `ledger/readiness.py` counts only `task_capability` at `closed_final` and reports diversity and excluded fractions; the threshold itself has not been pre-registered |
| Review verdict | PROPOSED (new) |
| Tenets | 4, 8, 9 |
| Related decisions | MEM-002, MEM-004, MEM-005, MEM-006, MEM-008, LRN-001, LRN-005, EVL-002, EVL-009 |
| Open questions | Q4, Q6 |

## Decision

Retrieval (MEM-008) and any learned component (LRN-003) gain advisory authority only when the evidence corpus passes a gate with four conditions, all pre-registered in `evl-config-v1.json` before being measured:

1. *Quantity.* At least `min_labels` outcomes typed `task_capability` at `closed_final` (MEM-002, MEM-004); the register's working figure is 300 and the overview records 34. Outcomes of any other type, and any outcome not at `closed_final`, are excluded from the count and reported separately.
2. *Quality.* Verifier precision (repeat-run agreement, flake rate, tree-drift rate per MEM-003) above the LRN-001 threshold on the same corpus; labels from unsandboxed or indeterminate runs never count.
3. *Representativeness.* At least `min_intents` distinct intent classes, `min_repos` distinct repositories and more than one user; the corpus's own non-claims (single-user, workflow-heavy) are reported as a condition on every figure.
4. *Suppressed fraction.* The share of traffic excluded from the corpus by privacy pin, suppression, degraded memory or subagent passthrough is reported next to the count; above `max_suppressed_fraction` the gate fails regardless of quantity.

## Context and rationale

Five decisions cite EVL-004 for a threshold it never stated. MEM-008 was approved because it "defers thresholds to EVL-004"; MEM-002 censors non-final outcomes for it; MEM-004 says only `task_capability` counts toward it; LRN-001 adds a diversity condition. This decision collects those obligations. The quantity figure is deliberately not fixed here: it is a pre-registered config field, because a threshold chosen after seeing the count is not a gate.

## Adversarial review (2026-09-03)

### Steelman
A count with a denominator, a precision condition and a representativeness condition is the smallest gate that cannot be passed by collecting more of the same easy task. It answers the MEM-008 attack that "300 evaluated decisions from a single user are 300 near-duplicates".

### Attacks
1. **Any fixed count is arbitrary.** Answered: the count is pre-registered and versioned; changing it is a new EVL config version with a recorded reason.
2. **Representativeness conditions can be gamed with a few token repositories.** Answered: `min_repos` counts repositories that each contribute at least a floor share of decisions.
3. **Verifier precision needs verified tasks to measure, which the corpus lacks.** Answered: that is a blocker (EVL-009), not a reason to lower the bar; the scorecard shows "precision unmeasured".
4. **Suppressed fraction is high by construction on a payments codebase.** Answered: then retrieval learns from an unrepresentative half of the world, which is exactly the MEM-008 attack; the gate should fail.

### Evidence
- ADRL-MEM-008; approved on the basis that thresholds live here.
- ADRL-MEM-002, ADRL-MEM-004; censoring and type restrictions this gate consumes.
- ADRL-LRN-001; minimum-diversity condition and verifier-precision demotion.
- `source/01-overview-tenets-taxonomy.md`; "Similar-task lookup has 34 evaluated decisions vs required 300"; "corpus is single-user, workflow-heavy".

### Verdict
**PROPOSED.** Long overdue; every consumer already behaves as if it existed. Needs an owner and pre-registered values.

## Follow-ups

- [ ] Pre-register `min_labels`, `min_intents`, `min_repos`, `max_suppressed_fraction` and the per-repository floor share in `evl-config-v1.json`.
- [ ] Golden test: readiness counts only `task_capability` at `closed_final`; a corpus with 300 labels from one repository fails the gate.
- [ ] Report the suppressed fraction on every retrieval metric in the scorecard (EVL-008).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
