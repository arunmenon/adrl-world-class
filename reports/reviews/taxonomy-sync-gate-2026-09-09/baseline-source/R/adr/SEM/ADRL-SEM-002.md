# ADRL-SEM-002 — Session key from wire headers, then metadata

| Field | Value |
|---|---|
| Bucket | SEM — Interaction Semantics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D3 Shadow for the key *derivation*; D1 for key *durability* (session→route state is a single-process Python dict, so the key's meaning does not survive a proxy restart) |
| Review verdict | AMEND |
| Tenets | 1, 6, 8 |
| Related decisions | SEM-001, SEM-003, SEM-006, SAF-002, MEM-001, MEM-005, OPS-001 |
| Open questions | Q3, Q5 |

## Decision

The session key is derived, in order of preference, from the `x-claude-code-session-id` header, then `metadata.user_id`, then a stable anonymous fallback; the key is combined with the agent lineage (`x-claude-code-agent-id`, or the parent's key when absent) to form the routing identity, is stored only as a keyed hash, and the fallback is scoped so that unrelated processes can never share routing or privacy state.

1. The stable anonymous fallback is derived from the client connection identity (peer address and port, plus process-local salt) and is valid only for the lifetime of that connection; two connections never share a fallback key.
2. `metadata.user_id` is treated as opaque and possibly user-level rather than session-level; when it is the only key available, the session boundary is additionally cut on any change of system-prompt prefix or on a `count_tokens`/pre-warm burst that indicates a new conversation.
3. The raw header or metadata value is never written to the ledger; a keyed hash (HMAC with a per-deployment secret) is, so that the ledger cannot be joined back to a person without the key.

## Product service evidence, 2026-09-07

The product session ID is the assertion-bound native session ID, hashed by the existing resolver. Credential renewal for that ID retains the same binding, route history and privacy identity. Cross-session credentials and conflicting native headers are rejected for bound traffic. Separate child binding and automated CLI resume remain unsupported.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

## Earlier foundation evidence, 2026-09-07

The product foundation extracts Claude Code's wire identity signals into `ClaudeCodeAdapter`
and leaves session/lineage derivation in the existing identity resolver. Four golden comparisons
against the unmodified implementation preserve the header, metadata, connection-fallback and
lineage-derived identities. These are correlation signals; the adapter does not authenticate a
workload or replace TRU-001's authority checks. No other harness adapter was implemented.

This is a refactor with offline regression evidence, not a new live-harness measurement or a
reassessment of every historical follow-up below. See the [implementation record](../../reports/adrl-product-foundation-implementation-2026-09-07.md)
and [register synchronization](../../reports/adrl-register-sync-2026-09-07.md).

## W3.1 retained operator captures, 2026-09-08

The internal capture path requires an existing bound session and matching workload, session identity and unexpired authenticated-principal context; the supplied workspace must match the signed inventory root. An attempt UUID is separate from the session and cannot manufacture a routing decision. Cross-session capture lookup and mismatched workload/root cases are denied. Parent relationships remain operator declarations until W3.2, and no child-session binding is added.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

Journal starts and transitions reuse the previously authenticated local principal and bound session, validating workload, session, expiry and canonical workspace. Attempts and future capture IDs remain distinct from session and route identities. Cross-session access, changed workspace under the same request ID and mismatched parent scopes are denied. The workspace reservation applies across sessions on one ledger, not across arbitrary installations. No new child-session binding or native harness identity guarantee is added.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## Context and rationale

You need to know which conversation this is, without a session ID. Claude Code carries a per-session identifier in `metadata.user_id` — a Phase 0 experiment that resolved favourably and let the team delete a planned hashing fallback. The stable anonymous fallback exists so that, if the key is absent, unrelated developers' traffic still cannot accidentally share routing state.

The amendment reorders the preference because Anthropic has since documented a purpose-built header: `x-claude-code-session-id`, "a unique identifier for the current Claude Code session. Use it to aggregate all requests from one session without parsing request bodies." By contrast, `metadata.user_id` is documented by the Messages API as "an external identifier for the *user* … Anthropic may use this id to help detect abuse", with a 512-character limit and no session semantics promised. Phase 0 observed that Claude Code populates it with something session-specific; that is an empirical fact about a client version, not a contract, and the header is the contract. The amendment also adds what the original left silent: how the fallback is actually made stable, how the key composes with subagent identity, and that a session key is a user identifier for privacy purposes and must be hashed at rest.

## Adversarial review (2026-09-02)

### Steelman
A router that cannot tell conversations apart cannot be sticky, cannot pin, and cannot attribute outcomes; the session key is the primary key of the whole ledger. Phase 0 found a real per-session value on the wire and simplified the design around it, which is exactly the "every correction simplified the design" pattern the overview celebrates. The anonymous fallback is defensive engineering against the one failure that would be catastrophic — two developers' pins and routes crossing.

### Attacks
1. **The chosen field is documented as a user ID, not a session ID.** Anthropic's API reference describes `metadata.user_id` as an external identifier for the user, for abuse detection. Whatever Claude Code puts there today, nothing stops a future release from putting an account-stable value there — at which point every session of a developer shares one key, a pin taken in one session persists into every later session (SAF-002 becomes a permanent per-developer pin), and sticky routes bleed across unrelated tasks. The documented session header removes this dependency.
2. **"Stable anonymous fallback" is not defined.** Stable across what? If the fallback is a constant, all key-less traffic shares state — the exact failure the sentence claims to prevent. If it is per-connection, it is not stable across the harness's connection pool. If it hashes the system prompt, two developers on the same repo with the same CLAUDE.md collide. The decision asserts a property without a construction.
3. **Subagents share the session key.** Every subagent request carries the same `x-claude-code-session-id` (and presumably the same `metadata.user_id`). Keyed on session alone, three parallel subagents and the parent write to one sticky-route slot in a Python dict, and the last writer wins. SEM-006 needs a lineage-qualified identity; SEM-002 is where the key is defined, so the composition belongs here.
4. **The key is stored in the clear and is PII-adjacent.** MEM-005 suppresses raw prompts and embeddings for private turns but says nothing about the session key. If `metadata.user_id` ever carries an account-derived component, the SQLite ledger becomes a per-person activity log joinable to HR data — at the company that is a privacy-review item in itself. Hash at rest, keyed, is cheap.
5. **The key's meaning is not durable.** The pack states session-to-route tracking is "held in a Python dict (single-process)". A proxy restart forgets every session's route *and pin* while the harness keeps sending the same key. The decision reads as if the key indexes durable state; today it indexes memory that evaporates. This is the SAF-002 durability finding seen from the SEM side.
6. **Resumed sessions.** `claude --resume` continues a transcript in a new process. Whether the session header or metadata value is preserved across resume is not stated in the docs fetched for this review; if it changes, a pinned transcript resumes unpinned. The decision should require the pin to travel with the transcript fingerprint, not only the key (Q5).

### Evidence
- Anthropic, "Gateway protocol reference" (Claude Code docs) — `x-claude-code-session-id` "a unique identifier for the current Claude Code session"; `x-claude-code-agent-id` present only on subagent requests, generated fresh per spawn; "don't treat the agent ID header as a user identifier"; bears on attacks 1, 3 — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Messages API" reference — `metadata.user_id`: "An external identifier for the user who is associated with the request … Anthropic may use this id to help detect abuse. Do not include any identifying information"; max length 512; bears on attacks 1, 4 — https://platform.claude.com/docs/en/api/messages
- Anthropic, "Create custom subagents" (Claude Code docs) — parallel background subagents, nesting to three levels, forks inheriting the parent conversation; bears on attack 3 — https://code.claude.com/docs/en/sub-agents
- ADRL evidence pack, `01-overview-tenets-taxonomy.md` — "Session-to-route tracking is held in a Python dict (single-process)"; bears on attack 5.
- No direct literature found on session-key derivation for LLM proxies; reasoning from first principles for attack 2.

### Verdict
**AMEND.** Attack 1 lands: the decision rests on an observed client behaviour where a documented contract now exists, and the failure mode if the observation changes is severe (permanent per-developer pins). Attack 3 lands and is the seam with SEM-006. Attack 2 is answered by giving the fallback a construction. Attack 4 is a cheap, company-relevant hardening. Attack 5 changes the maturity recommendation for durability, not the decision text, and is resolved in SAF-002. Attack 6 is a follow-up measurement. The Phase 0 finding remains valid as a fallback; it is demoted, not discarded.

## Amendments applied

- Reordered preference: `x-claude-code-session-id` header first, `metadata.user_id` second, anonymous fallback third.
- Added composition with agent lineage to form the routing identity.
- Added sub-clause 1 giving the anonymous fallback a concrete, non-sharing construction.
- Added sub-clause 2 treating `metadata.user_id` as possibly user-level and adding boundary cuts.
- Added sub-clause 3 requiring keyed hashing at rest.

## Follow-ups

- [ ] Measurement: on captured traffic, verify `x-claude-code-session-id` is present on 100% of `/v1/messages` and `count_tokens` requests from supported Claude Code versions; record the minimum version.
- [ ] Measurement: does `x-claude-code-session-id` (and `metadata.user_id`) survive `claude --resume`, `/clear`, and compaction? Write the answer into `reports/assumption-user-id.md`.
- [ ] Golden test: two concurrent connections with no session header and no metadata → distinct fallback keys; assert no shared sticky route or pin.
- [ ] Golden test: parent + two parallel subagents → three routing identities under one session key; assert independent sticky routes and shared pin.
- [ ] Implement HMAC-at-rest for the session key in `memory_facade.py`; migration for existing `router-memory.db` rows.
- [ ] Coordinate with SAF-002: pin state persisted to the ledger keyed by the hashed session key (durability).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-09-07 | Recorded Claude Code adapter extraction and baseline identity comparisons; correlation remains separate from authentication | Decision text unchanged; no adapter extraction evidence previously recorded |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: session header preferred; lineage composition; fallback construction; hashed at rest | "`metadata.user_id` is the preferred session key; a stable anonymous fallback prevents unrelated traffic from sharing state." |
