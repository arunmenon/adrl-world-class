# W3.2: Task attempts and the close boundary

**Execution update, 2026-09-08:** [W3.2a is locally validated](../adrl-w3-2a-attempt-journal-2026-09-08.md),
with 631 passing tests and eleven checks. W3.2b remains open. Quota exhaustion or erasure can
leave pending reservations blocked; terminal-capacity reservation and coordinated release are
explicit next requirements before real execution. Original acceptance cases are preserved below.

Packet `W3.2-attempt-lifecycle-v1`, frozen 8 September 2026 before implementation.
Parent: [W3 packet](w3-task-capture.md). Entry evidence: [W3.1](../adrl-w3-1-operator-captures-2026-09-08.md).
Owner: Codex, implementation and self-review. Product owner: Arun Menon. Independent review is
not claimed. Existing authorization covers bounded local engineering; only synthetic fixtures
are admitted in these slices. No model-service calls, new paid usage, live routing or public API.

## Contract and slices

**W3.2a: durable attempt history.** Record an attempt's start with its initial included-tree
manifest, source/workspace references, task ID, optional parent attempt, reserved future capture
ID and versioned limits. Store each transition as an encrypted append under the existing session
key. Supported transitions are start, request close, cancel and mark incomplete. No successful
completion, stopped-writer or verified-result state is available in this slice. There is no
placeholder supervisor method. That missing capability remains explicit work for W3.2b.

An identical request ID returns its original committed record, including after an acknowledgement
is lost or later phases are appended. A changed command under the same ID conflicts. A repeated
close with a different ID conflicts once close is pending. Out-of-order, post-terminal and
cross-session transitions fail. An initial-start retry uses the original initial manifest;
resending that request after the workspace changes must not replace the original starting point.

Allow one active journal attempt per canonical workspace across sessions on this ledger. Check
that reservation inside the serialized write transaction. This is a journal admission rule, not
an operating-system lock or proof that a terminal attempt's processes stopped. Failed/cancelled
history cannot by itself authorize the next supervisor to reuse a working directory. A parent
must be a terminal attempt for the same task/session/workspace. Starting an attempt after its
capture already exists is refused; no retrospective start attribution.

After reopening, an unfinished attempt stays unfinished and continues to reserve its workspace.
The local operator can append `incomplete` with an explicit reason. The journal does not infer
failure from elapsed time, silently resume a process, delete prior records or declare quiescence.
Fresh accesses and queued appends must recheck identity, expiry and erasure. Restoring an old key
must not bypass a preserved erasure audit. Corrupt sequences/identity/AEAD cannot yield a valid
history. Initial manifests contain names and hashes, not file contents, and remain encrypted.

**W3.2b: owned writers and capture association.** Before coding, refine the supervisor packet
around an explicit execution owner, process identity, writer containment, start/close ordering,
resource bounds, cancellation and restart. A leader process exiting is insufficient while a
descendant can still write. Bind capture to the durable close request and an evidenced writer
barrier. A fingerprint alone grants no completion attribution. Unsupported or ambiguous writer
containment yields incomplete/unestablished attribution, not a quiet reduction of the claim.
Do not infer process liveness or kill authority solely from a persisted PID after restart.

## Limits and ownership

One implementation writer; at most three failed repairs per task. At most three attempts per
session, eight events per attempt, 8,000,000 bytes per encrypted event's plaintext encoding, and
32,000,000 ciphertext-plus-nonce bytes for the attempt table. These are upper bounds, may be
lowered, and are recorded in the starting policy. The global quota includes erased ciphertext;
it is not an exact SQLite/WAL filesystem quota. Existing capture scan limits apply to the initial
manifest. No materialization or file-content archive is added here. Synthetic fixture state is
removed afterward. Individual check commands retain the ten-minute engineering-runner timeout.

Owning clauses: MEM-001 append/idempotency; MEM-002 attempt lifecycle; MEM-003 provenance;
MEM-005/010 protected payload and erasure; SEM-002/007 identity/product boundary; TRU-001
operator authority; OPS-001 scoped journal concurrency. This does not settle DQ6 or graduate a
decision. Active-copy erasure and crash cleanup still gate actual task payload capture.

## Frozen acceptance cases

| Case | Expected observation |
|---|---|
| Start, edit workspace, retry same start | Original manifest/time retained, one start row |
| Changed task, capture ID, policy or workspace under same event ID | Conflict without replacement |
| Close before start, repeat close with new ID, transition after terminal | Explicit conflict; no fabricated phase |
| Duplicate transition after later phases/reopen | Original acknowledgement returned; history retained |
| Two concurrent starts for one workspace in different sessions | Exactly one admitted; other explicitly rejected |
| Separate tasks/workspaces | Independent histories and identities |
| Parent task/session/workspace mismatch or nonterminal parent | Reject the start |
| Attempt's capture predates start | Reject retrospective start |
| Restart with pending close | Pending stays pending and reserves workspace; explicit incomplete is an appended event |
| Missing/wrong/expired identity, queued expiry/erasure, restored old key | Deny; no new key or resurrected history |
| Corrupt, missing or misordered event | Reject history; no successful/complete projection |
| Failed transaction or acknowledgement lost after commit | No partial history, or stable idempotent recovery of committed record |
| Bounds exceeded | Fail without partially appending; no automatic quota reclamation |
| Public contract and legacy captures/receipts | API preview 4 unchanged; migration preserves old evidence |
| Fake success/quiescence/verification command | Schema rejects it; no such lifecycle capability in W3.2a |

Passing W3.2a closes only the journal slice. Full W3.2 requires W3.2b evidence, and full W3 also
requires lease/crash recovery, retained verification/CLI/timeline binding and the bounded native
Claude demonstration. Publish actual results, failed checks, source identities and limitations;
synchronize the owning ADRs/index/buckets/changelog and update the running journey after closure.
