# ADRL-LRN-001 — Evidence tiers, not "outrank"

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D1 Code — `learning_contract.py` encodes the preference and is unit-tested, but with one strongly-verified task the tier-1 set is a single task, so the contract has never been exercised on a real training set |
| Review verdict | AMEND |
| Tenets | 8, 9 |
| Related decisions | MEM-002, MEM-003, MEM-004, LRN-002, LRN-003, LRN-004, EVL-004, EVL-005, EVL-009 |
| Open questions | Q6 |

## Decision

Training data is stratified into evidence tiers and only tier-1 labels — deterministically verified, cause-typed `task_capability`, `closed_final` — enter the estimator's objective; lower tiers (verified-but-not-final, proxy/heuristic, simulator) may be used only as declared weak or unlabeled signal with the tier recorded on every example, never pooled into tier-1, and the verifier's own precision is measured and reported as a condition of tier-1 status.

1. **Tiers.** T1: verified (MEM-003, non-indeterminate, no tree drift) + `task_capability`-typed (MEM-004) + `closed_final` (MEM-002) + organic (EVL-005). T2: verified but `closed_turn` only (censored). T3: proxy (no error, harness reported success) organic. T4: simulator/benchmark. T5: counterfactual pairs are tagged with their own tier (LRN-002) and never mixed with organic tiers (Tenet 8).
2. **Weak signal is allowed, pooling is not.** T2–T4 may be used for pre-training, pseudo-labelling under confident-learning-style noise estimation, or feature learning, provided the training manifest (LRN-005) lists the tier mix and the evaluation holdout is T1-only.
3. **The verifier is audited.** T1 status requires a measured verifier precision (repeat-run agreement, flake rate, tree-drift rate per MEM-003) above a threshold set by EVL; a verifier below threshold demotes its labels to T2.

## Session verification implementation, 2026-09-07

New session verification receipts have origin=pilot and eligible_for_learning=false. They create no route, internal outcome or derived learning label and are not consumed by label producers. A passed check on one task cannot be treated as a calibrated tier-1 corpus. Repeat checks and human disagreement analysis must precede any proposal to admit this evidence; existing route-based evidence-tier rules retain their current semantics.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Context and rationale

A small number of trustworthy labels beats a large number of plausible ones. Proxy signals — "the turn did not error, so call it a success" — are abundant and quietly wrong in exactly the direction that flatters the cheap rung; verified, cause-clean labels are scarce and honest. Fewer, better labels is the right instinct and the register's own blocking gates (organic verifier labels, label precision) already depend on it.

The amendment replaces "outrank" — which has no operational meaning — with tiers and rules. Two things forced this. First, "verified" is not ground truth: tests are flaky, benchmark curation found most "verified" coding tasks had invalid tests before review, and this system has one task with strong verification, so the verified set is currently a single task and any model trained on it is a single-task model. Second, the register's real problem is volume, and the literature offers a legitimate way to use noisy labels without pretending they are clean: keep them in a separate tier, estimate their noise, and never let them into the holdout. "Outrank" would have allowed a rank-weighted pool; tiers forbid pooling and make the mix auditable.

## Adversarial review (2026-09-02)

### Steelman
Everything downstream (LRN-003's estimator, EVL's readiness claims) is only as good as the labels, and the failure mode — proxies flattering the cheap rung — is systematic, not random, so more proxy data makes the bias worse rather than averaging it out. Preferring verified, cause-clean labels is the only defensible default and is consistent with MEM-003/004.

### Attacks
1. **"Outrank" has no operational meaning.** Does a verified label get weight 1.0 and a proxy 0.3? Are proxies excluded when any verified label exists for the same task class? Is the holdout allowed to contain proxies? Each reading yields a different estimator and a different readiness number. The decision as written cannot be implemented two ways that agree.
2. **Verified labels are not clean; the verifier is an instrument with its own error.** Flaky tests are common and mostly present from the moment the test is written; curated benchmarks found 68% of "verified" coding tasks had severe test or environment problems before human review. With one strongly-verified task, the entire T1 corpus depends on one test suite whose flake rate has not been measured. The decision must condition tier-1 status on verifier precision or "verified" is a label, not a fact.
3. **Single-task tier 1 is a degenerate training set.** A model trained on one task's verified outcomes learns that task. The decision is silent on minimum diversity for tier-1; EVL-004's 300-count does not fix this if all 300 are the same workflow (Q6: representativeness is binding). The maturity claim D2 for a contract that has never been applied to a multi-task set is generous.
4. **The decision throws away legitimate weak signal.** Confident learning and related methods can estimate label noise and use noisy labels safely if their noise structure is modelled and they are kept out of evaluation. "Outrank" neither permits this cleanly nor forbids it. Given the volume problem, a rule that allows tiered weak signal with a T1-only holdout is strictly more useful than a rank.
5. **Cause-clean depends on MEM-004, which was incomplete.** Until MEM-004's amendment (six/seven types, provenance, `unverifiable` default) lands, "cause-clean" labels in the current code may include `user_abort` and `unverifiable` outcomes typed as capability failures. LRN-001 inherits that error and must reference the amended typing explicitly.
6. **Simulator vs organic.** EVL-005 says simulator evidence is not organic evidence; the decision does not say which tier simulator-verified outcomes fall in. A simulator can produce thousands of "verified, cause-clean" labels that would satisfy the original wording. They must be a separate tier.

