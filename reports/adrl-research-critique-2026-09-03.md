# ADRL research critique, 2026-09-03
Are the 77 decisions in the ADRL register grounded in the latest research? A research-backed adversarial critique, one FOR case and one AGAINST case per decision, with a grounding verdict and a proposed disposition. Companion to REVIEW-LOG.md and INDEX.md; nothing in the register is changed by this report.
## 1. Method and honesty statement

This critique was produced on 2026-09-03 by five parallel literature searches, one per slice of the register (FND with SEM and TRU; SAF with OPS; RTG with CAS; MEM with LRN; EVL with a field survey). Each search read the current Decision, Context and existing Adversarial review of every decision in its slice, then searched the web for 2025 and 2026 research and vendor documentation on that decision's subject, and wrote a FOR case, an AGAINST case, a grounding verdict and a recommendation per decision.

Citation rule. Every claim carries a source tag naming the title, year and URL. A source is marked **fetched** when the page was retrieved and read on 2026-09-03, and **search** when only its title and snippet appeared in a search result with a matching title. Claims from memory were excluded by instruction; where a searcher could not source a claim it says so. Two pages returned HTTP 403 (OpenAI's SWE-bench Verified retirement post and the NSA MCP security sheet) and are cited by title with a secondary source for the figures. Several load-bearing papers are 2026 preprints, some single-author (the Replay Gap, Bounded Agents, the Handoff Tax); they are treated as the current frontier, not as settled results, and the verdicts say so where it matters.

Verdict scale. **CURRENT**: the decision is supported by 2025 to 2026 work. **DATED**: the principle holds but the mechanism or evidence base rests on pre-2025 work that newer work qualifies. **CONTESTED**: credible recent work argues both sides of a load-bearing clause. **UNGROUNDED**: no direct literature was found and the decision rests on first principles. Each verdict names the newest relevant source year.

Relation to the 2026-09-02 review. That review attacked each decision from system-specific angles and amended the text. This critique does not repeat those attacks; it asks a different question, whether the amended text is where the research is today, and where the two overlap it reports the newer source that confirms or overturns the earlier finding.

Scope. All 77 decisions in the register as of 2026-09-03: the 49 original decisions as amended, the six proposed on 2026-09-02, and the 22 proposed on 2026-09-03 (TRU-001 to 003, SEM-007, CAS-009, EVL-001 to 009, OPS-001 to 008). Sources: 315 distinct URLs after deduplication across the five searches, 250 fetched and 65 search-only.
## 2. Verdict summary
| Verdict | Decisions |
|---|---|
| CURRENT | 55 |
| CONTESTED | 17 |
| DATED | 5 |
| UNGROUNDED | 0 |
| Total | 77 |

| Bucket | Decisions | Current | Contested | Dated | Contested and dated decisions |
|---|---|---|---|---|---|
| FND System Boundary and Principles | 5 | 5 | 0 | 0 | none |
| SEM Interaction Semantics | 7 | 4 | 2 | 1 | SEM-002, SEM-006; dated: SEM-004 |
| SAF Safety, Privacy, Hard Constraints | 9 | 5 | 3 | 1 | SAF-002, SAF-007, SAF-008; dated: SAF-003 |
| TRU Trust, Residency and Egress | 3 | 3 | 0 | 0 | none |
| RTG Routing Intelligence and Economics | 9 | 5 | 3 | 1 | RTG-001, RTG-002, RTG-004; dated: RTG-006 |
| CAS Execution, Cascade, Recovery | 9 | 7 | 2 | 0 | CAS-004, CAS-005 |
| MEM Memory, Evidence, Label Integrity | 10 | 9 | 1 | 0 | MEM-004 |
| LRN Learning and Adaptation | 8 | 5 | 2 | 1 | LRN-003, LRN-007; dated: LRN-005 |
| EVL Evaluation, Graduation, Rollout | 9 | 6 | 3 | 0 | EVL-001, EVL-004, EVL-007 |
| OPS Platform, Runtime, Operations | 8 | 6 | 1 | 1 | OPS-006; dated: OPS-002 |

### The answer to the owner's question

The register is at the frontier where it is structural and behind where it is mechanical. Its spine, hard gates before optimisation, a monotone permitted set, one routing decision per turn with continuations inheriting, escalation only at action boundaries, an append-only ledger, verified-only training labels, live branches over replay, and human graduation, is what the 2026 literature independently recommends, and several of its 2026-09-03 additions (TRU, EVL, OPS) cite the newest sources directly. It is behind in five mechanisms that the field replaced in the last eighteen months: regex-and-entropy secret detection (SAF-003), a prompted single-shot difficulty classifier (RTG-006), client-side compaction as the model of utility traffic (SEM-004), long-lived KMS keys with annual rotation (OPS-002), and versioned-but-unsigned learned artifacts (LRN-005). And it is contested in seventeen places where the frontier itself is unsettled, most consequentially in routing direction: the newest evidence says escalating a cheap model's full trajectory recovers under half the quality gap at a cost premium while downshifting pays, that prompt-conditioned routers plateau far below the oracle and only trajectory-conditioned decisions escape it, and that giving verified past outcomes routing authority beats keeping them advisory. Those three results cut against local-first, carry-the-transcript handoff, sticky-up-only escalation and advisory-only retrieval at once, and they are preprints from June to August 2026. The honest position is that the register's routing economics were designed for a world of static routers, and the field moved to trajectory-conditioned routing while the register was being reviewed.

## 3. Findings that should change decisions, ranked
Ranked by how many load-bearing clauses the finding reaches and how strong the source is. Each item names the finding, its sources, the decisions affected and a concrete disposition for the owner.

### 3.1 The Handoff Tax inverts the direction of the cascade

**Finding.** Full-trajectory escalation from a cheap model to a strong one recovers less than half of the quality gap while incurring a substantial cost premium; reducing the cheap model's trajectory improves escalation quality; downshifting from a strong model to a cheap one is a favourable cost-quality point. The Replay Gap adds that a swapped model rewrites 61 to 94 percent of post-fork actions, so the carried transcript is mostly sunk cost.

**Sources.**
- The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents, 2026, https://arxiv.org/abs/2608.24358 (fetched)
- The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World, 2026, https://arxiv.org/abs/2608.08239 (fetched)
- Not Diamond Code: intelligent model routing for coding agents, 2026, https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents (fetched)

**Decisions affected.** ADRL-RTG-004, ADRL-CAS-004, ADRL-CAS-005, ADRL-RTG-001, ADRL-RTG-002, ADRL-RTG-007, ADRL-RTG-009, ADRL-CAS-003

**Proposed disposition.** Amend RTG-004 to reframe local-first as a short information-gathering exploration whose output feeds the temporal estimand, not a completion attempt. Amend CAS-004's pair table with direction and interface columns (escalate: compact or remove the cheap trajectory; downshift: keep the strong trajectory, strip its signatures). Amend CAS-005 to name lowering boundaries (compaction, verified progress) and to permit effort reduction within a rung. Declare downshift edges in RTG-001 and score downshift at a boundary in RTG-009 rather than as a switch penalty only. Compare frontier-first-then-downshift against local-first in shadow before widening local scope.

### 3.2 Prompt-conditioned routing has hit a plateau; only trajectory-conditioned decisions escape it

**Finding.** Across 21 routers and five benchmarks, routers converge into a narrow band far below the oracle because they learn global model averages rather than per-query signal; several commercial routers fail to beat a simple baseline on a 400K-instance benchmark; and once selection-valid intervals are used the strongest deployable prompt router recovers only 7.5 to 14.4 percent of the oracle gap. SWE-Router shows that conditioning on a cheap model's partial trajectory is Bayes-better than routing on the prompt.

**Sources.**
- The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers, 2026, https://arxiv.org/abs/2606.07587 (fetched)
- LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing, 2026, https://arxiv.org/abs/2601.07206 (fetched)
- Opportunity Is Not Realizability: Selection-Valid Diagnostics for Multi-LLM Routing, 2026, https://arxiv.org/abs/2608.08265 (fetched)
- SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks, 2026, https://arxiv.org/abs/2607.00053 (fetched)

**Decisions affected.** ADRL-RTG-002, ADRL-RTG-006, ADRL-RTG-003, ADRL-LRN-003, ADRL-EVL-001, ADRL-RTG-007

**Proposed disposition.** Amend RTG-002 so P(complete) is re-estimated at each action boundary from the partial trajectory. Reconsider RTG-006's mechanism: replace the prompted single-shot advisor with a small local model or a draft-agreement signal over the partial trajectory, keeping the governance clauses. State in RTG-003 that the ambiguous band is the plateau gap, not a minority residual. Add to RTG-007's gate a data threshold in the thousands and the plateau levers (richer encoders, end-to-end fine-tuning) as the funded path if the tabular estimator plateaus.

### 3.3 Execution-grounded memory given routing authority beats advisory retrieval, and policies that output a rung beat offline routers

**Finding.** Agent-as-a-Router accumulates verified task-level outcome statistics during deployment and gains 15.3 percent over a heuristic router built on the same priors, with the lowest regret on coding tasks. BaRP trains a policy from partial bandit feedback that outputs the rung and beats offline routers by at least 12.46 percent; OrcaRouter continues learning online in production. This is the mechanism MEM-008 keeps advisory and the output form LRN-003 forbids.

**Sources.**
- Agent-as-a-Router: Agentic Model Routing for Coding Tasks, 2026, https://arxiv.org/abs/2606.22902 (fetched)
- Learning to Route LLMs from Bandit Feedback: One Policy, Many Trade-offs (BaRP), 2025, https://arxiv.org/abs/2510.07429 (fetched)
- OrcaRouter: A Production-Oriented LLM Router with Hybrid Offline-Online Learning, 2026, https://arxiv.org/abs/2605.30736 (fetched)
- WISERouter: LLM Routing with Workload Budget Constraint, 2026, https://arxiv.org/abs/2607.23765 (fetched)

**Decisions affected.** ADRL-MEM-008, ADRL-LRN-003, ADRL-LRN-007, ADRL-RTG-003

**Proposed disposition.** Keep the gate in MEM-008 but change what it measures (coverage and verified-outcome agreement) and permit retrieval of verified outcomes to advise the estimator before it advises routing. Soften LRN-003 clause 3 to 'the decision layer must re-weight cost without retraining', which BaRP-style preference conditioning satisfies. Add a sunset condition to LRN-007: once T1 volume and verifier precision pass the EVL gate, a bounded-parameter online update inside a graduated feature schema is a permitted artifact class that graduates once. Keep the caveat that every 2026 online-routing result was measured with cheap verified rewards ADRL does not yet have.

### 3.4 Anthropic's thinking binding and the same-family trace exfiltration flaw make handoff a security boundary

**Finding.** Thinking signatures on the newest Anthropic models are bound to the model and the conversation prefix, enforced for accounts created on or after 31 August 2026; any prefix edit inside a rung yields a 400 unless the drop_block behaviour is set. A flaw disclosed in August 2026 let weaker models decode stronger models' encrypted reasoning within the same provider family, with 315,320 thinking blocks and 62 API keys recovered from public logs before mitigation. Effort changes at xhigh or max cannot turn thinking off.

**Sources.**
- Thinking (Claude Platform Docs), 2026, https://platform.claude.com/docs/en/build-with-claude/thinking (fetched)
- OpenAI, Anthropic, Google API Flaw Let Weaker AI Models Decode Stronger Models' Reasoning, 2026, https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html (fetched)
- Stealing Reasoning Traces from Proprietary LLM APIs (as reported), 2026, https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/ (fetched)
- Incident Report: Encrypted Content Failures in Multi-Region Responses API Load Balancing (LiteLLM), 2026, https://docs.litellm.ai/blog/responses-api-encrypted-content-incident (fetched)

**Decisions affected.** ADRL-CAS-004, ADRL-RTG-008, ADRL-CAS-006, ADRL-RTG-001, ADRL-RTG-005, ADRL-RTG-009

**Proposed disposition.** Amend CAS-004 with a compaction row (set drop_block or strip blocks) and key the pair table by served deployment, not model family. Amend RTG-008 with two contract clauses: the gateway never modifies the prefix inside a rung or reports every transformation, and hedging is disabled when tool calls may be emitted. Amend CAS-006 to add provider_fallback to served_source, record input_transformations verbatim, and flag a within-family downgrade with signatures present as a security event that forces the strip path. Add a re-reasoning charge on downswitch to RTG-005 and RTG-009. Record in RTG-001 that an effort change can change transcript contents.

### 3.5 Server-side compaction dates the utility-call model, and the auto-mode permission classifier is a class the taxonomy lacks

**Finding.** Anthropic's compaction beta (compact-2026-01-12, also on Bedrock, Vertex and Foundry) writes the summary as a compaction block inside the inference response after which all earlier content is ignored and earlier thinking blocks are dropped; OpenAI's compaction item is opaque and encrypted. Once the harness adopts it there is no compaction request to classify. Separately, auto-mode permission classifier requests skip the harness system prompt, carry the action under evaluation, and are identifiable only by the attribution block; serving them from a local model changes a safety verdict.

**Sources.**
- Compaction (Claude Platform Docs), 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)
- Compaction (OpenAI API guide), 2026, https://developers.openai.com/api/docs/guides/compaction (fetched)
- Gateway protocol reference (Claude Code docs), 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)

**Decisions affected.** ADRL-SEM-004, ADRL-SEM-001, ADRL-FND-003, ADRL-SEM-005, ADRL-SEM-007, ADRL-FND-001

**Proposed disposition.** Amend SEM-004 to define behaviour for both compaction modes, including the pinned-lineage rule when a cloud deployment would write the block, and keep the cosmetic-local rule. Amend SEM-001 to add the safety-classifier request as a seventh class that is always passthrough to the harness-requested model, and to recognise compaction-bearing requests. Amend FND-003 and SEM-005 to name the post-compaction first turn as a candidate re-decision point with a confirming signal. Amend SEM-007 so anthropic-messages-v1 covers only ANTHROPIC_BASE_URL traffic and lists the Bedrock and Vertex client formats as variants.

### 3.6 The harness sandbox SAF-007 relies on had four escapes in nine months and the vendor says use a VM for untrusted repositories

**Finding.** CVE-2025-66479 made deny-all network behave as allow-all for five weeks; a SOCKS5 null-byte bypass, CVE-2026-39861 (symlink following) and CVE-2026-55607 (a worktree named .git escaping Seatbelt, fixed July 2026) followed. Anthropic's own guidance for untrusted repositories is a dedicated VM, and on Linux the deny list is built at launch so a worktree created at the action boundary falls outside it. macOS sandbox-exec is deprecated with no removal date. Cursor's sandbox was escaped the same way.

**Sources.**
- Anthropic Silently Patches Claude Code Sandbox Bypass (SecurityWeek), 2026, https://www.securityweek.com/anthropic-silently-patches-claude-code-sandbox-bypass/ (fetched)
- CVE-2026-55607 advisory (GitLab), 2026, https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2026-55607/ (fetched)
- Choose a sandbox environment (Claude Code docs), 2026, https://code.claude.com/docs/en/sandbox-environments (fetched)
- Clarify sandbox-exec deprecation timeline (apple/containerization issue 737), 2026, https://github.com/apple/containerization/issues/737 (fetched)

**Decisions affected.** ADRL-SAF-007, ADRL-OPS-001, ADRL-OPS-003

**Proposed disposition.** Amend SAF-007 to require a microVM or container boundary (Firecracker, gVisor, Docker sandboxes) for restricted repositories and reserve Seatbelt and bubblewrap for unrestricted ones, matching the vendor's own tiering; add a synthetic 'sandbox actually on' probe before every verification run. Amend OPS-001 to define host as the isolation boundary the proxy shares with the harness. Amend OPS-003 to require authentication on every on-host endpoint, since MCP servers and hooks run unconstrained on the host.

### 3.7 The served-identity receipt has no source on streamed traffic, and the vendor gateway documents no per-response deployment identifier

**Finding.** LiteLLM omits x-litellm-model-api-base on chunked responses and a reported bug returns the group alias in the body model field; Claude Code requires streaming. Anthropic's Claude apps gateway fails over across regions and providers without developers noticing and documents no per-response deployment identifier. Route-receipt research names the artifact but does not say who signs it. Served identity therefore degrades to assumed_intended on nearly all inference traffic, and the 'pinned lineage reached cloud' runbook has no reliable trigger.

**Sources.**
- Response header x-litellm-model-api-base is missing on chunked responses (LiteLLM issue 7249), 2026, https://github.com/BerriAI/litellm/issues/7249 (search)
- response body model field returns model group alias (LiteLLM issue 22709), 2026, https://github.com/BerriAI/litellm/issues/22709 (search)
- Claude apps gateway (Claude Code docs), 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)
- Model Routing as a Trust Problem: Route Receipts for Adaptive AI Systems, 2026, https://arxiv.org/abs/2605.01710 (fetched)

**Decisions affected.** ADRL-OPS-006, ADRL-OPS-003, ADRL-OPS-007, ADRL-TRU-002, ADRL-FND-002, ADRL-RTG-008

**Proposed disposition.** Amend RTG-008 to require deployment identity in a trailer or in-band metadata on streamed responses, with return_raw_model_name as a second channel; until then treat every streamed row as assumed_intended and expect the OPS-006 blocker to hold. Add gateway_attested to the receipt source enum in TRU-002 as the Q7 target, add source_region and the gateway hop to the inventory entry, and state that a Claude apps gateway upstream yields assumed_intended receipts until it attests. Make the streamed-identity fix a prerequisite of the OPS-007 runbook, and reconcile served geography periodically against the provider's own log.

### 3.8 Rate-based fail-open SLIs cannot see a gate that is silently off

**Finding.** During the CVE-2025-66479 window a deny-all network setting behaved as allow-all for five weeks and the affected teams had no way to know; a gate that never runs produces zero fail-open events and a perfect SLO. The SRE error-budget framing, applied to gate-path fail-open on unpinned lineages, defines an accepted leak budget, and routing the alert to the developer whose session triggered it removes the independence the model assumes.

**Sources.**
- Anthropic Silently Patches Claude Code Sandbox Bypass (SecurityWeek), 2026, https://www.securityweek.com/anthropic-silently-patches-claude-code-sandbox-bypass/ (fetched)
- Implementing SLOs (Google SRE Workbook), 2018, https://sre.google/workbook/implementing-slos/ (fetched)
- Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents, 2026, https://arxiv.org/abs/2606.26479 (fetched)

**Decisions affected.** ADRL-OPS-008, ADRL-FND-005, ADRL-SAF-007

**Proposed disposition.** Amend OPS-008 to add a synthetic-probe SLI: a scheduled secret-bearing request that must produce a pin and a ledger row, so a silently-off gate breaches within one interval; require an error-budget policy with a freeze action for gate-path fail-open on unpinned lineages; route that alert to someone other than the developer. Amend FND-005's EVL follow-ups so every gate includes at least one adaptive adversarial test and one user-utility SLI.

### 3.9 Secret detection moved to regex plus LLM classification, and open PII detectors score below 0.14 F1 across domains

**Finding.** A regex-plus-LLM pipeline reaches 94.49 percent F1 (MSR 2026) and a fine-tuned 8B model reaches 0.985 on 818 repositories, with the authors concluding that regex and entropy tools generate high false positives from limited context; GitHub's July 2026 secret_category field separates provider patterns from generic and AI-detected ones, and its AI detector skips code files and test paths. PIIBench (2.37M sequences, 48 entity types) finds every open PII system below 0.14 span-level F1 with the best (Presidio) at 0.1385 and zero recall on most entity types.

**Sources.**
- Secret Leak Detection in Software Issue Reports using LLMs (MSR 2026), 2026, https://arxiv.org/abs/2410.23657 (fetched)
- Secret Breach Detection in Source Code with Large Language Models, 2025, https://arxiv.org/abs/2504.18784 (fetched)
- Improvements to secret scanning and public monitoring (GitHub Changelog), 2026, https://github.blog/changelog/2026-07-15-improvements-to-secret-scanning-and-public-monitoring/ (fetched)
- PIIBench, 2026, https://arxiv.org/abs/2604.15776 (fetched)

**Decisions affected.** ADRL-SAF-003, ADRL-SAF-008, ADRL-OPS-005

**Proposed disposition.** Amend SAF-003 to add an LLM contextual-classification tier served on the local rung, measured against the regex tiers on the same corpus, and to replace retroactive deletion with per-lineage or per-epoch encryption so suppression is key destruction. Demote SAF-008 clause 3 from a detector tier with pin semantics to shadow-only PII findings until a measured F1 on a the company fixture-and-log corpus exceeds a pre-registered floor. Record in OPS-005 that the shadow corpus is biased toward cloud-permitted traffic.

### 3.10 EDPB guidance, Ghost Vectors and Zero2Text change what 'prompt-class data' must mean for the ledger

**Finding.** The EDPB's final blockchain guidelines (v2, July 2026) recommend not registering clear-text, encrypted or hashed personal data on an immutable ledger at all and designing erasure in up front, accepting key destruction as erasure only where off-ledger storage was considered. Ghost Vectors shows soft-deleted vectors remain recoverable from HNSW index files with 100 percent recovery of structured demographics; encrypt-with-key-discard reduced recovery to zero. Zero2Text inverts black-box embeddings with no training pairs and defeats differential-privacy noise, so the quantisation follow-up in MEM-005 is dead on arrival. NIST SP 800-88 Rev. 2 says cryptographic erase is not assured where keys are backed up or escrowed.

**Sources.**
- EDPB Guidelines 02/2025 on processing of personal data through blockchain, v2.0, 2026, https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf (search)
- Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases, 2026, https://arxiv.org/abs/2606.18497 (fetched)
- Zero2Text: Zero-Training Cross-Domain Inversion Attacks on Textual Embeddings, 2026, https://arxiv.org/abs/2602.01757 (fetched)
- NIST SP 800-88 Rev. 2, Guidelines for Media Sanitization, 2025, https://csrc.nist.gov/pubs/sp/800/88/r2/final (search)

**Decisions affected.** ADRL-MEM-001, ADRL-MEM-005, ADRL-MEM-007, ADRL-MEM-010, ADRL-OPS-004, ADRL-SAF-003

**Proposed disposition.** Amend MEM-010 to store prompt-class ciphertext by reference in a deletable side store with only a pointer and skeleton in the ledger, and to forbid training or fine-tuning any model, including the local embedder, on ledger content without an unlearning procedure. Amend MEM-007 to require physical shredding of superseded projection files, enumerated in the erasure proof, and to exclude same-session later rows from as-of neighbours. Delete MEM-005's quantisation follow-up; if a noise layer is wanted at all, evaluate concept-aware mechanisms. Amend OPS-004 to put keystore backups under a sanitisation policy and to document the host key's read-only retention as a cryptographic-erase exception. Add a per-route hash chain to MEM-001 so immutability is verifiable rather than declared.

### 3.11 Failure attribution by inspection order is unreliable, and the taxonomy lacks grader and handoff faults

**Finding.** LLM-judge step attribution scores about 14 percent on Who&When; Causal Agent Replay argues the correct method is intervention and re-execution under the same stochastic policy with a Shapley split for interacting causes. The July 2026 interaction-centric taxonomy assigns 41 modes to component edges with grader and environment faults as a first-class category (kappa 0.76). Two 2026 causes have no type in the enum: a failure caused by the handoff itself and a failure caused by a corrupted-but-valid tool result; both would be typed task_capability today, the poisoning direction the decision guards against.

**Sources.**
- Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures, 2026, https://arxiv.org/abs/2606.08275 (fetched)
- Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?, 2026, https://arxiv.org/abs/2607.09996 (fetched)
- Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures, 2026, https://arxiv.org/abs/2607.28802 (fetched)
- When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents, 2026, https://arxiv.org/abs/2606.05806 (fetched)

**Decisions affected.** ADRL-MEM-004, ADRL-CAS-002, ADRL-MEM-003, ADRL-LRN-002

**Proposed disposition.** Amend MEM-004 and CAS-002 together into failure-types-v3: add grader_fault, handoff_induced and tool_output_corrupt above task_capability in precedence, allow a multi-label vector with per-type confidence, record a root-cause step index, and derive the cause by re-execution where the LRN-002 branch harness exists, recording which method produced the label. Amend MEM-003 with a test-adequacy field (mock density, assertion count, agent-authored in session) and N repeat runs before a suite's labels are tier-1. Amend LRN-002 to require k stochastic branches per arm so a bound counterfactual is a distribution.

### 3.12 Monotone pin inheritance is supported by attenuation work and qualified by recoverable IFC and aggregation inference

**Finding.** ChainCaps and Bounded Agents show monotone attenuation of authority down a delegation chain cuts attack success to near zero, which supports downward pin inheritance. Permissive IFC v3 and APPA show strict propagation over-blocks benign work and strands execution, and APPA sustains 64 to 91 percent utility with zero observed attacks using disposable child branches that absorb taint locally. Tallam's identity-governance work shows downward-only inheritance misses aggregation inference when a parent combines children's returns. Claude Code now defaults to 20 concurrent subagents at depth three with worktrees branched from the default branch.

**Sources.**
- ChainCaps: Composition-Safe Tool-Using Agents via Monotonic Capability Attenuation, 2026, https://arxiv.org/abs/2605.26542 (fetched)
- Bounded Agents: Delegation Security for Multi-Agent AI Systems, 2026, https://arxiv.org/abs/2608.15888 (fetched)
- APPA: Recoverable Information-Flow Control for Real-World LLM Agents, 2026, https://arxiv.org/abs/2607.24625 (fetched)
- Permissive Information-Flow Analysis for Large Language Models (v3), 2026, https://arxiv.org/abs/2410.03055 (fetched)
- Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure, 2026, https://arxiv.org/abs/2605.05440 (fetched)

**Decisions affected.** ADRL-SEM-006, ADRL-SAF-001, ADRL-SAF-002, ADRL-FND-004, ADRL-CAS-008

**Proposed disposition.** Keep downward inheritance as the safe default. Amend SEM-006 to record what a child actually received and to add an upward rule: a pinned child's return pins the parent lineage from that point. Add to SAF-001 and SAF-002 a follow-up to evaluate branch-scoped confinement for subagent lineages as a future relaxation, and reopen Q5 so a descendant lineage may be pinned without pinning the parent's future. Add to FND-004 a recovery clause for fail-closed pinned sessions (local-only compaction or an attended, audited, pin-preserving release), since abort-only enforcement is what the 2026 literature moves away from.

### 3.13 Three evaluation decisions certify on evidence that cannot carry the claim

**Finding.** EVL-001's best-single-model comparator is selected on the window it is evaluated on, which the selection-validity work shows invalidates paired inference. EVL-004 gates on label count when routing power comes from discordant pairs; 300 outcomes on which every rung agrees carry no routing information. EVL-007's D3 rung certifies a shadow router whose decisions are never executed, and its D4 has no concurrent control, duration or guardrail metrics, the before-and-after design SRE canarying warns against. Session-level bootstrap intervals below a few hundred sessions dramatically underestimate uncertainty.

**Sources.**
- Opportunity Is Not Realizability: Selection-Valid Diagnostics for Multi-LLM Routing, 2026, https://arxiv.org/abs/2608.08265 (fetched)
- Resolution Diagnostics for Paired LLM Evaluation, 2026, https://arxiv.org/abs/2605.30315 (fetched)
- Position: Don't Use the CLT in LLM Evals (ICML 2025), 2025, https://arxiv.org/abs/2503.01747 (fetched)
- Canarying Releases (Google SRE Workbook), 2018, https://sre.google/workbook/canarying-releases/ (fetched)
- Scrouting, 2026, https://arxiv.org/abs/2608.04804 (fetched)

**Decisions affected.** ADRL-EVL-001, ADRL-EVL-004, ADRL-EVL-007, ADRL-EVL-002, ADRL-EVL-006, ADRL-EVL-009

**Proposed disposition.** Amend EVL-001 to select the best-single-model comparator on the previous window or by pre-registration, to report selection-valid intervals otherwise, and to add a fifth comparator, always-local with mechanical escalation at the trip-wires. Amend EVL-004 with a fifth condition: a pre-registered minimum count of verified pairs on which rungs disagree, per slice. Rewrite EVL-007's D3 evidence as decision distribution, gate behaviour and plumbing on organic traffic plus branch studies, and D4 as a controlled pilot with a concurrent control, consistent assignment by lineage, guardrail metrics and a minimum duration. Add minimum cluster counts and resolution ratios to EVL-002 and EVL-006, and two blockers (version or serving-config change in window; synthetic figure without harness and benchmark versions) plus an unevaluable state to EVL-009.

### 3.14 An operator-run anchor is one witness, and long-lived KMS keys are the pre-2024 pattern

**Finding.** The transparency-log community's answer to a logger that might equivocate is independent witness cosigning; a single anchor inside the operator's trust domain cannot detect a split view, and Rekor v2 itself has not yet shipped witnessing. CloudTrail does not record what a KMS key signed, so 'signed by security's key' is not independently verifiable without a transparency log. The 2026 baseline for attestations is identity-bound keyless signing recorded in a witnessed log, and SLSA level 2 and above treat signed provenance as baseline. The checkpoint interval is the exposure window for an attacker who controls the host, and the decisions leave it unbounded.

**Sources.**
- Can I Get A Witness (Network)? (transparency.dev), 2025, https://blog.transparency.dev/can-i-get-a-witness-network (fetched)
- Rekor v2 GA (Sigstore blog), 2025, https://blog.sigstore.dev/rekor-v2-ga/ (fetched)
- Can Cloudtrail support KMS code signing transparency logs (AWS re:Post), 2025, https://repost.aws/questions/QUJlrDBq-CRYurHVCIUNxbjw/can-cloudtrail-support-kms-code-signing-transparency-logs-e-g-by-logging-signatures (search)
- Kettle: Attested builds for verifiable software provenance, 2026, https://arxiv.org/abs/2605.08363 (fetched)

**Decisions affected.** ADRL-TRU-003, ADRL-SAF-009, ADRL-OPS-007, ADRL-OPS-002, ADRL-LRN-005

**Proposed disposition.** Amend TRU-003 and OPS-007 to name the sink as a witnessed log (private Rekor v2 or Tessera) with at least one witness outside both the ADRL and gateway teams, adopt the C2SP checkpoint and cosignature format, pre-register the checkpoint interval as the maximum undetectable-tamper window, and prefer a hardware keystore for the checkpoint key. Amend OPS-002 to replace annual-rotation KMS keys for manifest and checkpoint signing with identity-bound keyless signing recorded in a private transparency log, keeping a KMS key only as the offline root. Amend LRN-005 to sign artifacts and manifests with OpenSSF Model Signing and to add a training-set membership commitment so erasure can identify affected artifacts.

## 4. Per-decision critique
All 77 decisions in register order. Text is taken from the five research files with headings normalised; no source was dropped and no verdict changed. Where a decision is shared by two slices the files agreed.

### FND: System Boundary and Principles

**State of the field, 2026.** The LLM gateway is now a commodity layer with a vendor-published contract. Anthropic ships a machine-readable protocol (`GET /protocol`), documents which headers must be forwarded byte-for-byte, states that a gateway must "inspect without modifying", and now ships its own self-hosted Claude apps gateway inside the `claude` binary, doing SSO, managed settings, telemetry and cross-provider failover "without developers noticing". Third-party gateways (LiteLLM, Portkey, now owned by Palo Alto Networks, Kong 3.14, Cloudflare's unified API) have moved semantic features into the gateway: guardrails with fail-closed defaults, NVIDIA-backed model routing, scope-based tool filtering. Fail-open remains the Kubernetes admission default while every 2025-2026 security guidance says fail closed for security-bearing checks. Routing economics research (Mahmood, Feb 2026) finds static per-task routing beats cascades in nearly all cases, and cache-aware, session-affine routing is the serving-layer consensus. Governance discipline has shifted to pre-committed if-then thresholds (frontier safety frameworks; DeepMind's Tracked Capability Levels, April 2026), while the EU deferred high-risk AI obligations to December 2027 because the conformity-assessment infrastructure was not ready.

#### ADRL-FND-001: Transparent control layer, protocol-scoped

