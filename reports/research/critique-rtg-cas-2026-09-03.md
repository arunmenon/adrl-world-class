# Research-grounded critique of ADRL RTG and CAS decisions

Date: 2026-09-03. Scope: adr/RTG/ADRL-RTG-001..009 and adr/CAS/ADRL-CAS-001..009 in /Users/arunmenon/projects/adrl-world-class. This review does not repeat the 2026-09-02 adversarial review; it asks whether each decision as it now reads is grounded in 2025-2026 research and practice. Every source below was either fetched in full (marked "fetched") or appeared as a titled search result whose title matched (marked "search-listed"). No other sources are used.

Verdict scale: CURRENT (decision matches the newest evidence), DATED (decision is right in spirit but its mechanism or constants lag the field), CONTESTED (newest evidence points the other way on a load-bearing clause), UNGROUNDED (no evidence either way).

---

# RTG - Routing Intelligence and Economics

## State of the field, 2026

Routing research moved in 2026 from single-turn prompt classifiers to trajectory-conditioned and step-level decisions inside agents. The Routing Plateau study of 21 routers found they converge far below the oracle because they learn global model averages, not instance signals; SWE-Router proved that conditioning on a cheap model's partial trajectory is Bayes-better than routing on the prompt; TwinRouterBench and the Replay Gap paper established that replayed transcripts score "the wrong world", so routers must be evaluated by live branching. Commercial practice converged on session-level, cache-aware decisions: GitHub Copilot's HyDRA routes only at cache boundaries and reports 72.5% savings; Not Diamond Code (August 2026) routes model and reasoning effort per step while weighing KV-cache state, sub-agent structure and compaction; OpenRouter pins model and provider per session id. Reasoning effort became a first-class per-step lever (Ares, TAB, DART). The Handoff Tax paper (August 2026) is the most consequential new result: escalating mid-trajectory recovers less than half the quality gap at a cost premium, while downshifting is favourable.

### ADRL-RTG-001: Three capability rungs with measured boundaries

Decision: three economic and service tiers (local, cheap cloud, frontier) with declared per-slice escalation edges, no total capability order, effort as a within-rung dispatch parameter.

