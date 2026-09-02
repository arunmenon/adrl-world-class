# ADRL-LRN-008 — Logged exploration in the ambiguous band

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Proposed 2026-09-02 (new, from adversarial review) |
| Maturity | D0 Design, review recommends D0 Design — nothing exists |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 4, 8, 9 |
| Related decisions | RTG (ambiguous band), SAF-001, SAF-002, CAS-005, MEM-001, MEM-009, LRN-001, LRN-002, LRN-003, LRN-006, LRN-007, EVL-005, EVL-006 |
| Open questions | Q4, Q6 |

## Decision

Inside the RTG ambiguous band only, and only among rungs that the SAF gates have already permitted, the deterministic policy applies a graduated, versioned exploration rule that randomises the rung with a bounded probability and records the propensity of the chosen rung on the decision event; exploration turns are tagged as their own evidence tier, never pooled with organic or counterfactual data, and exist to make doubly-robust off-policy evaluation and learning possible for LRN-003 alongside branched pairs (LRN-002).

1. **Where.** Only turns the deterministic policy has classified as ambiguous (Tenet 4); never in clear cases; never on pinned sessions (SAF-002) or where any hard gate has removed a rung (SAF-001, SAF-006); never mid-episode (CAS-005 stickiness applies after the first decision).
2. **How much.** Exploration probability ε per rung is a versioned parameter of the exploration artifact (LRN-005), bounded above by a value EVL sets from the savings-vs-risk budget (proposal: ε ≤ 0.10 per non-default rung), and the propensity actually used is written to the `decisions` row.
3. **Escalation stays armed.** An explored local turn runs with the same trip-wires and escalation as any local turn; exploration changes the starting rung, not the safety net. The cost of exploration is therefore bounded by one failed cheap attempt plus escalation.
4. **Evidence tier and estimators.** Exploration turns are tier `explore` (LRN-001). Off-policy estimates use doubly-robust estimators with the logged propensity and a reward model; estimator validity is checked against branched pairs (LRN-002) on the same slice before any OPE number enters an EVL pack.
5. **Graduation.** The exploration rule is itself an artifact that goes through EVL-006/007; changing ε is a new version. This is data collection under a graduated policy, not online promotion (LRN-007).

## Context and rationale

The bucket's binding problem is volume of legitimate labels, and the register's only instrument for the counterfactual arm is paired execution (LRN-002), which is expensive and (per the power arithmetic) an order of magnitude short. The literature on learning from logged bandit feedback offers the second instrument — off-policy evaluation and counterfactual risk minimisation — but every such method needs the logging policy's propensity for the action it took, and a deterministic policy has propensity one for its choice and zero for everything else: no overlap, no estimator. The only way to get propensities is to log them, which means occasionally choosing a rung the heuristic would not have chosen, in the one region where the heuristic admits it does not know.

Exploration in production is routine where rewards are cheap and immediate; here the reward is a verified outcome on a developer's task, so exploration must be small, bounded, gated behind the safety layer, and paid for by the escalation path that already exists. The proposal is deliberately narrow: ambiguous band only, hard gates untouched, pinned sessions excluded, stickiness intact, and the rule itself graduated like any artifact. If the ambiguous band turns out to be too small to make exploration worthwhile (Q4), that is the same finding that would defund LRN-003, and it should be discovered cheaply here first.

## Adversarial review (2026-09-02)

### Steelman
This is the missing half of the data strategy: pairs give clean but scarce counterfactuals; logged exploration gives cheaper, noisier counterfactuals at volume with a valid estimator, and the two validate each other. It exploits a property ADRL already has — escalation armed on every cheap attempt — so the downside of an explored local turn is one trip-wire and an escalation, a cost the system already pays on organic local misses.

