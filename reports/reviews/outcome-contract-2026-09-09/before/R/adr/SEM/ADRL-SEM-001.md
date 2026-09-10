# ADRL-SEM-001 — Mechanical classification of request classes

| Field | Value |
|---|---|
| Bucket | SEM — Interaction Semantics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D3 Shadow (single-user corpus; pre-warm class and header-based signals must be added to the canary tests before D4) |
| Review verdict | AMEND |
| Tenets | 1, 4 |
| Related decisions | FND-001, FND-003, SEM-002, SEM-003, SEM-004, SEM-006, SAF-001, SAF-002, SAF-003 |
| Open questions | Q3 |

## Decision

Requests are mechanically classified, using request shape and the harness's wire headers, as user turns, continuations, utility calls, subagent requests, pre-warm requests, or passthrough traffic; every class is subject to the SAF gates, and classification is fail-safe to passthrough only for unpinned sessions.

1. Mechanical signals include: the role and block types of the final message (`tool_result` ⇒ continuation), `max_tokens`, system-prompt shape, tool-list shape, endpoint path (`/v1/messages/count_tokens` ⇒ passthrough), and the `x-claude-code-session-id`, `x-claude-code-agent-id` and `x-claude-code-parent-agent-id` headers (agent-id present ⇒ subagent lineage).
2. Passthrough and utility requests carry conversation content (a `count_tokens` body is the full prompt; a compaction request is the full transcript) and are therefore *content-bearing*; the classifier labels every class with a content-bearing flag that SAF-002/SAF-003 consume.
3. The taxonomy is for Anthropic-Messages-format traffic; Responses-format traffic (Codex CLI) is unclassified and out of scope until a separate corpus and discriminator exist.

## Context and rationale

Five kinds of traffic look identical on the wire; treating them the same is the original sin. Every request arriving at the proxy is a `POST /v1/messages` (or `count_tokens`). Underneath it is a new user turn, a continuation, a utility call, a subagent, or protocol passthrough — the last was ~72% of raw wire volume and missing from the taxonomy until the corpus revealed it. "Mechanically" matters: classification uses request shape, not an LLM's opinion, so it is cheap and auditable.

The amendment adds three things the corpus and the vendor's own contract make necessary. Anthropic now documents session and agent identity *headers* on every Claude Code request, which is a stronger mechanical signal than any body heuristic and makes subagent detection exact. Real traffic contains a pre-warm request (`max_tokens: 1`, full tools) that the taxonomy would otherwise misfile as a user turn. And the "passthrough" label has been read as "not our concern", when a `count_tokens` request carries the whole prompt — the class with the most traffic is also the class most likely to carry a pinned session's code to the cloud unnoticed.

## Adversarial review (2026-09-02)

### Steelman
Shape-based classification is the only auditable option: it is deterministic, testable from captured fixtures (`tests/fixtures/handshakes`, `test_discriminator_canary.py`), costs microseconds, and cannot be prompt-injected. The corpus-driven discovery that passthrough was 72% of volume shows the method self-corrects when reality differs from the design. Everything downstream (turn boundary, sticky route, gates) is only as good as this classifier, and a mechanical classifier is the one you can prove things about.

### Attacks
1. **The pre-warm request is missing from the taxonomy.** Sung's trace shows Claude Code sends a dummy request with `max_tokens=1` and the full tool list in parallel with the Haiku metadata calls. Its final message is user-authored, so a last-message-role heuristic files it as a user turn, and the actual instruction that follows becomes a "continuation". Five classes are one short.
2. **The classifier ignores the strongest available signal.** Anthropic's gateway contract documents `x-claude-code-session-id`, `x-claude-code-agent-id` (present only on subagent requests) and `x-claude-code-parent-agent-id` (nested agents). Subagent detection by system-prompt fingerprint is fragile across Claude Code releases; the header is exact. SEM-006's "none of it is built" is partly because the design predates the headers.
3. **"Passthrough … unchanged" is a privacy hole.** `count_tokens` accepts "the same structured inputs as the Messages API" — system, tools, messages, thinking blocks. If a session is pinned local and the harness's token-count call is passed through "unchanged" to the cloud gateway, the full pinned context leaves the machine on the highest-volume request class. Classification is correct; the *consequence* attached to the class is wrong, and the decision text ("pass through unchanged") encourages it.
4. **Utility calls are content-bearing.** Title generation includes the user's message; topic detection includes recent turns; compaction includes the entire transcript. Labelling them "housekeeping" (SEM-004) hides that they are the second-largest exfiltration surface. The classifier must expose a content-bearing bit rather than leave it to each consumer to remember.
5. **Fork subagents are indistinguishable by body.** A Claude Code fork "inherits the entire conversation so far … sees the same system prompt, tools, model, and message history as the main session." By body shape it *is* the parent's continuation; only `x-claude-code-agent-id` distinguishes it. A body-only classifier will merge fork traffic into the parent's turn and sticky route.
6. **Single-user corpus.** The taxonomy was derived from one developer's workflow-heavy traffic. Classes that appear in other workflows (agent teams with stable name-based IDs, MCP tool-search `tool_reference` blocks, `context_management` edits) are untested. The canary test suite is only as representative as the fixtures.
7. **Codex CLI is unclassifiable.** The Responses API has `input` items, `function_call_output`, reasoning items and `previous_response_id` — none of the Messages-shape heuristics apply, and the register names Codex as a harness (FND-001).

