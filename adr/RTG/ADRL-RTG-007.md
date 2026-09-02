# ADRL-RTG-007 — Marginal-utility target, with a build gate

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D0 Design, review recommends D0 Design (unchanged; nothing is built and the amendment adds a pre-build gate, not implementation) |
| Review verdict | AMEND |
| Tenets | 4, 9 |
| Related decisions | RTG-003, RTG-005, RTG-009 (proposed), LRN-002, LRN-003, LRN-006, LRN-007, EVL-004, EVL-006, EVL-007 |
| Open questions | Q4, Q6 |

## Decision

The target learned decision is the marginal utility of frontier versus local — expressed in the session-marginal cost and verified-quality units of RTG-005/RTG-009 — with calibrated uncertainty and abstention; it is built only after a published pre-build gate shows the ambiguous band is large enough, and the achievable gain over the best-single-model and current-heuristic baselines is high enough, to repay the cost of building and governing it.

1. Pre-build gate (owned by EVL, evidence from MEM): (a) ambiguous-band share of turns and of spend on a representative population (not the single-user corpus alone); (b) an oracle-bound estimate — the cost/quality gain if every ambiguous turn were routed perfectly — measured from counterfactual pairs (LRN-002); (c) a required-minimum realised gain, versioned, that the estimator must beat offline against always-local, always-frontier and RTG-002-heuristic baselines after cache effects.
2. Abstention (LRN-006) is a prerequisite, not a feature: the estimator may not hold advisory authority until its abstention path to the deterministic policy is built and tested.
3. RTG-007 states the *runtime* target; LRN-003 owns the training target and data. The two must cite one shared definition of utility (RTG-009) and one shared baseline set (EVL) so they cannot drift.

## Context and rationale

The real target: not "how hard is this?" but "how much does frontier actually buy?" A classifier that imitates today's heuristics can never beat them. A utility estimator asks: for this task, what is the expected gain from spending frontier tokens? It needs calibrated uncertainty and abstention. None of it is built — D0. The amendment adds what Q4 is actually asking for: a bar. Independent benchmarks say learned routers frequently fail to beat the best single model, and that their value collapses as estimate noise rises; the project's own corpus says the ambiguous band is a minority and counterfactual pairs are scarce. Under those two facts, "build a calibrated utility estimator" is a hypothesis that could be false, and the register should state what evidence would settle it *before* engineering starts — otherwise FND-005 ("component presence is not readiness") is asserted for every bucket but this one.

## Adversarial review (2026-09-02)

### Steelman
Marginal utility is the theoretically correct routing target: RouteLLM learns a win-probability, Hybrid LLM a quality gap, and cascade-routing theory optimises expected quality minus cost — all are utility estimators, not difficulty classifiers. Calibration and abstention are the properties that make a learned router safe to put behind deterministic gates (selective classification gives a controlled-risk guarantee at the price of coverage). Stating the target now prevents the team from building a heuristic-imitating classifier later.

### Attacks
1. **The upside may not exist.** RouterBench: "none of the routing algorithms significantly outperform the baseline Zero router" on several datasets. LLMRouterBench (33 models, 400k instances): "several recent routing methods, even including the commercial router OpenRouter, do not outperform... the Best Single model" and gains come from "coarse-grained domain structure" — which RTG-003's rules already capture. The project's own Phase 0 finding is that the ambiguous band is a minority. A learned utility estimator over a minority band, beating rules that already capture the coarse structure, is a small target. The decision must name the bar.
2. **The estimator is unlearnable at current data volume.** LRN-002 requires paired local/frontier attempts on the same sanitised snapshot; the register says usable pair volume is "very low"; 34 of 300 evaluated decisions exist; one task has strong verification. RouteLLM needed ~80k preference pairs *plus* augmentation to beat random on MMLU. There is no evidence in the pack that a calibrated estimator can be trained on the foreseeable corpus, and the decision does not say what volume would be enough.
3. **Utility is undefined until RTG-009 exists.** "Marginal utility of frontier versus local" in which units? If per-turn list price, it is wrong (cache); if per-session, then the utility of a rung switch depends on transcript length and cache state — variables that today's features and the learning contract may not carry. A target without units is not yet a target.
4. **Calibration does not transfer, and the decision relies on it.** Kadavath et al. found models "struggle with calibration of P(IK) on new tasks"; RouteLLM's routers were near-random out of distribution; Xiong et al. found verbalised confidence overconfident with no consistently winning elicitation method. Abstention (LRN-006) is the safeguard, and it is D0 — so the property that makes RTG-007 safe does not exist. The sequencing question in LRN ("build abstention before the estimator?") should be answered here: yes (clause 2).
5. **Duplicate ownership with LRN-003.** RTG-007 and LRN-003 are the same decision stated twice with slightly different words ("marginal utility of frontier versus local" vs "marginal frontier gain"). Two Accepted texts for one target will drift; one must reference the other's definitions (clause 3).

