# ADRL-SAF-005 — Block, and make the block recoverable

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (blocking is tested; recoverability against the real harness is not, and the compaction deadlock has not been ruled out) |
| Review verdict | AMEND |
| Tenets | 2, 5 |
| Related decisions | SAF-002, SAF-004, SAF-006, SEM-004, CAS-003, FND-001, RTG-004 |
| Open questions | Q2, Q5 |

## Decision

Privacy-context conflicts block instead of leaking data or silently truncating context, and the block is emitted in a form the harness recognises as a context-limit error so that its own compaction path is triggered; the local rung offered to pinned lineages must be able to hold the harness's compaction request.

1. The block for "pinned and larger than the local window" carries the vendor's too-long error wording (or the `capability_rejected: prompt_too_long` token) so Claude Code auto-compacts and retries, rather than a gateway-worded error that leaves the developer to run `/compact` by hand.
2. Because Claude Code's auto-compact threshold is clamped to no less than 100,000 tokens, the local rung's largest model must accept at least the harness's compaction window plus the compaction prompt overhead; if it cannot, the local rung is infeasible for pinned lineages by construction and the pin degrades to "block every request", which must be reported at rung-configuration time, not discovered by a developer.
3. A block on a continuation is issued only at an action boundary (CAS-003): if a tool has executed and its result is the request being blocked, the block response tells the developer which tool ran so no side effect is hidden.
4. ADRL never truncates, summarises, or drops blocks from a request on any rung; the only context reduction is the harness's own, triggered through its documented error path.

## Context and rationale

A pinned session whose context is larger than the local rung can hold has three options: send to cloud (breaks the pin), silently drop context (the model answers confidently from partial information), or block and surface. We block.

The amendment keeps the choice and fixes the consequence. Claude Code recovers from an oversized context by itself — when it *recognises* the error. Anthropic's gateway documentation states that a gateway which "enforces a smaller context than the model's native window and rewrites the upstream error" leaves Claude Code unable to recognise the too-long condition, so it "doesn't compact and retry automatically" and the developer must run `/compact`. A block that is not recognisable is a dead end dressed as a safety feature. Worse, the compaction request itself carries the whole transcript: if the local rung cannot hold it, the pinned session cannot compact, cannot proceed, and cannot use cloud — a deadlock the register does not currently rule out. Since Claude Code clamps its auto-compact window to at least 100k tokens, a local rung whose largest model has a 32k or 64k window is *structurally* unable to serve a long pinned session, and that should be a configuration error, not a runtime surprise.

## Adversarial review (2026-09-02)

### Steelman
Silent truncation is the worst outcome in the register: a model that answers confidently from a partial transcript produces plausible wrong edits that the developer trusts because nothing signalled a problem. Sending to cloud breaks the one guarantee the layer makes. Blocking is the only option that is honest, and it preserves the pin without pretending the local rung can do what it cannot.

### Attacks
1. **A block the harness does not recognise is a dead end.** Claude Code auto-compacts only when the error matches the wording it knows. A gateway-worded block (or an ADRL-worded one) becomes "run `/compact` yourself" — a workflow change (FND-001) and a support ticket. The decision says nothing about the error's form.
2. **Compaction deadlock.** The compaction request carries the transcript. On a pinned lineage it must go local (SEM-004 as amended). If the transcript is larger than the local window, the compaction request is itself blocked, so the session can never shrink. Nothing in the register prevents this, and Claude Code's ≥100k clamp on the auto-compact window means any local rung under ~100k+overhead tokens guarantees it for long sessions.
3. **Blocking mid-tool-loop hides a side effect.** If the local model issued a write, the write executed, and the `tool_result` continuation is the request that overflows, blocking it leaves the developer with a mutated working tree and no model response explaining it. CAS-003's action-boundary rule needs to apply to blocks, and the block should name the executed tool.
4. **Truncation can happen upstream of ADRL.** LiteLLM or a local server (vLLM/llama.cpp) may truncate or reject long inputs in their own way — some servers silently truncate from the left. "We block" is only true if ADRL checks feasibility (SAF-006) *before* forwarding, with a tokenizer estimate that errs long. Sub-clause 3 states that ADRL never truncates; the follow-ups must verify the local servers do not either.
5. **Q2 interacts: the block rate is a routing signal, not just a safety event.** If many pinned sessions block, the local rung's context budget is the binding constraint on the savings case. The block rate per pinned lineage should feed RTG-004's "controlled cascade remains feasible" and the readiness gates, otherwise the pin's true cost is invisible.

### Evidence
- Anthropic, "Connect Claude Code to an LLM gateway" (Claude Code docs) — a gateway that enforces a smaller context and rewrites the error prevents automatic compaction; `CLAUDE_CODE_AUTO_COMPACT_WINDOW` is clamped to at least 100,000 tokens and at most the model's window, "so you can't match a gateway limit below 100,000, and `/compact` remains the recovery there"; bears on attacks 1, 2 — https://code.claude.com/docs/en/llm-gateway-connect
- Anthropic, "Gateway protocol reference" (Claude Code docs) — retry/recovery logic matches upstream error wording; a stable `capability_rejected:` token in a gateway envelope preserves recovery, e.g. `capability_rejected: prompt_too_long`; bears on attack 1 — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude Platform docs) — a tool-use loop is one assistant turn; side effects occur between round trips; bears on attack 3 — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- LiteLLM, "Fallbacks (Provider Failover)" — context-window fallbacks map provider too-long errors and re-route; shows the gateway has its own handling of this error class that must be disabled for pinned traffic; bears on attack 4 — https://docs.litellm.ai/docs/proxy/reliability
- No direct literature found on truncation behaviour of specific local inference servers under overflow; reasoning from first principles for attack 4 (follow-up measurement required).

### Verdict
**AMEND.** The choice to block is correct and unchallenged. Attack 1 lands: the block must speak the harness's dialect or it is not a recovery path. Attack 2 is the most important finding in this decision — a structural deadlock that turns "block" into "the pinned session is dead" for any local rung smaller than the harness's compaction floor — and it is resolvable only at configuration time, so the decision has to say so. Attack 3 is closed by applying CAS-003 to blocks. Attacks 4 and 5 are follow-ups.

## Amendments applied

- Added "and the block is emitted in a form the harness recognises as a context-limit error so that its own compaction path is triggered".
- Added "the local rung offered to pinned lineages must be able to hold the harness's compaction request".
- Added sub-clauses on error wording, the ≥100k compaction-window constraint as a configuration-time check, action-boundary blocks naming executed tools, and the no-truncation-by-ADRL rule.

## Follow-ups

- [ ] Protocol test against the current Claude Code: pinned overflow → ADRL block with vendor too-long wording → assert auto-compact fires and the retried request is served locally.
- [ ] Configuration check (CI): largest local model context ≥ `CLAUDE_CODE_AUTO_COMPACT_WINDOW` floor (100k) + measured compaction prompt overhead; fail the rung config otherwise and report "pinned lineages will deadlock".
- [ ] Golden test: overflow detected on a `tool_result` continuation after a write → block names the executed tool in its message.
- [ ] Measurement: behaviour of each local server (vLLM, llama.cpp, Ollama) on inputs exceeding the window — reject vs silent truncate; ADRL feasibility check must be configured to err long for any server that truncates.
- [ ] Emit block rate per pinned lineage to telemetry; add to the Q2 local-rung analysis and RTG-004 feasibility.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: harness-recognisable block; compaction-window feasibility as a configuration constraint; action-boundary blocks | "Privacy-context conflicts block instead of leaking data or silently truncating context." |
