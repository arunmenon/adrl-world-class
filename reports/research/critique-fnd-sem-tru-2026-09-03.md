# Research-grounded critique: FND, SEM, TRU (2026-09-03)

Scope: ADRL-FND-001..005, ADRL-SEM-001..007, ADRL-TRU-001..003. Each decision is judged against sources fetched or surfaced by search on 2026-09-03. Every citation is tagged `(fetched)` when the URL was retrieved and read, or `(search result)` when only the title and snippet appeared in a search result. The 2026-09-02 and 2026-09-03 adversarial reviews already in the register are not repeated; where a finding overlaps, the new source that qualifies or strengthens it is what is reported.

Verdict scale: CURRENT (supported by 2025-2026 work), DATED (rests on pre-2025 work that newer work qualifies), CONTESTED (credible recent work on both sides), UNGROUNDED (no direct literature; first principles only).

---

## FND: System Boundary and Principles

**State of the field, 2026.** The LLM gateway is now a commodity layer with a vendor-published contract. Anthropic ships a machine-readable protocol (`GET /protocol`), documents which headers must be forwarded byte-for-byte, states that a gateway must "inspect without modifying", and now ships its own self-hosted Claude apps gateway inside the `claude` binary, doing SSO, managed settings, telemetry and cross-provider failover "without developers noticing". Third-party gateways (LiteLLM, Portkey, now owned by Palo Alto Networks, Kong 3.14, Cloudflare's unified API) have moved semantic features into the gateway: guardrails with fail-closed defaults, NVIDIA-backed model routing, scope-based tool filtering. Fail-open remains the Kubernetes admission default while every 2025-2026 security guidance says fail closed for security-bearing checks. Routing economics research (Mahmood, Feb 2026) finds static per-task routing beats cascades in nearly all cases, and cache-aware, session-affine routing is the serving-layer consensus. Governance discipline has shifted to pre-committed if-then thresholds (frontier safety frameworks; DeepMind's Tracked Capability Levels, April 2026), while the EU deferred high-risk AI obligations to December 2027 because the conformity-assessment infrastructure was not ready.

### ADRL-FND-001: Transparent control layer, protocol-scoped

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

### ADRL-FND-002: Semantic policy vs mechanical execution, deployment-set-closed

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

### ADRL-FND-003: Routing boundary is the user turn

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

### ADRL-FND-004: Fail to last-known-safe, not fail-open

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

### ADRL-FND-005: Scope expands only through measured gates

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

---

## SEM: Interaction Semantics

**State of the field, 2026.** Session and agent identity are now on the wire: Anthropic documents `x-claude-code-session-id`, per-spawn `x-claude-code-agent-id`, `x-claude-code-parent-agent-id`, and stable name-based teammate IDs; MCP added `Mcp-Session-Id` in 2025 but its 2026-07-28 release candidate reportedly removes sessions to make requests stateless. Compaction moved server-side on both major APIs: Anthropic's `compaction` block (beta `compact-2026-01-12`) and OpenAI's opaque, encrypted compaction item. Codex CLI speaks only the Responses API since February 2026. Subagents scale to 20 concurrent and three levels by default, with worktree isolation. Information-flow control for agents split into two camps: monotone attenuation (ChainCaps, Bounded Agents, FIDES at SaTML 2026) and permissive or recoverable propagation (permissive IFC v3, APPA), with an adaptive-evaluation critique of both. Dialogue segmentation research (When F1 Fails, CobSeg) now targets LLM context management directly but warns that strict boundary metrics mislead.

### ADRL-SEM-001: Mechanical classification of request classes

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

### ADRL-SEM-002: Session key from wire headers, then metadata

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

### ADRL-SEM-003: Continuations inherit the sticky route

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

### ADRL-SEM-004: Utility calls split by content exposure

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

### ADRL-SEM-005: Episode boundaries, enumerated and measured

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

### ADRL-SEM-006: Subagents inherit constraints now, routing later

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

### ADRL-SEM-007: Protocol profiles (Proposed)

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

---

## TRU: Trust, Residency and Egress

**State of the field, 2026.** Workload identity has reached agents: HashiCorp positions SPIFFE/SPIRE as the standard for agentic non-human identity (April 2026), AIP proposes invocation-bound capability tokens because "neither MCP nor A2A verifies agent identity" (March 2026), and Bounded Agents chains delegated authority (August 2026). Attestation research argues the signing identity must chain to a root outside the operator (Kettle, May 2026), while industry summits still call self-attestation an open problem. Residency is an endpoint property in practice: Bedrock's EU geographic inference profiles keep routing inside the EU and stamp `inferenceRegion` in CloudTrail (June 2026); Anthropic's first-party API has no EU inference region and Foundry EU is "coming"; Cloudflare's AI Gateway is incompatible with its own Regional Services. The EU deferred high-risk AI obligations to December 2027 but GPAI and transparency duties stand. Tamper-evident logging standardised on tile-based logs with signed checkpoints (Rekor v2 GA October 2025, static CT API, 2026 shards) and independent witness cosigning; CloudTrail's hourly signed digests remain the cloud baseline. Route receipts (May 2026) frame served-path disclosure as a trust requirement.