### Evidence
- Hu et al., "RouterBench" (arXiv 2024) — routers match best single LLM at lower/similar cost but "none... significantly outperform the baseline Zero router"; oracle gap remains (attack 1) — https://arxiv.org/abs/2403.12031
- LLMRouterBench (arXiv 2026) — OpenRouter −24.7% vs Best Single; "contemporary routing approaches deliver nearly indistinguishable results"; "model-recall failures" dominate (attack 1) — https://arxiv.org/html/2601.07206v1
- Ong et al., "RouteLLM" (ICLR 2025) — matrix-factorisation router reaches 13.4% CPT(50%) on MT-Bench with augmented data, but Arena-only training was near-random on MMLU/GSM8K; gains depend on data similarity (attacks 2, 4) — https://arxiv.org/abs/2406.18665
- Dekoninck et al., "A Unified Approach to Routing and Cascading for LLMs" (arXiv 2024) — cascade routing gains over baselines are "between 1% to 4%" on RouterBench and the gap "narrows under higher noise levels"; "good quality estimators [are] the critical factor" (attacks 1, 4) — https://arxiv.org/abs/2410.10347
- Ding et al., "Hybrid LLM" (ICLR 2024) — quality-gap prediction with a desired-quality knob is the closest published instantiation of the RTG-007 target (steelman) — https://arxiv.org/abs/2404.14618v1
- Kadavath et al., "Language Models (Mostly) Know What They Know" (arXiv 2022) — P(IK) "struggle[s] with calibration... on new tasks" (attack 4) — https://arxiv.org/abs/2207.05221
- Xiong et al., "Can LLMs Express Their Uncertainty?" (ICLR 2024) — verbalised confidence is overconfident; no elicitation method consistently wins (attack 4) — https://arxiv.org/abs/2306.13063
- Geifman & El-Yaniv, "Selective Classification for Deep Neural Networks" (NeurIPS 2017) — reject option gives a desired risk "with high probability" at the cost of coverage (steelman for abstention; e.g. 2% top-5 error at ~60% coverage on ImageNet) — https://papers.neurips.cc/paper/7073-selective-classification-for-deep-neural-networks
- Chuang et al., "Learning to Route LLMs with Confidence Tokens" (ICML 2025) — trained confidence tokens improve routing/rejection over verbalised confidence and token probabilities, i.e. calibration for routing must be *trained*, not assumed (attack 4) — https://arxiv.org/abs/2410.13284
- RouteNLP, "Closed-Loop LLM Routing with Conformal Cascading" (arXiv 2026) — conformal guarantees applied to routing thresholds; a candidate mechanism for LRN-006's abstention (clause 2) — https://arxiv.org/abs/2604.23577

### Verdict
**AMEND.** The target is right in kind (attack-proof on theory: every serious router is a utility estimator) but the decision, as the only D0 in RTG, is stated as if building it were merely deferred rather than conditional. Attacks 1 and 2 land: independent benchmarks and the project's own data make "the estimator will pay for itself" an open empirical question, so the decision must carry a pre-build gate — this is Q4's answer. Attack 3 lands and is answered by RTG-009. Attack 4 lands and is answered by making abstention a prerequisite (clause 2). Attack 5 is a register-hygiene defect fixed by clause 3. REJECT was considered — "keep the objective simple and cache-aware first" (Q4 lean) could be read as withdrawing RTG-007 — but the target is still the correct long-run target and withdrawing it invites a heuristic-imitating classifier by default. It stays at D0 with a gate.

## Amendments applied
- Added units: "expressed in the session-marginal cost and verified-quality units of RTG-005/RTG-009".
- Added the pre-build gate (clause 1) with three named measurements and a versioned minimum gain.
- Added clause 2: abstention is a prerequisite for any authority.
- Added clause 3: single shared definition with LRN-003.

## Follow-ups
- [ ] EVL to publish the pre-build gate values (band share, oracle-bound gain, minimum realised gain) as a versioned config next to `readiness-score-v1.json`.
- [ ] MEM/LRN to report counterfactual-pair count and the pair volume at which a calibration curve is statistically meaningful; put that number in the gate.
- [ ] Build and test LRN-006 abstention against the deterministic policy *before* any estimator training run is scheduled.
- [ ] Amend LRN-003 to cite RTG-009 for utility units and EVL baselines; remove duplicate wording.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: utility units fixed to RTG-009; pre-build gate added; abstention made prerequisite; single definition shared with LRN-003 | "The target learned decision is the marginal utility of frontier versus local, with calibrated uncertainty and abstention." |
