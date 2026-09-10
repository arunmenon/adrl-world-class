# LRN — Learning and Adaptation

**Planning task-pack preparation, 2026-09-08:** [the next lab packet](../../reports/waves/lab-planning-deliverables.md) supplies draft PRD/HLD/LLD tasks and assessed-evidence contracts. Actual harness/mode execution, assessment calibration and any learning admission remain open. No runtime, decision text/status or maturity change is implied.

**W7.0a completed, 2026-09-08:** [mixed-intent routing correction](../../reports/adrl-routing-correction-2026-09-08.md) introduces features-v2 and explicit exploration compatibility protection. Two masking defects are corrected; lexical ambiguity/negation limits remain visible. All eleven checks pass: 911 tests passed, eight engine cases skipped, 322 stable inputs. Decision text/status/formal maturity and learning admission are unchanged. This was a bounded foreground implementation; hourly continuation remains paused. Earlier dated checkpoints below are preserved.

**Experiment lab, 2026-09-08:** [the proposed lab](../../design/adrl-experiment-lab-plan-2026-09-08.md) extends existing task/evidence contracts across qualified harnesses and task types. Initial knowledge is pinned to supported versions and remains a candidate; simulated/benchmark evidence is not organic, and changing harnesses changes the comparison scope. Decision wording, maturity and implementation are unchanged; execution stays paused.

**Product planning, 2026-09-08:** LRN estimates conditional model benefit from qualified evidence. Context-graph features and prior-step signals require admission and temporal-leakage disposition; classifier labels are not outcome targets. See the [startup roadmap](../../reports/adrl-product-roadmap-2026-09-08.md) and [context-graph proposal](../../design/adrl-context-graph-memory-proposal-2026-09-08.md). Implementation remains paused; decision text, architectural status and maturity are unchanged.

**Planning checkpoint, 2026-09-08:** the user requested the target adaptive routing/RSI architecture before further implementation. [Blueprint](../../reports/adrl-adaptive-routing-rsi-blueprint-2026-09-08.md) and [all-ADR map](../../reports/research/adaptive-routing-blueprint-2026-09-08/taxonomy-map.md) are proposals for disposition. Implementation continuation is paused; no decision wording, status or maturity is changed by the blueprint.

**Routing diagnostic, 2026-09-08:** [24 task prompts under five conditions](../../reports/adrl-routing-in-action-2026-09-08.md) exercised the unchanged router, cascade and explicit rule-health refresh. The 240 decisions are synthetic component probes; 135 existing focused tests pass. Two mixed-intent review hypotheses fail. Model quality, savings, live refresh, learning admission and all maturity promotions remain unproved/unchanged. [Routing correction](../../reports/waves/routing-decision-quality.md) is held pending blueprint disposition; W3 capture work remains open.

**Forward plan proposed, 2026-09-07:** the [implementation roadmap](../../reports/adrl-implementation-roadmap-2026-09-07.md)
assigns this bucket's decisions to evidence-gated waves, with explicit stop/recovery conditions.
This is a planning update; current implementation and maturity remain as recorded below.

**Latest offline improvement evidence, 2026-09-07:** [LRN-005](ADRL-LRN-005.md), [LRN-007](ADRL-LRN-007.md) record
the applied verifier-comparison workflow and its limits. The current and proposed verifiers
classified 4/7 and 7/7 curated examples correctly; 549 implementation tests pass. These are
visible variants of one task family, with no automatic promotion or learning admission.
See the [report](../../reports/adrl-improvement-experiment-2026-09-07.md).

**Current session verification update, 2026-09-07:** [LRN-001](ADRL-LRN-001.md) record
API preview 4, independent encrypted session receipts and 532 passing tests. Two verifier jobs
each passed eight tests on the same prior pilot task; no general graduation or learning admission
follows. See the [report](../../reports/adrl-session-verification-2026-09-07.md). Earlier notes
below preserve their original scope.

**Core question:** How do we learn a better policy?
**Owns / does not own:** Owns training data (tiers, pairs, exploration logs), the learning target, features and leakage rules, artifact versioning, calibration and abstention. Does not own live rollout approval (EVL), hard safety gates (SAF), or the ledger the data comes from (MEM).

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-LRN-001 | Evidence tiers, not "outrank" | AMEND | D2 → D1 | "Outrank" is unimplementable; verifier is itself noisy (flaky tests, 68% flawed "verified" benchmark tasks); tier-1 corpus is one task |
| ADRL-LRN-002 | Branched pairs, plus a logged-exploration channel | AMEND | D2 → D2 (contract) / D0 (evidence) | Pairs must be live branches, not replays (74–77% first-action divergence on swap); no propensity exists for OPE on deterministic logs; no power target (~115–235 pairs/slice at δ=0.10) |
| ADRL-LRN-003 | The target is a CATE, name it | AMEND | D0 → D0 | Estimand never named; classifier-vs-estimator dichotomy is false (RouteLLM, Hybrid LLM train classifiers on comparative outcomes); three rungs need two effects |
| ADRL-LRN-004 | Pre-decision features, enforced by construction | AMEND | D2 → D1 | Rule stated, not constructed: no decision-time feature snapshot, retrieval index leaks the future, no temporal split, `served_rung` not deny-listed |
| ADRL-LRN-005 | Every artifact is fully versioned | APPROVE | D2 → D2 (fixtures only) | Right components; manifest needs code commit, seed, embedding-model version, ledger position, tier mix, eval report — follow-ups, not text |
| ADRL-LRN-006 | Abstention with a declared risk-coverage target | AMEND | D0 → D0 | "Uncertain"/"OOD" undefined and unfalsifiable; needs selective-prediction risk target, feature-space OOD detector, reported abstention rate; build before estimator |
| ADRL-LRN-007 | No autonomous online promotion | APPROVE | D0 → D0 | "Too conservative" fails: production bandits (Spotify 2018/2025) still do offline eval + A/B graduation with bounded deviation, on rewards ADRL lacks |
| ADRL-LRN-008 | Logged exploration in the ambiguous band | PROPOSED (new) | — → D0 | Deterministic routing has no propensities, so OPE/CRM is impossible on organic logs; pairs alone are an order of magnitude short |

