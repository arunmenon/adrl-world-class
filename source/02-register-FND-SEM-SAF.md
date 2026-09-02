# ADRL Decision Register — FND, SEM, SAF

All decisions **Status: Accepted**. Source: Confluence bucket pages, updated Aug 27 2026.

---

## FND — System Boundary and Principles

| ID | Decision | Maturity |
|---|---|---|
| ADRL-FND-001 | ADRL is a transparent control layer between the coding harness and model gateway. | D3 Shadow |
| ADRL-FND-002 | ADRL owns semantic policy; LiteLLM and providers own mechanical model execution. | D2 Tested |
| ADRL-FND-003 | The normal routing boundary is a user turn, not every HTTP request. | D3 Shadow |
| ADRL-FND-004 | Failure defaults to unchanged upstream behaviour, with a one-step operator bypass. | D4 Pilot |
| ADRL-FND-005 | Scope expands only through measured phase gates; component presence is not readiness. | D3 Shadow |

### In plain terms

**FND-001 — "transparent" is a testable property, not a marketing word.** Claude Code asks for one model alias and gets back a normal Anthropic-protocol response. It does not know a router exists. The test of transparency: point `ANTHROPIC_BASE_URL` back at the gateway and everything still works, with nothing to uninstall. If a developer ever has to change how they work because of ADRL, this decision has been violated.

**FND-002 — ADRL says "this is hard," not "use this model."** ADRL emits "this deserves the frontier rung." It does *not* emit "use claude-opus-4-8 at this endpoint, retry twice, fall back to that one." The second sentence belongs to the gateway. The reason for the split is rate-of-change: endpoints, model IDs, quotas and providers churn constantly, while the semantic question — how hard is this piece of work — is stable. Coupling them would make every model deprecation a routing-logic change.

**FND-003 — one instruction is not one request.** You type "fix the failing test." The harness then sends perhaps fifteen HTTP requests: read the file, run the tests, propose an edit, re-run, and so on. Only the *first* carries a new decision; the other fourteen are the model working. Deciding fifteen times means re-deciding fourteen times with no new information — and because context grows with every handshake, any rule that scores context size ratchets upward until it flips models mid-task. So the decision happens once, at the start of the turn.

**FND-004 — the worst case is what you had before.** If ADRL crashes, times out, or cannot reach a verdict, the request proceeds exactly as if the layer were not installed. There is also a one-step operator bypass. This is what makes the layer safe to insert into a working setup: the failure mode is *no change*, not *no service*. It sits at D4 — the most mature decision in the register. That ordering is deliberate: the escape hatch should be better proven than the feature it protects.

**FND-005 — "we wrote the code" is not "it is ready."** Scope expands only through measured gates. This is a governance commitment rather than a technical one, and it is what licenses the honest D0 entries elsewhere in the register. Without it, the natural pressure is to treat a merged component as a delivered capability — which is precisely how a cost optimisation ends up degrading someone's workflow.

### What to scrutinise
- FND-002 is the load-bearing split. Every other bucket assumes ADRL decides capability and the gateway decides endpoint.
- FND-004 is the safety net, and the reason this can be piloted at all.
- FND-005 is what keeps the register honest.

Code map: FND-001 `proxy/wire_capture_proxy.py`, `router/live_router.py`, `src/gateway/routing.py`, `src/gateway/stack.py`. FND-002 `router/live_router.py` (semantic), `router/backends.py` + `src/gateway/routing.py` (role→endpoint). FND-003 `router/discriminator.py`, `router/live_router.py`, `router/state.py`. FND-004 `proxy/wire_capture_proxy.py`, `src/gateway/plug.py`, modes `off`/`shadow`/`live`. FND-005 `router/learning_readiness.py`, `config/readiness-score-v1.json`, `tools/check_readiness_score.py`, `reports/learning-readiness.md`.

---

## SEM — Interaction Semantics

| ID | Decision | Maturity |
|---|---|---|
| ADRL-SEM-001 | Requests are mechanically classified as user turns, continuations, utility calls, subagents, or passthrough traffic. | D3 Shadow |
| ADRL-SEM-002 | `metadata.user_id` is the preferred session key; a stable anonymous fallback prevents unrelated traffic from sharing state. | D3 Shadow |
| ADRL-SEM-003 | Continuations inherit the sticky route and do not trigger a fresh difficulty decision. | D2 Tested |
| ADRL-SEM-004 | Utility calls may use a small local model; protocol and unknown calls pass through unchanged. | D3 Shadow |
| ADRL-SEM-005 | Episode boundaries are conservative semantic events that may release escalation hysteresis. | D2 Tested |
| ADRL-SEM-006 | Subagents are linked to the parent for constraints but have separate routing identity and evidence. | **D0 Design** |

### In plain terms

**SEM-001 — five kinds of traffic look identical on the wire; treating them the same is the original sin.** Every request arriving at the proxy is a `POST /v1/messages`. Underneath, it is one of: a new user turn, a continuation (last message is tool results coming back), a utility call (harness asking a model to name the session or summarise), a subagent, or passthrough (protocol traffic like token counting, which was ~72% of raw wire volume and was missing from the taxonomy entirely until the corpus revealed it). "Mechanically" matters: classification uses request shape, not an LLM's opinion, so it is cheap and auditable.

**SEM-002 — you need to know which conversation this is, without a session ID.** Claude Code carries a per-session identifier in `metadata.user_id` — a Phase 0 experiment that resolved favourably and let us delete a planned hashing fallback. The stable anonymous fallback exists so that if the key is absent, unrelated developers' traffic still cannot accidentally share routing state.

**SEM-003 — the continuation rule is what makes cheap routing safe.** When tool results come back, that is not a new task. So the request inherits whatever rung the turn started on. Without it, the router re-scores a context that grows on every handshake and eventually switches models mid-reasoning — cold-starting the cache, confusing the new model, and in the Anthropic/OpenAI case getting the request rejected outright, because thinking-block signatures and encrypted reasoning items do not transfer between providers.

**SEM-004 — the harness makes small calls that aren't your work.** Naming a session, summarising for compaction — housekeeping, ideal for a small local model. Anything the discriminator does not recognise is passed through untouched. Corpus finding: utility calls turned out to run on Opus/Sonnet with tiny token budgets, not on a cheap model — so they are fingerprinted by request shape, not by model name.

**SEM-005 — how a task gets to come back down a rung.** Once work escalates to frontier it stays there (CAS-005). But it cannot stay elevated forever. An episode boundary — a conservative signal that you have genuinely moved on — is the only event allowed to release that. Conservative deliberately: a false boundary silently drops a hard task back to local mid-flight.

**SEM-006 — the known gap, honestly marked.** A subagent should inherit the parent's constraints (if the parent is privacy-pinned, the child must be too) but have its own routing identity and evidence, so its outcomes are not misattributed to the parent's turn. None of it is built — D0 — and the interim position is to pass subagent traffic straight through.

### Scrutinise / Open items
- SEM-001 is the foundation; highest-consequence classification in the system.
- SEM-006 is the D0 — Q3.
- Subagent routing identity and nested escalation safety (Q3).
- Episode-boundary detection is conservative by design — so conservative a rung is never lowered in practice?
- Real-payload edge cases — mixed content blocks, compaction, mid-loop interjections, empty turns — need golden tests.

Code map: SEM-001 `router/discriminator.py`, `tests/fixtures/handshakes`, `tests/test_discriminator_canary.py`. SEM-002 `router/discriminator.py`, `reports/assumption-user-id.md`. SEM-003 `router/policy.py`, `router/live_router.py`, `router/state.py`. SEM-004 `router/discriminator.py`, `router/hook.py`. SEM-005 `router/episode.py`, `router/state.py`, `tools/sem_label.py`. SEM-006 `router/discriminator.py` creates linked identities (row cut off).

