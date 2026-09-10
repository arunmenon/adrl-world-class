# State of the field, September 2026

Positioning note for a harness-side routing layer for coding agents. Every claim ends with a source tag; "fetched" means the page was retrieved and read, "search-only" means the claim rests on a search-result snippet and was not independently opened.

## (a) LLM routing for agentic coding

The 2026 literature has split routing into two problems, and only one of them is where the gains are. Static prompt-only routers have hit a ceiling: across 21 methods and five benchmarks, routers converge into a narrow band far below the oracle because they learn global model-quality averages rather than instance-specific signals; on RouterBench the top 15 routers differ by 0.23 points [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587, fetched]. A 400K-instance unified benchmark found several recent approaches, including commercial routers, fail to reliably beat a simple baseline, with the oracle gap driven by model-recall failures [source: LLMRouterBench, 2026, https://arxiv.org/abs/2601.07206, fetched]. Worse, the oracle itself is overstated: selecting the best fixed model on the same examples invalidates paired inference, and once selection-valid intervals are used the strongest deployable prompt router recovers only 7.5 to 14.4 percent of a 9.7 to 30.7 point oracle gap, with eleven policies' simultaneous interval touching zero [source: Opportunity Is Not Realizability, 2026, https://arxiv.org/abs/2608.08265, fetched].

The gains come from conditioning on execution. SWE-Router lets a cheap model run exploratory turns and routes on the partial trajectory, with a Bayes-optimality argument that trajectory conditioning never hurts [source: SWE-Router, ICML DL4C 2026, https://arxiv.org/abs/2607.00053, fetched]. Agent-as-a-Router frames routing as a context-action-feedback loop with a verifier and memory, and ships CodeRouterBench (about 10K instances, 8 frontier models) [source: Agent-as-a-Router, 2026, https://arxiv.org/abs/2606.22902, fetched]. MTRouter learns turn-level utility from logged trajectories and cuts cost 43 to 59 percent versus GPT-5 on ScienceWorld and HLE, while making fewer switches [source: MTRouter, ACL 2026, https://arxiv.org/abs/2604.23530, fetched]. TRACE-Router assigns one model per task at admission and learns from terminal reward, beating the best single model on Terminal-Bench by 7.1 points at 36 percent lower latency, and argues that not switching mid-workflow is what makes credit assignment possible [source: TRACE-Router, 2026, https://arxiv.org/abs/2607.22465, fetched]. Scrouting's ablation is the sharpest caution: with a 7B scout producing a verified handoff, the cheapest fixer alone matched the best single model on SWE-bench Pro Python at a fifth of the cost, so "the handoff rather than the routing decision carries the result" [source: Scrouting, 2026, https://arxiv.org/abs/2608.04804, fetched]. TwinRouterBench now pairs a static prefix track with a live 500-case SWE-bench dynamic track precisely because static scores do not settle live outcomes [source: TwinRouterBench, 2026, https://arxiv.org/abs/2605.18859, fetched].

Vendors converged on the same shape. Copilot's auto mode weighs availability plus reasoning, code-generation complexity, bug-diagnosis difficulty and tool-orchestration needs, routes "along natural cache boundaries" because mid-session switching "has shown increased cost without ample improvements in quality", gives a 10 percent discount, and offers policy exclusions for residency and FedRAMP but no local or on-prem target [source: About Copilot auto model selection, 2026, https://docs.github.com/copilot/concepts/auto-model-selection, fetched; changelog 2026-05-20, https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code/, fetched]. Cursor Router (July 22, 2026) exposes Intelligence, Balance and Cost dials and hides the routed model by default [source: Cursor Router changelog, 2026, https://cursor.com/changelog/router, fetched]; the "600K requests, 60 percent lower cost" figures circulate only in third-party write-ups [source: explainx.ai, 2026, https://www.explainx.ai/blog/cursor-router-auto-model-selection-july-2026, search-only]. Kiro's Auto is a 1.0x credit baseline with a pool from GPT-5.6 to Qwen3 Coder Next, and users file issues asking which model was used [source: Kiro Models docs, 2026, https://kiro.dev/docs/models/, fetched; Kiro issue #8903, search-only]. OpenRouter's Auto Beta classifies into task types and ranks models by community spend over a trailing seven-day window with a cost_tier dial [source: OpenRouter model routing blog, 2026-06-12, https://openrouter.ai/blog/insights/model-routing/, fetched]. Not Diamond Code routes per turn on session state, task complexity and "the state of the KV cache", may stay on an expensive model to keep a warm cache, and claims 39 percent savings on Poly-SWE-Bench through a local proxy [source: Not Diamond Code, 2026-08-04, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents, fetched]. vLLM's session-aware router hard-locks switches during tool loops and reports a 79 percent switch reduction across 21,600 turns [source: vLLM SAAR blog, 2026-06-02, https://vllm.ai/blog/2026-06-02-session-aware-agentic-routing, fetched].

## (b) Local models for coding in 2026

Open weights are close to frontier on public benchmarks but the reliability story is quantisation and tool calling. Qwen3-Coder-Next (80B total, 3B active, Apache 2.0, February 2026) reports 70.6 SWE-bench Verified, 44.3 SWE-bench Pro and 36.2 Terminal-Bench 2.0 [source: Qwen3-Coder-Next model card, 2026, https://huggingface.co/Qwen/Qwen3-Coder-Next, fetched]. DeepSeek V4-Pro (1.6T/49B active) and V4-Flash (284B/13B) shipped April 24, 2026 with 1M context and open weights [source: DeepSeek V4 release, 2026, https://api-docs.deepseek.com/news/news260424/, fetched]. Gemma 4 spans E2B to 31B dense under Apache 2.0 with native function calling and LiveCodeBench v6 up to 80.0 [source: Gemma 4 model card, 2026, https://ai.google.dev/gemma/docs/core/model_card_4, fetched]. Devstral 2 (123B, 72.2 Verified) and Devstral Small 2 (24B, 68.0) are reported in secondary sources only [source: Local AI Master Devstral review, 2026, https://localaimaster.com/models/devstral, search-only].

On real workloads, a 600-call-per-model MCP study at Q4_K_M found 93 to 97 percent well-formed calls for Gemma 4 27B, Qwen3-Coder 30B and Llama 3.3 70B, but "Q3 and below degrade tool-call reliability before they degrade chat quality" [source: Best Local Tool-Calling Models 2026, https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026, fetched]. A June 2026 feasibility review judged local agentic coding "possible" but workload-dependent, named tool-calling stability as the main failure mode, did not test real repositories, and recommended a golden set of 50 to 200 own tasks [source: Agentic Coding With Local LLMs, 2026, https://braindetox.kr/en/posts/local_llm_agentic_coding_2026.html, fetched]. No peer-reviewed local-versus-cloud study on private repositories was found; the Replay Gap paper's note that FP8-served controls diverged on 90 percent of forks while AWQ did not is the closest published evidence that serving configuration changes agent behaviour [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239, fetched].

## (c) Privacy and data residency

Anthropic's ZDR for Claude Code is per-organisation, requires separate enablement, excludes third-party MCP data, disables cloud sessions and artifacts, and Fable 5.x models "require data retention by default" under Covered Models policy [source: Zero data retention, Claude Code docs, 2026, https://code.claude.com/docs/en/zero-data-retention, fetched]. Enterprise Frontier Safeguards (September 2, 2026) moves safety monitoring onto customer-controlled cloud and sends signals to customers to review, so verification burden shifts to the enterprise [source: The Register, 2026-09-02, https://www.theregister.com/ai-and-ml/2026/09/02/anthropic-promises-zero-data-retention-but-customers-must-check-it-worked/5293789, fetched]. OpenAI announced ZDR for frontier models with Private Safety Processing on August 21, 2026 [source: OpenAI, 2026, https://openai.com/index/offering-zero-data-retention-for-frontier-models/, search-only]. US-only inference carries a 1.1x multiplier on the Claude API [source: Anthropic pricing docs, 2026, https://platform.claude.com/docs/en/about-claude/pricing, fetched]. Under the EU AI Act, GPAI provider obligations and Article 50 transparency took effect August 2, 2026; the Digital Omnibus (Regulation 2026/1744) pushed Annex III high-risk duties to December 2, 2027 and Annex I to August 2, 2028; deployer AI-literacy duties have applied since February 2025 [source: SIG EU AI Act summary, 2026, https://www.softwareimprovementgroup.com/blog/eu-ai-act-summary/, fetched]. Bank adoption figures (JPMorgan 40,000 developers on assistants, Bank of America 18,000 on Copilot) appear only in secondary reporting [source: LLRX AI in Finance, 2026, https://www.llrx.com/2026/04/ai-in-finance-and-banking-april-30-2026/, search-only].

## (d) Cost dynamics

Cache reads are now 0.1x base input on most Claude models and 0.025x on Fable 5.1 and Mythos 5.1; writes are 1.25x (5 minute) and 2x (1 hour); batch is 50 percent off and stacks with caching; Sonnet 5's introductory price became permanent on September 1, 2026; 4.7-and-later tokenizers emit about 30 percent more tokens [source: Anthropic pricing docs, 2026, https://platform.claude.com/docs/en/about-claude/pricing, fetched]. OpenAI cached input is about 10 percent of list and default cache retention moved to 24 hours on May 29, 2026 [source: Morph OpenAI pricing, 2026, https://www.morphllm.com/openai-api-pricing, search-only; Effloow cache retention, 2026, search-only]. The consequence for routing is structural: a switch pays a cache write on the new model and forfeits reads on the old one, which is why Copilot, Not Diamond and vLLM all route at cache boundaries.

## (e) Enterprise AI gateways

LiteLLM routes on simple-shuffle, least-busy, usage, latency and cost, with context-window and region pre-call filters and content-policy fallbacks; "no strategies condition on prompt content or task difficulty" [source: LiteLLM routing docs, 2026, https://docs.litellm.ai/docs/routing, fetched]. Portkey's conditional routing evaluates metadata, request parameters and URL path only, with primitive values and two-segment keys [source: Portkey conditional routing, 2026, https://portkey.ai/docs/product/ai-gateway/conditional-routing, fetched]. Kong's AI Proxy Advanced adds semantic and consistent-hash balancing, enterprise-only [source: Kong AI Proxy Advanced, 2026, https://developer.konghq.com/plugins/ai-proxy-advanced/, fetched]. Cloudflare AI Gateway is edge-only and documented as incompatible with Regional Services [source: Kosmoy, 2026-07-15, https://www.kosmoy.com/resources/blog/cloudflare-ai-gateway-alternatives/, fetched]. Bedrock intelligent prompt routing picks between exactly two models of one family, is English-only, and "can't adjust routing decisions or responses based on application-specific performance data" [source: AWS Bedrock docs, 2026, https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html, fetched]. Azure's model router (version 2025-11-18) routes across OpenAI, Anthropic, xAI, DeepSeek and Meta with Quality, Balanced and Cost modes, honours data zones, supports tools in Foundry Agent Service, but its context window is capped by the smallest pooled model, routing is text-only, and cache benefit exists "only when the same model handles consecutive requests" [source: Microsoft Learn model router concepts, updated 2026-09-01, https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router, fetched].

What none of these does, and a harness-side layer can: see the local decision (none has a local rung as a target), gate on secrets in tool results before egress, hold a durable per-session pin, learn from the organisation's own verified outcomes (Bedrock disclaims this explicitly), route on the partial trajectory rather than the prompt, and keep an egress ledger the enterprise can audit under the new ZDR-with-verification regime.

# EVL critique

**Bucket paragraph.** The EVL bucket is the most research-aligned bucket in the register, largely because it was written on 2026-09-03 with the Replay Gap paper and the review's power arithmetic in hand. Its central commitments, live branches over replay, exclusions before metrics, blockers outside the score, and human graduation on named evidence, each have direct 2026 support. The gaps are of two kinds. First, the bucket imports the routing literature's own weakest habit: EVL-001's "best single model repriced over the window" is a comparator selected on the evaluation data, which the selection-validity work shows inflates every paired claim. Second, three decisions were written before the field's newest distinction landed: static routers plateau, trajectory-conditioned routers do not, and shadow mode cannot evaluate a router because the shadow decision never executes. EVL-004 counts labels when what is scarce is discordance; EVL-007's D3 rung certifies a decision that has never been served; EVL-006 omits runs, seeds, harness and serving configuration that the harness-variance papers show dominate model choice. All nine remain sound in direction.

### ADRL-EVL-001: Baseline set: four fixed comparators, two price bases

One line: every evaluation reports against always-local, always-frontier, the current heuristic and the best single cloud model repriced over the window, at after-cache and list prices, as a versioned artifact.

**FOR.** A fixed comparator set is exactly what independent benchmarking says is missing: commercial routers "fail to reliably outperform a simple baseline" when a unified comparator is imposed [source: LLMRouterBench, 2026, https://arxiv.org/abs/2601.07206, fetched]. The two price bases match provider reality, with cache reads at 0.1x or 0.025x and writes at 1.25x to 2x [source: Anthropic pricing docs, 2026, https://platform.claude.com/docs/en/about-claude/pricing, fetched]. Vendors now route at cache boundaries because switching costs more than it gains [source: About Copilot auto model selection, 2026, https://docs.github.com/copilot/concepts/auto-model-selection, fetched], so charging the switch, as attack 3 answers, is current practice. Azure's own guidance tells buyers to "compare model router with your current baseline" before trusting managed routing [source: Microsoft Learn model router concepts, 2026, https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router, fetched].

**AGAINST.** Comparator 3 is chosen on the same window it is evaluated on. "Testing against a best fixed model selected on the same examples invalidates paired inference", and a full-information oracle "sees outcomes no deployable router observes"; with selection-valid intervals the realisable share of the oracle gap is 7.5 to 14.4 percent and the simultaneous interval for eleven policies has lower limit zero [source: Opportunity Is Not Realizability, 2026, https://arxiv.org/abs/2608.08265, fetched]. The decision's attack 2 addresses the counterfactual problem but not the selection problem. Separately, the comparator set has no trajectory-conditioned baseline; a cheap-model-then-escalate policy is the strongest deployable competitor in 2026 [source: SWE-Router, 2026, https://arxiv.org/abs/2607.00053, fetched], and a scout-plus-cheapest-fixer ablation matched the best single model at a fifth of the cost with no router at all [source: Scrouting, 2026, https://arxiv.org/abs/2608.04804, fetched]. "Beats both bounds" is therefore necessary but weak.

**Grounding verdict.** CONTESTED. Newest source 2026.

**Recommendation.** Amend: comparator 3 is selected on the previous window (or pre-registered) and re-priced on the evaluation window; report a selection-valid interval when it is not. Add a fifth comparator, "always-local with mechanical escalation at the CAS trip-wires", so the learned artifact is measured against the best deployable non-learned policy, not just the bounds.

### ADRL-EVL-002: Holdout and calibration protocol: temporal, session-grouped, tier-1 only

One line: metrics come from a later-in-time, session-grouped, tier-1 holdout with session-bootstrap intervals, reliability diagrams and abstention coverage, and report "insufficient" below a declared minimum.

**FOR.** Paired designs on the same items are the recommended discipline, with clustered standard errors and power analysis up front [source: Adding Error Bars to Evals, 2024, https://arxiv.org/abs/2411.00640, fetched]; the paired McNemar required N is a median 2.15x smaller than unpaired formulas, and 11 of 40 leaderboard comparisons are unresolved at conventional power [source: Resolution Diagnostics for Paired LLM Evaluation, 2026, https://arxiv.org/abs/2605.30315, fetched]. Time-ordered holdouts are the standard answer to leakage, and "no passive backtest can separate" skill from recency, so naming harness and model versions per window (attack 2) is the right mitigation [source: Temporal Leakage in LLM Backtesting, 2026, https://arxiv.org/abs/2608.02985, fetched]. Label error at the few-percent level reverses rankings, which justifies tier-1 only [source: Pervasive Label Errors, 2021, https://arxiv.org/abs/2103.14749, search-only, as cited in MEM-009].

**AGAINST.** Session-level bootstrap with a handful of sessions is itself unreliable: CLT and resampling intervals "dramatically underestimate uncertainty" below a few hundred datapoints, and the recommended fallback is Bayesian [source: Position: Don't Use the CLT in LLM Evals, ICML 2025, https://arxiv.org/abs/2503.01747, fetched]. With 34 evaluated decisions and one verified task, a reliability diagram with any bin count is noise, and ECE on that sample is a number without meaning. A temporal split also does not guarantee absence of leakage, because temporal signals are format-dependent [source: Test of Time, ACL 2026, https://arxiv.org/abs/2509.00072, fetched]. The decision fixes `min_holdout_sessions` but not the minimum number of clusters for the bootstrap or the resolution ratio N/N* that would say whether a comparison could ever be resolved.

**Grounding verdict.** CURRENT. Newest source 2026.

**Recommendation.** Add a minimum cluster count for bootstrap intervals and a Bayesian interval below it; report the resolution ratio q = N/N* for every pairwise comparison next to the interval; defer reliability diagrams until discordant-pair count passes a pre-registered floor.

### ADRL-EVL-003: Branch protocol and replay prohibition

One line: counterfactual evidence comes only from live branches from a shared snapshot; replay or model substitution in stored transcripts is prohibited as evidence; off-policy estimates are admissible only after branch validation.

**FOR.** The cited study now reads in full: across about 900 rollouts, swaps exceeded control floors by 0.25 to 0.66 normalised edit distance, 74 to 77 percent of early swaps diverged at the first post-fork action against 6 to 35 percent for controls, only 3 percent of replayed states remained valid, and five outcome flips appeared in swap arms against zero in 359 control forks [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239, fetched]. Independent work reached the same design: TwinRouterBench added a live dynamic track because static prefix scoring does not settle whether a cheaper substitution keeps downstream completion [source: TwinRouterBench, 2026, https://arxiv.org/abs/2605.18859, fetched]. The harness itself is a larger source of variance than model choice, with ranking reversals by harness configuration, so any replay that fixes the harness to the logged one is scoring the wrong system [source: Stop Comparing LLM Agents Without Disclosing the Harness, 2026, https://arxiv.org/abs/2605.23950, fetched].

**AGAINST.** The load-bearing paper is a single-author preprint with six paired runs, and its own caveat matters for ADRL: "temperature-0 determinism is configuration-dependent", with FP8-served controls diverging on 90 percent of forks while AWQ-served ones held [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239, fetched]. The noise floor is therefore a property of the serving stack, and a local rung on quantised MLX or llama.cpp will have a different floor from a cloud rung; the decision requires "a same-model control" but not one per serving configuration. The field also still trains from logged trajectories with reported gains [source: MTRouter, ACL 2026, https://arxiv.org/abs/2604.23530, fetched], so a blanket prohibition must be careful to forbid replay as evidence without forbidding logs as training input; the text does this, but the golden test on `source=replay` rows could over-reject.

**Grounding verdict.** CURRENT. Newest source 2026.

**Recommendation.** Require the same-model control floor per serving configuration (model, precision, runtime) and record it on the branch study; keep the prohibition; state explicitly that logged trajectories may feed features and training but never an outcome label.

### ADRL-EVL-004: Label quantity and quality gate for retrieval and learned authority

One line: retrieval and learned components gain advisory authority only after pre-registered quantity, verifier-precision, representativeness and suppressed-fraction conditions are met.

**FOR.** Reliable ranking needs tasks with intermediate success rates: filtering to 30 to 70 percent historical success cut evaluation size 44 to 70 percent while preserving rank fidelity, and random sampling was unstable across seeds [source: Efficient Benchmarking of AI Agents, 2026, https://arxiv.org/abs/2603.23749, fetched]. That supports the representativeness clause and the answer to attack 2. Verifier precision as a precondition is supported by the retirement of SWE-bench Verified after 59.4 percent of 138 audited hard tasks proved flawed [source: SWE-bench Verified Retired, Pebblous summary of OpenAI, 2026, https://blog.pebblous.ai/blog/swe-bench-verified-retired/en/, fetched; OpenAI post, https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/, search-only].

**AGAINST.** The gate counts labels; what routing needs is discordance. Routers plateau because they "mainly learn global averaged model-performance trends rather than fine-grained query-specific routing signals" [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587, fetched]. Three hundred `task_capability` outcomes on which every rung agrees carry no routing information, and the paired test's power depends on discordant pairs, roughly 40 to 50 at n = 400 for 80 percent power [source: Eval Set Sizing, 2026, https://dev.to/gabrielanhaia/eval-set-sizing-the-statistical-power-math-behind-llm-ab-tests-4gpc, search-only; Resolution Diagnostics, 2026, fetched]. The four conditions never mention the ambiguous-band share or a minimum number of pairs where rungs disagree, so the gate can pass on a corpus that is uninformative for the estimand LRN-003 names.

**Grounding verdict.** CONTESTED. Newest source 2026.

**Recommendation.** Add a fifth condition: a pre-registered minimum count of verified pairs on which the rungs' outcomes differ, per slice, derived from the RTG-007 power target; report the ambiguous-band share next to `min_labels`.

### ADRL-EVL-005: Simulator and benchmark evidence is not organic evidence

One line: simulator, benchmark and synthetic evidence is a separate family, tier T4, reported separately, and may qualify mechanisms or bound claims but never establish reliability on the organisation's code.

**FOR.** The benchmark that anchored coding-agent claims was retired by its own author for contamination and flawed tests, with all major frontier models showing signs of training on solutions [source: SWE-bench Verified Retired, 2026, https://blog.pebblous.ai/blog/swe-bench-verified-retired/en/, fetched]. Terminal-Bench 2.1 had to repair 28 of 89 tasks for broken dependencies, tight budgets and instruction-test mismatch, and introduced continuous validation [source: Terminal-Bench 2.1 leaderboard, 2026, https://snorkel.ai/leaderboard/terminal-bench-2-1/, fetched]. Simulators lie in specific ways: reward-relevant perturbations cost about 40 points and transition perturbations about 30, and scale did not close the gap [source: When Simulation Lies, 2026, https://arxiv.org/abs/2605.11928, fetched]; a unified MDP view names observation, action, transition and reward gaps [source: The Sim-to-Real Gap of Foundation Model Agents, 2026, https://arxiv.org/abs/2606.07017, fetched]. Benchmarks conflate model and harness and grade against one reference solution [source: Position: Coding Benchmarks Are Misaligned, 2026, https://arxiv.org/abs/2606.17799, fetched].

**AGAINST.** Contamination-resistant benchmarks now exist: SWE-bench Pro's private set draws on 18 proprietary codebases that trainers cannot legally access [source: SWE-bench Pro leaderboard, Scale, 2026, https://labs.scale.com/leaderboard/swe_bench_pro_private, search-only]. A private-repository benchmark run through the organisation's own harness is arguably closer to organic than the register's single-user corpus, and domain randomisation shows synthetic evidence can transfer to unseen failure classes [source: When Simulation Lies, 2026, fetched]. The decision's "never admit" is stricter than the field's practice and stricter than needed; the real defect is that the decision does not require harness-version and benchmark-version disclosure on any benchmark number, although harness effects exceed model effects [source: Stop Comparing LLM Agents Without Disclosing the Harness, 2026, fetched].

**Grounding verdict.** CURRENT. Newest source 2026.

**Recommendation.** Keep the family separation; require every synthetic figure to carry benchmark version, harness version and run count; allow a benchmark run through ADRL's own harness on a private task set to serve as a bound that can prune rungs and to size the organic pilot, still never as admission.

### ADRL-EVL-006: Offline evaluation against baselines, branched or propensity-weighted

One line: before graduation, an artifact receives a six-item report (baseline version, holdout protocol, branch-only counterfactuals, excluded and tier mix, minimum realised gain, manifest hash) and an incomplete report cannot be presented.

**FOR.** Evaluation reporting is moving from prose cards to composed, machine-readable records tying benchmark metadata, run data and model metadata, with reproducibility, completeness, provenance and comparability signals, applied at scale to 101,843 results [source: Evaluation Cards, 2026, https://arxiv.org/abs/2606.09809, fetched]. STREAM's reporting template for model reports pushes the same direction [source: STREAM, 2025, https://arxiv.org/abs/2508.09853, fetched]. Hashing the report into the manifest is the versioned-artifact practice model cards are moving toward.

**AGAINST.** The six items omit what the 2026 variance work says dominates: run count and seeds, harness version, and serving configuration. Absolute scores degrade under scaffold shift while rank order survives [source: Efficient Benchmarking of AI Agents, 2026, https://arxiv.org/abs/2603.23749, fetched], so the report must say whether it claims a rank or a magnitude. Item 1 inherits EVL-001's selection problem. The word "offline" still invites replay even with EVL-003 in place; TwinRouterBench's vocabulary of static and dynamic tracks is cleaner [source: TwinRouterBench, 2026, fetched]. The lightweight path for parameter-only changes has no independent support and is the kind of shortcut the harness papers warn about.

**Grounding verdict.** CURRENT. Newest source 2026.

**Recommendation.** Add items 7 to 9: run count and seeds with per-run spread; harness and serving configuration per rung; the claim type (rank versus magnitude) and its resolution ratio. Rename to "pre-exposure evaluation report" and give it a machine-readable header in the Evaluation Cards style.

### ADRL-EVL-007: Explicit human graduation and the D2 to D5 ladder

One line: maturity moves one rung at a time on named evidence by a recorded human decision, artifacts need a signature from a key outside the training team, and a new implementation inherits nothing above D2.

**FOR.** Canarying with a concurrent control, a dozen stack-ranked metrics and explicit limits on what canaries detect is the reference discipline [source: Google SRE, Canarying Releases, https://sre.google/workbook/canarying-releases/, fetched]. Progressive delivery with shadow, 1 percent canary, consistent user assignment and automated rollback thresholds is 2026 practice for LLM releases [source: Releasing AI Features Without Breaking Production, 2026, https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing, fetched]. Safety cases are moving to continuously updated forms tied to performance indicators rather than one-time gates [source: Dynamic safety cases for frontier AI, 2024, https://arxiv.org/abs/2412.17618, fetched]. The "no inheritance" rule matches the identity-stable canary principle that "the agent you certified is still the agent you have" [source: ICAN-Deploy, 2026, https://arxiv.org/abs/2605.28097, fetched].

**AGAINST.** D3 as written certifies a router on evidence that cannot exist. A shadow router records a decision but never executes it, so the shadow window measures decision distribution and gate behaviour, not outcome; the Replay Gap result means a shadow decision's counterfactual outcome is unknown until branched [source: The Replay Gap, 2026, fetched]. Canaries "cannot reliably detect state-dependent regressions" or shared-infrastructure failures [source: Google SRE, fetched], which for a router means a pilot with no concurrent control and no declared guardrail metrics is a before-and-after comparison, the design SRE warns against. Microsoft's platform makes ship decisions on pre-defined guardrail metrics, not a single score [source: A/B Testing Infrastructure Changes at Microsoft ExP, 2024, https://www.microsoft.com/en-us/research/articles/a-b-testing-infrastructure-changes-at-microsoft-exp/, fetched]; the D4 rung names a population but no control, duration or guardrails. One reviewer from a different reporting line is a weaker bar than any 2026 lab framework [source: Frontier Model Safety Analysis, 2026, https://futureagi.com/blog/frontier-model-safety-analysis-2026/, search-only].

**Grounding verdict.** CONTESTED. Newest source 2026.

**Recommendation.** Rewrite D3 evidence as "decision distribution, gate behaviour and plumbing on organic traffic, plus branch studies at the LRN-002 budget"; rewrite D4 as a controlled pilot with a concurrent control population, consistent assignment by session lineage, pre-declared guardrail metrics and a minimum duration in the EVL config.

### ADRL-EVL-008: Scorecard format: every number with its denominator, window and exclusions

One line: one fixed-structure scorecard per window with identity, denominators, exclusions-first, organic metrics with intervals, synthetic section, pairs, open blockers and ladder positions.

**FOR.** The field's diagnosis is that results are "reported inconsistently across leaderboards, model cards, benchmark papers, and company blogs" so that omissions cannot be seen, and the answer is a composed, machine-readable record [source: Evaluation Cards, 2026, https://arxiv.org/abs/2606.09809, fetched]. Vendors are going the other way: Cursor hides the routed model by default [source: Cursor Router changelog, 2026, fetched] and Kiro users cannot see which model answered [source: Kiro issue #8903, search-only], so a scorecard with served-rung denominators is a differentiator. Exclusions-first implements the register's denominator rule and matches the "disclose the harness" position [source: Stop Comparing LLM Agents Without Disclosing the Harness, 2026, fetched].

**AGAINST.** Section 1 names harness and model versions but not serving configuration, and precision and runtime change agent determinism [source: The Replay Gap, 2026, fetched]; a scorecard cannot compare two windows if the local rung silently moved from Q6 to Q4. Section 4 reports intervals but not the resolution ratio that says whether a difference could be detected at all [source: Resolution Diagnostics, 2026, fetched]. The scorecard is defined as a document; the Evaluation Cards work shows the value comes from a schema that tools can ingest and compare.

**Grounding verdict.** CURRENT. Newest source 2026.

**Recommendation.** Add serving configuration per rung to section 1 and the resolution ratio to section 4; publish the scorecard as JSON with a rendered view; add a "routed model visibility" line so the layer's transparency is itself measured.

### ADRL-EVL-009: Blockers are never averaged away

One line: eight pre-registered named conditions hold a decision at its rung regardless of score, are listed in every scorecard, and change only by config version with a reason.

**FOR.** Guardrail metrics that decide ship or no-ship independent of the headline metric are the established experimentation discipline [source: A/B Testing Infrastructure Changes at Microsoft ExP, 2024, fetched]. Compliance-first gating, where a regulatory violation fails the gate regardless of other dimensions, is 2026 agent-evaluation practice, with ISO 42001 and NIST AI RMF now embedded as gates in regulated sectors [source: LLM Evaluation in 2026, https://medium.com/@nairmilind3/llm-evaluation-in-2026-e631a78c67dc, search-only]. Frontier frameworks define capability thresholds that pause deployment until safeguards exist [source: Frontier Model Safety Analysis, 2026, search-only]. Blocker 2 is vindicated by the benchmark whose verifier turned out to be 59 percent wrong on hard tasks [source: SWE-bench Verified Retired, 2026, fetched].

**AGAINST.** Two blockers the literature would add are missing: a harness, model or serving-configuration change inside the window (the temporal confound EVL-002 only "splits" on) and a benchmark or harness disclosure gap for any synthetic figure. Dynamic safety cases pair each claim with a monitored indicator and a revision cadence rather than a static list [source: Dynamic safety cases, 2024, fetched]; the eight blockers have no re-check cadence, so a closed blocker stays closed until someone reopens it. Blocker 6 depends on OPS thresholds that do not exist, so it is currently unevaluable rather than open or closed, a third state the decision does not name.

**Grounding verdict.** CURRENT. Newest source 2026.

**Recommendation.** Add blockers 9 (version or serving-config change inside the window) and 10 (synthetic figure without harness and benchmark version); give each blocker a re-check cadence and an "unevaluable" state that is reported as open.

## Verdict tally

| Verdict | Decisions |
|---|---|
| CURRENT | EVL-002, EVL-003, EVL-005, EVL-006, EVL-008, EVL-009 |
| CONTESTED | EVL-001, EVL-004, EVL-007 |
| DATED | none |
| UNGROUNDED | none |

# Sources

Fetched pages are marked F; search-result-only sources are marked S.

- F. A. Gonuguntla, The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World, 2026. https://arxiv.org/abs/2608.08239
- F. S. Son et al., SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks, ICML DL4C 2026. https://arxiv.org/abs/2607.00053
- F. Y. Lu et al., The Routing Plateau, 2026. https://arxiv.org/abs/2606.07587
- F. H. Li et al., LLMRouterBench, 2026. https://arxiv.org/abs/2601.07206
- F. I. F. Shihab et al., Opportunity Is Not Realizability: Selection-Valid Diagnostics for Multi-LLM Routing, 2026. https://arxiv.org/abs/2608.08265
- F. P. Zhou et al., Agent-as-a-Router, 2026. https://arxiv.org/abs/2606.22902
- F. Y. Zhang et al., MTRouter, ACL 2026. https://arxiv.org/abs/2604.23530
- F. R. Raj et al., TRACE-Router, 2026. https://arxiv.org/abs/2607.22465
- F. I. Bhola et al., Scrouting, 2026. https://arxiv.org/abs/2608.04804
- F. P. Yang et al., TwinRouterBench, 2026. https://arxiv.org/abs/2605.18859
- S. LLMRouter: Unified Infrastructure, 2026. https://arxiv.org/abs/2608.06867
- F. A. Kotawala, Resolution Diagnostics for Paired LLM Evaluation, 2026. https://arxiv.org/abs/2605.30315
- F. E. Miller, Adding Error Bars to Evals, 2024. https://arxiv.org/abs/2411.00640
- F. S. Bowyer et al., Position: Don't Use the CLT in LLM Evals, ICML 2025. https://arxiv.org/abs/2503.01747
- S. Eval Set Sizing: The Statistical Power Math Behind LLM A/B Tests, 2026. https://dev.to/gabrielanhaia/eval-set-sizing-the-statistical-power-math-behind-llm-ab-tests-4gpc
- F. Z. Zhang, B. Stadie, Temporal Leakage in LLM Backtesting, 2026. https://arxiv.org/abs/2608.02985
- F. T. J. Zhang et al., Test of Time, ACL 2026. https://arxiv.org/abs/2509.00072
- S. C. Northcutt et al., Pervasive Label Errors in Test Sets, NeurIPS 2021. https://arxiv.org/abs/2103.14749
- F. F. Ndzomga, Efficient Benchmarking of AI Agents, 2026. https://arxiv.org/abs/2603.23749
- F. Y. Zhang et al., Stop Comparing LLM Agents Without Disclosing the Harness, 2026. https://arxiv.org/abs/2605.23950
- F. M. Gorinova et al., Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering, 2026. https://arxiv.org/abs/2606.17799
- F. Pebblous, SWE-bench Verified Retired, 2026. https://blog.pebblous.ai/blog/swe-bench-verified-retired/en/
- S. OpenAI, Why SWE-bench Verified no longer measures frontier coding capabilities, 2026. https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- S. Scale, SWE-Bench Pro leaderboards, 2026. https://labs.scale.com/leaderboard/swe_bench_pro_private and https://labs.scale.com/leaderboard/swe_bench_pro_public
- F. M. Merrill et al., Terminal-Bench, 2026. https://arxiv.org/abs/2601.11868
- F. Snorkel AI, Terminal-Bench 2.1 leaderboard, 2026. https://snorkel.ai/leaderboard/terminal-bench-2-1/
- F. X. Liu et al., The Sim-to-Real Gap of Foundation Model Agents, 2026. https://arxiv.org/abs/2606.07017
- F. X. Zhou et al., When Simulation Lies, 2026. https://arxiv.org/abs/2605.11928
- F. A. Ghosh et al., Evaluation Cards, 2026. https://arxiv.org/abs/2606.09809
- F. McCaslin et al., STREAM (ChemBio), 2025. https://arxiv.org/abs/2508.09853
- F. C. Cârlan et al., Dynamic safety cases for frontier AI, 2024. https://arxiv.org/abs/2412.17618
- F. X. Qin et al., ICAN-Deploy, 2026. https://arxiv.org/abs/2605.28097
- S. Frontier Model Safety Analysis 2026 (RSP, Preparedness, FSF). https://futureagi.com/blog/frontier-model-safety-analysis-2026/
- F. Google SRE, Canarying Releases. https://sre.google/workbook/canarying-releases/
- F. Microsoft Research, A/B Testing Infrastructure Changes at Microsoft ExP, 2024. https://www.microsoft.com/en-us/research/articles/a-b-testing-infrastructure-changes-at-microsoft-exp/
- F. MLflow, What Is Online Evaluation in ML: A 2026 Guide. https://mlflow.org/articles/what-is-online-evaluation-in-ml-a-2026-guide/
- F. TianPan, Releasing AI Features Without Breaking Production, 2026. https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing
- S. LLM Evaluation in 2026 (Medium). https://medium.com/@nairmilind3/llm-evaluation-in-2026-e631a78c67dc
- F. GitHub Docs, About Copilot auto model selection, 2026. https://docs.github.com/copilot/concepts/auto-model-selection
- F. GitHub Changelog, Auto model selection now routes based on your task in VS Code, 2026-05-20. https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code/
- F. Cursor, Cursor Router changelog, 2026-07-22. https://cursor.com/changelog/router
- S. explainx.ai, Cursor Router: Auto Model Selection, 2026. https://www.explainx.ai/blog/cursor-router-auto-model-selection-july-2026
- F. Kiro, Models docs, 2026. https://kiro.dev/docs/models/
- S. Kiro issue #8903, Show which model is used per response in Auto mode. https://github.com/kirodotdev/Kiro/issues/8903
- F. OpenRouter, How OpenRouter Model Routing Works, 2026-06-12. https://openrouter.ai/blog/insights/model-routing/
- F. Not Diamond, Not Diamond Code, 2026-08-04. https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents
- F. vLLM, Session-Aware Agentic Routing, 2026-06-02. https://vllm.ai/blog/2026-06-02-session-aware-agentic-routing
- F. Qwen, Qwen3-Coder-Next model card, 2026. https://huggingface.co/Qwen/Qwen3-Coder-Next
- F. DeepSeek, V4 Preview Release, 2026-04-24. https://api-docs.deepseek.com/news/news260424/
- F. Google, Gemma 4 model card, 2026. https://ai.google.dev/gemma/docs/core/model_card_4
- S. Local AI Master, Devstral 2 Review, 2026. https://localaimaster.com/models/devstral
- F. PromptQuorum, Best Local Tool-Calling Models 2026. https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026
- F. braindetox, Agentic Coding With Local LLMs, 2026. https://braindetox.kr/en/posts/local_llm_agentic_coding_2026.html
- F. Claude Code Docs, Zero data retention, 2026. https://code.claude.com/docs/en/zero-data-retention
- F. The Register, Anthropic promises zero data retention, 2026-09-02. https://www.theregister.com/ai-and-ml/2026/09/02/anthropic-promises-zero-data-retention-but-customers-must-check-it-worked/5293789
- S. OpenAI, Offering Zero Data Retention for frontier models, 2026. https://openai.com/index/offering-zero-data-retention-for-frontier-models/
- F. Anthropic, Pricing (platform docs), 2026. https://platform.claude.com/docs/en/about-claude/pricing
- S. Morph, OpenAI API Pricing 2026. https://www.morphllm.com/openai-api-pricing
- S. Effloow, OpenAI's 24h Prompt Cache, 2026. https://effloow.com/articles/openai-prompt-cache-retention-24h-cost-proof-2026
- F. SIG, A comprehensive EU AI Act Summary (August 2026 update). https://www.softwareimprovementgroup.com/blog/eu-ai-act-summary/
- S. LLRX, AI in Finance and Banking, April 30, 2026. https://www.llrx.com/2026/04/ai-in-finance-and-banking-april-30-2026/
- F. LiteLLM, Routing docs. https://docs.litellm.ai/docs/routing
- F. Portkey, Conditional routing docs. https://portkey.ai/docs/product/ai-gateway/conditional-routing
- F. Kong, AI Proxy Advanced plugin. https://developer.konghq.com/plugins/ai-proxy-advanced/
- F. Kosmoy, Cloudflare AI Gateway Alternatives, 2026-07-15. https://www.kosmoy.com/resources/blog/cloudflare-ai-gateway-alternatives/
- F. AWS, Understanding intelligent prompt routing in Amazon Bedrock. https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- F. Microsoft Learn, Model router for Microsoft Foundry concepts, updated 2026-09-01. https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router