Tally: 2 APPROVE, 5 AMEND, 0 REJECT, 1 PROPOSED.

## Cross-cutting findings

1. **The crux decision (LRN-003) never names what it estimates.** "Marginal utility of frontier" is a conditional average treatment effect: treatment = rung, outcome = verified T1 result, conditioning = pre-decision features. Naming it supplies estimators (T-/X-/DR-learners), a known pitfall (S-learner shrinkage), the correct meaning of "calibrated" (per-arm probabilities plus uncertainty on the difference), and the fact that three rungs need two effects. It also exposes a false premise: the register contrasts a "utility estimator" with "a classifier that imitates heuristics", but RouteLLM and Hybrid LLM are classifiers trained on comparative outcomes that generalise across model pairs. The line that matters is the *label source* — heuristic decisions (forbidden) vs comparative verified outcomes (required) — not the model class.

2. **Off-policy evaluation cannot substitute for pairs on this system's logs — but it can complement them, and nothing in the register enables it.** CRM and doubly-robust estimation need the logging policy's propensity; ADRL's deterministic policy has propensity 1/0, so there is no overlap and no estimator. Pairs (LRN-002) are the only counterfactual instrument today and the power arithmetic (McNemar, α=0.05, power 0.80) says δ=0.10 needs ~115–235 pairs per slice at 15–30% discordance — versus 34 evaluated decisions and one verified task. LRN-008 (proposed) adds bounded, gated, logged exploration in the ambiguous band so that DR-OPE becomes possible and can be validated against branched pairs. This is data collection under a graduated policy, not online learning; LRN-007 is untouched.

3. **Pairs must be branches, not replays.** The 2026 "Replay Gap" branched-rollout study shows early model swaps diverge at the first post-fork action in 74–77% of cases and that replay-based evaluators predicted none of the observed outcome flips. LRN-002's "same sanitised snapshot" was compatible with replay; the amendment requires the same transcript prefix, tool state and harness dialect, executed live on both arms. This also bears on EVL-006: "offline evaluation" of a routing artifact must be branched or propensity-weighted, never replay.

4. **Three decisions were "stated, not enforced" and claimed D2 on the strength of a contract file.** LRN-001 (outrank), LRN-004 (leakage) and LRN-005 (versioning) are all encoded in `learning_contract.py` and tested against fixtures; none has been exercised on a real training set because none exists. LRN-004 in particular has three concrete leak paths open today: features recomputed from the ledger after the fact, a retrieval index containing the future (MEM-007), and random splits over dependent turns. The fix is construction — snapshot the feature vector at the decision boundary, as-of projections, temporal splits, a named deny-list including `served_rung` — and the maturity is honestly D1 until then.

5. **Build the cage before the animal.** LRN-006 (abstention) is D0 and undefined; LRN-003 (estimator) is D0. The register asks whether abstention should come first. Yes: an abstention gate — selective-prediction threshold for a target risk, feature-space OOD detector, abstention-rate telemetry with EVL-009 bounds — is the cheapest D2 in the bucket and needs no pairs. The amendment writes the ordering into LRN-006.

6. **"Verified" is an instrument, not a fact.** Flaky tests (45% async-wait, 20% concurrency in one study), benchmark curation finding 68% of "verified" coding tasks flawed, and a single strongly-verified task in this repo mean tier-1 status must be conditioned on measured verifier precision (LRN-001 clause 3, MEM-003 amendments). Otherwise "fewer, better labels" is fewer labels with an unmeasured error rate, and the label-error literature shows a few percent is enough to invert a rung comparison.

7. **The privacy bias is everywhere and is never reported.** Pinned sessions cannot produce frontier arms (LRN-002), cannot be explored (LRN-008), have no embeddings (LRN-004 missingness), and are absent from retrieval (MEM-008). Every training set and every metric in this bucket is computed on the non-sensitive subset of work. Each amended decision now requires the excluded fraction to be reported next to the metric; EVL should treat it as a representativeness condition (Q6).

