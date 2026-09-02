# ADRL-LRN-003 — The target is a CATE, name it

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D0 Design, review recommends D0 Design — nothing is built and the amended text does not change that |
| Review verdict | AMEND |
| Tenets | 3, 4, 9 |
| Related decisions | RTG (utility/cost objective), LRN-001, LRN-002, LRN-004, LRN-006, LRN-007, LRN-008 (proposed), MEM-004, EVL-004, EVL-006 |
| Open questions | Q4 |

## Decision

Train a calibrated estimator of the conditional effect of rung choice on verified outcome and cost — the conditional average treatment effect (CATE) of frontier over cheaper rungs given pre-decision features — using paired and logged-exploration data (LRN-002, LRN-008) as the label source; never train on the deterministic policy's own routing decisions as targets, and never deploy a model whose output is a rung rather than a calibrated effect estimate with an uncertainty.

1. **Estimand.** τ(x) = E[Y(frontier) − Y(cheaper) | x] where Y is the verified T1 outcome (LRN-001) and x is the pre-decision feature vector (LRN-004); with three rungs, two pairwise effects (frontier vs cheap_cloud, cheap_cloud vs local) are estimated, not one.
2. **Estimator family.** Meta-learners (T-, X- or DR-learner) over the existing feature set are the default; the X-learner is preferred while pair volume is small and treatment groups unbalanced. A single-model S-learner is acceptable only as a baseline, because it tends to regularise the treatment effect toward zero.
3. **Cost enters the decision, not the label.** The estimator predicts τ(x) and its uncertainty; RTG combines τ(x) with post-cache marginal cost to choose a rung. The estimator does not output a rung.
4. **Outcome-preference data is a valid label source.** Pairwise "which arm's verified outcome was better" labels (as in preference-trained routers) are consistent with the estimand; what is prohibited is the heuristic's *decision* as a label.

## Context and rationale

Do not build a model that imitates the rules you already have. Supervised learning on past routing decisions clones today's heuristics, with their blind spots, and can never discover that the local rung would have succeeded on a class of tasks the heuristic always sends to frontier. The target instead is: for this specific task, how much does frontier actually improve the outcome, and is that worth its cost?

The amendment names that quantity. It is a conditional average treatment effect — treatment = rung, outcome = verified success, conditioning = pre-decision features — and the uplift/CATE literature supplies estimators, their failure modes, and the reason a naive "classifier" framing goes wrong (a single model with rung as a feature shrinks the effect it is supposed to estimate). Naming it also resolves a false dichotomy in the original: preference-trained routers such as RouteLLM are "classifiers", but they are trained on outcome comparisons between the two arms, not on anyone's routing rule, and they generalise to unseen model pairs — so they are not the imitation the decision warns against. The line that matters is not classifier vs estimator; it is *label = heuristic decision* (forbidden) vs *label = comparative outcome* (required).

## Adversarial review (2026-09-02)

### Steelman
Behaviour cloning of a heuristic is a known trap: it reproduces the heuristic's mistakes with a learned model's opacity and can never route where the heuristic never went. A utility (marginal gain) target is the only formulation that lets the learned component earn savings in the ambiguous band rather than re-encode the rules. Keeping it D0 until data exists is honest.

### Attacks
1. **The register never names the estimand, so the decision cannot be evaluated.** "Marginal utility of frontier" is a conditional average treatment effect. Not saying so leaves open how it is estimated, what "calibrated" means for a difference of two probabilities, how cost enters, and whether three rungs means one effect or two. The uplift literature has a settled vocabulary and known pitfalls (S-learner shrinkage, X-learner for unbalanced arms, DR-learner for logged data); the decision should use it.
2. **The classifier-vs-estimator dichotomy is false, and RouteLLM is the counterexample.** RouteLLM trains routers (including a BERT classifier and a causal-LLM classifier) on human preference data between a strong and a weak model, reports >2× cost reduction at held quality, and shows transfer when the model pair changes. Those are classifiers trained on *comparative outcomes*, which is exactly a discretised CATE, and they do not imitate any heuristic. Hybrid LLM likewise trains a router on the predicted quality gap between small and large models. The decision's premise — "a classifier imitates current heuristic routes" — conflates the model class with the label source. The prohibition must be re-aimed at the label.
3. **"Marginal frontier gain" ignores the cheap-cloud rung.** ADRL has three rungs. One effect (frontier vs "not frontier") cannot decide between local and cheap_cloud. Either two pairwise effects or a per-rung outcome model are needed, with a consistent way to combine them; the decision is silent.
4. **Calibration of an effect is not calibration of a probability.** τ(x) is a difference of two conditional probabilities; standard calibration (isotonic, Platt) applies to each arm's outcome probability, not directly to the difference, and abstention (LRN-006) needs an uncertainty on τ, not on Y. The decision says "calibrated" without saying of what.
5. **Is the ambiguous band big enough to repay this?** Q4 and the register both say deterministic rules own most decisions and the learned band is a minority. A CATE estimator needs pairs *from that band* (LRN-002 power: ~100–250 per slice). If the band is, say, 15% of turns and pairs cost a frontier call each, the estimator's data cost could exceed the savings it is meant to unlock. The decision should require RTG to publish the band size and the savings ceiling before the estimator is funded. Not a text change here; a gate in EVL/RTG.
6. **Without exploration, the estimator is a direct-method OPE on a deterministic log.** All organic labels come from the rung the heuristic chose; the estimator will extrapolate τ(x) into regions where it has never seen the counterfactual arm. Pairs (LRN-002) fix this only inside the band and only at pair scale; LRN-008's exploration channel is the other half. The decision should cite both as its label sources rather than leaving the data question implicit.

