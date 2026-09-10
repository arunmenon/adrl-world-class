# One-shot fixture execution event contract v1

Frozen 8 September 2026 before runtime edits. Implements the next scoped application of
OPS-001, MEM-001/002/003/005/010, SAF-007 and TRU-001 under
[the active packet](w3-isolated-launch-runtime.md). No general harness, networking or real data.

## Record and ordering

New product_launch_events table: operation_key, event_seq, event_type, payload_json, prev_mac,
mac. Append-only sequence 0..7, payload <=4096 bytes, one unique operation/sequence, at most
32 histories. This reserves a logical maximum 8 x 4096 bytes per admitted history independently
of the encrypted attempt-content quota; it is not preallocated disk. Refuse a largest-event
serialization that would exceed the policy limit before claiming. Old schema/data stay intact.

Payload v1 fields: schema_version, operation_key, workspace_key, host_key_id, resource_id,
resource_created, resource_mac (authenticated original bound-event MAC), engine_ref,
configuration_ref (execution projection HMAC), fixture_ref, policy, sequence, phase, recorded_at,
started_at (null until acknowledged, then exact immutable daemon timestamp), workspace_state,
exact_close_eligible and eligible_for_learning. The last three are blocked/false/false.
No raw command, path, socket, engine profile or task payload is persisted. All event and nested
policy fields, six SQL columns and marker/lock filesystem metadata are inventoried.

Legal transitions: claim -> acknowledged or sealed; acknowledged -> sealed; sealed -> stopped
or discard_issued; stopped -> discard_issued; discard_issued -> discarded. Repeated identical
phase is read-only, never another side effect. Every history authenticates against the original
resource binding, immutable fields and previous MAC. Interior gaps/corruption fail; an earlier
valid prefix alone is not detected. Marker presence denies launch even after ledger-only rollback.

Prevalidate readable started attempt/grant and exact never-started original binding. Validate
the pinned fixture layer (RootFS single diff-ID equals the recorded tar SHA), image ID, exact
argv, explicit seccomp and engine capability profile. Publish the permanent denial marker with
exclusive create/fsync file/directory; release marker lock before ledger waits. Then append a
unique claim with a fresh admission check. Only that original marker/claim caller sends start,
once, requiring HTTP 204. A lost claim acknowledgement never authorizes dispatch.

After acknowledged start, validate the exact StartedAt and execution projection, append
acknowledged then seal future admission. The worker itself runs outside the caller event loop,
observes authority/stop/deadline, stops a known launch and observes matching exit before stopped.
Cancellation drains this worker. The independent seven-second lifetime belongs only to the
pinned self-authored binary. Host owner death leaves an explicit recovery obligation; there is
no general hard real-time or arbitrary-harness watchdog claim.

Recovery never starts or resumes dispatch. It authenticates existing history and original exact
resource, seals and discards, then confirms exact-ID absence. If audit append fails, separately
authenticated emergency cleanup may still run; report physical resource observation separately
from audit failure, never invent a durable terminal event. Configuration/engine/known StartedAt
mismatch refuses cleanup. A marker alone grants no cleanup authority. All fences remain blocked.

## Policy and fixture

ExecutionPolicy v1 freezes <=32 histories/markers, <=8 events, 4096 event bytes, <=64 marker
bytes; local nonblocking lock, private mode-0700 launch-denials-v1 under the keystore root,
mode-0600 operation-key.denied files, fixed version text plus newline. Presence including partial
or malformed markers denies launch forever. No marker release/removal API. Lost/replaced roots
or restoration of both database and marker/key state remain unqualified.

Policy also records the pinned Docker 27.3.1/API 1.47/Linux arm64/kernel/cgroup profile, required
memory/swap/PIDs/CPU capabilities, unsupported OOM control, public seccomp SHA, self-authored tar
and executable SHA, fixed /probe forced_stop argv, polling/deadline and ledger-wait bounds.
No policy option expands fixture authority. Only OOM false/null is projected; all other original
Config/HostConfig/mount/image/name/command plus Id/Created fields retain byte-exact canonical JSON
comparison. Raw engine profile and original image-layer evidence are used in memory and hashed.

## Acceptance before closure

Meaningful offline fault tests: known stop; lost startup/claim/ack/seal/discard acknowledgement;
competing callers; marker-only/claim-only and prefix rollback; unsafe marker root/partial file/
capacity/fsync; wrong or revoked/expired/closed principal/grant; engine/configuration/StartedAt
drift; repeated cancellation; resource disappearance; audit failure with cleanup; reopened-store
recovery; fixture/HTTP profile refusal. Preserve all previous checks, run all eleven checks and
record source hashes. Real-engine runtime acceptance needs a separately frozen finite packet;
the preceding research batches remain closed. No maturity promotion or complete-W3 claim.

## Pre-closure refinement, 2026-09-08

Self-review after the first runtime engine batch adds a separate operation recovery lock under
private launch-recovery-locks-v1, recorded in ExecutionPolicy and the filesystem inventory.
Only authenticated existing histories create these empty keyed-name lock files, bounded by
32 histories. The nonblocking lock spans recovery ledger/daemon work; ledger callbacks never
acquire it and marker publication never holds its own lock across a ledger wait. This serializes
competing cleanup callers. An already-issued discard reconciles only exact absence; a still-
present resource stays uncertain without another DELETE. The independently authenticated
emergency cleanup exception remains when audit recording is unavailable, without an exactly-once
network-delivery claim. All prior contract text and engine evidence remain preserved.

The first four-case runtime batch had three passing cases and one final test assertion failure:
erasure cleanup succeeded, but the relaunch-denial assertion expected ValueError rather than the
existing LedgerAppendFailure wrapper. All four fixtures were confirmed absent. Correct that
assertion and retain the regression controls for recovery serialization before the second and
last focused invocation. The first executed source snapshot is preserved in private evidence.
