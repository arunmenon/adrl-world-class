# ADRL-EVL-002: Holdout and calibration protocol: temporal, session-grouped, tier-1 only

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D1 Code; adrl-core `learning/dataset.py` implements temporal session-grouped splits and rejects random K-fold, and `learning/abstention.py` measures calibration on a time-ordered holdout; no protocol document or scorecard exists |
| Review verdict | PROPOSED (new) |
| Tenets | 8, 9 |
| Related decisions | LRN-001, LRN-004, LRN-006, MEM-002, EVL-001, EVL-004, EVL-006 |
| Open questions | Q4, Q6 |

## Decision

Every reported metric for a routing artifact is computed on a holdout that is later in time than all training data, grouped so that no session spans training and holdout, and restricted to tier-1 evidence (LRN-001) at `closed_final` (MEM-002). Calibration is reported as reliability (expected calibration error and a reliability diagram) for each pairwise effect the artifact outputs (LRN-003), and abstention coverage and realised risk are reported alongside (LRN-006). Every metric carries a confidence interval from session-level bootstrap and the number of sessions and decisions in its denominator. A window smaller than the declared minimum (`min_holdout_sessions` in the EVL config) reports "insufficient" instead of a point estimate.

## Context and rationale

LRN-004 forbids random K-fold and requires temporal splits; LRN-001 restricts the objective to tier 1; LRN-006 defines abstention on a time-ordered holdout. This decision is where those three rules meet the scorecard: it says what a number reported to a graduation meeting must have been computed on. The session-grouped bootstrap is chosen because decisions within a session are not independent (continuations inherit the route), so per-decision intervals would be too narrow.

## Adversarial review (2026-09-03)

### Steelman
Temporal, grouped, tier-1 holdouts are the standard defence against the two leaks the review found most likely: features that encode the future (LRN-004) and labels that are not yet final (MEM-002). Reporting the denominator with every number implements the review's register-wide rule.

### Attacks
1. **Tier-1-only holdouts will be tiny for a long time.** The overview records one verified task and 34 evaluated decisions. Answered: that is the truth the scorecard must show; "insufficient" is a valid result, and EVL-009 forbids averaging it away.
2. **A temporal holdout confounds policy change with drift.** If the harness or the models changed inside the window, the holdout measures the change. Answered: the window names harness and model versions (OPS-003 inventory); a version change inside a window splits the window.
3. **Session-level bootstrap under-counts when one session dominates.** Answered: the scorecard reports the largest session's share of decisions; above a declared share the window is flagged.

### Evidence
- ADRL-LRN-004; temporal splits, session grouping, deny-list; this decision applies them to reporting.
- ADRL-LRN-001; tier definitions; T1-only objective and holdout.
- ADRL-LRN-006; selective prediction on a time-ordered holdout; coverage and risk reporting.
- C. Northcutt et al., "Pervasive Label Errors in Test Sets" (NeurIPS 2021), as cited in ADRL-MEM-009; label error at the few-percent level reverses rankings; motivates tier-1-only holdouts.

### Verdict
**PROPOSED.** Needs an owner and the EVL config fields (`min_holdout_sessions`, dominant-session share) pre-registered before the first scorecard.

## Follow-ups

- [ ] Add `evl-config-v1.json` with `min_holdout_sessions`, dominant-session share threshold, bootstrap resamples and the calibration bin count.
- [ ] Golden test: a metric computed on a holdout containing a session also present in training is rejected.
- [ ] Publish the first reliability diagram for the stub estimator (LRN-006) even though it is a constant, to exercise the pipeline.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
