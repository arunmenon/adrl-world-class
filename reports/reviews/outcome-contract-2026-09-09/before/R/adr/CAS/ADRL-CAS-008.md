# ADRL-CAS-008 — Escalation scope under subagents

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Proposed 2026-09-02 (new, from adversarial review) |
| Maturity | D0 Design, review recommends D0 Design (depends on SEM-006, also D0; interim behaviour — passthrough — is what runs today) |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 5, 6, 8 |
| Related decisions | SEM-006, SEM-001, CAS-001, CAS-003, CAS-005, CAS-006, SAF-002, RTG-005, RTG-009 |
| Open questions | Q3 |

## Decision

Escalation is scoped to a single routing identity: a subagent's trip-wires, action boundary, sticky state and handoff apply to the subagent's own transcript and never change the parent's rung, and a parent's escalation never changes an in-flight child's rung; constraints (privacy pin, permitted-rung set, budget ceiling) flow parent→child at spawn time only, and outcomes flow child→parent as typed evidence, not as escalation triggers.

1. Identity: each subagent request stream is a separate routing identity (SEM-006) linked to the parent's `route_id`; in Claude Code the link is the `agent_id`/`agent_type` present on hook events and, on the wire, the request shape the discriminator recognises as a subagent. Until SEM-006 is built, subagent traffic follows the SEM-006 interim — constrained passthrough at the model the harness requested, with the parent's pin and gate state inherited — and is shadow-logged with `subagent=true`; no trip-wire fires on it. (A *fork*, which shares the parent's transcript prefix, starts at the parent's served rung — see attack 5.)
2. Constraint inheritance: a child inherits the parent's pin (one-way, SAF-002) and permitted-rung set at spawn; a pin acquired by the child (e.g. it reads a secret) pins the child and is reported to the parent's identity as a `policy_constraint` event so the parent's *next* decision is pinned — it does not retroactively alter in-flight parent requests.
3. No cross-identity escalation: a child that trips a wire escalates its own stream at its own action boundary (CAS-003); the parent continues on its rung. A child's terminal failure (CAS-007) surfaces to the parent as the child's result (the harness already returns subagent completions to the parent), never as a parent-level protocol error. The parent may then escalate on its own trip-wires (e.g. repeated failed delegations count as repeated tool errors).
4. Budget: the parent's identity carries an episode budget (tokens / cost per RTG-009) from which children draw; a child cannot escalate to a rung whose expected cost exceeds its remaining allocation; exhaustion is a typed `policy_constraint` outcome, not a capability failure. Nested subagents (Claude Code allows three layers) inherit recursively.
5. Evidence: parent and child outcomes are never pooled; MEM-004 typing applies per identity; a child's failure is not evidence about the parent's task difficulty and vice versa.

## Context and rationale

Q3 states the problem: parent and subagents are in flight simultaneously; escalating one risks split-brain; escalating both multiplies cost. The register's lean — v1 passthrough, shadow-log, nested escalation as a separate decision — is correct, and this is that separate decision. The precedents point the same way. Claude Code subagents run in isolated context windows, concurrently with the parent, up to 20 at a time and three layers deep, and return results to the parent as a completion; the natural escalation unit is therefore the subagent's own transcript, and the only things that should cross the parent/child boundary are constraints (downward, at spawn) and typed results (upward, at completion). The multi-agent failure literature is explicit that inter-agent misalignment (37% of failures in MAST) and loss of conversation history are distinct failure classes from single-agent loops — which is a reason to keep each identity's trip-wires and stickiness separate rather than to invent a combined "system" escalation. The one thing the parent must do is treat a child's repeated failure as *its own* tool-error signal, so that a parent stuck delegating to a child that cannot succeed is itself escalated by ordinary CAS-001 wires.

## Adversarial review (2026-09-02)

### Steelman
Per-identity scoping is the only rule that composes: it needs no global coordinator, it cannot produce split-brain (each stream has one rung), it makes budgets hierarchical in the obvious way, and it reuses CAS-001/003/005 unchanged at every level. Passthrough as the interim is exactly the FND-004 default.