### Evidence
- Anthropic, "Gateway protocol reference" (Claude Code docs) — defines `x-claude-code-session-id`, `x-claude-code-agent-id`, `x-claude-code-parent-agent-id`; `count_tokens` is optional and Claude Code falls back to counting via the inference endpoint when absent; bears on attacks 2, 3, 5 — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Token counting" (Claude Platform docs) — `count_tokens` accepts the same inputs as Messages (system, tools, images, PDFs, thinking blocks, messages), is free, separately rate-limited; bears on attack 3 — https://platform.claude.com/docs/en/build-with-claude/token-counting
- George Sung, "Tracing Claude Code's LLM Traffic" (Medium, 2026) — pre-warm request (`max_tokens=1`, full tools, Opus), Haiku metadata requests (title, `isNewTopic` topic detection, suggestions), subagent request characteristics; bears on attacks 1, 4 — https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5
- Anthropic, "Create custom subagents" (Claude Code docs) — forks inherit the entire parent conversation; subagents run in parallel and nest; bears on attack 5 — https://code.claude.com/docs/en/sub-agents
- Anthropic, "Messages API" reference — `metadata.user_id` is an opaque external user identifier (≤512 chars) used for abuse detection; `tool_result` block param; background for the shape heuristics — https://platform.claude.com/docs/en/api/messages
- OpenAI, "Reasoning models" (API guide) — Responses-format reasoning items and stateless `encrypted_content`; bears on attack 7 — https://developers.openai.com/api/docs/guides/reasoning

### Verdict
**AMEND.** The method is right and the verdict is not in doubt; the taxonomy is incomplete (attack 1), under-uses documented signals (attacks 2, 5), and attaches a dangerous default to its largest class (attacks 3, 4). Those four are textual changes. Attacks 6 and 7 are scope: they do not invalidate the decision, they bound its evidence. The single most important consequence of this review is sub-clause 2 — the classifier must tell SAF which classes carry content, because the pin has to cover them.

## Amendments applied

- Added "pre-warm requests" as a sixth class and "using request shape and the harness's wire headers" to the method.
- Added "every class is subject to the SAF gates" and made fail-safe-to-passthrough conditional on the session being unpinned.
- Added sub-clause 1 enumerating the mechanical signals, including the three `x-claude-code-*` headers.
- Added sub-clause 2 introducing the content-bearing flag for passthrough and utility classes.
- Added sub-clause 3 scoping out Responses-format traffic.

## Follow-ups

- [ ] Add pre-warm fixtures to `tests/fixtures/handshakes` and a canary assertion that they are never classified as user turns.
- [ ] Extend `router/discriminator.py` to read `x-claude-code-agent-id` / `-parent-agent-id` and prefer them over system-prompt fingerprints for the subagent class; keep the fingerprint as fallback with a divergence counter.
- [ ] Golden test: pinned session + `count_tokens` request → request is served locally (local tokenizer estimate) or rejected, never forwarded to the cloud gateway.
- [ ] Emit `content_bearing: true|false` per classified request into telemetry; SAF-002 consumes it.
- [ ] Corpus expansion: capture at least three additional developers' traffic (including agent-team and MCP tool-search usage) before claiming D4 for the classifier.
- [ ] Proposed ADR (SEM-007): Responses-format discriminator for Codex CLI, status Proposed, D0.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: pre-warm class added; wire headers as signals; content-bearing flag; gates on every class; Responses format scoped out | "Requests are mechanically classified as user turns, continuations, utility calls, subagents, or passthrough traffic." |
