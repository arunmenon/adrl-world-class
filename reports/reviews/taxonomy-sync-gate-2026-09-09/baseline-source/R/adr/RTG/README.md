# RTG — Routing Intelligence and Economics

**Planning task-pack preparation, 2026-09-08:** [the next lab packet](../../reports/waves/lab-planning-deliverables.md) supplies draft PRD/HLD/LLD tasks and assessed-evidence contracts. Actual harness/mode execution, assessment calibration and any learning admission remain open. No runtime, decision text/status or maturity change is implied.

**W7.0a completed, 2026-09-08:** [mixed-intent routing correction](../../reports/adrl-routing-correction-2026-09-08.md) introduces features-v2 and explicit exploration compatibility protection. Two masking defects are corrected; lexical ambiguity/negation limits remain visible. All eleven checks pass: 911 tests passed, eight engine cases skipped, 322 stable inputs. Decision text/status/formal maturity and learning admission are unchanged. This was a bounded foreground implementation; hourly continuation remains paused. Earlier dated checkpoints below are preserved.

**Current Lab A.1 evidence, 2026-09-08:** [the synthetic routing workbench](../../reports/adrl-lab-first-run-2026-09-08.md) records tested scope for [RTG-002](ADRL-RTG-002.md). Actual decisions/dispatch and negative cases are inspectable; the engine and policy are unchanged. 894 tests passed, eight engine cases skipped, all eleven checks passed. Decision text/status/maturity and real-harness/learning gates remain unchanged. Only this bounded foreground slice restarted; hourly continuation stays paused. Earlier planning checkpoints below are historical.

**Product planning, 2026-09-08:** Decision-time context and completed-task benefit drive the proposed sequence; classification, comparative estimation and action selection have separate roles. See the [startup roadmap](../../reports/adrl-product-roadmap-2026-09-08.md) and [context-graph proposal](../../design/adrl-context-graph-memory-proposal-2026-09-08.md). Implementation remains paused; decision text, architectural status and maturity are unchanged.

**Planning checkpoint, 2026-09-08:** the user requested the target adaptive routing/RSI architecture before further implementation. [Blueprint](../../reports/adrl-adaptive-routing-rsi-blueprint-2026-09-08.md) and [all-ADR map](../../reports/research/adaptive-routing-blueprint-2026-09-08/taxonomy-map.md) are proposals for disposition. Implementation continuation is paused; no decision wording, status or maturity is changed by the blueprint.

**Routing diagnostic, 2026-09-08:** [24 task prompts under five conditions](../../reports/adrl-routing-in-action-2026-09-08.md) exercised the unchanged router, cascade and explicit rule-health refresh. The 240 decisions are synthetic component probes; 135 existing focused tests pass. Two mixed-intent review hypotheses fail. Model quality, savings, live refresh, learning admission and all maturity promotions remain unproved/unchanged. [Routing correction](../../reports/waves/routing-decision-quality.md) is held pending blueprint disposition; W3 capture work remains open.

**Core question:** Which permitted rung is the best choice?
**Owns / does not own:** Owns the runtime choice of rung, the utility/cost objective, uncertainty and abstention policy, and policy precedence inside the permitted set. Does not own what is forbidden (SAF), how a chosen rung executes or escalates (CAS), or how models are trained (LRN).

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-RTG-001 | Three capability rungs with measured boundaries | AMEND | D3 Shadow → D3 Shadow (local boundary flagged unmeasured) | Three is defensible; rungs must carry measured boundaries and reasoning effort must be declared a within-rung parameter, not a hidden fourth rung. |
| ADRL-RTG-002 | Cheapest rung likely to complete, defined | AMEND | D2 Tested → D2 Tested | Neither "likely" nor "cheapest" was defined; now a thresholded named estimator and session-marginal cost including cascade and cache. |
| ADRL-RTG-003 | Rules own clear cases, measured | AMEND | D3 Shadow → D3 Shadow | "Clear" was defined by the rules themselves (unfalsifiable); now a versioned band with measured, revocable precision. |
| ADRL-RTG-004 | Local-first only with a bounded, clean cascade | AMEND | D2 Tested → D2 Tested | Conflicted with SAF-004 on pinned sessions; feasibility must include side-effect recoverability and a capped attempt. |
| ADRL-RTG-005 | Objective: verified quality, retry, latency, session cost | AMEND | D3 Shadow → **D2 Tested** | Cache was in the rationale but not the decision; terms unweighted; inputs are shadowed but the objective was never baselined. |
| ADRL-RTG-006 | Advisory LLM classifier, gated and bounded | AMEND | D3 Shadow → D3 Shadow | The classifier *call* is itself a route (pin leak); fallback for the middle band was unnamed; no latency/cost budget. |
| ADRL-RTG-007 | Marginal-utility target, with a build gate | AMEND | D0 Design → D0 Design | Right target; benchmarks show learned routers often fail to beat best-single-model, so a pre-build gate and abstention-first sequencing are required (Q4). |
| ADRL-RTG-008 | Rung vs endpoint, with a leak contract | AMEND | D2 Tested → D2 Tested | Separation is right but leaks through per-model caches and reasoning signatures; a gateway contract (served identity, within-rung stability, shared membership) is the Q7 boundary. |
| ADRL-RTG-009 | Session-marginal, cache-aware cost accounting | PROPOSED (new) | — → D0 Design | Three RTG decisions depend on a cost unit none defines; the register's own open item names the gap. |

