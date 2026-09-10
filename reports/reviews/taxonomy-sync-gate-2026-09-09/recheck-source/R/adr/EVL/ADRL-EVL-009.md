# ADRL-EVL-009: Blockers are never averaged away

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture; referenced by the overview, MEM-006, MEM-010, LRN-006 since 2026-08-27) |
| Maturity | D1 Code; adrl-core `learning/readiness.py` and `ledger/readiness.py` list blockers by name and never fold them into a score; the blocker list itself is not yet pre-registered |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8, 9 |
| Related decisions | FND-005, MEM-006, MEM-010, LRN-006, SAF-001, SAF-002, SAF-003, SAF-007, EVL-004, EVL-007, EVL-008 |
| Open questions | Q6 |

## Decision

A blocker is a named condition that, while open, prevents a decision from moving up the maturity ladder (EVL-007) regardless of any score. Blockers are listed by name in every scorecard (EVL-008) and are never converted into a weight, a penalty or a component of the readiness score. The pre-registered blocker set is:

1. *Safety not attacked.* A SAF or TRU decision whose adversarial suite has not run in the window; blocks that decision above D2.
2. *Verifier precision unmeasured or below threshold* (LRN-001, EVL-004); blocks any learned or retrieval authority.
3. *Degraded memory non-zero in the window* (MEM-006); blocks the window's evidence from counting toward any gate.
4. *Erasure inside the window* (MEM-010); blocks the window.
5. *Abstention rate outside declared bounds* (LRN-006); blocks the artifact.
6. *Fail-open rate above threshold in any failure class* (FND-004, OPS-008); blocks any routing decision above D3.
7. *Excluded fraction above `max_suppressed_fraction`* (EVL-004); blocks retrieval and learned authority.
8. *Unanchored egress ledger* (SAF-009, OPS-007): no verified checkpoint in the window; blocks any SAF or TRU decision above D2.

Adding or removing a blocker is a new EVL config version with a recorded reason.

## Offline verifier improvement implementation, 2026-09-07

The verifier evaluator records explicit blockers for incomplete trials, input drift, repeat disagreement, changed evaluator files and execution/integrity failures. An unavailable sandbox, timeout or unavailable executor cannot earn an improvement recommendation. A deliberate test-environment error can retain its expected indeterminate classification. Each distinct case must match expectations on every repetition to count as correct.

A higher aggregate score cannot excuse a baseline-correct case becoming incorrect, a candidate false pass or a false failure. Focused tests exercise those failures, including an accept-everything candidate. This scoped blocker logic is implemented; the broader preregistered routing graduation blocker list remains separate.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## W0 execution baseline, 2026-09-07

The W0 engineering runner reports each failed, unavailable, timed-out or cancelled command rather than hiding it in an aggregate score. Stale contracts, missing ADR ownership/index coverage and changed declared inputs block a passing run. A killed runner may leave an incomplete running record. These engineering checks do not replace or edit the versioned routing graduation blocker set.

See the [W0 packet](../../reports/waves/w0-baseline.md), [journey](../../reports/adrl-implementation-journey.md),
[check/source evidence](../../reports/research/adrl-w0-baseline-2026-09-07.json),
[maturity inventory](../../reports/research/adrl-maturity-baseline-2026-09-07.json) and
[engineering runner](/Users/arunmenon/projects/adrl-core/tools/check_all.py).
All 556 implementation tests and eleven engineering checks pass for the recorded build. This is
scoped local evidence; prior decision wording, status and maturity remain unchanged.


## Taxonomy synchronization tooling, 2026-09-09

The checker reports named failures with nonzero exit status for missing ownership, stale evidence, incomplete review and invalid register mappings. These blockers cannot be offset by a passing test total. It also protects changed canonical fields and owning summary verdict/maturity cells with explicit human-record checks. This is a scoped application of measured engineering gates; it does not amend runtime graduation blockers or promote maturity. Global INDEX IDs and affected bucket coverage are checked; historical grade/other-bucket reconciliation remains unfinished. Code: [checker](../../tools/check_taxonomy_sync.py), [tests](../../tests/test_taxonomy_sync.py). 2026-09-09 <!-- taxonomy-sync:taxonomy-sync-gate:ADRL-EVL-009 --> [Evidence and limits](../../reports/reviews/taxonomy-sync-gate-2026-09-09/report.md).

## Context and rationale

The overview states the rule and names three blocking gates (organic verifier labels, label precision, learned-router authority); MEM-006, MEM-010 and LRN-006 each added a blocker of their own. The old readiness score of 40.5 was explicitly a comparable series that "never blends" blockers. This decision writes the blocker list down so that a score cannot quietly absorb one, which is the failure mode FND-005's review called self-graded gates.

## Adversarial review (2026-09-03)

### Steelman
A list of named conditions that a score cannot touch is the simplest possible guard against goal-seeking on the score. Every entry traces to a decision that already declared it.

### Attacks
1. **Eight blockers will keep everything at D2 forever.** Answered: that is the accurate state of a system with no organic traffic. Blockers close by doing the work they name, and each names it.
2. **"Adversarial suite has run" is satisfiable by a trivial suite.** Answered: the suite for each SAF decision is enumerated in that decision's follow-ups; the blocker names the enumerated suite, not "a suite".
3. **Blockers can be removed by a config version change.** Answered: recorded reason, reviewed at graduation, and the scorecard shows the config version so a removal is visible.

### Evidence
- `source/01-overview-tenets-taxonomy.md`; "Blockers never averaged away (EVL-009)"; the three blocking gates; the readiness series that never blends estimates.
- ADRL-MEM-006; degraded-memory count as an EVL-009 blocker when non-zero.
- ADRL-MEM-010; erasure removing evidence from a window is an EVL-009 blocker.
- ADRL-LRN-006; abstention rate collapse or saturation is an EVL-009 blocker.
- `REVIEW-LOG.md`, register-wide rules; "Tested, not attacked is a maturity ceiling for SAF."

### Verdict
**PROPOSED.** The rule was always in force by citation; this makes the list explicit and versioned.

## Follow-ups

- [ ] Pre-register the eight blockers and their thresholds in `evl-config-v1.json`.
- [ ] Golden test: the readiness score is unchanged when a blocker opens or closes; only the blocker list changes.
- [ ] Scorecard generator lists every open blocker with the decision IDs it holds at their current level.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-09 | <!-- taxonomy-sync:taxonomy-sync-gate:ADRL-EVL-009 --> [Local sync-gate evidence](../../reports/reviews/taxonomy-sync-gate-2026-09-09/report.md); no grade change | Prior decision wording and dated evidence preserved |
| 2026-09-07 | Recorded W0 baseline, repeatable checks and explicit remaining gates | Prior decision wording and evidence preserved; no architecture or maturity change |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |

