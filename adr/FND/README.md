# FND — System Boundary and Principles

**Core question:** Who owns what, and what invariants govern the system?
**Owns / does not own:** Owns the product boundary, control-plane ownership, invariants and architectural shape. Does not own individual routing thresholds or model training.

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-FND-001 | Transparent control layer, protocol-scoped | AMEND | D3 → D3 (Anthropic path); D0 (Codex path) | "Transparent" contradicts SAF-004/005 and documented harness capability-degradation; must be wire-level, with enumerated exceptions; Codex CLI is Responses-API only and unevidenced |
| ADRL-FND-002 | Semantic policy vs mechanical execution, rung-closed | AMEND | D2 → D2 | LiteLLM context-window/content-policy fallbacks are semantic and can cross rungs, breaking pins; gateway content guardrails overlap SAF and need an authority rule |
| ADRL-FND-003 | Routing boundary is the user turn | AMEND | D3 → D3 | Principle vindicated by cache evidence; "user turn" undefined mechanically; pre-warm request misfiles as a turn; gating must be per request; boundary must be per agent lineage |
| ADRL-FND-004 | Fail to last-known-safe, not fail-open | REJECT | D4 → D3 | Blanket fail-open sends pinned sessions to the cloud on scanner failure, contradicting SAF-002/004; proxy death has no in-process fallback; no pilot population exists for D4 |
| ADRL-FND-005 | Scope expands only through measured gates | APPROVE | D3 → D3 (governance note) | Sound and currently honoured; gaps (self-graded, no pre-registration, no de-promotion) belong to EVL follow-ups |

Tally: 1 APPROVE, 3 AMEND, 1 REJECT.

## Cross-cutting findings

1. **The escape hatch beats the safety gate.** FND-004's universal fail-open, at D4, is ordered above the D2 privacy gates it can override. For unpinned sessions fail-open is the right default (baseline was cloud anyway); for pinned sessions it is a textbook security anti-pattern. The replacement splits behaviour by pin state and by failure class (routing / gate / proxy) and requires every fail-open to be recorded and rate-alerted. This interacts with SAF-001, SAF-002, SAF-004 and the proposed SAF-009.

2. **The gateway is not a passive executor.** LiteLLM's documented context-window and content-policy fallbacks change the model class in response to content. Unless fallback groups are rung-closed (and local-only for pinned traffic), the FND-002 split leaks: a pinned request that overflows local can be served by cloud with no policy involved. The amendment introduces a shared, versioned rung configuration consumed by both ADRL and the gateway config. Q7's boundary question is answered for fallbacks (rung-closed) and for overlapping content controls (ADRL authoritative, gateway defence in depth).

3. **Transparency has documented limits the register did not own.** Anthropic's gateway contract says Claude Code sends adaptive `thinking` to unrecognised model names and, when an upstream rejects `thinking`, a thinking signature, a mid-conversation system message or `cache_control`, "disables the rejected capability for the rest of the conversation". A first turn routed to a local model without ADRL stripping those fields can therefore degrade the whole session invisibly. FND-001 now assigns the rewrite to ADRL and lists the permitted developer-visible surfaces.

4. **Codex CLI is named but not supported.** Codex speaks only the OpenAI Responses API. Nothing in SEM applies to it and no corpus exists. FND-001 scopes it out; SEM proposes a separate discriminator ADR.

5. **"User turn" was never defined.** Real Claude Code traffic includes a cache pre-warm request (`max_tokens: 1`, full tool list), Haiku metadata calls, and subagent forks whose bodies are indistinguishable from parent continuations. FND-003 now defines the boundary mechanically and per agent lineage, and separates routing-once-per-turn from gating-every-request — the latter being the single largest privacy finding of the review (see SAF README).

6. **Maturity labels certified text rather than behaviour in two places** (FND-004 D4; SAF-007 D2). FND-005 is approved precisely because it is the decision that licenses this review to lower them; its follow-ups (pre-registered thresholds, de-promotion triggers, named independent approver) are the machinery that would have caught both earlier.

## Sources consulted

- Anthropic, "Gateway protocol reference" (Claude Code docs) — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Connect Claude Code to an LLM gateway" (Claude Code docs) — https://code.claude.com/docs/en/llm-gateway-connect
- Anthropic, "Prompt caching" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- Anthropic, "Create custom subagents" (Claude Code docs) — https://code.claude.com/docs/en/sub-agents
- LiteLLM, "Fallbacks (Provider Failover)" — https://docs.litellm.ai/docs/proxy/reliability
- LiteLLM, "Secret Detection/Redaction (Enterprise-only)" — https://docs.litellm.ai/docs/proxy/guardrails/secret_detection
- LiteLLM, "PII, PHI Masking - Presidio" — https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2
- AWS, "Understanding intelligent prompt routing in Amazon Bedrock" — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- OpenAI, "Reasoning models" (API guide) — https://developers.openai.com/api/docs/guides/reasoning
- Daniel Vaughan, "Codex CLI Custom Model Providers: The Complete Configuration Guide" (blog, Apr 2026) — https://codex.danielvaughan.com/2026/04/23/codex-cli-custom-model-providers-configuration-guide/
- George Sung, "Tracing Claude Code's LLM Traffic: Agentic loop, sub-agents, tool use, prompts" (Medium, 2026) — https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5
- AuthZed, "Understanding 'Failed Open' and 'Fail Closed' in Software Engineering" — https://authzed.com/blog/fail-open
- gardener/gardener issue #7013, "Webhook with `failurePolicy=Ignore` can be problematic" — https://github.com/gardener/gardener/issues/7013
- Cisco Community, "Fail-open & Fail-close explanation" (title from search) — https://community.cisco.com/t5/security-knowledge-base/fail-open-amp-fail-close-explanation/ta-p/5012930
- Google SRE, "Canarying Releases" (The Site Reliability Workbook, ch. 16) — https://sre.google/workbook/canarying-releases/
- NASA, "Technology Readiness Levels" — https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/
- Basak et al., "A Comparative Study of Software Secrets Reporting by Secret Detection Tools" (arXiv 2307.00714) — https://arxiv.org/abs/2307.00714
