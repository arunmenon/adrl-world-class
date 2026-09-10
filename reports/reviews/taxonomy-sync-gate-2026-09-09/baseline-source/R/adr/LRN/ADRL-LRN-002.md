# ADRL-LRN-002 — Branched pairs, plus a logged-exploration channel

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested for the pairing contract in `counterfactual.py`; the evidence it is meant to produce is effectively D0 (usable pair volume "very low"; no power target) |
| Review verdict | AMEND |
| Tenets | 8, 9 |
| Related decisions | MEM-003, MEM-009, LRN-001, LRN-003, LRN-004, LRN-008 (proposed), CAS-003, CAS-004, SAF-002, EVL-005 |
| Open questions | Q4, Q6 |

## Decision

Counterfactual training data uses paired local/frontier attempts branched from the same sanitised snapshot *and the same turn state* (identical transcript prefix, tool results and harness dialect up to the decision boundary), verified by the same verifier version, bound to the explicit `route_id` (MEM-009), and tagged as counterfactual tier; pairs are the primary estimand for marginal frontier gain, are sized to a declared power target, and are complemented — not replaced — by logged-propensity exploration data (LRN-008) for off-policy evaluation.

1. **A pair is a branch, not a replay.** Both arms execute live from the same container/tree state and the same transcript prefix; substituting one model's logged output into the other's trajectory is not a pair.
2. **Same rules on both arms.** Sanitisation, privacy pin status, protected-path policy and trip-wire configuration are identical across arms; a pinned session cannot produce a frontier arm (SAF-002), so pinned turns are excluded from pairing and the exclusion is reported.
3. **Power target declared.** The pair budget is set from a stated minimum detectable marginal gain δ and discordance rate; at δ = 0.10 and 15–30% discordance this is roughly 115–235 pairs per slice for 80% power at α = 0.05 (McNemar), i.e. an order of magnitude above today's corpus.
4. **Deterministic routing has no propensity.** Because the deterministic policy assigns each turn to exactly one rung, importance-weighted off-policy estimators cannot be applied to organic logs; OPE becomes possible only for turns inside an exploration band with logged propensities (LRN-008).

## Context and rationale

To learn what frontier buys you have to run the same task twice. A usable training example is a pair: the same sanitised snapshot, attempted on both rungs, verified the same way. It is expensive and slow, which is the honest reason the bucket is D0 — a shortage of legitimate pairs.

The amendment answers the register's own question ("would you accept a weaker pairing standard for volume?") with a precise no and a precise alternative. No: the closed-loop nature of agent trajectories means a "pair" that is a replay — the frontier's logged output dropped into the local attempt's transcript — scores a world that never existed; the correct pair is a live branch from the same state, which is *stronger* than the original wording, not weaker. The alternative for volume is not weaker pairs but a second, separately-tagged channel: randomise a small fraction of ambiguous-band decisions, log the propensity, and use doubly-robust off-policy estimators. That channel is impossible under purely deterministic routing (no overlap, no propensity), which is why it needs its own decision (LRN-008). The power arithmetic makes clear that neither channel is optional at the scale the estimator needs.

## Adversarial review (2026-09-02)

### Steelman
Pairs are the gold standard for a treatment-effect question ("what does frontier add on this task?"): same unit, both treatments, same measurement. Every alternative — organic logs, proxies, simulators — either lacks the counterfactual arm or lacks the verification. The register is right that a pair shortage is the honest reason LRN is D0, and right to refuse a weaker standard.

### Attacks
1. **The original wording admits replay pairs, and replay scores the wrong world.** "Paired attempts from the same sanitised snapshot" can be satisfied by re-running the other rung from the snapshot with the same prompt — but an agent turn is a closed loop: the model's first action determines the next observation. Branched-rollout experiments show early model swaps diverge at the very first post-fork action in 74–77% of cases, that 61–94% of subsequent actions differ, and that replay-based evaluators predicted none of the observed outcome flips. A pair has to be a live branch from the same transcript prefix and tool state. The decision must say so.
2. **Can OPE substitute for pairs? Not on this system's logs.** Counterfactual risk minimisation and doubly-robust estimation need the logging policy's propensity for the action taken and overlap between logging and target policies. ADRL's deterministic policy has propensity 1 for the rung it chose and 0 for the others: no overlap, infinite (undefined) importance weights. Doubly-robust estimation with a reward model alone collapses to the direct method — i.e. the estimator LRN-003 has not built. So OPE is not a shortcut around pairs *today*; it becomes one only with logged exploration, which the register has no decision for.
3. **No power target, so "very low volume" is unquantified.** With ~34 evaluated decisions and one verified task, the corpus cannot detect any plausible marginal gain. A quick McNemar calculation (α = 0.05 two-sided, power 0.80): for δ = 0.10 (frontier fixes 10 percentage points more of the tasks local fails, net), n ≈ 115 pairs at 15% discordance and ≈ 235 at 30%; for δ = 0.05, 470–940 pairs; for δ = 0.20, 40–56 pairs. Assumptions: binary verified outcome, pairs independent, one slice. A per-slice CATE (LRN-003) multiplies this by the number of slices. The decision should state the target so the shortfall is a number, not an adjective.
4. **Same snapshot ≠ same conditions.** The two arms may see different prompt-cache states, different harness dialects (local rung uses a different edit format), different trip-wire configurations, and — under SAF-002 — a pinned session can never produce a frontier arm at all. Pairs are therefore only available for un-pinned turns, which biases the pair corpus away from sensitive code exactly as MEM-005 biases retrieval. The decision should require rule-equivalence across arms and report the pinned exclusion.
5. **Verification must be the same instrument.** MEM-003's amendment adds verifier version and tree identity; a pair verified by different verifier versions, or where one arm's verification ran on a drifted tree, is not a pair. Cross-reference required.
6. **Cost.** Every pair costs a frontier call (or a local run) that produced no developer value, on a system whose purpose is to cut spend. Answered: pairs are drawn only from the ambiguous band (Tenet 4), which the register says is a minority of traffic, and the frontier arm can be run asynchronously off the developer's critical path from the branched container. The cost is real and should be budgeted against the savings the estimator is supposed to unlock (Q4).

