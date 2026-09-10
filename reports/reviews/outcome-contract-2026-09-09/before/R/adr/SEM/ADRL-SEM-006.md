# ADRL-SEM-006 — Subagents inherit constraints now, routing later

| Field | Value |
|---|---|
| Bucket | SEM — Interaction Semantics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D0 Design, review recommends D0 for routing identity and evidence separation, but requires the constraint-inheritance half to reach D2 *before* any live pilot — because the current interim (passthrough) violates SAF-002 for forked subagents |
| Review verdict | AMEND |
| Tenets | 2, 6, 8 |
| Related decisions | SEM-001, SEM-002, SAF-002, SAF-004, CAS-003, CAS-005, MEM-001, MEM-009 |
| Open questions | Q3 |

## Decision

Subagents are linked to the parent for constraints but have separate routing identity and evidence; the interim position is *constrained passthrough*: subagent requests inherit the parent's privacy pin and gate state immediately, keep the model the harness requested, and are shadow-logged under their own agent lineage.

1. Lineage is taken from `x-claude-code-agent-id` and `x-claude-code-parent-agent-id`; the pin and gate state of a subagent is the union of its own gate results and its ancestors' at spawn time and thereafter (a child pinning does not pin the parent; a parent pinning pins all descendants from that moment).
2. Until Q3 is resolved, ADRL does not choose a rung for subagents: the harness's per-subagent model selection (`model:` frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, or inherit) is honoured, except that a pinned lineage is served locally or blocked per SAF-004/005.
3. Every subagent request is recorded with its own `route_id` and lineage so that outcomes are never attributed to the parent's turn; nested escalation is a separate decision (CAS, Proposed).

## W3.2b1 owned process groups, 2026-09-08

W3.2b1 records a scoped process-descendant limitation: same-group cleanup is exercised, while a deliberately detached fixture survives. Direct-parent exit cannot establish completion of its full descendant tree. This is process cleanup evidence only; OS process ancestry is not harness agent lineage. No subagent routing identity, wire correlation, privacy-pin inheritance, model selection or per-agent outcome attribution changes. The maturity and harness-level follow-ups above remain in force.

See the [plain-language report](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b1-process-ownership-2026-09-08.json),
[runner](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_owner.py),
[launcher](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_anchor.py),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_process_owner.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/process-ownership.md).
All 669 tests and eleven checks pass on the recorded Darwin build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved. Full W3
and exact task-close attribution remain open.

## W3.2b2c writer-boundary research, 2026-09-08

A detached child formed its own process group inside the fixture container. Process-group detachment did not escape the tested PID-namespace lifetime, while death of the outside Docker client did not end that lifetime. These are separate parent/descendant and owner relationships; a harness parent hint or saved host PID cannot be substituted for the proposed resource-ownership contract. No change to shipped child-session identity or pin propagation follows.