### Attacks
1. **Passthrough leaves a gap: subagent work is the traffic the value thesis is about.** The Evidence page says the capability-unlock story — running multi-agent workflows on a free local rung — is the stronger enterprise argument. Passing subagents through at the parent's rung forfeits that until SEM-006 is built. Accepted as the cost of safety; the decision's interim clause is explicit so the gap is visible, and SEM-006 is the blocker, not this decision.
2. **A child's pin must reach the parent, or the pin is not one-way.** If a child reads a secret and is pinned, but the parent (unpinned) receives the child's summary and continues on cloud, secret-derived content has crossed the boundary. Clause 2 makes the child's pin an event for the parent's next decision; whether the *summary* itself must be treated as pinned content is a SAF question (Q5) and is flagged as a follow-up rather than decided here.
3. **Budgets can deadlock or starve.** A parent that allocates most of its budget to one child leaves siblings unable to escalate; a child that exhausts budget fails with `policy_constraint`, the parent retries the delegation, and the loop repeats. Answered partially: parent-level CAS-001 wires count repeated failed delegations; budget exhaustion is typed so it never looks like capability. Allocation policy is left to OPS (budgets) and is a follow-up.
4. **The wire may not reveal parent/child structure.** SEM-001 classifies subagents by request shape; Claude Code's `agent_id` is only visible to hooks, not in the API request. If the discriminator misclassifies a child as a fresh user turn, it gets a fresh decision and its own stickiness — which is *safe* under this decision (per-identity scoping still holds) but loses the constraint inheritance. Clause 1 therefore names both signals and makes hook ingestion a follow-up; misclassification degrades to "no inheritance", never to "cross-identity escalation".
5. **Forks are not subagents.** Claude Code's fork "inherits the entire conversation so far"; its transcript shares the parent's prefix (and cache). A fork escalated independently would break the parent's cache assumptions only for itself, but a fork *should* probably inherit the parent's served rung as its starting rung. The decision treats a fork as a child whose initial rung is the parent's served rung (CAS-006) — noted as a sub-clause of 1 for implementation.

### Evidence
- Claude Code, "Create custom subagents" — isolated context windows; foreground blocks, background runs concurrently; 20 concurrent by default; three layers deep by default; results return "as a completion notification"; forks inherit the whole conversation; model resolution order per invocation → frontmatter → env → main model (clauses 1, 3, 5; attacks 4, 5) — https://code.claude.com/docs/en/sub-agents
- Claude Code, "Hooks reference" — hooks "also run inside subagents... the input carries the `agent_id` and `agent_type`"; `SubagentStart`/`SubagentStop` events (clause 1, attack 4) — https://code.claude.com/docs/en/hooks
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2025) — inter-agent misalignment 36.94% of failures (e.g. "fail to ask for clarification" 11.65%, "reasoning-action mismatch" 13.98%); "loss of conversation history" 3.33% (a specification/system-design mode) — distinct classes from single-agent loops (rationale) — https://arxiv.org/html/2503.13657v2
- Google SRE Book, "Addressing Cascading Failures" — multiplicative retries across layers; per-layer retry budgets (attack 3, clause 4) — https://sre.google/sre-book/addressing-cascading-failures/
- Claude Code issue #5456, "Sub-agents Don't Inherit Model Configuration in Task Tool" — evidence that model inheritance for subagents has been a real, user-visible inconsistency in the harness (attack 4) — https://github.com/anthropics/claude-code/issues/5456
- No direct literature found on parent/child *escalation* semantics with budget propagation for LLM agents; a 2026 arXiv cost-performance study of hierarchical compound agents exists (arXiv 2605.16205) but was not fetched in full and is not relied on. Reasoning from harness documentation and distributed-systems precedent.

### Verdict
**PROPOSED (new).** Q3 asks whether passthrough leaves an unacceptable gap and whether there is a cleaner identity model; this decision answers "the gap is acceptable because it is explicit and bounded by SEM-006", and "per-identity scoping with downward constraints and upward typed evidence" as the identity model. Attacks 1–5 are constraints on the design, each answered by a clause or a named follow-up; none refutes the scoping rule. Recommend acceptance at D0 alongside SEM-006.

## Amendments applied
- New decision; no prior text.

## Follow-ups
- [ ] SEM-006: define the wire-level subagent identity and link to parent `route_id`; add hook-event sidecar ingestion for `agent_id` if request shape is insufficient.
- [ ] Golden test (interim): subagent-shaped request during a parent escalation → served at parent's rung, `subagent=true`, no trip-wire evaluation.
- [ ] Golden test (target): child trips a wire → child escalates at its boundary; parent's sticky state unchanged; child failure surfaces as child result; two child failures → parent tool-error wire increments.
- [ ] SAF follow-up (Q5): decide whether a pinned child's returned summary pins the parent's session or is redacted.
- [ ] OPS follow-up: episode budget allocation policy across concurrent children (equal share vs reserve).
- [ ] Implementation note: forks start at the parent's served rung (CAS-006), not at a fresh decision.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-02 | Proposed (adversarial review) | — |
