# ADRL-CAS-003 — Action boundary defined; no re-issue after side effects

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Accepted · amended 2026-09-02 · amended 2026-09-03 (proposed amendment, pending disposition) |
| Maturity | D2 Tested, review recommends D2 Tested only after the golden trace in the follow-ups exists; the current tests cover "wait for boundary" but not the streamed-partial-response and parallel-tool-call cases that are where a replay would actually occur |
| Review verdict | AMEND |
| Tenets | 5 |
| Related decisions | CAS-001, CAS-004, CAS-006, CAS-007, RTG-004, SEM-001, SEM-003, FND-001, FND-004, SAF-007 |
| Open questions | Q3, Q7 |

## Current implementation evidence, 2026-09-08: routing diagnostic

The real controller retained local while tool results were incomplete, then selected cheap_cloud and constructed a handoff at the completed boundary. An injected local-only gate prevented cloud escalation. Requests, observations and gate outcomes were synthetic; dispatch, trust attestation and model recovery were not exercised.

[Report](../../reports/adrl-routing-in-action-2026-09-08.md) · [raw traces](../../reports/research/routing-demonstration-2026-09-08/results.json) · [next correction packet](../../reports/waves/routing-decision-quality.md). The focused 135 routing/cascade/learning tests pass; all 316 runtime inputs match the previous full build. Architectural status, maturity and decision wording are unchanged.

## Decision

Escalation occurs only at a controlled action boundary, defined as the arrival of a continuation request in which the harness has supplied a `tool_result` for every `tool_use` id in the preceding assistant message; ADRL never re-issues, on any deployment, a request whose original response had begun streaming tool-use content to the harness; recovery from a partially delivered response is the harness's, not the router's; and the side-effect class of every executed call is established by the provenance rule of CAS-009, which trusts MCP annotations only from allow-listed servers, parses compound commands, treats unknown actions as destructive and enumerates read-only calls in the record.

1. Boundary definition: for Anthropic-protocol traffic the boundary is a request whose last user message contains `tool_result` blocks matching every `tool_use.id` in the last assistant message (including `is_error: true` results for calls the harness declined to run). A request with a partial set of results is not a boundary; it is passed through on the served rung (CAS-006).
2. No blind replay: if a response fails after the first `tool_use` content block has been streamed to the harness, ADRL does not retry that request on any rung (the harness may already be executing the tool). Transport failure *before* any content is streamed may be retried by the gateway under its budget (CAS-007). A failure after streaming is surfaced as a protocol-conformant error.
3. Side-effect inheritance: the escalated model inherits a workspace mutated by the prior rung. The handoff note (CAS-004) must enumerate the side-effecting tool calls executed since the turn began (tool name, target path or command, result status) so the new model does not re-derive and re-apply them. Side-effect class is derived mechanically from tool name / MCP annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`), not from model text.
4. Non-idempotent executed actions are never undone by ADRL (no compensation); a turn whose trip-wire fired after a destructive tool executed is escalated with the note, and the outcome row carries `side_effects_before_escalation=true` for MEM.
5. Provenance (CAS-009): side-effect class comes from the built-in tool table, an attested annotation from an allow-listed MCP server, or a parsed command, in that order of preference; annotations from unlisted servers are ignored; compound shell commands are classified by their most severe component; unknown is destructive. The handoff record lists every executed call with its class and provenance source, read-only included.

## Context and rationale

You cannot escalate in the middle of a tool call. If the local model has just issued a write, the write has executed, and the result is coming back, switching models there means the new model inherits a world where side effects already happened but its own reasoning did not produce them. Escalation waits for a clean action boundary. This is the most safety-critical decision on the page: get it wrong and you get duplicated writes or migrations applied twice. The amendment pins down three things the original left implicit. First, *what a boundary is* on the wire — with parallel tool calls the boundary is after *all* results return, and the provider docs say every `tool_use` must receive a `tool_result` in one message. Second, *what "blindly replayed" means* for a transparent proxy: ADRL does not execute tools — the harness does — so the only way ADRL can cause a duplicate side effect is by re-sending a request whose response the harness had already started acting on. That is prohibited outright. Third, that a boundary protects against *replay* but not against *inheritance*: a wrong edit made by the cheap rung is still in the working tree, and the stronger model must be told, mechanically, what was done. The distributed-systems precedent is exact: at-least-once delivery plus non-idempotent side effects is the duplicate-charge problem, and the accepted answers are idempotency keys, at-most-once for non-idempotent steps, and explicit records of what executed.

## Adversarial review (2026-09-02)

### Steelman
Escalating only when the harness has returned all tool results is the one point in the loop where the transcript is internally consistent (every `tool_use` has its `tool_result`) and no tool is in flight. The proxy sees that state mechanically from request shape (SEM-001), so it needs no model judgment. Combined with tool-id preservation (CAS-004), the new model sees exactly what happened.

### Attacks
1. **"Action boundary" is undefined for parallel tool calls and streamed responses.** Claude Code routinely issues several `tool_use` blocks in one assistant message; the Anthropic docs require *all* corresponding `tool_result`s in the next user message and say splitting them "teaches Claude to avoid parallel calls". A boundary defined as "after a tool result" is therefore wrong; it must be "after *every* result". And because the proxy streams the response, the harness executes tools before the proxy has finished observing the response — the proxy cannot "wait" mid-response; it can only act on the *next* request.
2. **The real replay hazard is a retry after partial streaming, and the decision does not mention it.** If the upstream connection drops after the proxy has forwarded a complete `tool_use` block but before the response ends, a naive retry (by ADRL or the gateway) produces a *second* `tool_use` with a new id for the same intended edit or command. The harness executes both. This is the duplicate-write case, and it lives in the transport path, not in escalation. Stripe's idempotency essay describes exactly this ambiguity: "the operation executed successfully, but the client couldn't get the result."
3. **A clean boundary does not undo what the cheap rung already did.** SWE-agent shows failed edits cascade (edit success drops from 90.5% to 57.2% after one failure). If local made three wrong edits and then looped, escalation at the boundary hands frontier a repo with three wrong edits and a transcript in which those edits look like deliberate progress. Without a mechanical list of executed side effects in the handoff, the stronger model either trusts the edits or spends tokens rediscovering them. Temporal's guidance for non-idempotent activities — at-most-once plus compensating actions plus explicit records — is the relevant precedent; ADRL can do the "explicit record" part cheaply.
4. **The proxy cannot know which tools have side effects unless something tells it.** `Read`/`Grep` are safe to inherit; `Edit`/`Write`/`Bash` are not. MCP has standardised `readOnlyHint`/`destructiveHint`/`idempotentHint` for exactly this and warns they are untrusted unless the server is trusted; Claude Code's built-in tools have fixed names. The decision should say side-effect classification is mechanical (tool name / annotation), not inferred from model text.
5. **Subagents break the boundary (Q3).** A parent's continuation may arrive while a background subagent is mid-tool. If the parent escalates, the subagent's later results are returned into a transcript now served by a different rung, with tool ids the new model never issued. CAS-003 is silent; this review proposes CAS-008 for it rather than overloading CAS-003.

### Evidence
- Anthropic, "Parallel tool use" (platform docs) — "return one `tool_result` for each `tool_use` block, all together in the next user message"; declined calls still need a `tool_result` with `is_error: true`; splitting results across messages "teaches Claude to avoid parallel calls" (attack 1, clause 1) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- Stripe, "Designing robust and predictable APIs with idempotency" — the lost-response ambiguity; client-generated idempotency keys; server replays the stored result (attack 2) — https://stripe.com/blog/idempotency
- Temporal, "What is idempotency? And why it matters for durable systems" — activities are at-least-once; non-idempotent side effects should be at-most-once (`MaximumAttempts: 1`) with compensating actions and explicit operation records (attack 3, clause 4) — https://temporal.io/blog/idempotency-and-durable-execution
- MCP blog, "Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do" (2026) — `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`; "clients must treat them as untrusted unless they come from a trusted server"; `idempotentHint: true` → safe retry logic (attack 4, clause 3) — https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- Yang et al., "SWE-agent" (NeurIPS 2024) — edit-success probability 90.5% → 57.2% after one failed edit; cascading failed edits 23.4% of failures (attack 3) — https://arxiv.org/html/2405.15793
- Google SRE Book, "Addressing Cascading Failures" — "A single request at the highest layer may produce a number of attempts as large as the product of the number of attempts at each layer"; decide "if you really need to perform retries at a given level" (attack 2) — https://sre.google/sre-book/addressing-cascading-failures/
- Claude Code, "Create custom subagents" — background subagents "run concurrently while you continue working"; up to 20 concurrent by default; nested up to three layers (attack 5) — https://code.claude.com/docs/en/sub-agents

### Verdict
**AMEND.** The register itself asked reviewers to "trace an escalation through a tool-call sequence and try to construct a case where a side effect could be replayed." The trace finds two: (i) a retry after partial streaming (attack 2) — which is not an escalation at all, but a transport retry, and the decision must forbid ADRL from doing it and bound the gateway from doing it; (ii) parallel tool calls with a partial result set (attack 1), where "after a tool result" is not a boundary. Both are closed by clauses 1–2. Attack 3 lands and reframes the decision: a boundary prevents *replay* but not *inheritance*, and inheritance needs a mechanical side-effect record (clause 3–4). Attack 4 is answered by using tool names and MCP annotations. Attack 5 is deferred to a new decision (CAS-008). The core rule stands; its definition was the gap.

## Adversarial review (2026-09-03)

### Steelman
Clause 3's "mechanical, not from model text" was the right instinct; tool names and annotations are structured fields, not prose.

### Attacks
1. **Annotations are attacker-controlled fields.** The MCP specification says clients must treat them as untrusted unless the server is trusted; a tool named `delete` with `readOnlyHint: true` was classified read-only by the implementation.
2. **A command's first word is not its effect.** `echo $TOKEN > /tmp/leak` and `git status && touch owned` were both read-only under prefix matching.
3. **Omitting read-only calls hides the mis-classifications that matter most.** The receiving model inherits mutations the record says never happened, which is the failure clause 3 exists to prevent.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P1-4, verified with the three examples above.
- Model Context Protocol, "Tools" (specification 2025-06-18) - https://modelcontextprotocol.io/specification/2025-06-18/server/tools (cited by the 2026-09-03 external review; not independently fetched)

### Verdict
**AMEND (proposed).** Clause 3 keeps "mechanical" and gains a provenance rule (clause 5, CAS-009). Pending disposition.

## Amendments applied
- Defined "controlled action boundary" on the wire (all `tool_use` ids answered).
- Added the no-re-issue-after-streaming rule (clause 2) and separated transport retry from escalation.
- Added mechanical side-effect enumeration in the handoff (clause 3) and no-compensation with ledger marker (clause 4).
- 2026-09-03: provenance rule added to the decision sentence and as clause 5; annotations trusted only from allow-listed servers; compound commands parsed; unknown actions destructive; read-only calls enumerated.

## Follow-ups
- [ ] Golden trace `tests/fixtures/handshakes/escalation_parallel_tools.json`: assistant message with three `tool_use`; continuation with two `tool_result`s → passthrough on served rung; continuation with all three → boundary, escalation permitted.
- [ ] Golden trace: upstream disconnect after a `tool_use` block has been streamed → no retry on any rung; protocol-conformant error to the harness; outcome typed `infrastructure` with `partial_stream=true`.
- [ ] Implement side-effect classification table for Claude Code / Codex CLI built-in tools plus MCP annotations; handoff note enumerates executed side-effecting calls since turn start.
- [ ] Confirm with the gateway team (Q7) that gateway retries are disabled once any response bytes have been forwarded, or that the gateway retries only on connection-level failure before first byte.
- [ ] Write ADRL-CAS-008 (subagent escalation) — proposed in this review.
- [ ] 2026-09-03: replace prefix matching with the CAS-009 parser; golden corpus includes `echo $TOKEN > /tmp/leak` (destructive), `git status && touch owned` (destructive), MCP `delete` with `readOnlyHint` from an unlisted server (destructive).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: boundary defined as all tool_use ids answered; no re-issue after streamed tool content; mechanical side-effect record in handoff | "Escalation occurs only at a controlled action boundary so partial tool execution is not replayed blindly." |
| 2026-09-03 | Amended (proposed, external review): side-effect provenance rule per CAS-009; read-only calls recorded | "Escalation occurs only at a controlled action boundary — defined as the arrival of a continuation request in which the harness has supplied a `tool_result` for every `tool_use` id in the preceding assistant message — and ADRL never re-issues, on any rung, a request whose original response had begun streaming tool-use content to the harness; recovery from a partially delivered response is the harness's, not the router's." |
| 2026-09-08 | Added scoped offline routing-diagnostic evidence and limitations; behaviour and grades unchanged | Decision wording retained unchanged; prior implementation/research notes preserved. |