8. **Conflicts with other buckets recorded:** LRN-004 vs MEM-007 (as-of projections required); LRN-002/LRN-007 vs EVL-006 (offline evaluation must be branched or propensity-weighted, not replay); LRN-003 vs RTG (cost enters the decision, not the label; band size and savings ceiling must be published before funding the estimator — Q4); LRN-006 vs MEM-006/MEM-005 (degraded-memory and privacy-suppressed abstentions must be counted under their own reason codes); LRN-001 vs EVL-004/EVL-005 (simulator is a separate tier; 300-count needs a diversity condition).

**Proposed new decision:** ADRL-LRN-008 — Logged exploration in the ambiguous band (status Proposed; file written).

## Sources consulted

- A. Swaminathan, T. Joachims, "Counterfactual Risk Minimization: Learning from Logged Bandit Feedback" (ICML 2015) — https://arxiv.org/abs/1502.02362 ; JMLR version https://jmlr.org/papers/v16/swaminathan15a.html ; dblp https://dblp.org/rec/conf/icml/SwaminathanJ15.html
- M. Dudík, J. Langford, L. Li, "Doubly Robust Policy Evaluation and Learning" (ICML 2011) — https://www.arxiv.org/abs/1103.4601
- Y. Saito et al., "Open Bandit Dataset and Pipeline: Towards Realistic and Reproducible Off-Policy Evaluation" (NeurIPS 2021 D&B) — https://arxiv.org/abs/2008.07146
- S. Künzel, J. Sekhon, P. Bickel, B. Yu, "Metalearners for estimating heterogeneous treatment effects using machine learning" (PNAS 2019) — https://arxiv.org/abs/1706.03461
- I. Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data" (arXiv 2406.18665, 2024) — https://arxiv.org/abs/2406.18665
- D. Ding et al., "Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing" (ICLR 2024) — https://arxiv.org/abs/2404.14618
- Q. Hu et al., "RouterBench: A Benchmark for Multi-LLM Routing Systems" (arXiv 2403.12031, 2024) — https://arxiv.org/pdf/2403.12031
- "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World" (arXiv 2608.08239, 2026) — https://arxiv.org/html/2608.08239
- "UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing" (arXiv 2605.18796, 2026) — https://arxiv.org/html/2605.18796
- "A Linear Expectation Constraint for Selective Prediction and Routing with False-Discovery Control" (arXiv 2512.01556, 2025) — https://arxiv.org/html/2512.01556v2
- Y. Geifman, R. El-Yaniv, "Selective Classification for Deep Neural Networks" (NeurIPS 2017) — https://arxiv.org/abs/1705.08500v2
- H. Mozannar, D. Sontag, "Consistent Estimators for Learning to Defer to an Expert" (ICML 2020) — https://arxiv.org/abs/2006.01862
- S. Kaufman, S. Rosset, C. Perlich, O. Stitelman, "Leakage in Data Mining: Formulation, Detection, and Avoidance" (ACM TKDD 2012) — https://dl.acm.org/doi/10.1145/2382577.2382579 ; PDF mirror https://www.cs.umb.edu/~ding/history/470_670_fall_2011/papers/cs670_Tran_PreferredPaper_LeakingInDataMining.pdf
- M. Mitchell et al., "Model Cards for Model Reporting" (FAT* 2019) — https://arxiv.org/abs/1810.03993
- D. Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NIPS 2015) — https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- E. Breck et al., "The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction" (IEEE BigData 2017) — https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/ ; PDF https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf
- Spotify Research, "Calibrated Recommendations with Contextual Bandits on Spotify Homepage" (2025) — https://research.atspotify.com/2025/9/calibrated-recommendations-with-contextual-bandits-on-spotify-homepage
- J. McInerney et al., "Explore, Exploit, Explain: Personalizing Explainable Recommendations with Bandits" (RecSys 2018) — https://research.atspotify.com/publications/explore-exploit-explain-personalizing-explainable-recommendations-with-bandits
- Q. Luo et al., "An Empirical Analysis of Flaky Tests" (FSE 2014) — https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf
- OpenAI, "Introducing SWE-bench Verified" (2024) — https://openai.com/index/introducing-swe-bench-verified/
- C. Northcutt, L. Jiang, I. Chuang, "Confident Learning" (JAIR 2021) — https://arxiv.org/abs/1911.00068
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021) — https://arxiv.org/abs/2103.14749
- O. Chapelle, "Modeling delayed feedback in display advertising" (KDD 2014) — https://dl.acm.org/doi/10.1145/2623330.2623634
- Microsoft Azure Architecture Center, "Event Sourcing pattern" — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- SQLite, "PRAGMA statements" / "Write-Ahead Logging" — https://www.sqlite.org/pragma.html ; https://www.sqlite.org/wal.html
- Sample-size arithmetic (McNemar paired proportions; α=0.05 two-sided, power 0.80): computed by the reviewer; table in ADRL-LRN-002 attack 3. Not an external source.
- D. Madras, T. Pitassi, R. Zemel, "Predict Responsibly" (NeurIPS 2018) — named in the brief, not fetched; not relied on.