### Evidence
- S. Künzel, J. Sekhon, P. Bickel, B. Yu, "Metalearners for estimating heterogeneous treatment effects using machine learning" (PNAS 2019; arXiv 1706.03461) — defines the CATE and the S/T/X meta-learners; X-learner is efficient when treatment groups are unbalanced and can reach parametric rates when the CATE is smoother than the response surfaces; no meta-learner is uniformly best; attacks 1, 2 (clause 2) — https://arxiv.org/abs/1706.03461
- I. Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data" (arXiv 2406.18665, 2024) — routers trained on human preference data with data augmentation; >2× cost reduction in some cases without quality loss; transfer when strong/weak models change at test time; the counterexample to the classifier-imitates-heuristic premise (attack 2) — https://arxiv.org/abs/2406.18665
- D. Ding et al., "Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing" (ICLR 2024; arXiv 2404.14618) — router assigns queries by predicted difficulty and a desired quality level; up to 40% fewer large-model calls with no quality drop; a quality-gap target, i.e. an effect, not an imitation (attack 2) — https://arxiv.org/abs/2404.14618
- M. Dudík, J. Langford, L. Li, "Doubly Robust Policy Evaluation and Learning" (ICML 2011) — with only a reward model, evaluation is the direct method and carries its bias; the DR-learner family for CATE inherits the same structure (attack 6) — https://www.arxiv.org/abs/1103.4601
- A. Gonuguntla (CMU), "The Replay Gap" (arXiv 2608.08239, 2026) — explicitly calls for off-policy estimators (IS, DR) validated against branched ground truth for agentic routing; supports pairing the CATE estimator with LRN-002 branches and LRN-008 exploration (attack 6) — https://arxiv.org/html/2608.08239
- (authors not captured) "UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing" (arXiv 2605.18796, 2026) — isotonic-calibrated error probability of the small model plus a cost-optimised threshold; 31% cost cut at fixed F1 on 75k NER queries; needed ~22.5k calibration and ~15k validation queries with both models' outputs — an order-of-magnitude reference for what "calibrated" costs in data (attacks 4, 5) — https://arxiv.org/html/2605.18796

### Verdict
**AMEND.** Attack 1 is the core finding: the register's crux decision never names its estimand, and naming it (CATE) immediately supplies estimator choices, pitfalls, and the correct reading of "calibrated". Attack 2 lands: the original's dichotomy is false and RouteLLM/Hybrid LLM are counterexamples, so the prohibition is re-aimed at the label source (heuristic decisions) rather than the model class. Attacks 3 and 4 are fixed by clauses 1 and 3. Attacks 5 and 6 are gates and cross-references (RTG/EVL, LRN-002, LRN-008). The spirit — do not clone the heuristic; estimate what frontier buys — is preserved and made precise. Maturity remains D0.

## Amendments applied

- Named the estimand as a CATE with explicit treatment, outcome and conditioning set; two pairwise effects for three rungs (clause 1).
- Named the default estimator family and the S-learner shrinkage caveat (clause 2).
- Separated cost (RTG decision input) from the label; estimator outputs an effect with uncertainty, never a rung (clause 3).
- Re-aimed the prohibition: forbidden label = the heuristic's decision; permitted label = comparative verified outcome, including pairwise preference (clause 4).
- Cited LRN-002 and LRN-008 as the label sources.

## Follow-ups

- [ ] RTG/EVL: publish the ambiguous-band share of turns and the savings ceiling if the estimator were perfect (oracle router on current pairs); this is the go/no-go for funding LRN-003 (Q4).
- [ ] Write the estimator spec: features (LRN-004 manifest), meta-learner choice, per-arm calibration method, uncertainty method for τ(x) (bootstrap or conformal), and the abstention interface to LRN-006.
- [ ] Golden test on synthetic data: an S-learner and an X-learner on a known τ(x); confirm the S-learner's shrinkage and the X-learner's recovery before touching real pairs.
- [ ] Baseline: a RouteLLM-style pairwise preference model trained on current pairs, evaluated T1-only, as the reference the CATE estimator must beat (EVL-006).
- [ ] Add a CI check that no training manifest lists `served_rung` or the heuristic's `decision` as a target column.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: estimand named as CATE; classifier-vs-estimator dichotomy replaced by label-source prohibition; cost separated from label; two effects for three rungs | "Train a calibrated utility estimator for marginal frontier gain, not a classifier that imitates current heuristic routes." |