### ADRL-TRU-001: Authenticated workload identity (Proposed)

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

### ADRL-TRU-002: Permitted deployment set (Proposed)

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

### ADRL-TRU-003: Egress anchoring (Proposed)

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

---

## Verdict tally

| Verdict | Decisions |
|---|---|
| CURRENT | FND-001, FND-002, FND-003, FND-004, FND-005 (by analogy), SEM-001, SEM-003, SEM-005, SEM-007, TRU-001, TRU-002, TRU-003 |
| CONTESTED | SEM-002, SEM-006 |
| DATED | SEM-004 |
| UNGROUNDED | none |

## Sources

Fetched (URL retrieved and read on 2026-09-03):
- Anthropic, "Gateway protocol reference" (Claude Code docs, 2026), https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Claude apps gateway" (Claude Code docs, 2026), https://code.claude.com/docs/en/claude-apps-gateway
- Anthropic, "Create custom subagents" (Claude Code docs, 2026), https://code.claude.com/docs/en/sub-agents
- Anthropic, "Prompt caching" (Claude Platform docs, 2026), https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, "Compaction" (Claude Platform docs, 2026), https://platform.claude.com/docs/en/build-with-claude/compaction
- OpenAI, "Compaction" (API guide, 2026), https://developers.openai.com/api/docs/guides/compaction
- OpenAI, "Conversation state" (API guide, 2026), https://developers.openai.com/api/docs/guides/conversation-state
- Siddiqui et al., "Permissive Information-Flow Analysis for Large Language Models" (arXiv 2410.03055, v3 January 2026), https://arxiv.org/abs/2410.03055
- Kravchenko et al., "APPA: Recoverable Information-Flow Control for Real-World LLM Agents" (arXiv 2607.24625, July–August 2026), https://arxiv.org/abs/2607.24625
- Jiang et al., "ChainCaps: Composition-Safe Tool-Using Agents via Monotonic Capability Attenuation" (arXiv 2605.26542, May–July 2026), https://arxiv.org/abs/2605.26542
- Jing et al., "Isolation as a First-Class Principle for LLM-Agent System Safety" (arXiv 2607.12406, July–September 2026), https://arxiv.org/abs/2607.12406
- Muruaga, "Bounded Agents: Delegation Security for Multi-Agent AI Systems" (arXiv 2608.15888, August 2026), https://arxiv.org/abs/2608.15888
- Narisetty et al., "Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents" (arXiv 2606.26479, June 2026), https://arxiv.org/abs/2606.26479
- BerriAI/litellm PR #17785, "feat(guardrails): add configurable fail-open, timeout, and app_user tracking to panw_prisma_airs guardrail" (merged 2025-12-11), https://github.com/BerriAI/litellm/pull/17785
- Open Policy Agent, "Failing Closed | Gatekeeper", https://open-policy-agent.github.io/gatekeeper/website/docs/failing-closed/
- Sigstore blog, "Rekor v2 GA - Cheaper to run, simpler to maintain" (October 2025), https://blog.sigstore.dev/rekor-v2-ga/
- Prakash, "AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A" (arXiv 2603.24775, March 2026), https://arxiv.org/abs/2603.24775
- HashiCorp, "SPIFFE: Securing the identity of agentic AI and non-human actors" (April 2026), https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors
- Tallam, "Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure" (arXiv 2605.05440, May 2026), https://arxiv.org/abs/2605.05440
- Asad and Arko, "Kettle: Attested builds for verifiable software provenance" (arXiv 2605.08363, May 2026), https://arxiv.org/abs/2605.08363
- Coen, "When F1 Fails: Granularity-Aware Evaluation for Dialogue Topic Segmentation" (arXiv 2512.17083, December 2025), https://arxiv.org/abs/2512.17083
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2503.13657, 2025), https://arxiv.org/abs/2503.13657
- AWS Machine Learning Blog, "Unlocking AI flexibility in Europe: A guide to cross-region inference for EU data processing and model access" (June 2026), https://aws.amazon.com/blogs/machine-learning/unlocking-ai-flexibility-in-europe-a-guide-to-cross-region-inference-for-eu-data-processing-and-model-access/
- Schmalbach, "Model Routing as a Trust Problem: Route Receipts for Adaptive AI Systems" (arXiv 2605.01710, May 2026), https://arxiv.org/abs/2605.01710
- Mahmood, "Routing, Cascades, and User Choice for LLMs" (arXiv 2602.09902, February 2026), https://arxiv.org/abs/2602.09902
- Cloud Security Alliance, "EU AI Act's High-Risk Deadline: Deferred, Not Cancelled" (August 2026), https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/
- Kong, "Govern the Full AI Data Path with Kong AI Gateway 3.14" (April 2026), https://konghq.com/blog/product-releases/kong-ai-gateway-3-14
- Portkey, "Safeguard your AI requests with guardrails" (fetched; page did not expose the fail-open status-code detail, so it is not cited above), https://portkey.ai/features/guardrails