### Evidence
- A. Gonuguntla (CMU), "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World" (arXiv 2608.08239, 2026) — branching rollout protocol on SWE-bench (forks at 30%/70% depth, ~900 rollouts, Qwen3-4B↔14B); replay evaluation mispredicts outcome-relevant calls; recommends live/branched evaluation and OPE validated against branched ground truth; attack 1 — https://arxiv.org/html/2608.08239
- A. Swaminathan, T. Joachims, "Counterfactual Risk Minimization: Learning from Logged Bandit Feedback" (ICML 2015; JMLR 2015) — learning from logged data requires propensities of the logging policy; variance of propensity-weighted risk drives the bound; attack 2 — https://arxiv.org/abs/1502.02362 ; https://jmlr.org/papers/v16/swaminathan15a.html
- M. Dudík, J. Langford, L. Li, "Doubly Robust Policy Evaluation and Learning" (ICML 2011) — accurate if *either* the reward model or the propensity model is good; with a deterministic logging policy the propensity side is unavailable and the estimator reduces to the reward model; attack 2 — https://www.arxiv.org/abs/1103.4601
- Y. Saito et al., "Open Bandit Dataset and Pipeline" (NeurIPS 2021 Datasets & Benchmarks; arXiv 2008.07146) — real logged bandit data collected under multiple policies on one platform, the precondition for OPE research; illustrates that OPE needs logged behaviour policies, which ADRL does not have (attack 2, LRN-008) — https://arxiv.org/abs/2008.07146
- Q. Hu et al., "RouterBench" (arXiv 2403.12031, 2024) — 405k outcomes with every candidate model's output and score per prompt: the "full pairs for everything" design at benchmark scale, and a reminder of the volume gap (attack 3) — https://arxiv.org/pdf/2403.12031
- Sample-size arithmetic: computed by the reviewer (McNemar paired-proportions, normal approximation, α = 0.05 two-sided, power 0.80); assumptions stated in attack 3; no external source.

### Verdict
**AMEND.** Attack 1 lands and tightens the decision rather than loosening it: pairs must be branches, not replays. Attack 2 answers the review's central question — OPE cannot substitute for pairs on deterministic logs, but it can complement them once exploration is logged — and yields LRN-008. Attack 3 turns "very low" into a number the bucket can plan against. Attacks 4 and 5 are rule-equivalence and cross-reference clauses. Attack 6 is answered by scoping pairs to the ambiguous band. The register's refusal of a weaker pairing standard is upheld and made stronger.

## Amendments applied

- "from the same sanitised snapshot" → "branched from the same sanitised snapshot *and the same turn state*"; replay explicitly excluded (clause 1).
- Added rule-equivalence across arms and the pinned-session exclusion with reporting (clause 2).
- Added a declared power target with the reviewer's arithmetic as the initial figure (clause 3).
- Added the no-propensity statement and the pointer to the logged-exploration channel LRN-008 (clause 4).
- Added same-verifier-version and explicit-`route_id` binding (MEM-003, MEM-009) and counterfactual tier tagging (LRN-001).

## Follow-ups

- [ ] Golden test in `counterfactual.py`: a pair whose arms have different transcript prefixes, tool-result sets, harness dialect or verifier version is rejected.
- [ ] Build the branched-rollout harness: snapshot container + transcript prefix at the decision boundary (CAS-003), run both arms live, verify both with MEM-003 provenance; measure same-model control divergence first to know the noise floor.
- [ ] Publish the pair budget: chosen δ, assumed discordance, resulting n per slice; report current pair count against it in every EVL pack.
- [ ] Report the fraction of ambiguous-band turns excluded from pairing by SAF-002 pins.
- [ ] Draft ADRL-LRN-008 (exploration and logged propensities in the ambiguous band).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: pairs must be live branches from the same turn state; rule-equivalence across arms; declared power target; OPE positioned as complement via LRN-008 | "Counterfactual training data uses paired local/frontier attempts from the same sanitised snapshot." |
