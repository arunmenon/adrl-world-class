# SEM — Interaction Semantics

**Core question:** What does this request or interaction mean?
**Owns / does not own:** Owns request, turn, continuation, session, episode, utility-call and subagent meaning. Does not own which model wins for a classified turn.

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-SEM-001 | Mechanical classification of request classes | AMEND | D3 → D3 | Taxonomy lacks the pre-warm request; ignores documented `x-claude-code-*` headers; "passthrough unchanged" sends full-prompt `count_tokens` bodies around the pin; needs a content-bearing flag; Codex out of scope |
| ADRL-SEM-002 | Session key from wire headers, then metadata | AMEND | D3 → D3 (derivation); D1 (durability) | `metadata.user_id` is documented as a *user* id for abuse detection; `x-claude-code-session-id` is the documented session key; fallback undefined; must compose with agent lineage; hash at rest |
| ADRL-SEM-003 | Continuations inherit the sticky route | APPROVE | D2 → D3 | Best-evidenced rule in the bucket (real-traffic cache-hit measurement); rationale corrected on signature portability; "no difficulty decision" must not be read as "no gates" |
| ADRL-SEM-004 | Utility calls split by content exposure | AMEND | D3 → D2 | Compaction is context-bearing and quality-critical, not housekeeping; utility calls carry transcript content and must respect pins; pre-warm fingerprints as utility |
| ADRL-SEM-005 | Episode boundaries, enumerated and measured | AMEND | D2 → D2 | Unfalsifiable as written; signals enumerated; harness's own `isNewTopic` call is a free candidate signal; boundaries release hysteresis only, never pins; two shadow metrics defined |
| ADRL-SEM-006 | Subagents inherit constraints now, routing later | AMEND | D0 → D0 (routing); D2 required for constraint inheritance before pilot | Interim passthrough sends forked subagents' full parent transcript around the pin; lineage headers make constraint inheritance a lookup; harness model choice must be honoured |

Tally: 1 APPROVE, 5 AMEND, 0 REJECT.

## Cross-cutting findings

1. **The harness now publishes the identity SEM was reverse-engineering.** Anthropic's gateway contract documents `x-claude-code-session-id`, `x-claude-code-agent-id` (subagent requests only, fresh per spawn) and `x-claude-code-parent-agent-id` (nested agents), and notes teammate agents reuse stable name-based IDs. SEM-001, SEM-002 and SEM-006 were written before or without these; each is amended to prefer the header over body heuristics, with the body heuristic retained as fallback and a divergence counter.

2. **Three request classes carry the conversation and were treated as not-our-problem.** `count_tokens` (full prompt, ~72% of wire volume), utility calls (title text, topic-detect turns, the entire transcript for compaction) and forked subagents (the whole parent conversation) all leave the machine under the original SEM-001/004/006 interims regardless of pin state. SEM-001 now labels every class with a content-bearing flag; SAF-002 consumes it. This is the seam finding shared with SAF.

3. **Two real-traffic request types were missing from the taxonomy.** The cache pre-warm request (`max_tokens: 1`, full tool list, sent in parallel with Haiku metadata requests) and the harness's topic-detection call (`isNewTopic` JSON). The first misfiles as a user turn or a utility call; the second is a free episode-boundary signal SEM-005 should read rather than reinvent.

4. **"Turn" and "gate" were conflated across FND-003 / SEM-003 / SAF-003.** Routing once per turn is right and evidenced; gating once per turn misses the tool results that carry secrets. SEM-003 is approved because its sentence scopes itself to the *difficulty* decision; SAF-001 and FND-003 carry the per-request gating amendment.

5. **Signature portability was mis-stated in the rationale.** Anthropic documents thinking signatures as compatible across the Claude API, Bedrock and Vertex; the incompatibility is across *model vendors* (Claude→non-Claude), and OpenAI reasoning items are reusable only within a GPT model family. The conclusion (never switch vendors mid-turn) is unchanged; the reason is corrected so an engineer configuring multi-platform frontier rungs is not misled.

6. **Compaction is the under-examined event.** It is not an episode boundary (task continues), it is the harness's context-reduction path that SAF-005's block must trigger, its request is content-bearing (must go local on a pinned lineage), and a compaction summary written by a small local model degrades every later frontier turn invisibly. SEM-004 splits utility calls on exactly this property; SEM-005 excludes compaction from boundaries; SAF-005 checks the local rung can hold the compaction request at configuration time.

7. **Durability is a SEM problem too.** Session→route state (and therefore pin state) lives in a single-process Python dict. SEM-002's key indexes memory that does not survive a restart; SEM-006's parallel subagents race on it. Both amendments require lineage-qualified keys and defer durability to SAF-002/MEM.

8. **Codex CLI.** Named as a harness in FND-001; speaks only the Responses API; nothing in this bucket applies. Proposed: ADRL-SEM-007 (Responses-format discriminator and session key), status Proposed, D0 — not written as a file in this review because no corpus or design exists to review; recorded here so the gap is on the register.

## Sources consulted

- Anthropic, "Gateway protocol reference" (Claude Code docs) — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Connect Claude Code to an LLM gateway" (Claude Code docs) — https://code.claude.com/docs/en/llm-gateway-connect
- Anthropic, "Messages API" reference — https://platform.claude.com/docs/en/api/messages
- Anthropic, "Token counting" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/token-counting
- Anthropic, "Prompt caching" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, "Thinking" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/thinking
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- Anthropic, "Compaction" (Claude Platform docs; title from search) — https://platform.claude.com/docs/en/build-with-claude/compaction
- Anthropic, "Create custom subagents" (Claude Code docs) — https://code.claude.com/docs/en/sub-agents
- OpenAI, "Reasoning models" (API guide) — https://developers.openai.com/api/docs/guides/reasoning
- George Sung, "Tracing Claude Code's LLM Traffic: Agentic loop, sub-agents, tool use, prompts" (Medium, 2026) — https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5
- anthropics/claude-code issue #10548, "[FEATURE] auto-compact with Haiku" (title from search) — https://github.com/anthropics/claude-code/issues/10548
- "An Unsupervised Dialogue Topic Segmentation Model Based on Utterance Rewriting" (arXiv 2409.07672) — https://arxiv.org/abs/2409.07672
- Google SRE, "Canarying Releases" (The Site Reliability Workbook) — https://sre.google/workbook/canarying-releases/
- Costa, Köpf et al., "Securing AI Agents with Information-Flow Control" (arXiv 2505.23643) — https://arxiv.org/abs/2505.23643
