# ADRL-SEM-003 — Continuations inherit the sticky route

| Field | Value |
|---|---|
| Bucket | SEM — Interaction Semantics |
| Status | Accepted · unchanged |
| Maturity | D2 Tested, review recommends D3 Shadow — the Phase 0 cache-hit measurement on real traffic is shadow-grade evidence for exactly this rule, and the register under-claims |
| Review verdict | APPROVE |
| Tenets | 1, 6 |
| Related decisions | FND-003, SEM-001, SAF-001, SAF-006, CAS-003, CAS-004, CAS-005, CAS-006, RTG-005 |
| Open questions | — |

## Decision

Continuations inherit the sticky route and do not trigger a fresh difficulty decision.

## Context and rationale

When tool results come back, that is not a new task, so the request inherits whatever rung the turn started on. Without this rule the router re-scores a context that grows on every handshake and eventually switches models mid-reasoning — cold-starting the cache, confusing the new model, and in the cross-provider case getting the request rejected outright.

Two corrections to the *rationale* (not the decision). First, the register says "thinking-block signatures and encrypted reasoning items do not transfer between providers". Anthropic's documentation says signatures *are* compatible across the Claude API, Bedrock and Google Cloud — the incompatibility is across *model vendors*, not across Claude-serving platforms; a Claude thinking block cannot be given to a Llama or GPT model, and OpenAI reasoning items are reusable only within the same GPT model family. Second, the register's "does not trigger a fresh difficulty decision" is the right wording and must not be read as "does not run the gates": the tool result coming back is the main way secrets and oversized context enter the transcript, and SAF-001 (as amended) runs on every request. Inheriting the *rung* is a routing statement; inheriting the *gate outcome* would be a security bug.

## Adversarial review (2026-09-02)

### Steelman
This is the rule that makes cheap routing safe, and it has the best evidence in the register: Anthropic's cache is prefix-exact and, by implication of its per-model rules, per-model, the tool-use loop is by Anthropic's definition one assistant turn whose thinking blocks must be echoed back verbatim, and Phase 0 measured a very high cache-hit ratio on real traffic under this rule. Every alternative — re-scoring on growth, periodic re-evaluation — either destroys the cache or produces the mid-turn model switch the vendor's API rejects.

### Attacks
1. **Inherit the route, or inherit the gate?** The decision says no fresh *difficulty* decision. If the implementation also skips the SAF gate set on continuations (because gates were bound to "before routing", SAF-003), then a `tool_result` carrying `cat ~/.aws/credentials` or a production `.env` is never scanned, and the session is never pinned. This is the single largest privacy gap found in the review — but it is a gap in SAF-001/SAF-003's wording and in FND-003's, not in this sentence, which correctly scopes itself to difficulty.
2. **Feasibility can change mid-turn.** Context grows with each handshake; the inherited local route can become infeasible (SAF-006) three tool calls in. "Inherit" cannot mean "send anyway". The register handles this: infeasibility is a SAF-005 block on pinned sessions and a CAS escalation at an action boundary otherwise. The decision is silent but not wrong; CAS-003/CAS-005 own the exception.
3. **The cross-provider rationale is imprecise.** Signatures transfer across Claude platforms; what does not transfer is a Claude thinking block to a non-Claude model, or an OpenAI reasoning item across GPT families. The consequence for ADRL is unchanged (never switch mid-turn between vendors), but the register's stated reason would mislead an engineer configuring Bedrock and Vertex endpoints in the same frontier rung — that switch is *allowed* by the signature rule (though still cache-cold).
4. **Escalation is a route change mid-turn.** CAS-003/CAS-004 explicitly switch models inside a turn at an action boundary, stripping private reasoning. So "continuations inherit the sticky route" has a documented exception that this decision does not mention. It is not a contradiction — CAS-005 makes the *new* rung sticky — but a reader of SEM-003 alone would not know an exception exists.
5. **Transport fallback silently changes the served rung.** If the gateway fails over inside the rung (allowed by FND-002 as amended) the continuation inherits the *intended* route, but CAS-006 says sticky state must record the *served* rung. The two agree only if the inherited state is updated from the response, which is CAS-006's job. Answered.

### Evidence
- Anthropic, "Prompt caching" (Claude Platform docs) — exact prefix matching; 5-minute default TTL measured from request start; per-model minimum cacheable lengths (512–4,096 tokens) and model-specific thinking-block handling imply caches do not carry across models, though the page does not say so explicitly; supports the steelman — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, "Thinking" (Claude Platform docs) — "`signature` values are compatible across platforms (the Claude API, Amazon Bedrock, and Google Cloud)"; modified thinking blocks are rejected with 400; changing thinking configuration "starts the cache over"; bears on attack 3 — https://platform.claude.com/docs/en/build-with-claude/thinking
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude Platform docs) — "A tool-use loop is one assistant turn"; thinking blocks must be passed back complete and unmodified within the turn; supports the steelman — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- OpenAI, "Reasoning models" (API guide) — "Persisted reasoning can be reused only within the same model family"; incompatible reasoning is omitted on family switch; bears on attack 3 — https://developers.openai.com/api/docs/guides/reasoning
- Anthropic, "Gateway protocol reference" (Claude Code docs) — a rejected thinking signature causes Claude Code to disable the capability for the rest of the conversation; shows the cost of a mid-turn vendor switch is conversation-wide, supporting the steelman — https://code.claude.com/docs/en/llm-gateway-protocol
- ADRL evidence pack, `01-overview-tenets-taxonomy.md` — "never-switch-mid-turn vindicated (prompt-cache hit ratio on real traffic very high)"; supports the maturity recommendation.

### Verdict
**APPROVE.** The decision sentence is precise — it scopes itself to the *difficulty decision* — and every attack that lands (1, 2, 4) lands on a neighbouring decision's wording or on a missing cross-reference, not on this one. Attack 3 is a factual correction to the rationale, applied above, that does not change the conclusion. The evidence is the strongest in the SEM bucket and includes a real-traffic measurement, so the review recommends the maturity be *raised* to D3: the register already has shadow-grade evidence for this rule and is under-claiming.

## Amendments applied

None — decision stands as written. Rationale corrected: thinking signatures are portable across Claude-serving platforms but not across model vendors; OpenAI reasoning items are reusable only within a GPT model family. Rationale clarified: "no fresh difficulty decision" does not mean "no gates" (SAF-001 as amended runs on every request).

## Follow-ups

- [ ] Cross-reference: add "except CAS escalation at an action boundary (CAS-003/CAS-005)" to the register's plain-terms entry for SEM-003.
- [ ] Golden test (owned by SAF-001/SAF-003): continuation whose `tool_result` contains a high-confidence secret → session becomes pinned on that request, before the request is forwarded.
- [ ] Golden test: continuation that exceeds local context on an unpinned local route → CAS escalation at action boundary, not a rejected request or a silent gateway context-window fallback.
- [ ] Fixture: escalation mid-turn from local (no thinking blocks) to frontier with thinking enabled — confirm the frontier accepts an assistant `tool_use` turn that has no preceding thinking block, or document that CAS-004 must wait for the turn to end. (Anthropic docs fetched here do not settle this.)
- [ ] Register: raise SEM-003 to D3 with a pointer to the Phase 0 cache-hit measurement.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged; rationale corrected on signature portability; D3 recommended | "Continuations inherit the sticky route and do not trigger a fresh difficulty decision." |