Search results only (title and snippet seen; URL not retrieved):
- LiteLLM, "Fallbacks (Provider Failover)", https://docs.litellm.ai/docs/proxy/reliability
- openai/codex, "Deprecating chat/completions support in Codex", Discussion #7782 (2025), https://github.com/openai/codex/discussions/7782
- Daniel Vaughan, "Codex CLI Custom Model Providers: The Complete Configuration Guide" (April 2026), https://codex.danielvaughan.com/2026/04/23/codex-cli-custom-model-providers-configuration-guide/
- OpenRouter, "Codex CLI with OpenRouter: config.toml Setup and Models" (2026), https://openrouter.ai/blog/tutorials/codex-cli-openrouter/
- Kong, "Intelligent Model Routing: Kong AI Gateway Applies NVIDIA NeMo Switchyard Across Model Traffic" (2026), https://konghq.com/blog/engineering/llm-routing-kong-ai-gateway-nvidia-nemo-switchyard
- Cloudflare, "AI Gateway Changelog" (unified API, May 2026), https://developers.cloudflare.com/changelog/product/ai-gateway/
- API Evangelist, "Cloudflare AI Gateway" third-party profile (2026), https://github.com/api-evangelist/cloudflare-ai-gateway
- OneUptime, "How to Configure Webhook FailurePolicy and TimeoutSeconds" (February 2026), https://oneuptime.com/blog/post/2026-02-09-webhook-failure-policy-timeout/view
- METR, "Common Elements of Frontier AI Safety Policies", https://metr.org/common-elements
- Google DeepMind, "Google DeepMind strengthens the Frontier Safety Framework" (April 2026), https://deepmind.google/blog/strengthening-our-frontier-safety-framework/
- DesignGurus, "How do you do progressive delivery (flags + canaries) safely?", https://www.designgurus.io/answers/detail/how-do-you-do-progressive-delivery-flags-canaries-safely
- LangChain, "Short-term memory" (docs), https://docs.langchain.com/oss/python/langchain/short-term-memory
- OpenAI, "Sessions - OpenAI Agents SDK", https://openai.github.io/openai-agents-python/sessions/
- Model Context Protocol, "Transports" (2025-03-26 specification), https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
- sergiobayona/vector_mcp, "streamable-http-spec-compliance.md" (claim that the 2026-07-28 RC removes session IDs), https://github.com/sergiobayona/vector_mcp/blob/main/docs/streamable-http-spec-compliance.md
- "AGENTSERVESIM: A Hardware-aware Simulator for Multi-Turn LLM Agent Serving" (arXiv 2606.09613, 2026), https://arxiv.org/pdf/2606.09613
- DigitalOcean, "DigitalOcean Inference Router, Now Cache-Aware" (2026), https://www.digitalocean.com/blog/inference-router-cache-aware
- "RLM-Cascade: Response-Level Speculative Decoding for Cost-Efficient LLM API Serving" (arXiv 2606.22840, 2026), https://arxiv.org/html/2606.22840
- badlogic, "Context Compaction Research: Claude Code, Codex CLI, OpenCode, Amp" (gist, 2026), https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f
- "CobSeg: Coherence Boundary Modeling for Dialogue Topic Segmentation" (arXiv 2605.30668, May 2026), https://arxiv.org/abs/2605.30668
- "S3C2 Summit 2025-07: Government Secure Supply Chain Summit" (arXiv 2605.29140), https://arxiv.org/pdf/2605.29140
- "Ethical Hyper-Velocity (EHV): A Hardware-Rooted Zero-Trust Runtime Enforcement Architecture for Agentic AI Systems" (arXiv 2605.17909, 2026), https://arxiv.org/pdf/2605.17909
- InfoQ, "Claude Reaches GA on Microsoft Foundry: European Enterprises Cannot Deploy It" (July 2026), https://www.infoq.com/news/2026/07/claude-foundry-ga-europe/
- Anthropic Privacy Center, "Where are your servers located? Do you host your models on EU servers?", https://privacy.anthropic.com/en/articles/7996890-where-are-your-servers-located-do-you-host-your-models-on-eu-servers
- transparency.dev, "Can I Get A Witness (Network)?", https://blog.transparency.dev/can-i-get-a-witness-network
- transparency-dev/witness (GitHub), https://github.com/transparency-dev/witness
- AWS, "Validating CloudTrail log file integrity", https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html
- C2SP, "The Static Certificate Transparency API" v1.1.0, https://c2sp.org/static-ct-api@v1.1.0
- Costa and Köpf, "Securing AI Agents with Information-Flow Control" (FIDES; arXiv 2505.23643; SaTML 2026), https://arxiv.org/abs/2505.23643 (background only; not cited in a bullet)
- Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL; arXiv 2503.18813, 2025), https://arxiv.org/abs/2503.18813 (background only; not cited in a bullet)