### Evidence
- Q. Luo et al., "An Empirical Analysis of Flaky Tests" (FSE 2014) — 201 flaky-test fixes, 77% from async wait, concurrency and order dependency; 78% flaky from creation; attack 2 — https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf
- OpenAI, "Introducing SWE-bench Verified" (2024) — 68.3% of samples had a severe issue after review by 93 developers; GPT-4o 33.2% vs 16% on verified vs original; "the tests" are not automatically ground truth (attack 2) — https://openai.com/index/introducing-swe-bench-verified/
- C. Northcutt, L. Jiang, I. Chuang, "Confident Learning: Estimating Uncertainty in Dataset Labels" (JAIR 2021) — estimates the noisy/true label joint and prunes; the mechanism clause 2 permits for T2–T4 (attack 4) — https://arxiv.org/abs/1911.00068
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize ML Benchmarks" (NeurIPS 2021) — ≥3.3% test-set error changes model rankings; motivates a T1-only holdout (attacks 2, 4) — https://arxiv.org/abs/2103.14749
- E. Breck et al., "The ML Test Score" (2017) — "Offline proxy metrics correlate with actual online impact metrics" and "Model quality is validated before serving" as required tests; a proxy tier must be validated against T1, not assumed (attack 1) — https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
- O. Chapelle, "Modeling delayed feedback in display advertising" (KDD 2014) — not-yet-final outcomes are unlabeled, not negative; basis for T2 as censored (attack 1, tier definition) — https://dl.acm.org/doi/10.1145/2623330.2623634

### Verdict
**AMEND.** Attack 1 alone requires a rewrite: an unimplementable preference is not a decision. Attacks 2, 3 and 6 show that "verified" and "cause-clean" both need conditions attached (verifier precision, diversity, organic-only) to mean what the decision wants them to mean. Attack 4 shows the rewrite should permit tiered weak signal rather than an implicit ban, because volume is the bucket's binding problem. Attack 5 is a cross-reference to the amended MEM-004. The spirit — fewer, better labels — is preserved and made checkable.

## Amendments applied

- "outrank" replaced by explicit tiers T1–T5 with T1-only objective and T1-only holdout.
- Added: lower tiers permitted as declared weak/unlabeled signal with the tier recorded per example and listed in the LRN-005 manifest; pooling forbidden.
- Added: verifier precision measured and required for T1 status (clause 3).
- Added: simulator and counterfactual data are separate tiers (Tenet 8, EVL-005, LRN-002).
- Cross-referenced amended MEM-002 (censoring), MEM-003 (indeterminate/tree drift) and MEM-004 (typing) as tier-1 conditions.

## Follow-ups

- [ ] Encode tiers in `learning_contract.py` / `learning-contract-v1.json`; golden test that a training manifest with T3 examples in the holdout is rejected.
- [ ] Golden test: an outcome with `closed_turn` only, or verifier `indeterminate`, or `tree_drift=true`, or type ≠ `task_capability`, cannot be T1.
- [ ] Measure the flake rate of the one strongly-verified task's suite (run ×10); record it as the first verifier-precision number; set the T1 threshold in EVL.
- [ ] Add a minimum-diversity condition to `learning_readiness.py` (distinct intent classes and repos in T1) and report it alongside the 300-count.
- [ ] Re-derive the "34/300 evaluated decisions" figure by tier and publish the tier histogram in the EVL pack.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: "outrank" replaced by evidence tiers with T1-only objective/holdout, verifier-precision condition, and permitted weak-signal use | "Verified, cause-clean outcomes outrank heuristic proxy labels for training." |