Tally: 8 AMEND, 0 APPROVE, 0 REJECT, 1 PROPOSED. No decision was rejected because in every case the *principle* survived the attacks; the defects were under-specification (undefined operative terms), register/code drift, and cross-bucket conflicts.

## Cross-cutting findings

1. **The bucket has no cost unit.** RTG-002 ("cheapest"), RTG-005 ("cost") and RTG-007 ("marginal utility") each depend on a definition of cost that none of them gives, while Phase 0's strongest finding (very high prompt-cache hit ratio) and provider pricing (cache reads at 0.1×/0.025× base, writes at 1.25–2×, caches per model) make per-turn list price the wrong unit by an order of magnitude on long transcripts. Two shipping coding-agent routers (GitHub Copilot auto selection, Not Diamond Code) have independently converged on session-level, cache-boundary-aware objectives. RTG-009 is proposed to give the bucket one shared definition; RTG-002/005/007 are amended to cite it.

2. **Several decisions were unfalsifiable as written.** "Likely to complete", "clear cases", and a four-term objective with no weights can each be implemented two opposite ways and both implementations would be "compliant". Every amendment in this bucket adds a named estimator, a versioned threshold, or a measured precision so that the decision can be *wrong* in a way MEM can record — which is what FND-005 and tenet 8 require of the rest of the register.

3. **The learned-router upside is an open empirical question, not a deferred build.** Independent benchmarks (RouterBench 2024; LLMRouterBench 2026, 33 models / 400k instances) report that predictive routers frequently fail to beat the best single model and that a commercial router scored −24.7% against it; cascade-routing theory reports gains of only 1–4% on RouterBench that narrow further as estimator noise rises; the project's own corpus says the ambiguous band is a minority and counterfactual pairs are scarce. RTG-007 is amended to carry a pre-build gate (band share, oracle-bound gain, minimum realised gain vs three baselines after cache effects) and to require abstention (LRN-006) before any authority. This is the review's answer to Q4: keep it simple and cache-aware first, and state the bar.

4. **Reasoning effort is an unacknowledged routing axis.** Frontier providers price thinking/effort as multiples; Not Diamond routes over "models and reasoning efforts". RTG-001 now declares effort a within-rung dispatch parameter so CAS stickiness and RTG-009 accounting stay rung-based; whether ADRL should ever *set* effort is left open and should be raised with the CAS/OPS owners.

5. **Cross-bucket conflicts found:** RTG-004 vs SAF-002/004 (local-first requires a cascade; pinned sessions have none) — resolved by an explicit carve-out with ledger marker. RTG-006 vs SAF-003 (a cloud classifier call on a flagged session is a leak) — resolved by binding classifier placement to the gates. RTG-007 vs LRN-003 (same decision, two texts) — resolved by making LRN-003 cite RTG-009 units and EVL baselines. RTG-008 vs CAS-006/OPS-006 (served-rung observability needs a gateway contract) — resolved by stating the contract; this is the concrete Q7 boundary.

6. **Maturity over-claim:** RTG-005 is the one decision in the bucket where D3 conflates *telemetry in shadow* with *an objective evaluated in shadow*; no baseline comparison on organic traffic exists (one verified task; 34/300 evaluated decisions). Recommend D2 until the Q6 comparison runs.

