# ADRL-FND-003 — Routing boundary is the user turn

| Field | Value |
|---|---|
| Bucket | FND — System Boundary and Principles |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D3 Shadow (cache-hit evidence on real traffic supports it; the warm-up-request and subagent edge cases need golden tests before D4) |
| Review verdict | AMEND |
| Tenets | 1, 6 |
| Related decisions | SEM-001, SEM-003, SEM-004, SEM-006, SAF-001, CAS-003, CAS-005, RTG-005 |
| Open questions | Q3 |

## Decision

The normal routing boundary is a user turn, not every HTTP request; a user turn is the first request in an agent lineage whose latest message is developer-authored content and which is neither a utility call, a passthrough call, nor a harness pre-warm request.

1. Routing (rung selection) happens once per user turn; hard gates (SAF-001) run on every request regardless of class.
2. The harness's cache pre-warm request — a request carrying the full tool list and conversation prefix with `max_tokens: 1` — is not a turn boundary and inherits the current sticky route.
3. Each agent lineage (parent, and each subagent identified by `x-claude-code-agent-id`) has its own turn boundary; a subagent's first request is its own boundary, not a continuation of the parent's turn (SEM-006).
4. The only in-turn route change permitted is a CAS escalation at an action boundary.

## Context and rationale

One instruction is not one request. You type "fix the failing test"; the harness then sends perhaps fifteen HTTP requests. Only the first carries a new decision; the other fourteen are the model working. Deciding fifteen times means re-deciding fourteen times with no new information — and because context grows with every handshake, any rule that scores context size ratchets upward until it flips models mid-task. Phase 0 measured a very high prompt-cache hit ratio on real traffic, which vindicates never switching mid-turn.

The amendment makes "user turn" mechanical rather than intuitive. Claude Code's real traffic includes a pre-warm request (full tool list, `max_tokens: 1`) fired in parallel with metadata requests at the start of a conversation, background Haiku calls for titles and topic detection, and subagent requests whose latest message is a task-delegation message written by the parent model, not the developer. Each of these can look like "a user turn" to a discriminator that only checks the role of the last message. The amendment also separates *routing* (once per turn) from *gating* (every request), because the ingress vector for secrets is the tool result, not the typed instruction.

## Adversarial review (2026-09-02)

### Steelman
Turn-scoped routing is the single most-validated idea in the register: Anthropic's prompt cache requires an identical prefix and is model-specific, so any mid-turn switch throws away the cached prefix at exactly the moment the transcript is largest, and Phase 0 measured the cache-hit ratio that proves the point. It also removes the context-size ratchet by construction. Every alternative (per-request scoring, periodic re-evaluation) reintroduces oscillation.

### Attacks
1. **The pre-warm request is a fake turn.** Sung's wire trace of Claude Code shows "a dummy request with max_tokens=1 and the full tool list … sent in parallel with metadata requests, likely to pre-fill the cache". If the discriminator classifies this as the user turn, the rung is decided on a dummy prompt, the real instruction arrives next and is treated as a continuation, and the pre-warm goes to whichever rung the dummy earned. Worse, if it goes local, the frontier cache is never warmed and the first real turn pays a full cache write. The register's taxonomy (SEM-001) has no class for it.
2. **"Once per turn" has been read as "gate once per turn".** SAF-003 says detection happens "before routing". If routing happens once per turn, and detection is bound to routing, then the fourteen continuation requests — the ones that carry `cat .env`, `aws configure list`, or a test fixture with a live key back into the context as `tool_result` blocks — are never scanned. The turn boundary is the right unit for *optimisation*; it is the wrong unit for *gating*. The decision must say both.
3. **Subagent requests break the lineage assumption.** Claude Code subagents run in isolated context windows, in parallel, up to three levels deep, and a *fork* inherits the parent's entire conversation. A fork's first request looks like a continuation of the parent (same prefix); a fresh subagent's first request looks like a new user turn (its last message is the delegation text). Without agent-lineage keying, a turn decision made for the parent leaks to siblings, or each sibling triggers a fresh decision on the parent's session state, and a Python-dict session→route map has a race between concurrent siblings.
4. **Context growth is not the only ratchet.** The rationale argues turn-scoping removes the context-size ratchet. It does not remove the *feasibility* ratchet: a continuation can exceed the local rung's window mid-turn (SAF-006), at which point "inherit the route" produces a request the route cannot serve. The decision should acknowledge that the sticky route is inherited *subject to feasibility*, and that infeasibility mid-turn is a CAS/SAF event, not a routing re-decision.
5. **Compaction resets the prefix anyway.** When Claude Code compacts, the transcript is replaced by a summary; the cache prefix is gone regardless of what ADRL does. The cache argument therefore justifies "never switch *between* compactions", which is weaker than "never switch mid-turn" but also suggests compaction is the natural cheap point to re-decide — something SEM-005's episode boundary does not currently consider.

