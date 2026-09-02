# ADRL-LRN-006 — Abstention with a declared risk-coverage target

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D0 Design, review recommends D0 Design — nothing built; the amendment adds that the abstention gate should reach D2 *before* the estimator (LRN-003) is trained, which the register itself suggests |
| Review verdict | AMEND |
| Tenets | 2, 4, 9 |
| Related decisions | SAF-001, RTG (ambiguous band), LRN-003, LRN-005, LRN-007, MEM-006, EVL-004, EVL-006, EVL-009 |
| Open questions | Q4 |

## Decision

Uncertain or out-of-distribution predictions abstain to the deterministic safe policy, where "uncertain" and "out-of-distribution" are defined per artifact by a calibrated selective-prediction rule with a declared target risk and measured coverage on a time-ordered T1 holdout, an OOD detector on the pre-decision feature vector, and a hard floor: the learned component may act only inside the RTG ambiguous band, and its abstention rate is a reported metric whose collapse toward 0% or rise toward 100% is itself an EVL-009 blocker.

1. **Selective prediction, not a confidence cutoff.** Each artifact (LRN-005) ships a selection function and the (risk, coverage) point it was validated at — e.g. "accept when the calibrated error probability on the routing effect is below α; measured coverage 55% on holdout H, risk 4%". The threshold is chosen for a target risk, and coverage is what falls out, never the reverse.
2. **OOD is feature-space, not outcome-space.** The OOD detector operates on the decision-time feature snapshot (LRN-004): repo, intent class, context size, embedding distance to training support, harness. A turn outside training support abstains regardless of the estimator's confidence.
3. **The safe policy is the deterministic policy, and it is not an oracle.** Abstention hands the decision to the current heuristic rung choice with escalation armed; learning-to-defer results show that the combined system is only better than either component if the deferral rule accounts for the deferred-to policy's own error, so the risk target is set on *system* outcome, not on the estimator's accuracy alone.
4. **Abstention before estimation.** The abstention gate, its calibration harness and its telemetry are built and tested (D2) with a trivial estimator before LRN-003 is trained; a learned component without a working abstention path cannot hold advisory status, let alone authority.

## Context and rationale

The model must be allowed to say "I don't know". On a request unlike anything in training, or with low confidence, the estimator abstains and the deterministic policy decides. Until abstention exists no learned component should hold authority — and this bucket is D0 precisely because the safety property that justifies a learned router does not yet exist.

The amendment replaces two undefined words ("uncertain", "out-of-distribution") with the selective-prediction vocabulary that gives them meaning: a target risk, a measured coverage, a calibration set, and an OOD detector on the features the router actually sees. It also fixes the ordering the register asks about: build abstention first. An abstention gate is a small, testable component that does not need pairs or an estimator to reach D2 — it needs a calibration harness, an OOD detector and telemetry. Building it first means that when the estimator arrives it is born inside a cage, and that EVL can measure the cage before anything is in it.

## Adversarial review (2026-09-02)

### Steelman
Abstention is what makes Tenet 4 ("the learned system advises; it is not the safety authority") operational: a model that cannot decline is either always trusted or never used. Deferring to the deterministic policy is the correct fallback because that policy already has shadow-grade evidence and because it keeps the learned component out of clear cases. Selective classification with guaranteed risk is a mature technique.

### Attacks
1. **"Uncertain" and "out-of-distribution" are undefined, so the decision is unfalsifiable.** No threshold, no calibration set, no detector, no metric. Two implementations that abstain 1% and 99% of the time both satisfy the text. The register concedes "calibration and abstention thresholds undefined pending data" — but the *form* of the definition (target risk → coverage, on a T1 time-ordered holdout) can and should be fixed now.
2. **Confidence cutoffs on the estimator are the wrong instrument for OOD.** A CATE estimator (LRN-003) extrapolates smoothly outside its support and can be very confident there. OOD must be detected in feature space — distance to training support on the decision-time snapshot — not read off the estimator's output. Selective-prediction methods provide risk guarantees only under exchangeability of calibration and test data, which OOD turns violate; hence a separate detector.
3. **The safe policy is not an oracle, and the decision treats it as one.** Deferring is only beneficial where the deferred-to policy is better. The deterministic policy is exactly the thing the estimator is supposed to improve on in the ambiguous band; if abstention is too aggressive, the system reverts to the heuristic and pays the estimator's cost for nothing; if too lax, it acts where it should not. The learning-to-defer literature makes the deferred-to expert's error part of the objective; the risk target must be a system target.
4. **Coverage collapse is invisible.** An artifact that abstains on 98% of turns is "safe" and useless; one that abstains on 0.5% after drift is dangerous. Neither is detected unless the abstention rate is a first-class reported metric with bounds. The decision must make it one.
5. **Abstention interacts with degraded memory and privacy.** MEM-006's degraded mode already forces the deterministic policy; MEM-005's suppressed embeddings make private turns look OOD to any embedding-distance detector. The first is consistent (same fallback), the second is a feature: private turns *should* abstain. But both must be counted separately in the abstention metric or drift analysis will be confounded. Rationale and follow-up.
6. **Ordering.** Building the estimator first (the natural engineering order) means the first evaluated artifact has no cage; EVL would be measuring an uncaged advisory. The register itself asks whether abstention should come first. Yes — and the decision should say so, because it is the cheapest D2 in the bucket.

