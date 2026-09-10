# Research-grounded critique of ADRL MEM and LRN decisions

Date: 2026-09-03. Scope: adr/MEM/001-010 and adr/LRN/001-008 in /Users/arunmenon/projects/adrl-world-class. Every citation below is a URL that was either fetched (marked F) or appeared in a WebSearch result with a matching title (marked S). Nothing is cited from memory. The 2026-09-02 adversarial reviews already in the ADRs are not repeated; where a 2026 source confirms or overturns a claim those reviews made, that is said explicitly.

Verdict legend: CURRENT (decision matches 2025-2026 research and practice), DATED (decision is right in spirit but its mechanism or evidence base has been superseded), CONTESTED (2025-2026 sources pull in both directions), UNGROUNDED (no research basis found either way).

---

## MEM: Memory, Evidence, Label Integrity

### State of the field 2026

Three things changed in the last eighteen months. First, the "verified" in verified coding labels collapsed as a trust anchor: OpenAI stopped reporting SWE-bench Verified in 2026 after an audit found 59.4% of a hard subset had test flaws that reject correct patches, and 2026 mining studies show agent-written tests are flakier and more heavily mocked than human ones. Second, embeddings are now formally treated as prompt-class data: Zero2Text (Feb 2026) inverts black-box embeddings with no training pairs and defeats differential-privacy noise, and Ghost Vectors (Jun 2026) shows soft-deleted vectors remain recoverable from HNSW index files; the only defence that survives both is per-key encryption with key destruction, which the EDPB's final blockchain guidelines (v2, July 2026) endorse as erasure. Third, failure attribution moved from enum typing to counterfactual re-execution: LLM judges attribute failing steps at roughly 14% accuracy, and 2026 taxonomies (41 modes on component edges, kappa 0.76) place harness, grader and environment faults alongside model faults. Append-only, hash-chained agent ledgers are now routine.

---

### ADRL-MEM-001: Append-only ledger keyed by route_id

**Decision.** Transaction memory is an append-only decision/outcome/event ledger keyed by an immutable route_id; every event carries a sequence number, idempotency key and schema version; erasure is the one logged mutation.