---

## SAF — Safety, Privacy, Hard Constraints

> Security and privacy architects: this is your page.

| ID | Decision | Maturity |
|---|---|---|
| ADRL-SAF-001 | Hard gates execute before, and cannot be overridden by, heuristics or learned policy. | D2 Tested |
| ADRL-SAF-002 | Privacy pinning is one-way for the session; once local-only, it stays local-only. | D2 Tested |
| ADRL-SAF-003 | Secret detection occurs before routing and suppresses prompt-derived embeddings and identifiers. | D3 Shadow |
| ADRL-SAF-004 | A pinned session cannot fall back or escalate to cloud; unresolved failure is surfaced to the user. | D2 Tested |
| ADRL-SAF-005 | Privacy-context conflicts block instead of leaking data or silently truncating context. | D2 Tested |
| ADRL-SAF-006 | Unhealthy or context-infeasible rungs are removed before optimisation. | D2 Tested |
| ADRL-SAF-007 | Verification commands are constrained by protected paths and execution policy. | D2 Tested |

### In plain terms

**SAF-001 — ordering is the security property.** Gates run first and produce a set of permitted rungs. Only then does anything optimise inside that set. The classifier is never in a position to say "frontier would give a better answer" and send secret-bearing code to the cloud.

**SAF-002 — one-way, because the alternative is unauditable.** If a session touches something sensitive, it is pinned local-only for the rest of the session and cannot be quietly released. A pin that can lift itself means the safe state depends on a chain of later judgements, and you can no longer answer "did this code ever leave the machine?" with a simple yes or no. The cost is real — one flagged file can make a long session local — which is why scanner precision (SAF-003) is the highest-leverage knob.

**SAF-003 — detect before deciding, and don't leak through the metadata.** Scanning happens before routing. For a secret-bearing turn, ADRL also suppresses derived artefacts — embeddings and instruction hashes. A vector built from your prompt is still your prompt, statistically. Consequence: we lose training signal on exactly the sessions we understand least.

**SAF-004 — a pinned session fails loudly rather than reaching for cloud.** On a pinned route, escalation is not available; if work cannot complete the developer is told. "Just this once, use cloud" converts a privacy guarantee into a probability.

**SAF-005 — blocking beats silent truncation.** A pinned session whose context is larger than the local rung can hold: send to cloud (breaks pin), silently drop context (model answers confidently from partial info), or block and surface. We block.

**SAF-006 — "infeasible" is a safety concern.** A rung whose endpoint is unhealthy or whose context window cannot hold the request is removed from the candidate set before optimisation — not scored poorly and possibly still chosen.

**SAF-007 — the verifier is code execution, so it gets a leash.** Deterministic verification runs tests/checks — arbitrary execution. Unconstrained, it could touch protected paths or mutate the thing it measures. So it runs under explicit path and execution policy.

### Scrutinise / Open items
- SAF-001 is the precedence rule — tenet 2 in decision form.
- SAF-004/005 both choose "block and tell the user" over "silently degrade."
- SAF-003 at D3 because precision, not recall, is the binding constraint: over-flagging pins whole sessions local and pushes developers to disable the layer — a worse privacy outcome.
- Completeness: seven gates listed; most valuable comment names a MISSING gate.
- Privacy-pin granularity: is session the right scope? (Q5)
- Adversarial evidence outstanding: gates are tested, not attacked.
- Data-residency constraints for specific repositories are not yet expressed as a gate.

Code map: SAF section of architecture-code-map not captured. Memory facade (`memory_facade.py`) implements: remove raw instruction before saving; hash normal instructions; do not hash private instructions; no embeddings for private/secret tasks. `verifier.py` checks protected files not changed and changes stayed inside task scope.
