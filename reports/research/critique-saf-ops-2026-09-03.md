# Research-backed critique: SAF and OPS buckets

Date: 2026-09-03. Scope: ADRL-SAF-001 to 009 and ADRL-OPS-001 to 008 as they stand in the register after the 2026-09-02 and 2026-09-03 reviews. This critique does not repeat those reviews' attacks; it asks whether each decision is grounded in 2025 and 2026 research and practice, and gives the strongest FOR and AGAINST case from sources actually retrieved.

Citation discipline: every `[source: ...]` tag names a URL that was either fetched with WebFetch ("fetched") or appeared in a WebSearch result with a matching title ("search title"). Nothing else is cited. Where a search summary mentioned a fact without a matching title, the fact is omitted.

Verdict scale: CURRENT (grounded in the newest practice), DATED (correct principle, mechanism superseded), CONTESTED (newest evidence cuts both ways or against), UNGROUNDED (no external grounding found). Each verdict names the newest relevant source year.

---

## SAF: Safety, Privacy, Hard Constraints

**State of the field, 2026.** Three things changed since the register's sources were chosen. First, secret detection moved from regex-and-entropy to hybrid regex-plus-LLM classification: MSR 2026 reports 94.49% F1 with fine-tuned open models, and GitHub now ships AI generic-secret detection with a `secret_category` field separating provider patterns from generic and AI-detected ones. Second, the coding-agent threat model became empirical rather than theoretical: Claude Code, Cursor and Codex each shipped sandbox escapes and injection CVEs in 2025 and 2026, Anthropic's own guidance now says to use a dedicated VM for untrusted repositories, and Apple still lists `sandbox-exec` as deprecated with no removal date. Third, information-flow control for agents matured past strict taint: FIDES (2025), APPA and NeuroTaint (2026) show recoverable, branch-scoped labels with 64 to 91% utility and zero observed attacks, while PIIBench (2026) shows every open PII detector below 0.14 F1 across domains. The register's ordering and pin principles hold; several mechanisms are a generation behind.

### ADRL-SAF-001: Hard gates first, on every request

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

**Grounding verdict:** CURRENT (newest source 2026), with the monotonicity clause contested by APPA.

**Recommendation:** Keep ordering and per-request scope as written; they are the consensus of 2025 to 2026 agent-security work. Add a follow-up to evaluate branch-scoped (APPA-style) confinement for subagent lineages as a future relaxation of sub-clause 2, and add a semantic-carrier test (secret paraphrased in a compaction summary) to the adversarial suite.

### ADRL-SAF-002: One-way pin, durable, lineage-scoped, audited release

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

**Grounding verdict:** CONTESTED (newest source 2026).

**Recommendation:** Keep one-way for the human-facing path and the delegated-reviewer model, which is now enterprise practice. Reopen Q5 in light of APPA: specify that a descendant subagent lineage may be pinned without pinning the parent's future requests, and require the pin store to be under the same integrity control as the egress ledger (SAF-009), not a plain file.

### ADRL-SAF-003: Secret detection per request, precision-measured

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

**Grounding verdict:** DATED (principle current, mechanism a generation behind; newest source 2026).

**Recommendation:** Add an LLM contextual-classification tier served on the local rung and measure it against the regex tiers on the same corpus. Replace "retroactive deletion" with per-lineage or per-epoch encryption of embeddings so suppression is key destruction, aligning with OPS-004.

### ADRL-SAF-004: Pinned sessions fail loudly, in the harness's dialect

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

**Grounding verdict:** CURRENT (newest source 2026).

**Recommendation:** Add `disable_fallbacks` on the pinned key or per request as the mechanical binding, and a CI check that `default_fallbacks` contains no cloud deployment. Pin the surfacing contract to a tested Claude Code version range and re-run the protocol test on each release, as the follow-up already implies.

### ADRL-SAF-005: Block, and make the block recoverable

Decision: privacy-context conflicts block; the block uses the vendor's too-long wording so the harness compacts; the local rung must hold the harness's compaction request (100k floor).