7. **What the review could not find:** no peer-reviewed work on LLM-routing cost under provider prompt caching (the 2026 survey lists it as absent), and no external evidence on the fraction of *coding-agent* turns that are routing-ambiguous beyond vendor claims. Both are stated as gaps in the affected files rather than filled with inference.

## Sources consulted

- Aggarwal, Madaan et al., "AutoMix: Automatically Mixing Language Models" (NeurIPS 2024) — https://arxiv.org/abs/2310.12963
- Anthropic, "Prompt caching" (Claude platform docs) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, "Thinking" (Claude platform docs) — https://platform.claude.com/docs/en/build-with-claude/thinking
- AWS, "Understanding intelligent prompt routing in Amazon Bedrock" — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- Chen, Zaharia, Zou, "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance" (arXiv 2023 / TMLR 2024) — https://arxiv.org/abs/2305.05176
- Chuang et al., "Learning to Route LLMs with Confidence Tokens" (ICML 2025) — https://arxiv.org/abs/2410.13284
- Dekoninck et al., "A Unified Approach to Routing and Cascading for LLMs" (arXiv 2024) — https://arxiv.org/abs/2410.10347
- Ding et al., "Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing" (ICLR 2024) — https://arxiv.org/abs/2404.14618v1
- "Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey" (arXiv 2026) — https://arxiv.org/html/2603.04445v2
- Geifman & El-Yaniv, "Selective Classification for Deep Neural Networks" (NeurIPS 2017) — https://papers.neurips.cc/paper/7073-selective-classification-for-deep-neural-networks
- GitHub Docs, "About Copilot auto model selection" — https://docs.github.com/copilot/concepts/auto-model-selection
- GitHub Changelog, "Copilot CLI auto model selection routes based on task" (2026-07-01) — https://github.blog/changelog/2026-07-01-copilot-cli-auto-model-selection-routes-based-on-task/
- Hu et al., "RouterBench: A Benchmark for Multi-LLM Routing System" (arXiv 2024) — https://arxiv.org/abs/2403.12031
- Kadavath et al., "Language Models (Mostly) Know What They Know" (arXiv 2022) — https://arxiv.org/abs/2207.05221
- Kiro docs, "Models" — https://kiro.dev/docs/models/ ; Kiro issues #8575, #8903 — https://github.com/kirodotdev/Kiro/issues/8575
- LiteLLM, "'Thinking' / 'Reasoning Content'" — https://docs.litellm.ai/docs/reasoning_content
- LLMRouterBench, "A Massive Benchmark and Unified Framework for LLM Routing" (arXiv 2026) — https://arxiv.org/html/2601.07206v1
- MCP blog, "Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do" (2026) — https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- Not Diamond, "Not Diamond Code: intelligent model routing for coding agents" (2026) — https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents
- Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data" (ICLR 2025) — https://arxiv.org/abs/2406.18665
- OpenAI, "Prompt caching" (API docs) — https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI, "Reasoning models" (API docs) — https://developers.openai.com/api/docs/guides/reasoning
- OpenHands, "Stuck Detector" (SDK docs) — https://docs.openhands.dev/sdk/guides/agent-stuck-detector
- OpenRouter, "Auto Router - Intelligent Model Selection" — https://openrouter.ai/docs/guides/routing/routers/auto-router
- OpenTelemetry, "Gen AI" semantic-convention attribute registry — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- RouteNLP, "Closed-Loop LLM Routing with Conformal Cascading and Distillation Co-Optimization" (arXiv 2026) — https://arxiv.org/abs/2604.23577
- Shi et al., "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge" (arXiv 2024) — https://arxiv.org/abs/2406.07791
- Shnitzer et al., "Large Language Model Routing with Benchmark Datasets" (arXiv 2023) — https://arxiv.org/pdf/2309.15789 (title located; not relied on for claims)
- Tran et al. (Katanemo), "Arch-Router: Aligning LLM Routing with Human Preferences" (arXiv 2025) — https://arxiv.org/abs/2506.16655 (consulted; preference-domain routing, not relied on for claims)
- Wataoka et al., "Self-Preference Bias in LLM-as-a-Judge" (NeurIPS 2024 workshop) — https://arxiv.org/abs/2410.21819
- Xiong et al., "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs" (ICLR 2024) — https://arxiv.org/abs/2306.13063
- Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering" (NeurIPS 2024) — https://arxiv.org/html/2405.15793
- "Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering" (arXiv 2026) — https://arxiv.org/html/2604.16790v1
