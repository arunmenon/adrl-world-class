# W3.2b2a: Leave room to record what happened

8 September 2026. Offline engineering under the
[roadmap](adrl-implementation-roadmap-2026-09-07.md) and
[frozen capacity packet](waves/w3-2b2a-terminal-capacity.md).

ADRL now reserves space for a terminal record before accepting a new journal attempt.
**All 697 tests and eleven engineering checks pass**, including 28 new capacity cases.
This closes a specific reliability gap: ordinary journal work can no longer use the slot
or bytes reserved for that attempt's cancellation or interruption record.

## The problem in plain language

Imagine beginning a task, filling the journal, and then discovering that there is no room
left to write “this task was interrupted.” ADRL would be left with a pending record even
though the operator was trying to explain how the attempt ended.

The v1 journal allowed this. It could use its last event slot, reach its byte limit, or be
given a lower limit before the terminal record was written. The new v2 policy makes a
small commitment at admission: leave one event slot and a bounded byte allowance available
for cancellation or explicit interruption.

| Situation | New behavior |
|---|---|
| The initial event fits, but its terminal allowance does not | Refuse the start without recording a partial attempt |
| A close request would spend the reserved slot or bytes | Refuse the close request; keep the terminal allowance available |
| Another caller offers a larger budget | Preserve the smaller ceiling promised to active attempts |
| The caller lowers its limit after admission | Apply it to new/nonterminal work; preserve the original bounded terminal grant |
| The terminal record commits but its acknowledgement is lost | A retry returns the same record without spending capacity twice |
| A session key is erased | Deny further encrypted writes and keep its pending commitment visible |

The last row is deliberate. A quota reservation cannot restore an erased key, prove a
process stopped, or make it safe to release a workspace. That coordination is still next.

## What was implemented

New starts use `operator-attempt-policy-v2`. The initial encrypted event and its capacity
grant commit in one database transaction. The default terminal allowance is 1,024 bytes;
the versioned field allows 1,024–4,096 bytes. Before admission, every permitted terminal
reason must fit the event and allowance limits. The existing upper limits remain: three
attempts per session, eight events per attempt, 8 MB per event and 32 MB of logical history.

Every append accounts for stored encrypted bytes plus all pending grants. A terminal event
consumes its own allowance. Its original grant stays in the append-only ledger; the code
infers consumption from the terminal history. There is no mutable release counter or
deletion of old evidence. Once an attempt consumes its grant, its active admission ceiling
ends, while its stored history still counts against quota.

Schema 9 adds a capacity-version header and five grant fields. The header is authenticated
with v2 event encryption; the grant reuses existing keyed session, attempt and start-event
references and records the allowance and ceiling. Reads and transitions check the grant
against the owning encrypted policy. Missing required grants and structural mismatches
prevent admission. The data inventory now covers all **279 stored fields**.

Historical v1 records still decrypt, retain their original limits, and support matching-policy
retries and continuations. A new v1 start is refused. Migration does not rewrite old
ciphertext/nonces or pretend that historical attempts had reserved capacity. V1 continuations
also respect active v2 commitments. Public API preview 4 is unchanged.

## Evidence and corrections

The new cases cover quota and slot exhaustion, every terminal reason, lowering/raising
caller budgets, concurrent admission on different workspaces, restart and duplicate requests,
lost acknowledgement, transaction rollback, missing or corrupt grant/header data, erasure,
expiry and schema-8 v1 compatibility. The old one-slot behavior remains tested through a
legacy record; the new policy requires at least two slots.

The first focused run had **62 passes and four fixture failures**. Two example budgets were
larger than the failure boundary they were meant to exercise; two migration fixtures treated
a fingerprint digest as a file manifest. Measuring the actual encoded sizes and correcting
the manifest setup resolved those errors without changing the frozen reservation contract.
Lint also found three long SQL fixture strings. After correction and two additional cases,
all **68 focused cases** passed. The first full combined run passed **697 tests and all
eleven checks**, with no declared-source drift. No failed invariant was waived.

The implementation and its evidence were self-reviewed by the same assistant. This is not
independent evaluation or security review.

## Maturity and remaining limits

This improves the reliability of ADRL's evidence collection. It does not demonstrate task
quality, routing savings or RSI. A terminal journal entry still means a recorded cancellation
or interruption; it is not evidence that every writer stopped or that the task succeeded.
Attribution remains unestablished and learning eligibility remains false.

Five owning ADRs now record the applied contract: **MEM-001, MEM-002, MEM-005, MEM-010
and OPS-001**. Their earlier wording and all 77 architectural-status/maturity fields remain
intact. **No grade is promoted.** Full W3 and exact task-close attribution remain open.

This is logical quota reservation, not preallocated disk space. Disk/database failures,
expired credentials, erasure and corruption can still prevent an append. Metadata does not
provide an external tamper anchor or protection against a hostile database writer. Mixed
old/new runtime writers are not qualified. Pending erased attempts can still block capacity
and a journal workspace reservation; the implementation keeps that uncertainty visible.

## Next

W3.2b2b must coordinate erasure, actual process ownership and reservation release, including
restart and failure ordering. It must preserve the difference between “we recorded an
interruption” and “the workspace is safe to reuse.” Complete writer containment is still
unqualified; the earlier process-group runner cannot contain detached or unrelated writers.

Only after that boundary is evidenced should W3.2b3 bind a close request to its retained
capture. Active plaintext lease and crash recovery must also pass before real task payload
capture. This slice used synthetic fixtures only: no native harness task, model-service call,
new paid usage, live routing change, commit or deployment.

The [journey](adrl-implementation-journey.md) records the progression and the
[execution state](research/adrl-execution-state.json) identifies the next bounded packet.

Evidence: [check/source manifest](research/adrl-w3-2b2a-terminal-capacity-2026-09-08.json),
[source diff](research/adrl-w3-2b2a-terminal-capacity-2026-09-08.patch),
[journal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py),
[capacity migration](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/migrations/0009_attempt_capacity.sql),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_capacity.py) and
[internal guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