### Evidence
- Y. Geifman, R. El-Yaniv, "Selective Classification for Deep Neural Networks" (NeurIPS 2017; arXiv 1705.08500) — choose a selection threshold for a desired risk with high-probability guarantee; e.g. 2% top-5 error on ImageNet at ~60% coverage with 99.9% confidence; the risk→coverage form clause 1 adopts (attacks 1, 4) — https://arxiv.org/abs/1705.08500v2
- H. Mozannar, D. Sontag, "Consistent Estimators for Learning to Defer to an Expert" (ICML 2020; arXiv 2006.01862) — consistent surrogate loss for jointly learning to predict or defer, where the expert's (here: deterministic policy's) own accuracy enters the objective; attack 3 — https://arxiv.org/abs/2006.01862
- (authors not captured) "A Linear Expectation Constraint for Selective Prediction and Routing with False-Discovery Control" (arXiv 2512.01556, 2025) — finite-sample FDR control among accepted predictions using only a calibration set of uncertainty scores and binary error labels under exchangeability; a concrete recipe for clause 1 and a statement of the exchangeability assumption clause 2 guards (attacks 1, 2) — https://arxiv.org/html/2512.01556v2
- (authors not captured) "UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing" (arXiv 2605.18796, 2026) — isotonic calibration of small-model error probability, threshold chosen by cost-minimisation under an accuracy constraint; 31% cost cut at fixed F1; needed ~22.5k calibration and ~15k validation queries; shows both the mechanism and the data appetite (attacks 1, 4) — https://arxiv.org/html/2605.18796
- D. Madras, T. Pitassi, R. Zemel, "Predict Responsibly: Improving Fairness and Accuracy by Learning to Defer" (NeurIPS 2018) — named in the review brief; not fetched in this review, so not relied on; listed for the caller's follow-up only — no URL recorded.

### Verdict
**AMEND.** Attack 1 is decisive: an abstention rule with no definable threshold, coverage or metric cannot be tested, and D0 will never become D2. Attacks 2–4 supply the definition: feature-space OOD detector, system-level risk target that includes the fallback policy's error, and abstention rate as a bounded, reported metric. Attack 6 answers the register's ordering question and is written into the decision (clause 4). Attack 5 is a rationale note and telemetry follow-up. The decision's spirit — the model may say "I don't know" and the deterministic policy decides — is unchanged.

## Amendments applied

- Defined "uncertain" as a calibrated selective-prediction rule with a declared target risk and measured coverage on a time-ordered T1 holdout (clause 1).
- Defined "out-of-distribution" as a feature-space detector on the decision-time snapshot (clause 2).
- Added the hard floor: learned component acts only inside the ambiguous band; abstention rate is a reported metric with EVL-009 blocker bounds.
- Added that the risk target is a system outcome including the deterministic policy's own error (clause 3).
- Added ordering: abstention gate reaches D2 before the estimator is trained (clause 4).

## Follow-ups

- [ ] Build the abstention gate with a stub estimator: selection function interface, isotonic/conformal calibration harness on T1 holdout, feature-space OOD detector (e.g. kNN distance on the LRN-004 snapshot), telemetry for abstain/act with reason codes (uncertain / OOD / degraded-memory / privacy-suppressed).
- [ ] Golden tests: OOD turn (unseen repo/intent) abstains even with estimator confidence 0.99; abstention rate outside declared bounds raises an EVL-009 blocker; degraded memory (MEM-006) records `reason=degraded`, not `reason=uncertain`.
- [ ] Publish the initial target risk (proposal: routing-effect error ≤ 5% among accepted turns) and expected coverage from the first calibration run; revise with data.
- [ ] Add abstention rate by reason code to the EVL pack from the first shadow run of any artifact.
- [ ] Fetch and assess Madras et al. 2018 before citing it in the EVL pack.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: uncertain/OOD defined via selective prediction with target risk and feature-space OOD; abstention rate reported and bounded; abstention built before estimator | "Uncertain or out-of-distribution predictions abstain to the deterministic safe policy." |