### Attacks
1. **Exploration degrades a developer's turn on purpose.** Yes, with probability ≤ ε in the ambiguous band, bounded by escalation. The developer-facing cost is latency of one failed cheap attempt. Whether that is acceptable is a product decision (Q2/Q4) and should be made explicitly; the alternative is to never learn what local can do in the band.
2. **Downward exploration is the dangerous direction.** Exploring *up* (frontier where the heuristic said local) costs money and is safe; exploring *down* (local where the heuristic said frontier) risks a wrong edit. Clause 1 confines exploration to the ambiguous band where the heuristic itself is unsure, clause 3 keeps escalation armed, and Q2 excludes security-sensitive and deployment-touching categories from local regardless. Downward ε can be set lower than upward ε.
3. **Small ε makes importance weights large.** With ε = 0.05 the weight on an explored turn is 20; variance of IPS estimates will be high at low volume. Answered by clause 4 — doubly-robust estimators and validation against branched pairs — and by the honest expectation that OPE on this corpus will be informative only in aggregate for some time.
4. **Exploration data is biased by the same privacy suppression as everything else.** Pinned sessions are excluded (clause 1), so the exploration corpus under-represents sensitive work. Same bias as MEM-005/MEM-008; must be reported, not hidden.
5. **Is this online learning by another name?** No: the policy that acts is fixed and graduated; only the data changes. The estimators trained on it go through LRN-007's gate. Bandit deployments that adapt online are a different thing and are not proposed.

### Evidence
- A. Swaminathan, T. Joachims, "Counterfactual Risk Minimization: Learning from Logged Bandit Feedback" (ICML 2015) — learning from logs requires logged propensities; variance grows as propensities shrink — https://arxiv.org/abs/1502.02362
- M. Dudík, J. Langford, L. Li, "Doubly Robust Policy Evaluation and Learning" (ICML 2011) — accurate if either the propensity model or the reward model is good; the estimator clause 4 adopts — https://www.arxiv.org/abs/1103.4601
- Y. Saito et al., "Open Bandit Dataset and Pipeline: Towards Realistic and Reproducible Off-Policy Evaluation" (NeurIPS 2021 D&B; arXiv 2008.07146) — logged bandit data under multiple policies on one platform as the basis for OPE research; the data shape this decision creates — https://arxiv.org/abs/2008.07146
- A. Gonuguntla (CMU), "The Replay Gap" (arXiv 2608.08239, 2026) — recommends developing OPE estimators validated against branched ground truth for agentic routing; the validation loop in clause 4 — https://arxiv.org/html/2608.08239
- Spotify Research, "Calibrated Recommendations with Contextual Bandits on Spotify Homepage" (2025) — ε-greedy exploration bounded by a KL penalty in production, after offline and A/B validation; the shape of bounded exploration under a graduated policy — https://research.atspotify.com/2025/9/calibrated-recommendations-with-contextual-bandits-on-spotify-homepage

### Verdict
**PROPOSED (new).** Without this decision LRN-002's power arithmetic says the estimator cannot be trained at the corpus's growth rate, and LRN-003's CATE cannot be validated outside the pair set. The attacks are cost and bias questions with explicit answers in clauses 1–5. Recommend acceptance at D0 with ε and the band definition to be set by RTG/EVL.

## Amendments applied

New decision — no prior text.

## Follow-ups

- [ ] RTG: publish the ambiguous-band definition and its share of turns; if < 5% of turns, revisit whether exploration (and LRN-003) is worth building.
- [ ] Add `propensity` and `explore_version` columns to the `decisions` row (MEM-001 schema v2); golden test that a non-explored turn logs propensity 1.0 for the chosen rung.
- [ ] Golden tests: no exploration on pinned sessions, on turns with any gate-removed rung, or after the first decision of an episode.
- [ ] Implement DR estimation in an offline notebook against the first 50 explored turns and compare with branched pairs on the same slice before any number enters the EVL pack.
- [ ] Product decision (Q2/Q4): approve the upward and downward ε bounds and the categories excluded from downward exploration.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-02 | Proposed (adversarial review) | — |