See the [plain-language report](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md),
[experiment and source evidence](../../reports/research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[fixture source](../../reports/research/writer-boundary-2026-09-08/probe.go),
[frozen packet](../../reports/waves/w3-2b2c-writer-boundary.md) and
[next ownership packet](../../reports/waves/w3-2b2d-resource-ownership.md).
The corrected research run completed six bounded observations, including negative controls.
The previously passing 759-test/eleven-check runtime source is unchanged; all 300 declared
hashes were reverified, not rerun. This research changes no runtime behavior, architectural
status, maturity, release authority or whole-W3 completion claim. Prior wording is retained.

## Context and rationale

A subagent should inherit the parent's constraints (if the parent is privacy-pinned, the child must be too) but have its own routing identity and evidence, so its outcomes are not misattributed to the parent's turn. None of the routing half is built — D0 — and the original interim position was to pass subagent traffic straight through.

The amendment changes the interim, not the decision. Passing subagent traffic "straight through" means: a *fork* subagent — which by Claude Code's definition "inherits the entire conversation so far … the same system prompt, tools, model, and message history as the main session" — carries a pinned parent's full transcript to the cloud gateway. Non-fork subagents receive the task-delegation text the parent model wrote, plus CLAUDE.md and git status, which routinely contain the very file contents or paths that triggered the pin. So the interim silently undoes SAF-002 for the fastest-growing class of traffic. The good news is that the constraint half is now cheap: Anthropic's gateway contract puts agent and parent-agent identifiers on every subagent request, so "inherit the parent's pin" is a header lookup, not a design problem. The routing half (which rung serves a subagent, how nested escalation interacts with a parent in flight) remains D0 and honestly so; the interim honours whatever model the harness asked for, which is also what FND-001's transparency demands.

## Adversarial review (2026-09-02)

### Steelman
Marking this D0 is the register at its most honest: parent/child escalation under concurrency is genuinely unsolved, the corpus treats subagent work as free at the margin, and Q3 is open. Passing subagent traffic through is the zero-risk *routing* choice — it changes nothing the developer would notice — and the decision text already commits to the two properties that matter (constraint inheritance, separate identity) so that when it is built, it is built right.

### Attacks
1. **The interim breaks the pin.** A fork subagent's first request is byte-for-byte the parent's transcript plus a delegation message. If the parent is pinned and subagent traffic passes through to the gateway, the pinned code leaves the machine. Non-fork subagents get CLAUDE.md, git status and the parent-written task description — often including the secret-bearing file name or snippet. "Passthrough" is a privacy regression, not a neutral default.
2. **Constraint inheritance is a header lookup, so D0 is no longer honest for that half.** The harness sends `x-claude-code-agent-id` on every subagent request and `x-claude-code-parent-agent-id` on nested ones. Resolving the ancestor chain and OR-ing pin state is an afternoon's work against `router/state.py`. Leaving it at D0 because the *routing* half is hard conflates two problems with very different costs and very different consequences.
3. **Routing a subagent contradicts the harness's explicit model choice.** Subagent definitions carry `model: sonnet|opus|haiku|inherit`; Claude Code resolves per-invocation model, frontmatter, env var, then the main model. If ADRL sends an `opus`-declared reviewer subagent to a local model, it overrides an explicit developer configuration — a FND-001 violation with no cache justification. The interim must honour the harness's selection.
4. **Concurrency against a single-process dict.** Subagents run in parallel by default and nest to three levels. Session-to-route tracking is a Python dict keyed (today) by session. Parallel siblings racing on one slot is a correctness bug for sticky state and a safety bug for pins (a child's pin write can be overwritten by a sibling's route write). Lineage-qualified keys (SEM-002 amendment) are a prerequisite.
5. **Evidence pollution.** Without separate `route_id`s, a subagent's tool-loop failures are appended to the parent's turn outcome, tripping the parent's trip-wires (CAS-001) and mislabelling the parent's rung as failing (MEM-004). The register already knows this ("so its outcomes are not misattributed"); the interim passthrough does not log subagents at all, so the shadow corpus is also missing them.
6. **Agent teams are a different identity model.** The gateway contract notes teammate agents "reuse a stable name-based ID across reconnections", unlike per-spawn subagent IDs. A lineage model built only on per-spawn IDs will treat a reconnecting teammate as a new agent and lose its pin. The decision should not assume IDs are ephemeral.

### Evidence
- Anthropic, "Create custom subagents" (Claude Code docs) — isolated context windows; forks inherit the entire parent conversation; `model:` frontmatter and resolution order; parallel background execution; nesting to three levels; initial context includes CLAUDE.md, git status and the delegation message; bears on attacks 1, 3, 4 — https://code.claude.com/docs/en/sub-agents
- Anthropic, "Gateway protocol reference" (Claude Code docs) — `x-claude-code-agent-id` present only on subagent requests, fresh per spawn; `x-claude-code-parent-agent-id` for nested agents; teammate agents reuse stable name-based IDs; bears on attacks 2, 6 — https://code.claude.com/docs/en/llm-gateway-protocol
- George Sung, "Tracing Claude Code's LLM Traffic" (Medium, 2026) — subagents receive identical system-reminder blocks with CLAUDE.md content and restricted tool lists; bears on attack 1 — https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5
- ADRL evidence pack, `01-overview-tenets-taxonomy.md` — "Session-to-route tracking is held in a Python dict (single-process)"; "subagent work effectively free at margin (directional findings usable, magnitudes not)"; bears on attacks 4, 5.

### Verdict
**AMEND.** The decision sentence is right and stays. Attack 1 is the finding: the *interim* is not neutral, it is a pin bypass, and it must be replaced before any pinned session is exposed to a subagent. Attack 2 shows the fix is cheap because the harness now supplies lineage on the wire. Attack 3 fixes the interim's routing posture (honour the harness). Attacks 4–6 are prerequisites and design notes that flow into SEM-002 and CAS. Q3 (nested escalation, split-brain) remains genuinely open and is left at D0; the review does not pretend otherwise.

## Amendments applied

- Replaced the interim "pass subagent traffic straight through" with "constrained passthrough": inherit pin/gate state, honour harness model choice, shadow-log under own lineage.
- Added sub-clause 1 defining lineage from wire headers and the direction of pin inheritance (descendants only).
- Added sub-clause 2 fixing the routing posture until Q3 resolves.
- Added sub-clause 3 requiring per-subagent `route_id` and naming nested escalation as a separate Proposed CAS decision.

## Follow-ups

- [ ] Implement ancestor-chain pin inheritance keyed on `x-claude-code-agent-id`/`-parent-agent-id` in `router/state.py`; unit and fault tests (D2) before any live pilot.
- [ ] Golden test: pinned parent spawns a fork → fork's first request is served locally or blocked; never reaches the gateway.
- [ ] Golden test: parent unpinned, child reads a secret → child lineage pinned, parent unaffected; a later fork of the parent is unpinned; a later child of the pinned child is pinned.
- [ ] Golden test: three parallel siblings with independent sticky routes and one shared inherited pin; no lost writes.
- [ ] Shadow corpus: begin logging subagent requests with their own `route_id`s so Q3 can be argued from data (currently they are not logged).
- [ ] Handle stable teammate IDs (agent teams) in the lineage model; do not assume per-spawn IDs.
- [ ] New ADR (CAS, Proposed): nested escalation and parent/child split-brain rules.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b1 process ownership and tested cleanup limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: interim changed from passthrough to constrained passthrough (pin inheritance via wire lineage); harness model choice honoured; per-lineage evidence | "Subagents are linked to the parent for constraints but have separate routing identity and evidence." |