### Evidence
- Anthropic, "Prompt caching" (Claude Platform docs) — cache hits require an identical prefix ("Cache hits require 100% identical prompt segments"), 5-minute default TTL measured from request start, and tool/system/message ordering invalidates downstream cache; the page does not state cross-model cache reuse explicitly — model-specificity is implied by per-model minimum cacheable lengths and the "Dropped thinking blocks" invalidation row; supports the steelman and bears on attacks 1, 5 — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- George Sung, "Tracing Claude Code's LLM Traffic" (Medium, 2026) — documents the pre-warm request (`max_tokens=1`, full tool list, sent in parallel with Haiku metadata requests) and subagent request shapes; bears on attacks 1, 3 — https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5
- Anthropic, "Create custom subagents" (Claude Code docs) — subagents have isolated context, run in parallel, nest up to three levels, and forks inherit the whole parent conversation; bears on attack 3 — https://code.claude.com/docs/en/sub-agents
- Anthropic, "Gateway protocol reference" (Claude Code docs) — `x-claude-code-session-id`, `x-claude-code-agent-id`, `x-claude-code-parent-agent-id` headers identify session and agent lineage without parsing bodies; bears on attack 3 — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude Platform docs) — "a tool-use loop is one assistant turn"; thinking blocks must be passed back within the turn; supports the steelman's definition of turn — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows

### Verdict
**AMEND.** The principle is vindicated by the cache evidence and stands. Attacks 1, 2 and 3 land as under-specification: "user turn" was never defined mechanically, the pre-warm request is a documented real-traffic class the taxonomy lacks, gating was left ambiguous, and agent lineage was not part of the definition. Attack 4 is answered by the existing CAS/SAF machinery but the text should reference it (sub-clause 4). Attack 5 is a genuine observation that feeds SEM-005 rather than changing this decision.

## Amendments applied

- Appended a mechanical definition of "user turn" (first request in an agent lineage whose latest message is developer-authored, excluding utility, passthrough and pre-warm).
- Added sub-clause 1 separating routing-once-per-turn from gating-every-request.
- Added sub-clause 2 classifying the pre-warm request as a non-boundary that inherits the sticky route.
- Added sub-clause 3 making the boundary per agent lineage.
- Added sub-clause 4 naming CAS escalation as the only in-turn route change.

## Follow-ups

- [ ] Golden test from a captured handshake: pre-warm request (`max_tokens: 1`, full tools) followed by the real first turn → assert the rung decision is made on the real turn and the pre-warm inherits.
- [ ] Golden test: parallel subagent requests with distinct `x-claude-code-agent-id` → assert independent turn boundaries and no shared sticky-route state between siblings.
- [ ] Measurement (shadow): fraction of turns in which the pre-warm or a Haiku metadata call was misclassified as the turn boundary under the current discriminator.
- [ ] Add to SEM-005's candidate boundary list: post-compaction first turn (cache prefix is already cold).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: mechanical definition of user turn; pre-warm excluded; gating per request; per-lineage boundary | "The normal routing boundary is a user turn, not every HTTP request." |