Decision: ADRL is a protocol-transparent, removable layer between an Anthropic-Messages harness and the gateway; it changes the wire contract only through SAF-enumerated surfaces; Codex CLI is out of scope.

**FOR**
- The vendor contract is explicit and machine-readable: it separates "forward unchanged" (`anthropic-version`, `anthropic-beta`) from "consume" (`x-claude-code-*`), and a running gateway serves the same contract at `GET /protocol`, giving the removal test a mechanical oracle. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Anthropic's own Claude apps gateway is exactly the kind of layer FND-001 describes: clients "speak the Anthropic Messages API to the gateway, and the gateway translates for each upstream ... with failover between them. You can change regions, providers, or failover order without developers noticing or reconfiguring." The transparent-layer architecture is the vendor's own. [source: Anthropic, "Claude apps gateway", 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)]
- Codex CLI's Chat Completions support was deprecated in December 2025 and removed in early February 2026; every endpoint Codex talks to must speak Responses, so scoping Codex out of a Messages-shaped decision is the only honest position. [source: openai/codex, "Deprecating chat/completions support in Codex", Discussion #7782, 2025, https://github.com/openai/codex/discussions/7782 (search result)]

**AGAINST**
- The contract says "treat the headers and body fields as open lists" and "a gateway pinned to an observed list strips the next capability's header or field and breaks it on the release that introduces it." ADRL's clause 1 commits to an enumerated rewrite for non-Claude rungs (strip `thinking`, `cache_control`, beta tool fields); that list is by construction closed and will silently drift from the harness. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- The system-prompt attribution block adds a constraint FND-001 does not mention: the strip is positional and only works "when the gateway forwards the `system` array unchanged"; "any other upstream receives it as part of the prompt" and the prompt cache key. A local-rung rewrite that touches `system` changes cache identity on the frontier path too unless it is prefix-preserving. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Auto-mode permission classifier requests "skip the rest of Claude Code's system prompt, so on those requests the block is the only marker in the request body that identifies them as Claude Code traffic", and on a direct connection they keep the block even with `CLAUDE_CODE_ATTRIBUTION_HEADER=0`. A safety classifier request is a developer-invisible traffic class that ADRL neither enumerates nor may serve from a non-Claude rung. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- The 2026 routing-transparency literature argues the opposite of invisibility: relying parties need a "route receipt" recording "version aliases, service tiers, tool choices, regional endpoints, fallback rules, or safety handling" because "which model answered" is only part of the audit question. A layer whose design goal is that "the harness does not know a router exists" is in tension with that direction. [source: Schmalbach, "Model Routing as a Trust Problem: Route Receipts for Adaptive AI Systems", 2026, https://arxiv.org/abs/2605.01710 (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Keep. Amend clause 1 to make the non-Claude rewrite a deny-list against the machine-readable `/protocol` contract rather than a hand-enumerated field list, add the attribution-block and auto-mode classifier constraints to the enumerated surfaces, and state whether ADRL sits in front of or replaces a Claude apps gateway.

#### ADRL-FND-002: Semantic policy vs mechanical execution, deployment-set-closed

Decision: ADRL owns semantic policy; the gateway owns mechanical execution within the permitted deployment set computed per request; the signed deployment inventory is shared configuration.

**FOR**
- LiteLLM's three fallback classes (`fallbacks`, `content_policy_fallbacks`, `context_window_fallbacks`) are declared lists of model groups, so closure under a permitted set is a property of generated configuration and is checkable in CI, as the amendment requires. [source: LiteLLM, "Fallbacks (Provider Failover)", 2026, https://docs.litellm.ai/docs/proxy/reliability (search result)]
- The vendor's own gateway already does what FND-002 delegates: it "holds the upstream credential, enforces model access and managed settings by IdP group", and fails over between Bedrock, Claude Platform on AWS, Google Cloud, Foundry and the Anthropic API. Mechanical execution is a solved gateway concern. [source: Anthropic, "Claude apps gateway", 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)]
- Kong 3.14 implements attribute-based policy at the gateway ("an agent carrying a `flights:read` scope gets read-only tools", "token downscoping", "audience restriction"), showing that computed permitted sets keyed on attributes are the current gateway idiom, matching TRU-002's attribute-computed set. [source: Kong, "Govern the Full AI Data Path with Kong AI Gateway 3.14", 2026, https://konghq.com/blog/product-releases/kong-ai-gateway-3-14 (fetched)]
- Route receipts research treats "regional endpoints, fallback rules" as material facts to be recorded per request, endorsing CAS-006's served-deployment receipt as the detective backstop. [source: Schmalbach, "Model Routing as a Trust Problem", 2026, https://arxiv.org/abs/2605.01710 (fetched)]

**AGAINST**
- The vendor gateway's failover is region- and provider-crossing by design ("change regions, providers, or failover order without developers noticing") and the page documents no per-response deployment identifier. If the organisation's gateway is or wraps a Claude apps gateway, the deployment-set-closed contract has no vendor mechanism to bind to; it must be imposed on the gateway's `models` failover configuration by the generator. [source: Anthropic, "Claude apps gateway", 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)]
- Semantic routing is moving into the gateway: Kong applies NVIDIA NeMo Switchyard routing across model traffic, and Cloudflare's May 2026 unified API lets any model be called through one endpoint. "Semantic policy is ADRL's" is a boundary the gateway vendors are already crossing; Q1's non-delegable list is overdue. [source: Kong, "Intelligent Model Routing: Kong AI Gateway Applies NVIDIA NeMo Switchyard Across Model Traffic", 2026, https://konghq.com/blog/engineering/llm-routing-kong-ai-gateway-nvidia-nemo-switchyard (search result); Cloudflare, "AI Gateway Changelog", 2026, https://developers.cloudflare.com/changelog/product/ai-gateway/ (search result)]
- Gateway guardrails now default to fail-closed ("`fallback_on_error`: 'block' (fail-closed, default) or 'allow'", with authentication errors always blocking). Clause 3 says the gateway's control is "defence in depth" but does not say what happens when that control blocks or errors on a request ADRL already gated and pinned; two authorities still produce two answers on the failure path. [source: BerriAI/litellm PR #17785, "add configurable fail-open, timeout ... to panw_prisma_airs guardrail", merged 2025-12-11, https://github.com/BerriAI/litellm/pull/17785 (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Keep with the TRU-002 amendment. Add a clause that the gateway's multi-upstream failover order is itself generated from the deployment inventory, and extend clause 3 to define the outcome when a gateway guardrail fails closed on an ADRL-passed request.

#### ADRL-FND-003: Routing boundary is the user turn

Decision: Rung selection happens once per user turn per agent lineage; gates run on every request; pre-warm inherits; the only in-turn change is CAS escalation.

