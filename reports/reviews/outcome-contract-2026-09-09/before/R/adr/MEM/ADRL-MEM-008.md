# ADRL-MEM-008 — Retrieval stays advisory until gated

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · unchanged |
| Maturity | D3 Shadow, review recommends D3 Shadow — `shadow_retrieval.py` runs against real traffic without authority, which is the D3 definition; the shadow *measurement* itself is thin (34/300 evaluated decisions) but that is what D3 is for |
| Review verdict | APPROVE |
| Tenets | 4, 8, 9 |
| Related decisions | MEM-005, MEM-007, LRN-004, LRN-006, LRN-007, EVL-004, EVL-005, EVL-009, RTG (ambiguous band) |
| Open questions | Q4, Q6 |

## Context-graph planning note, 2026-09-08

A bounded context-graph retrieval candidate is proposed for connecting relevant task context, prior decisions, verified/corrected outcomes and policy/ADR changes. Compare it with structured-only and flat/vector retrieval on the same permitted evidence, including total cost and completed-task benefit. Existing retrieval/data/advisory gates remain; graph connectivity confers no additional authority or causal proof. See the [proposal](../../design/adrl-context-graph-memory-proposal-2026-09-08.md) and [product roadmap](../../reports/adrl-product-roadmap-2026-09-08.md). Current decision wording, status and maturity are unchanged.

## Decision

Retrieval remains advisory/shadow until evaluated-label quantity and quality gates pass.

## Context and rationale

"The system remembers similar past tasks" is the most intuitive feature in the register and the easiest to over-trust. Similar-task lookup by embedding is cheap and often looks right; it is also the mechanism by which a thin, single-user, workflow-heavy corpus would be turned into confident routing advice. So retrieval advises and is measured in shadow, and cannot take authority until the label gates named in EVL-004 pass. Today the code reality is 34 evaluated decisions against a required 300, and the decision is doing exactly what it should: holding the door shut.

The review leaves the text unchanged because it is already the strongest form of the claim — it names no threshold of its own, defers to EVL-004, and grants retrieval no authority path outside EVL. The attacks below are real but land on EVL-004's gate definition and on MEM-005/MEM-007, where they are recorded as amendments and follow-ups. The one caution worth stating here is that "quantity and quality" are not "representativeness", and the register's own Q6 says representativeness is the binding constraint.

## Adversarial review (2026-09-02)

### Steelman
Retrieval-based routing (kNN over past tasks) is in the literature the weakest learned router family but the cheapest to build, and it becomes dangerous precisely when it is trusted early on a small corpus. Keeping it advisory until label gates pass is Tenet 4 and Tenet 9 applied to the one component that would otherwise sneak into authority through "it's just a hint". The decision is short, defers thresholds to EVL, and is honestly labelled D3.

### Attacks
1. **Quantity gates measure the wrong thing.** 300 evaluated decisions from a single user doing workflow-heavy tasks (the register's own non-claim) is 300 near-duplicates. kNN retrieval on such a corpus will report high neighbour similarity and high agreement — because the corpus is homogeneous — and pass a quantity gate while telling you nothing about the next developer. The gate must be a coverage/representativeness gate, not a count. (Lands on EVL-004, not on this text.)
2. **Retrieval learns only from the non-sensitive half of the world.** MEM-005 suppresses embeddings for private/secret/pinned turns. The retrieval index therefore systematically lacks exactly the sessions that touch payments code, secrets and protected paths — which are the sessions where a wrong advisory is most costly. Any shadow metric will be computed over the biased subset. The decision should be read with that bias explicit. (Recorded as an EVL-004 follow-up: report shadow metrics with the suppressed fraction.)
3. **Shadow advice can leak into authority through a human.** A shadow advisory that is displayed to the operator (or surfaces in a dashboard the developer sees) changes behaviour without ever "taking authority". The decision's word "advisory" must mean "logged, not shown to the routing path or the developer" until graduation; otherwise the shadow measurement contaminates itself. Answered: the code map shows `shadow_retrieval.py` as a logging path; the follow-up is a test that its output is not on any decision or UI path.
4. **kNN routing evidence is weak even at scale.** In RouteLLM's comparison the similarity-weighted (kNN-style) router is one of several and the learned routers (matrix factorisation, BERT, causal LLM) are the ones reported as strong; RouterDC exists because embedding-similarity routers struggle when several models perform comparably. Retrieval as *advice to a learned estimator* is defensible; retrieval as *the* router is not, and the decision should never be read as a path to the latter. Answered: the text grants no authority path; LRN-003 owns the estimator.
5. **Projection staleness is an unmeasured variable in the shadow.** If the NumPy index is stale relative to the ledger (MEM-007), the shadow measures a different retrieval system than would serve. Answered by MEM-007's amendment (staleness labelled and excluded from evidence).

### Evidence
- I. Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data" (arXiv 2406.18665, 2024) — trains routers on preference data with several router families including a similarity-weighted ranking router; reports >2× cost reduction and transfer across model pairs; the paper does not rank router families against each other, so no claim that the similarity-weighted (kNN-style) router is weakest should be attributed to it (attack 4) — https://arxiv.org/abs/2406.18665
- S. Chen et al., "RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models" (NeurIPS 2024; arXiv 2409.19886) — motivated by existing routers struggling when multiple LLMs perform comparably; +2.76% in-distribution and +1.90% out-of-distribution over baselines; supports attack 4's point that retrieval-style similarity is not sufficient for close calls — https://arxiv.org/abs/2409.19886
- Q. Hu et al., "RouterBench: A Benchmark for Multi-LLM Routing System" (arXiv 2403.12031, 2024) — 405k+ inference outcomes over 11 models / 8 datasets; per-prompt cost and quality for every candidate; oracle router and AIQ metric; the shape a proper offline evaluation of retrieval advice would take, and the scale gap to 34 decisions (attack 1) — https://arxiv.org/pdf/2403.12031
- S. Kaufman et al., "Leakage in Data Mining" (TKDD 2012) — learn-predict separation; supports the "shadow output must not reach the decision path" rule (attack 3) — https://dl.acm.org/doi/10.1145/2382577.2382579
- No direct literature found on representativeness gates for single-user coding corpora; attack 1 is reasoned from the register's own non-claims and Q6.

### Verdict
**APPROVE.** Every attack either lands on a neighbouring decision (EVL-004 for the gate definition; MEM-005/MEM-007 for bias and staleness) or is answered by the text's refusal to name any authority path of its own. The decision is the correct shape: it says what retrieval may not do and defers the "when" to EVL. Changing it would weaken it. The follow-ups carry the substantive findings to where they belong.

## Amendments applied

None — decision stands as written.

## Follow-ups

- [ ] EVL-004: add a representativeness condition to the retrieval authority gate (distinct intent classes, distinct repos, >1 user) alongside the 300-count; report the suppressed (private/pinned) fraction of turns next to every shadow retrieval metric.
- [ ] Golden test: `shadow_retrieval.py` output reaches the ledger only — assert no import from it in `live_router.py`, `policy.py` or any UI/telemetry surface the developer sees.
- [ ] Define the shadow metric now (e.g. agreement with the served rung, and neighbour-outcome-predicted vs verified outcome on the 34 evaluated decisions) so the D3 claim has a number attached before the next review.
- [ ] Re-check the RouteLLM paper body for the relative ranking of the similarity-weighted router before citing it in the EVL pack.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Retrieval remains advisory/shadow until evaluated-label quantity and quality gates pass." |
