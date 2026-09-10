# ADRL-EVL-001: Baseline set: four fixed comparators, two price bases

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D0 Design; the overview records "a best-single-model cost baseline exists" (Phase 0), but no baseline set is defined as a versioned artifact; the adrl-core build carries price vectors but computes no baseline comparison |
| Review verdict | PROPOSED (new) |
| Tenets | 3, 8, 9 |
| Related decisions | RTG-002, RTG-005, RTG-007, RTG-009, LRN-003, EVL-002, EVL-006, EVL-008 |
| Open questions | Q4, Q6 |

## Decision

Every evaluation of a routing policy, heuristic or learned artifact reports against the same four comparators on the same evaluation window: always-local, always-frontier, the current deterministic heuristic (RTG-002 at its recorded policy version), and the best single cloud model repriced over the whole window. Each comparator is reported at two price bases, after cache effects and at list price (RTG-009), and the two are never mixed in one figure. The baseline set is a versioned artifact (`baselines-v<N>`) naming the window, the comparators, the price vectors and the verifier version; an evaluation that does not cite a baseline version is not an evaluation.

1. *Always-local* and *always-frontier* are the two bounds of the rung order; a policy that does not beat both on the objective (RTG-005) has not earned any exposure.
2. *Current heuristic* is the policy actually serving shadow traffic; it is the comparator a learned artifact must beat to leave D2 (RTG-007 pre-build gate).
3. *Best single model* is the Phase 0 baseline generalised: the cheapest single model that would have produced the same verified outcomes over the window, repriced with the window's cache statistics.
4. Quality in every comparison is verified quality only (MEM-003, LRN-001 tier 1); proxy quality is reported separately and labelled.

## Context and rationale

The register's Q6 asks what evidence would justify live routing. The honest answer starts with a fixed comparator set, because a router can always look good against a baseline chosen after the fact. RTG-005 already names the objective and RTG-009 the cost unit; this decision fixes who the objective is compared against. The four comparators are the ones the review used implicitly when it said a learned router must beat "always-local, always-frontier and the current heuristic after cache effects" (RTG-007). Best single model is added because it is the comparator a buyer will ask about first and because the Phase 0 corpus already computed it.

## Adversarial review (2026-09-03)

### Steelman
Fixed comparators with a version and a window are the minimum that makes two evaluations comparable, and the cache-versus-list split is the one number the review found the register lacked. Nothing here is expensive: all four comparators are computable from the ledger and the price vectors.

### Attacks
1. **Always-frontier is not a single policy.** With three frontier deployments and adaptive thinking, "always-frontier" has several costs. Answered: the comparator names a deployment and an effort setting per window in the baseline artifact; a change is a new baseline version.
2. **Best single model repriced over the window ignores that the model would have produced different transcripts.** A cheaper model does not produce the same trajectory (the register's own Replay Gap citation). Answered: the comparator is labelled as a repricing bound, not a counterfactual, and EVL-003 forbids treating it as one.
3. **Cache effects depend on the policy under test.** A policy that switches rungs pays cache-write costs the baselines never pay, so "after cache effects" penalises switching. Answered: that is the point; RTG-009 charges the switch because the provider does.
4. **Four comparators on a small window produce four noisy numbers.** Answered: EVL-002 requires confidence intervals and a declared minimum window; a comparison without an interval is reported as "insufficient window".

### Evidence
- Register: `source/01-overview-tenets-taxonomy.md`; "a best-single-model cost baseline exists" (Phase 0 findings); this decision generalises it.
- ADRL-RTG-009 (Proposed); cost unit and the after-cache versus list-price labelling rule reused here.
- ADRL-RTG-007; pre-build gate names always-local, always-frontier and the current heuristic as the comparators; this decision makes them a versioned artifact.
- A. Gonuguntla, "The Replay Gap" (arXiv 2608.08239, 2026), as cited in ADRL-MEM-009; repricing a logged trajectory is a bound, not a counterfactual (attack 2).

### Verdict
**PROPOSED.** The bucket cannot answer Q6 without a fixed comparator set. Needs an owner and a first baseline version computed on the shadow corpus before any RTG-007 gate is evaluated.

## Follow-ups

- [ ] Write `baselines-v1.json` (window, four comparators with deployment and effort, price vectors version, verifier version) next to `readiness-score-v1.json`.
- [ ] Compute the four comparators on the existing shadow corpus and publish both price bases in the first EVL scorecard (EVL-008).
- [ ] CI check: any evaluation report that lacks `baseline_version` is rejected.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