**FOR**
- The 100k clamp is confirmed verbatim: Claude Code "clamps the value to at least 100,000 tokens and at most the model's context window, so you can't match a gateway limit below 100,000, and `/compact` remains the recovery there" [source: Connect Claude Code to an LLM gateway, 2026, https://code.claude.com/docs/en/llm-gateway-connect (fetched)].
- The harness's own context-limit path is now specified: on a request rejected because "the input plus `max_tokens` exceeds the context limit", Claude Code "retries with a reduced `max_tokens`, and stops retrying and compacts instead" when nothing fits [source: Claude Code errors reference, 2026 (fetched)].
- LiteLLM's `context_window_fallbacks` with `enable_pre_call_checks` is the gateway-side analogue, and it is what must be disabled for pinned traffic [source: LiteLLM reliability docs (fetched)].

**AGAINST**
- The decision promises "one clear failure" but the harness's documented behaviour on a recognised too-long error is to retry first with a reduced `max_tokens` and compact only when no reduction fits; a pinned overflow block will therefore be retried at least once, and the block must be idempotent and cheap [source: Claude Code errors reference (fetched)].
- Token budgets moved under the decision's feet: the Opus 4.7 tokenizer maps "the same input ... to more tokens, roughly 1.0 to 1.35x", measured at 1.46x on a real system prompt; a compaction floor computed in one tokenizer is wrong for the next [source: Claude Token Counter, now with model comparisons, Simon Willison, 2026, https://simonwillison.net/2026/Apr/20/claude-token-counts/ (fetched)].
- `count_tokens` is optional at the gateway; when absent "Claude Code falls back to counting context usage through the inference endpoint", which means the harness's own view of context size may come from inference calls that a pinned lineage must serve locally [source: Gateway protocol reference (fetched)].

**Grounding verdict:** CURRENT (newest source 2026).

**Recommendation:** Amend sub-clause 1 to state that the block is idempotent under the harness's reduced-`max_tokens` retry and that at most one such retry is expected before compaction. Compute the compaction-floor check per model family and re-run it on each tokenizer change.

### ADRL-SAF-006: Infeasible rungs removed before optimisation

Decision: unhealthy or context-infeasible rungs are removed from the candidate set before optimisation.

**FOR**
- The gateway does the same thing at its layer: LiteLLM's health-check-driven routing removes a deployment "immediately, before a user request lands on it", and cooldowns "temporarily remove unhealthy deployments from the active pool" [source: Health Check Driven Routing, LiteLLM docs, https://docs.litellm.ai/docs/proxy/health_check_routing (search title); LiteLLM reliability docs (fetched)].
- Tokenizer files for local families are downloadable, so exact counts on the rung's own tokenizer are available: "Qwen3, DeepSeek-V3, Llama 4, Mistral's Tekken, and GLM-5 all ship downloadable tokenizer files" [source: Token Counting Explained: tiktoken, Anthropic, and Gemini, Propel Code, 2025, https://www.propelcode.ai/blog/token-counting-tiktoken-anthropic-gemini-guide-2025 (search title)].

**AGAINST**
- A once-calibrated safety ratio is stale by construction: Anthropic's own tokenizer changed by "roughly 1.0 to 1.35x" at Opus 4.7, and the decision's follow-up proposes a static per-rung ratio [source: Claude Token Counter, Simon Willison, 2026 (fetched)].
- The gateway health view the decision wants to read may not exist: "Background health checks are off by default" in LiteLLM, so "read the gateway's view" degrades to reading cooldown state derived from failed requests, which is reactive rather than predictive [source: Health Check Driven Routing, LiteLLM docs (search title)].
- Cross-family divergence on code is larger than on prose: modern tokenizers are "15 to 40% more efficient for code than older tokenizers", so a Claude-derived count applied to a local model errs in an unknown direction, as the review already noted, and the magnitude is now quantified [source: Tokenizer Comparison, Part 2, Medium, https://atul4u.medium.com/tokenizer-comparison-part2-comprehensive-tokenizer-performance-analysis-a8e0613bed0d (search title)].

**Grounding verdict:** CURRENT (newest source 2026).

**Recommendation:** Replace the "safety ratio" follow-up with exact counting on each local rung's published tokenizer and treat the Claude count as an estimate for the cloud rungs only. Enable gateway background health checks as a prerequisite of "read the gateway's view".

### ADRL-SAF-007: Verification runs sandboxed, then diffed

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

**Grounding verdict:** CONTESTED (newest source 2026).

**Recommendation:** For restricted repositories (SAF-008 class), require a microVM or container boundary (Firecracker, Docker Sandboxes, gVisor) for verification and reserve the Seatbelt/bubblewrap path for unrestricted repositories, matching Anthropic's own tiering. Add a synthetic "sandbox actually on" probe (attempt egress, attempt a write outside scratch) before every verification run, because the five-week CVE-2025-66479 window shows configuration alone is not evidence.

### ADRL-SAF-008: Repository and data-class gate (PII tier retained in SAF)

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

**Grounding verdict:** CONTESTED (newest source 2026): residency clauses CURRENT, PII tier UNGROUNDED on code.

**Recommendation:** Keep clauses 1, 2 and 4 and hand them to TRU as planned. Demote clause 3 from "detector tier with pin semantics" to "shadow-only PII findings until a measured F1 on a the company fixture-and-log corpus exceeds a pre-registered floor", and cite PIIBench as the reason the floor is needed.

### ADRL-SAF-009: Egress ledger and gate-audit integrity

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

**Grounding verdict:** CURRENT (newest source 2026), with a witness gap.

**Recommendation:** Specify the anchor as a witnessed transparency log (a private Rekor v2 or Tessera instance with at least one witness outside the gateway team) rather than "an endpoint", and pre-register the checkpoint interval as the maximum undetectable-tamper window. Record the signed digest alongside every KMS signature because the KMS audit trail will not.

---

## OPS: Platform, Runtime, Operations

**State of the field, 2026.** Operations practice for AI gateways converged on three things the register partly anticipates. Observability standardised on OpenTelemetry's `gen_ai.*` conventions, which remain in Development status: `gen_ai.provider.name` is Required and `gen_ai.response.model` only Recommended, and LiteLLM's deployment headers are absent on streamed responses. Key custody moved from long-lived KMS keys with annual rotation to identity-bound keyless signing and witnessed transparency logs (Rekor v2 GA October 2025), and NIST SP 800-88 Rev. 2 (September 2025) formalised cryptographic erase while warning it is not assured where keys are backed up or escrowed. Sandboxing guidance from Anthropic now treats the per-command sandbox as insufficient for unattended runs, and 175,000 exposed Ollama hosts showed that "local" is a network property, not a label. Shadow-mode and SLO practice still rest on the Google SRE books; the new lesson from CVE-2025-66479 is that rate-based SLIs cannot see a control that is silently off.

### ADRL-OPS-001: Multi-worker consistency and the single-process constraint

Decision: one ADRL process per host until every gate- or pin-affecting state item is port-backed; SQLite single-writer contract; startup lock; versioned state inventory.

**FOR**
- The SQLite contract named (WAL, `busy_timeout`, `BEGIN IMMEDIATE`) matches current practice: "if you run transactions without using BEGIN IMMEDIATE, you might hit SQLITE_BUSY regardless of your timeout setting", and timeouts below five seconds "led to occasional 'database is locked' errors" [source: SQLite concurrent writes and "database is locked" errors, tenthousandmeters, https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/ (search title); SQLite in Practice (1), DOCSAID, https://docsaid.org/en/blog/sqlite-wal-busy-timeout-for-workers/ (search title)].
- The online backup API the sibling decision relies on works with a live single writer: "the source database does not need to be locked for the duration of the copy" [source: SQLite Online Backup API, https://www.sqlite.org/backup.html (fetched)].
- Declaring an inventory of process-local state is the same discipline Fowler recommends for toggles: keep decision points separate and "manage toggle configuration via source control" so what was active is auditable [source: Feature Toggles, Martin Fowler, https://martinfowler.com/articles/feature-toggles.html (fetched)].

**AGAINST**
- The constraint is stricter than SQLite practice warrants: multi-process writers are routine with WAL, `BEGIN IMMEDIATE` and a five-second `busy_timeout`, and app-level locking is advised only "if you have a lot of concurrent writers" [source: tenthousandmeters, SQLite concurrent writes (search title)]. The real blocker is the in-memory pin cache, which the decision admits; the SQLite clause is not load-bearing.
- "One process per host" is ambiguous once verification or the harness runs in a VM or container, which Anthropic now recommends for untrusted repositories; a lock file inside a VM does not prevent a second proxy on the laptop, and vice versa [source: Choose a sandbox environment, Claude Code docs, 2026 (fetched)].
- The backup API restarts when another process writes: "If another thread or process writes to the source database while this function is sleeping, then SQLite detects this and usually restarts the backup process", so a second (read-mostly) process that also writes telemetry will stall backups the decision does not mention [source: SQLite Online Backup API (fetched)].

**Grounding verdict:** CURRENT (newest source 2025).

**Recommendation:** Keep the lock and inventory; drop the implication that SQLite is a reason for single-process. Define "host" as the isolation boundary the proxy shares with the harness (laptop, VM or container) and require the lock to live inside that boundary.

### ADRL-OPS-002: Key custody and rotation

Decision: four key classes with named custodians; manifest and checkpoint keys separated in hardware or managed KMS with annual rotation; dev keys refused by default; a separate signer process.

**FOR**
- Separating the audit-trail signer from the signed party is exactly the transparency-log model: Rekor v2 "folds witnessing into the log" so the log operator alone cannot vouch for itself [source: Rekor v2 GA, Sigstore blog, 2025 (fetched); Can I Get A Witness, transparency.dev (fetched)].
- Per-session keys destroyed on erasure are the NIST-endorsed pattern: SP 800-88 Rev. 2 (26 September 2025) expands guidance on cryptographic erase and recommends zeroisation of target keys [source: NIST SP 800-88 Rev. 2, 2025, https://csrc.nist.gov/pubs/sp/800/88/r2/final (search title)].
- Refusing committed development keys addresses a real class: the Claude Code CVE chain shows credential-helper config values executed with `shell: true`, so anything under a developer-writable config path is in scope [source: Three CVEs in Claude Code CLI, Phoenix Security, 2026 (fetched)].

**AGAINST**
- Long-lived KMS keys with annual rotation is the pre-2024 pattern; the 2026 baseline for attestations is keyless: Fulcio issues "short-lived certificates binding an ephemeral key to an OpenID Connect identity", "eliminating the 'lost private key' scenario", and SLSA level 2+ treats signed provenance as baseline [source: Sigstore Keyless Signing and Cosign Verification, systemshardening.com, https://www.systemshardening.com/articles/cicd/sigstore-keyless-signing/ (search title); Verifying Software Integrity with Sigstore: The 2026 Cheat Sheet, https://techbytes.app/posts/software-integrity-sigstore-cosign-rekor-cheat-sheet/ (search title)].
- The KMS audit trail is weaker than the decision assumes: CloudTrail does not log "the original message digest or the resulting signature" for KMS sign calls, so "signed by security's key" is not independently verifiable after the fact without a transparency log [source: AWS re:Post, CloudTrail and KMS signing (search title)].
- Session keys "wrapped by a host master key" and backed up (OPS-004) conflict with NIST: CE "should not be considered an assured method of sanitization on [media] that have been escrowed or have a backup, unless the organization is confident about storage and management of the encryption keys outside of the [media]" [source: NIST SP 800-88 Rev. 2 (search title); What is Cryptographic Erase as per NIST SP 800-88 Rev.2, BitRaser, https://www.bitraser.com/blog/cryptographic-erase-and-supported-devices/ (search title)].

**Grounding verdict:** DATED (newest source 2026).

**Recommendation:** Replace "hardware or managed KMS, annual rotation" for the manifest and checkpoint keys with identity-bound keyless signing recorded in a private Rekor v2 instance, keeping a KMS key only as the offline root. Add the NIST CE caveat to the key inventory: the session-key wrapping key must have a sanitisation policy that covers its backups.

### ADRL-OPS-003: Endpoint inventory, rollout and change control

Decision: signed endpoint inventory with trust zone, geography and data-use profile; LiteLLM config generated only from it; `local` must be `on_host` on loopback or a Unix socket; served identity matched against it.

**FOR**
- The evidence that "local" must be enforced, not labelled, is overwhelming: 175,000 Ollama hosts exposed, "roughly 23,000 remaining persistently online", with LLMjacking campaigns "systematically scanning the internet for exposed Ollama instances, vLLM servers, and OpenAI-compatible APIs running without authentication" [source: The Hacker News, 175,000 Ollama servers, 2026 (fetched); Exposed Ollama Servers, Security Boulevard, 2026, https://securityboulevard.com/2026/03/exposed-ollama-servers-security-risks-of-publicly-accessible-llm-infrastructure/ (search title)].
- The gateway can name the deployment it used: LiteLLM returns `x-litellm-model-id`, `x-litellm-model-group` and `x-litellm-model-api-base`, and "the headers above still name the deployment that answered" even for auto-routed aliases [source: Response Headers, LiteLLM docs, https://docs.litellm.ai/docs/proxy/response_headers (fetched)].
- Geography as an inventory attribute matches how Bedrock exposes it (geographic vs global profiles) and how it is evidenced (`inferenceRegion` in CloudTrail) [source: AWS Bedrock cross-region inference docs (fetched)].

**AGAINST**
- Loopback plus `on_host` is not a trust zone when the host runs unconstrained processes: Anthropic's docs state "MCP servers and hooks are separate processes that run unconstrained on the host", and the MCP spec advises local servers to "Use the `stdio` transport to limit access to just the MCP client" or "Require an authorization token" on HTTP. An unauthenticated loopback model endpoint is reachable by every MCP server and hook the developer installed [source: Choose a sandbox environment (fetched); MCP Security Best Practices, spec 2026-07-28, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices (fetched)].
- The inventory's "geography" is a class, not a place, for cloud entries: geographic profiles route "within the geography" to a region Bedrock selects; the inventory can assert "EU", not a region, and the ledger must take the region from the provider's own record [source: AWS Bedrock cross-region inference docs (fetched)].
- The served identity the inventory is matched against is unreliable on streams: the `x-litellm-model-api-base` header "is absent" on chunked responses, and a LiteLLM bug reports the body `model` field returning "model group alias instead of resolved deployment model" [source: Response header missing on streamed responses, LiteLLM issue 7249, https://github.com/BerriAI/litellm/issues/7249 (search title); response body model returns alias, LiteLLM issue 22709, https://github.com/BerriAI/litellm/issues/22709 (search title)].

**Grounding verdict:** CURRENT (newest source 2026).

**Recommendation:** Add "authenticated" as a required attribute of every `on_host` entry (bearer token or Unix socket with file-mode restriction), because loopback without auth is reachable by unconstrained MCP servers and hooks. Make the CI check assert the served-identity header is present on a streamed test response before the inventory match is trusted.

### ADRL-OPS-004: Backup, restore and erasure

Decision: SQLite online backups with the writer paused; keystore backed up separately; erasure by key deletion with a field-level inventory; restore replays events and verifies the egress chain.

**FOR**
- Cryptographic erase is now the standard's preferred mechanism: SP 800-88 Rev. 2 (September 2025) "expands guidance on cryptographic erase" and prescribes zeroisation of the target keys [source: NIST SP 800-88 Rev. 2, 2025 (search title); NIST 800 88 Rev.2 Guidelines, BitRaser (search title)].
- The vector-store precedent is direct: Ghost Vectors proposes "Epoch Key Rotation" that "encrypts vectors and discards the key upon deletion", completing deletion of 500 vectors in about 2.5 ms and producing "cryptographic proof of deletion via ECDSA signatures", reducing PII recovery to 0% [source: Ghost Vectors, 2026 (fetched)].
- The backup mechanism is sound: the online backup API copies incrementally and "the source database does not need to be locked for the duration of the copy" [source: SQLite Online Backup API (fetched)].

**AGAINST**
- The decision backs up the keystore, and NIST says that breaks the assurance: CE is not assured "on [media] that have been escrowed or have a backup, unless the organization is confident about storage and management of the encryption keys outside" it, and documentation must address "how these potential sources from which the key can be recovered have been addressed". Clause 2's replay of `erased` events after restore is a process control on top of a compromised guarantee, not CE [source: NIST SP 800-88 Rev. 2 (search title)].
- The NumPy in-memory index and any HNSW file are soft-delete stores by construction; deletion "marks records as deleted without actually removing the underlying embedding data from disk", so "move embeddings under session keys" must mean encrypt-at-rest per epoch, not delete rows [source: Ghost Vectors, 2026 (fetched)].
- Deletion must extend to every layer including backups under the GDPR reading the decision implicitly targets, and a keyed hash "reveals nothing without the key" only while the rotatable host key is retained read-only "for the evidence horizon", which is the escrow NIST warns about [source: NIST 800-88 guide, GoWorkwize, https://www.goworkwize.com/blog/what-is-nist-800-88-guide (search title); OPS-002 as written].

**Grounding verdict:** CURRENT (newest source 2026).

**Recommendation:** State explicitly that keystore backups are themselves under a sanitisation policy and that the host key's read-only retention is a documented CE exception, per SP 800-88 Rev. 2. Adopt epoch-keyed encryption for embeddings with a signed deletion receipt, which the Ghost Vectors work makes cheap.

### ADRL-OPS-005: Shadow-mode semantics per subsystem

Decision: gates `enforce`/`observe`, routing `off`/`shadow`/`live`, fallback `off`/`shadow`/`live`; observe writes to a shadow namespace with no authority; mode changes are versioned and ledgered.

**FOR**
- The core rule (observation must not affect the control) is the SRE canary principle: "bad behavior of the canary deployment can also negatively impact the control", including via "two consecutive requests sent by a single client" where the first response alters the second request [source: Canarying Releases, Google SRE Workbook, https://sre.google/workbook/canarying-releases/ (fetched)].
- Versioned, ledgered mode changes follow the toggle literature: "Managing toggle configuration via source control and re-deployments is preferable" for auditability of what was active [source: Feature Toggles, Martin Fowler (fetched)].
- The separate-namespace pattern is what the largest secret scanner does for its AI tier: AI-detected generic secrets "are surfaced as alerts ... in a separate list from regular secret scanning alerts" [source: Responsible detection of generic secrets, GitHub Docs (fetched)].

**AGAINST**
- "Shadow findings on live traffic are the labelled corpus" is a biased corpus: observe mode is only permitted on traffic "whose policy already permits cloud", so the precision measurement excludes exactly the restricted repositories where the detectors matter most, and the SRE guidance warns that canary metrics must be "clearly attributable to the change we are canarying, and ... not be influenced by external factors" [source: Canarying Releases, SRE Workbook (fetched)].
- Fowler distinguishes short-lived release toggles ("not stick around much longer than a week or two") from long-lived ops toggles; the decision's `observe` mode is a release toggle for a new detector but is specified like a permanent ops mode, with no expiry, so a detector can sit in observe indefinitely while its findings accrue [source: Feature Toggles, Martin Fowler (fetched)].
- A shadow namespace still stores span hashes and locating features for a lineage the authoritative namespace never pinned; under NeuroTaint's cross-session persistence finding, that store is a taint carrier with no suppression rule attached [source: Ghost in the Agent, 2026 (fetched)].

**Grounding verdict:** CURRENT (newest source 2026).

**Recommendation:** Give every `observe` entry an expiry and an owner, as a release toggle. State that shadow-namespace findings are prompt-class data under MEM-005 with the same retention as pinned lineages, and record the corpus bias (cloud-permitted traffic only) in the SAF-003 precision report.

### ADRL-OPS-006: Record the served identity, not the intended one

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

**Grounding verdict:** CONTESTED (newest source 2026): principle current, evidence path broken on streamed traffic.

**Recommendation:** Require the gateway contract (RTG-008) to emit deployment id in a trailer or in-band metadata on streamed responses, and set `return_raw_model_name` as a second channel; until then treat every streamed row as `assumed_intended` and expect the blocker to hold. Add a periodic reconciliation of served geography against the provider's own log (CloudTrail `inferenceRegion` or equivalent).

### ADRL-OPS-007: Audit-anchor availability, rollback and incident response

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

**Grounding verdict:** CURRENT (newest source 2025 for the anchor design, 2026 for the runbook dependencies).

**Recommendation:** Name the sink as a witnessed log (private Rekor v2 or Tessera) with one witness outside both the ADRL and gateway teams, and record witness cosignatures as the receipt. Make OPS-006's streamed-identity fix a prerequisite of the "pinned lineage reached cloud" runbook.

### ADRL-OPS-008: Fail-open SLOs, alerting and bypass audit

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

**Grounding verdict:** CURRENT (newest source 2026), with a coverage gap for silent-off failures.

**Recommendation:** Add a synthetic-probe SLI: a known secret-bearing request injected on a schedule that must produce a pin and a ledger row, so a gate that is silently off breaches within one probe interval. Require an error-budget policy with a freeze action for `gate_path` on unpinned lineages, and route that alert to someone other than the developer whose session triggered it.

---

## Verdict tally

| Verdict | Decisions |
|---|---|
| CURRENT | SAF-001, SAF-004, SAF-005, SAF-006, SAF-009, OPS-001, OPS-003, OPS-004, OPS-005, OPS-007, OPS-008 (11) |
| CONTESTED | SAF-002, SAF-007, SAF-008, OPS-006 (4) |
| DATED | SAF-003, OPS-002 (2) |
| UNGROUNDED | none as a whole; SAF-008 clause 3 (PII tier) is ungrounded on code |

## Sources

Fetched with WebFetch:
- How we contain Claude across products (Anthropic, via Simon Willison), 2026, https://simonwillison.net/2026/May/30/how-we-contain-claude/
- Configure the sandboxed Bash tool (Claude Code docs), 2026, https://code.claude.com/docs/en/sandboxing
- Choose a sandbox environment (Claude Code docs), 2026, https://code.claude.com/docs/en/sandbox-environments
- Connect Claude Code to an LLM gateway (Claude Code docs), 2026, https://code.claude.com/docs/en/llm-gateway-connect
- Gateway protocol reference (Claude Code docs), 2026, https://code.claude.com/docs/en/llm-gateway-protocol
- Claude Code errors reference (Claude Code docs), 2026, https://code.claude.com/docs/en/errors
- Responsible detection of generic secrets with Copilot secret scanning (GitHub Docs), https://docs.github.com/en/code-security/responsible-use/responsible-ai-generic-secrets
- Improvements to secret scanning and public monitoring (GitHub Changelog), 2026, https://github.blog/changelog/2026-07-15-improvements-to-secret-scanning-and-public-monitoring/
- Ghost Vectors: Soft-Deleted Embeddings Remain Reconstructible in HNSW Vector Databases, 2026, https://arxiv.org/pdf/2606.18497
- Three CVEs in Claude Code CLI (Phoenix Security), 2026, https://phoenix.security/claude-code-leak-to-vulnerability-three-cves-in-claude-code-cli-and-the-chain-that-connects-them/
- Critical Cursor Flaws Could Let Prompt Injection Escape Sandbox (The Hacker News), 2026, https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html
- Tool Annotations as Risk Vocabulary (MCP blog), 2026, https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- MCP Security Best Practices (spec 2026-07-28), https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices
- Canarying Releases (Google SRE Workbook), https://sre.google/workbook/canarying-releases/
- Implementing SLOs (Google SRE Workbook), https://sre.google/workbook/implementing-slos/
- CVE-2026-55607 advisory (GitLab), 2026, https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2026-55607/
- Anthropic Silently Patches Claude Code Sandbox Bypass (SecurityWeek), 2026, https://www.securityweek.com/anthropic-silently-patches-claude-code-sandbox-bypass/
- Fallbacks (Provider Failover) (LiteLLM docs), https://docs.litellm.ai/docs/proxy/reliability
- Response Headers (LiteLLM docs), https://docs.litellm.ai/docs/proxy/response_headers
- Claude Token Counter, now with model comparisons (Simon Willison), 2026, https://simonwillison.net/2026/Apr/20/claude-token-counts/
- GLiNER2-PII, 2026, https://arxiv.org/abs/2605.09973
- PIIBench, 2026, https://arxiv.org/abs/2604.15776
- Secret Breach Detection in Source Code with Large Language Models, 2025, https://arxiv.org/abs/2504.18784
- Secret Leak Detection in Software Issue Reports using LLMs (MSR 2026), https://arxiv.org/abs/2410.23657
- Agent Data Injection Attacks are Realistic Threats to AI Agents, 2026, https://arxiv.org/html/2607.05120v1
- Defense Against Indirect Prompt Injection via Tool Result Parsing, 2026, https://arxiv.org/abs/2601.04795
- Agentic Permissions Policy Algebra for Taint Confinement in LLM Agents (APPA), 2026, https://arxiv.org/abs/2607.24625
- Ghost in the Agent: Redefining Information Flow Tracking for LLM Agents (NeuroTaint), 2026, https://arxiv.org/abs/2604.23374
- Inside the LLM Call: GenAI Observability with OpenTelemetry (OpenTelemetry blog), 2026, https://opentelemetry.io/blog/2026/genai-observability/
- GenAI spans (OpenTelemetry semantic-conventions-genai), https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md
- Feature Toggles (Martin Fowler), https://martinfowler.com/articles/feature-toggles.html
- Rekor v2 GA (Sigstore blog), 2025, https://blog.sigstore.dev/rekor-v2-ga/
- Can I Get A Witness (Network)? (transparency.dev), https://blog.transparency.dev/can-i-get-a-witness-network
- SQLite Online Backup API, https://www.sqlite.org/backup.html
- Researchers Find 175,000 Publicly Exposed Ollama AI Servers (The Hacker News), 2026, https://thehackernews.com/2026/01/researchers-find-175000-publicly.html
- Route model inference requests across AWS Regions with cross-Region inference (AWS Bedrock docs), https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
- Clarify sandbox-exec deprecation timeline (apple/containerization issue 737), 2026, https://github.com/apple/containerization/issues/737
- OpenAI Codex CLI Sandbox Analysis Report (Agent Safehouse), 2026, https://agent-safehouse.dev/docs/agent-investigations/codex
- Article 12: Record-Keeping (EU AI Act explorer), https://artificialintelligenceact.eu/article/12/

Search result titles (not fetched):
- A Comparative Study of Software Secrets Reporting by Secret Detection Tools, 2023, https://arxiv.org/abs/2307.00714
- Defeating Prompt Injections by Design (CaMeL), 2025, https://arxiv.org/pdf/2503.18813
- Securing AI Agents with Information-Flow Control (FIDES), 2025, https://arxiv.org/abs/2505.23643
- QueryIPI: Query-agnostic Indirect Prompt Injection on Coding Agents, 2026, https://arxiv.org/abs/2510.23675
- MCP-38: A Comprehensive Threat Taxonomy for Model Context Protocol Systems, 2026, https://arxiv.org/pdf/2603.18063
- Model Context Protocol (MCP): Security Design Considerations (NSA CSI), 2026, https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF (fetch returned 403)
- Delegated bypass for push protection (GitHub Docs), https://docs.github.com/en/enterprise-cloud@latest/code-security/concepts/secret-security/about-delegated-bypass-for-push-protection
- Delegated bypass controls for push protection now available at the enterprise level (GitHub Changelog), 2025, https://github.blog/changelog/2025-09-16-delegated-bypass-controls-for-push-protection-now-available-at-the-enterprise-level/
- The State of Secrets Sprawl 2026 (GitGuardian), https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/
- Critical Claude Code Sandbox Vulnerability Enables Network Escape and Arbitrary File Write Attacks (Medium), 2026, https://medium.com/@Inforsecpro/critical-claude-code-sandbox-vulnerability-enables-network-escape-and-arbitrary-file-write-attacks-2186222829d4
- Health Check Driven Routing (LiteLLM docs), https://docs.litellm.ai/docs/proxy/health_check_routing
- Response header x-litellm-model-api-base is missing on chunked responses (LiteLLM issue 7249), https://github.com/BerriAI/litellm/issues/7249
- response body "model" field returns model group alias instead of resolved deployment model (LiteLLM issue 22709), https://github.com/BerriAI/litellm/issues/22709
- Token Counting Explained: tiktoken, Anthropic, and Gemini (Propel Code), 2025, https://www.propelcode.ai/blog/token-counting-tiktoken-anthropic-gemini-guide-2025
- Tokenizer Comparison, Part 2 (Medium), https://atul4u.medium.com/tokenizer-comparison-part2-comprehensive-tokenizer-performance-analysis-a8e0613bed0d
- Best Open Source Models for PII Redaction (Grepture), https://grepture.com/blog/best-open-source-models-pii-redaction
- Exposed Ollama Servers: Security Risks of Publicly Accessible LLM Infrastructure (Security Boulevard), 2026, https://securityboulevard.com/2026/03/exposed-ollama-servers-security-risks-of-publicly-accessible-llm-infrastructure/
- NIST SP 800-88 Rev. 2, Guidelines for Media Sanitization, 2025, https://csrc.nist.gov/pubs/sp/800/88/r2/final
- What is Cryptographic Erase as per NIST SP 800-88 Rev.2 (BitRaser), https://www.bitraser.com/blog/cryptographic-erase-and-supported-devices/
- NIST 800-88: Complete Guide to Media Sanitization (GoWorkwize), https://www.goworkwize.com/blog/what-is-nist-800-88-guide
- SQLite concurrent writes and "database is locked" errors (tenthousandmeters), https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/
- SQLite in Practice (1): The Database Is Locked Again! (DOCSAID), https://docsaid.org/en/blog/sqlite-wal-busy-timeout-for-workers/
- Sigstore Keyless Signing and Cosign Verification (systemshardening.com), https://www.systemshardening.com/articles/cicd/sigstore-keyless-signing/
- Verifying Software Integrity with Sigstore: The 2026 Cheat Sheet (techbytes), https://techbytes.app/posts/software-integrity-sigstore-cosign-rekor-cheat-sheet/
- Rekor v2 alpha (Sigstore blog), https://blog.sigstore.dev/rekor-v2-alpha/
- Can Cloudtrail support KMS code signing transparency logs (AWS re:Post), https://repost.aws/questions/QUJlrDBq-CRYurHVCIUNxbjw/can-cloudtrail-support-kms-code-signing-transparency-logs-e-g-by-logging-signatures
- Rethinking Tamper-Evident Logging: A High-Performance, Co-Designed Auditing System, 2025, https://arxiv.org/pdf/2509.03821
- What the EU AI Act requires for AI agent logging (Help Net Security), 2026, https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/
- OpenTelemetry GenAI Semantic Conventions (DEV Community), https://dev.to/x4nent/opentelemetry-genai-semantic-conventions-the-standard-for-llm-observability-1o2a
- OpenTelemetry for LLMs: Instrumentation Guide for a Multi-Provider AI Gateway (TrueFoundry), https://www.truefoundry.com/blog/opentelemetry-llm-gateway-instrumentation