**FOR**
- Adding candidates to a router has sharply diminishing returns and "larger ensembles exhibit diminishing returns compared to careful model curation", which supports a small, curated tier set rather than a per-model policy. [source: LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing, 2026, https://arxiv.org/abs/2601.07206; fetched]
- Agent-as-a-Router states that frontier LLMs "often excel at distinct domains, yet none dominate all", which is the empirical basis for the 2026-09-03 amendment removing the total capability order in favour of per-slice edges. [source: Agent-as-a-Router: Agentic Model Routing for Coding Tasks, 2026, https://arxiv.org/abs/2606.22902; fetched]
- Copilot's production router first "identifies models that can meet the quality bar for the task, then chooses the best fit among them", a tier-then-select shape close to ADRL's rung-then-endpoint split. [source: Getting more from each token: How Copilot improves context handling and model routing, 2026, https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/; fetched]
- Per-step effort selection is separable from model choice in current research (a lightweight router predicts "the lowest appropriate reasoning level for each step"), which is consistent with treating effort as a dispatch parameter rather than a rung. [source: Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents, 2026, https://arxiv.org/abs/2603.07915; fetched]

**AGAINST**
- The leading commercial coding router predicts "future rewards and costs for a given model and reasoning effort at each step" jointly; pushing effort down to the gateway removes the joint (model, effort) optimisation from ADRL's objective entirely. [source: Not Diamond Code: intelligent model routing for coding agents, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents; fetched]
- Effort is where most of the savings are: Ares cuts reasoning tokens "by up to 52.7% compared to fixed high-effort reasoning" and DART cuts thinking tokens 32-73%; a rung model that is blind to effort delegates the largest cost lever to a layer that RTG-008 says ADRL does not control. [source: DART: Draft-Agreement Routing for Training-Free Adaptive Thinking Budgets in Hybrid Reasoning Models, 2026, https://arxiv.org/abs/2606.23181; fetched]
- Effort is not protocol-neutral on Anthropic: at effort xhigh or max on Claude Opus 5 and later "thinking cannot be turned off" and the request returns a 400, and thinking blocks carry signatures; so a change of effort can change what the transcript contains, which the "not a rung change for sticky-state purposes" clause does not account for. [source: Thinking (Claude Platform Docs), 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- Handoff Tax finds downshifting "offers a favorable cost-quality point" while escalation does not, so the ladder's only well-evidenced traversal direction is the one the register's escalation edges do not declare. [source: The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents, 2026, https://arxiv.org/abs/2608.24358; fetched]

**Grounding verdict**: CONTESTED (newest relevant source 2026).

**Recommendation**: Keep three economic tiers and per-slice edges, but add effort to the registry as a second declared axis with its own escalation edges (for example local:none, cheap:low to cheap:high, frontier:medium) so RTG-005/009 can score effort changes and CAS-005 can decide whether an effort change is sticky. Declare downshift edges alongside escalation edges, because the 2026 evidence says downshift is the traversal that pays.

### ADRL-RTG-002: Cheapest rung likely to complete, defined

Decision: pick the cheapest healthy rung whose P(complete | rung, features) meets a versioned threshold, with cost measured as session-marginal cost including cascade and cache.

**FOR**
- Calibrated per-query error probabilities plus a cost-minimising threshold are cost-optimal under stated assumptions and beat FrugalGPT-style learned thresholds; UCCI "cuts inference cost by 31%" while "reducing ECE from 0.12 to 0.03", which is exactly the tau_rung construction with a calibration report. [source: UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing, 2026, https://arxiv.org/abs/2605.18796; fetched]
- Conformal cascades give "probabilistic guarantees on inference costs relative to a user-defined budget" from unlabeled outputs and small calibration sets, so a thresholded cascade can carry a cost guarantee even at ADRL's low label volume. [source: C3PO: Optimized Large Language Model Cascades with Probabilistic Cost Constraints for Reasoning, 2025, https://arxiv.org/abs/2511.07396; fetched]
- Copilot's HyDRA applies a quality bar first and then chooses the best fit, achieving "72.5% cost savings" on a five-model pool; the shape of RTG-002 is in production at scale. [source: Getting more from each token, 2026, https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/; fetched]

**AGAINST**
- The estimator is the weak link and 2026 says prompt features cannot fix it: "a similar issue can hide either a localized typo or a multi-module refactor, and the prompt does not separate the two", and conditioning on a short partial trajectory "never harms routing and is strictly better whenever exploration is informative". RTG-002's P(complete) is prompt-conditioned. [source: SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks, 2026, https://arxiv.org/abs/2607.00053; fetched]
- Across 21 methods routers "converge to a narrow performance range that remains far below the oracle router" because they "learn global averaged model-performance trends rather than fine-grained query-specific routing signals"; a versioned tau over band heuristics is a global-average router by construction. [source: The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers, 2026, https://arxiv.org/abs/2606.07587; fetched]
- Clause 2 charges the cascade's token cost but not its quality cost: "full-trajectory escalation recovers less than half of the LC-to-HC quality gap while incurring a substantial cost premium". A cheap attempt that fails is not made whole by escalating. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]
- Budget-conditioned benchmarks show agents fail in both directions, "either stopping before warranted escalation or overspending on cheap tasks", with at most 7.3% economic consistency, so a single threshold per rung will be wrong on one side unless the threshold is scored on both under- and over-escalation. [source: EcoAgent-Bench: Evaluating Economic Decision-Making in Budget-Constrained LLM Agents, 2026, https://arxiv.org/html/2608.05519; fetched]

**Grounding verdict**: CONTESTED (2026).

**Recommendation**: Keep the thresholded form but state that P(complete) is re-estimated at each CAS-003 boundary from the partial trajectory, not only at the user turn, and add an expected-quality-loss-on-cascade term next to the cascade cost term. Report tau's error split into under-escalation and over-escalation as EcoAgent-Bench does.

### ADRL-RTG-003: Rules own clear cases, measured

Decision: deterministic rules own versioned, precision-gated clear bands; learned intelligence is reserved for a measured ambiguous band.

**FOR**
- "Many routing methods exhibit similar performance under unified evaluation, and several recent approaches, including commercial routers, fail to reliably outperform a simple baseline", which is the strongest 2026 support for keeping rules as the default. [source: LLMRouterBench, 2026, https://arxiv.org/abs/2601.07206; fetched]
- The Routing Plateau shows kNN and trained routers land in the same band, so a simple rule set forfeits little on the queries routers can solve at all. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587; fetched]
- Declarative "Domain and Action" route policies supplied as context to a 1.5B model reach 93.17% routing accuracy and beat proprietary models on multi-turn benchmarks, which shows that user-authored, versioned policy (the same shape as ADRL's bands) is competitive with learned routing. [source: Arch-Router: Aligning LLM Routing with Human Preferences, 2025, https://arxiv.org/abs/2506.16655; search-listed]
- Copilot's production router evaluates "reasoning, code generation complexity, bug diagnosis difficulty, and tool orchestration needs", a small coarse taxonomy consistent with rules on coarse structure. [source: Copilot CLI auto model selection routes based on task, 2026, https://github.blog/changelog/2026-07-01-copilot-cli-auto-model-selection-routes-based-on-task/; fetched]

**AGAINST**
- The plateau is broken by "larger training datasets, stronger encoders, and end-to-end fine-tuning", meaning the ambiguous middle is not a small residual; it is the set of hard queries all routers fail on, and rules by construction cannot shrink it. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587; fetched]
- Adding execution-grounded performance statistics "yields a 15.3% relative gain, surpassing a heuristic router built on the same dimension-level priors"; rules on the same features lose to a memory of what actually happened, which the register keeps in MEM but RTG-003 does not consume. [source: Agent-as-a-Router, 2026, https://arxiv.org/abs/2606.22902; fetched]
- Silent semantic failure "dominates failure, covering 80% of Llama 4's failing runs and 68% of GPT-5's" and "completion-based and consistency-based monitoring both look healthy exactly when the agent should not be trusted", so rule precision measured on anything short of test-verified outcomes will overstate how clear a band is. [source: Confident and Wrong: Silent Semantic Failures in Coding Agents, 2026, https://arxiv.org/abs/2603.25764; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the decision and add that band precision is computed only on test-verified outcomes and that the rule engine may read MEM's per-slice outcome statistics as a feature (execution-grounded priors), which is the one 2026 result that beats heuristics on the same inputs. State the ambiguous-band ceiling as "the plateau gap", not a minority share.

### ADRL-RTG-004: Local-first only with a bounded, clean cascade

Decision: local-first only when a higher rung is healthy, the post-attempt transcript fits, side effects are recoverable and the attempt is capped; pinned sessions carved out.

**FOR**
- A cheap model's exploratory turns are informative: conditioning the continue-or-escalate decision on them is Bayes-better, so a bounded local attempt is a routing input, not just a gamble. [source: SWE-Router, 2026, https://arxiv.org/abs/2607.00053; fetched]
- Agents show "systemic over-trust in corrupted outputs" and get "trapped in futile trial-and-error loops", and fault tolerance "improves with model scale 3.66x slower than basic task execution", which justifies a hard attempt cap rather than trusting the local model to stop. [source: When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents, 2026, https://arxiv.org/abs/2606.05806; fetched]
- Infinite agentic loops were confirmed in 47 of 6,549 projects, causing "cost exhaustion, model denial of service, context growth, and repeated external side effects"; clause 1(c)'s budget is the recommended bound. [source: When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents, 2026, https://arxiv.org/abs/2607.01641; fetched]

**AGAINST**
- The direction is contradicted for coding agents: "full-trajectory escalation recovers less than half of the LC-to-HC quality gap while incurring a substantial cost premium", whereas downshifting is favourable. Starting low and escalating is the expensive path. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]
- The escalated model does not continue the local attempt, it redoes it: swaps rewrite "61-94% of post-fork actions" and leave "only 3% of replayed states valid", so the transcript the cascade carries is mostly sunk cost. [source: The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World, 2026, https://arxiv.org/abs/2608.08239; fetched]
- Coding-agent workloads are "long contexts with short outputs" with "high but imperfect prefix cache hit rates"; a local attempt that grows the prefix guarantees a cold frontier cache exactly when the transcript is largest. [source: TraceLab: Characterizing Coding Agent Workloads for LLM Serving, 2026, https://arxiv.org/abs/2606.30560; fetched]
- Not Diamond's production router "when context window utilization is low or the cache is cold" prioritises routing economics, i.e. it goes to the right model at the start rather than trying cheap first; local-first at a cold start is the opposite policy. [source: Not Diamond Code, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents; fetched]

**Grounding verdict**: CONTESTED (2026).

**Recommendation**: Reframe local-first as "local exploration with a short, information-gathering budget" whose output feeds the RTG-007 temporal estimand, and require the escalation interface to be trajectory-reducing (CAS-004) because full transfer is the worst case measured. Add a "frontier-first then downshift at a boundary" edge for the Q2 slice and compare both directions in shadow before widening local scope.

### ADRL-RTG-005: Objective: verified quality, retry, latency, session cost

Decision: optimise expected verified quality, retry risk, mode-aware latency and cache-aware session-marginal cost, with versioned weights and unknown terms treated as unknown.

**FOR**
- Not Diamond's router "weighs KV cache state, sub-agent structure, compaction events, and the full session history before recommending a model and a reasoning level", the same session-level objective. [source: Not Diamond Code, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents; fetched]
- Copilot routes "on the first turn, when there is no cache to lose, and after compaction" and reports 72.5% cost savings, confirming cache state belongs inside the objective. [source: Getting more from each token, 2026, https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/; fetched]
- Task-level routing that "updates its policy using the task's terminal reward, jointly accounting for accuracy and latency" beats per-call routing by 7-8 accuracy points, supporting a multi-term, task-terminal objective over per-request difficulty. [source: TRACE-Router: Task-Consistent and Adaptive Online Routing for Agentic AI, 2026, https://arxiv.org/html/2607.22465v2; fetched]

**AGAINST**
- The quality term's fallback (proxy labels) is worse than the ADR assumes: no LLM-judge configuration "exceeds AUROC 0.65 on tau2-bench" and judges "rely on surface completion proxies", so proxy quality should be weighted near zero, not merely reduced. [source: From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents, 2026, https://arxiv.org/abs/2606.09863; fetched]
- Cost constants drift silently: Claude Code's cache TTL "silently regressed from 1 hour to 5 minutes around early March 2026" with 17.1% overpayment measured over 119,866 calls; a versioned price vector that is not observed from usage fields will be wrong without a policy change. [source: Cache TTL silently regressed from 1h to 5m around early March 2026 (anthropics/claude-code issue #46829), 2026, https://github.com/anthropics/claude-code/issues/46829; fetched]
- A switch now has a reasoning cost the objective omits: on the newest models a thinking block "is preserved only while the conversation prefix it was produced from stays unchanged" and switching down "drops it", so the switched-to model "reasons again from the visible messages", billed as output tokens. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- "Recent capability gains have only yielded small improvements in reliability", so retry risk must be measured per served model, not inherited from the rung's capability tier. [source: Towards a Science of AI Agent Reliability, 2026, https://arxiv.org/abs/2602.16666; fetched]

**Grounding verdict**: CURRENT (2026), with DATED constants.

**Recommendation**: Keep the four terms and add a fifth observable, "reasoning re-derivation cost on switch", fed by input_transformations and output-token deltas after a handoff. Require the cost term's constants (TTL, write and read multipliers) to be inferred from provider usage fields per session rather than pinned in config.

### ADRL-RTG-006: Advisory LLM classifier, gated and bounded

Decision: an LLM advisor runs only on the ambiguous band, only at a permitted rung, under a budget, with a conservative fallback and logged provenance.

**FOR**
- Learned routers are in production at scale: OpenAI describes GPT-5 as a system with "a real-time router that quickly decides which to use based on conversation type, complexity, tool needs, and your explicit intent". [source: Introducing GPT-5, 2025, https://openai.com/index/introducing-gpt-5/; search-listed]
- A 1.5B router with policies passed in context can run locally, which satisfies clause 1's "on a privacy-pinned session it runs locally". [source: Arch-Router, 2025, https://arxiv.org/abs/2506.16655; search-listed]
- Routing between reasoning and non-reasoning judges under a fixed budget is a solved formulation ("constrained distributionally robust optimization"), so bounding the advisor's own cost is grounded. [source: Reasoning Is Not Free: Robust Adaptive Cost-Efficient Routing for LLM-as-a-Judge, 2026, https://arxiv.org/abs/2605.10805; search-listed]

**AGAINST**
- A single-shot prompted classifier is the plateau: 21 methods "achieve very similar accuracy" far below oracle, so the advisor adds little on exactly the band it is scoped to. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587; fetched]
- Judges "rely on surface completion proxies" such as "confident closing language" and "coarse action-sequence volume", and lightweight TF-IDF detectors beat them (AUROC 0.83 vs 0.65); the same surface-proxy bias applies to a difficulty classifier reading a prompt. [source: From Confident Closing to Silent Failure, 2026, https://arxiv.org/abs/2606.09863; fetched]
- Training-free draft agreement ("two cheap no-think drafts" and entropy) replaces a classifier for the effort decision with a mechanical signal, at 32-73% token savings; the register should compare the advisor against this cheaper mechanism. [source: DART, 2026, https://arxiv.org/abs/2606.23181; fetched]
- The 2026 step-level routers condition on interaction history with a lightweight trained router, not a prompted LLM; Ares uses "a lightweight router to predict the lowest appropriate reasoning level for each step based on the interaction history". [source: Ares, 2026, https://arxiv.org/abs/2603.07915; fetched]
- Production routers budget the advisor at about "100-150ms per call"; the ADR sets no number, and its budget clause should be anchored to this figure. [source: Not Diamond Code, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents; fetched]

**Grounding verdict**: DATED (2026).

**Recommendation**: Keep the governance (gated, budgeted, provenance-logged) and replace the mechanism target: the advisor should be a small local model or a draft-agreement signal over the partial trajectory, benchmarked in shadow against the rules-only fallback with the plateau gap as the ceiling. Set the latency budget at or below 150 ms per call.

### ADRL-RTG-007: Marginal-utility target, with a build gate

Decision: two estimands (initial placement and a temporal continue-vs-escalate value at boundaries), calibrated with abstention, replay prohibited, built only after a published gate.

**FOR**
- The temporal estimand is now theoretically grounded: conditioning on a partial trajectory "never harms routing and is strictly better whenever exploration is informative". [source: SWE-Router, 2026, https://arxiv.org/abs/2607.00053; fetched]
- Replay prohibition is confirmed: "replay-based benchmarks score the wrong world for agentic routing", with only 3% of replayed states valid. [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239; fetched]
- A dynamic track that "runs routers on the full 500-case SWE-bench Verified suite" and scores "official task resolution and realized API spend" exists, so the branched evaluation the gate requires has a public harness. [source: TwinRouterBench: Fast Static and Live Dynamic Evaluation for Realistic Agentic LLM Routing, 2026, https://arxiv.org/abs/2605.18859; fetched]
- Multi-turn routers that learn from logged trajectories make "fewer model switches" and reduce cost by 43-59% versus a single frontier model, evidence that the estimand can pay for itself. [source: MTRouter: Cost-Aware Multi-Turn LLM Routing with History-Model Joint Embeddings, 2026, https://arxiv.org/html/2604.23530v1; fetched]

**AGAINST**
- Breaking the plateau needs "larger training datasets, stronger encoders, and end-to-end fine-tuning"; the register's 34 of 300 evaluated decisions cannot supply that, so the gate's data threshold should be stated in the thousands. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587; fetched]
- The temporal estimand's action space is wrong: escalation with the full trajectory is the poorly performing action and "reducing LC-model trajectory information improves escalation quality", so the estimand must range over (target deployment, handoff interface), not deployment alone. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]
- Calibration remains hard even with training: budget-aware "interval coverage capping at 47% after SFT+RL", and frontier models are "consistently over-optimistic"; abstention as a prerequisite is right but the calibration bar must be a number. [source: BAGEN: Are LLM Agents Budget-Aware?, 2026, https://arxiv.org/abs/2606.00198; fetched]
- Calibrated cascade routers use token-level margins and isotonic regression, which need logits that cloud APIs do not return, so the estimator must be feasible on observable features only. [source: UCCI, 2026, https://arxiv.org/abs/2605.18796; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Extend the temporal estimand's action set to include the handoff interface (full, compacted, removed) and the direction (escalate or downshift), since these dominate the outcome in the newest evidence. Put a branched-pair count and a calibration coverage target in the pre-build gate, and adopt TwinRouterBench's dynamic track as the external baseline.

### ADRL-RTG-008: Rung vs endpoint, with a leak contract

Decision: rung selection is separate from endpoint selection, with a gateway contract for served identity, within-rung stability and shared rung membership.

**FOR**
- Gateways now pin deployments for reasoning state: after encrypted items "could not be verified" under multi-region load balancing, LiteLLM added "encrypted_content_affinity" that encodes the originating deployment into item ids; the contract ADRL asks for is what gateways already had to build. [source: Incident Report: Encrypted Content Failures in Multi-Region Responses API Load Balancing, 2026, https://docs.litellm.ai/blog/responses-api-encrypted-content-incident; fetched]
- OpenRouter's session id pins "both the resolved model and the provider for the conversation, so follow-up turns keep hitting the same warm cache", a within-rung stability clause in production. [source: OpenRouter Prompt Caching: What Cached Tokens Cost, 2026, https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/; fetched]
- Fallback "endpoints must reside within the approved set for the request's data classification", which is clause 3's shared membership stated as a gateway design rule. [source: LLM fallback routing: the retry chain that survives provider outages without leaking policy, 2026, https://www.deepinspect.ai/blog/llm-fallback-routing; fetched]
- Provider-side model substitution is now reported: with the controls beta a dropped block "is reported in input_transformations as model_binding_mismatch", giving ADRL a provider-native served-identity signal. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]

**AGAINST**
- The contract is missing a security clause: encrypted reasoning could be replayed "across sessions, users, and compatible models within the same provider family" and "every model under the same family used the same encryption key", so a within-rung, within-family swap was an exfiltration path, not only a cache event. [source: Stealing Reasoning Traces from Proprietary LLM APIs (as reported), 2026, https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/; fetched]
- Provider-side prefix binding is now enforced "for new accounts created on or after August 31, 2026", so any gateway that edits history (translation, param dropping) inside a rung turns into a 400 unless drop_block is set; the contract must include "gateway does not modify the prefix". [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- Hedged duplicate requests (fire a second request when the primary exceeds P90, take the fastest) are recommended gateway practice, and hedging across providers violates "endpoint held stable within a turn" by design. [source: The Tail-Tolerant Retry Policy Your LLM Gateway Doesn't Have, 2026, https://tianpan.co/blog/2026-05-02-tail-tolerant-retry-policy-llm-gateway-latency-cliff; fetched]
- OpenAI's cache keys "influence routing; they do not pin requests to a machine or guarantee a cache read hit", so served identity is necessary but not sufficient to know cache state. [source: Prompt caching (OpenAI API docs), 2026, https://developers.openai.com/api/docs/guides/prompt-caching; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Add two contract clauses: the gateway never modifies the message prefix inside a rung (or reports every transformation), and hedging is disabled for requests that may emit tool calls. Treat a within-family downswitch as a security event that requires stripping stronger-model signatures, not only a cost event.

### ADRL-RTG-009: Session-marginal, cache-aware cost accounting

Decision: cost is expected remaining-episode cost given cache state plus rebuild cost on switch plus expected cascade cost; every figure is labelled list price or after cache effects.

**FOR**
- A production router built on this accounting reports 72.5% savings and ties OpenRouter Auto "on resolution rate (70.8%) at 3.3x the savings". [source: Getting more from each token, 2026, https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/; fetched]
- Coding-agent sessions "repeatedly reuse large prefixes and create sustained KVCache pressure", and prefix-aware scheduling improves session completion time up to 3.5x, confirming prefix economics dominate this workload on the serving side too. [source: CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents, 2026, https://arxiv.org/abs/2606.16824; fetched]
- Provider constants now support the model: GPT-5.6+ caches remain "eligible for reuse for 30 minutes after its most recent write or reuse" at 1.25x write and 0.1x read, while Anthropic reads are 0.1x or 0.025x on the newest models. [source: Prompt caching (Claude Platform Docs), 2026, https://platform.claude.com/docs/en/build-with-claude/prompt-caching; fetched]
- Not Diamond's router will "stay on a more expensive model to preserve a warm cache" or "break cache to upgrade", the exact trade this ADR formalises. [source: Not Diamond Code, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents; fetched]

**AGAINST**
- The price vector is not stable: a silent TTL change produced 17.1% overpayment and pushed subscription users into quota limits, so clause 1's "versioned in config" must be replaced by observation from usage fields. [source: anthropics/claude-code issue #46829, 2026, https://github.com/anthropics/claude-code/issues/46829; fetched]
- Cache reads "are not deducted against your rate limit", a throughput value of stickiness the cost model does not carry; rate-limit headroom is often the binding constraint on frontier. [source: Prompt caching (Claude Platform Docs), 2026, https://platform.claude.com/docs/en/build-with-claude/prompt-caching; fetched]
- Switching down loses preserved reasoning and the model "reasons again from the visible conversation", billed as output; the accounting counts input rebuild only. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- Downshifting "offers a favorable cost-quality point"; a cost model that scores every switch as a cache-write penalty will suppress the one switch direction that measurably pays. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Add a rate-limit-headroom credit for cache reads and an output-side re-reasoning charge for downswitches, and derive the price vector per session from cache_read, cache_creation and input_transformations fields rather than config. Score downshift at a boundary as a candidate with its measured quality delta, not as a switch penalty only.

---

# CAS - Execution, Cascade, Recovery

## State of the field, 2026

The 2026 failure literature says the dangerous failures are silent: confident closing language over a failed state (45-76% of failures depending on setting), silent semantic patches that stay consistent across runs, and "fail-plausible" narratives in production runtimes, with LLM judges no better than 0.65 AUROC while cheap text detectors reach 0.83-0.95. Loop failures remain real (68 confirmed infinite-loop defects across 47 projects) and every serious harness now ships fingerprint-based stuck detection. Hand-offs between models are now a measured phenomenon: the Handoff Tax paper shows escalation recovers under half the gap and downshift is favourable, and the Replay Gap shows a swapped model rewrites 61-94% of subsequent actions. Providers hardened reasoning-state semantics in 2026: Anthropic binds thinking signatures to model and prefix (enforced for accounts from 31 August 2026) and reports drops via input_transformations; OpenAI reuses encrypted reasoning only within a family; a same-family key flaw let weaker models decode stronger models' traces until mitigated in August. Gateways adopted deployment affinity, retry budgets and per-tool replay tokens. MCP's current spec says clients MUST treat annotations as untrusted.

### ADRL-CAS-001: Deterministic trip-wires, with measured coverage

Decision: escalation fires on mechanical post-call wires (loops, schema, tool errors, budget exhaustion, verifier failure), never on model self-report, with per-rung thresholds and a published miss rate.

**FOR**
- Mechanical beats judgement: TF-IDF detectors reach "AUROC 0.83 on tau2-bench and 0.95 on AppWorld" while no LLM-judge configuration exceeds 0.65, and the authors advise "lightweight, domain-calibrated detectors as triage signals rather than relying on LLM judges". [source: From Confident Closing to Silent Failure, 2026, https://arxiv.org/abs/2606.09863; fetched]
- Verifier-first is the right first-class wire: the recommendation is to "score agents by test-verified correctness over repeated runs" because completion and consistency signals look healthy when the agent is wrong. [source: Confident and Wrong, 2026, https://arxiv.org/abs/2603.25764; fetched]
- "Search loops" were "the most stable" recurring anti-pattern across a coding-agent corpus, validating the repetition wire as a durable signal. [source: What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents, 2026, https://arxiv.org/pdf/2607.06184; fetched]
- Infinite loops are a confirmed class in the wild (68 across 47 projects), with "repeated external side effects" among the harms; loop wires are load-bearing, not hygiene. [source: When Agents Do Not Stop, 2026, https://arxiv.org/abs/2607.01641; fetched]

**AGAINST**
- The blind spot has grown in the newest measurements: silent semantic failure covers "80% of Llama 4's failing runs and 68% of GPT-5's" and is consistent across runs, so counters, budgets and even repeated-run consistency miss it; only class (e) sees it and class (e) exists for one task. [source: Confident and Wrong, 2026, https://arxiv.org/abs/2603.25764; fetched]
- Implicit tool failures (corrupted but well-formed outputs) cause the "most severe performance degradation" and agents "over-trust" them, so the tool-error wire, which keys on explicit errors, misses the worst class. [source: When Tools Fail, 2026, https://arxiv.org/abs/2606.05806; fetched]
- Clause 4's "model-authored text is never a wire" excludes a proven cheap detector: text features of "confident closing language" are what the 0.83-AUROC detector reads; a calibrated text trigger is mechanical in the sense that matters (no model in the loop). [source: From Confident Closing to Silent Failure, 2026, https://arxiv.org/abs/2606.09863; fetched]
- In a production runtime "approximately 70% of silent failures were detected through human observation" and audits had "zero ex-ante prevention capability", which puts an upper bound on what any post-call wire set will catch and argues for a human-visible miss-rate budget. [source: When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime, 2026, https://arxiv.org/abs/2606.14589; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the set and narrow clause 4: model self-assessment is never a wire, but a versioned, calibrated text detector over the model's closing message (no LLM call) is admissible as a low-weight wire with its own precision report. Add an implicit-tool-failure wire based on result-shape anomalies where the harness can supply them.

### ADRL-CAS-002: Typed failures, versioned enum, measured attribution

Decision: seven typed failure causes with a precedence rule, an unverifiable default, and measured attribution precision before use as training signal.

**FOR**
- Independent taxonomies separate system execution from reasoning and planning errors; TRAIL's taxonomy spans "reasoning errors (like hallucinations), system execution errors (like API issues), and planning/coordination errors", the same partition as infrastructure versus capability. [source: TRAIL: Trace Reasoning and Agentic Issue Localization, 2025, https://arxiv.org/abs/2505.08638; search-listed]
- The explicit/implicit by transient/permanent 2x2 for tool failures maps directly onto infrastructure (transient) versus capability (permanent, implicit), supporting typed handling. [source: When Tools Fail, 2026, https://arxiv.org/abs/2606.05806; fetched]
- "Error swallowing and dilution" is a named production failure class, which is the case for an explicit unverifiable type rather than a guessed cause. [source: When Errors Become Narratives, 2026, https://arxiv.org/abs/2606.14589; fetched]

**AGAINST**
- Automated attribution is weak: the best long-context model "scor[es] a mere 11% on TRAIL", so clause 4's precision gate will likely exclude most types from LRN for a long time; the ADR should say what LRN trains on meanwhile. [source: TRAIL, 2025, https://arxiv.org/abs/2505.08638; search-listed]
- A single type per outcome loses the causal chain: "a single root-cause error propagates through subsequent decisions, leading to task failure", and the taxonomy that fixed it distinguishes memory, reflection, planning, action and system levels. [source: Where LLM Agents Fail and How They can Learn From Failures, 2025, https://arxiv.org/abs/2509.25370; fetched]
- Two 2026 causes have no type: a failure caused by the handoff itself (the handoff tax) and a failure caused by a corrupted-but-valid tool result; both would be typed task_capability today, which is the poisoning direction the ADR guards against. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Add handoff_induced and tool_output_corrupt to failure-types-v3, placed above task_capability in precedence, and record a root-cause step index alongside the type so chains are recoverable. State the interim LRN data source while attribution precision is below gate.

### ADRL-CAS-003: Action boundary defined; no re-issue after side effects

Decision: escalate only when every tool_use has a tool_result; never re-issue a request once tool-use content has streamed; side effects are inherited, enumerated and classified by the CAS-009 provenance rule.

**FOR**
- Gateway practice now attaches "a replay token derived from the request ID plus a per-tool nonce" to every tool call so "the tool server rejects a duplicate token"; the duplicate-side-effect hazard the ADR closes by policy is recognised and closed by mechanism elsewhere. [source: LLM fallback routing, 2026, https://www.deepinspect.ai/blog/llm-fallback-routing; fetched]
- Streaming makes "first body byte, not first header byte" the correct point for retry and hedge decisions, which matches clause 2's "before any content is streamed". [source: The Tail-Tolerant Retry Policy Your LLM Gateway Doesn't Have, 2026, https://tianpan.co/blog/2026-05-02-tail-tolerant-retry-policy-llm-gateway-latency-cliff; fetched]
- The current MCP specification states clients "MUST consider tool annotations to be untrusted unless they come from trusted servers", grounding clause 5's provenance rule. [source: Tools (Model Context Protocol specification 2025-11-25), 2025, https://modelcontextprotocol.io/specification/2025-11-25/server/tools; fetched]

**AGAINST**
- Inheritance is the wrong interface: "reducing LC-model trajectory information improves escalation quality", so clause 3's full inheritance plus enumeration is the interface the evidence rates worst for escalation. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]
- Post-boundary continuations diverge anyway: "74-77% of early swaps diverge at the first post-fork action", so the boundary protects against replay but the new model will largely redo the work; the ADR should not describe the boundary as preserving progress. [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239; fetched]
- Hedged duplicates are a new replay vector: gateways are advised to fire a duplicate request when the primary is slow and to use "idempotency keys on agent workflows where model calls trigger state mutations"; clause 2 forbids ADRL re-issue but is silent on gateway hedging, which produces two tool_use blocks for one intent. [source: The Tail-Tolerant Retry Policy, 2026, https://tianpan.co/blog/2026-05-02-tail-tolerant-retry-policy-llm-gateway-latency-cliff; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the boundary and no-re-issue rule, and add that gateway hedging is prohibited for any request whose tool schema includes side-effecting tools. Move the inherited-transcript question to CAS-004 and let the handoff interface reduce the prior trajectory while the side-effect record stays complete.

### ADRL-CAS-004: Cross-model handoff: provider-pair rules, not one stripping rule

Decision: preserve tool ids and results, transform reasoning per versioned provider-pair rule, append a mechanical delimited handoff note at the end of the last user message.

**FOR**
- Anthropic now documents the pair rule directly: "Keep passing thinking blocks back unchanged when you switch models", blocks are "readable only by the model that produced it or a newer one", and the API "ignores or drops the blocks the target model can't read"; a per-direction table is the correct shape. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- OpenAI: "Persisted reasoning can be reused only within the same model family", and "you should pass back all reasoning items, function call items, and function call output items, since the last user message", matching clause 1's strip-across-family rule. [source: Reasoning models (OpenAI API docs), 2026, https://developers.openai.com/api/docs/guides/reasoning; fetched]
- Translation layers still break on this: a gateway's streaming path dropped redacted_thinking blocks and hit "thinking or redacted_thinking blocks in the latest assistant message cannot be modified" (July 2026), so a tested pair table with redacted_thinking fixtures remains necessary. [source: Streaming /v1/responses drops Anthropic redacted_thinking blocks (maximhq/bifrost issue #5093), 2026, https://github.com/maximhq/bifrost/issues/5093; fetched]

**AGAINST**
- The ADR's only interface (full transcript plus note) is the measured worst for escalation: "reducing LC-model trajectory information improves escalation quality, whereas removing the HC-model trajectory reduces downshift quality". The pair table needs an interface column (full, compacted, removed) keyed by direction. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]
- Prefix binding conflicts with any compaction: a Fable 5.1 block is preserved only while "the conversation prefix it was produced from stays unchanged", and for keep-tail compaction the docs say to "strip thinking and redacted_thinking from every turn you carry across" or set prefix_mismatch_behavior to drop_block; the pair table has no compaction row. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- Downshift is a security boundary, not only a protocol one: replaying a stronger model's encrypted reasoning into "a weaker compatible model" decoded it, with 315,320 thinking blocks and 62 API keys recovered from public logs before mitigation; strip-on-downshift should be mandatory regardless of what the API would drop. [source: OpenAI, Anthropic, Google API Flaw Let Weaker AI Models Decode Stronger Models' Reasoning, 2026, https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html; fetched]
- Gateways must pin the originating deployment for reasoning items ("encrypted_content_affinity"), so the pair rule must be keyed by served deployment (CAS-006), not by model family alone. [source: LiteLLM incident report, 2026, https://docs.litellm.ai/blog/responses-api-encrypted-content-incident; fetched]

**Grounding verdict**: CONTESTED (2026).

**Recommendation**: Extend the pair table with direction and interface columns (escalate: compact or remove LC trajectory; downshift: keep HC trajectory, strip HC signatures) and a compaction row that sets drop_block or strips blocks. Key the table by served deployment and record input_transformations on the outcome row as the provider's own account of what was dropped.

### ADRL-CAS-005: Sticky escalation within an episode

Decision: escalation is sticky within an episode; only a conservative episode boundary may lower the rung.

**FOR**
- Multi-turn routers trained on trajectories make "fewer model switches" and gain "tolerance to transient errors", an independent finding that switching is costly. [source: MTRouter, 2026, https://arxiv.org/html/2604.23530v1; fetched]
- Task-consistent routing "pins all subsequent LLM calls to the selected backend" and beats per-call routing, supporting stickiness as a quality property, not only a cache property. [source: TRACE-Router, 2026, https://arxiv.org/html/2607.22465v2; fetched]
- OpenRouter's session id pins model and provider "so follow-up turns keep hitting the same warm cache"; stickiness is now a first-class gateway feature. [source: OpenRouter Prompt Caching, 2026, https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/; fetched]
- Switching up to the newest Anthropic models "keeps the conversation's reasoning and switching down drops it", so sticky-up is aligned with signature semantics. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]

**AGAINST**
- The evidence says the one handoff that works is the one stickiness forbids: downshifting "offers a favorable cost-quality point" while escalation recovers under half the gap; sticky-up plus a conservative lowering boundary locks in the expensive rung after the hard reasoning is done. [source: The Handoff Tax, 2026, https://arxiv.org/abs/2608.24358; fetched]
- A concrete, production-proven lowering boundary exists: Copilot switches "after compaction, when Copilot summarizes older turns and the prompt prefix resets"; ADRL's SEM-005 boundary is undefined in practice and this ADR gives it no floor. [source: Getting more from each token, 2026, https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/; fetched]
- Within-model effort lowering per step saves "up to 35% tokens" without any rung change, so a cheaper release valve than lowering the rung exists and the ADR does not mention it. [source: Not All Turns Are Equally Hard: Adaptive Thinking Budgets For Efficient Multi-Turn Reasoning, 2026, https://arxiv.org/abs/2604.05164; fetched]

**Grounding verdict**: CONTESTED (2026).

**Recommendation**: Keep "no oscillation" but replace "only a conservative episode boundary" with a named set of lowering boundaries that includes compaction and a verified-progress boundary (tests pass), and permit effort reduction within the rung between boundaries. Measure the ratchet cost against the downshift gain from Handoff Tax before SEM-005 is tuned.

### ADRL-CAS-006: Record the served model, not only the served rung

Decision: sticky state and outcome rows carry served rung, model, provider and the provenance of that record; within-rung model change is an infrastructure event; state loss is explicit.

**FOR**
- A gateway that "had no mechanism to track which deployment created specific encrypted content items" broke follow-up requests and had to add deployment affinity, which is exactly the served-identity record this ADR mandates. [source: LiteLLM incident report, 2026, https://docs.litellm.ai/blog/responses-api-encrypted-content-incident; fetched]
- Provider-side substitution is now self-reported: "A server-side fallback drops unreadable blocks the same way" and, with the controls beta, the drop is listed in input_transformations; ADRL can ingest a provider-native served-identity signal. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- Router models on OpenRouter pin "both the resolved model and the provider", so served identity is available from at least one gateway by contract. [source: OpenRouter Prompt Caching, 2026, https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/; fetched]

**AGAINST**
- The served record is also a security record: because reasoning could be replayed into "a weaker compatible model" of the same family, a substitution to a weaker sibling while signatures are present is a leak path that CAS-006's infrastructure typing does not flag. [source: The Hacker News report on Stealing Reasoning Traces, 2026, https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html; fetched]
- served_source has no value for provider-side fallback (Anthropic's classifier refusal fallback and server-side fallback substitute a model inside the provider), which is neither gateway_reported nor proxy_observed. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- Served model does not determine cache state: OpenAI cache keys "influence routing; they do not pin requests to a machine or guarantee a cache read hit", so RTG-009's warm-cache assumption cannot be derived from CAS-006's record alone. [source: Prompt caching (OpenAI API docs), 2026, https://developers.openai.com/api/docs/guides/prompt-caching; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Add provider_fallback to served_source and record input_transformations verbatim on the outcome row. Flag a within-family downgrade with signatures present as a security event that forces CAS-004's strip path on the next continuation.

### ADRL-CAS-007: Terminal failure surfaced; ADRL owns zero retries

Decision: top-rung or pinned failures surface as protocol-conformant typed errors; ADRL never retries; gateway retries are budgeted and never cross rung, pin or a streamed boundary.

**FOR**
- Retry practice for LLM traffic now includes explicit budgets ("limit retry tokens to 5-15% of base traffic") and recognises that "timeout is the modal failure", supporting a per-turn budget owned by one layer. [source: The Tail-Tolerant Retry Policy, 2026, https://tianpan.co/blog/2026-05-02-tail-tolerant-retry-policy-llm-gateway-latency-cliff; fetched]
- "Two or three total attempts (primary plus one or two fallbacks)" is the recommended chain, and fallbacks must stay inside the approved set for the data classification, matching clause 2's rung and pin constraints. [source: LLM fallback routing, 2026, https://www.deepinspect.ai/blog/llm-fallback-routing; fetched]
- Production evidence favours loud failure: the recommendation is agent systems "whose failures are loud, attributable, and boring", against "fail-plausible" narratives; clause 1's ban on synthetic assistant messages is that principle. [source: When Errors Become Narratives, 2026, https://arxiv.org/abs/2606.14589; fetched]
- Anthropic's fallback credit "requires the body unchanged", so any ADRL-side rewrite before a retry would also forfeit a provider credit. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]

**AGAINST**
- Hedging is neither a retry nor a fallback: firing a duplicate when the primary exceeds P90 and taking the fastest is recommended practice, and the ADR's contract does not name it, so a gateway could hedge within budget and still duplicate a tool call. [source: The Tail-Tolerant Retry Policy, 2026, https://tianpan.co/blog/2026-05-02-tail-tolerant-retry-policy-llm-gateway-latency-cliff; fetched]
- Providers now perform their own fallback (classifier refusal fallback, server-side fallback) that no gateway budget bounds; "a retry never crosses a rung" cannot be guaranteed for provider-internal substitution unless the served model is checked afterwards. [source: Thinking, 2026, https://platform.claude.com/docs/en/build-with-claude/thinking; fetched]
- Surfacing only at the top rung is late: frontier models "continue spending on tasks that are unlikely to succeed, instead of alerting the user early", and early stopping "saves 28-64% tokens on failed trajectories"; the ADR has no early-surface path below the top rung. [source: BAGEN, 2026, https://arxiv.org/abs/2606.00198; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Name hedging explicitly in the retry contract (prohibited when side-effecting tools are in the schema) and add a served-model check after any provider-internal fallback. Add an early-surface path: when the remaining budget estimate says completion is unlikely at the top permitted rung, surface before spending it.

### ADRL-CAS-008: Escalation scope under subagents

Decision: escalation is scoped per routing identity; constraints flow parent to child at spawn; outcomes flow child to parent as typed evidence; children draw from the parent's episode budget.

**FOR**
- Formal contracts with "conservation laws" ensure "delegated budgets respect parent constraints", and experiments report "zero conservation violations in multi-agent delegation"; clause 4 is the informal version of this. [source: Agent Contracts: A Formal Framework for Resource-Bounded Autonomous AI Systems, 2026, https://arxiv.org/html/2601.08815v3; fetched]
- Complexity-aware budgeting that "strictly regulate[s] electron instantiation" improves token efficiency by up to 30% in hierarchical multi-agent systems, supporting budget as a spawn-time constraint. [source: ATOM: Instantiating Budget-Controllable Multi-Agent Collaboration via Nucleus-Electron Hierarchy, 2026, https://arxiv.org/abs/2605.26178; fetched]
- Closed-loop allocation of models across subtasks under budget and deadline ("replans after observed outcomes") is the published shape for the OPS follow-up on allocation policy. [source: On Time, Within Budget: Constraint-Driven Online Resource Allocation for Agentic Workflows, 2026, https://arxiv.org/abs/2605.06110; fetched]

**AGAINST**
- Budget ceilings will not be honoured by model behaviour: "strong agents do not necessarily have strong budget-awareness, with correlation r=0.35" and interval coverage caps at 47% even after training, so the proxy must enforce child budgets mechanically and the ADR should say the child model is never told to self-limit. [source: BAGEN, 2026, https://arxiv.org/abs/2606.00198; fetched]
- Agents fail both by "stopping before warranted escalation" and by "overspending on cheap tasks", so a child that hits its allocation is as likely under-funded as wasteful; typing exhaustion as policy_constraint hides which. [source: EcoAgent-Bench, 2026, https://arxiv.org/html/2608.05519; fetched]
- Sub-agent structure is a routing input in production ("the router weighs KV cache state, sub-agent structure, compaction events"), so strict per-identity isolation forfeits information that a shipping router uses. [source: Not Diamond Code, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents; fetched]
- Agent Contracts bound "temporal boundaries and success criteria" as well as resources; CAS-008's budget is tokens and cost only, with no deadline term for interactive parents. [source: Agent Contracts, 2026, https://arxiv.org/html/2601.08815v3; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep per-identity escalation but let the parent's RTG-005 objective read child outcomes as features (structure, not control), and add a wall-clock term to the child budget for interactive parents. Record on exhaustion whether the child was still making verified progress, so under-funding and waste are distinguishable.

### ADRL-CAS-009: Action-effect provenance and authorization boundary

Decision: side-effect class comes from a built-in table, attested annotations from allow-listed MCP servers, or a parsed command; unknown is destructive; every call is enumerated; the handoff note carries no authority.

**FOR**
- The current specification is normative: clients "MUST consider tool annotations to be untrusted unless they come from trusted servers", and clients SHOULD "prompt for user confirmation on sensitive operations". [source: Tools (MCP specification 2025-11-25), 2025, https://modelcontextprotocol.io/specification/2025-11-25/server/tools; fetched]
- The protocol maintainers say annotations "aren't enforcement", "an untrusted server can lie", and a tool's risk "cannot be made in isolation from other session tools", which is the case for parsing compound commands and closing the world. [source: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do, 2026, https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/; fetched]
- "Repeated external side effects" are a documented harm of agent loops, so a complete side-effect record is needed for both handoff and post-mortem. [source: When Agents Do Not Stop, 2026, https://arxiv.org/abs/2607.01641; fetched]

**AGAINST**
- The same guidance says to keep "actual safety guarantees in deterministic controls" such as sandboxing and network controls; a classification record inside a routing proxy is neither, and the ADR should not be read as an authorization boundary when the harness permission system and sandbox are the real ones. [source: Tool Annotations as Risk Vocabulary, 2026, https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/; fetched]
- Shipping coding routers do not classify side effects at all and still route per step with reported savings, which suggests side-effect class matters for handoff correctness (CAS-003) but is not a routing precondition of the weight RTG-004 gives it. [source: Not Diamond Code, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents; fetched]
- Per-tool replay tokens make duplicate execution impossible at the tool server; where a harness supports them, they are a stronger control than classification and the ADR does not mention them. [source: LLM fallback routing, 2026, https://www.deepinspect.ai/blog/llm-fallback-routing; fetched]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Retitle the decision to "provenance record", drop "authorization boundary", and state that enforcement lives in the harness permission system and sandbox. Add an optional replay-token field per executed call for harnesses that support it, and publish the false-destructive rate so RTG-004's local-first eligibility can be tuned against it.

---

## Verdict tally

| Verdict | Decisions |
|---|---|
| CURRENT | RTG-003, RTG-005, RTG-007, RTG-008, RTG-009, CAS-001, CAS-002, CAS-003, CAS-006, CAS-007, CAS-008, CAS-009 (12) |
| DATED | RTG-006 (1) |
| CONTESTED | RTG-001, RTG-002, RTG-004, CAS-004, CAS-005 (5) |
| UNGROUNDED | none (0) |

## Sources

Fetched in full (F) or search-listed with matching title (S).

- (F) The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers, 2026, https://arxiv.org/abs/2606.07587
- (F) SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks, 2026, https://arxiv.org/abs/2607.00053
- (F) Agent-as-a-Router: Agentic Model Routing for Coding Tasks, 2026, https://arxiv.org/abs/2606.22902
- (F) MTRouter: Cost-Aware Multi-Turn LLM Routing with History-Model Joint Embeddings, 2026, https://arxiv.org/html/2604.23530v1
- (F) The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents, 2026, https://arxiv.org/abs/2608.24358
- (F) The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World, 2026, https://arxiv.org/abs/2608.08239
- (F) TwinRouterBench: Fast Static and Live Dynamic Evaluation for Realistic Agentic LLM Routing, 2026, https://arxiv.org/abs/2605.18859
- (F) TRACE-Router: Task-Consistent and Adaptive Online Routing for Agentic AI, 2026, https://arxiv.org/html/2607.22465v2
- (F) LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing, 2026, https://arxiv.org/abs/2601.07206
- (S) Arch-Router: Aligning LLM Routing with Human Preferences, 2025, https://arxiv.org/abs/2506.16655
- (F) Universal Model Routing for Efficient LLM Inference (UniRoute), 2025, https://arxiv.org/abs/2502.08773
- (F) Adaptive LLM Routing under Budget Constraints (PILOT), 2025, https://arxiv.org/html/2508.21141v1
- (S) Introducing GPT-5, 2025, https://openai.com/index/introducing-gpt-5/
- (F) GPT-5's Router: how it works and why Frontier Labs are now targeting the Pareto Frontier, 2025, https://www.latent.space/p/gpt5-router
- (F) Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents, 2026, https://arxiv.org/abs/2603.07915
- (F) Not All Turns Are Equally Hard: Adaptive Thinking Budgets For Efficient Multi-Turn Reasoning, 2026, https://arxiv.org/abs/2604.05164
- (F) DART: Draft-Agreement Routing for Training-Free Adaptive Thinking Budgets in Hybrid Reasoning Models, 2026, https://arxiv.org/abs/2606.23181
- (S) Reasoning Is Not Free: Robust Adaptive Cost-Efficient Routing for LLM-as-a-Judge, 2026, https://arxiv.org/abs/2605.10805
- (F) UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing, 2026, https://arxiv.org/abs/2605.18796
- (F) C3PO: Optimized Large Language Model Cascades with Probabilistic Cost Constraints for Reasoning, 2025, https://arxiv.org/abs/2511.07396
- (F) The Diminishing Returns of Early-Exit Decoding in Modern LLMs, 2026, https://arxiv.org/abs/2603.23701
- (F) Getting more from each token: How Copilot improves context handling and model routing, 2026, https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/
- (F) About Copilot auto model selection (GitHub Docs), 2026, https://docs.github.com/en/copilot/concepts/models/auto-model-selection
- (F) Copilot CLI auto model selection routes based on task (GitHub Changelog), 2026, https://github.blog/changelog/2026-07-01-copilot-cli-auto-model-selection-routes-based-on-task/
- (F) Not Diamond Code: intelligent model routing for coding agents, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents
- (F) OpenRouter Prompt Caching: What Cached Tokens Cost (sticky routing), 2026, https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/
- (F) Prompt caching (Claude Platform Docs), 2026, https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- (F) Prompt caching (OpenAI API docs), 2026, https://developers.openai.com/api/docs/guides/prompt-caching
- (F) Cache TTL silently regressed from 1h to 5m around early March 2026 (anthropics/claude-code issue #46829), 2026, https://github.com/anthropics/claude-code/issues/46829
- (F) TraceLab: Characterizing Coding Agent Workloads for LLM Serving, 2026, https://arxiv.org/abs/2606.30560
- (F) CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents, 2026, https://arxiv.org/abs/2606.16824
- (F) LLM Query Scheduling with Prefix Reuse and Latency Constraints (k-LPM), 2025, https://arxiv.org/abs/2502.04677
- (F) Thinking (Claude Platform Docs), 2026, https://platform.claude.com/docs/en/build-with-claude/thinking
- (F) Reasoning models (OpenAI API docs), 2026, https://developers.openai.com/api/docs/guides/reasoning
- (F) Incident Report: Encrypted Content Failures in Multi-Region Responses API Load Balancing (LiteLLM), 2026, https://docs.litellm.ai/blog/responses-api-encrypted-content-incident
- (F) OpenAI, Anthropic, Google API Flaw Let Weaker AI Models Decode Stronger Models' Reasoning (The Hacker News), 2026, https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html
- (F) Stealing Reasoning Traces from Proprietary LLM APIs (as reported by Simon Willison; arXiv 2608.09867 per that report), 2026, https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/
- (F) Streaming /v1/responses drops Anthropic redacted_thinking blocks (maximhq/bifrost issue #5093), 2026, https://github.com/maximhq/bifrost/issues/5093
- (F) The Tail-Tolerant Retry Policy Your LLM Gateway Doesn't Have, 2026, https://tianpan.co/blog/2026-05-02-tail-tolerant-retry-policy-llm-gateway-latency-cliff
- (F) LLM fallback routing: the retry chain that survives provider outages without leaking policy (DeepInspect), 2026, https://www.deepinspect.ai/blog/llm-fallback-routing
- (F) Tools (Model Context Protocol specification 2025-11-25), 2025, https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- (F) Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog), 2026, https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- (F) From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents, 2026, https://arxiv.org/abs/2606.09863
- (F) Confident and Wrong: Silent Semantic Failures in Coding Agents, 2026, https://arxiv.org/abs/2603.25764
- (F) When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents, 2026, https://arxiv.org/abs/2607.01641
- (F) When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents (ToolMaze), 2026, https://arxiv.org/abs/2606.05806
- (F) What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents (TraceProbe), 2026, https://arxiv.org/pdf/2607.06184
- (F) When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime, 2026, https://arxiv.org/abs/2606.14589
- (F) Where LLM Agents Fail and How They can Learn From Failures (AgentErrorTaxonomy), 2025, https://arxiv.org/abs/2509.25370
- (S) TRAIL: Trace Reasoning and Agentic Issue Localization, 2025, https://arxiv.org/abs/2505.08638
- (F) Towards a Science of AI Agent Reliability, 2026, https://arxiv.org/abs/2602.16666
- (S) StuckLoopDetection: How We Stopped an Agent Burning $12 on 47 Identical Calls (pydantic-deep), 2026, https://medium.com/@kacperwlodarczyk/stuckloopdetection-how-we-stopped-an-agent-burning-12-on-47-identical-calls-a12b5ea1f193
- (S) Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned, 2026, https://arxiv.org/html/2603.05344v1 (fetched, but the loop-detection section was truncated in the fetch; the fingerprint details in the search snippet are not relied on)
- (F) Agent Contracts: A Formal Framework for Resource-Bounded Autonomous AI Systems, 2026, https://arxiv.org/html/2601.08815v3
- (F) BAGEN: Are LLM Agents Budget-Aware?, 2026, https://arxiv.org/abs/2606.00198
- (F) EcoAgent-Bench: Evaluating Economic Decision-Making in Budget-Constrained LLM Agents, 2026, https://arxiv.org/html/2608.05519
- (F) ATOM: Instantiating Budget-Controllable Multi-Agent Collaboration via Nucleus-Electron Hierarchy, 2026, https://arxiv.org/abs/2605.26178
- (F) On Time, Within Budget: Constraint-Driven Online Resource Allocation for Agentic Workflows, 2026, https://arxiv.org/abs/2605.06110
- (F) Budgeted Act-or-Defer Multi-Agent LLM Deliberation with Local Reliability Bounds, 2026, https://arxiv.org/abs/2606.29654
- (S) tau2-bench (sierra-research), 2025, https://github.com/sierra-research/tau2-bench
- (S) Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey, 2026, https://arxiv.org/html/2603.04445v2

Searched but not used for claims: tau-bench 2 failure analyses beyond the False Success paper; SGLang and vLLM prefix-caching product pages (search-listed only; CacheWise, TraceLab and k-LPM carry the prefix-caching evidence instead); RouteJudge (2606.18774, search-listed); TCAndon-Router (fetched, not relevant to escalation).