**FOR**
- Append-only, replayable action ledgers are the 2026 baseline for agent accountability; a 2026 survey of persistent agent systems names "provenance and audit records" as core state and observes the field under-invests in governing and relinquishing state, which is exactly what clauses 2 and 3 add. [source: Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents, 2026, https://arxiv.org/abs/2606.30306 · F]
- Sample-level, tamper-evident provenance is now argued as necessary for auditable ML pipelines: FG-Trac tracks whether a specific sample was used, when, and whether its records remain intact, using cryptographic commitments, which is the route_id-per-event discipline at finer grain. [source: Fine-Grained Traceability for Transparent ML Pipelines, 2026, https://arxiv.org/abs/2601.14971 · F]
- Reproducibility is being framed as a trust primitive for agent tool use, with a verifiable interaction ledger logging capability definitions, execution claims and provenance at under 0.02% overhead; the ledger-first posture of MEM-001 is aligned. [source: Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use, 2026, https://arxiv.org/abs/2603.14332 · F]

**AGAINST**
- The EDPB's final Guidelines 02/2025 (v2.0 adopted 7 July 2026) recommend not registering clear-text, encrypted or hashed personal data on an immutable ledger at all, and treat key destruction as erasure only where off-ledger design was considered up front. MEM-001 keeps ciphertext and keyed hashes in the immutable stream forever; the "skeleton survives" clause is defensible but the guidance says the default should be by-reference storage, not encrypted-in-stream. [source: EDPB Guidelines 02/2025 on processing of personal data through blockchain (v2, July 2026), 2026, https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf · S] and [source: EDPB adopts guidelines on processing personal data through blockchains, 2025, https://www.edpb.europa.eu/news/news/2025/edpb-adopts-guidelines-processing-personal-data-through-blockchains-and-ready_en · F]
- 2026 agent ledgers are hash-chained (SHA-256 or SHA3 per action, Ed25519 signed) so that any in-place edit breaks the chain; MEM-001 relies on a provider port refusing UPDATE, which is a convention, not tamper evidence. A ledger that EVL readiness claims stand on has no integrity proof. [source: Governed Reasoning for Institutional AI, 2026, https://arxiv.org/pdf/2604.10658 · S] and [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 · F]
- Inference nondeterminism is measured at 5.8x variance across nine models and seven providers; an append-only record of "what the router saw and did" cannot claim the served model's output was reproducible from the event, so replay-from-ledger is provenance, not reproduction. The decision text implies more than it can deliver for the model side. [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 · F]

**Grounding verdict.** CURRENT (newest relevant source: 2026).

**Recommendation.** Keep the decision; add a per-route_id hash chain (previous-event hash on every event) so immutability is verifiable rather than declared, and record in the rationale that the ledger proves what was logged, not that model output is reproducible. Reconsider, with MEM-010, whether prompt-class ciphertext should be stored by reference outside the stream as the EDPB now recommends.

---

### ADRL-MEM-002: Three-state outcome lifecycle with defined close

**Decision.** pending, closed_turn, closed_final after a versioned closing window; late evidence is appended and re-derives the label; non-final outcomes are censored.

**FOR**
- The 2026 delayed-feedback literature confirms the posture: WWW 2026 work on net conversion (purchase then refund) shows a two-stage cascaded delay must be modelled as separate stages with stage-wise debiasing, and that delay time itself is a predictive feature. ADRL's "closed_turn success then human revert" is structurally the same cascade. [source: Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction: Benchmark, Insights and Solutions, 2026, https://arxiv.org/abs/2601.19965 · F]
- The largest 2026 study of coding-agent sessions (20,574 sessions, 1,639 repos) finds 91.49% of visible resolutions of agent misalignment required explicit user correction, confirming that the human is the dominant late-evidence source the amended text names. [source: How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions, 2026, https://arxiv.org/abs/2605.29442 · F]
- Code churn (rewritten or deleted within two weeks) roughly doubled from 3.3% pre-AI to 7.1% in 2025 in GitClear's 2026 analysis, so a label frozen at first success systematically over-credits AI-authored edits, which is the bias clause 3's time-to-close measurement is meant to expose. [source: The Maintainability Gap: 2026 AI Code Quality Research, GitClear, 2026, https://www.gitclear.com/the_ai_code_quality_maintainability_gap · S]

**AGAINST**
- The field has moved past "wait then close": TRACE (Apr 2026) uses the evolving post-click trajectory to refine the label posterior before the window closes, with a reliability-gated completer for early samples. MEM-002 has no trajectory signal; it either waits or freezes. For ADRL the analogue is the next-N-turn edit trajectory on the same files, which the follow-up describes but the decision does not require. [source: Follow the TRACE: Exploiting Post-Click Trajectories for Online Delayed Conversion Rate Prediction, 2026, https://arxiv.org/abs/2604.23197 · F]
- Agentic PR data shows a two-regime world: 28.3% of 33,707 agent PRs merge almost immediately while a large share of the rest enter iterative review and are abandoned. A single closing window will be too long for the first regime and too short for the second; the window should be conditioned on the regime, not global. [source: Early-Stage Prediction of Review Effort in AI-Generated Pull Requests (MSR 2026), 2026, https://arxiv.org/html/2601.00753 · S]
- The Microsoft rollout study warns that "a merged PR is not the same as the value it delivers"; closed_final defined by absence of revert still measures survival, not correctness, so the label semantics remain proxy even after the window. [source: Adoption and Impact of Command-Line AI Coding Agents, 2026, https://arxiv.org/abs/2607.01418 · F]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the three states, but make the closing rule regime-aware (instant-merge versus iterative) and add a required same-file edit-trajectory signal that can shorten or extend the window, following TRACE rather than a fixed N turns. State in the rationale that closed_final is a survival label, not a correctness label, unless MEM-003 verification also attaches.

---

### ADRL-MEM-003: Verification enriches, never overwrites

**Decision.** Each verification run is an appended event with verifier version, command, tree identity and pass/fail/indeterminate; drifted-tree runs are excluded from capability labels.

**FOR**
- OpenAI's 2026 audit of SWE-bench Verified found 59.4% of a hard 27.6% subset had test flaws that reject functionally correct submissions (35.5% too narrow, 18.8% too wide), and stopped reporting the benchmark. "The tests" are now officially an unreliable instrument, which vindicates recording verifier provenance and an indeterminate state. [source: Why SWE-bench Verified no longer measures frontier coding capabilities, OpenAI, 2026, https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ · S; page returned 403, numbers taken from OpenAI Abandons SWE-Bench Verified, SiliconReport, 2026, https://www.siliconreport.com/openai-abandons-swe-bench-verified-citing-widespread-data-contamination-and-flawed-tests-6ebd9b34 · F; note the announcement date is reported as February 2026 by CodeSOTA and July 2026 by SiliconReport]
- LLM-generated tests are measurably flakier than existing tests across SAP HANA, DuckDB, MySQL and SQLite, with unordered-collection dependence in 63% of flaky cases, and flakiness transfers from existing tests through prompt context. A verifier that runs agent-authored tests needs the repeat-run flake measurement clause 2 implies. [source: On the Flakiness of LLM-Generated Tests for Industrial and Open-Source Database Management Systems, 2026, https://arxiv.org/abs/2601.08998 · F]
- Production-derived benchmark curation now uses multi-run stability checks and agentic test-relevance validation as standard layers, which is the provenance-plus-repeat pattern MEM-003 adopts. [source: REAP: Automatic Curation of Coding Agent Benchmarks from Interactive Production Usage, 2026, https://arxiv.org/abs/2604.01527 · F]

**AGAINST**
- Coding agents add mocks in 36% of test commits versus 26% for humans across 1.2M commits; over-mocked tests "may be less effective at validating real interactions". A verifier that runs the repository's own tests, increasingly agent-authored, is partly verifying the agent against itself. MEM-003 records which tests ran but has no notion of test adequacy or mock density, so a "verified pass" can be a pass against a mock. [source: Are Coding Agents Generating Over-Mocked Tests? An Empirical Study, 2026, https://arxiv.org/abs/2602.00409 · F]
- Formal verification of agent workflows (Lean4Agent) separates verification-passing from failing trajectories by 11.94% on SWE-bench Verified, showing that trajectory-level verification carries signal that test pass/fail alone does not; MEM-003's verification is outcome-only. [source: Lean4Agent: Formal Modeling and Verification for Agent Workflow and Trajectory, 2026, https://arxiv.org/abs/2606.06523 · F]
- REAP and SWE-rebench both use LLM-based task classification and automated validity checks at scale; MEM-003 forbids nothing here but the register's "deterministic verification only" framing leaves no tier for an LLM-judged adequacy check, which the field uses as a filter (not a label). [source: SWE-rebench, 2025, https://arxiv.org/abs/2505.20411 · F]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the decision; add a test-adequacy field to the verification event (mock density, assertion count, whether tests were agent-authored in the same session) and treat "passed only agent-authored tests" as a lower verification grade in LRN-001. Require N repeat runs, not two, before a suite's labels are tier-1.

---

### ADRL-MEM-004: Cause-typed labels, seven types not four

**Decision.** task_capability is kept separate from harness_dialect, infrastructure, policy_constraint, context_feasibility, user_abort, unverifiable; labels carry rule version, confidence and source event; first-occurring cause is primary.

**FOR**
- The July 2026 interaction-centric taxonomy assigns 41 failure modes to edges between components and tags each as model-side, harness-side, or environment/grader-side, with a maximum Cohen's kappa of 0.76; the model-versus-harness split is exactly MEM-004's task_capability versus harness_dialect and is now mainstream. [source: Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures, 2026, https://arxiv.org/abs/2607.28802 · F]
- A July 2026 synthesis of 27 taxonomy and audit papers identifies "long-horizon degradation from context accumulation" as its own cluster and finds failures compound nonlinearly with task length, which supports the new context_feasibility type. [source: Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents, 2026, https://arxiv.org/abs/2607.05775 · F]
- Label noise is the most damaging noise type in LLM fine-tuning across three model families, ahead of typographical and grammatical corruption, which justifies spending effort on label cause-cleanliness rather than volume. [source: Analyzing the Effect of Noise in LLM Fine-tuning, 2026, https://arxiv.org/abs/2604.12469 · F]

**AGAINST**
- Attribution by inspection is unreliable: LLM-judge step attribution scores about 14% on Who&When, and the 2026 Causal Agent Replay paper argues the correct method is intervention and re-execution under the same stochastic policy, with a Monte-Carlo Shapley split when steps interact. MEM-004's "first-occurring cause is primary" is a heuristic that the 2026 attribution literature treats as insufficient for interacting causes. [source: Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures, 2026, https://arxiv.org/abs/2606.08275 · F] and [source: Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?, 2026, https://arxiv.org/abs/2607.09996 · F]
- The 2026 taxonomies place "environment or grader failure" as a first-class category; MEM-004's enum has no grader/verifier-fault type. A flaky or over-mocked verifier (MEM-003) currently lands in unverifiable or infrastructure, neither of which is right. [source: Model or Harness?, 2026, https://arxiv.org/abs/2607.28802 · F]
- Seven-category taxonomies for long-horizon agents treat categories as orthogonal dimensions that co-occur (catastrophic forgetting, false assumptions, history error accumulation), not as a primary plus one secondary. [source: The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break, 2026, https://arxiv.org/html/2604.11978v1 · S]

**Grounding verdict.** CONTESTED (2026).

**Recommendation.** Keep the exclusion principle (only task_capability trains the estimator) but add a grader_fault type and allow a multi-label vector with per-type confidence instead of primary plus secondary. Where the counterfactual harness of LRN-002 exists, derive the cause by re-execution (Causal Agent Replay style) rather than by inspection order, and record which method produced the label.

---

### ADRL-MEM-005: Prompt-derived artefacts are prompt-class data

**Decision.** Raw prompts are never stored; embeddings, keyed hashes, paths, argv, verifier output and any locating field are prompt-class under a field-level inventory with a schema test; pin suppression is retroactive.

**FOR**
- Zero2Text (Feb 2026) inverts embeddings from closed-source encoders in a strict black-box setting with no in-domain training pairs and reports that "standard defenses, such as differential privacy, fail to effectively mitigate this adaptive threat". The reclassification of embeddings as prompt-class is not conservative, it is the only reading consistent with 2026 attacks. [source: Zero2Text: Zero-Training Cross-Domain Inversion Attacks on Textual Embeddings, 2026, https://arxiv.org/abs/2602.01757 · F]
- Ghost Vectors (Jun 2026) shows soft-deleted vectors in three HNSW implementations remain physically recoverable from index files and, via Vec2Text, yield 25.5% exact person names and 100% of structured patient demographics; encryption with key discard at deletion reduced PII recovery to 0%. This is the MEM-005/MEM-010 design validated externally. [source: Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases, 2026, https://arxiv.org/abs/2606.18497 · F]
- BeamClean (2025) jointly estimates noise parameters and decodes tokens without knowing the obfuscation mechanism, beating distance-based attacks under Laplacian and Gaussian noise, so noise-only mitigations are not a substitute for access control. [source: BeamClean: Language Aware Embedding Reconstruction, 2025, https://arxiv.org/abs/2505.13758 · S]

**AGAINST**
- The ADR's follow-up to "evaluate quantisation/noise on stored embeddings as defence in depth" is dated by Zero2Text and BeamClean; the 2026 defence literature has moved to concept-aware, dimension-calibrated noise (SPARSE, Mahalanobis mechanism) precisely because uniform noise destroys utility before it stops inversion. If ADRL wants a noise defence it should test SPARSE-style mechanisms, not 8-bit quantisation. [source: Concept-Aware Privacy Mechanisms for Defending Embedding Inversion Attacks, 2026, https://arxiv.org/abs/2602.07090 · F]
- The 2026 sources say erasure must propagate to caches, summaries, search indexes and conversation histories, and that deleting vectors does nothing for an embedding model fine-tuned on the data. MEM-005's inventory covers ledger, projections, WAL and backups but not any future fine-tuning of the local encoder on ADRL's own corpus; a one-line prohibition is missing. [source: Art.17 Right to Erasure: LLM Training Data Removal & RAG Vector Store Deletion 2026, sota.io, 2026, https://sota.io/blog/eu-ai-act-gdpr-art17-right-erasure-training-data-llm-2026 · F]
- Per-session encryption keeps a lossy copy of source code on disk, and the EDPB's final guidance is that encrypted or hashed personal data on an immutable store should be avoided, not merely encrypted; the honest cost is that suppressing embeddings entirely for retrieval, or holding them only in an ephemeral in-memory index, is the compliant default. [source: EDPB Guidelines 02/2025 v2, 2026, https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf · S]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the replacement text; delete the quantisation follow-up and replace it with a SPARSE-style evaluation only if a noise layer is wanted at all. Add a clause forbidding fine-tuning of the local embedding model on ledger content without an unlearning path, and consider making the retrieval index ephemeral (decrypt to memory per process, never persist the NumPy array) so the persisted store is ciphertext only.

---

### ADRL-MEM-006: Memory facade, fail-safe but never silent

**Decision.** Provider port with NullProvider fallback; degraded decisions are counted, surfaced and excluded from evidence; routing state goes through the port or is declared process-local; the port declares concurrency guarantees.

**FOR**
- 2026 production guidance on SQLite still says single writer at a time, use WAL, set busy_timeout, serialise writes through one worker; lock errors are negligible under roughly 20 concurrent writers and p99 degrades beyond that. Declaring these at the port, as clause 4 does, matches practice. [source: SQLite in Production 2026: Real Benchmarks, Limits, and When to Migrate to Postgres, 2026, https://sesamedisk.com/sqlite-in-production-2026-benchmarks-limits/ · S]
- The 2026 persistent-agent survey introduces an evaluation protocol that scores "state mutation and recovery obligations rather than answer quality alone", which is the framing of clause 1: degraded mode is a recovery obligation with a metric. [source: Always-On Agents, 2026, https://arxiv.org/abs/2606.30306 · F]

**AGAINST**
- The OpenTelemetry GenAI conventions now model agent runs as invoke_agent, chat, execute_tool and memory-operation spans, and MCP calls share the vocabulary since v1.42.0 (June 2026); ADRL emits a bespoke memory_degraded event. Degraded memory should be an attribute on the standard span, or EVL-009 blockers will live in a telemetry silo. The conventions are still marked Development, so the risk is churn, not absence. [source: OpenTelemetry's GenAI semantic conventions are NOT stable yet, 2026, https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke · S] and [source: How OpenTelemetry Traces LLM Calls, Agent Reasoning, and MCP Tools, Greptime, 2026, https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions · S]
- Litestream-style replication is "disaster recovery, not high availability" and can lose the last second of writes; if OPS ever replicates router-memory.db this way, a write-behind outcome_events path (the ADR's recommended choice) silently widens the unlogged window without triggering memory_degraded. [source: SQLite Litestream Replication in Production Guide, 2026, https://www.matthewswong.com/en/blog/sqlite-litestream-replication-production/ · S]
- No 2025-2026 research directly evaluates fail-open telemetry stores for ML evidence; the decision is grounded in engineering practice, not in a measured result about how much unlogged traffic biases a routing corpus.

**Grounding verdict.** CURRENT (2026, practice-level rather than research-level).

**Recommendation.** Keep the decision; emit degraded-mode state as attributes on OpenTelemetry GenAI spans rather than a private event so EVL, OPS and any external observability share one vocabulary. Record the write-through/write-behind choice now and make replication lag part of the degraded counter.

---

### ADRL-MEM-007: Projections are rebuildable and versioned

**Decision.** Retrieval indexes are projections stamped with ledger high-water mark, embedding-model version and projection-code version; stale is a labelled state; erasure forces invalidation; change detection via PRAGMA data_version.

**FOR**
- LiveVectorLake (Nov 2025) builds exactly this: content-addressable chunk hashing for deterministic change detection, a hot vector tier separate from a cold versioned tier, and point-in-time retrieval with ACID consistency, re-processing 10-15% of content per update instead of 100%. The stamp-and-rebuild design is current practice. [source: LiveVectorLake: A Real-Time Versioned Knowledge Base Architecture for Streaming Vector Updates and Temporal Retrieval, 2025, https://arxiv.org/abs/2601.05270 · F]
- Feature-store practice treats point-in-time (AS OF) joins as the standard leakage defence: each training row gets the latest feature value at or before its timestamp. MEM-007's as-of projection rebuild is the retrieval-feature equivalent. [source: Point-in-time feature joins, Databricks docs, 2026, https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series · F]

**AGAINST**
- Ghost Vectors shows "rebuilt without the affected vectors" is not enough: the old index file, and any copy of it, still holds the vector. Clause 3 must require the previous NumPy file be overwritten or shredded, and the erasure proof in MEM-010 must enumerate projection files, not just the ledger. [source: Ghost Vectors, 2026, https://arxiv.org/abs/2606.18497 · F]
- Sequential-recommender evaluation shows that "temporal user split" still leaks and only a global temporal split prevents leakage; an as-of projection keyed to one decision's ledger position is a per-row cut, and the same warning applies if neighbours from the same session but later turns are permitted. Clause 2 should exclude same-session later rows explicitly. [source: Time to Split: Exploring Data Splitting Strategies for Offline Evaluation of Sequential Recommenders, 2025, https://arxiv.org/abs/2507.16289 · F]
- The as-of rebuild cost scales with the number of training decisions; LiveVectorLake solves this with a versioned cold tier and sub-2s temporal queries, whereas ADRL's plan is "rebuild the NumPy index as of position N" per evaluation, which will not scale to the multi-worker future without a versioned tier.

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the decision; require physical shredding of superseded projection files and add them to the MEM-010 erasure proof. Exclude same-session later rows from as-of neighbours and plan a versioned cold tier (Delta or Parquet snapshots by ledger position) rather than per-query full rebuilds.

---

### ADRL-MEM-008: Retrieval stays advisory until gated

**Decision.** Retrieval remains advisory/shadow until evaluated-label quantity and quality gates pass.

**FOR**
- A May 2026 study of 21 routing methods on five benchmarks finds diverse routers, kNN included, converge to a "routing plateau" well below optimal because they learn global model-performance trends rather than query-specific signal. Retrieval-by-similarity is the canonical plateau router, so keeping it advisory is warranted. [source: The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers, 2026, https://arxiv.org/abs/2606.07587 · F]
- LLMRouterBench (400K instances, 33 models) finds several recent approaches, including commercial routers, fail to reliably beat a simple baseline, and that backbone embedding models have limited impact, so a thin embedding index is unlikely to be the exception. [source: LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing, 2026, https://arxiv.org/abs/2601.07206 · F]
- RouterArena evaluation finds judge scoring deviates from exact-match by 10-24 points, so any retrieval "agreement" metric computed against LLM-judged outcomes rather than verified ones is not a gate. [source: RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers, ICLR 2026, https://proceedings.iclr.cc/paper_files/paper/2026/file/4987bb24bc53c198785922d1bd9e18cf-Paper-Conference.pdf · S]

**AGAINST**
- The strongest 2026 result for coding-task routing comes from execution-grounded memory: an orchestrator-verifier-memory loop that accumulates task-level performance statistics during deployment gives a 15.3% relative gain over a heuristic router and the lowest cumulative regret on CodeRouterBench, generalising to out-of-distribution agentic tasks. That is retrieval of verified past outcomes, i.e. the MEM-008 mechanism, given authority. A gate that only counts labels may be starving the one signal shown to work. [source: Agent-as-a-Router: Agentic Model Routing for Coding Tasks, 2026, https://arxiv.org/abs/2606.22902 · F]
- Production-derived benchmarks diverge from public ones in language distribution, prompt style and codebase structure; a count gate (300) says nothing about whether the 300 cover the production distribution. The ADR's own follow-up asks for representativeness but the decision text still defers to "quantity and quality". [source: REAP, 2026, https://arxiv.org/abs/2604.01527 · F]
- Contextual-bandit routers now learn from partial feedback with far less exploration data than supervised routers require, so the "advisory until enough labels" posture can be replaced by a bounded-regret online learner that earns authority incrementally rather than by a threshold. [source: WISERouter: LLM Routing with Workload Budget Constraint, 2026, https://arxiv.org/abs/2607.23765 · F]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the decision but change what the gate measures: require a coverage/representativeness condition and a verified-outcome agreement metric, and permit retrieval to advise the LRN-003 estimator (as Agent-as-a-Router's memory does) before it advises routing. The plateau literature says retrieval alone should never be the router; the execution-grounded result says retrieval of verified outcomes is the feature that breaks the plateau.

---

### ADRL-MEM-009: Counterfactuals bind only to explicit route_id

**Decision.** Counterfactual evidence attaches only to an explicit route_id; proximity is never used.

**FOR**
- Causal Agent Replay models an agent run as a structural causal model, applies do() to a named step and re-executes forward; attribution is by explicit intervention identity, never by time. Who&When Pro likewise constructs 12,326 failure trajectories by "injecting a failure only after exactly replaying a successful prefix", which is explicit binding to a prefix. [source: Causal Agent Replay, 2026, https://arxiv.org/abs/2606.08275 · F] and [source: Who&When Pro, 2026, https://arxiv.org/abs/2607.09996 · F]
- The Replay Gap (Aug 2026) shows 74-77% of early model swaps diverge at the first post-fork action and replay predicts patches with 0.00-0.11 similarity to reality; any binding looser than "this decision, this state" scores a different world. [source: The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World, 2026, https://arxiv.org/abs/2608.08239 · F]
- A June 2026 analysis of 33,596 agent PRs shows a naive pooled comparison (53.8% vs 79.8% merge rate) reverses under repository and commit-count controls; inference from co-occurrence is exactly what MEM-009 forbids. [source: Beyond Simpson's Paradox: A Cascade of Confounders in AI Agent Pull-Request Co-Authorship, 2026, https://arxiv.org/abs/2606.22711 · F]

**AGAINST**
- Explicit binding does not fix nondeterminism: measured inference determinism varies 5.8x across providers, so two runs bound to the same route_id can differ for reasons unrelated to the rung. Causal Agent Replay handles this with multiple stochastic re-executions and a point-of-commitment rule; MEM-009 plus LRN-002 currently allow one branch per arm. [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 · F] and [source: Causal Agent Replay, 2026, https://arxiv.org/abs/2606.08275 · F]
- The rule makes subagent counterfactuals impossible (SEM-006 at D0); the 2026 attribution benchmarks are multi-agent by construction, so ADRL's corpus will be blind to the class of failures the literature now studies most.

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the rule unchanged. Add to the rationale that explicit binding is necessary and that LRN-002 must supply repeated stochastic branches per arm so the bound counterfactual is a distribution, not a single sample.

---

### ADRL-MEM-010: Retention and erasure of ledger and derived artefacts

**Decision.** Every inventoried field has a retention period and erasure procedure; prompt-class rows are encrypted per session and crypto-shredded; erasure is an event, invalidates projections, and is proven by a check over every store including WAL and backups.

**FOR**
- The EDPB's final blockchain guidelines (v2.0, 7 July 2026) accept rendering data unidentifiable by destroying encryption keys or erasing off-chain components where technical deletion is infeasible, which is clause 2. [source: EDPB Guidelines 02/2025 v2, 2026, https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf · S] and [source: Blockchain And GDPR: EDPB Guidelines 02/2025 Adopted, Mondaq, 2026, https://www.mondaq.com/fin-tech/1617044/blockchain-and-gdpr-edpb-guidelines-022025-adopted · S]
- Ghost Vectors' Epoch Key Rotation (encrypt vectors, discard keys on deletion, emit cryptographic proof of deletion) reduced PII recovery to 0% and completed deletion of 500 vectors in 2.5 ms; MEM-010 clause 5's erasure_verified event is the same "proof of deletion" idea. [source: Ghost Vectors, 2026, https://arxiv.org/abs/2606.18497 · F]
- A January 2026 crypto-shredding design for GDPR-plus-MiFID II retention uses per-subject AES-256-GCM keys, keeps hash-chain integrity after shredding, mandates backup destruction, and issues erasure certificates; this is MEM-010 with an HSM. [source: Crypto-Shredding: The Technical Foundation for Reconciling GDPR and Financial Record-Keeping Obligations, VeritasChain, 2026, https://veritaschain.org/blog/posts/2026-01-18-crypto-shredding-gdpr-mifid-ii-reconciliation/ · F]

**AGAINST**
- The same EDPB guidance recommends not registering clear-text, encrypted or hashed personal data on the immutable ledger in the first place and considering erasure at design time; MEM-010 chooses encrypt-in-stream over store-by-reference. For a payments company the by-reference design (ciphertext in a deletable side store, only a pointer in the ledger) is the more defensible default. [source: EDPB adopts guidelines on processing personal data through blockchains, 2025, https://www.edpb.europa.eu/news/news/2025/edpb-adopts-guidelines-processing-personal-data-through-blockchains-and-ready_en · F]
- Per-session keys on a developer laptop, rotated never, are far from the HSM-backed, annually rotated key management the 2026 design assumes; losing the keystore is "safe" for privacy but destroys the retrieval corpus, and the ADR defers this to OPS-001 without a date.
- Machine unlearning is now a regulatory expectation: 2026 analyses say deleting vectors does not touch an embedding model fine-tuned on the data, and "unlearning-ready" architectures are forecast to become required. MEM-010 has no clause for the encoder. [source: sota.io Art.17 analysis, 2026, https://sota.io/blog/eu-ai-act-gdpr-art17-right-erasure-training-data-llm-2026 · F] and [source: SoK: Unlearnability and Unlearning for Model Dememorization, 2026, https://arxiv.org/pdf/2605.11592 · S]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Accept at D0 with two changes: store prompt-class ciphertext by reference in a deletable side table (ledger keeps only the pointer and skeleton), and add a clause that no model, including the local embedding model, is ever trained or fine-tuned on ledger content without a declared unlearning procedure. Replace the provisional 90-day figure with the neighbour-age measurement before any pilot.

---

## LRN: Learning and Adaptation

### State of the field 2026

LLM routing research has moved from supervised routers on preference labels to three things ADRL's LRN bucket must reckon with. First, the diagnosis: 2026 benchmarks show most routers, commercial ones included, plateau near a simple baseline because they learn average model quality rather than per-query signal, and larger datasets, stronger encoders and end-to-end fine-tuning are the levers. Second, the data model: routers now learn from partial bandit feedback online (BaRP, OrcaRouter, WISERouter with O(sqrt(T)) regret under budget constraints), and Meta-Router reframes router training as causal inference with preference-label bias as a CATE. Third, the evaluation model: the Replay Gap (Aug 2026) invalidates replay-based evaluation for agentic routing, Causal Agent Replay attributes failures by re-execution, and OPE under deterministic logging is shown to be severely biased (ICLR 2026), with logging-policy design now a research topic. Selective prediction matured into conformal risk control with impossibility bounds, group-conditional guarantees and anytime-valid deployment certificates. Model signing (OpenSSF OMS, sigstore v1.0) is the new artifact baseline.

---

### ADRL-LRN-001: Evidence tiers, not "outrank"

**Decision.** Only T1 (verified, cause-typed, closed_final, organic) enters the objective and holdout; T2-T5 are declared weak signal; verifier precision is a T1 condition.

**FOR**
- Meta-Router (2025) states the exact dilemma: gold-standard labels are accurate but costly, preference and judge labels are cheap "yet often biased in reflecting the true quality of responses". Separating the two sources is the premise; LRN-001's tiers are that separation. [source: Meta-Router: Bridging Gold-standard and Preference-based Evaluations in Large Language Model Routing, 2025, https://arxiv.org/abs/2509.25535 · F]
- Label noise is the single most damaging noise type in LLM fine-tuning, which supports spending scarce effort on tier-1 purity rather than volume. [source: Analyzing the Effect of Noise in LLM Fine-tuning, 2026, https://arxiv.org/abs/2604.12469 · F]
- OpenAI's 2026 withdrawal from SWE-bench Verified (59.4% test flaws in the hard subset, verbatim solution reproduction) confirms clause 3: verified-by-tests is a tier only if the verifier's own precision is measured. [source: OpenAI Abandons SWE-Bench Verified, SiliconReport, 2026, https://www.siliconreport.com/openai-abandons-swe-bench-verified-citing-widespread-data-contamination-and-flawed-tests-6ebd9b34 · F]

**AGAINST**
- Meta-Router's remedy is not exclusion of cheap labels but causal correction: treat evaluation source as treatment assignment and jointly model gold and preference data, which improved routing accuracy over either source alone. LRN-001 permits T2-T4 only as "weak or unlabeled signal", forbidding the joint-modelling route that the 2025 paper shows is the efficient use of a small gold set plus a large biased set. [source: Meta-Router, 2025, https://arxiv.org/abs/2509.25535 · F]
- Confident-learning-style noise estimation (clause 2) requires per-example predicted probabilities from a model; a 2025-2026 benchmark finds in-sample gathering with average-probability aggregation and logit-margin disagreement works best, but all variants need a trained model with more than one task in its support. With a single-task T1, the noise estimator LRN-001 relies on cannot be fit. [source: Benchmarking noisy label detection methods, 2025 (revised 2026), https://arxiv.org/abs/2510.16211 · F]
- The 2025-2026 answer to "not enough organic verified tasks" is automated pipelines that mine fresh, decontaminated, executable tasks at scale (21,000 in SWE-rebench; production-in-distribution in REAP with multi-run stability checks). LRN-001 puts all of that in T4 "simulator/benchmark" with no path to T1, even when the tasks come from the organisation's own repositories under REAP-style curation. [source: SWE-rebench, 2025, https://arxiv.org/abs/2505.20411 · F] and [source: REAP, 2026, https://arxiv.org/abs/2604.01527 · F]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the tiers and the T1-only holdout, but permit a declared joint-modelling estimator (Meta-Router style) over T1 plus T3 with the bias term reported, instead of restricting lower tiers to pre-training and pseudo-labels. Add a T1b tier for tasks mined from the organisation's own repositories under REAP-style curation, distinct from public benchmarks.

---

### ADRL-LRN-002: Branched pairs, plus a logged-exploration channel

**Decision.** Pairs are live branches from the same snapshot and turn state with identical rules and verifier, sized to a power target, complemented by logged-propensity exploration (LRN-008).

**FOR**
- The Replay Gap (Aug 2026, ~900 rollouts) is the direct evidence: swaps rewrite 61-94% of post-fork actions, only 3% of replayed states remain valid, and replay mispredicts every success-relevant outcome call. Clause 1 is what the paper recommends. [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239 · F]
- IPS-style OPE "suffers from severe bias when the logging policy is fully deterministic" (ICLR 2026), which is clause 4's no-propensity statement stated as a theorem-level result. [source: Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies, 2026, https://arxiv.org/abs/2603.21485 · F]
- Logging-policy design is now a research area: concentrating mass on high-reward actions reduces variance but "risks missing signal on actions the target policy may take", which is the argument for pairs in the ambiguous band plus bounded exploration. [source: Logging Policy Design for Off-Policy Evaluation, 2026, https://arxiv.org/abs/2605.15108 · F]

**AGAINST**
- One branch per arm is not a pair under a stochastic policy. Causal Agent Replay re-executes forward "under the same stochastic policy" multiple times and measures the shift in the outcome distribution; measured inference determinism varies 5.8x across providers. The McNemar arithmetic in clause 3 assumes a deterministic outcome per arm and will understate the required n. [source: Causal Agent Replay, 2026, https://arxiv.org/abs/2606.08275 · F] and [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 · F]
- Model-based OPE for LLM agents now exists: ADWM learns a latent diffusion world model of environment responses and simulates the evaluated agent's own trajectories, avoiding both importance weights and live execution. LRN-002 names only pairs and logged exploration; a world-model channel, validated against branched ground truth, is the third instrument the 2026 literature offers and the Replay Gap explicitly asks for. [source: Autoregressive Diffusion World Models for Off-Policy Evaluation of LLM Agents, 2026, https://arxiv.org/abs/2606.05558 · F]
- WISERouter reports comparable routing performance on SWE-Bench "while using substantially less exploration data" via a constrained bandit; the pair budget of 115-235 per slice may be the wrong unit if online learning can amortise exploration across slices. [source: WISERouter, 2026, https://arxiv.org/abs/2607.23765 · F]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the decision; change clause 1 to require k stochastic branches per arm (k set from the same-model control divergence measured first) so each pair yields an outcome distribution, and restate the power target for paired proportions with within-arm variance. Add a third evidence channel, world-model OPE validated against branches, as a declared tier.

---

### ADRL-LRN-003: The target is a CATE, name it

**Decision.** Estimate the CATE of frontier over cheaper rungs given pre-decision features using meta-learners (X-learner default), from paired and exploration data; never train on the heuristic's decisions; never deploy a model that outputs a rung.

**FOR**
- Meta-Router independently reaches the same framing: router training is a causal-inference problem and "preference-data bias corresponds to conditional average treatment effects". [source: Meta-Router, 2025, https://arxiv.org/abs/2509.25535 · F]
- A May 2026 position paper by thirteen authors argues that routing and agentic workflows are inherently causal questions, that logged data are subject to confounding and distribution shift, and that learned judges are biased, which is LRN-003's rationale restated. [source: Causal Methods for LLM Development and Evaluation, 2026, https://arxiv.org/abs/2605.25998 · F]
- The Simpson's-paradox study of agent PRs shows naive outcome comparisons on observational logs reverse under controls, so refusing to train on the heuristic's own routing outcomes as targets is justified. [source: Beyond Simpson's Paradox, 2026, https://arxiv.org/abs/2606.22711 · F]

**AGAINST**
- The X-learner default is dated: the Hybrid learner (2025, revised Jan 2026) shows neither direct nor indirect meta-learners dominate and an interpolating H-learner sits on the Pareto frontier across benchmarks. Clause 2 should name the H-learner or a data-driven choice, not fix X. [source: Hybrid Meta-learners for Estimating Heterogeneous Treatment Effects, 2025/2026, https://arxiv.org/abs/2506.13680 · F]
- The plateau results cut against the estimator-first framing. Twenty-one routers on five benchmarks plateau because they learn global averages, and the levers are more data, stronger encoders and end-to-end fine-tuning; LLMRouterBench finds backbone embeddings barely matter and model-recall failures dominate. A CATE over a small tabular pre-decision feature vector is a plateau router by construction, and ADRL's D0 estimator has no plan for the levers. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587 · F] and [source: LLMRouterBench, 2026, https://arxiv.org/abs/2601.07206 · F]
- "Never deploy a model whose output is a rung" is contradicted by the strongest 2025-2026 routing results: BaRP trains a policy from partial bandit feedback that outputs the rung and beats offline routers by at least 12.46%; OrcaRouter's LinUCB policy ranked second on RouterArena. Cost-preference conditioning at inference (BaRP) achieves what clause 3 wants without separating estimator from decision. [source: Learning to Route LLMs from Bandit Feedback: One Policy, Many Trade-offs, 2025, https://arxiv.org/abs/2510.07429 · F] and [source: OrcaRouter, 2026, https://arxiv.org/abs/2605.30736 · F]
- Uncertainty on tau(x) has a 2025-2026 answer the ADR leaves open: conformal prediction intervals for individual treatment effects with coverage lower bounds under non-exchangeability. [source: Prediction Intervals for Individual Treatment Effects in a Multiple Decision Point Framework using Conformal Inference, 2025, https://arxiv.org/abs/2512.08828 · F]

**Grounding verdict.** CONTESTED (2026).

**Recommendation.** Keep the estimand and the label-source prohibition; replace the fixed X-learner with an H-learner or a validated choice, and specify conformal ITE intervals as the uncertainty method. Soften clause 3 to "the decision layer must be able to re-weight cost without retraining" (BaRP-style preference conditioning satisfies this) and add the plateau levers (richer encoders, end-to-end fine-tuning) as the funded path if the tabular estimator plateaus.

---

### ADRL-LRN-004: Pre-decision features, enforced by construction

**Decision.** Decision-time feature snapshot is the sole training source; retrieval features use as-of projections; temporal, session-grouped splits; versioned deny-list including served_rung.

**FOR**
- Point-in-time correct joins are the industry mechanism for exactly this: each training row takes the latest feature value at or before its label timestamp, and the documentation names future leakage as the failure being prevented. [source: Point-in-time feature joins, Databricks docs, 2026, https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series · F]
- RecSys 2025 shows evaluation outcomes and model rankings change materially between leave-one-out and global temporal splits, and only global temporal splitting prevents leakage; clause 3 is the right choice. [source: Time to Split, 2025, https://arxiv.org/abs/2507.16289 · F]
- The agent-PR confounder cascade (repository, commit count) is the observational-data warning behind grouping splits by session and repo. [source: Beyond Simpson's Paradox, 2026, https://arxiv.org/abs/2606.22711 · F]

**AGAINST**
- Snapshot-only training forbids feature engineering after the fact: a new feature cannot be back-tested on historical decisions because only features_v<N> was persisted. Feature-store practice keeps the raw event log and recomputes as-of features with versioned transformations, which is more flexible and equally leak-free. LRN-004 should allow as-of recomputation from the ledger under the same deny-list, not only the snapshot. [source: Point-in-time feature joins, Databricks docs, 2026, https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series · F]
- The plateau literature says routers need stronger encoders and end-to-end fine-tuning; if the pre-decision feature vector is frozen at decision time and the local embedding model changes (MEM-007), the snapshot becomes incomparable across time and the deny-list does not cover this drift. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587 · F]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the decision; permit a second training source, as-of recomputation from the ledger under the same deny-list and MEM-007 stamps, so that new features can be evaluated historically. Add the embedding-model version to the feature schema so snapshots from different encoders are never pooled.

---

### ADRL-LRN-005: Every artifact is fully versioned

**Decision.** Every learned artifact versions its feature schema, data snapshot, objective, calibration, thresholds and policy compatibility.

**FOR**
- 2026 MLOps guidance says every version must be traceable from training run to deployment through a registry, with audit logs and model cards generated as pipeline artifacts; LRN-005 is that rule. [source: MLOps Pipeline Automation Best Practices in 2026, MLflow, 2026, https://mlflow.org/articles/mlops-pipeline-automation-best-practices-in-2026/ · F]
- Atlas (2025) shows attestable ML pipelines built from open supply-chain provenance specifications, trusted hardware and transparency logs are practical in prototype. [source: Atlas: A Framework for ML Lifecycle Provenance & Transparency, 2025, https://arxiv.org/abs/2502.19567 · F]

**AGAINST**
- The field's baseline moved from "versioned" to "signed and attested": sigstore's model-signing v1.0 (April 2025) and the OpenSSF Model Signing specification bind artifacts to workload or developer identity with transparency-log inclusion proofs, and are integrated into major model hubs. LRN-005 versions the manifest but nothing signs it, so an artifact's declared lineage is not verifiable. [source: Taming the Wild West of ML: Practical Model Signing with Sigstore, 2025, https://blog.sigstore.dev/model-transparency-v1.0/ · F] and [source: OpenSSF Model Signing (OMS) Specification, 2025, https://github.com/ossf/model-signing-spec · S]
- Sample-level provenance (which ledger rows trained this artifact, with tamper-evident commitments) is now demonstrated with practical overhead; "data snapshot" as a ledger high-water mark is coarse by comparison and cannot answer "was this erased session in the training set?", which MEM-010 needs. [source: FG-Trac, 2026, https://arxiv.org/abs/2601.14971 · F]
- Sigstore itself says trusted provenance for ML workflows and dataset signing are "a future step", so attestation of the data side is not yet standardised; ADRL should not wait for that, but it means the manifest, not a standard, must carry the tier mix and high-water mark. [source: sigstore model-transparency v1.0, 2025, https://blog.sigstore.dev/model-transparency-v1.0/ · F]

**Grounding verdict.** DATED (mechanism; newest relevant source 2026).

**Recommendation.** Keep the text; add a follow-up to sign each artifact and its manifest with OpenSSF Model Signing so lineage claims are verifiable, and add a training-set membership commitment (Merkle root of route_ids in the training set) so MEM-010 erasure can identify affected artifacts.

---

### ADRL-LRN-006: Abstention with a declared risk-coverage target

**Decision.** Selective prediction with a declared target risk and measured coverage on a time-ordered T1 holdout; feature-space OOD detector; system-level risk target; abstention rate bounded and reported; abstention built before the estimator.

**FOR**
- Conformal risk control for LLM outputs now comes with a feasibility check: when base risk exceeds the target, any distribution-free method must abstain on at least a closed-form fraction, and adaptive conformal inference cut risk-target violations from 71% to 21% under shift. Clause 1's "risk first, coverage falls out" is the right form. [source: When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation, 2026, https://arxiv.org/abs/2606.29054 · F]
- Anytime-valid selective risk bounds for per-round deployment certification exist (e-processes on a Bonferroni grid, pathwise validity on 550+ streams), which is the deployment-side guarantee an EVL-009 abstention blocker needs across time. [source: Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs, 2026, https://arxiv.org/abs/2605.20270 · F]
- A bandit framing where abstention is an action and the agent learns "when not to learn" gives sublinear regret without exploration in regions where a single action could cause irreparable harm; it matches clause 3's hand-off to the deterministic policy. [source: Learning When Not to Learn: Risk-Sensitive Abstention in Bandits with Unbounded Rewards, 2025 (AISTATS 2026), https://arxiv.org/abs/2510.14884 · F]

**AGAINST**
- Marginal risk guarantees are insufficient: a model can meet the population budget while over-exposing subgroups, with violations reaching 47% under group-composition shift; hierarchical group-conditional CRC fixes this at a participation cost of 22-37 points. ADRL's subgroups are repos, intent classes and harnesses; clause 1 declares one marginal risk. [source: Hierarchical Group-Conditional Conformal Risk Control for Selective Prediction in Language Models, 2026, https://arxiv.org/abs/2607.24562 · F]
- Entropy or confidence alone has a model-dependent failure mode for abstention; combining it with a correctness probe improves the risk-coverage trade-off. Clause 1 leaves the uncertainty score unspecified. [source: Entropy Alone is Insufficient for Safe Selective Prediction in LLMs, 2026, https://arxiv.org/abs/2603.21172 · F]
- A May 2026 router decomposes uncertainty into reducible and irreducible parts and uses three actions: weak model when low, oracle when reducible is high, abstain when irreducible is high. LRN-006 has a two-way act/abstain gate; the three-way rule maps directly onto local, frontier and deterministic fallback and avoids paying for frontier on inherently ambiguous turns. [source: Flexible Routing via Uncertainty Decomposition, 2026, https://arxiv.org/abs/2605.07805 · F]
- Multi-expert learning-to-defer now has realizable H-consistent surrogates and a training-free conformal alternative; clause 3 cites two-expert deferral, but ADRL has three rungs plus the heuristic. [source: Mastering Multiple-Expert Routing: Realizable H-Consistency and Strong Guarantees for Learning to Defer, 2025, https://arxiv.org/abs/2506.20650 · S] and [source: No Need for Learning to Defer? A Training Free Deferral Framework to Multiple Experts through Conformal Prediction, 2025, https://arxiv.org/abs/2509.12573 · S]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Keep the decision; make the risk target group-conditional over repo and intent class (HG-CRC style) and use an anytime-valid certificate so the EVL-009 bound holds across the stream, not only on the holdout. Replace the binary gate with the reducible/irreducible three-way rule so abstention and "route up" are distinct outputs.

---

### ADRL-LRN-007: No autonomous online promotion

**Decision.** Learning may propose updates; deployment requires offline evaluation and explicit graduation; no autonomous online promotion.

**FOR**
- 2026 MLOps guidance: "automation without gating is just faster failure"; hard gates at data validation, champion-challenger evaluation on held-out data, and a named human owner for every pipeline. [source: MLOps Pipeline Automation Best Practices in 2026, MLflow, 2026, https://mlflow.org/articles/mlops-pipeline-automation-best-practices-in-2026/ · F]
- Spotify's deployed contextual bandit was validated offline and by A/B test before rollout, and its adaptation is bounded inside a graduated policy; this remains the production shape the ADR describes. [source: Calibrated Recommendations with Contextual Bandits on Spotify Homepage, 2025, https://research.atspotify.com/2025/9/calibrated-recommendations-with-contextual-bandits-on-spotify-homepage · S] and [source: Calibrated Recommendations with Contextual Bandits, 2025, https://arxiv.org/abs/2509.05460 · S]
- Where a single action can cause irreparable damage, the safe learner abstains rather than explores; that is the correct prior for a payments codebase. [source: Learning When Not to Learn, 2025, https://arxiv.org/abs/2510.14884 · F]

**AGAINST**
- Continuous online learning is now the norm in routing research, not the exception: BaRP learns under deployment's partial-feedback restriction and beats strong offline routers by at least 12.46%; OrcaRouter initialises offline then "can optionally continue learning from bandit feedback" in production; Agent-as-a-Router accumulates execution-grounded experience during deployment for the lowest regret on coding tasks. The ADR permits exploration data collection but not the policy update loop these systems rely on. [source: Learning to Route LLMs from Bandit Feedback, 2025, https://arxiv.org/abs/2510.07429 · F], [source: OrcaRouter: A Production-Oriented LLM Router with Hybrid Offline-Online Learning, 2026, https://arxiv.org/abs/2605.30736 · F], [source: Agent-as-a-Router, 2026, https://arxiv.org/abs/2606.22902 · F]
- Constrained contextual bandits now carry end-to-end regret bounds covering exploration and exploitation under a shared budget (O(sqrt(T)) for WISERouter; high-probability budget and latency satisfaction for COPAC-UCB). "No autonomous promotion" forgoes guarantees that are formally stronger than a monthly human review. [source: WISERouter, 2026, https://arxiv.org/abs/2607.23765 · F] and [source: Online LLM Selection via Constrained Bandits with Time-Varying Demand, 2026, https://arxiv.org/html/2606.17489 · S]
- The offline evaluation the ADR requires is itself unreliable for agentic routing (Replay Gap), and the world-model OPE alternative is new and unvalidated at ADRL's scale; "offline evaluation then graduate" may be a gate that certifies the wrong world. [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239 · F]

**Grounding verdict.** CONTESTED (2026).

**Recommendation.** Keep the rule for now, since every 2026 online-routing result is measured on benchmarks with cheap verified rewards that ADRL lacks. Add a sunset condition: when T1 volume and verifier precision pass the EVL gate, a bounded-parameter online update (LinUCB-style, inside a graduated feature schema, with a regret budget) is a permitted artifact class that graduates once, not per update.

---

### ADRL-LRN-008: Logged exploration in the ambiguous band

**Decision.** Inside the ambiguous band, among SAF-permitted rungs, a graduated exploration rule randomises the rung with bounded probability and logs the propensity; exploration turns are their own tier; DR estimators are validated against branched pairs.

**FOR**
- IPS estimators "suffer from severe bias when the logging policy is fully deterministic" (ICLR 2026); logging propensities is the precondition the paper states. [source: Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies, 2026, https://arxiv.org/abs/2603.21485 · F]
- Logging-policy design is now treated as an optimisation with practical design principles when the target policy is unknown or partially known; a versioned exploration artifact with a declared epsilon is that design made explicit. [source: Logging Policy Design for Off-Policy Evaluation, 2026, https://arxiv.org/abs/2605.15108 · F]
- Constrained bandit routers achieve comparable performance "while using substantially less exploration data" than supervised routers, so bounded exploration is the cheaper route to labels than full pairs. [source: WISERouter, 2026, https://arxiv.org/abs/2607.23765 · F]

**AGAINST**
- The ICLR 2026 result also shows an alternative: exploit intrinsic stochasticity in the environment (there, user clicks) to get low-bias OPE without randomising the logging policy. ADRL's analogue is the sampling stochasticity of the models and the escalation path; whether that yields usable propensities has not been examined, and it would avoid degrading developer turns on purpose. [source: Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies, 2026, https://arxiv.org/abs/2603.21485 · F]
- Surrogate rewards (a reward model's noisy estimate) can be combined with true rewards in a correlation-aware bandit with regret bounds that degrade gracefully when the surrogate is wrong; LRN-008's tier separation forbids blending surrogates with explored outcomes, which is the mechanism that would make small epsilon informative. [source: Correlation-Aware Contextual Bandits with Surrogate Rewards for LLM Routing, 2026, https://arxiv.org/abs/2607.09015 · F]
- The risk-sensitive bandit literature argues that in settings where one action can do irreparable harm, the right policy is to establish a trusted region and never explore outside it. Downward exploration (local where the heuristic said frontier) on payments code is exactly that setting; clause 2's "downward epsilon can be set lower" should be "downward exploration only inside a verified trusted region". [source: Learning When Not to Learn, 2025, https://arxiv.org/abs/2510.14884 · F]
- Doubly-robust methods "partially mitigate bias but do not resolve the fundamental difficulties of long-horizon distribution shift in high-dimensional text spaces"; validating DR against branched pairs (clause 4) is necessary but the pair count needed to validate is the same count the exploration channel was meant to avoid. [source: Autoregressive Diffusion World Models for OPE of LLM Agents, 2026, https://arxiv.org/abs/2606.05558 · F]

**Grounding verdict.** CURRENT (2026).

**Recommendation.** Accept at D0 with two edits: restrict downward exploration to a trusted region defined by prior verified local successes (not just the ambiguous band), and add a follow-up to test whether model sampling stochasticity plus escalation outcomes yield usable propensities before any developer turn is randomised. Permit a declared surrogate-reward blend inside the explore tier under the correlation-aware estimator.

---

## Verdict tally

| Verdict | Decisions |
|---|---|
| CURRENT | MEM-001, MEM-002, MEM-003, MEM-005, MEM-006, MEM-007, MEM-008, MEM-009, MEM-010, LRN-001, LRN-002, LRN-004, LRN-006, LRN-008 (14) |
| CONTESTED | MEM-004, LRN-003, LRN-007 (3) |
| DATED | LRN-005 (1) |
| UNGROUNDED | none (0) |

---

## Sources

F = fetched with WebFetch; S = appeared in a WebSearch result with matching title, not fetched.

1. Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents (2026), https://arxiv.org/abs/2606.30306 · F
2. Fine-Grained Traceability for Transparent ML Pipelines (FG-Trac) (2026), https://arxiv.org/abs/2601.14971 · F
3. Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use (2026), https://arxiv.org/abs/2603.14332 · F
4. Governed Reasoning for Institutional AI (2026), https://arxiv.org/pdf/2604.10658 · S
5. EDPB Guidelines 02/2025 on processing of personal data through blockchain, v2.0 (July 2026), https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf · S
6. EDPB news: adopts guidelines on processing personal data through blockchains (April 2025), https://www.edpb.europa.eu/news/news/2025/edpb-adopts-guidelines-processing-personal-data-through-blockchains-and-ready_en · F
7. Blockchain And GDPR: EDPB Guidelines 02/2025 Adopted, Mondaq (2026), https://www.mondaq.com/fin-tech/1617044/blockchain-and-gdpr-edpb-guidelines-022025-adopted · S
8. Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction (WWW 2026), https://arxiv.org/abs/2601.19965 · F
9. Follow the TRACE: Exploiting Post-Click Trajectories for Online Delayed Conversion Rate Prediction (2026), https://arxiv.org/abs/2604.23197 · F
10. How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions (2026), https://arxiv.org/abs/2605.29442 · F
11. The Maintainability Gap: 2026 AI Code Quality Research, GitClear (2026), https://www.gitclear.com/the_ai_code_quality_maintainability_gap · S
12. Early-Stage Prediction of Review Effort in AI-Generated Pull Requests (MSR 2026), https://arxiv.org/html/2601.00753 · S
13. Adoption and Impact of Command-Line AI Coding Agents (Microsoft, 2026), https://arxiv.org/abs/2607.01418 · F
14. Why SWE-bench Verified no longer measures frontier coding capabilities, OpenAI (2026), https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ · S (fetch returned 403)
15. OpenAI Abandons SWE-Bench Verified, SiliconReport (2026), https://www.siliconreport.com/openai-abandons-swe-bench-verified-citing-widespread-data-contamination-and-flawed-tests-6ebd9b34 · F
16. Is SWE-bench Verified Contaminated? OpenAI Shifts to SWE-bench Pro, CodeSOTA (2026), https://www.codesota.com/news/swe-bench-contamination-debate · F
17. On the Flakiness of LLM-Generated Tests for Industrial and Open-Source Database Management Systems (2026), https://arxiv.org/abs/2601.08998 · F
18. Are Coding Agents Generating Over-Mocked Tests? An Empirical Study (2026), https://arxiv.org/abs/2602.00409 · F
19. Lean4Agent: Formal Modeling and Verification for Agent Workflow and Trajectory (2026), https://arxiv.org/abs/2606.06523 · F
20. REAP: Automatic Curation of Coding Agent Benchmarks from Interactive Production Usage (ASE 2026), https://arxiv.org/abs/2604.01527 · F
21. SWE-rebench (NeurIPS 2025), https://arxiv.org/abs/2505.20411 · F
22. Testing with AI Agents: An Empirical Study of Test Generation Frequency, Quality, and Coverage (MSR 2026), https://arxiv.org/abs/2603.13724 · F
23. Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures (2026), https://arxiv.org/abs/2607.28802 · F
24. Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in LLM Agents (2026), https://arxiv.org/abs/2607.05775 · F
25. The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break (2026), https://arxiv.org/html/2604.11978v1 · S
26. Who&When Pro: Can LLMs Really Attribute Failures in AI Agents? (2026), https://arxiv.org/abs/2607.09996 · F
27. Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures (2026), https://arxiv.org/abs/2606.08275 · F
28. Analyzing the Effect of Noise in LLM Fine-tuning (2026), https://arxiv.org/abs/2604.12469 · F
29. Benchmarking noisy label detection methods (2025, revised 2026), https://arxiv.org/abs/2510.16211 · F
30. Zero2Text: Zero-Training Cross-Domain Inversion Attacks on Textual Embeddings (2026), https://arxiv.org/abs/2602.01757 · F
31. Concept-Aware Privacy Mechanisms for Defending Embedding Inversion Attacks (SPARSE) (2026), https://arxiv.org/abs/2602.07090 · F
32. BeamClean: Language Aware Embedding Reconstruction (2025), https://arxiv.org/abs/2505.13758 · S
33. Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases (2026), https://arxiv.org/abs/2606.18497 · F
34. Art.17 Right to Erasure: LLM Training Data Removal & RAG Vector Store Deletion 2026, sota.io (2026), https://sota.io/blog/eu-ai-act-gdpr-art17-right-erasure-training-data-llm-2026 · F
35. Crypto-Shredding: The Technical Foundation for Reconciling GDPR and Financial Record-Keeping Obligations, VeritasChain (2026), https://veritaschain.org/blog/posts/2026-01-18-crypto-shredding-gdpr-mifid-ii-reconciliation/ · F
36. SoK: Unlearnability and Unlearning for Model Dememorization (2026), https://arxiv.org/pdf/2605.11592 · S
37. SQLite in Production 2026: Real Benchmarks, Limits, and When to Migrate to Postgres (2026), https://sesamedisk.com/sqlite-in-production-2026-benchmarks-limits/ · S
38. SQLite Litestream Replication in Production Guide (2026), https://www.matthewswong.com/en/blog/sqlite-litestream-replication-production/ · S
39. OpenTelemetry's GenAI semantic conventions are NOT stable yet (2026), https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke · S
40. How OpenTelemetry Traces LLM Calls, Agent Reasoning, and MCP Tools, Greptime (2026), https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions · S
41. LiveVectorLake: A Real-Time Versioned Knowledge Base Architecture for Streaming Vector Updates and Temporal Retrieval (2025), https://arxiv.org/abs/2601.05270 · F
42. Point-in-time feature joins, Databricks docs (2026), https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series · F
43. Time to Split: Exploring Data Splitting Strategies for Offline Evaluation of Sequential Recommenders (RecSys 2025), https://arxiv.org/abs/2507.16289 · F
44. The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers (2026), https://arxiv.org/abs/2606.07587 · F
45. LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing (2026), https://arxiv.org/abs/2601.07206 · F
46. RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers (ICLR 2026), https://proceedings.iclr.cc/paper_files/paper/2026/file/4987bb24bc53c198785922d1bd9e18cf-Paper-Conference.pdf · S
47. Agent-as-a-Router: Agentic Model Routing for Coding Tasks (2026), https://arxiv.org/abs/2606.22902 · F
48. WISERouter: LLM Routing with Workload Budget Constraint (2026), https://arxiv.org/abs/2607.23765 · F
49. The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World (2026), https://arxiv.org/abs/2608.08239 · F
50. Beyond Simpson's Paradox: A Cascade of Confounders in AI Agent Pull-Request Co-Authorship (2026), https://arxiv.org/abs/2606.22711 · F
51. Meta-Router: Bridging Gold-standard and Preference-based Evaluations in LLM Routing (2025), https://arxiv.org/abs/2509.25535 · F
52. Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies (ICLR 2026), https://arxiv.org/abs/2603.21485 · F
53. Logging Policy Design for Off-Policy Evaluation (2026), https://arxiv.org/abs/2605.15108 · F
54. Autoregressive Diffusion World Models for Off-Policy Evaluation of LLM Agents (2026), https://arxiv.org/abs/2606.05558 · F
55. Causal Methods for LLM Development and Evaluation (2026), https://arxiv.org/abs/2605.25998 · F
56. Hybrid Meta-learners for Estimating Heterogeneous Treatment Effects (2025, revised 2026), https://arxiv.org/abs/2506.13680 · F
57. Learning to Route LLMs from Bandit Feedback: One Policy, Many Trade-offs (BaRP) (2025), https://arxiv.org/abs/2510.07429 · F
58. OrcaRouter: A Production-Oriented LLM Router with Hybrid Offline-Online Learning (2026), https://arxiv.org/abs/2605.30736 · F
59. Prediction Intervals for Individual Treatment Effects in a Multiple Decision Point Framework using Conformal Inference (2025), https://arxiv.org/abs/2512.08828 · F
60. MLOps Pipeline Automation Best Practices in 2026, MLflow (2026), https://mlflow.org/articles/mlops-pipeline-automation-best-practices-in-2026/ · F
61. Atlas: A Framework for ML Lifecycle Provenance & Transparency (2025), https://arxiv.org/abs/2502.19567 · F
62. Taming the Wild West of ML: Practical Model Signing with Sigstore (model-transparency v1.0) (2025), https://blog.sigstore.dev/model-transparency-v1.0/ · F
63. OpenSSF Model Signing (OMS) Specification (2025), https://github.com/ossf/model-signing-spec · S
64. When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation (2026), https://arxiv.org/abs/2606.29054 · F
65. Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs (2026), https://arxiv.org/abs/2605.20270 · F
66. Hierarchical Group-Conditional Conformal Risk Control for Selective Prediction in Language Models (2026), https://arxiv.org/abs/2607.24562 · F
67. Entropy Alone is Insufficient for Safe Selective Prediction in LLMs (2026), https://arxiv.org/abs/2603.21172 · F
68. Conformal Selective Prediction with General Risk Control (SCoRE) (2026), https://arxiv.org/abs/2603.24704 · F
69. Learning When Not to Learn: Risk-Sensitive Abstention in Bandits with Unbounded Rewards (AISTATS 2026), https://arxiv.org/abs/2510.14884 · F
70. Flexible Routing via Uncertainty Decomposition (2026), https://arxiv.org/abs/2605.07805 · F
71. Mastering Multiple-Expert Routing: Realizable H-Consistency and Strong Guarantees for Learning to Defer (2025), https://arxiv.org/abs/2506.20650 · S
72. No Need for Learning to Defer? A Training Free Deferral Framework to Multiple Experts through Conformal Prediction (2025), https://arxiv.org/abs/2509.12573 · S
73. macrOData: New Benchmarks of Thousands of Datasets for Tabular Outlier Detection (KDD 2026), https://arxiv.org/abs/2602.09329 · F (consulted for LRN-006 OOD; abstract gives no method ranking, so not cited in a bullet)
74. From Zero to Hero: Advancing Zero-Shot Foundation Models for Tabular Outlier Detection (2026), https://arxiv.org/abs/2602.03018 · F (consulted for LRN-006 OOD; not cited in a bullet)
75. Calibrated Recommendations with Contextual Bandits on Spotify Homepage (2025), https://research.atspotify.com/2025/9/calibrated-recommendations-with-contextual-bandits-on-spotify-homepage · S
76. Calibrated Recommendations with Contextual Bandits (2025), https://arxiv.org/abs/2509.05460 · S
77. Online LLM Selection via Constrained Bandits with Time-Varying Demand (2026), https://arxiv.org/html/2606.17489 · S
78. Correlation-Aware Contextual Bandits with Surrogate Rewards for LLM Routing (2026), https://arxiv.org/abs/2607.09015 · F
79. Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey (TMLR 2026), https://arxiv.org/abs/2603.04445 · F (consulted for the LRN field summary)
80. Uncertainty-Guided LLM Semantic Augmentation for Heterogeneous Treatment Effect Estimation (CURL) (2026), https://arxiv.org/abs/2607.26599 · F (consulted for LRN-003; not cited in a bullet)