**FOR**
- Cache economics are stronger than when the decision was written: cache reads are 0.1x base input price, 0.025x for Fable 5.1 and Mythos 5.1, and "cache hits require 100% identical prompt segments"; caches are isolated per organisation and workspace. Every mid-turn switch forfeits that discount at the largest transcript size. [source: Anthropic, "Prompt caching", 2026, https://platform.claude.com/docs/en/build-with-claude/prompt-caching (fetched)]
- The serving-systems literature converges on session affinity: routing "which pins each program to the instance that served its first turn reaches a 96.26% hit rate", matching the single-instance ceiling. Turn-scoped stickiness is the same principle one layer up. [source: "AGENTSERVESIM: A Hardware-aware Simulator for Multi-Turn LLM Agent Serving", 2026, https://arxiv.org/pdf/2606.09613 (search result)]
- Routing theory: "in nearly all cases, the optimal routing policy involves a static policy with no cascading that depends on the expected utility of the models to the user." A single decision at the turn boundary is the static policy; per-request re-scoring is the cascade the paper finds suboptimal. [source: Mahmood, "Routing, Cascades, and User Choice for LLMs", 2026, https://arxiv.org/abs/2602.09902 (fetched)]

**AGAINST**
- Server-side compaction (beta `compact-2026-01-12`) now produces a `compaction` block after which "all content blocks before it are ignored" and "thinking blocks from before a compaction block aren't carried forward". The cache prefix is reset by the vendor's own mechanism, so the post-compaction request is the cheapest possible re-decision point and the decision's "only in-turn change is escalation" leaves that value on the table. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]
- Cache lifetime "is measured from the start of the request that writes or reads the cache entry ... if a response takes 4 minutes to stream, a follow-up request that reuses the same cached prefix must start within about 1 minute". Long tool loops on a slow rung can lose the cache inside a turn anyway, which weakens the cache argument for inheriting a slow local route and argues for ADRL preserving `ttl: "1h"` markers on the frontier path. [source: Anthropic, "Prompt caching", 2026, https://platform.claude.com/docs/en/build-with-claude/prompt-caching (fetched)]
- Mahmood also finds a "misalignment gap between the provider-optimal and user-preferred routes". Turn-level routing with no user-visible choice optimises the operator's cost; the decision has no user-utility term. [source: Mahmood, "Routing, Cascades, and User Choice for LLMs", 2026, https://arxiv.org/abs/2602.09902 (fetched)]
- Per-lineage boundaries now multiply: the default is 20 concurrent subagents and three levels of nesting, and forks "skip both filters and receive the main conversation's exact tool pool". "One decision per turn" is one per lineage per turn, potentially dozens per user instruction. [source: Anthropic, "Create custom subagents", 2026, https://code.claude.com/docs/en/sub-agents (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Keep. Amend to name the post-compaction request as a candidate re-decision point owned by SEM-005, and require the frontier-path rewrite to preserve `cache_control` TTL markers.

#### ADRL-FND-004: Fail to last-known-safe, not fail-open

Decision: Routing-path and gate-path failures fail open for unpinned sessions, fail closed for pinned ones; proxy death has only an audited operator bypass that cannot release a pin; fail-open events are rate-alerted.

**FOR**
- Gateway guardrail practice now defaults closed: the LiteLLM Prisma AIRS guardrail added "`fallback_on_error` config: 'block' (fail-closed, default) or 'allow' (fail-open)", with transient errors honouring the setting and 401/403 always blocking. The split by failure class is what production gateways implement. [source: BerriAI/litellm PR #17785, 2025, https://github.com/BerriAI/litellm/pull/17785 (fetched)]
- Kubernetes guidance for 2026: "configure critical security admission webhooks with failurePolicy: Fail (fail-closed) in production" and "consider fail-open policy for development environments". FND-004's pin-state split mirrors the criticality split. [source: OneUptime, "How to Configure Webhook FailurePolicy and TimeoutSeconds", 2026, https://oneuptime.com/blog/post/2026-02-09-webhook-failure-policy-timeout/view (search result)]
- Gatekeeper documents the same asymmetry ADRL adopts: it defaults to `failurePolicy: Ignore` yet publishes a "Failing Closed" guide for security-critical use, treating fail-open as the availability default and fail-closed as the opt-in for enforced policy. [source: Open Policy Agent, "Failing Closed | Gatekeeper", 2026, https://open-policy-agent.github.io/gatekeeper/website/docs/failing-closed/ (fetched)]

**AGAINST**
- Gatekeeper's warning applies directly: failing closed "is possible to put the cluster in a state where automatic self-healing is impossible" and "it can be hard to say for certain that all critical resources have been exempted because dependencies can be non-obvious". A pinned session whose scanner and local rung are both down cannot compact (compaction is content-bearing), so it cannot recover; FND-004 has no exemption list analogous to exempted namespaces. [source: Open Policy Agent, "Failing Closed | Gatekeeper", 2026, https://open-policy-agent.github.io/gatekeeper/website/docs/failing-closed/ (fetched)]
- The 2026 information-flow literature has moved against abort-only enforcement: conventional IFC "either over-blocks benign operations or permanently strands downstream execution once an agent ingests unvetted data", and APPA proposes "a policy-governed recovery system" instead. Fail-closed on pinned sessions is abort-only; the register offers no recovery primitive short of operator bypass. [source: Kravchenko et al., "APPA: Recoverable Information-Flow Control for Real-World LLM Agents", 2026, https://arxiv.org/abs/2607.24625 (fetched)]
- The vendor's answer to proxy-path death is not an in-process fallback but a highly available gateway with server-side state ("stores auth state in PostgreSQL", sessions "refresh silently before `ttl_hours` expiry"). Clause 3's "operator repoints `ANTHROPIC_BASE_URL`" is a manual runbook where the field expects supervised HA; this is an OPS gap the decision should reference rather than own. [source: Anthropic, "Claude apps gateway", 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Keep the replacement. Add a recovery clause for fail-closed pinned sessions (a local-only compaction path or an attended, audited, pin-preserving release), modelled on Gatekeeper's exemption guidance and APPA's recovery framing.

#### ADRL-FND-005: Scope expands only through measured gates

Decision: Scope expands only through measured phase gates; component presence is not readiness.

**FOR**
- Pre-committed gates are now the norm in AI deployment governance: frontier safety frameworks are "if-then commitments" with "predefined levels of dangerous capabilities that, if crossed, trigger heightened protections", at least 12 companies have published one, and DeepMind added Tracked Capability Levels in April 2026. [source: METR, "Common Elements of Frontier AI Safety Policies", 2025, https://metr.org/common-elements (search result); Google DeepMind, "Google DeepMind strengthens the Frontier Safety Framework", 2026, https://deepmind.google/blog/strengthening-our-frontier-safety-framework/ (search result)]
- The EU deferred Annex III high-risk obligations from 2 August 2026 to 2 December 2027 because "neither industry nor the harmonized standards bodies ... would be ready in time, and ... the conformity-assessment infrastructure the Act assumes had not yet matured": a regulator applying "component presence is not readiness" to itself. [source: Cloud Security Alliance, "EU AI Act's High-Risk Deadline: Deferred, Not Cancelled", 2026, https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/ (fetched)]
- Progressive-delivery practice in 2026 defines guardrail and goal metrics "upfront" with "defined pass or fail thresholds and absolute conditions that trigger rollback", and error-budget consumption gates promotion. [source: DesignGurus, "How do you do progressive delivery (flags + canaries) safely?", 2026, https://www.designgurus.io/answers/detail/how-do-you-do-progressive-delivery-flags-canaries-safely (search result)]

**AGAINST**
- The frontier frameworks that supply the analogy share the weakness the 2026-09-02 review found: they are self-assessed. The search results "don't specifically detail independent assessor requirements"; METR's common-elements list is about what companies commit to, not who checks. FND-005's gates remain self-graded and the field offers no stronger template. [source: METR, "Common Elements of Frontier AI Safety Policies", 2025, https://metr.org/common-elements (search result)]
- Static-benchmark gates are exactly the methodology the adaptive-evaluation literature discredits: out-of-band defenses are "validated only on static benchmarks (a fixed set of injection attempts), the same methodology that made in-band defenses look strong until adaptive, defense-aware attacks broke twelve of them at over 90% success". ADRL's canary fixtures are static; "tested, not attacked" is the register's own phrase. [source: Narisetty et al., "Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents", 2026, https://arxiv.org/abs/2606.26479 (fetched)]
- Measured on what? Mahmood's misalignment gap means a cost gate can pass while user utility falls; nothing in FND-005 requires a user-utility SLI at any gate. [source: Mahmood, "Routing, Cascades, and User Choice for LLMs", 2026, https://arxiv.org/abs/2602.09902 (fetched)]
- Multi-agent failure taxonomy work attributes a large share of failures to "task verification" and "specification" gaps rather than component absence; a gate that measures runtime metrics but not specification conformance passes systems that fail for the dominant reasons. [source: Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", 2025, https://arxiv.org/abs/2503.13657 (fetched)]

**Grounding verdict**: CURRENT by analogy (newest source 2026); there is still no direct literature on pre-registering engineering readiness thresholds.

**Recommendation**: Keep the sentence. Add to the EVL follow-ups a requirement that every gate include at least one adversarial (adaptive) test and one user-utility SLI, and name an approver outside the team, since the 2026 analogues are only as strong as their assessor.


### SEM: Interaction Semantics

**State of the field, 2026.** Session and agent identity are now on the wire: Anthropic documents `x-claude-code-session-id`, per-spawn `x-claude-code-agent-id`, `x-claude-code-parent-agent-id`, and stable name-based teammate IDs; MCP added `Mcp-Session-Id` in 2025 but its 2026-07-28 release candidate reportedly removes sessions to make requests stateless. Compaction moved server-side on both major APIs: Anthropic's `compaction` block (beta `compact-2026-01-12`) and OpenAI's opaque, encrypted compaction item. Codex CLI speaks only the Responses API since February 2026. Subagents scale to 20 concurrent and three levels by default, with worktree isolation. Information-flow control for agents split into two camps: monotone attenuation (ChainCaps, Bounded Agents, FIDES at SaTML 2026) and permissive or recoverable propagation (permissive IFC v3, APPA), with an adaptive-evaluation critique of both. Dialogue segmentation research (When F1 Fails, CobSeg) now targets LLM context management directly but warns that strict boundary metrics mislead.

#### ADRL-SEM-001: Mechanical classification of request classes

Decision: Requests are classified from shape and wire headers into six classes; every class is gated; passthrough fail-safe applies only to unpinned sessions.

**FOR**
- Every signal the decision names is documented: the session header exists "to aggregate all requests from one session without parsing request bodies"; the agent header is "present only on requests from an agent Claude Code spawned inside the session"; inference posts to `/v1/messages?beta=true` "so match on the path, not the full URL"; `count_tokens` is optional with fallback through inference. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Startup traffic is enumerated (`HEAD /api/hello` warming probe, `GET /v1/models?limit=1000` discovery with a 3-second timeout), so the passthrough class has a documented membership. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Codex removed Chat Completions in February 2026, so the Responses format is structurally distinct and the scope exclusion holds. [source: Daniel Vaughan, "Codex CLI Custom Model Providers: The Complete Configuration Guide", 2026, https://codex.danielvaughan.com/2026/04/23/codex-cli-custom-model-providers-configuration-guide/ (search result)]

**AGAINST**
- A seventh class exists: auto-mode permission classifier requests, which "skip the rest of Claude Code's system prompt" and are identifiable only by the attribution block. They carry the command or action under evaluation, are neither cosmetic nor a user turn, and must never be answered by a model other than the one the harness expects. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Server-side compaction changes request shape: a `compaction` block may appear in `messages` and "all content blocks before it are ignored". The classifier must recognise compaction-bearing requests and the `compact-2026-01-12` beta header, or its continuation heuristics (final-message role, transcript length) misfire after the first compaction. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]
- Teammate agents "reuse a stable name-based ID across reconnections" and workflow agents exist; a subagent class defined by fresh-per-spawn IDs misclassifies teams. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- The contract is an open list: "Claude Code gains capabilities over releases, and they arrive as new `anthropic-beta` values, new request body fields, and occasionally new ... `x-claude-code-*` headers." A shape classifier is versioned against a moving target and must be re-validated per Claude Code release. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Keep. Amend to add the auto-mode classifier request as a class that is always passthrough to the requested model, handle compaction-bearing requests explicitly, and record the Claude Code version range each discriminator version was validated against.

#### ADRL-SEM-002: Session key from wire headers, then metadata

Decision: Session key from `x-claude-code-session-id`, then `metadata.user_id`, then a per-connection fallback; composed with agent lineage; stored as a keyed hash.

**FOR**
- The header is documented as "a unique identifier for the current Claude Code session", and the vendor states the agent header "identifies an agent, not a person or a device, so don't treat the agent ID header as a user identifier", matching the session/lineage composition and the privacy posture. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Agent frameworks use the same two-level split: in LangGraph "thread-id scopes a single session, while user-id scopes across sessions"; the OpenAI Agents SDK's sessions are client-side memory keyed by session id. Sub-clause 2's treatment of `metadata.user_id` as possibly user-level matches the frameworks. [source: LangChain, "Short-term memory", 2026, https://docs.langchain.com/oss/python/langchain/short-term-memory (search result); OpenAI, "Sessions - OpenAI Agents SDK", 2026, https://openai.github.io/openai-agents-python/sessions/ (search result)]
- Protocol-level session identity is standard practice: MCP's Streamable HTTP transport assigns an `Mcp-Session-Id` at initialisation that clients "must include ... on all of their subsequent HTTP requests", and it "should be globally unique and cryptographically secure". [source: Model Context Protocol, "Transports" (2025-03-26 spec), https://modelcontextprotocol.io/specification/2025-03-26/basic/transports (search result)]

**AGAINST**
- The session header is client-generated and unauthenticated. The agent-identity literature's starting point is that "neither protocol verifies agent identity" and proposes invocation-bound tokens; keying pins and sticky state on a value the client can set to anything is the same class of problem TRU-001 corrects for repository identity. [source: Prakash, "AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A", 2026, https://arxiv.org/abs/2603.24775 (fetched)]
- An authenticated key now exists above the header: a Claude apps gateway binds each session to an IdP identity, refreshes it before `ttl_hours` expiry, and stamps telemetry "with user identity". SEM-002's preference order has no tier for an authenticated gateway session token, which is stronger than any header. [source: Anthropic, "Claude apps gateway", 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)]
- The protocol trend is away from sticky sessions: the MCP 2026-07-28 release candidate reportedly "removes the handshake and session ID entirely, making every request self-contained and routable to any server instance without sticky sessions". Durable session-keyed state at the proxy runs against where transports are heading. [source: sergiobayona/vector_mcp, "streamable-http-spec-compliance.md", 2026, https://github.com/sergiobayona/vector_mcp/blob/main/docs/streamable-http-spec-compliance.md (search result)]

**Grounding verdict**: CONTESTED (newest source 2026): header-based session identity is documented and standard, but 2026 identity work treats unauthenticated IDs as insufficient for security state and one major protocol is removing sessions.

**Recommendation**: Keep the derivation order. Amend to add an authenticated tier (gateway session token or IdP subject) above the header when present, and state explicitly that an unauthenticated session key may attach a pin but never release or narrow one.

#### ADRL-SEM-003: Continuations inherit the sticky route

Decision: Continuations inherit the sticky route and do not trigger a fresh difficulty decision.

**FOR**
- Cache reads at 0.1x (0.025x on Fable 5.1 and Mythos 5.1) with "100% identical prompt segments" required make inheriting the route the dominant economic choice for every continuation. [source: Anthropic, "Prompt caching", 2026, https://platform.claude.com/docs/en/build-with-claude/prompt-caching (fetched)]
- Session-affine routing is the serving consensus: pinning later turns to the instance that served the first turn "reaches a 96.26% hit rate", and cache-aware routers now offer "explicit model affinity for applications that already manage sessions". [source: "AGENTSERVESIM", 2026, https://arxiv.org/pdf/2606.09613 (search result); DigitalOcean, "DigitalOcean Inference Router, Now Cache-Aware", 2026, https://www.digitalocean.com/blog/inference-router-cache-aware (search result)]
- Static routing without cascading is optimal "in nearly all cases" under the user-utility model; re-scoring each continuation is a cascade. [source: Mahmood, "Routing, Cascades, and User Choice for LLMs", 2026, https://arxiv.org/abs/2602.09902 (fetched)]

**AGAINST**
- Cache lifetime is counted from request start, so a slow local rung can outlive its own cache inside a turn ("a follow-up request ... must start within about 1 minute of that response completing" after a 4-minute stream); the cache argument for inheritance weakens on exactly the rung ADRL wants to keep. [source: Anthropic, "Prompt caching", 2026, https://platform.claude.com/docs/en/build-with-claude/prompt-caching (fetched)]
- Within-turn model changes at the proxy layer are now a research direction: RLM-Cascade applies "speculative decoding at the response level" where "a fast, inexpensive draft model generates a candidate response and a capable verify model accepts, enhances, or is bypassed". Inheritance is a policy choice, not a technical necessity, and the register should say so. [source: "RLM-Cascade: Response-Level Speculative Decoding for Cost-Efficient LLM API Serving", 2026, https://arxiv.org/html/2606.22840 (search result)]
- A continuation inherited onto a rung that rejects `thinking` or a signature causes Claude Code to "disable the rejected capability for the rest of the conversation"; inheritance without a per-request capability check has conversation-wide cost. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Keep and raise to D3 as the 2026-09-02 review recommended. Add a rationale note that inheritance is an economic policy which response-level cascades could later relax at an action boundary.

#### ADRL-SEM-004: Utility calls split by content exposure

Decision: Cosmetic utility calls may go local; context-bearing ones (compaction) inherit the session's rung and gate state; on pinned sessions every utility call is local or empty.

**FOR**
- The vendor confirms the quality stake: after compaction "the summary is all the model has of that earlier work", and thinking blocks before it are dropped. A weak summary is a hidden, session-long regression. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]
- On the OpenAI side the compaction item is "opaque and not intended to be human-interpretable" and encrypted; a local model cannot produce or consume it, so context-bearing utility work is provider-bound by construction. [source: OpenAI, "Compaction", 2026, https://developers.openai.com/api/docs/guides/compaction (fetched)]
- Community traces confirm harnesses (Claude Code, Codex CLI, OpenCode, Amp) still issue client-side compaction prompts with distinct shapes, so shape fingerprinting remains feasible for the client-side path. [source: badlogic, "Context Compaction Research: Claude Code, Codex CLI, OpenCode, Amp", 2026, https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f (search result)]

**AGAINST**
- Compaction is becoming a block inside the inference response rather than a separate request: the API "detects when input tokens reach your specified trigger threshold, generates a summary of the current conversation, creates a `compaction` block", and supports Bedrock, Google Cloud and Foundry in beta. Once Claude Code adopts it, there is no "compaction request" to classify; the serving deployment writes the summary, and a local rung would produce none. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]
- A third kind of utility call exists that the split cannot place: auto-mode permission classifier requests, which are safety-bearing (they decide whether an action is allowed), carry action content, and on a direct connection go to `api.anthropic.com`. Serving them from a small local model changes a safety verdict, not a title. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Server-side compaction "works well with prompt caching" only if the compaction block gets its own `cache_control` breakpoint; ADRL's rewrite path must preserve that marker or the compacted prefix is re-billed every turn. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]

**Grounding verdict**: DATED (newest source 2026): the decision rests on the client-side compaction model that server-side compaction on both major APIs now qualifies.

**Recommendation**: Amend to define behaviour for both compaction modes (client-side request and server-side `compaction` block, including the pinned-session rule when the block would be written by a cloud deployment), and add "safety classifier requests" as a class that always goes to the harness-requested model. Keep the cosmetic-local rule.

#### ADRL-SEM-005: Episode boundaries, enumerated and measured

Decision: Boundaries come from an enumerated signal list, release escalation hysteresis only, and are logged so false-boundary and release rates are measurable.

**FOR**
- The segmentation field now targets exactly ADRL's use: "modern LLM-based conversational systems increasingly rely on segmentation to manage conversation history beyond fixed context windows", and it warns that strict boundary metrics mislead, which supports logging candidates and measuring with tolerant metrics rather than trusting a detector. [source: Coen, "When F1 Fails: Granularity-Aware Evaluation for Dialogue Topic Segmentation", 2025, https://arxiv.org/abs/2512.17083 (fetched)]
- Trainable segmenters in 2026 still report Pk and WindowDiff and reach Pk of 1.0 on DialSeg711 while the harder sets remain far from solved; a conservative conjunction of signals is the right posture for coding transcripts. [source: "CobSeg: Coherence Boundary Modeling for Dialogue Topic Segmentation", 2026, https://arxiv.org/abs/2605.30668 (search result)]
- The vendor's compaction semantics ("all content blocks before it are ignored") describe a memory replacement, not a task change, which is the reason the decision excludes compaction as a boundary. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]

**AGAINST**
- "Reported performance differences often reflect annotation granularity mismatch rather than boundary placement quality alone." ADRL's false-boundary rate (a trip-wire within N turns) is a proxy label with its own granularity; pre-registering a threshold on a proxy can be pre-registering noise. [source: Coen, "When F1 Fails", 2025, https://arxiv.org/abs/2512.17083 (fetched)]
- Post-compaction is now the cheapest re-decision point (prefix reset by the vendor, and the summary can be steered: "if you write your own `instructions`, tell the model what the summary must retain"). Excluding compaction "alone" is right for stickiness but the decision should evaluate "compaction plus a confirming signal" as a candidate rather than exclude it. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]
- The harness topic-detection call is an undocumented internal behaviour in an open-list contract; the vendor's own documented signals (session header, compaction block) are versioned, the `isNewTopic` call is not. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]

**Grounding verdict**: CURRENT for the measurement contract (newest source 2026); the specific signal list remains first-principles.

**Recommendation**: Keep. Amend sub-clause 3 to use window-tolerant metrics alongside the two rates, and add "post-compaction first turn with a confirming signal" to the evaluated candidate list rather than the exclusion list.

#### ADRL-SEM-006: Subagents inherit constraints now, routing later

Decision: Subagents inherit the parent's pin and gate state via wire lineage, keep the harness's model choice, and are logged under their own route_id; routing for subagents stays D0.

**FOR**
- Monotonic attenuation is the 2026 result: "a value can preserve or lose authority as it moves through a tool chain, but it cannot gain new authority through composition", cutting attack success from 25-68% to 0-4.8% at 96-100% benign completion. Pin inheritance down a lineage is this principle applied to confidentiality. [source: Jiang et al., "ChainCaps: Composition-Safe Tool-Using Agents via Monotonic Capability Attenuation", 2026, https://arxiv.org/abs/2605.26542 (fetched)]
- Bounded Agents' Agentic Principal Chain "carries forward and restricts delegated scope and budgets" across principals; the decision's ancestor-union rule is a special case. [source: Muruaga, "Bounded Agents: Delegation Security for Multi-Agent AI Systems", 2026, https://arxiv.org/abs/2608.15888 (fetched)]
- Identity governance work names "transitive delegation" as a first-class problem to be "enforced at every interaction boundary, and designed into the system before orchestration logic is allowed to scale", which is the order SEM-006 imposes (constraints first, routing later). [source: Tallam, "Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure", 2026, https://arxiv.org/abs/2605.05440 (fetched)]
- The wire supplies the lineage: `x-claude-code-agent-id` on every spawned agent and `x-claude-code-parent-agent-id` for nested agents. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]

**AGAINST**
- The permissive camp argues monotone propagation over-blocks: propagating "only the labels of the samples that were influential in generating the model output" beats the conservative join "in more than 85% of the cases", and APPA finds monotone taint "either over-blocks benign operations or permanently strands downstream execution". A parent pin that pins every descendant forever, regardless of what the child actually receives, is the coarse policy this work qualifies. [source: Siddiqui et al., "Permissive Information-Flow Analysis for Large Language Models", v3 2026, https://arxiv.org/abs/2410.03055 (fetched); Kravchenko et al., "APPA", 2026, https://arxiv.org/abs/2607.24625 (fetched)]
- Downward-only inheritance misses "aggregation inference": authorization implications arise "when combining results". A child pinning "does not pin the parent", yet the parent synthesises children's returns; SAF-003 content scanning catches literal secrets in returned tool results but not restricted-by-combination content. [source: Tallam, "Authorization Propagation in Multi-Agent AI Systems", 2026, https://arxiv.org/abs/2605.05440 (fetched)]
- Scale and identity assumptions have moved: 20 concurrent subagents and three nesting levels by default, worktree isolation "branched by default from your default branch rather than the parent session's HEAD" (a different checkout, which bears on TRU-001 corroboration), and teammates with stable names where "SendMessage checks that a name still refers to the same agent". A single-process dict and per-spawn IDs are two generations behind. [source: Anthropic, "Create custom subagents", 2026, https://code.claude.com/docs/en/sub-agents (fetched)]
- Every out-of-band defense that reports near-elimination on AgentDojo "is validated only on static benchmarks", and adaptive attacks broke twelve in-band defenses "at over 90% success". SEM-006's inheritance rules have only golden tests planned. [source: Narisetty et al., "Adaptive Evaluation of Out-of-Band Defenses", 2026, https://arxiv.org/abs/2606.26479 (fetched)]

**Grounding verdict**: CONTESTED (newest source 2026): monotone inheritance is supported by ChainCaps and Bounded Agents and qualified by permissive and recoverable IFC and by aggregation inference.

**Recommendation**: Keep downward pin inheritance as the safe default. Amend clause 1 to record what a child actually received (delegation text, CLAUDE.md, fork transcript) so a future permissive rule has evidence, and add an upward rule: a pinned child's return pins the parent lineage from that point.

#### ADRL-SEM-007: Protocol profiles (Proposed)

Decision: Every accepted wire format is a versioned profile; `anthropic-messages-v1` is the only one; a Responses profile has enumerated prerequisites; cross-profile handoff is forbidden until both reach D2.

**FOR**
- The Responses state model is fundamentally different: with `previous_response_id` "all previous input tokens for responses in the chain are billed as input tokens", response objects "are saved for 30 days by default", and Conversation objects "are not subject to the 30 day TTL". None of SEM-001's shape heuristics apply to a request that carries only the new message. [source: OpenAI, "Conversation state", 2026, https://developers.openai.com/api/docs/guides/conversation-state (fetched)]
- The compaction item is "opaque and not intended to be human-interpretable" and "fully stateless and ZDR-friendly"; a content-bearing flag cannot be computed on it, which is why clause 3 requires a state decision before admission. [source: OpenAI, "Compaction", 2026, https://developers.openai.com/api/docs/guides/compaction (fetched)]
- The vendor's own protocol page is organised as a table of formats (Anthropic Messages, Bedrock InvokeModel, Google rawPredict) each with its own "forward unchanged" rule, and a machine-readable `/protocol`. Profiles mirror the vendor's structure. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- Codex users are already served by translating gateways: "for providers that only expose Chat Completions, put a translating gateway (LiteLLM, or a router ...) between Codex and the provider". An adapter per profile is current practice. [source: OpenRouter, "Codex CLI with OpenRouter: config.toml Setup and Models", 2026, https://openrouter.ai/blog/tutorials/codex-cli-openrouter/ (search result)]

**AGAINST**
- Profile v1 is already incomplete for Claude Code itself: with `CLAUDE_CODE_USE_BEDROCK=1` the client sends `anthropic_beta` and `anthropic_version` as body fields not headers, Bedrock streams "application/vnd.amazon.eventstream" that must not be converted to SSE, and the 300-second byte watchdog does not apply. A Claude Code fleet on Bedrock format is not `anthropic-messages-v1`. [source: Anthropic, "Gateway protocol reference", 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)]
- The prerequisite in clause 3 may be unmeetable rather than merely unmet: gating a Responses lineage requires either forbidding stored state (forcing `store=false` and full replay of every output item, which the client controls) or resolving server-side state ADRL cannot read. The profile may have to be admitted as passthrough-only with an egress marker, permanently. [source: OpenAI, "Conversation state", 2026, https://developers.openai.com/api/docs/guides/conversation-state (fetched)]
- Anthropic's server-side compaction block is provider-bound in the same way as OpenAI's item (beta on Claude API, Bedrock, Google Cloud, Foundry), so clause 4's cross-profile handoff ban also needs an intra-profile, cross-deployment rule for compacted transcripts. [source: Anthropic, "Compaction", 2026, https://platform.claude.com/docs/en/build-with-claude/compaction (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Accept at D0. Amend to define `anthropic-messages-v1` as covering only `ANTHROPIC_BASE_URL` traffic and to list the Bedrock and Vertex client formats as variants or separate profiles before the register claims v1 covers Claude Code.


### SAF: Safety, Privacy, Hard Constraints

**State of the field, 2026.** Three things changed since the register's sources were chosen. First, secret detection moved from regex-and-entropy to hybrid regex-plus-LLM classification: MSR 2026 reports 94.49% F1 with fine-tuned open models, and GitHub now ships AI generic-secret detection with a `secret_category` field separating provider patterns from generic and AI-detected ones. Second, the coding-agent threat model became empirical rather than theoretical: Claude Code, Cursor and Codex each shipped sandbox escapes and injection CVEs in 2025 and 2026, Anthropic's own guidance now says to use a dedicated VM for untrusted repositories, and Apple still lists `sandbox-exec` as deprecated with no removal date. Third, information-flow control for agents matured past strict taint: FIDES (2025), APPA and NeuroTaint (2026) show recoverable, branch-scoped labels with 64 to 91% utility and zero observed attacks, while PIIBench (2026) shows every open PII detector below 0.14 F1 across domains. The register's ordering and pin principles hold; several mechanisms are a generation behind.

#### ADRL-SAF-001: Hard gates first, on every request

Decision: hard gates run on every request class before any optimisation, cannot be overridden by heuristics, learned policy or the failure fallback, and outcomes only tighten within a lineage.

**FOR**
- The newest agent-security work agrees that safety must be enforced deterministically before an action, not by the model: CaMeL's interpreter "enforces security policies before each tool call" and the MCP maintainers advise to "keep your actual safety guarantees in deterministic controls" because annotations "don't make the model resist prompt injection" [source: Tool Annotations as Risk Vocabulary, MCP blog, 2026, https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/ (fetched); Defeating Prompt Injections by Design, 2025, https://arxiv.org/pdf/2503.18813 (search title)].
- Per-request gating on tool results is now backed by attack evidence: QueryIPI turns tool descriptions into optimised payloads with up to 87% success that "transfer to real-world coding agents", and the Agent Data Injection paper shows Claude Code, Codex and Gemini CLI "do not isolate trusted data from untrusted data" [source: QueryIPI, 2026, https://arxiv.org/abs/2510.23675 (search title); Agent Data Injection Attacks are Realistic Threats to AI Agents, 2026, https://arxiv.org/html/2607.05120v1 (fetched)].
- The "gate outcomes only tighten" rule is the classical high-water-mark and is what FIDES enforces: confidentiality labels "tracked dynamically through agent steps and enforced deterministically" [source: Securing AI Agents with Information-Flow Control, 2025, https://arxiv.org/abs/2505.23643 (search title)].

**AGAINST**
- Strict monotone tainting is the design the 2026 IFC literature explicitly moves away from. APPA states traditional IFC "permanently strands downstream execution once an agent ingests unvetted data" and replaces it with "disposable child branches [that] absorb taint locally", sustaining "64.2-91% utility with zero observed attacks across 1,320 guarded episodes"; SAF-001 sub-clause 2 forbids exactly that recovery for every automated actor [source: Agentic Permissions Policy Algebra for Taint Confinement in LLM Agents, 2026, https://arxiv.org/abs/2607.24625 (fetched)].
- "New content of every request" assumes taint is carried by explicit content. NeuroTaint argues propagation "must be understood not only as explicit content transfer, but also as semantic transformation, causal influence on decisions, and cross-session persistence through memory"; a compaction summary that paraphrases a secret is scanned as new content but may no longer match any detector [source: Ghost in the Agent: Redefining Information Flow Tracking for LLM Agents, 2026, https://arxiv.org/abs/2604.23374 (fetched)].
- The gate reads metadata the harness reports (cwd, headers, working-directory) and the ADI paper's core finding is that attackers inject "security-critical metadata (e.g., resource identifiers or data origins)" and that ADI "easily bypasses existing IPI defenses" [source: Agent Data Injection Attacks, 2026, https://arxiv.org/html/2607.05120v1 (fetched)].
- Gate latency compounds with harness retry policy: Claude Code retries transient failures "up to 10 times with exponential backoff", so a slow or erroring gate on a continuation is multiplied, not merely added [source: Claude Code errors reference, 2026, https://code.claude.com/docs/en/errors (fetched)].

**Grounding verdict**: CURRENT (newest source 2026), with the monotonicity clause contested by APPA.

**Recommendation**: Keep ordering and per-request scope as written; they are the consensus of 2025 to 2026 agent-security work. Add a follow-up to evaluate branch-scoped (APPA-style) confinement for subagent lineages as a future relaxation of sub-clause 2, and add a semantic-carrier test (secret paraphrased in a compaction summary) to the adversarial suite.

#### ADRL-SAF-002: One-way pin, durable, lineage-scoped, audited release

Decision: pins are one-way per lineage, durable across restarts, cover every content-bearing class, and release only by an audited, reason-coded human action.

**FOR**
- The audited human release now has a stronger precedent than the register cites: GitHub's delegated bypass lets organisations "designate reviewers for bypass requests", requests "expire after 7 days", and since September 2025 reviewers are set at enterprise level with comments "added to the review request timeline and the secret scanning alert timeline" [source: Delegated bypass for push protection, GitHub Docs, https://docs.github.com/en/enterprise-cloud@latest/code-security/concepts/secret-security/about-delegated-bypass-for-push-protection (search title); Delegated bypass controls now available at the enterprise level, GitHub Changelog, 2025, https://github.blog/changelog/2025-09-16-delegated-bypass-controls-for-push-protection-now-available-at-the-enterprise-level/ (search title)].
- Lineage scope, including descendants and memory, is supported by NeuroTaint's finding that taint persists "cross-session ... through memory" and by the register's own MEM embeddings [source: Ghost in the Agent, 2026, https://arxiv.org/abs/2604.23374 (fetched)].
- The base rate justifies a pin-first posture: GitGuardian measured AI-assisted commits leaking secrets at "roughly 2x the baseline", with Claude Code-assisted commits peaking at "31 secrets per 1,000 commits" [source: The State of Secrets Sprawl 2026, GitGuardian, https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/ (search title)].

**AGAINST**
- Recoverable IFC is now demonstrated, not hypothetical. APPA's "prospective acquisition enforcement" evaluates "label descents and missing prerequisites before data acquisition occurs", so the register's claim that session scope is "forced" by the transcript model is weaker than in 2024; a subagent branch can be pinned without pinning its parent's future [source: APPA, 2026, https://arxiv.org/abs/2607.24625 (fetched)].
- The industry precedent the decision leans on has automatic dampening the decision forbids: Copilot generic secret detection stops alerting on a file after five false-positive marks and "may not detect secrets in test code", skipping paths containing "test", "mock" or "spec" [source: Responsible detection of generic secrets with Copilot secret scanning, GitHub Docs, https://docs.github.com/en/code-security/responsible-use/responsible-ai-generic-secrets (fetched)].
- Durability via a local ledger is only as strong as the host. The Claude Code CVE chain (CVE-2026-35020 to 35022) "writes a malicious .claude/settings.json" and later reads "~/.aws/credentials, ~/.ssh/id_rsa, the process environment", so pin state in a developer-writable file is attacker-writable under the same threat model [source: Three CVEs in Claude Code CLI, Phoenix Security, 2026, https://phoenix.security/claude-code-leak-to-vulnerability-three-cves-in-claude-code-cli-and-the-chain-that-connects-them/ (fetched)].
- Generic secrets "can't be validated" and prioritising only validated secrets "creates blind spots (46% missed)", so a reason-coded release on `false_positive` will be exercised often, and every release is an audit event a small team must review [source: The State of Secrets Sprawl 2026, GitGuardian (search title)].

**Grounding verdict**: CONTESTED (newest source 2026).

**Recommendation**: Keep one-way for the human-facing path and the delegated-reviewer model, which is now enterprise practice. Reopen Q5 in light of APPA: specify that a descendant subagent lineage may be pinned without pinning the parent's future requests, and require the pin store to be under the same integrity control as the egress ledger (SAF-009), not a plain file.

#### ADRL-SAF-003: Secret detection per request, precision-measured

Decision: scan the new content of every request with a detector set tiered by measured precision; suppress embeddings, hashes and locating features retroactively for pinned lineages.

**FOR**
- Tiering by category is now how the largest deployment works: GitHub's July 2026 webhook adds `secret_category` distinguishing "default: provider patterns plus your custom patterns" from "generic: generic patterns and AI-detected secrets", and push protection blocks only the default tier by default [source: Improvements to secret scanning and public monitoring, GitHub Changelog, 2026, https://github.blog/changelog/2026-07-15-improvements-to-secret-scanning-and-public-monitoring/ (fetched)].
- The precision problem the decision names has a measured 2026 answer: a regex-plus-LLM pipeline reaches "up to 94.49% F1" with Qwen and LLaMA, versus regex "high recall but poor precision", validated at 81.6% F1 on 178 real repositories [source: Secret Leak Detection in Software Issue Reports using LLMs, MSR 2026, https://arxiv.org/abs/2410.23657 (fetched)].
- Retroactive suppression is justified beyond Vec2Text: soft-deleted vectors "remain physically recoverable by accessing the raw index files" in three HNSW implementations, with 100% recovery of patient demographics [source: Ghost Vectors, 2026, https://arxiv.org/pdf/2606.18497 (fetched)].

**AGAINST**
- The decision tiers regex and entropy detectors; the field's 2025 to 2026 answer is contextual LLM classification, with a fine-tuned LLaMA-3.1 8B reaching "an F1-score of 0.9852" on 818 repositories and the authors concluding that "traditional regex and entropy-based tools often generate high false positives due to limited contextual understanding". A local 8B classifier is an unmentioned, feasible tier on the local rung [source: Secret Breach Detection in Source Code with Large Language Models, 2025, https://arxiv.org/abs/2504.18784 (fetched)].
- "Representative the company traffic" is dominated by code files, which the most mature AI generic detector declines to scan: GitHub skips ".cs, .go, .java, .js, .kt, .php, .py, .rb, .scala, .swift, .ts" and test paths for AI detection [source: Responsible detection of generic secrets, GitHub Docs (fetched)]. A published precision figure on such traffic will be lower than any vendor number.
- The only cross-tool precision study the register cites is 2023; no 2025 or 2026 tool comparison surfaced in search, so the "25 to 75%" figures are dated even if directionally right [source: A Comparative Study of Software Secrets Reporting by Secret Detection Tools, 2023, https://arxiv.org/abs/2307.00714 (search title)].
- Retroactive deletion from a NumPy index or SQLite is a soft delete unless the storage is rewritten; Ghost Vectors' mitigation is "Epoch Key Rotation" that "encrypts vectors and discards the key upon deletion" with signed proof, which sub-clause 3 does not require [source: Ghost Vectors, 2026 (fetched)].

**Grounding verdict**: DATED (principle current, mechanism a generation behind; newest source 2026).

**Recommendation**: Add an LLM contextual-classification tier served on the local rung and measure it against the regex tiers on the same corpus. Replace "retroactive deletion" with per-lineage or per-epoch encryption of embeddings so suppression is key destruction, aligning with OPS-004.

#### ADRL-SAF-004: Pinned sessions fail loudly, in the harness's dialect

Decision: no cloud for a pinned lineage by any actor; failure surfaced as a non-retried, harness-recognisable error naming pin, detector and recoveries; intra-local escalation permitted.

**FOR**
- The harness retry contract is now documented precisely enough to design against: Claude Code retries 5xx, timeouts and transient 429 "up to 10 times", but "spend-limit 429 ... isn't a throttle" and fails immediately, so a non-retried status class exists [source: Claude Code errors reference, 2026, https://code.claude.com/docs/en/errors (fetched)].
- The `capability_rejected:` token is a stable published mechanism: retry logic "matches on the upstream's error wording", and an envelope breaks recovery "unless the envelope's message carries a stable `capability_rejected:` token" [source: Gateway protocol reference, Claude Code docs, 2026, https://code.claude.com/docs/en/llm-gateway-protocol (fetched)].
- Binding the gateway is implementable today: LiteLLM supports `"disable_fallbacks": true` per request and per key, which gives ADRL a mechanical way to make pinned traffic fallback-free [source: Fallbacks (Provider Failover), LiteLLM docs, https://docs.litellm.ai/docs/proxy/reliability (fetched)].

**AGAINST**
- Gateway fallback semantics have a documented exception that defeats "rung-closed": "If all models in a group are in cooldown ... LiteLLM will fallback to the model with the specific model ID. This skips any cooldown check for the fallback model" [source: LiteLLM reliability docs (fetched)]. A pinned local group in cooldown can be served by whatever `default_fallbacks` names.
- Unattended sessions change the retry contract: `CLAUDE_CODE_RETRY_WATCHDOG` "retries 429/529 indefinitely", so a block emitted as either of those statuses on a CI runner is a permanent loop, not one visible error [source: Claude Code errors reference (fetched)].
- The dialect is versioned by harness release. The gateway docs record behaviour changes at v2.1.181, v2.1.197, v2.1.223, v2.1.227, v2.1.229 and v2.1.248 in one page; a "harness-recognisable error" is a contract with a moving target and the decision has no version pin [source: Gateway protocol reference (fetched)].
- Direct-to-Anthropic paths remain outside the pin: the fast-mode check and the WebFetch domain safety check "call api.anthropic.com directly rather than following ANTHROPIC_BASE_URL" [source: Gateway protocol reference (fetched)].

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Add `disable_fallbacks` on the pinned key or per request as the mechanical binding, and a CI check that `default_fallbacks` contains no cloud deployment. Pin the surfacing contract to a tested Claude Code version range and re-run the protocol test on each release, as the follow-up already implies.

#### ADRL-SAF-005: Block, and make the block recoverable

Decision: privacy-context conflicts block; the block uses the vendor's too-long wording so the harness compacts; the local rung must hold the harness's compaction request (100k floor).

**FOR**
- The 100k clamp is confirmed verbatim: Claude Code "clamps the value to at least 100,000 tokens and at most the model's context window, so you can't match a gateway limit below 100,000, and `/compact` remains the recovery there" [source: Connect Claude Code to an LLM gateway, 2026, https://code.claude.com/docs/en/llm-gateway-connect (fetched)].
- The harness's own context-limit path is now specified: on a request rejected because "the input plus `max_tokens` exceeds the context limit", Claude Code "retries with a reduced `max_tokens`, and stops retrying and compacts instead" when nothing fits [source: Claude Code errors reference, 2026 (fetched)].
- LiteLLM's `context_window_fallbacks` with `enable_pre_call_checks` is the gateway-side analogue, and it is what must be disabled for pinned traffic [source: LiteLLM reliability docs (fetched)].

**AGAINST**
- The decision promises "one clear failure" but the harness's documented behaviour on a recognised too-long error is to retry first with a reduced `max_tokens` and compact only when no reduction fits; a pinned overflow block will therefore be retried at least once, and the block must be idempotent and cheap [source: Claude Code errors reference (fetched)].
- Token budgets moved under the decision's feet: the Opus 4.7 tokenizer maps "the same input ... to more tokens, roughly 1.0 to 1.35x", measured at 1.46x on a real system prompt; a compaction floor computed in one tokenizer is wrong for the next [source: Claude Token Counter, now with model comparisons, Simon Willison, 2026, https://simonwillison.net/2026/Apr/20/claude-token-counts/ (fetched)].
- `count_tokens` is optional at the gateway; when absent "Claude Code falls back to counting context usage through the inference endpoint", which means the harness's own view of context size may come from inference calls that a pinned lineage must serve locally [source: Gateway protocol reference (fetched)].

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Amend sub-clause 1 to state that the block is idempotent under the harness's reduced-`max_tokens` retry and that at most one such retry is expected before compaction. Compute the compaction-floor check per model family and re-run it on each tokenizer change.

#### ADRL-SAF-006: Infeasible rungs removed before optimisation

Decision: unhealthy or context-infeasible rungs are removed from the candidate set before optimisation.

**FOR**
- The gateway does the same thing at its layer: LiteLLM's health-check-driven routing removes a deployment "immediately, before a user request lands on it", and cooldowns "temporarily remove unhealthy deployments from the active pool" [source: Health Check Driven Routing, LiteLLM docs, https://docs.litellm.ai/docs/proxy/health_check_routing (search title); LiteLLM reliability docs (fetched)].
- Tokenizer files for local families are downloadable, so exact counts on the rung's own tokenizer are available: "Qwen3, DeepSeek-V3, Llama 4, Mistral's Tekken, and GLM-5 all ship downloadable tokenizer files" [source: Token Counting Explained: tiktoken, Anthropic, and Gemini, Propel Code, 2025, https://www.propelcode.ai/blog/token-counting-tiktoken-anthropic-gemini-guide-2025 (search title)].

**AGAINST**
- A once-calibrated safety ratio is stale by construction: Anthropic's own tokenizer changed by "roughly 1.0 to 1.35x" at Opus 4.7, and the decision's follow-up proposes a static per-rung ratio [source: Claude Token Counter, Simon Willison, 2026 (fetched)].
- The gateway health view the decision wants to read may not exist: "Background health checks are off by default" in LiteLLM, so "read the gateway's view" degrades to reading cooldown state derived from failed requests, which is reactive rather than predictive [source: Health Check Driven Routing, LiteLLM docs (search title)].
- Cross-family divergence on code is larger than on prose: modern tokenizers are "15 to 40% more efficient for code than older tokenizers", so a Claude-derived count applied to a local model errs in an unknown direction, as the review already noted, and the magnitude is now quantified [source: Tokenizer Comparison, Part 2, Medium, https://atul4u.medium.com/tokenizer-comparison-part2-comprehensive-tokenizer-performance-analysis-a8e0613bed0d (search title)].

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Replace the "safety ratio" follow-up with exact counting on each local rung's published tokenizer and treat the Claude count as an estimate for the cloud rungs only. Enable gateway background health checks as a prerequisite of "read the gateway's view".

#### ADRL-SAF-007: Verification runs sandboxed, then diffed

Decision: verification runs inside the harness's OS-enforced sandbox (Seatbelt, bubblewrap plus seccomp) in strict mode with no egress, against a worktree snapshot, with a per-repository command allow-list.

**FOR**
- Reusing the harness's primitive is how the vendors themselves contain agents: Anthropic uses "Seatbelt on macOS, Bubblewrap on Linux" for Claude Code, gVisor for claude.ai, and full VMs for Cowork, on the principle that "if credentials never enter the sandbox, they can't be exfiltrated" [source: How we contain Claude across products, via Simon Willison, 2026, https://simonwillison.net/2026/May/30/how-we-contain-claude/ (fetched)].
- Codex independently chose the same primitives (Seatbelt; bubblewrap plus Landlock plus seccomp; Windows restricted tokens) and marks ".git/ and .codex/ directories within writable roots ... read-only", the same self-widening concern SAF-007 names [source: OpenAI Codex CLI Sandbox Analysis Report, Agent Safehouse, 2026, https://agent-safehouse.dev/docs/agent-investigations/codex (fetched)].
- Strict mode is real and documented: with `allowUnsandboxedCommands: false` "the `dangerouslyDisableSandbox` parameter is completely ignored", and deny rules hold inside wider allows [source: Configure the sandboxed Bash tool, Claude Code docs, 2026, https://code.claude.com/docs/en/sandboxing (fetched)].

**AGAINST**
- The chosen primitive has a nine-month escape record: CVE-2025-66479 (deny-all interpreted as allow-all, live from 20 October to 26 November 2025), a SOCKS5 null-byte hostname bypass fixed in v2.1.88, CVE-2026-39861 (symlink following) and CVE-2026-55607 (worktree named `.git`, code execution "outside of seatbelt sandbox restrictions", fixed v2.1.163, July 2026). A team "had no way to know the sandbox was effectively off" for five weeks [source: Anthropic Silently Patches Claude Code Sandbox Bypass, SecurityWeek, 2026, https://www.securityweek.com/anthropic-silently-patches-claude-code-sandbox-bypass/ (fetched); CVE-2026-55607 advisory, GitLab, 2026, https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2026-55607/ (fetched); Critical Claude Code Sandbox Vulnerability Enables Network Escape, Medium, 2026, https://medium.com/@Inforsecpro/critical-claude-code-sandbox-vulnerability-enables-network-escape-and-arbitrary-file-write-attacks-2186222829d4 (search title)].
- Anthropic's own guidance for the verifier's threat class is a VM, not Seatbelt: for "Work on an untrusted repository" the docs say "A dedicated virtual machine", and warn that the Bash sandbox "constrains only Bash" while "MCP servers and hooks are separate processes that run unconstrained on the host" [source: Choose a sandbox environment, Claude Code docs, 2026, https://code.claude.com/docs/en/sandbox-environments (fetched)].
- Sub-clauses 1 and 2 collide on Linux. The sandbox runtime "builds the deny list once at launch ... and does not cover anything the session creates later, such as `git init`, `git clone`, or scaffolding"; a worktree created at the action boundary is exactly such a later creation, so the snapshot the decision requires is outside the deny list the decision relies on [source: Choose a sandbox environment (fetched)].
- The macOS primitive is deprecated with no replacement: `sandbox-exec` prints "WARNING: sandbox-exec is deprecated. Consider adopting the App Sandbox instead", App Sandbox requires code signing and Xcode, and Apple has not answered the removal-timeline question opened in May 2026 [source: Clarify sandbox-exec deprecation timeline, apple/containerization issue 737, 2026, https://github.com/apple/containerization/issues/737 (fetched)]. Cursor's parallel sandbox was escaped the same way (CVE-2026-50548/50549, CVSS 9.8, via `working_directory` and symlink validation) [source: Critical Cursor Flaws Could Let Prompt Injection Escape Sandbox, The Hacker News, 2026, https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html (fetched)].

**Grounding verdict**: CONTESTED (newest source 2026).

**Recommendation**: For restricted repositories (SAF-008 class), require a microVM or container boundary (Firecracker, Docker Sandboxes, gVisor) for verification and reserve the Seatbelt/bubblewrap path for unrestricted repositories, matching Anthropic's own tiering. Add a synthetic "sandbox actually on" probe (attempt egress, attempt a write outside scratch) before every verification run, because the five-week CVE-2025-66479 window shows configuration alone is not evidence.

#### ADRL-SAF-008: Repository and data-class gate (PII tier retained in SAF)

Decision: repository identity sets a rung ceiling and residency constraint before content scanning; PII is a separate detector tier with in-region-or-local pin semantics.

**FOR**
- Residency-by-profile is current provider practice: Bedrock's geographic profiles keep "data residency within geographic boundaries (such as US, EU, and APAC)", global profiles route "any supported AWS commercial Region worldwide" for "approximately 10% savings", and CloudTrail records `additionalEventData.inferenceRegion` "to identify where requests were processed" [source: Route model inference requests across AWS Regions, AWS Bedrock docs, https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html (fetched)].
- PII tooling has improved: GLiNER2-PII (0.3B parameters) covers "42 PII entity types at character-span resolution" and "achieves the highest span-level F1 among five compared systems" on SPY; Presidio remains the production framework with GLiNER as a pluggable engine [source: GLiNER2-PII, 2026, https://arxiv.org/abs/2605.09973 (fetched); Best Open Source Models for PII Redaction, Grepture, https://grepture.com/blog/best-open-source-models-pii-redaction (search title)].
- Container-level classification before content scanning is the pattern GitHub uses for secret protection (per-repository and organisation configuration, enterprise security configurations) [source: Delegated bypass for push protection, GitHub Docs (search title)].

**AGAINST**
- The PII tier is ungrounded on realistic mixed-domain text. PIIBench (2.37M sequences, 48 entity types, ten sources) finds "All systems achieve span-level F1 below 0.14, with the best system (Presidio, F1=0.1385) still producing zero recall on most entity types"; code, fixtures and logs are further from any training domain than PIIBench's sources [source: PIIBench, 2026, https://arxiv.org/abs/2604.15776 (fetched)].
- Classification inputs are attacker-controlled metadata: the ADI paper's attack surface is precisely "resource identifiers or data origins" disguised as trusted data, and a cwd or git remote reported in a system prompt block is such metadata [source: Agent Data Injection Attacks, 2026 (fetched)].
- "Local" is not a safe default class for unknown endpoints: 175,000 Ollama hosts were found exposed across 130 countries, "48% of hosts support tool-calling", and the recommended posture is to treat LLM infrastructure "with the same authentication, monitoring, and network controls as other externally accessible infrastructure" [source: Researchers Find 175,000 Publicly Exposed Ollama AI Servers, The Hacker News, 2026, https://thehackernews.com/2026/01/researchers-find-175000-publicly.html (fetched)].
- Geographic profiles pin a geography, not a deployment: within a geographic profile "Amazon Bedrock automatically selects a commercial AWS Region", so a residency tag at the granularity the decision proposes (deployment tagged with a profile) still has run-time region variance the ledger must record from CloudTrail, not infer [source: AWS Bedrock cross-region inference docs (fetched)].

**Grounding verdict**: CONTESTED (newest source 2026): residency clauses CURRENT, PII tier UNGROUNDED on code.

**Recommendation**: Keep clauses 1, 2 and 4 and hand them to TRU as planned. Demote clause 3 from "detector tier with pin semantics" to "shadow-only PII findings until a measured F1 on a the company fixture-and-log corpus exceeds a pre-registered floor", and cite PIIBench as the reason the floor is needed.

#### ADRL-SAF-009: Egress ledger and gate-audit integrity

Decision: append-only, hash-chained, content-free egress ledger with periodic signed checkpoints shipped off-device, separate from and surviving the evidence ledger.

**FOR**
- The construction is now commodity: Rekor v2 went GA on 10 October 2025 as a "tile-backed transparency log" that "will provide stronger security guarantees that the log remains append-only by integrating witnessing directly", with Tessera backends for AWS, MySQL and POSIX filesystems for private operators [source: Rekor v2 GA, Sigstore blog, 2025, https://blog.sigstore.dev/rekor-v2-ga/ (fetched)].
- Automatic, appropriate logging is becoming a legal expectation for AI systems: EU AI Act Article 12 requires that high-risk systems "technically allow for the automatic recording of events (logs) over the lifetime of the system" [source: Article 12: Record-Keeping, EU AI Act explorer, https://artificialintelligenceact.eu/article/12/ (fetched)].
- Tamper-evident logging research is active and performance-aware: a CCS 2025 paper co-designs a high-performance tamper-evident auditing system, so the hot-path cost the review worried about has published mitigations [source: Rethinking Tamper-Evident Logging: A High-Performance, Co-Designed Auditing System, 2025, https://arxiv.org/pdf/2509.03821 (search title)].

**AGAINST**
- Off-device checkpoints signed by the operator do not prove append-only; the transparency community's answer is independent witnesses: "only a single witness is required to prove a log is append-only" and multiple witnesses detect "split view attacks". SAF-009 has no witness, so an operator who controls both host and sink can present two consistent histories [source: Can I Get A Witness (Network)?, transparency.dev, https://blog.transparency.dev/can-i-get-a-witness-network (fetched)].
- A KMS-backed signer leaves no independent record of what it signed: CloudTrail "only record[s] that a sign operation was requested against a key ID at a specific time" and does not include "the original message digest or the resulting signature" [source: Can Cloudtrail support KMS code signing transparency logs, AWS re:Post, https://repost.aws/questions/QUJlrDBq-CRYurHVCIUNxbjw/can-cloudtrail-support-kms-code-signing-transparency-logs-e-g-by-logging-signatures (search title)].
- Ledger integrity inherits the host's integrity. The Claude Code CVE chain writes `.claude/settings.json` and reads "Claude Code's own MEMORY.md"; a hash chain on the same disk can be regenerated by the same attacker between checkpoints, so the checkpoint interval is the exposure window and the decision leaves it unbounded [source: Three CVEs in Claude Code CLI, Phoenix Security, 2026 (fetched)].
- Regulatory timing is less settled than the trade press claims: the EU AI Act explorer now lists Article 12 as applying from 2 December 2027 (Annex III) and 2 August 2028 (Annex I), while several vendor posts still say 2 August 2026; the register should not cite the earlier date as a driver [source: Article 12, EU AI Act explorer (fetched); What the EU AI Act requires for AI agent logging, Help Net Security, 2026, https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/ (search title)].

**Grounding verdict**: CURRENT (newest source 2026), with a witness gap.

**Recommendation**: Specify the anchor as a witnessed transparency log (a private Rekor v2 or Tessera instance with at least one witness outside the gateway team) rather than "an endpoint", and pre-register the checkpoint interval as the maximum undetectable-tamper window. Record the signed digest alongside every KMS signature because the KMS audit trail will not.


### TRU: Trust, Residency and Egress

**State of the field, 2026.** Workload identity has reached agents: HashiCorp positions SPIFFE/SPIRE as the standard for agentic non-human identity (April 2026), AIP proposes invocation-bound capability tokens because "neither MCP nor A2A verifies agent identity" (March 2026), and Bounded Agents chains delegated authority (August 2026). Attestation research argues the signing identity must chain to a root outside the operator (Kettle, May 2026), while industry summits still call self-attestation an open problem. Residency is an endpoint property in practice: Bedrock's EU geographic inference profiles keep routing inside the EU and stamp `inferenceRegion` in CloudTrail (June 2026); Anthropic's first-party API has no EU inference region and Foundry EU is "coming"; Cloudflare's AI Gateway is incompatible with its own Regional Services. The EU deferred high-risk AI obligations to December 2027 but GPAI and transparency duties stand. Tamper-evident logging standardised on tile-based logs with signed checkpoints (Rekor v2 GA October 2025, static CT API, 2026 shards) and independent witness cosigning; CloudTrail's hourly signed digests remain the cloud baseline. Route receipts (May 2026) frame served-path disclosure as a trust requirement.

#### ADRL-TRU-001: Authenticated workload identity (Proposed)

Decision: Repository and data-class identity comes from a signed launcher assertion checked against SCM inventory and corroborated by a content fingerprint; prompt text is evidence only; unknown identity is local-only.

**FOR**
- The agent-identity literature starts from the same observation as TRU-001: protocols do not verify identity, so identity must be an issued, bound credential; AIP's chained tokens catch "delegation depth violation and audit evasion through empty context" with a 100% rejection rate across 600 attacks. [source: Prakash, "AIP: Agent Identity Protocol", 2026, https://arxiv.org/abs/2603.24775 (fetched)]
- SPIFFE is now the de facto standard for agent identity: "each agent receives a SPIFFE ID (SVID) and certificate from a central SPIRE server", with ephemeral identities and automatic rotation. Identity issued by an attestor the subject does not control is the industry model TRU-001 adopts. [source: HashiCorp, "SPIFFE: Securing the identity of agentic AI and non-human actors", 2026, https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors (fetched)]
- Provenance research agrees the trust anchor must sit outside the operator: Kettle chains the signing identity "to the TEE manufacturer's root of trust rather than to the build infrastructure operator", and the 2025 government supply-chain summit records that "self-attestation can be misleading or fabricated, which is still an open problem". Prompt-derived identity is self-attestation. [source: Asad and Arko, "Kettle: Attested builds for verifiable software provenance", 2026, https://arxiv.org/abs/2605.08363 (fetched); "S3C2 Summit 2025-07: Government Secure Supply Chain Summit", 2026, https://arxiv.org/pdf/2605.29140 (search result)]

**AGAINST**
- Certificate-style issuance does not fit spawn rates: "SPIRE requires dedicated infrastructure and X.509 certificate issuance latency is incompatible with ephemeral agent creation". With 20 concurrent subagents and three levels by default, per-lineage assertions inherited from the parent are the right shape, but worktree subagents run in a checkout "branched by default from your default branch", so the parent's content fingerprint will not corroborate the child's tree. [source: "Ethical Hyper-Velocity (EHV): A Hardware-Rooted Zero-Trust Runtime Enforcement Architecture for Agentic AI Systems", 2026, https://arxiv.org/pdf/2605.17909 (search result); Anthropic, "Create custom subagents", 2026, https://code.claude.com/docs/en/sub-agents (fetched)]
- Kettle's argument cuts against a laptop launcher: only a root of trust the operator cannot touch removes the operator from the trust surface. A wrapper the developer can run as root yields, as the decision's own attack 1 concedes, denial rather than integrity; hardware-backed keystores (TPM, Secure Enclave) are not mentioned. [source: Asad and Arko, "Kettle", 2026, https://arxiv.org/abs/2605.08363 (fetched)]
- A simpler trusted channel already exists: the Claude apps gateway delivers managed settings by IdP group, "a developer can't override what their policy locks", and it can push egress allowlists and directory rules to the client. Repository classification could arrive as a locked managed setting bound to the authenticated session rather than through a new launcher and assertion schema. [source: Anthropic, "Claude apps gateway", 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Accept at D0. Amend to evaluate the gateway managed-settings channel as the assertion transport (OPS follow-up), define fingerprint corroboration for worktree children, and prefer a hardware keystore for the assertion-binding key where the device has one.

#### ADRL-TRU-002: Permitted deployment set (Proposed)

Decision: Gates tighten and routing chooses from a signed inventory of deployments with trust zone, geography and data-use profile; local entries are loopback by rule; every dispatch yields a served-deployment receipt.

**FOR**
- Geography is a deployment property in the largest provider's model: EU geographic profiles mean "requests from EU source Regions can't get routed to non-EU Regions", logs "continue to record log entries only in the source Region", and CloudTrail exposes the "inferenceRegion field in the additionalEventData section", which is a vendor-issued served-deployment receipt. [source: AWS, "Unlocking AI flexibility in Europe: A guide to cross-region inference for EU data processing and model access", 2026, https://aws.amazon.com/blogs/machine-learning/unlocking-ai-flexibility-in-europe-a-guide-to-cross-region-inference-for-eu-data-processing-and-model-access/ (fetched)]
- Rungs cannot encode residency: Anthropic's first-party API processes on US infrastructure by default with no EU inference region, EU residency exists "only by deploying Claude through AWS Bedrock or Google Cloud Vertex AI EU regions", and Foundry EU is listed as "Coming 2026". A "frontier" rung spans deployments with different residency. [source: InfoQ, "Claude Reaches GA on Microsoft Foundry: European Enterprises Cannot Deploy It", 2026, https://www.infoq.com/news/2026/07/claude-foundry-ga-europe/ (search result); Anthropic Privacy Center, "Where are your servers located?", https://privacy.anthropic.com/en/articles/7996890-where-are-your-servers-located-do-you-host-your-models-on-eu-servers (search result)]
- Route receipts research treats "regional endpoints, fallback rules" as material facts a relying party must be able to reconstruct; clause 4 is that artifact. [source: Schmalbach, "Model Routing as a Trust Problem", 2026, https://arxiv.org/abs/2605.01710 (fetched)]
- Intersection is the right algebra: ChainCaps' budgets "propagate by intersection, meaning authority can only be preserved or reduced, never gained", which is the monotone permitted set of clause 2. [source: Jiang et al., "ChainCaps", 2026, https://arxiv.org/abs/2605.26542 (fetched)]
- Gateway choice is itself a residency property: Cloudflare's AI Gateway "runs only on Cloudflare's edge ... and the product is documented as incompatible with Cloudflare's own Regional Services for data localization". The inventory must cover the gateway hop, not only the model endpoint. [source: API Evangelist, "Cloudflare AI Gateway" profile, 2026, https://github.com/api-evangelist/cloudflare-ai-gateway (search result)]

**AGAINST**
- The vendor gateway fails over across regions and providers "without developers noticing" and the documentation shows no per-response deployment identifier, so a `gateway_reported` receipt has no defined source when the upstream is a Claude apps gateway; `proxy_observed` sees only the gateway's host. Clause 4's receipt is unattainable for the most likely enterprise topology until Q7 attestation exists. [source: Anthropic, "Claude apps gateway", 2026, https://code.claude.com/docs/en/claude-apps-gateway (fetched)]
- Route receipts are "documentation-based artifacts intended for transparency"; the paper "does not specify who signs route receipts". The literature has the concept but not the attestation mechanism the decision's attack 1 needs. [source: Schmalbach, "Model Routing as a Trust Problem", 2026, https://arxiv.org/abs/2605.01710 (fetched)]
- Source region matters, not only destination geo: "requests originating from outside of the EU can also be optimized with EU CRIS, where CRIS optimizes inference within the EU Regions in addition to respective source Regions". The inventory entry needs a `source_region` (where the gateway or proxy runs), which the schema lacks. [source: AWS, "Unlocking AI flexibility in Europe", 2026, https://aws.amazon.com/blogs/machine-learning/unlocking-ai-flexibility-in-europe-a-guide-to-cross-region-inference-for-eu-data-processing-and-model-access/ (fetched)]
- Regulatory pressure shifted: Annex III high-risk obligations moved to 2 December 2027; GPAI provider and Article 50 transparency duties remain. Residency in the inventory is a GDPR and contractual driver, not an AI Act one, and the decision should say which obligation `data_use_profile` serves. [source: Cloud Security Alliance, "EU AI Act's High-Risk Deadline: Deferred, Not Cancelled", 2026, https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/ (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Accept at D0. Amend the inventory entry to include `source_region` and the gateway hop, add `gateway_attested` to the receipt source enum as the Q7 target, and state that a Claude apps gateway upstream yields `assumed_intended` receipts until it attests.

#### ADRL-TRU-003: Egress anchoring (Proposed)

Decision: Ledger checkpoints are automatic, signed with a separate OPS-provisioned key, shipped to an off-device anchor, verified for signatures and anchors, with development keys refused by default.

**FOR**
- The state of the art is a signed, append-only, tile-based log whose clients "should persist" inclusion proofs "alongside artifacts and their signatures"; Rekor v2 reached GA on 10 October 2025 on Trillian-Tessera. Automatic checkpoints and client-held proofs are the baseline TRU-003 adopts. [source: Sigstore, "Rekor v2 GA - Cheaper to run, simpler to maintain", 2025, https://blog.sigstore.dev/rekor-v2-ga/ (fetched)]
- Witness cosigning is the accepted answer to a logger that might equivocate: a witness "signs it only after verifying the consistency proof" and "a set of witnesses (ideally an odd number) can be used to detect split view attacks". The anchor acknowledgement in clause 3 is a one-witness instance. [source: transparency.dev, "Can I Get A Witness (Network)?", https://blog.transparency.dev/can-i-get-a-witness-network (search result); transparency-dev/witness, https://github.com/transparency-dev/witness (search result)]
- Cloud audit logging already does periodic signed digests: CloudTrail "creates and delivers a file that references the log files for the last hour and contains a hash of each", signed with SHA-256 with RSA, validated with a published public key. Clause 2's timer-driven checkpoint has a direct precedent. [source: AWS, "Validating CloudTrail log file integrity", https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html (search result)]
- Checkpoint formats standardised: C2SP static CT API and tlog-tiles define signed checkpoints that "may include other note signatures ... by third parties such as witnesses", with 2026 shards rolling out. The anchor acknowledgement can be a standard cosignature rather than a bespoke format. [source: C2SP, "The Static Certificate Transparency API", v1.1.0, https://c2sp.org/static-ct-api@v1.1.0 (search result)]

**AGAINST**
- One anchor inside the operator's trust domain is one witness, and the decision lets the gateway host it (Q7). Split-view detection needs independent witnesses; an OPS-run anchor audits the OPS-run operator bypass with an OPS-held key. [source: transparency.dev, "Can I Get A Witness (Network)?", https://blog.transparency.dev/can-i-get-a-witness-network (search result)]
- Even Rekor v2 has not shipped witnessing: "this will be implemented soon". TRU-003 proposes a stronger property than the reference public log delivers today, which bounds what maturity a laptop-side implementation can honestly claim. [source: Sigstore, "Rekor v2 GA", 2025, https://blog.sigstore.dev/rekor-v2-ga/ (fetched)]
- Per-device key provisioning over the same OPS channel TRU-001 uses means one device compromise defeats both identity and audit; Kettle's position is that only a root of trust outside the operator (and the device owner) closes this, and the decision does not require a hardware keystore for the checkpoint key. [source: Asad and Arko, "Kettle", 2026, https://arxiv.org/abs/2605.08363 (fetched)]
- Deployer logging duties that would have made the ledger a compliance artifact are deferred to December 2027 for Annex III systems; the ledger's justification is internal audit and GDPR accountability, and the decision should not lean on the AI Act. [source: Cloud Security Alliance, "EU AI Act's High-Risk Deadline: Deferred, Not Cancelled", 2026, https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/ (fetched)]

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Accept at D0. Amend clause 3 to require at least one witness outside the gateway operator's control for pinned or residency-tagged lineages (a public witness network or a security-team-run witness), adopt the C2SP checkpoint and cosignature format, and prefer a hardware keystore for the checkpoint key.


### RTG: Routing Intelligence and Economics

**State of the field, 2026.** Routing research moved in 2026 from single-turn prompt classifiers to trajectory-conditioned and step-level decisions inside agents. The Routing Plateau study of 21 routers found they converge far below the oracle because they learn global model averages, not instance signals; SWE-Router proved that conditioning on a cheap model's partial trajectory is Bayes-better than routing on the prompt; TwinRouterBench and the Replay Gap paper established that replayed transcripts score "the wrong world", so routers must be evaluated by live branching. Commercial practice converged on session-level, cache-aware decisions: GitHub Copilot's HyDRA routes only at cache boundaries and reports 72.5% savings; Not Diamond Code (August 2026) routes model and reasoning effort per step while weighing KV-cache state, sub-agent structure and compaction; OpenRouter pins model and provider per session id. Reasoning effort became a first-class per-step lever (Ares, TAB, DART). The Handoff Tax paper (August 2026) is the most consequential new result: escalating mid-trajectory recovers less than half the quality gap at a cost premium, while downshifting is favourable.

#### ADRL-RTG-001: Three capability rungs with measured boundaries

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

#### ADRL-RTG-002: Cheapest rung likely to complete, defined

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

#### ADRL-RTG-003: Rules own clear cases, measured

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

#### ADRL-RTG-004: Local-first only with a bounded, clean cascade

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

#### ADRL-RTG-005: Objective: verified quality, retry, latency, session cost

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

#### ADRL-RTG-006: Advisory LLM classifier, gated and bounded

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

#### ADRL-RTG-007: Marginal-utility target, with a build gate

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

#### ADRL-RTG-008: Rung vs endpoint, with a leak contract

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

#### ADRL-RTG-009: Session-marginal, cache-aware cost accounting

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


### CAS: Execution, Cascade, Recovery

**State of the field, 2026.** The 2026 failure literature says the dangerous failures are silent: confident closing language over a failed state (45-76% of failures depending on setting), silent semantic patches that stay consistent across runs, and "fail-plausible" narratives in production runtimes, with LLM judges no better than 0.65 AUROC while cheap text detectors reach 0.83-0.95. Loop failures remain real (68 confirmed infinite-loop defects across 47 projects) and every serious harness now ships fingerprint-based stuck detection. Hand-offs between models are now a measured phenomenon: the Handoff Tax paper shows escalation recovers under half the gap and downshift is favourable, and the Replay Gap shows a swapped model rewrites 61-94% of subsequent actions. Providers hardened reasoning-state semantics in 2026: Anthropic binds thinking signatures to model and prefix (enforced for accounts from 31 August 2026) and reports drops via input_transformations; OpenAI reuses encrypted reasoning only within a family; a same-family key flaw let weaker models decode stronger models' traces until mitigated in August. Gateways adopted deployment affinity, retry budgets and per-tool replay tokens. MCP's current spec says clients MUST treat annotations as untrusted.

#### ADRL-CAS-001: Deterministic trip-wires, with measured coverage

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

#### ADRL-CAS-002: Typed failures, versioned enum, measured attribution

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

#### ADRL-CAS-003: Action boundary defined; no re-issue after side effects

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

#### ADRL-CAS-004: Cross-model handoff: provider-pair rules, not one stripping rule

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

#### ADRL-CAS-005: Sticky escalation within an episode

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

#### ADRL-CAS-006: Record the served model, not only the served rung

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

#### ADRL-CAS-007: Terminal failure surfaced; ADRL owns zero retries

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

#### ADRL-CAS-008: Escalation scope under subagents

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

#### ADRL-CAS-009: Action-effect provenance and authorization boundary

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


### MEM: Memory, Evidence, Label Integrity

**State of the field, 2026.** Three things changed in the last eighteen months. First, the "verified" in verified coding labels collapsed as a trust anchor: OpenAI stopped reporting SWE-bench Verified in 2026 after an audit found 59.4% of a hard subset had test flaws that reject correct patches, and 2026 mining studies show agent-written tests are flakier and more heavily mocked than human ones. Second, embeddings are now formally treated as prompt-class data: Zero2Text (Feb 2026) inverts black-box embeddings with no training pairs and defeats differential-privacy noise, and Ghost Vectors (Jun 2026) shows soft-deleted vectors remain recoverable from HNSW index files; the only defence that survives both is per-key encryption with key destruction, which the EDPB's final blockchain guidelines (v2, July 2026) endorse as erasure. Third, failure attribution moved from enum typing to counterfactual re-execution: LLM judges attribute failing steps at roughly 14% accuracy, and 2026 taxonomies (41 modes on component edges, kappa 0.76) place harness, grader and environment faults alongside model faults. Append-only, hash-chained agent ledgers are now routine.

#### ADRL-MEM-001: Append-only ledger keyed by route_id

Decision: Transaction memory is an append-only decision/outcome/event ledger keyed by an immutable route_id; every event carries a sequence number, idempotency key and schema version; erasure is the one logged mutation.

**FOR**
- Append-only, replayable action ledgers are the 2026 baseline for agent accountability; a 2026 survey of persistent agent systems names "provenance and audit records" as core state and observes the field under-invests in governing and relinquishing state, which is exactly what clauses 2 and 3 add. [source: Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents, 2026, https://arxiv.org/abs/2606.30306 (fetched)]
- Sample-level, tamper-evident provenance is now argued as necessary for auditable ML pipelines: FG-Trac tracks whether a specific sample was used, when, and whether its records remain intact, using cryptographic commitments, which is the route_id-per-event discipline at finer grain. [source: Fine-Grained Traceability for Transparent ML Pipelines, 2026, https://arxiv.org/abs/2601.14971 (fetched)]
- Reproducibility is being framed as a trust primitive for agent tool use, with a verifiable interaction ledger logging capability definitions, execution claims and provenance at under 0.02% overhead; the ledger-first posture of MEM-001 is aligned. [source: Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use, 2026, https://arxiv.org/abs/2603.14332 (fetched)]

**AGAINST**
- The EDPB's final Guidelines 02/2025 (v2.0 adopted 7 July 2026) recommend not registering clear-text, encrypted or hashed personal data on an immutable ledger at all, and treat key destruction as erasure only where off-ledger design was considered up front. MEM-001 keeps ciphertext and keyed hashes in the immutable stream forever; the "skeleton survives" clause is defensible but the guidance says the default should be by-reference storage, not encrypted-in-stream. [source: EDPB Guidelines 02/2025 on processing of personal data through blockchain (v2, July 2026), 2026, https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf (search)] and [source: EDPB adopts guidelines on processing personal data through blockchains, 2025, https://www.edpb.europa.eu/news/news/2025/edpb-adopts-guidelines-processing-personal-data-through-blockchains-and-ready_en (fetched)]
- 2026 agent ledgers are hash-chained (SHA-256 or SHA3 per action, Ed25519 signed) so that any in-place edit breaks the chain; MEM-001 relies on a provider port refusing UPDATE, which is a convention, not tamper evidence. A ledger that EVL readiness claims stand on has no integrity proof. [source: Governed Reasoning for Institutional AI, 2026, https://arxiv.org/pdf/2604.10658 (search)] and [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 (fetched)]
- Inference nondeterminism is measured at 5.8x variance across nine models and seven providers; an append-only record of "what the router saw and did" cannot claim the served model's output was reproducible from the event, so replay-from-ledger is provenance, not reproduction. The decision text implies more than it can deliver for the model side. [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 (fetched)]

**Grounding verdict**: CURRENT (newest relevant source: 2026).

**Recommendation**: Keep the decision; add a per-route_id hash chain (previous-event hash on every event) so immutability is verifiable rather than declared, and record in the rationale that the ledger proves what was logged, not that model output is reproducible. Reconsider, with MEM-010, whether prompt-class ciphertext should be stored by reference outside the stream as the EDPB now recommends.

#### ADRL-MEM-002: Three-state outcome lifecycle with defined close

Decision: pending, closed_turn, closed_final after a versioned closing window; late evidence is appended and re-derives the label; non-final outcomes are censored.

**FOR**
- The 2026 delayed-feedback literature confirms the posture: WWW 2026 work on net conversion (purchase then refund) shows a two-stage cascaded delay must be modelled as separate stages with stage-wise debiasing, and that delay time itself is a predictive feature. ADRL's "closed_turn success then human revert" is structurally the same cascade. [source: Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction: Benchmark, Insights and Solutions, 2026, https://arxiv.org/abs/2601.19965 (fetched)]
- The largest 2026 study of coding-agent sessions (20,574 sessions, 1,639 repos) finds 91.49% of visible resolutions of agent misalignment required explicit user correction, confirming that the human is the dominant late-evidence source the amended text names. [source: How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions, 2026, https://arxiv.org/abs/2605.29442 (fetched)]
- Code churn (rewritten or deleted within two weeks) roughly doubled from 3.3% pre-AI to 7.1% in 2025 in GitClear's 2026 analysis, so a label frozen at first success systematically over-credits AI-authored edits, which is the bias clause 3's time-to-close measurement is meant to expose. [source: The Maintainability Gap: 2026 AI Code Quality Research, GitClear, 2026, https://www.gitclear.com/the_ai_code_quality_maintainability_gap (search)]

**AGAINST**
- The field has moved past "wait then close": TRACE (Apr 2026) uses the evolving post-click trajectory to refine the label posterior before the window closes, with a reliability-gated completer for early samples. MEM-002 has no trajectory signal; it either waits or freezes. For ADRL the analogue is the next-N-turn edit trajectory on the same files, which the follow-up describes but the decision does not require. [source: Follow the TRACE: Exploiting Post-Click Trajectories for Online Delayed Conversion Rate Prediction, 2026, https://arxiv.org/abs/2604.23197 (fetched)]
- Agentic PR data shows a two-regime world: 28.3% of 33,707 agent PRs merge almost immediately while a large share of the rest enter iterative review and are abandoned. A single closing window will be too long for the first regime and too short for the second; the window should be conditioned on the regime, not global. [source: Early-Stage Prediction of Review Effort in AI-Generated Pull Requests (MSR 2026), 2026, https://arxiv.org/html/2601.00753 (search)]
- The Microsoft rollout study warns that "a merged PR is not the same as the value it delivers"; closed_final defined by absence of revert still measures survival, not correctness, so the label semantics remain proxy even after the window. [source: Adoption and Impact of Command-Line AI Coding Agents, 2026, https://arxiv.org/abs/2607.01418 (fetched)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the three states, but make the closing rule regime-aware (instant-merge versus iterative) and add a required same-file edit-trajectory signal that can shorten or extend the window, following TRACE rather than a fixed N turns. State in the rationale that closed_final is a survival label, not a correctness label, unless MEM-003 verification also attaches.

#### ADRL-MEM-003: Verification enriches, never overwrites

Decision: Each verification run is an appended event with verifier version, command, tree identity and pass/fail/indeterminate; drifted-tree runs are excluded from capability labels.

**FOR**
- OpenAI's 2026 audit of SWE-bench Verified found 59.4% of a hard 27.6% subset had test flaws that reject functionally correct submissions (35.5% too narrow, 18.8% too wide), and stopped reporting the benchmark. "The tests" are now officially an unreliable instrument, which vindicates recording verifier provenance and an indeterminate state. [source: Why SWE-bench Verified no longer measures frontier coding capabilities, OpenAI, 2026, https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ S; page returned 403, numbers taken from OpenAI Abandons SWE-Bench Verified, SiliconReport, 2026, https://www.siliconreport.com/openai-abandons-swe-bench-verified-citing-widespread-data-contamination-and-flawed-tests-6ebd9b34 F; note the announcement date is reported as February 2026 by CodeSOTA and July 2026 by SiliconReport]
- LLM-generated tests are measurably flakier than existing tests across SAP HANA, DuckDB, MySQL and SQLite, with unordered-collection dependence in 63% of flaky cases, and flakiness transfers from existing tests through prompt context. A verifier that runs agent-authored tests needs the repeat-run flake measurement clause 2 implies. [source: On the Flakiness of LLM-Generated Tests for Industrial and Open-Source Database Management Systems, 2026, https://arxiv.org/abs/2601.08998 (fetched)]
- Production-derived benchmark curation now uses multi-run stability checks and agentic test-relevance validation as standard layers, which is the provenance-plus-repeat pattern MEM-003 adopts. [source: REAP: Automatic Curation of Coding Agent Benchmarks from Interactive Production Usage, 2026, https://arxiv.org/abs/2604.01527 (fetched)]

**AGAINST**
- Coding agents add mocks in 36% of test commits versus 26% for humans across 1.2M commits; over-mocked tests "may be less effective at validating real interactions". A verifier that runs the repository's own tests, increasingly agent-authored, is partly verifying the agent against itself. MEM-003 records which tests ran but has no notion of test adequacy or mock density, so a "verified pass" can be a pass against a mock. [source: Are Coding Agents Generating Over-Mocked Tests? An Empirical Study, 2026, https://arxiv.org/abs/2602.00409 (fetched)]
- Formal verification of agent workflows (Lean4Agent) separates verification-passing from failing trajectories by 11.94% on SWE-bench Verified, showing that trajectory-level verification carries signal that test pass/fail alone does not; MEM-003's verification is outcome-only. [source: Lean4Agent: Formal Modeling and Verification for Agent Workflow and Trajectory, 2026, https://arxiv.org/abs/2606.06523 (fetched)]
- REAP and SWE-rebench both use LLM-based task classification and automated validity checks at scale; MEM-003 forbids nothing here but the register's "deterministic verification only" framing leaves no tier for an LLM-judged adequacy check, which the field uses as a filter (not a label). [source: SWE-rebench, 2025, https://arxiv.org/abs/2505.20411 (fetched)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the decision; add a test-adequacy field to the verification event (mock density, assertion count, whether tests were agent-authored in the same session) and treat "passed only agent-authored tests" as a lower verification grade in LRN-001. Require N repeat runs, not two, before a suite's labels are tier-1.

#### ADRL-MEM-004: Cause-typed labels, seven types not four

Decision: task_capability is kept separate from harness_dialect, infrastructure, policy_constraint, context_feasibility, user_abort, unverifiable; labels carry rule version, confidence and source event; first-occurring cause is primary.

**FOR**
- The July 2026 interaction-centric taxonomy assigns 41 failure modes to edges between components and tags each as model-side, harness-side, or environment/grader-side, with a maximum Cohen's kappa of 0.76; the model-versus-harness split is exactly MEM-004's task_capability versus harness_dialect and is now mainstream. [source: Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures, 2026, https://arxiv.org/abs/2607.28802 (fetched)]
- A July 2026 synthesis of 27 taxonomy and audit papers identifies "long-horizon degradation from context accumulation" as its own cluster and finds failures compound nonlinearly with task length, which supports the new context_feasibility type. [source: Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents, 2026, https://arxiv.org/abs/2607.05775 (fetched)]
- Label noise is the most damaging noise type in LLM fine-tuning across three model families, ahead of typographical and grammatical corruption, which justifies spending effort on label cause-cleanliness rather than volume. [source: Analyzing the Effect of Noise in LLM Fine-tuning, 2026, https://arxiv.org/abs/2604.12469 (fetched)]

**AGAINST**
- Attribution by inspection is unreliable: LLM-judge step attribution scores about 14% on Who&When, and the 2026 Causal Agent Replay paper argues the correct method is intervention and re-execution under the same stochastic policy, with a Monte-Carlo Shapley split when steps interact. MEM-004's "first-occurring cause is primary" is a heuristic that the 2026 attribution literature treats as insufficient for interacting causes. [source: Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures, 2026, https://arxiv.org/abs/2606.08275 (fetched)] and [source: Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?, 2026, https://arxiv.org/abs/2607.09996 (fetched)]
- The 2026 taxonomies place "environment or grader failure" as a first-class category; MEM-004's enum has no grader/verifier-fault type. A flaky or over-mocked verifier (MEM-003) currently lands in unverifiable or infrastructure, neither of which is right. [source: Model or Harness?, 2026, https://arxiv.org/abs/2607.28802 (fetched)]
- Seven-category taxonomies for long-horizon agents treat categories as orthogonal dimensions that co-occur (catastrophic forgetting, false assumptions, history error accumulation), not as a primary plus one secondary. [source: The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break, 2026, https://arxiv.org/html/2604.11978v1 (search)]

**Grounding verdict**: CONTESTED (2026).

**Recommendation**: Keep the exclusion principle (only task_capability trains the estimator) but add a grader_fault type and allow a multi-label vector with per-type confidence instead of primary plus secondary. Where the counterfactual harness of LRN-002 exists, derive the cause by re-execution (Causal Agent Replay style) rather than by inspection order, and record which method produced the label.

#### ADRL-MEM-005: Prompt-derived artefacts are prompt-class data

Decision: Raw prompts are never stored; embeddings, keyed hashes, paths, argv, verifier output and any locating field are prompt-class under a field-level inventory with a schema test; pin suppression is retroactive.

**FOR**
- Zero2Text (Feb 2026) inverts embeddings from closed-source encoders in a strict black-box setting with no in-domain training pairs and reports that "standard defenses, such as differential privacy, fail to effectively mitigate this adaptive threat". The reclassification of embeddings as prompt-class is not conservative, it is the only reading consistent with 2026 attacks. [source: Zero2Text: Zero-Training Cross-Domain Inversion Attacks on Textual Embeddings, 2026, https://arxiv.org/abs/2602.01757 (fetched)]
- Ghost Vectors (Jun 2026) shows soft-deleted vectors in three HNSW implementations remain physically recoverable from index files and, via Vec2Text, yield 25.5% exact person names and 100% of structured patient demographics; encryption with key discard at deletion reduced PII recovery to 0%. This is the MEM-005/MEM-010 design validated externally. [source: Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases, 2026, https://arxiv.org/abs/2606.18497 (fetched)]
- BeamClean (2025) jointly estimates noise parameters and decodes tokens without knowing the obfuscation mechanism, beating distance-based attacks under Laplacian and Gaussian noise, so noise-only mitigations are not a substitute for access control. [source: BeamClean: Language Aware Embedding Reconstruction, 2025, https://arxiv.org/abs/2505.13758 (search)]

**AGAINST**
- The ADR's follow-up to "evaluate quantisation/noise on stored embeddings as defence in depth" is dated by Zero2Text and BeamClean; the 2026 defence literature has moved to concept-aware, dimension-calibrated noise (SPARSE, Mahalanobis mechanism) precisely because uniform noise destroys utility before it stops inversion. If ADRL wants a noise defence it should test SPARSE-style mechanisms, not 8-bit quantisation. [source: Concept-Aware Privacy Mechanisms for Defending Embedding Inversion Attacks, 2026, https://arxiv.org/abs/2602.07090 (fetched)]
- The 2026 sources say erasure must propagate to caches, summaries, search indexes and conversation histories, and that deleting vectors does nothing for an embedding model fine-tuned on the data. MEM-005's inventory covers ledger, projections, WAL and backups but not any future fine-tuning of the local encoder on ADRL's own corpus; a one-line prohibition is missing. [source: Art.17 Right to Erasure: LLM Training Data Removal & RAG Vector Store Deletion 2026, sota.io, 2026, https://sota.io/blog/eu-ai-act-gdpr-art17-right-erasure-training-data-llm-2026 (fetched)]
- Per-session encryption keeps a lossy copy of source code on disk, and the EDPB's final guidance is that encrypted or hashed personal data on an immutable store should be avoided, not merely encrypted; the honest cost is that suppressing embeddings entirely for retrieval, or holding them only in an ephemeral in-memory index, is the compliant default. [source: EDPB Guidelines 02/2025 v2, 2026, https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf (search)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the replacement text; delete the quantisation follow-up and replace it with a SPARSE-style evaluation only if a noise layer is wanted at all. Add a clause forbidding fine-tuning of the local embedding model on ledger content without an unlearning path, and consider making the retrieval index ephemeral (decrypt to memory per process, never persist the NumPy array) so the persisted store is ciphertext only.

#### ADRL-MEM-006: Memory facade, fail-safe but never silent

Decision: Provider port with NullProvider fallback; degraded decisions are counted, surfaced and excluded from evidence; routing state goes through the port or is declared process-local; the port declares concurrency guarantees.

**FOR**
- 2026 production guidance on SQLite still says single writer at a time, use WAL, set busy_timeout, serialise writes through one worker; lock errors are negligible under roughly 20 concurrent writers and p99 degrades beyond that. Declaring these at the port, as clause 4 does, matches practice. [source: SQLite in Production 2026: Real Benchmarks, Limits, and When to Migrate to Postgres, 2026, https://sesamedisk.com/sqlite-in-production-2026-benchmarks-limits/ (search)]
- The 2026 persistent-agent survey introduces an evaluation protocol that scores "state mutation and recovery obligations rather than answer quality alone", which is the framing of clause 1: degraded mode is a recovery obligation with a metric. [source: Always-On Agents, 2026, https://arxiv.org/abs/2606.30306 (fetched)]

**AGAINST**
- The OpenTelemetry GenAI conventions now model agent runs as invoke_agent, chat, execute_tool and memory-operation spans, and MCP calls share the vocabulary since v1.42.0 (June 2026); ADRL emits a bespoke memory_degraded event. Degraded memory should be an attribute on the standard span, or EVL-009 blockers will live in a telemetry silo. The conventions are still marked Development, so the risk is churn, not absence. [source: OpenTelemetry's GenAI semantic conventions are NOT stable yet, 2026, https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke (search)] and [source: How OpenTelemetry Traces LLM Calls, Agent Reasoning, and MCP Tools, Greptime, 2026, https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions (search)]
- Litestream-style replication is "disaster recovery, not high availability" and can lose the last second of writes; if OPS ever replicates router-memory.db this way, a write-behind outcome_events path (the ADR's recommended choice) silently widens the unlogged window without triggering memory_degraded. [source: SQLite Litestream Replication in Production Guide, 2026, https://www.matthewswong.com/en/blog/sqlite-litestream-replication-production/ (search)]
- No 2025-2026 research directly evaluates fail-open telemetry stores for ML evidence; the decision is grounded in engineering practice, not in a measured result about how much unlogged traffic biases a routing corpus.

**Grounding verdict**: CURRENT (2026, practice-level rather than research-level).

**Recommendation**: Keep the decision; emit degraded-mode state as attributes on OpenTelemetry GenAI spans rather than a private event so EVL, OPS and any external observability share one vocabulary. Record the write-through/write-behind choice now and make replication lag part of the degraded counter.

#### ADRL-MEM-007: Projections are rebuildable and versioned

Decision: Retrieval indexes are projections stamped with ledger high-water mark, embedding-model version and projection-code version; stale is a labelled state; erasure forces invalidation; change detection via PRAGMA data_version.

**FOR**
- LiveVectorLake (Nov 2025) builds exactly this: content-addressable chunk hashing for deterministic change detection, a hot vector tier separate from a cold versioned tier, and point-in-time retrieval with ACID consistency, re-processing 10-15% of content per update instead of 100%. The stamp-and-rebuild design is current practice. [source: LiveVectorLake: A Real-Time Versioned Knowledge Base Architecture for Streaming Vector Updates and Temporal Retrieval, 2025, https://arxiv.org/abs/2601.05270 (fetched)]
- Feature-store practice treats point-in-time (AS OF) joins as the standard leakage defence: each training row gets the latest feature value at or before its timestamp. MEM-007's as-of projection rebuild is the retrieval-feature equivalent. [source: Point-in-time feature joins, Databricks docs, 2026, https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series (fetched)]

**AGAINST**
- Ghost Vectors shows "rebuilt without the affected vectors" is not enough: the old index file, and any copy of it, still holds the vector. Clause 3 must require the previous NumPy file be overwritten or shredded, and the erasure proof in MEM-010 must enumerate projection files, not just the ledger. [source: Ghost Vectors, 2026, https://arxiv.org/abs/2606.18497 (fetched)]
- Sequential-recommender evaluation shows that "temporal user split" still leaks and only a global temporal split prevents leakage; an as-of projection keyed to one decision's ledger position is a per-row cut, and the same warning applies if neighbours from the same session but later turns are permitted. Clause 2 should exclude same-session later rows explicitly. [source: Time to Split: Exploring Data Splitting Strategies for Offline Evaluation of Sequential Recommenders, 2025, https://arxiv.org/abs/2507.16289 (fetched)]
- The as-of rebuild cost scales with the number of training decisions; LiveVectorLake solves this with a versioned cold tier and sub-2s temporal queries, whereas ADRL's plan is "rebuild the NumPy index as of position N" per evaluation, which will not scale to the multi-worker future without a versioned tier.

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the decision; require physical shredding of superseded projection files and add them to the MEM-010 erasure proof. Exclude same-session later rows from as-of neighbours and plan a versioned cold tier (Delta or Parquet snapshots by ledger position) rather than per-query full rebuilds.

#### ADRL-MEM-008: Retrieval stays advisory until gated

Decision: Retrieval remains advisory/shadow until evaluated-label quantity and quality gates pass.

**FOR**
- A May 2026 study of 21 routing methods on five benchmarks finds diverse routers, kNN included, converge to a "routing plateau" well below optimal because they learn global model-performance trends rather than query-specific signal. Retrieval-by-similarity is the canonical plateau router, so keeping it advisory is warranted. [source: The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers, 2026, https://arxiv.org/abs/2606.07587 (fetched)]
- LLMRouterBench (400K instances, 33 models) finds several recent approaches, including commercial routers, fail to reliably beat a simple baseline, and that backbone embedding models have limited impact, so a thin embedding index is unlikely to be the exception. [source: LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing, 2026, https://arxiv.org/abs/2601.07206 (fetched)]
- RouterArena evaluation finds judge scoring deviates from exact-match by 10-24 points, so any retrieval "agreement" metric computed against LLM-judged outcomes rather than verified ones is not a gate. [source: RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers, ICLR 2026, https://proceedings.iclr.cc/paper_files/paper/2026/file/4987bb24bc53c198785922d1bd9e18cf-Paper-Conference.pdf (search)]

**AGAINST**
- The strongest 2026 result for coding-task routing comes from execution-grounded memory: an orchestrator-verifier-memory loop that accumulates task-level performance statistics during deployment gives a 15.3% relative gain over a heuristic router and the lowest cumulative regret on CodeRouterBench, generalising to out-of-distribution agentic tasks. That is retrieval of verified past outcomes, i.e. the MEM-008 mechanism, given authority. A gate that only counts labels may be starving the one signal shown to work. [source: Agent-as-a-Router: Agentic Model Routing for Coding Tasks, 2026, https://arxiv.org/abs/2606.22902 (fetched)]
- Production-derived benchmarks diverge from public ones in language distribution, prompt style and codebase structure; a count gate (300) says nothing about whether the 300 cover the production distribution. The ADR's own follow-up asks for representativeness but the decision text still defers to "quantity and quality". [source: REAP, 2026, https://arxiv.org/abs/2604.01527 (fetched)]
- Contextual-bandit routers now learn from partial feedback with far less exploration data than supervised routers require, so the "advisory until enough labels" posture can be replaced by a bounded-regret online learner that earns authority incrementally rather than by a threshold. [source: WISERouter: LLM Routing with Workload Budget Constraint, 2026, https://arxiv.org/abs/2607.23765 (fetched)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the decision but change what the gate measures: require a coverage/representativeness condition and a verified-outcome agreement metric, and permit retrieval to advise the LRN-003 estimator (as Agent-as-a-Router's memory does) before it advises routing. The plateau literature says retrieval alone should never be the router; the execution-grounded result says retrieval of verified outcomes is the feature that breaks the plateau.

#### ADRL-MEM-009: Counterfactuals bind only to explicit route_id

Decision: Counterfactual evidence attaches only to an explicit route_id; proximity is never used.

**FOR**
- Causal Agent Replay models an agent run as a structural causal model, applies do() to a named step and re-executes forward; attribution is by explicit intervention identity, never by time. Who&When Pro likewise constructs 12,326 failure trajectories by "injecting a failure only after exactly replaying a successful prefix", which is explicit binding to a prefix. [source: Causal Agent Replay, 2026, https://arxiv.org/abs/2606.08275 (fetched)] and [source: Who&When Pro, 2026, https://arxiv.org/abs/2607.09996 (fetched)]
- The Replay Gap (Aug 2026) shows 74-77% of early model swaps diverge at the first post-fork action and replay predicts patches with 0.00-0.11 similarity to reality; any binding looser than "this decision, this state" scores a different world. [source: The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World, 2026, https://arxiv.org/abs/2608.08239 (fetched)]
- A June 2026 analysis of 33,596 agent PRs shows a naive pooled comparison (53.8% vs 79.8% merge rate) reverses under repository and commit-count controls; inference from co-occurrence is exactly what MEM-009 forbids. [source: Beyond Simpson's Paradox: A Cascade of Confounders in AI Agent Pull-Request Co-Authorship, 2026, https://arxiv.org/abs/2606.22711 (fetched)]

**AGAINST**
- Explicit binding does not fix nondeterminism: measured inference determinism varies 5.8x across providers, so two runs bound to the same route_id can differ for reasons unrelated to the rung. Causal Agent Replay handles this with multiple stochastic re-executions and a point-of-commitment rule; MEM-009 plus LRN-002 currently allow one branch per arm. [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 (fetched)] and [source: Causal Agent Replay, 2026, https://arxiv.org/abs/2606.08275 (fetched)]
- The rule makes subagent counterfactuals impossible (SEM-006 at D0); the 2026 attribution benchmarks are multi-agent by construction, so ADRL's corpus will be blind to the class of failures the literature now studies most.

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the rule unchanged. Add to the rationale that explicit binding is necessary and that LRN-002 must supply repeated stochastic branches per arm so the bound counterfactual is a distribution, not a single sample.

#### ADRL-MEM-010: Retention and erasure of ledger and derived artefacts

Decision: Every inventoried field has a retention period and erasure procedure; prompt-class rows are encrypted per session and crypto-shredded; erasure is an event, invalidates projections, and is proven by a check over every store including WAL and backups.

**FOR**
- The EDPB's final blockchain guidelines (v2.0, 7 July 2026) accept rendering data unidentifiable by destroying encryption keys or erasing off-chain components where technical deletion is infeasible, which is clause 2. [source: EDPB Guidelines 02/2025 v2, 2026, https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf (search)] and [source: Blockchain And GDPR: EDPB Guidelines 02/2025 Adopted, Mondaq, 2026, https://www.mondaq.com/fin-tech/1617044/blockchain-and-gdpr-edpb-guidelines-022025-adopted (search)]
- Ghost Vectors' Epoch Key Rotation (encrypt vectors, discard keys on deletion, emit cryptographic proof of deletion) reduced PII recovery to 0% and completed deletion of 500 vectors in 2.5 ms; MEM-010 clause 5's erasure_verified event is the same "proof of deletion" idea. [source: Ghost Vectors, 2026, https://arxiv.org/abs/2606.18497 (fetched)]
- A January 2026 crypto-shredding design for GDPR-plus-MiFID II retention uses per-subject AES-256-GCM keys, keeps hash-chain integrity after shredding, mandates backup destruction, and issues erasure certificates; this is MEM-010 with an HSM. [source: Crypto-Shredding: The Technical Foundation for Reconciling GDPR and Financial Record-Keeping Obligations, VeritasChain, 2026, https://veritaschain.org/blog/posts/2026-01-18-crypto-shredding-gdpr-mifid-ii-reconciliation/ (fetched)]

**AGAINST**
- The same EDPB guidance recommends not registering clear-text, encrypted or hashed personal data on the immutable ledger in the first place and considering erasure at design time; MEM-010 chooses encrypt-in-stream over store-by-reference. For a payments company the by-reference design (ciphertext in a deletable side store, only a pointer in the ledger) is the more defensible default. [source: EDPB adopts guidelines on processing personal data through blockchains, 2025, https://www.edpb.europa.eu/news/news/2025/edpb-adopts-guidelines-processing-personal-data-through-blockchains-and-ready_en (fetched)]
- Per-session keys on a developer laptop, rotated never, are far from the HSM-backed, annually rotated key management the 2026 design assumes; losing the keystore is "safe" for privacy but destroys the retrieval corpus, and the ADR defers this to OPS-001 without a date.
- Machine unlearning is now a regulatory expectation: 2026 analyses say deleting vectors does not touch an embedding model fine-tuned on the data, and "unlearning-ready" architectures are forecast to become required. MEM-010 has no clause for the encoder. [source: sota.io Art.17 analysis, 2026, https://sota.io/blog/eu-ai-act-gdpr-art17-right-erasure-training-data-llm-2026 (fetched)] and [source: SoK: Unlearnability and Unlearning for Model Dememorization, 2026, https://arxiv.org/pdf/2605.11592 (search)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Accept at D0 with two changes: store prompt-class ciphertext by reference in a deletable side table (ledger keeps only the pointer and skeleton), and add a clause that no model, including the local embedding model, is ever trained or fine-tuned on ledger content without a declared unlearning procedure. Replace the provisional 90-day figure with the neighbour-age measurement before any pilot.


### LRN: Learning and Adaptation

**State of the field, 2026.** LLM routing research has moved from supervised routers on preference labels to three things ADRL's LRN bucket must reckon with. First, the diagnosis: 2026 benchmarks show most routers, commercial ones included, plateau near a simple baseline because they learn average model quality rather than per-query signal, and larger datasets, stronger encoders and end-to-end fine-tuning are the levers. Second, the data model: routers now learn from partial bandit feedback online (BaRP, OrcaRouter, WISERouter with O(sqrt(T)) regret under budget constraints), and Meta-Router reframes router training as causal inference with preference-label bias as a CATE. Third, the evaluation model: the Replay Gap (Aug 2026) invalidates replay-based evaluation for agentic routing, Causal Agent Replay attributes failures by re-execution, and OPE under deterministic logging is shown to be severely biased (ICLR 2026), with logging-policy design now a research topic. Selective prediction matured into conformal risk control with impossibility bounds, group-conditional guarantees and anytime-valid deployment certificates. Model signing (OpenSSF OMS, sigstore v1.0) is the new artifact baseline.

#### ADRL-LRN-001: Evidence tiers, not "outrank"

Decision: Only T1 (verified, cause-typed, closed_final, organic) enters the objective and holdout; T2-T5 are declared weak signal; verifier precision is a T1 condition.

**FOR**
- Meta-Router (2025) states the exact dilemma: gold-standard labels are accurate but costly, preference and judge labels are cheap "yet often biased in reflecting the true quality of responses". Separating the two sources is the premise; LRN-001's tiers are that separation. [source: Meta-Router: Bridging Gold-standard and Preference-based Evaluations in Large Language Model Routing, 2025, https://arxiv.org/abs/2509.25535 (fetched)]
- Label noise is the single most damaging noise type in LLM fine-tuning, which supports spending scarce effort on tier-1 purity rather than volume. [source: Analyzing the Effect of Noise in LLM Fine-tuning, 2026, https://arxiv.org/abs/2604.12469 (fetched)]
- OpenAI's 2026 withdrawal from SWE-bench Verified (59.4% test flaws in the hard subset, verbatim solution reproduction) confirms clause 3: verified-by-tests is a tier only if the verifier's own precision is measured. [source: OpenAI Abandons SWE-Bench Verified, SiliconReport, 2026, https://www.siliconreport.com/openai-abandons-swe-bench-verified-citing-widespread-data-contamination-and-flawed-tests-6ebd9b34 (fetched)]

**AGAINST**
- Meta-Router's remedy is not exclusion of cheap labels but causal correction: treat evaluation source as treatment assignment and jointly model gold and preference data, which improved routing accuracy over either source alone. LRN-001 permits T2-T4 only as "weak or unlabeled signal", forbidding the joint-modelling route that the 2025 paper shows is the efficient use of a small gold set plus a large biased set. [source: Meta-Router, 2025, https://arxiv.org/abs/2509.25535 (fetched)]
- Confident-learning-style noise estimation (clause 2) requires per-example predicted probabilities from a model; a 2025-2026 benchmark finds in-sample gathering with average-probability aggregation and logit-margin disagreement works best, but all variants need a trained model with more than one task in its support. With a single-task T1, the noise estimator LRN-001 relies on cannot be fit. [source: Benchmarking noisy label detection methods, 2025 (revised 2026), https://arxiv.org/abs/2510.16211 (fetched)]
- The 2025-2026 answer to "not enough organic verified tasks" is automated pipelines that mine fresh, decontaminated, executable tasks at scale (21,000 in SWE-rebench; production-in-distribution in REAP with multi-run stability checks). LRN-001 puts all of that in T4 "simulator/benchmark" with no path to T1, even when the tasks come from the organisation's own repositories under REAP-style curation. [source: SWE-rebench, 2025, https://arxiv.org/abs/2505.20411 (fetched)] and [source: REAP, 2026, https://arxiv.org/abs/2604.01527 (fetched)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the tiers and the T1-only holdout, but permit a declared joint-modelling estimator (Meta-Router style) over T1 plus T3 with the bias term reported, instead of restricting lower tiers to pre-training and pseudo-labels. Add a T1b tier for tasks mined from the organisation's own repositories under REAP-style curation, distinct from public benchmarks.

#### ADRL-LRN-002: Branched pairs, plus a logged-exploration channel

Decision: Pairs are live branches from the same snapshot and turn state with identical rules and verifier, sized to a power target, complemented by logged-propensity exploration (LRN-008).

**FOR**
- The Replay Gap (Aug 2026, ~900 rollouts) is the direct evidence: swaps rewrite 61-94% of post-fork actions, only 3% of replayed states remain valid, and replay mispredicts every success-relevant outcome call. Clause 1 is what the paper recommends. [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239 (fetched)]
- IPS-style OPE "suffers from severe bias when the logging policy is fully deterministic" (ICLR 2026), which is clause 4's no-propensity statement stated as a theorem-level result. [source: Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies, 2026, https://arxiv.org/abs/2603.21485 (fetched)]
- Logging-policy design is now a research area: concentrating mass on high-reward actions reduces variance but "risks missing signal on actions the target policy may take", which is the argument for pairs in the ambiguous band plus bounded exploration. [source: Logging Policy Design for Off-Policy Evaluation, 2026, https://arxiv.org/abs/2605.15108 (fetched)]

**AGAINST**
- One branch per arm is not a pair under a stochastic policy. Causal Agent Replay re-executes forward "under the same stochastic policy" multiple times and measures the shift in the outcome distribution; measured inference determinism varies 5.8x across providers. The McNemar arithmetic in clause 3 assumes a deterministic outcome per arm and will understate the required n. [source: Causal Agent Replay, 2026, https://arxiv.org/abs/2606.08275 (fetched)] and [source: Governing Dynamic Capabilities, 2026, https://arxiv.org/abs/2603.14332 (fetched)]
- Model-based OPE for LLM agents now exists: ADWM learns a latent diffusion world model of environment responses and simulates the evaluated agent's own trajectories, avoiding both importance weights and live execution. LRN-002 names only pairs and logged exploration; a world-model channel, validated against branched ground truth, is the third instrument the 2026 literature offers and the Replay Gap explicitly asks for. [source: Autoregressive Diffusion World Models for Off-Policy Evaluation of LLM Agents, 2026, https://arxiv.org/abs/2606.05558 (fetched)]
- WISERouter reports comparable routing performance on SWE-Bench "while using substantially less exploration data" via a constrained bandit; the pair budget of 115-235 per slice may be the wrong unit if online learning can amortise exploration across slices. [source: WISERouter, 2026, https://arxiv.org/abs/2607.23765 (fetched)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the decision; change clause 1 to require k stochastic branches per arm (k set from the same-model control divergence measured first) so each pair yields an outcome distribution, and restate the power target for paired proportions with within-arm variance. Add a third evidence channel, world-model OPE validated against branches, as a declared tier.

#### ADRL-LRN-003: The target is a CATE, name it

Decision: Estimate the CATE of frontier over cheaper rungs given pre-decision features using meta-learners (X-learner default), from paired and exploration data; never train on the heuristic's decisions; never deploy a model that outputs a rung.

**FOR**
- Meta-Router independently reaches the same framing: router training is a causal-inference problem and "preference-data bias corresponds to conditional average treatment effects". [source: Meta-Router, 2025, https://arxiv.org/abs/2509.25535 (fetched)]
- A May 2026 position paper by thirteen authors argues that routing and agentic workflows are inherently causal questions, that logged data are subject to confounding and distribution shift, and that learned judges are biased, which is LRN-003's rationale restated. [source: Causal Methods for LLM Development and Evaluation, 2026, https://arxiv.org/abs/2605.25998 (fetched)]
- The Simpson's-paradox study of agent PRs shows naive outcome comparisons on observational logs reverse under controls, so refusing to train on the heuristic's own routing outcomes as targets is justified. [source: Beyond Simpson's Paradox, 2026, https://arxiv.org/abs/2606.22711 (fetched)]

**AGAINST**
- The X-learner default is dated: the Hybrid learner (2025, revised Jan 2026) shows neither direct nor indirect meta-learners dominate and an interpolating H-learner sits on the Pareto frontier across benchmarks. Clause 2 should name the H-learner or a data-driven choice, not fix X. [source: Hybrid Meta-learners for Estimating Heterogeneous Treatment Effects, 2025/2026, https://arxiv.org/abs/2506.13680 (fetched)]
- The plateau results cut against the estimator-first framing. Twenty-one routers on five benchmarks plateau because they learn global averages, and the levers are more data, stronger encoders and end-to-end fine-tuning; LLMRouterBench finds backbone embeddings barely matter and model-recall failures dominate. A CATE over a small tabular pre-decision feature vector is a plateau router by construction, and ADRL's D0 estimator has no plan for the levers. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587 (fetched)] and [source: LLMRouterBench, 2026, https://arxiv.org/abs/2601.07206 (fetched)]
- "Never deploy a model whose output is a rung" is contradicted by the strongest 2025-2026 routing results: BaRP trains a policy from partial bandit feedback that outputs the rung and beats offline routers by at least 12.46%; OrcaRouter's LinUCB policy ranked second on RouterArena. Cost-preference conditioning at inference (BaRP) achieves what clause 3 wants without separating estimator from decision. [source: Learning to Route LLMs from Bandit Feedback: One Policy, Many Trade-offs, 2025, https://arxiv.org/abs/2510.07429 (fetched)] and [source: OrcaRouter, 2026, https://arxiv.org/abs/2605.30736 (fetched)]
- Uncertainty on tau(x) has a 2025-2026 answer the ADR leaves open: conformal prediction intervals for individual treatment effects with coverage lower bounds under non-exchangeability. [source: Prediction Intervals for Individual Treatment Effects in a Multiple Decision Point Framework using Conformal Inference, 2025, https://arxiv.org/abs/2512.08828 (fetched)]

**Grounding verdict**: CONTESTED (2026).

**Recommendation**: Keep the estimand and the label-source prohibition; replace the fixed X-learner with an H-learner or a validated choice, and specify conformal ITE intervals as the uncertainty method. Soften clause 3 to "the decision layer must be able to re-weight cost without retraining" (BaRP-style preference conditioning satisfies this) and add the plateau levers (richer encoders, end-to-end fine-tuning) as the funded path if the tabular estimator plateaus.

#### ADRL-LRN-004: Pre-decision features, enforced by construction

Decision: Decision-time feature snapshot is the sole training source; retrieval features use as-of projections; temporal, session-grouped splits; versioned deny-list including served_rung.

**FOR**
- Point-in-time correct joins are the industry mechanism for exactly this: each training row takes the latest feature value at or before its label timestamp, and the documentation names future leakage as the failure being prevented. [source: Point-in-time feature joins, Databricks docs, 2026, https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series (fetched)]
- RecSys 2025 shows evaluation outcomes and model rankings change materially between leave-one-out and global temporal splits, and only global temporal splitting prevents leakage; clause 3 is the right choice. [source: Time to Split, 2025, https://arxiv.org/abs/2507.16289 (fetched)]
- The agent-PR confounder cascade (repository, commit count) is the observational-data warning behind grouping splits by session and repo. [source: Beyond Simpson's Paradox, 2026, https://arxiv.org/abs/2606.22711 (fetched)]

**AGAINST**
- Snapshot-only training forbids feature engineering after the fact: a new feature cannot be back-tested on historical decisions because only features_v<N> was persisted. Feature-store practice keeps the raw event log and recomputes as-of features with versioned transformations, which is more flexible and equally leak-free. LRN-004 should allow as-of recomputation from the ledger under the same deny-list, not only the snapshot. [source: Point-in-time feature joins, Databricks docs, 2026, https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series (fetched)]
- The plateau literature says routers need stronger encoders and end-to-end fine-tuning; if the pre-decision feature vector is frozen at decision time and the local embedding model changes (MEM-007), the snapshot becomes incomparable across time and the deny-list does not cover this drift. [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587 (fetched)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the decision; permit a second training source, as-of recomputation from the ledger under the same deny-list and MEM-007 stamps, so that new features can be evaluated historically. Add the embedding-model version to the feature schema so snapshots from different encoders are never pooled.

#### ADRL-LRN-005: Every artifact is fully versioned

Decision: Every learned artifact versions its feature schema, data snapshot, objective, calibration, thresholds and policy compatibility.

**FOR**
- 2026 MLOps guidance says every version must be traceable from training run to deployment through a registry, with audit logs and model cards generated as pipeline artifacts; LRN-005 is that rule. [source: MLOps Pipeline Automation Best Practices in 2026, MLflow, 2026, https://mlflow.org/articles/mlops-pipeline-automation-best-practices-in-2026/ (fetched)]
- Atlas (2025) shows attestable ML pipelines built from open supply-chain provenance specifications, trusted hardware and transparency logs are practical in prototype. [source: Atlas: A Framework for ML Lifecycle Provenance & Transparency, 2025, https://arxiv.org/abs/2502.19567 (fetched)]

**AGAINST**
- The field's baseline moved from "versioned" to "signed and attested": sigstore's model-signing v1.0 (April 2025) and the OpenSSF Model Signing specification bind artifacts to workload or developer identity with transparency-log inclusion proofs, and are integrated into major model hubs. LRN-005 versions the manifest but nothing signs it, so an artifact's declared lineage is not verifiable. [source: Taming the Wild West of ML: Practical Model Signing with Sigstore, 2025, https://blog.sigstore.dev/model-transparency-v1.0/ (fetched)] and [source: OpenSSF Model Signing (OMS) Specification, 2025, https://github.com/ossf/model-signing-spec (search)]
- Sample-level provenance (which ledger rows trained this artifact, with tamper-evident commitments) is now demonstrated with practical overhead; "data snapshot" as a ledger high-water mark is coarse by comparison and cannot answer "was this erased session in the training set?", which MEM-010 needs. [source: FG-Trac, 2026, https://arxiv.org/abs/2601.14971 (fetched)]
- Sigstore itself says trusted provenance for ML workflows and dataset signing are "a future step", so attestation of the data side is not yet standardised; ADRL should not wait for that, but it means the manifest, not a standard, must carry the tier mix and high-water mark. [source: sigstore model-transparency v1.0, 2025, https://blog.sigstore.dev/model-transparency-v1.0/ (fetched)]

**Grounding verdict**: DATED (mechanism; newest relevant source 2026).

**Recommendation**: Keep the text; add a follow-up to sign each artifact and its manifest with OpenSSF Model Signing so lineage claims are verifiable, and add a training-set membership commitment (Merkle root of route_ids in the training set) so MEM-010 erasure can identify affected artifacts.

#### ADRL-LRN-006: Abstention with a declared risk-coverage target

Decision: Selective prediction with a declared target risk and measured coverage on a time-ordered T1 holdout; feature-space OOD detector; system-level risk target; abstention rate bounded and reported; abstention built before the estimator.

**FOR**
- Conformal risk control for LLM outputs now comes with a feasibility check: when base risk exceeds the target, any distribution-free method must abstain on at least a closed-form fraction, and adaptive conformal inference cut risk-target violations from 71% to 21% under shift. Clause 1's "risk first, coverage falls out" is the right form. [source: When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation, 2026, https://arxiv.org/abs/2606.29054 (fetched)]
- Anytime-valid selective risk bounds for per-round deployment certification exist (e-processes on a Bonferroni grid, pathwise validity on 550+ streams), which is the deployment-side guarantee an EVL-009 abstention blocker needs across time. [source: Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs, 2026, https://arxiv.org/abs/2605.20270 (fetched)]
- A bandit framing where abstention is an action and the agent learns "when not to learn" gives sublinear regret without exploration in regions where a single action could cause irreparable harm; it matches clause 3's hand-off to the deterministic policy. [source: Learning When Not to Learn: Risk-Sensitive Abstention in Bandits with Unbounded Rewards, 2025 (AISTATS 2026), https://arxiv.org/abs/2510.14884 (fetched)]

**AGAINST**
- Marginal risk guarantees are insufficient: a model can meet the population budget while over-exposing subgroups, with violations reaching 47% under group-composition shift; hierarchical group-conditional CRC fixes this at a participation cost of 22-37 points. ADRL's subgroups are repos, intent classes and harnesses; clause 1 declares one marginal risk. [source: Hierarchical Group-Conditional Conformal Risk Control for Selective Prediction in Language Models, 2026, https://arxiv.org/abs/2607.24562 (fetched)]
- Entropy or confidence alone has a model-dependent failure mode for abstention; combining it with a correctness probe improves the risk-coverage trade-off. Clause 1 leaves the uncertainty score unspecified. [source: Entropy Alone is Insufficient for Safe Selective Prediction in LLMs, 2026, https://arxiv.org/abs/2603.21172 (fetched)]
- A May 2026 router decomposes uncertainty into reducible and irreducible parts and uses three actions: weak model when low, oracle when reducible is high, abstain when irreducible is high. LRN-006 has a two-way act/abstain gate; the three-way rule maps directly onto local, frontier and deterministic fallback and avoids paying for frontier on inherently ambiguous turns. [source: Flexible Routing via Uncertainty Decomposition, 2026, https://arxiv.org/abs/2605.07805 (fetched)]
- Multi-expert learning-to-defer now has realizable H-consistent surrogates and a training-free conformal alternative; clause 3 cites two-expert deferral, but ADRL has three rungs plus the heuristic. [source: Mastering Multiple-Expert Routing: Realizable H-Consistency and Strong Guarantees for Learning to Defer, 2025, https://arxiv.org/abs/2506.20650 (search)] and [source: No Need for Learning to Defer? A Training Free Deferral Framework to Multiple Experts through Conformal Prediction, 2025, https://arxiv.org/abs/2509.12573 (search)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Keep the decision; make the risk target group-conditional over repo and intent class (HG-CRC style) and use an anytime-valid certificate so the EVL-009 bound holds across the stream, not only on the holdout. Replace the binary gate with the reducible/irreducible three-way rule so abstention and "route up" are distinct outputs.

#### ADRL-LRN-007: No autonomous online promotion

Decision: Learning may propose updates; deployment requires offline evaluation and explicit graduation; no autonomous online promotion.

**FOR**
- 2026 MLOps guidance: "automation without gating is just faster failure"; hard gates at data validation, champion-challenger evaluation on held-out data, and a named human owner for every pipeline. [source: MLOps Pipeline Automation Best Practices in 2026, MLflow, 2026, https://mlflow.org/articles/mlops-pipeline-automation-best-practices-in-2026/ (fetched)]
- Spotify's deployed contextual bandit was validated offline and by A/B test before rollout, and its adaptation is bounded inside a graduated policy; this remains the production shape the ADR describes. [source: Calibrated Recommendations with Contextual Bandits on Spotify Homepage, 2025, https://research.atspotify.com/2025/9/calibrated-recommendations-with-contextual-bandits-on-spotify-homepage (search)] and [source: Calibrated Recommendations with Contextual Bandits, 2025, https://arxiv.org/abs/2509.05460 (search)]
- Where a single action can cause irreparable damage, the safe learner abstains rather than explores; that is the correct prior for a payments codebase. [source: Learning When Not to Learn, 2025, https://arxiv.org/abs/2510.14884 (fetched)]

**AGAINST**
- Continuous online learning is now the norm in routing research, not the exception: BaRP learns under deployment's partial-feedback restriction and beats strong offline routers by at least 12.46%; OrcaRouter initialises offline then "can optionally continue learning from bandit feedback" in production; Agent-as-a-Router accumulates execution-grounded experience during deployment for the lowest regret on coding tasks. The ADR permits exploration data collection but not the policy update loop these systems rely on. [source: Learning to Route LLMs from Bandit Feedback, 2025, https://arxiv.org/abs/2510.07429 (fetched)], [source: OrcaRouter: A Production-Oriented LLM Router with Hybrid Offline-Online Learning, 2026, https://arxiv.org/abs/2605.30736 (fetched)], [source: Agent-as-a-Router, 2026, https://arxiv.org/abs/2606.22902 (fetched)]
- Constrained contextual bandits now carry end-to-end regret bounds covering exploration and exploitation under a shared budget (O(sqrt(T)) for WISERouter; high-probability budget and latency satisfaction for COPAC-UCB). "No autonomous promotion" forgoes guarantees that are formally stronger than a monthly human review. [source: WISERouter, 2026, https://arxiv.org/abs/2607.23765 (fetched)] and [source: Online LLM Selection via Constrained Bandits with Time-Varying Demand, 2026, https://arxiv.org/html/2606.17489 (search)]
- The offline evaluation the ADR requires is itself unreliable for agentic routing (Replay Gap), and the world-model OPE alternative is new and unvalidated at ADRL's scale; "offline evaluation then graduate" may be a gate that certifies the wrong world. [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239 (fetched)]

**Grounding verdict**: CONTESTED (2026).

**Recommendation**: Keep the rule for now, since every 2026 online-routing result is measured on benchmarks with cheap verified rewards that ADRL lacks. Add a sunset condition: when T1 volume and verifier precision pass the EVL gate, a bounded-parameter online update (LinUCB-style, inside a graduated feature schema, with a regret budget) is a permitted artifact class that graduates once, not per update.

#### ADRL-LRN-008: Logged exploration in the ambiguous band

Decision: Inside the ambiguous band, among SAF-permitted rungs, a graduated exploration rule randomises the rung with bounded probability and logs the propensity; exploration turns are their own tier; DR estimators are validated against branched pairs.

**FOR**
- IPS estimators "suffer from severe bias when the logging policy is fully deterministic" (ICLR 2026); logging propensities is the precondition the paper states. [source: Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies, 2026, https://arxiv.org/abs/2603.21485 (fetched)]
- Logging-policy design is now treated as an optimisation with practical design principles when the target policy is unknown or partially known; a versioned exploration artifact with a declared epsilon is that design made explicit. [source: Logging Policy Design for Off-Policy Evaluation, 2026, https://arxiv.org/abs/2605.15108 (fetched)]
- Constrained bandit routers achieve comparable performance "while using substantially less exploration data" than supervised routers, so bounded exploration is the cheaper route to labels than full pairs. [source: WISERouter, 2026, https://arxiv.org/abs/2607.23765 (fetched)]

**AGAINST**
- The ICLR 2026 result also shows an alternative: exploit intrinsic stochasticity in the environment (there, user clicks) to get low-bias OPE without randomising the logging policy. ADRL's analogue is the sampling stochasticity of the models and the escalation path; whether that yields usable propensities has not been examined, and it would avoid degrading developer turns on purpose. [source: Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies, 2026, https://arxiv.org/abs/2603.21485 (fetched)]
- Surrogate rewards (a reward model's noisy estimate) can be combined with true rewards in a correlation-aware bandit with regret bounds that degrade gracefully when the surrogate is wrong; LRN-008's tier separation forbids blending surrogates with explored outcomes, which is the mechanism that would make small epsilon informative. [source: Correlation-Aware Contextual Bandits with Surrogate Rewards for LLM Routing, 2026, https://arxiv.org/abs/2607.09015 (fetched)]
- The risk-sensitive bandit literature argues that in settings where one action can do irreparable harm, the right policy is to establish a trusted region and never explore outside it. Downward exploration (local where the heuristic said frontier) on payments code is exactly that setting; clause 2's "downward epsilon can be set lower" should be "downward exploration only inside a verified trusted region". [source: Learning When Not to Learn, 2025, https://arxiv.org/abs/2510.14884 (fetched)]
- Doubly-robust methods "partially mitigate bias but do not resolve the fundamental difficulties of long-horizon distribution shift in high-dimensional text spaces"; validating DR against branched pairs (clause 4) is necessary but the pair count needed to validate is the same count the exploration channel was meant to avoid. [source: Autoregressive Diffusion World Models for OPE of LLM Agents, 2026, https://arxiv.org/abs/2606.05558 (fetched)]

**Grounding verdict**: CURRENT (2026).

**Recommendation**: Accept at D0 with two edits: restrict downward exploration to a trusted region defined by prior verified local successes (not just the ambiguous band), and add a follow-up to test whether model sampling stochasticity plus escalation outcomes yield usable propensities before any developer turn is randomised. Permit a declared surrogate-reward blend inside the explore tier under the correlation-aware estimator.


### EVL: Evaluation, Graduation, Rollout

**State of the field, 2026.** The EVL bucket is the most research-aligned bucket in the register, largely because it was written on 2026-09-03 with the Replay Gap paper and the review's power arithmetic in hand. Its central commitments, live branches over replay, exclusions before metrics, blockers outside the score, and human graduation on named evidence, each have direct 2026 support. The gaps are of two kinds. First, the bucket imports the routing literature's own weakest habit: EVL-001's "best single model repriced over the window" is a comparator selected on the evaluation data, which the selection-validity work shows inflates every paired claim. Second, three decisions were written before the field's newest distinction landed: static routers plateau, trajectory-conditioned routers do not, and shadow mode cannot evaluate a router because the shadow decision never executes. EVL-004 counts labels when what is scarce is discordance; EVL-007's D3 rung certifies a decision that has never been served; EVL-006 omits runs, seeds, harness and serving configuration that the harness-variance papers show dominate model choice. All nine remain sound in direction.

#### ADRL-EVL-001: Baseline set: four fixed comparators, two price bases

Decision: every evaluation reports against always-local, always-frontier, the current heuristic and the best single cloud model repriced over the window, at after-cache and list prices, as a versioned artifact.

**FOR**

A fixed comparator set is exactly what independent benchmarking says is missing: commercial routers "fail to reliably outperform a simple baseline" when a unified comparator is imposed [source: LLMRouterBench, 2026, https://arxiv.org/abs/2601.07206, fetched]. The two price bases match provider reality, with cache reads at 0.1x or 0.025x and writes at 1.25x to 2x [source: Anthropic pricing docs, 2026, https://platform.claude.com/docs/en/about-claude/pricing, fetched]. Vendors now route at cache boundaries because switching costs more than it gains [source: About Copilot auto model selection, 2026, https://docs.github.com/copilot/concepts/auto-model-selection, fetched], so charging the switch, as attack 3 answers, is current practice. Azure's own guidance tells buyers to "compare model router with your current baseline" before trusting managed routing [source: Microsoft Learn model router concepts, 2026, https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router, fetched].

**AGAINST**

Comparator 3 is chosen on the same window it is evaluated on. "Testing against a best fixed model selected on the same examples invalidates paired inference", and a full-information oracle "sees outcomes no deployable router observes"; with selection-valid intervals the realisable share of the oracle gap is 7.5 to 14.4 percent and the simultaneous interval for eleven policies has lower limit zero [source: Opportunity Is Not Realizability, 2026, https://arxiv.org/abs/2608.08265, fetched]. The decision's attack 2 addresses the counterfactual problem but not the selection problem. Separately, the comparator set has no trajectory-conditioned baseline; a cheap-model-then-escalate policy is the strongest deployable competitor in 2026 [source: SWE-Router, 2026, https://arxiv.org/abs/2607.00053, fetched], and a scout-plus-cheapest-fixer ablation matched the best single model at a fifth of the cost with no router at all [source: Scrouting, 2026, https://arxiv.org/abs/2608.04804, fetched]. "Beats both bounds" is therefore necessary but weak.

**Grounding verdict**: CONTESTED. Newest source 2026.

**Recommendation**: Amend: comparator 3 is selected on the previous window (or pre-registered) and re-priced on the evaluation window; report a selection-valid interval when it is not. Add a fifth comparator, "always-local with mechanical escalation at the CAS trip-wires", so the learned artifact is measured against the best deployable non-learned policy, not just the bounds.

#### ADRL-EVL-002: Holdout and calibration protocol: temporal, session-grouped, tier-1 only

Decision: metrics come from a later-in-time, session-grouped, tier-1 holdout with session-bootstrap intervals, reliability diagrams and abstention coverage, and report "insufficient" below a declared minimum.

**FOR**

Paired designs on the same items are the recommended discipline, with clustered standard errors and power analysis up front [source: Adding Error Bars to Evals, 2024, https://arxiv.org/abs/2411.00640, fetched]; the paired McNemar required N is a median 2.15x smaller than unpaired formulas, and 11 of 40 leaderboard comparisons are unresolved at conventional power [source: Resolution Diagnostics for Paired LLM Evaluation, 2026, https://arxiv.org/abs/2605.30315, fetched]. Time-ordered holdouts are the standard answer to leakage, and "no passive backtest can separate" skill from recency, so naming harness and model versions per window (attack 2) is the right mitigation [source: Temporal Leakage in LLM Backtesting, 2026, https://arxiv.org/abs/2608.02985, fetched]. Label error at the few-percent level reverses rankings, which justifies tier-1 only [source: Pervasive Label Errors, 2021, https://arxiv.org/abs/2103.14749, search-only, as cited in MEM-009].

**AGAINST**

Session-level bootstrap with a handful of sessions is itself unreliable: CLT and resampling intervals "dramatically underestimate uncertainty" below a few hundred datapoints, and the recommended fallback is Bayesian [source: Position: Don't Use the CLT in LLM Evals, ICML 2025, https://arxiv.org/abs/2503.01747, fetched]. With 34 evaluated decisions and one verified task, a reliability diagram with any bin count is noise, and ECE on that sample is a number without meaning. A temporal split also does not guarantee absence of leakage, because temporal signals are format-dependent [source: Test of Time, ACL 2026, https://arxiv.org/abs/2509.00072, fetched]. The decision fixes `min_holdout_sessions` but not the minimum number of clusters for the bootstrap or the resolution ratio N/N* that would say whether a comparison could ever be resolved.

**Grounding verdict**: CURRENT. Newest source 2026.

**Recommendation**: Add a minimum cluster count for bootstrap intervals and a Bayesian interval below it; report the resolution ratio q = N/N* for every pairwise comparison next to the interval; defer reliability diagrams until discordant-pair count passes a pre-registered floor.

#### ADRL-EVL-003: Branch protocol and replay prohibition

Decision: counterfactual evidence comes only from live branches from a shared snapshot; replay or model substitution in stored transcripts is prohibited as evidence; off-policy estimates are admissible only after branch validation.

**FOR**

The cited study now reads in full: across about 900 rollouts, swaps exceeded control floors by 0.25 to 0.66 normalised edit distance, 74 to 77 percent of early swaps diverged at the first post-fork action against 6 to 35 percent for controls, only 3 percent of replayed states remained valid, and five outcome flips appeared in swap arms against zero in 359 control forks [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239, fetched]. Independent work reached the same design: TwinRouterBench added a live dynamic track because static prefix scoring does not settle whether a cheaper substitution keeps downstream completion [source: TwinRouterBench, 2026, https://arxiv.org/abs/2605.18859, fetched]. The harness itself is a larger source of variance than model choice, with ranking reversals by harness configuration, so any replay that fixes the harness to the logged one is scoring the wrong system [source: Stop Comparing LLM Agents Without Disclosing the Harness, 2026, https://arxiv.org/abs/2605.23950, fetched].

**AGAINST**

The load-bearing paper is a single-author preprint with six paired runs, and its own caveat matters for ADRL: "temperature-0 determinism is configuration-dependent", with FP8-served controls diverging on 90 percent of forks while AWQ-served ones held [source: The Replay Gap, 2026, https://arxiv.org/abs/2608.08239, fetched]. The noise floor is therefore a property of the serving stack, and a local rung on quantised MLX or llama.cpp will have a different floor from a cloud rung; the decision requires "a same-model control" but not one per serving configuration. The field also still trains from logged trajectories with reported gains [source: MTRouter, ACL 2026, https://arxiv.org/abs/2604.23530, fetched], so a blanket prohibition must be careful to forbid replay as evidence without forbidding logs as training input; the text does this, but the golden test on `source=replay` rows could over-reject.

**Grounding verdict**: CURRENT. Newest source 2026.

**Recommendation**: Require the same-model control floor per serving configuration (model, precision, runtime) and record it on the branch study; keep the prohibition; state explicitly that logged trajectories may feed features and training but never an outcome label.

#### ADRL-EVL-004: Label quantity and quality gate for retrieval and learned authority

Decision: retrieval and learned components gain advisory authority only after pre-registered quantity, verifier-precision, representativeness and suppressed-fraction conditions are met.

**FOR**

Reliable ranking needs tasks with intermediate success rates: filtering to 30 to 70 percent historical success cut evaluation size 44 to 70 percent while preserving rank fidelity, and random sampling was unstable across seeds [source: Efficient Benchmarking of AI Agents, 2026, https://arxiv.org/abs/2603.23749, fetched]. That supports the representativeness clause and the answer to attack 2. Verifier precision as a precondition is supported by the retirement of SWE-bench Verified after 59.4 percent of 138 audited hard tasks proved flawed [source: SWE-bench Verified Retired, Pebblous summary of OpenAI, 2026, https://blog.pebblous.ai/blog/swe-bench-verified-retired/en/, fetched; OpenAI post, https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/, search-only].

**AGAINST**

The gate counts labels; what routing needs is discordance. Routers plateau because they "mainly learn global averaged model-performance trends rather than fine-grained query-specific routing signals" [source: The Routing Plateau, 2026, https://arxiv.org/abs/2606.07587, fetched]. Three hundred `task_capability` outcomes on which every rung agrees carry no routing information, and the paired test's power depends on discordant pairs, roughly 40 to 50 at n = 400 for 80 percent power [source: Eval Set Sizing, 2026, https://dev.to/gabrielanhaia/eval-set-sizing-the-statistical-power-math-behind-llm-ab-tests-4gpc, search-only; Resolution Diagnostics, 2026, fetched]. The four conditions never mention the ambiguous-band share or a minimum number of pairs where rungs disagree, so the gate can pass on a corpus that is uninformative for the estimand LRN-003 names.

**Grounding verdict**: CONTESTED. Newest source 2026.

**Recommendation**: Add a fifth condition: a pre-registered minimum count of verified pairs on which the rungs' outcomes differ, per slice, derived from the RTG-007 power target; report the ambiguous-band share next to `min_labels`.

#### ADRL-EVL-005: Simulator and benchmark evidence is not organic evidence

Decision: simulator, benchmark and synthetic evidence is a separate family, tier T4, reported separately, and may qualify mechanisms or bound claims but never establish reliability on the organisation's code.

**FOR**

The benchmark that anchored coding-agent claims was retired by its own author for contamination and flawed tests, with all major frontier models showing signs of training on solutions [source: SWE-bench Verified Retired, 2026, https://blog.pebblous.ai/blog/swe-bench-verified-retired/en/, fetched]. Terminal-Bench 2.1 had to repair 28 of 89 tasks for broken dependencies, tight budgets and instruction-test mismatch, and introduced continuous validation [source: Terminal-Bench 2.1 leaderboard, 2026, https://snorkel.ai/leaderboard/terminal-bench-2-1/, fetched]. Simulators lie in specific ways: reward-relevant perturbations cost about 40 points and transition perturbations about 30, and scale did not close the gap [source: When Simulation Lies, 2026, https://arxiv.org/abs/2605.11928, fetched]; a unified MDP view names observation, action, transition and reward gaps [source: The Sim-to-Real Gap of Foundation Model Agents, 2026, https://arxiv.org/abs/2606.07017, fetched]. Benchmarks conflate model and harness and grade against one reference solution [source: Position: Coding Benchmarks Are Misaligned, 2026, https://arxiv.org/abs/2606.17799, fetched].

**AGAINST**

Contamination-resistant benchmarks now exist: SWE-bench Pro's private set draws on 18 proprietary codebases that trainers cannot legally access [source: SWE-bench Pro leaderboard, Scale, 2026, https://labs.scale.com/leaderboard/swe_bench_pro_private, search-only]. A private-repository benchmark run through the organisation's own harness is arguably closer to organic than the register's single-user corpus, and domain randomisation shows synthetic evidence can transfer to unseen failure classes [source: When Simulation Lies, 2026, fetched]. The decision's "never admit" is stricter than the field's practice and stricter than needed; the real defect is that the decision does not require harness-version and benchmark-version disclosure on any benchmark number, although harness effects exceed model effects [source: Stop Comparing LLM Agents Without Disclosing the Harness, 2026, fetched].

**Grounding verdict**: CURRENT. Newest source 2026.

**Recommendation**: Keep the family separation; require every synthetic figure to carry benchmark version, harness version and run count; allow a benchmark run through ADRL's own harness on a private task set to serve as a bound that can prune rungs and to size the organic pilot, still never as admission.

#### ADRL-EVL-006: Offline evaluation against baselines, branched or propensity-weighted

Decision: before graduation, an artifact receives a six-item report (baseline version, holdout protocol, branch-only counterfactuals, excluded and tier mix, minimum realised gain, manifest hash) and an incomplete report cannot be presented.

**FOR**

Evaluation reporting is moving from prose cards to composed, machine-readable records tying benchmark metadata, run data and model metadata, with reproducibility, completeness, provenance and comparability signals, applied at scale to 101,843 results [source: Evaluation Cards, 2026, https://arxiv.org/abs/2606.09809, fetched]. STREAM's reporting template for model reports pushes the same direction [source: STREAM, 2025, https://arxiv.org/abs/2508.09853, fetched]. Hashing the report into the manifest is the versioned-artifact practice model cards are moving toward.

**AGAINST**

The six items omit what the 2026 variance work says dominates: run count and seeds, harness version, and serving configuration. Absolute scores degrade under scaffold shift while rank order survives [source: Efficient Benchmarking of AI Agents, 2026, https://arxiv.org/abs/2603.23749, fetched], so the report must say whether it claims a rank or a magnitude. Item 1 inherits EVL-001's selection problem. The word "offline" still invites replay even with EVL-003 in place; TwinRouterBench's vocabulary of static and dynamic tracks is cleaner [source: TwinRouterBench, 2026, fetched]. The lightweight path for parameter-only changes has no independent support and is the kind of shortcut the harness papers warn about.

**Grounding verdict**: CURRENT. Newest source 2026.

**Recommendation**: Add items 7 to 9: run count and seeds with per-run spread; harness and serving configuration per rung; the claim type (rank versus magnitude) and its resolution ratio. Rename to "pre-exposure evaluation report" and give it a machine-readable header in the Evaluation Cards style.

#### ADRL-EVL-007: Explicit human graduation and the D2 to D5 ladder

Decision: maturity moves one rung at a time on named evidence by a recorded human decision, artifacts need a signature from a key outside the training team, and a new implementation inherits nothing above D2.

**FOR**

Canarying with a concurrent control, a dozen stack-ranked metrics and explicit limits on what canaries detect is the reference discipline [source: Google SRE, Canarying Releases, https://sre.google/workbook/canarying-releases/, fetched]. Progressive delivery with shadow, 1 percent canary, consistent user assignment and automated rollback thresholds is 2026 practice for LLM releases [source: Releasing AI Features Without Breaking Production, 2026, https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing, fetched]. Safety cases are moving to continuously updated forms tied to performance indicators rather than one-time gates [source: Dynamic safety cases for frontier AI, 2024, https://arxiv.org/abs/2412.17618, fetched]. The "no inheritance" rule matches the identity-stable canary principle that "the agent you certified is still the agent you have" [source: ICAN-Deploy, 2026, https://arxiv.org/abs/2605.28097, fetched].

**AGAINST**

D3 as written certifies a router on evidence that cannot exist. A shadow router records a decision but never executes it, so the shadow window measures decision distribution and gate behaviour, not outcome; the Replay Gap result means a shadow decision's counterfactual outcome is unknown until branched [source: The Replay Gap, 2026, fetched]. Canaries "cannot reliably detect state-dependent regressions" or shared-infrastructure failures [source: Google SRE, fetched], which for a router means a pilot with no concurrent control and no declared guardrail metrics is a before-and-after comparison, the design SRE warns against. Microsoft's platform makes ship decisions on pre-defined guardrail metrics, not a single score [source: A/B Testing Infrastructure Changes at Microsoft ExP, 2024, https://www.microsoft.com/en-us/research/articles/a-b-testing-infrastructure-changes-at-microsoft-exp/, fetched]; the D4 rung names a population but no control, duration or guardrails. One reviewer from a different reporting line is a weaker bar than any 2026 lab framework [source: Frontier Model Safety Analysis, 2026, https://futureagi.com/blog/frontier-model-safety-analysis-2026/, search-only].

**Grounding verdict**: CONTESTED. Newest source 2026.

**Recommendation**: Rewrite D3 evidence as "decision distribution, gate behaviour and plumbing on organic traffic, plus branch studies at the LRN-002 budget"; rewrite D4 as a controlled pilot with a concurrent control population, consistent assignment by session lineage, pre-declared guardrail metrics and a minimum duration in the EVL config.

#### ADRL-EVL-008: Scorecard format: every number with its denominator, window and exclusions

Decision: one fixed-structure scorecard per window with identity, denominators, exclusions-first, organic metrics with intervals, synthetic section, pairs, open blockers and ladder positions.

**FOR**

The field's diagnosis is that results are "reported inconsistently across leaderboards, model cards, benchmark papers, and company blogs" so that omissions cannot be seen, and the answer is a composed, machine-readable record [source: Evaluation Cards, 2026, https://arxiv.org/abs/2606.09809, fetched]. Vendors are going the other way: Cursor hides the routed model by default [source: Cursor Router changelog, 2026, fetched] and Kiro users cannot see which model answered [source: Kiro issue #8903, search-only], so a scorecard with served-rung denominators is a differentiator. Exclusions-first implements the register's denominator rule and matches the "disclose the harness" position [source: Stop Comparing LLM Agents Without Disclosing the Harness, 2026, fetched].

**AGAINST**

Section 1 names harness and model versions but not serving configuration, and precision and runtime change agent determinism [source: The Replay Gap, 2026, fetched]; a scorecard cannot compare two windows if the local rung silently moved from Q6 to Q4. Section 4 reports intervals but not the resolution ratio that says whether a difference could be detected at all [source: Resolution Diagnostics, 2026, fetched]. The scorecard is defined as a document; the Evaluation Cards work shows the value comes from a schema that tools can ingest and compare.

**Grounding verdict**: CURRENT. Newest source 2026.

**Recommendation**: Add serving configuration per rung to section 1 and the resolution ratio to section 4; publish the scorecard as JSON with a rendered view; add a "routed model visibility" line so the layer's transparency is itself measured.

#### ADRL-EVL-009: Blockers are never averaged away

Decision: eight pre-registered named conditions hold a decision at its rung regardless of score, are listed in every scorecard, and change only by config version with a reason.

**FOR**

Guardrail metrics that decide ship or no-ship independent of the headline metric are the established experimentation discipline [source: A/B Testing Infrastructure Changes at Microsoft ExP, 2024, fetched]. Compliance-first gating, where a regulatory violation fails the gate regardless of other dimensions, is 2026 agent-evaluation practice, with ISO 42001 and NIST AI RMF now embedded as gates in regulated sectors [source: LLM Evaluation in 2026, https://medium.com/@nairmilind3/llm-evaluation-in-2026-e631a78c67dc, search-only]. Frontier frameworks define capability thresholds that pause deployment until safeguards exist [source: Frontier Model Safety Analysis, 2026, search-only]. Blocker 2 is vindicated by the benchmark whose verifier turned out to be 59 percent wrong on hard tasks [source: SWE-bench Verified Retired, 2026, fetched].

**AGAINST**

Two blockers the literature would add are missing: a harness, model or serving-configuration change inside the window (the temporal confound EVL-002 only "splits" on) and a benchmark or harness disclosure gap for any synthetic figure. Dynamic safety cases pair each claim with a monitored indicator and a revision cadence rather than a static list [source: Dynamic safety cases, 2024, fetched]; the eight blockers have no re-check cadence, so a closed blocker stays closed until someone reopens it. Blocker 6 depends on OPS thresholds that do not exist, so it is currently unevaluable rather than open or closed, a third state the decision does not name.

**Grounding verdict**: CURRENT. Newest source 2026.

**Recommendation**: Add blockers 9 (version or serving-config change inside the window) and 10 (synthetic figure without harness and benchmark version); give each blocker a re-check cadence and an "unevaluable" state that is reported as open.


### OPS: Platform, Runtime, Operations

**State of the field, 2026.** Operations practice for AI gateways converged on three things the register partly anticipates. Observability standardised on OpenTelemetry's `gen_ai.*` conventions, which remain in Development status: `gen_ai.provider.name` is Required and `gen_ai.response.model` only Recommended, and LiteLLM's deployment headers are absent on streamed responses. Key custody moved from long-lived KMS keys with annual rotation to identity-bound keyless signing and witnessed transparency logs (Rekor v2 GA October 2025), and NIST SP 800-88 Rev. 2 (September 2025) formalised cryptographic erase while warning it is not assured where keys are backed up or escrowed. Sandboxing guidance from Anthropic now treats the per-command sandbox as insufficient for unattended runs, and 175,000 exposed Ollama hosts showed that "local" is a network property, not a label. Shadow-mode and SLO practice still rest on the Google SRE books; the new lesson from CVE-2025-66479 is that rate-based SLIs cannot see a control that is silently off.

#### ADRL-OPS-001: Multi-worker consistency and the single-process constraint

Decision: one ADRL process per host until every gate- or pin-affecting state item is port-backed; SQLite single-writer contract; startup lock; versioned state inventory.

**FOR**
- The SQLite contract named (WAL, `busy_timeout`, `BEGIN IMMEDIATE`) matches current practice: "if you run transactions without using BEGIN IMMEDIATE, you might hit SQLITE_BUSY regardless of your timeout setting", and timeouts below five seconds "led to occasional 'database is locked' errors" [source: SQLite concurrent writes and "database is locked" errors, tenthousandmeters, https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/ (search title); SQLite in Practice (1), DOCSAID, https://docsaid.org/en/blog/sqlite-wal-busy-timeout-for-workers/ (search title)].
- The online backup API the sibling decision relies on works with a live single writer: "the source database does not need to be locked for the duration of the copy" [source: SQLite Online Backup API, https://www.sqlite.org/backup.html (fetched)].
- Declaring an inventory of process-local state is the same discipline Fowler recommends for toggles: keep decision points separate and "manage toggle configuration via source control" so what was active is auditable [source: Feature Toggles, Martin Fowler, https://martinfowler.com/articles/feature-toggles.html (fetched)].

**AGAINST**
- The constraint is stricter than SQLite practice warrants: multi-process writers are routine with WAL, `BEGIN IMMEDIATE` and a five-second `busy_timeout`, and app-level locking is advised only "if you have a lot of concurrent writers" [source: tenthousandmeters, SQLite concurrent writes (search title)]. The real blocker is the in-memory pin cache, which the decision admits; the SQLite clause is not load-bearing.
- "One process per host" is ambiguous once verification or the harness runs in a VM or container, which Anthropic now recommends for untrusted repositories; a lock file inside a VM does not prevent a second proxy on the laptop, and vice versa [source: Choose a sandbox environment, Claude Code docs, 2026 (fetched)].
- The backup API restarts when another process writes: "If another thread or process writes to the source database while this function is sleeping, then SQLite detects this and usually restarts the backup process", so a second (read-mostly) process that also writes telemetry will stall backups the decision does not mention [source: SQLite Online Backup API (fetched)].

**Grounding verdict**: CURRENT (newest source 2025).

**Recommendation**: Keep the lock and inventory; drop the implication that SQLite is a reason for single-process. Define "host" as the isolation boundary the proxy shares with the harness (laptop, VM or container) and require the lock to live inside that boundary.

#### ADRL-OPS-002: Key custody and rotation

Decision: four key classes with named custodians; manifest and checkpoint keys separated in hardware or managed KMS with annual rotation; dev keys refused by default; a separate signer process.

**FOR**
- Separating the audit-trail signer from the signed party is exactly the transparency-log model: Rekor v2 "folds witnessing into the log" so the log operator alone cannot vouch for itself [source: Rekor v2 GA, Sigstore blog, 2025 (fetched); Can I Get A Witness, transparency.dev (fetched)].
- Per-session keys destroyed on erasure are the NIST-endorsed pattern: SP 800-88 Rev. 2 (26 September 2025) expands guidance on cryptographic erase and recommends zeroisation of target keys [source: NIST SP 800-88 Rev. 2, 2025, https://csrc.nist.gov/pubs/sp/800/88/r2/final (search title)].
- Refusing committed development keys addresses a real class: the Claude Code CVE chain shows credential-helper config values executed with `shell: true`, so anything under a developer-writable config path is in scope [source: Three CVEs in Claude Code CLI, Phoenix Security, 2026 (fetched)].

**AGAINST**
- Long-lived KMS keys with annual rotation is the pre-2024 pattern; the 2026 baseline for attestations is keyless: Fulcio issues "short-lived certificates binding an ephemeral key to an OpenID Connect identity", "eliminating the 'lost private key' scenario", and SLSA level 2+ treats signed provenance as baseline [source: Sigstore Keyless Signing and Cosign Verification, systemshardening.com, https://www.systemshardening.com/articles/cicd/sigstore-keyless-signing/ (search title); Verifying Software Integrity with Sigstore: The 2026 Cheat Sheet, https://techbytes.app/posts/software-integrity-sigstore-cosign-rekor-cheat-sheet/ (search title)].
- The KMS audit trail is weaker than the decision assumes: CloudTrail does not log "the original message digest or the resulting signature" for KMS sign calls, so "signed by security's key" is not independently verifiable after the fact without a transparency log [source: AWS re:Post, CloudTrail and KMS signing (search title)].
- Session keys "wrapped by a host master key" and backed up (OPS-004) conflict with NIST: CE "should not be considered an assured method of sanitization on [media] that have been escrowed or have a backup, unless the organization is confident about storage and management of the encryption keys outside of the [media]" [source: NIST SP 800-88 Rev. 2 (search title); What is Cryptographic Erase as per NIST SP 800-88 Rev.2, BitRaser, https://www.bitraser.com/blog/cryptographic-erase-and-supported-devices/ (search title)].

**Grounding verdict**: DATED (newest source 2026).

**Recommendation**: Replace "hardware or managed KMS, annual rotation" for the manifest and checkpoint keys with identity-bound keyless signing recorded in a private Rekor v2 instance, keeping a KMS key only as the offline root. Add the NIST CE caveat to the key inventory: the session-key wrapping key must have a sanitisation policy that covers its backups.

#### ADRL-OPS-003: Endpoint inventory, rollout and change control

Decision: signed endpoint inventory with trust zone, geography and data-use profile; LiteLLM config generated only from it; `local` must be `on_host` on loopback or a Unix socket; served identity matched against it.

**FOR**
- The evidence that "local" must be enforced, not labelled, is overwhelming: 175,000 Ollama hosts exposed, "roughly 23,000 remaining persistently online", with LLMjacking campaigns "systematically scanning the internet for exposed Ollama instances, vLLM servers, and OpenAI-compatible APIs running without authentication" [source: The Hacker News, 175,000 Ollama servers, 2026 (fetched); Exposed Ollama Servers, Security Boulevard, 2026, https://securityboulevard.com/2026/03/exposed-ollama-servers-security-risks-of-publicly-accessible-llm-infrastructure/ (search title)].
- The gateway can name the deployment it used: LiteLLM returns `x-litellm-model-id`, `x-litellm-model-group` and `x-litellm-model-api-base`, and "the headers above still name the deployment that answered" even for auto-routed aliases [source: Response Headers, LiteLLM docs, https://docs.litellm.ai/docs/proxy/response_headers (fetched)].
- Geography as an inventory attribute matches how Bedrock exposes it (geographic vs global profiles) and how it is evidenced (`inferenceRegion` in CloudTrail) [source: AWS Bedrock cross-region inference docs (fetched)].

**AGAINST**
- Loopback plus `on_host` is not a trust zone when the host runs unconstrained processes: Anthropic's docs state "MCP servers and hooks are separate processes that run unconstrained on the host", and the MCP spec advises local servers to "Use the `stdio` transport to limit access to just the MCP client" or "Require an authorization token" on HTTP. An unauthenticated loopback model endpoint is reachable by every MCP server and hook the developer installed [source: Choose a sandbox environment (fetched); MCP Security Best Practices, spec 2026-07-28, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices (fetched)].
- The inventory's "geography" is a class, not a place, for cloud entries: geographic profiles route "within the geography" to a region Bedrock selects; the inventory can assert "EU", not a region, and the ledger must take the region from the provider's own record [source: AWS Bedrock cross-region inference docs (fetched)].
- The served identity the inventory is matched against is unreliable on streams: the `x-litellm-model-api-base` header "is absent" on chunked responses, and a LiteLLM bug reports the body `model` field returning "model group alias instead of resolved deployment model" [source: Response header missing on streamed responses, LiteLLM issue 7249, https://github.com/BerriAI/litellm/issues/7249 (search title); response body model returns alias, LiteLLM issue 22709, https://github.com/BerriAI/litellm/issues/22709 (search title)].

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Add "authenticated" as a required attribute of every `on_host` entry (bearer token or Unix socket with file-mode restriction), because loopback without auth is reachable by unconstrained MCP servers and hooks. Make the CI check assert the served-identity header is present on a streamed test response before the inventory match is trusted.

#### ADRL-OPS-004: Backup, restore and erasure

Decision: SQLite online backups with the writer paused; keystore backed up separately; erasure by key deletion with a field-level inventory; restore replays events and verifies the egress chain.

**FOR**
- Cryptographic erase is now the standard's preferred mechanism: SP 800-88 Rev. 2 (September 2025) "expands guidance on cryptographic erase" and prescribes zeroisation of the target keys [source: NIST SP 800-88 Rev. 2, 2025 (search title); NIST 800 88 Rev.2 Guidelines, BitRaser (search title)].
- The vector-store precedent is direct: Ghost Vectors proposes "Epoch Key Rotation" that "encrypts vectors and discards the key upon deletion", completing deletion of 500 vectors in about 2.5 ms and producing "cryptographic proof of deletion via ECDSA signatures", reducing PII recovery to 0% [source: Ghost Vectors, 2026 (fetched)].
- The backup mechanism is sound: the online backup API copies incrementally and "the source database does not need to be locked for the duration of the copy" [source: SQLite Online Backup API (fetched)].

**AGAINST**
- The decision backs up the keystore, and NIST says that breaks the assurance: CE is not assured "on [media] that have been escrowed or have a backup, unless the organization is confident about storage and management of the encryption keys outside" it, and documentation must address "how these potential sources from which the key can be recovered have been addressed". Clause 2's replay of `erased` events after restore is a process control on top of a compromised guarantee, not CE [source: NIST SP 800-88 Rev. 2 (search title)].
- The NumPy in-memory index and any HNSW file are soft-delete stores by construction; deletion "marks records as deleted without actually removing the underlying embedding data from disk", so "move embeddings under session keys" must mean encrypt-at-rest per epoch, not delete rows [source: Ghost Vectors, 2026 (fetched)].
- Deletion must extend to every layer including backups under the GDPR reading the decision implicitly targets, and a keyed hash "reveals nothing without the key" only while the rotatable host key is retained read-only "for the evidence horizon", which is the escrow NIST warns about [source: NIST 800-88 guide, GoWorkwize, https://www.goworkwize.com/blog/what-is-nist-800-88-guide (search title); OPS-002 as written].

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: State explicitly that keystore backups are themselves under a sanitisation policy and that the host key's read-only retention is a documented CE exception, per SP 800-88 Rev. 2. Adopt epoch-keyed encryption for embeddings with a signed deletion receipt, which the Ghost Vectors work makes cheap.

#### ADRL-OPS-005: Shadow-mode semantics per subsystem

Decision: gates `enforce`/`observe`, routing `off`/`shadow`/`live`, fallback `off`/`shadow`/`live`; observe writes to a shadow namespace with no authority; mode changes are versioned and ledgered.

**FOR**
- The core rule (observation must not affect the control) is the SRE canary principle: "bad behavior of the canary deployment can also negatively impact the control", including via "two consecutive requests sent by a single client" where the first response alters the second request [source: Canarying Releases, Google SRE Workbook, https://sre.google/workbook/canarying-releases/ (fetched)].
- Versioned, ledgered mode changes follow the toggle literature: "Managing toggle configuration via source control and re-deployments is preferable" for auditability of what was active [source: Feature Toggles, Martin Fowler (fetched)].
- The separate-namespace pattern is what the largest secret scanner does for its AI tier: AI-detected generic secrets "are surfaced as alerts ... in a separate list from regular secret scanning alerts" [source: Responsible detection of generic secrets, GitHub Docs (fetched)].

**AGAINST**
- "Shadow findings on live traffic are the labelled corpus" is a biased corpus: observe mode is only permitted on traffic "whose policy already permits cloud", so the precision measurement excludes exactly the restricted repositories where the detectors matter most, and the SRE guidance warns that canary metrics must be "clearly attributable to the change we are canarying, and ... not be influenced by external factors" [source: Canarying Releases, SRE Workbook (fetched)].
- Fowler distinguishes short-lived release toggles ("not stick around much longer than a week or two") from long-lived ops toggles; the decision's `observe` mode is a release toggle for a new detector but is specified like a permanent ops mode, with no expiry, so a detector can sit in observe indefinitely while its findings accrue [source: Feature Toggles, Martin Fowler (fetched)].
- A shadow namespace still stores span hashes and locating features for a lineage the authoritative namespace never pinned; under NeuroTaint's cross-session persistence finding, that store is a taint carrier with no suppression rule attached [source: Ghost in the Agent, 2026 (fetched)].

**Grounding verdict**: CURRENT (newest source 2026).

**Recommendation**: Give every `observe` entry an expiry and an owner, as a release toggle. State that shadow-namespace findings are prompt-class data under MEM-005 with the same retention as pinned lineages, and record the corpus bias (cloud-permitted traffic only) in the SAF-003 precision report.

#### ADRL-OPS-006: Record the served identity, not the intended one

Decision: record deployment id, model, provider, trust zone and geography that actually served each response, with a `served_source` of `gateway_reported`, `proxy_observed` or `assumed_intended`; `assumed_intended` share is a blocker metric.

**FOR**
- The attribute names now have a standard: OpenTelemetry defines `gen_ai.provider.name` (Required) as "the Generative AI provider as identified by the client or server instrumentation" and `gen_ai.response.model` (Recommended) as "the name of the model that generated the response" [source: GenAI spans, OpenTelemetry semantic-conventions-genai, https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md (fetched)].
- The gateway can report it: LiteLLM's `x-litellm-model-id` and `x-litellm-model-api-base` "name the deployment that answered" [source: Response Headers, LiteLLM docs (fetched)].
- For cloud geography the provider keeps an authoritative record: CloudTrail's `additionalEventData.inferenceRegion` identifies "where requests were processed" [source: AWS Bedrock cross-region inference docs (fetched)].

**AGAINST**
- The primary source fails on the dominant traffic: LiteLLM's `x-litellm-model-api-base` "is absent" on chunked (streamed) responses, and Claude Code requires streaming ("if your gateway buffers complete responses before relaying them, Claude Code stalls"). `gateway_reported` will be missing on almost every inference response unless the gateway is changed [source: LiteLLM issue 7249 (search title); Gateway protocol reference, Claude Code docs (fetched)].
- The secondary source is also unreliable: a LiteLLM bug reports the body `model` field returning the "model group alias instead of resolved deployment model", so `message_start.model` can name the group, not the deployment, and `proxy_observed` becomes `assumed_intended` in disguise [source: LiteLLM issue 22709 (search title)].
- The conventions the contract would pin to are "in Development status", their "attribute names have shifted recently, and most SDKs in the wild still emit the older variants" [source: GenAI spans, OpenTelemetry (fetched); OpenTelemetry GenAI Semantic Conventions, DEV Community, https://dev.to/x4nent/opentelemetry-genai-semantic-conventions-the-standard-for-llm-observability-1o2a (search title)].
- Geography is a class for cloud entries: a geographic profile's region is selected at run time, so `served_geography` derived from the inventory is an assertion, and only the provider log is evidence [source: AWS Bedrock cross-region inference docs (fetched)].

**Grounding verdict**: CONTESTED (newest source 2026): principle current, evidence path broken on streamed traffic.

**Recommendation**: Require the gateway contract (RTG-008) to emit deployment id in a trailer or in-band metadata on streamed responses, and set `return_raw_model_name` as a second channel; until then treat every streamed row as `assumed_intended` and expect the blocker to hold. Add a periodic reconciliation of served geography against the provider's own log (CloudTrail `inferenceRegion` or equivalent).

#### ADRL-OPS-007: Audit-anchor availability, rollback and incident response

Decision: automatic checkpoints signed by a separate signer and shipped to an append-only sink with receipts; `unanchored` windows are blockers; one-step rollback exercised before D4; five runbooks.

**FOR**
- The anchor shape is the transparency-log shape and the tooling is mature: Rekor v2 is "cheaper to run, simpler to maintain", tile-based, sharded by year, with Tessera backends for AWS, MySQL and POSIX [source: Rekor v2 GA, Sigstore blog, 2025 (fetched); Rekor v2 alpha, Sigstore blog, https://blog.sigstore.dev/rekor-v2-alpha/ (search title)].
- Exercising rollback before exposure and reviewing runbooks at graduation is standard SRE practice; the SLO chapter's error-budget policy ("production freeze halts certain changes until budget recovery") is the enforcement mechanism the runbooks need [source: Implementing SLOs, Google SRE Workbook, https://sre.google/workbook/implementing-slos/ (fetched)].
- Freezing routing to `off` while gates stay enforced is consistent with the harness contract: `off` forwards to the harness-requested model, which Claude Code handles without any change on its side [source: Gateway protocol reference (fetched)].

**AGAINST**
- A sink with receipts is not a witness. "A witness cosigns checkpoints consistent with those it previously signed" only "after verifying the consistency proof"; an S3 object-lock bucket or a telemetry endpoint stores whatever it is sent and cannot detect a split view. The decision's "append-only anchor sink" needs at least one cosigning witness outside the gateway team [source: Can I Get A Witness (Network)?, transparency.dev (fetched)].
- The proposed Q7 sink (the gateway's telemetry path) is operated by the party one runbook investigates ("served identity outside the inventory ... notify the gateway team"); an anchor held by a suspect is not an anchor for that incident [source: OPS-003 and OPS-007 as written; witness rationale above].
- KMS-based signing leaves no digest in the provider's audit trail, so "signer signs and ships" is unverifiable from CloudTrail alone [source: AWS re:Post, CloudTrail and KMS signing (search title)].
- The runbook for "pinned lineage reached a cloud rung" depends on served identity, which OPS-006 shows is `assumed_intended` on streamed traffic today; the runbook's trigger may never fire [source: LiteLLM issue 7249 (search title)].

**Grounding verdict**: CURRENT (newest source 2025 for the anchor design, 2026 for the runbook dependencies).

**Recommendation**: Name the sink as a witnessed log (private Rekor v2 or Tessera) with one witness outside both the ADRL and gateway teams, and record witness cosignatures as the receipt. Make OPS-006's streamed-identity fix a prerequisite of the "pinned lineage reached cloud" runbook.

#### ADRL-OPS-008: Fail-open SLOs, alerting and bypass audit

Decision: per-class fail-open SLIs with pre-registered thresholds; alerts to a named owner recorded in the egress ledger; audited operator bypass with duration bound.

**FOR**
- Pre-registering thresholds before data exists is what the SRE Workbook advises: "your current performance can be a good place to start", round to manageable figures, and "don't let current performance limit you as you refine your SLO" [source: Implementing SLOs, Google SRE Workbook (fetched)].
- Recording alerts in the ledger so "the audit trail shows when the operator knew" aligns with Article 12's purpose of "identifying situations that may result in the high-risk AI system presenting a risk" [source: Article 12, EU AI Act explorer (fetched)].
- The metrics vocabulary exists: `gen_ai.client.operation.duration` and `gen_ai.client.token.usage` are defined, and gateway instrumentation guides cover "how fallback shows up in the trace tree" [source: Inside the LLM Call: GenAI Observability with OpenTelemetry, OpenTelemetry blog, 2026, https://opentelemetry.io/blog/2026/genai-observability/ (fetched); OpenTelemetry for LLMs: Instrumentation Guide for a Multi-Provider AI Gateway, TrueFoundry, https://www.truefoundry.com/blog/opentelemetry-llm-gateway-instrumentation (search title)].

**AGAINST**
- Rate-based SLIs cannot see a control that is silently off. CVE-2025-66479 made a deny-all network setting behave as allow-all for five weeks, and "a team running [the vulnerable configuration] in production ... had no way to know the sandbox was effectively off". A gate that never runs produces zero fail-open events and a perfect SLO [source: Anthropic Silently Patches Claude Code Sandbox Bypass, SecurityWeek, 2026 (fetched)].
- The error-budget framing is for availability, where "100% reliability is the wrong target"; applied to `gate_path` fail-open on unpinned lineages it defines an accepted leak budget, and the SRE text's own enforcement ("production freeze") is the right response to a confidentiality SLI breach, which the decision does not require [source: Implementing SLOs, SRE Workbook (fetched)].
- The bypass audit is a self-report: FND-004's one-step bypass is repointing `ANTHROPIC_BASE_URL`, and the harness sends "nonessential background traffic outside the gateway path" plus direct calls for fast mode and WebFetch checks, so a bypass window's egress is only partly observable from ADRL [source: Connect Claude Code to an LLM gateway (fetched); Gateway protocol reference (fetched)].
- Alerting "to the named on-call owner" who "may be the developer" removes the independence the SRE model assumes between the party breaching the budget and the party enforcing the policy ("if all three parties do not agree to enforce the error budget policy, you need to iterate") [source: Implementing SLOs, SRE Workbook (fetched)].

**Grounding verdict**: CURRENT (newest source 2026), with a coverage gap for silent-off failures.

**Recommendation**: Add a synthetic-probe SLI: a known secret-bearing request injected on a schedule that must produce a pin and a ledger row, so a gate that is silently off breaches within one probe interval. Require an error-budget policy with a freeze action for `gate_path` on unpinned lineages, and route that alert to someone other than the developer whose session triggered it.

## 5. What the critique could not find

- No peer-reviewed local-versus-cloud study of coding agents on private repositories. The closest evidence is the Replay Gap's note that FP8-served controls diverged on 90 percent of forks while AWQ-served ones did not, and a June 2026 feasibility review that judged local agentic coding workload-dependent without testing real repositories.
- No 2025 or 2026 cross-tool precision comparison of secret detectors; the only such study is from 2023, so the register's 25 to 75 percent precision figures are directionally right but dated.
- No direct literature on pre-registering engineering readiness thresholds; FND-005 is graded CURRENT by analogy with frontier safety frameworks and progressive-delivery practice, both of which are self-assessed.
- No measured result on how much unlogged traffic under a fail-open memory facade biases a routing corpus; MEM-006 is grounded in engineering practice only.
- No published mechanism for who signs a route receipt; the concept exists (May 2026) and no vendor gateway documents a per-response deployment identifier.
- No vendor documentation for a served-endpoint header on streamed LiteLLM responses; the absence is documented only in open issues.
- No independent confirmation of the claim that the MCP 2026-07-28 release candidate removes session identifiers; it came from a search snippet and is marked as such.
- Two pages returned 403: OpenAI's SWE-bench Verified retirement post (figures taken from secondary reporting, which disagrees on the announcement month) and the NSA MCP security sheet.
- The loop-detection parameters in one terminal-coding-agents paper appeared only in a search snippet and the fetched page truncated that section, so they are not relied on.

## 6. Sources

315 distinct URLs, grouped by host. Marked fetched or search-only.

### advisories.gitlab.com

- CVE-2026-55607 advisory (GitLab), 2026 (fetched). https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2026-55607/

### agent-safehouse.dev

- OpenAI Codex CLI Sandbox Analysis Report (Agent Safehouse), 2026 (fetched). https://agent-safehouse.dev/docs/agent-investigations/codex

### ai.google.dev

- Google, Gemma 4 model card, 2026 (fetched). https://ai.google.dev/gemma/docs/core/model_card_4

### api-docs.deepseek.com

- DeepSeek, V4 Preview Release, 2026-04-24 (fetched). https://api-docs.deepseek.com/news/news260424/

### artificialintelligenceact.eu

- Article 12: Record-Keeping (EU AI Act explorer) (fetched). https://artificialintelligenceact.eu/article/12/

### arxiv.org

- "AGENTSERVESIM: A Hardware-aware Simulator for Multi-Turn LLM Agent Serving" (arXiv 2606.09613, 2026) (search-only). https://arxiv.org/pdf/2606.09613
- "CobSeg: Coherence Boundary Modeling for Dialogue Topic Segmentation" (arXiv 2605.30668, May 2026) (search-only). https://arxiv.org/abs/2605.30668
- "Ethical Hyper-Velocity (EHV): A Hardware-Rooted Zero-Trust Runtime Enforcement Architecture for Agentic AI Systems" (arXiv 2605.17909, 2026) (fetched). https://arxiv.org/pdf/2605.17909
- "RLM-Cascade: Response-Level Speculative Decoding for Cost-Efficient LLM API Serving" (arXiv 2606.22840, 2026) (search-only). https://arxiv.org/html/2606.22840
- "S3C2 Summit 2025-07: Government Secure Supply Chain Summit" (arXiv 2605.29140) (fetched). https://arxiv.org/pdf/2605.29140
- A Comparative Study of Software Secrets Reporting by Secret Detection Tools, 2023 (search-only). https://arxiv.org/abs/2307.00714
- A. Ghosh et al., Evaluation Cards, 2026 (fetched). https://arxiv.org/abs/2606.09809
- A. Kotawala, Resolution Diagnostics for Paired LLM Evaluation, 2026 (fetched). https://arxiv.org/abs/2605.30315
- Adaptive LLM Routing under Budget Constraints (PILOT), 2025 (fetched). https://arxiv.org/html/2508.21141v1
- Adoption and Impact of Command-Line AI Coding Agents (Microsoft, 2026) (fetched). https://arxiv.org/abs/2607.01418
- Agent Contracts: A Formal Framework for Resource-Bounded Autonomous AI Systems, 2026 (fetched). https://arxiv.org/html/2601.08815v3
- Agent Data Injection Attacks are Realistic Threats to AI Agents, 2026 (fetched). https://arxiv.org/html/2607.05120v1
- Agent-as-a-Router: Agentic Model Routing for Coding Tasks, 2026 (fetched). https://arxiv.org/abs/2606.22902
- Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents (2026) (fetched). https://arxiv.org/abs/2606.30306
- Analyzing the Effect of Noise in LLM Fine-tuning (2026) (fetched). https://arxiv.org/abs/2604.12469
- Arch-Router: Aligning LLM Routing with Human Preferences, 2025 (search-only). https://arxiv.org/abs/2506.16655
- Are Coding Agents Generating Over-Mocked Tests? An Empirical Study (2026) (fetched). https://arxiv.org/abs/2602.00409
- Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents, 2026 (fetched). https://arxiv.org/abs/2603.07915
- Asad and Arko, "Kettle: Attested builds for verifiable software provenance" (arXiv 2605.08363, May 2026) (fetched). https://arxiv.org/abs/2605.08363
- Atlas: A Framework for ML Lifecycle Provenance & Transparency (2025) (fetched). https://arxiv.org/abs/2502.19567
- ATOM: Instantiating Budget-Controllable Multi-Agent Collaboration via Nucleus-Electron Hierarchy, 2026 (fetched). https://arxiv.org/abs/2605.26178
- Autoregressive Diffusion World Models for Off-Policy Evaluation of LLM Agents (2026) (fetched). https://arxiv.org/abs/2606.05558
- BAGEN: Are LLM Agents Budget-Aware?, 2026 (fetched). https://arxiv.org/abs/2606.00198
- BeamClean: Language Aware Embedding Reconstruction (2025) (fetched). https://arxiv.org/abs/2505.13758
- Benchmarking noisy label detection methods (2025, revised 2026) (fetched). https://arxiv.org/abs/2510.16211
- Beyond Simpson's Paradox: A Cascade of Confounders in AI Agent Pull-Request Co-Authorship (2026) (fetched). https://arxiv.org/abs/2606.22711
- Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in LLM Agents (2026) (fetched). https://arxiv.org/abs/2607.05775
- Budgeted Act-or-Defer Multi-Agent LLM Deliberation with Local Reliability Bounds, 2026 (fetched). https://arxiv.org/abs/2606.29654
- Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned, 2026, (fetched, but the loop-detection section was truncated in the fetch; the fingerprint details in the search snippet are not relied on) (fetched). https://arxiv.org/html/2603.05344v1
- C. Cârlan et al., Dynamic safety cases for frontier AI, 2024 (fetched). https://arxiv.org/abs/2412.17618
- C. Northcutt et al., Pervasive Label Errors in Test Sets, NeurIPS 2021 (search-only). https://arxiv.org/abs/2103.14749
- C3PO: Optimized Large Language Model Cascades with Probabilistic Cost Constraints for Reasoning, 2025 (fetched). https://arxiv.org/abs/2511.07396
- CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents, 2026 (fetched). https://arxiv.org/abs/2606.16824
- Calibrated Recommendations with Contextual Bandits (2025) (fetched). https://arxiv.org/abs/2509.05460
- Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures (2026) (fetched). https://arxiv.org/abs/2606.08275
- Causal Methods for LLM Development and Evaluation (2026) (fetched). https://arxiv.org/abs/2605.25998
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2503.13657, 2025) (fetched). https://arxiv.org/abs/2503.13657
- chmalbach, "Model Routing as a Trust Problem: Route Receipts for Adaptive AI Systems" (arXiv 2605.01710, May 2026) (fetched). https://arxiv.org/abs/2605.01710
- Coen, "When F1 Fails: Granularity-Aware Evaluation for Dialogue Topic Segmentation" (arXiv 2512.17083, December 2025) (fetched). https://arxiv.org/abs/2512.17083
- Concept-Aware Privacy Mechanisms for Defending Embedding Inversion Attacks (SPARSE) (2026) (fetched). https://arxiv.org/abs/2602.07090
- Confident and Wrong: Silent Semantic Failures in Coding Agents, 2026 (fetched). https://arxiv.org/abs/2603.25764
- Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs (2026) (fetched). https://arxiv.org/abs/2605.20270
- Conformal Selective Prediction with General Risk Control (SCoRE) (2026) (fetched). https://arxiv.org/abs/2603.24704
- Correlation-Aware Contextual Bandits with Surrogate Rewards for LLM Routing (2026) (fetched). https://arxiv.org/abs/2607.09015
- Costa and Köpf, "Securing AI Agents with Information-Flow Control" (FIDES; arXiv 2505.23643; SaTML 2026), (background only; not cited in a bullet) (search-only). https://arxiv.org/abs/2505.23643
- DART: Draft-Agreement Routing for Training-Free Adaptive Thinking Budgets in Hybrid Reasoning Models, 2026 (fetched). https://arxiv.org/abs/2606.23181
- Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL; arXiv 2503.18813, 2025), (background only; not cited in a bullet) (search-only). https://arxiv.org/abs/2503.18813
- Defeating Prompt Injections by Design (CaMeL), 2025 (fetched). https://arxiv.org/pdf/2503.18813
- Defense Against Indirect Prompt Injection via Tool Result Parsing, 2026 (fetched). https://arxiv.org/abs/2601.04795
- Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey (TMLR 2026), F (consulted for the LRN field summary) (fetched). https://arxiv.org/abs/2603.04445
- Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey, 2026 (search-only). https://arxiv.org/html/2603.04445v2
- E. Miller, Adding Error Bars to Evals, 2024 (fetched). https://arxiv.org/abs/2411.00640
- Early-Stage Prediction of Review Effort in AI-Generated Pull Requests (MSR 2026) (fetched). https://arxiv.org/html/2601.00753
- EcoAgent-Bench: Evaluating Economic Decision-Making in Budget-Constrained LLM Agents, 2026 (fetched). https://arxiv.org/html/2608.05519
- ecret Breach Detection in Source Code with Large Language Models, 2025 (fetched). https://arxiv.org/abs/2504.18784
- ecret Leak Detection in Software Issue Reports using LLMs (MSR 2026) (fetched). https://arxiv.org/abs/2410.23657
- Entropy Alone is Insufficient for Safe Selective Prediction in LLMs (2026) (fetched). https://arxiv.org/abs/2603.21172
- F. Ndzomga, Efficient Benchmarking of AI Agents, 2026 (fetched). https://arxiv.org/abs/2603.23749
- From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents, 2026 (fetched). https://arxiv.org/abs/2606.09863
- Ghost in the Agent: Redefining Information Flow Tracking for LLM Agents (NeuroTaint), 2026 (fetched). https://arxiv.org/abs/2604.23374
- Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases (2026) (fetched). https://arxiv.org/abs/2606.18497
- Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases, 2026 (fetched). https://arxiv.org/pdf/2606.18497
- GLiNER2-PII, 2026 (fetched). https://arxiv.org/abs/2605.09973
- Governed Reasoning for Institutional AI (2026) (fetched). https://arxiv.org/pdf/2604.10658
- Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use (2026) (fetched). https://arxiv.org/abs/2603.14332
- Hierarchical Group-Conditional Conformal Risk Control for Selective Prediction in Language Models (2026) (fetched). https://arxiv.org/abs/2607.24562
- How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions (2026) (fetched). https://arxiv.org/abs/2605.29442
- Hybrid Meta-learners for Estimating Heterogeneous Treatment Effects (2025, revised 2026) (fetched). https://arxiv.org/abs/2506.13680
- I. Bhola et al., Scrouting, 2026 (fetched). https://arxiv.org/abs/2608.04804
- I. F. Shihab et al., Opportunity Is Not Realizability: Selection-Valid Diagnostics for Multi-LLM Routing, 2026 (fetched). https://arxiv.org/abs/2608.08265
- iddiqui et al., "Permissive Information-Flow Analysis for Large Language Models" (arXiv 2410.03055, v3 January 2026) (fetched). https://arxiv.org/abs/2410.03055
- ine-Grained Traceability for Transparent ML Pipelines (FG-Trac) (2026) (fetched). https://arxiv.org/abs/2601.14971
- Jiang et al., "ChainCaps: Composition-Safe Tool-Using Agents via Monotonic Capability Attenuation" (arXiv 2605.26542, May-July 2026) (fetched). https://arxiv.org/abs/2605.26542
- Jing et al., "Isolation as a First-Class Principle for LLM-Agent System Safety" (arXiv 2607.12406, July-September 2026) (fetched). https://arxiv.org/abs/2607.12406
- Kravchenko et al., "APPA: Recoverable Information-Flow Control for Real-World LLM Agents" (arXiv 2607.24625, July-August 2026) (fetched). https://arxiv.org/abs/2607.24625
- Lean4Agent: Formal Modeling and Verification for Agent Workflow and Trajectory (2026) (fetched). https://arxiv.org/abs/2606.06523
- Learning to Route LLMs from Bandit Feedback: One Policy, Many Trade-offs (BaRP) (2025) (fetched). https://arxiv.org/abs/2510.07429
- Learning When Not to Learn: Risk-Sensitive Abstention in Bandits with Unbounded Rewards (AISTATS 2026) (fetched). https://arxiv.org/abs/2510.14884
- lexible Routing via Uncertainty Decomposition (2026) (fetched). https://arxiv.org/abs/2605.07805
- LiveVectorLake: A Real-Time Versioned Knowledge Base Architecture for Streaming Vector Updates and Temporal Retrieval (2025) (fetched). https://arxiv.org/abs/2601.05270
- LLM Query Scheduling with Prefix Reuse and Latency Constraints (k-LPM), 2025 (fetched). https://arxiv.org/abs/2502.04677
- LLMRouter: Unified Infrastructure, 2026 (search-only). https://arxiv.org/abs/2608.06867
- LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing, 2026 (fetched). https://arxiv.org/abs/2601.07206
- Logging Policy Design for Off-Policy Evaluation (2026) (fetched). https://arxiv.org/abs/2605.15108
- M. Gorinova et al., Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering, 2026 (fetched). https://arxiv.org/abs/2606.17799
- M. Merrill et al., Terminal-Bench, 2026 (fetched). https://arxiv.org/abs/2601.11868
- macrOData: New Benchmarks of Thousands of Datasets for Tabular Outlier Detection (KDD 2026), F (consulted for LRN-006 OOD; abstract gives no method ranking, so not cited in a bullet) (fetched). https://arxiv.org/abs/2602.09329
- Mahmood, "Routing, Cascades, and User Choice for LLMs" (arXiv 2602.09902, February 2026) (fetched). https://arxiv.org/abs/2602.09902
- Mastering Multiple-Expert Routing: Realizable H-Consistency and Strong Guarantees for Learning to Defer (2025) (fetched). https://arxiv.org/abs/2506.20650
- McCaslin et al., STREAM (ChemBio), 2025 (fetched). https://arxiv.org/abs/2508.09853
- MCP-38: A Comprehensive Threat Taxonomy for Model Context Protocol Systems, 2026 (search-only). https://arxiv.org/pdf/2603.18063
- Meta-Router: Bridging Gold-standard and Preference-based Evaluations in LLM Routing (2025) (fetched). https://arxiv.org/abs/2509.25535
- Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures (2026) (fetched). https://arxiv.org/abs/2607.28802
- Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction (WWW 2026) (fetched). https://arxiv.org/abs/2601.19965
- MTRouter: Cost-Aware Multi-Turn LLM Routing with History-Model Joint Embeddings, 2026 (fetched). https://arxiv.org/html/2604.23530v1
- Muruaga, "Bounded Agents: Delegation Security for Multi-Agent AI Systems" (arXiv 2608.15888, August 2026) (fetched). https://arxiv.org/abs/2608.15888
- Narisetty et al., "Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents" (arXiv 2606.26479, June 2026) (fetched). https://arxiv.org/abs/2606.26479
- No Need for Learning to Defer? A Training Free Deferral Framework to Multiple Experts through Conformal Prediction (2025) (fetched). https://arxiv.org/abs/2509.12573
- Not All Turns Are Equally Hard: Adaptive Thinking Budgets For Efficient Multi-Turn Reasoning, 2026 (fetched). https://arxiv.org/abs/2604.05164
- Off-Policy Evaluation for Ranking Policies under Deterministic Logging Policies (ICLR 2026) (fetched). https://arxiv.org/abs/2603.21485
- oK: Unlearnability and Unlearning for Model Dememorization (2026) (fetched). https://arxiv.org/pdf/2605.11592
- ollow the TRACE: Exploiting Post-Click Trajectories for Online Delayed Conversion Rate Prediction (2026) (fetched). https://arxiv.org/abs/2604.23197
- On the Flakiness of LLM-Generated Tests for Industrial and Open-Source Database Management Systems (2026) (fetched). https://arxiv.org/abs/2601.08998
- On Time, Within Budget: Constraint-Driven Online Resource Allocation for Agentic Workflows, 2026 (fetched). https://arxiv.org/abs/2605.06110
- Online LLM Selection via Constrained Bandits with Time-Varying Demand (2026) (fetched). https://arxiv.org/html/2606.17489
- OrcaRouter: A Production-Oriented LLM Router with Hybrid Offline-Online Learning (2026) (fetched). https://arxiv.org/abs/2605.30736
- PIIBench, 2026 (fetched). https://arxiv.org/abs/2604.15776
- Prakash, "AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A" (arXiv 2603.24775, March 2026) (fetched). https://arxiv.org/abs/2603.24775
- Prediction Intervals for Individual Treatment Effects in a Multiple Decision Point Framework using Conformal Inference (2025) (fetched). https://arxiv.org/abs/2512.08828
- QueryIPI: Query-agnostic Indirect Prompt Injection on Coding Agents, 2026 (fetched). https://arxiv.org/abs/2510.23675
- R. Raj et al., TRACE-Router, 2026 (fetched). https://arxiv.org/abs/2607.22465
- REAP: Automatic Curation of Coding Agent Benchmarks from Interactive Production Usage (ASE 2026) (fetched). https://arxiv.org/abs/2604.01527
- Reasoning Is Not Free: Robust Adaptive Cost-Efficient Routing for LLM-as-a-Judge, 2026 (search-only). https://arxiv.org/abs/2605.10805
- Rethinking Tamper-Evident Logging: A High-Performance, Co-Designed Auditing System, 2025 (search-only). https://arxiv.org/pdf/2509.03821
- rom Zero to Hero: Advancing Zero-Shot Foundation Models for Tabular Outlier Detection (2026), F (consulted for LRN-006 OOD; not cited in a bullet) (fetched). https://arxiv.org/abs/2602.03018
- S. Bowyer et al., Position: Don't Use the CLT in LLM Evals, ICML 2025 (fetched). https://arxiv.org/abs/2503.01747
- SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks, 2026 (fetched). https://arxiv.org/abs/2607.00053
- T. J. Zhang et al., Test of Time, ACL 2026 (fetched). https://arxiv.org/abs/2509.00072
- Tallam, "Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure" (arXiv 2605.05440, May 2026) (fetched). https://arxiv.org/abs/2605.05440
- Testing with AI Agents: An Empirical Study of Test Generation Frequency, Quality, and Coverage (MSR 2026) (fetched). https://arxiv.org/abs/2603.13724
- The Diminishing Returns of Early-Exit Decoding in Modern LLMs, 2026 (fetched). https://arxiv.org/abs/2603.23701
- The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents, 2026 (fetched). https://arxiv.org/abs/2608.24358
- The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break (2026) (fetched). https://arxiv.org/html/2604.11978v1
- The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World, 2026 (fetched). https://arxiv.org/abs/2608.08239
- The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers, 2026 (fetched). https://arxiv.org/abs/2606.07587
- Time to Split: Exploring Data Splitting Strategies for Offline Evaluation of Sequential Recommenders (RecSys 2025) (fetched). https://arxiv.org/abs/2507.16289
- Towards a Science of AI Agent Reliability, 2026 (fetched). https://arxiv.org/abs/2602.16666
- TRACE-Router: Task-Consistent and Adaptive Online Routing for Agentic AI, 2026 (fetched). https://arxiv.org/html/2607.22465v2
- TraceLab: Characterizing Coding Agent Workloads for LLM Serving, 2026 (fetched). https://arxiv.org/abs/2606.30560
- TRAIL: Trace Reasoning and Agentic Issue Localization, 2025 (search-only). https://arxiv.org/abs/2505.08638
- TwinRouterBench: Fast Static and Live Dynamic Evaluation for Realistic Agentic LLM Routing, 2026 (fetched). https://arxiv.org/abs/2605.18859
- UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing, 2026 (fetched). https://arxiv.org/abs/2605.18796
- Uncertainty-Guided LLM Semantic Augmentation for Heterogeneous Treatment Effect Estimation (CURL) (2026), F (consulted for LRN-003; not cited in a bullet) (fetched). https://arxiv.org/abs/2607.26599
- Universal Model Routing for Efficient LLM Inference (UniRoute), 2025 (fetched). https://arxiv.org/abs/2502.08773
- WE-rebench (NeurIPS 2025) (fetched). https://arxiv.org/abs/2505.20411
- What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents (TraceProbe), 2026 (fetched). https://arxiv.org/pdf/2607.06184
- When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents, 2026 (fetched). https://arxiv.org/abs/2607.01641
- When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation (2026) (fetched). https://arxiv.org/abs/2606.29054
- When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime, 2026 (fetched). https://arxiv.org/abs/2606.14589
- When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents (ToolMaze), 2026 (fetched). https://arxiv.org/abs/2606.05806
- Where LLM Agents Fail and How They can Learn From Failures (AgentErrorTaxonomy), 2025 (fetched). https://arxiv.org/abs/2509.25370
- Who&When Pro: Can LLMs Really Attribute Failures in AI Agents? (2026) (fetched). https://arxiv.org/abs/2607.09996
- WISERouter: LLM Routing with Workload Budget Constraint (2026) (fetched). https://arxiv.org/abs/2607.23765
- X. Liu et al., The Sim-to-Real Gap of Foundation Model Agents, 2026 (fetched). https://arxiv.org/abs/2606.07017
- X. Qin et al., ICAN-Deploy, 2026 (fetched). https://arxiv.org/abs/2605.28097
- X. Zhou et al., When Simulation Lies, 2026 (fetched). https://arxiv.org/abs/2605.11928
- Y. Zhang et al., MTRouter, ACL 2026 (fetched). https://arxiv.org/abs/2604.23530
- Y. Zhang et al., Stop Comparing LLM Agents Without Disclosing the Harness, 2026 (fetched). https://arxiv.org/abs/2605.23950
- Z. Zhang, B. Stadie, Temporal Leakage in LLM Backtesting, 2026 (fetched). https://arxiv.org/abs/2608.02985
- Zero2Text: Zero-Training Cross-Domain Inversion Attacks on Textual Embeddings (2026) (fetched). https://arxiv.org/abs/2602.01757

### atul4u.medium.com

- Tokenizer Comparison, Part 2 (Medium) (search-only). https://atul4u.medium.com/tokenizer-comparison-part2-comprehensive-tokenizer-performance-analysis-a8e0613bed0d

### aws.amazon.com

- AWS Machine Learning Blog, "Unlocking AI flexibility in Europe: A guide to cross-region inference for EU data processing and model access" (June 2026) (fetched). https://aws.amazon.com/blogs/machine-learning/unlocking-ai-flexibility-in-europe-a-guide-to-cross-region-inference-for-eu-data-processing-and-model-access/

### bitraser.com

- What is Cryptographic Erase as per NIST SP 800-88 Rev.2 (BitRaser) (search-only). https://www.bitraser.com/blog/cryptographic-erase-and-supported-devices/

### blog.gitguardian.com

- The State of Secrets Sprawl 2026 (GitGuardian) (search-only). https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/

### blog.modelcontextprotocol.io

- Tool Annotations as Risk Vocabulary (MCP blog), 2026 (fetched). https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/

### blog.pebblous.ai

- Pebblous, SWE-bench Verified Retired, 2026 (fetched). https://blog.pebblous.ai/blog/swe-bench-verified-retired/en/

### blog.sigstore.dev

- igstore blog, "Rekor v2 GA - Cheaper to run, simpler to maintain" (October 2025) (fetched). https://blog.sigstore.dev/rekor-v2-ga/
- Rekor v2 alpha (Sigstore blog) (fetched). https://blog.sigstore.dev/rekor-v2-alpha/
- Taming the Wild West of ML: Practical Model Signing with Sigstore (model-transparency v1.0) (2025) (fetched). https://blog.sigstore.dev/model-transparency-v1.0/

### blog.transparency.dev

- transparency.dev, "Can I Get A Witness (Network)?" (fetched). https://blog.transparency.dev/can-i-get-a-witness-network

### braindetox.kr

- braindetox, Agentic Coding With Local LLMs, 2026 (fetched). https://braindetox.kr/en/posts/local_llm_agentic_coding_2026.html

### c2sp.org

- C2SP, "The Static Certificate Transparency API" v1.1.0 (search-only). https://c2sp.org/static-ct-api@v1.1.0

### code.claude.com

- Anthropic, "Claude apps gateway" (Claude Code docs, 2026) (fetched). https://code.claude.com/docs/en/claude-apps-gateway
- Anthropic, "Create custom subagents" (Claude Code docs, 2026) (fetched). https://code.claude.com/docs/en/sub-agents
- Anthropic, "Gateway protocol reference" (Claude Code docs, 2026) (fetched). https://code.claude.com/docs/en/llm-gateway-protocol
- Choose a sandbox environment (Claude Code docs), 2026 (fetched). https://code.claude.com/docs/en/sandbox-environments
- Claude Code Docs, Zero data retention, 2026 (fetched). https://code.claude.com/docs/en/zero-data-retention
- Claude Code errors reference (Claude Code docs), 2026 (fetched). https://code.claude.com/docs/en/errors
- Configure the sandboxed Bash tool (Claude Code docs), 2026 (fetched). https://code.claude.com/docs/en/sandboxing
- Connect Claude Code to an LLM gateway (Claude Code docs), 2026 (fetched). https://code.claude.com/docs/en/llm-gateway-connect

### codesota.com

- Is SWE-bench Verified Contaminated? OpenAI Shifts to SWE-bench Pro, CodeSOTA (2026) (fetched). https://www.codesota.com/news/swe-bench-contamination-debate

### codex.danielvaughan.com

- Daniel Vaughan, "Codex CLI Custom Model Providers: The Complete Configuration Guide" (April 2026) (search-only). https://codex.danielvaughan.com/2026/04/23/codex-cli-custom-model-providers-configuration-guide/

### csrc.nist.gov

- NIST SP 800-88 Rev. 2, Guidelines for Media Sanitization, 2025 (search-only). https://csrc.nist.gov/pubs/sp/800/88/r2/final

### cursor.com

- Cursor, Cursor Router changelog, 2026-07-22 (fetched). https://cursor.com/changelog/router

### deepinspect.ai

- LLM fallback routing: the retry chain that survives provider outages without leaking policy (DeepInspect), 2026 (fetched). https://www.deepinspect.ai/blog/llm-fallback-routing

### deepmind.google

- Google DeepMind, "Google DeepMind strengthens the Frontier Safety Framework" (April 2026) (search-only). https://deepmind.google/blog/strengthening-our-frontier-safety-framework/

### designgurus.io

- DesignGurus, "How do you do progressive delivery (flags + canaries) safely?" (search-only). https://www.designgurus.io/answers/detail/how-do-you-do-progressive-delivery-flags-canaries-safely

### dev.to

- Eval Set Sizing: The Statistical Power Math Behind LLM A/B Tests, 2026 (fetched). https://dev.to/gabrielanhaia/eval-set-sizing-the-statistical-power-math-behind-llm-ab-tests-4gpc
- OpenTelemetry GenAI Semantic Conventions (DEV Community) (fetched). https://dev.to/x4nent/opentelemetry-genai-semantic-conventions-the-standard-for-llm-observability-1o2a
- OpenTelemetry's GenAI semantic conventions are NOT stable yet (2026) (fetched). https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke

### developer.konghq.com

- Kong, AI Proxy Advanced plugin (fetched). https://developer.konghq.com/plugins/ai-proxy-advanced/

### developers.cloudflare.com

- Cloudflare, "AI Gateway Changelog" (unified API, May 2026) (search-only). https://developers.cloudflare.com/changelog/product/ai-gateway/

### developers.openai.com

- OpenAI, "Compaction" (API guide, 2026) (fetched). https://developers.openai.com/api/docs/guides/compaction
- OpenAI, "Conversation state" (API guide, 2026) (fetched). https://developers.openai.com/api/docs/guides/conversation-state
- Prompt caching (OpenAI API docs), 2026 (fetched). https://developers.openai.com/api/docs/guides/prompt-caching
- Reasoning models (OpenAI API docs), 2026 (fetched). https://developers.openai.com/api/docs/guides/reasoning

### digitalocean.com

- DigitalOcean, "DigitalOcean Inference Router, Now Cache-Aware" (2026) (search-only). https://www.digitalocean.com/blog/inference-router-cache-aware

### docs.aws.amazon.com

- AWS, "Validating CloudTrail log file integrity" (search-only). https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html
- AWS, Understanding intelligent prompt routing in Amazon Bedrock (fetched). https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- Route model inference requests across AWS Regions with cross-Region inference (AWS Bedrock docs) (fetched). https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html

### docs.databricks.com

- Point-in-time feature joins, Databricks docs (2026) (fetched). https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series

### docs.github.com

- About Copilot auto model selection (GitHub Docs), 2026 (fetched). https://docs.github.com/en/copilot/concepts/models/auto-model-selection
- Delegated bypass for push protection (GitHub Docs) (search-only). https://docs.github.com/en/enterprise-cloud@latest/code-security/concepts/secret-security/about-delegated-bypass-for-push-protection
- GitHub Docs, About Copilot auto model selection, 2026 (fetched). https://docs.github.com/copilot/concepts/auto-model-selection
- Responsible detection of generic secrets with Copilot secret scanning (GitHub Docs) (fetched). https://docs.github.com/en/code-security/responsible-use/responsible-ai-generic-secrets

### docs.langchain.com

- LangChain, "Short-term memory" (docs) (search-only). https://docs.langchain.com/oss/python/langchain/short-term-memory

### docs.litellm.ai

- Health Check Driven Routing (LiteLLM docs) (fetched). https://docs.litellm.ai/docs/proxy/health_check_routing
- Incident Report: Encrypted Content Failures in Multi-Region Responses API Load Balancing (LiteLLM), 2026 (fetched). https://docs.litellm.ai/blog/responses-api-encrypted-content-incident
- LiteLLM, "Fallbacks (Provider Failover)" (fetched). https://docs.litellm.ai/docs/proxy/reliability
- LiteLLM, Routing docs (fetched). https://docs.litellm.ai/docs/routing
- Response Headers (LiteLLM docs) (fetched). https://docs.litellm.ai/docs/proxy/response_headers

### docsaid.org

- QLite in Practice (1): The Database Is Locked Again! (DOCSAID) (search-only). https://docsaid.org/en/blog/sqlite-wal-busy-timeout-for-workers/

### edpb.europa.eu

- EDPB Guidelines 02/2025 on processing of personal data through blockchain, v2.0 (July 2026) (fetched). https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf
- EDPB news: adopts guidelines on processing personal data through blockchains (April 2025) (fetched). https://www.edpb.europa.eu/news/news/2025/edpb-adopts-guidelines-processing-personal-data-through-blockchains-and-ready_en

### effloow.com

- Effloow, OpenAI's 24h Prompt Cache, 2026 (search-only). https://effloow.com/articles/openai-prompt-cache-retention-24h-cost-proof-2026

### explainx.ai

- explainx.ai, Cursor Router: Auto Model Selection, 2026 (search-only). https://www.explainx.ai/blog/cursor-router-auto-model-selection-july-2026

### futureagi.com

- Frontier Model Safety Analysis 2026 (RSP, Preparedness, FSF) (search-only). https://futureagi.com/blog/frontier-model-safety-analysis-2026/

### gist.github.com

- badlogic, "Context Compaction Research: Claude Code, Codex CLI, OpenCode, Amp" (gist, 2026) (search-only). https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f

### gitclear.com

- The Maintainability Gap: 2026 AI Code Quality Research, GitClear (2026) (fetched). https://www.gitclear.com/the_ai_code_quality_maintainability_gap

### github.blog

- Copilot CLI auto model selection routes based on task (GitHub Changelog), 2026 (fetched). https://github.blog/changelog/2026-07-01-copilot-cli-auto-model-selection-routes-based-on-task/
- Delegated bypass controls for push protection now available at the enterprise level (GitHub Changelog), 2025 (search-only). https://github.blog/changelog/2025-09-16-delegated-bypass-controls-for-push-protection-now-available-at-the-enterprise-level/
- Getting more from each token: How Copilot improves context handling and model routing, 2026 (fetched). https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/
- GitHub Changelog, Auto model selection now routes based on your task in VS Code, 2026-05-20 (fetched). https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code/
- Improvements to secret scanning and public monitoring (GitHub Changelog), 2026 (fetched). https://github.blog/changelog/2026-07-15-improvements-to-secret-scanning-and-public-monitoring/

### github.com

- API Evangelist, "Cloudflare AI Gateway" third-party profile (2026) (search-only). https://github.com/api-evangelist/cloudflare-ai-gateway
- BerriAI/litellm PR #17785, "feat(guardrails): add configurable fail-open, timeout, and app_user tracking to panw_prisma_airs guardrail" (merged 2025-12-11) (fetched). https://github.com/BerriAI/litellm/pull/17785
- Cache TTL silently regressed from 1h to 5m around early March 2026 (anthropics/claude-code issue #46829), 2026 (fetched). https://github.com/anthropics/claude-code/issues/46829
- Clarify sandbox-exec deprecation timeline (apple/containerization issue 737), 2026 (fetched). https://github.com/apple/containerization/issues/737
- GenAI spans (OpenTelemetry semantic-conventions-genai) (fetched). https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md
- Kiro issue #8903, Show which model is used per response in Auto mode (search-only). https://github.com/kirodotdev/Kiro/issues/8903
- openai/codex, "Deprecating chat/completions support in Codex", Discussion #7782 (2025) (search-only). https://github.com/openai/codex/discussions/7782
- OpenSSF Model Signing (OMS) Specification (2025) (fetched). https://github.com/ossf/model-signing-spec
- response body "model" field returns model group alias instead of resolved deployment model (LiteLLM issue 22709) (search-only). https://github.com/BerriAI/litellm/issues/22709
- Response header x-litellm-model-api-base is missing on chunked responses (LiteLLM issue 7249) (search-only). https://github.com/BerriAI/litellm/issues/7249
- sergiobayona/vector_mcp, "streamable-http-spec-compliance.md" (claim that the 2026-07-28 RC removes session IDs) (search-only). https://github.com/sergiobayona/vector_mcp/blob/main/docs/streamable-http-spec-compliance.md
- Streaming /v1/responses drops Anthropic redacted_thinking blocks (maximhq/bifrost issue #5093), 2026 (fetched). https://github.com/maximhq/bifrost/issues/5093
- tau2-bench (sierra-research), 2025 (search-only). https://github.com/sierra-research/tau2-bench
- transparency-dev/witness (GitHub) (search-only). https://github.com/transparency-dev/witness

### goworkwize.com

- NIST 800-88: Complete Guide to Media Sanitization (GoWorkwize) (search-only). https://www.goworkwize.com/blog/what-is-nist-800-88-guide

### greptime.com

- How OpenTelemetry Traces LLM Calls, Agent Reasoning, and MCP Tools, Greptime (2026) (fetched). https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions

### grepture.com

- Best Open Source Models for PII Redaction (Grepture) (fetched). https://grepture.com/blog/best-open-source-models-pii-redaction

### hashicorp.com

- HashiCorp, "SPIFFE: Securing the identity of agentic AI and non-human actors" (April 2026) (fetched). https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors

### helpnetsecurity.com

- What the EU AI Act requires for AI agent logging (Help Net Security), 2026 (fetched). https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/

### huggingface.co

- Qwen, Qwen3-Coder-Next model card, 2026 (fetched). https://huggingface.co/Qwen/Qwen3-Coder-Next

### infoq.com

- InfoQ, "Claude Reaches GA on Microsoft Foundry: European Enterprises Cannot Deploy It" (July 2026) (search-only). https://www.infoq.com/news/2026/07/claude-foundry-ga-europe/

### kiro.dev

- Kiro, Models docs, 2026 (fetched). https://kiro.dev/docs/models/

### konghq.com

- Kong, "Govern the Full AI Data Path with Kong AI Gateway 3.14" (April 2026) (fetched). https://konghq.com/blog/product-releases/kong-ai-gateway-3-14
- Kong, "Intelligent Model Routing: Kong AI Gateway Applies NVIDIA NeMo Switchyard Across Model Traffic" (2026) (search-only). https://konghq.com/blog/engineering/llm-routing-kong-ai-gateway-nvidia-nemo-switchyard

### kosmoy.com

- Kosmoy, Cloudflare AI Gateway Alternatives, 2026-07-15 (fetched). https://www.kosmoy.com/resources/blog/cloudflare-ai-gateway-alternatives/

### labs.cloudsecurityalliance.org

- Cloud Security Alliance, "EU AI Act's High-Risk Deadline: Deferred, Not Cancelled" (August 2026) (fetched). https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/

### labs.scale.com

- Scale, SWE-Bench Pro leaderboards, 2026. and (search-only). https://labs.scale.com/leaderboard/swe_bench_pro_private
- Scale, SWE-Bench Pro leaderboards, 2026. and (search-only). https://labs.scale.com/leaderboard/swe_bench_pro_public

### latent.space

- GPT-5's Router: how it works and why Frontier Labs are now targeting the Pareto Frontier, 2025 (fetched). https://www.latent.space/p/gpt5-router

### learn.microsoft.com

- Microsoft Learn, Model router for Microsoft Foundry concepts, updated 2026-09-01 (fetched). https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router

### llrx.com

- LLRX, AI in Finance and Banking, April 30, 2026 (search-only). https://www.llrx.com/2026/04/ai-in-finance-and-banking-april-30-2026/

### localaimaster.com

- Local AI Master, Devstral 2 Review, 2026 (search-only). https://localaimaster.com/models/devstral

### martinfowler.com

- eature Toggles (Martin Fowler) (fetched). https://martinfowler.com/articles/feature-toggles.html

### matthewswong.com

- QLite Litestream Replication in Production Guide (2026) (fetched). https://www.matthewswong.com/en/blog/sqlite-litestream-replication-production/

### media.defense.gov

- Model Context Protocol (MCP): Security Design Considerations (NSA CSI), 2026, (fetch returned 403) (search-only). https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF

### medium.com

- Critical Claude Code Sandbox Vulnerability Enables Network Escape and Arbitrary File Write Attacks (Medium), 2026 (fetched). https://medium.com/@Inforsecpro/critical-claude-code-sandbox-vulnerability-enables-network-escape-and-arbitrary-file-write-attacks-2186222829d4
- LLM Evaluation in 2026 (Medium) (search-only). https://medium.com/@nairmilind3/llm-evaluation-in-2026-e631a78c67dc
- StuckLoopDetection: How We Stopped an Agent Burning $12 on 47 Identical Calls (pydantic-deep), 2026 (search-only). https://medium.com/@kacperwlodarczyk/stuckloopdetection-how-we-stopped-an-agent-burning-12-on-47-identical-calls-a12b5ea1f193

### metr.org

- METR, "Common Elements of Frontier AI Safety Policies" (search-only). https://metr.org/common-elements

### microsoft.com

- Microsoft Research, A/B Testing Infrastructure Changes at Microsoft ExP, 2024 (fetched). https://www.microsoft.com/en-us/research/articles/a-b-testing-infrastructure-changes-at-microsoft-exp/

### mlflow.org

- MLflow, What Is Online Evaluation in ML: A 2026 Guide (fetched). https://mlflow.org/articles/what-is-online-evaluation-in-ml-a-2026-guide/
- MLOps Pipeline Automation Best Practices in 2026, MLflow (2026) (fetched). https://mlflow.org/articles/mlops-pipeline-automation-best-practices-in-2026/

### modelcontextprotocol.io

- MCP Security Best Practices (spec 2026-07-28) (fetched). https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices
- Model Context Protocol, "Transports" (2025-03-26 specification) (search-only). https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
- Tools (Model Context Protocol specification 2025-11-25), 2025 (fetched). https://modelcontextprotocol.io/specification/2025-11-25/server/tools

### mondaq.com

- Blockchain And GDPR: EDPB Guidelines 02/2025 Adopted, Mondaq (2026) (fetched). https://www.mondaq.com/fin-tech/1617044/blockchain-and-gdpr-edpb-guidelines-022025-adopted

### morphllm.com

- Morph, OpenAI API Pricing 2026 (search-only). https://www.morphllm.com/openai-api-pricing

### notdiamond.ai

- Not Diamond Code: intelligent model routing for coding agents, 2026 (fetched). https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents

### oneuptime.com

- OneUptime, "How to Configure Webhook FailurePolicy and TimeoutSeconds" (February 2026) (search-only). https://oneuptime.com/blog/post/2026-02-09-webhook-failure-policy-timeout/view

### open-policy-agent.github.io

- Open Policy Agent, "Failing Closed | Gatekeeper" (fetched). https://open-policy-agent.github.io/gatekeeper/website/docs/failing-closed/

### openai.com

- Introducing GPT-5, 2025 (search-only). https://openai.com/index/introducing-gpt-5/
- OpenAI, Offering Zero Data Retention for frontier models, 2026 (search-only). https://openai.com/index/offering-zero-data-retention-for-frontier-models/
- Why SWE-bench Verified no longer measures frontier coding capabilities, OpenAI (2026), S (fetch returned 403) (fetched). https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/

### openai.github.io

- OpenAI, "Sessions - OpenAI Agents SDK" (search-only). https://openai.github.io/openai-agents-python/sessions/

### openrouter.ai

- OpenRouter Prompt Caching: What Cached Tokens Cost (sticky routing), 2026 (fetched). https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/
- OpenRouter, "Codex CLI with OpenRouter: config.toml Setup and Models" (2026) (search-only). https://openrouter.ai/blog/tutorials/codex-cli-openrouter/
- OpenRouter, How OpenRouter Model Routing Works, 2026-06-12 (fetched). https://openrouter.ai/blog/insights/model-routing/

### opentelemetry.io

- Inside the LLM Call: GenAI Observability with OpenTelemetry (OpenTelemetry blog), 2026 (fetched). https://opentelemetry.io/blog/2026/genai-observability/

### phoenix.security

- Three CVEs in Claude Code CLI (Phoenix Security), 2026 (fetched). https://phoenix.security/claude-code-leak-to-vulnerability-three-cves-in-claude-code-cli-and-the-chain-that-connects-them/

### platform.claude.com

- Anthropic, "Compaction" (Claude Platform docs, 2026) (fetched). https://platform.claude.com/docs/en/build-with-claude/compaction
- Anthropic, "Prompt caching" (Claude Platform docs, 2026) (fetched). https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, Pricing (platform docs), 2026 (fetched). https://platform.claude.com/docs/en/about-claude/pricing
- Thinking (Claude Platform Docs), 2026 (fetched). https://platform.claude.com/docs/en/build-with-claude/thinking

### portkey.ai

- Portkey, "Safeguard your AI requests with guardrails" (fetched; page did not expose the fail-open status-code detail, so it is not cited above) (fetched). https://portkey.ai/features/guardrails
- Portkey, Conditional routing docs (fetched). https://portkey.ai/docs/product/ai-gateway/conditional-routing

### privacy.anthropic.com

- Anthropic Privacy Center, "Where are your servers located? Do you host your models on EU servers?" (search-only). https://privacy.anthropic.com/en/articles/7996890-where-are-your-servers-located-do-you-host-your-models-on-eu-servers

### proceedings.iclr.cc

- RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers (ICLR 2026) (fetched). https://proceedings.iclr.cc/paper_files/paper/2026/file/4987bb24bc53c198785922d1bd9e18cf-Paper-Conference.pdf

### promptquorum.com

- PromptQuorum, Best Local Tool-Calling Models 2026 (fetched). https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026

### propelcode.ai

- Token Counting Explained: tiktoken, Anthropic, and Gemini (Propel Code), 2025 (search-only). https://www.propelcode.ai/blog/token-counting-tiktoken-anthropic-gemini-guide-2025

### repost.aws

- Can Cloudtrail support KMS code signing transparency logs (AWS re:Post) (search-only). https://repost.aws/questions/QUJlrDBq-CRYurHVCIUNxbjw/can-cloudtrail-support-kms-code-signing-transparency-logs-e-g-by-logging-signatures

### research.atspotify.com

- Calibrated Recommendations with Contextual Bandits on Spotify Homepage (2025) (fetched). https://research.atspotify.com/2025/9/calibrated-recommendations-with-contextual-bandits-on-spotify-homepage

### securityboulevard.com

- Exposed Ollama Servers: Security Risks of Publicly Accessible LLM Infrastructure (Security Boulevard), 2026 (fetched). https://securityboulevard.com/2026/03/exposed-ollama-servers-security-risks-of-publicly-accessible-llm-infrastructure/

### securityweek.com

- Anthropic Silently Patches Claude Code Sandbox Bypass (SecurityWeek), 2026 (fetched). https://www.securityweek.com/anthropic-silently-patches-claude-code-sandbox-bypass/

### sesamedisk.com

- QLite in Production 2026: Real Benchmarks, Limits, and When to Migrate to Postgres (2026) (fetched). https://sesamedisk.com/sqlite-in-production-2026-benchmarks-limits/

### siliconreport.com

- OpenAI Abandons SWE-Bench Verified, SiliconReport (2026) (fetched). https://www.siliconreport.com/openai-abandons-swe-bench-verified-citing-widespread-data-contamination-and-flawed-tests-6ebd9b34

### simonwillison.net

- Claude Token Counter, now with model comparisons (Simon Willison), 2026 (fetched). https://simonwillison.net/2026/Apr/20/claude-token-counts/
- How we contain Claude across products (Anthropic, via Simon Willison), 2026 (fetched). https://simonwillison.net/2026/May/30/how-we-contain-claude/
- Stealing Reasoning Traces from Proprietary LLM APIs (as reported by Simon Willison; arXiv 2608.09867 per that report), 2026 (fetched). https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/

### snorkel.ai

- Snorkel AI, Terminal-Bench 2.1 leaderboard, 2026 (fetched). https://snorkel.ai/leaderboard/terminal-bench-2-1/

### softwareimprovementgroup.com

- SIG, A comprehensive EU AI Act Summary (August 2026 update) (fetched). https://www.softwareimprovementgroup.com/blog/eu-ai-act-summary/

### sota.io

- Art.17 Right to Erasure: LLM Training Data Removal & RAG Vector Store Deletion 2026, sota.io (2026) (fetched). https://sota.io/blog/eu-ai-act-gdpr-art17-right-erasure-training-data-llm-2026

### sqlite.org

- QLite Online Backup API (fetched). https://www.sqlite.org/backup.html

### sre.google

- Canarying Releases (Google SRE Workbook) (fetched). https://sre.google/workbook/canarying-releases/
- Implementing SLOs (Google SRE Workbook) (fetched). https://sre.google/workbook/implementing-slos/

### systemshardening.com

- igstore Keyless Signing and Cosign Verification (systemshardening.com) (search-only). https://www.systemshardening.com/articles/cicd/sigstore-keyless-signing/

### techbytes.app

- Verifying Software Integrity with Sigstore: The 2026 Cheat Sheet (techbytes) (search-only). https://techbytes.app/posts/software-integrity-sigstore-cosign-rekor-cheat-sheet/

### tenthousandmeters.com

- QLite concurrent writes and "database is locked" errors (tenthousandmeters) (search-only). https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/

### thehackernews.com

- Critical Cursor Flaws Could Let Prompt Injection Escape Sandbox (The Hacker News), 2026 (fetched). https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html
- OpenAI, Anthropic, Google API Flaw Let Weaker AI Models Decode Stronger Models' Reasoning (The Hacker News), 2026 (fetched). https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html
- Researchers Find 175,000 Publicly Exposed Ollama AI Servers (The Hacker News), 2026 (fetched). https://thehackernews.com/2026/01/researchers-find-175000-publicly.html

### theregister.com

- The Register, Anthropic promises zero data retention, 2026-09-02 (fetched). https://www.theregister.com/ai-and-ml/2026/09/02/anthropic-promises-zero-data-retention-but-customers-must-check-it-worked/5293789

### tianpan.co

- The Tail-Tolerant Retry Policy Your LLM Gateway Doesn't Have, 2026 (fetched). https://tianpan.co/blog/2026-05-02-tail-tolerant-retry-policy-llm-gateway-latency-cliff
- TianPan, Releasing AI Features Without Breaking Production, 2026 (fetched). https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing

### truefoundry.com

- OpenTelemetry for LLMs: Instrumentation Guide for a Multi-Provider AI Gateway (TrueFoundry) (fetched). https://www.truefoundry.com/blog/opentelemetry-llm-gateway-instrumentation

### veritaschain.org

- Crypto-Shredding: The Technical Foundation for Reconciling GDPR and Financial Record-Keeping Obligations, VeritasChain (2026) (fetched). https://veritaschain.org/blog/posts/2026-01-18-crypto-shredding-gdpr-mifid-ii-reconciliation/

### vllm.ai

- vLLM, Session-Aware Agentic Routing, 2026-06-02 (fetched). https://vllm.ai/blog/2026-06-02-session-aware-agentic-routing

