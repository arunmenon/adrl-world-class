# ADRL-CAS-004 — Cross-model handoff: provider-pair rules, not one stripping rule

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D2 Tested — shadow mode cannot exercise a cross-provider continuation (it never sends the transformed transcript to the target model), so "shadow evidence" here is evidence that the transformation *runs*, not that any provider *accepts* it; D3 should be re-claimed only after replay tests against each live provider pair pass |
| Review verdict | AMEND |
| Tenets | 5, 7 |
| Related decisions | CAS-003, CAS-005, CAS-006, RTG-008, RTG-009, SEM-003, SAF-003, FND-002 |
| Open questions | Q7 |

## Decision

Cross-model continuation preserves tool IDs and tool results, transforms private reasoning according to a versioned per-provider-pair rule (strip, keep, or let the API drop), and appends a short, mechanically generated, clearly delimited handoff note at the end of the last user message — never in the system prompt — listing the escalation cause and the side-effecting actions already executed.

1. Reasoning blocks: the rule is keyed by (source model family, target model family, thinking enabled on target). Anthropic→Anthropic within a family that can read the blocks: keep them (the API requires the latest assistant message's thinking blocks to be unmodified when thinking is enabled, and drops unreadable older-model blocks itself). Anthropic→non-Anthropic or OpenAI→anything: strip `thinking`, `redacted_thinking` and encrypted reasoning items, and disable thinking-continuation parameters on the first request after handoff. The rule table is versioned config; an unknown pair defaults to strip-and-disable.
2. Tool identity: `tool_use.id`/`tool_result.tool_use_id` pairs are preserved verbatim within a provider and mapped 1:1 (with the mapping recorded on the outcome row) when the target provider's id format differs; every `tool_use` in the transcript retains a matching result (CAS-003 clause 1) and tool-result content types the target cannot accept are downgraded to text with an explicit marker.
3. Handoff note: generated from ledger fields only (trip-wire type, rung from/to, executed side-effecting tool calls per CAS-003 clause 3, verifier result if any); never model-authored; placed after all `tool_result` blocks in the last user message (provider ordering rule) and wrapped in a fixed delimiter so it is distinguishable from user text and cannot be mistaken for an instruction from the developer. The note's schema version is recorded on the outcome row.
4. Cache: a handoff is a cache-cold event on the target by construction (different model, different prefix); its cost is charged per RTG-009. Nothing in the handoff may modify `tools` or `system`, so the *source* rung's cache survives if the episode later returns to it.

## Context and rationale

Hand over the chart, not the patient's story again. On escalation the stronger model receives the tool ids and tool results already gathered; the previous model's private reasoning is stripped, because thinking-block signatures and encrypted reasoning items do not transfer across providers and would be rejected; a short handoff note is added. The provider documentation makes the picture more specific than "strip": Anthropic *requires* thinking blocks to be passed back unmodified within the latest assistant turn when thinking is on (a 400 error otherwise), automatically drops blocks an earlier model cannot read, and lets newer models keep reading older blocks; OpenAI's encrypted reasoning "can be reused only within the same model family". So one stripping rule is wrong in both directions — it breaks a same-family Anthropic escalation with thinking on, and it is unnecessary where the API drops blocks itself. Gateway translation layers have hit exactly these bugs. The amendment replaces the single rule with a versioned per-pair table and makes the handoff note a mechanical artefact with a fixed position and delimiter, because a free-text note injected into the user turn is otherwise both a prompt-injection surface and an unversioned prompt.

## Adversarial review (2026-09-02)

### Steelman
Preserving tool ids and results is the minimum that keeps the protocol valid and the cache of *observations* intact; stripping reasoning is the minimum that keeps the target provider from rejecting the request; a short note is the minimum that tells the new model why it is here. The design is deliberately lossy on the one thing that cannot be transferred anyway (another model's private reasoning).

### Attacks
1. **"Removes private reasoning" is wrong for same-provider escalation with thinking enabled.** Anthropic: "Within the latest assistant message, the sequence of consecutive `thinking` blocks must match what the model generated in the original request: you can't rearrange, edit, or partially drop them... Modified thinking blocks are rejected with a 400 error." An escalation from a cheap Anthropic model to a frontier Anthropic model at a tool boundary, with thinking still enabled, must *keep* the latest turn's blocks — or disable thinking for that request. The decision as written produces a 400 on the most likely escalation path in an Anthropic-first shop.
2. **Filtering by `type == "thinking"` silently drops `redacted_thinking` and breaks the protocol.** The docs warn explicitly. A stripping implementation that is not tested against a `redacted_thinking` fixture is a latent 400.
3. **Tool id formats and result content types differ across providers.** Anthropic `toolu_…` ids and content-block results (text, image, JSON) do not map 1:1 onto OpenAI `call_…` ids and string outputs. LiteLLM's translation is the seam, and its issue tracker shows multi-turn breakage in exactly this conversion (#27946: Anthropic→OpenAI-compatible reasoning models fail on turn two). "Preserves tool IDs" must say *how* when the format changes, and must record the mapping so MEM can pair outcomes.
4. **The handoff note is an unversioned prompt and an injection surface.** It is text ADRL writes into the user turn. If it is free-form, it is a prompt whose effect on the target model is unmeasured and un-diffable; if it can contain model-generated summaries, it is a channel by which a cheap model's confabulation reaches the frontier model as apparent user context. It must be mechanical, delimited, versioned — and placed after tool results, because Anthropic requires `tool_result` blocks before any text in that message.
5. **D3 is over-claimed.** Shadow mode by definition does not affect execution; the transformed transcript is never sent to the target provider. The "shadow evidence" for CAS-004 can only show that `escalate.py` produced a payload, not that Anthropic/OpenAI/Bedrock accepted it. That is D2 evidence (tests pass) until a replay harness sends real handoffs to each provider pair.

### Evidence
- Anthropic, "Thinking" (platform docs) — signature "verif[ies] that thinking blocks were generated by Claude"; "you can't rearrange, edit, or partially drop them... rejected with a 400 error"; `redacted_thinking` must be passed back; filtering on `block.type == "thinking"` alone "silently drops `redacted_thinking` blocks and breaks the multi-turn protocol"; newer models keep older blocks readable, earlier models "can't read their blocks, the API drops them" (attacks 1, 2; clause 1) — https://platform.claude.com/docs/en/build-with-claude/thinking
- Anthropic, "Thinking in tool and multi-turn workflows" — "Echo the assistant message exactly as received: rebuilding the message or filtering out `redacted_thinking` blocks triggers a 400 error" (attacks 1, 2) — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- OpenAI, "Reasoning models" (API docs) — pass back reasoning items with function calls; `encrypted_content` for stateless use; "Persisted reasoning can be reused only within the same model family" (clause 1) — https://developers.openai.com/api/docs/guides/reasoning
- LiteLLM issue #27946, "Anthropic → OpenAI conversion drops reasoning_content, breaks multi-turn with reasoning models" — first turn succeeds, second fails with "The `reasoning_content` in the thinking mode must be passed back to the API" (attack 3) — https://github.com/BerriAI/litellm/issues/27946
- LiteLLM, "'Thinking' / 'Reasoning Content'" docs — `thinking_blocks` with `signature` are Anthropic-only; `drop_params`/`modify_params` needed when switching providers (attack 3) — https://docs.litellm.ai/docs/reasoning_content
- opencode issue #29879 — encrypted reasoning content "could not be verified" after 3–4 tool-calling turns in stateless mode; illustrates that reasoning-item round-tripping is fragile even within one provider (attack 5) — https://github.com/anomalyco/opencode/issues/29879
- Anthropic, "Parallel tool use" — "put every `tool_result` block before any text content in that message" (attack 4, clause 3) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- Anthropic, "Prompt caching" — cache hierarchy tools→system→messages; changing `system` invalidates everything below (clause 4) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching

### Verdict
**AMEND**, with a maturity downgrade. Attack 1 is decisive: the single "remove private reasoning" rule causes a 400 on same-family Anthropic escalation with thinking enabled, which is the most common escalation path for this deployment. Attacks 2 and 3 show the transformation has provider-pair-specific failure modes that a single sentence cannot capture; a versioned pair table is the right shape. Attack 4 lands: the note must be mechanical, delimited and positioned per provider rules. Attack 5 lands on maturity: shadow cannot validate acceptance, so D2 is the honest level until replay tests against live providers pass. The spirit — carry observations, drop the other model's private state, tell the new model why — is correct and stands.

## Amendments applied
- Replaced "removes private reasoning" with a versioned per-provider-pair rule (keep / strip / let API drop) including `redacted_thinking` and thinking-parameter handling (clause 1).
- Specified tool-id preservation across id formats with a recorded mapping and content downgrades (clause 2).
- Made the handoff note mechanical, delimited, positioned after tool results, never in `system`, schema-versioned (clause 3).
- Added cache consequence (clause 4).
- Maturity recommendation D2 until live-provider replay tests exist.

## Follow-ups
- [ ] Replay harness: take five shadow escalation payloads per provider pair (Anthropic cheap→Anthropic frontier with thinking on/off; Anthropic→OpenAI; OpenAI→Anthropic; local→each) and send them to the live endpoints in a sandbox; assert 2xx and a coherent first response. This is the gate to re-claim D3.
- [ ] Fixtures with `redacted_thinking` in the latest assistant message; golden test that the same-family keep path echoes it unmodified.
- [ ] Tool-id mapping table recorded on the outcome row; golden test that every `tool_use` id in the transformed transcript has exactly one `tool_result`.
- [ ] Handoff note schema v1 (fields: cause, from_rung, to_rung, executed_side_effects[], verifier_result?) with a fixed delimiter; prohibit any free-text or model-generated field.
- [ ] Confirm with the gateway team which provider pairs LiteLLM translates in the deployed version and pin the version in the pair table.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: per-provider-pair reasoning rule; tool-id mapping recorded; mechanical delimited handoff note positioned per provider rules; maturity D2 recommended | "Cross-model continuation preserves tool IDs/results, removes private reasoning, and adds a short handoff note." |
