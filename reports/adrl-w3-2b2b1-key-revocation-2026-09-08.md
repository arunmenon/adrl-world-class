# W3.2b2b1: Make revocation survive an interrupted erasure

8 September 2026. A prerequisite recovery fix under the
[roadmap](adrl-implementation-roadmap-2026-09-07.md) and
[frozen revocation packet](waves/w3-2b2b1-key-revocation.md).

We found and fixed an erasure recovery hole: if the audit write failed after a key file was
removed, the keystore could accept a restored copy of that key or create a replacement for
the same session. ADRL now persists revocation before changing the key file and honors that
revocation across reads, key creation and product access. **All 724 tests and eleven
engineering checks pass.**

## What changed in the plan

The next planned work was coordination between erasure, running processes and workspace
release. Inspecting that dependency exposed this lower-level ordering problem. We reproduced
it with a disposable keystore and a deliberately failing database audit, then split out this
repair before connecting more machinery to erasure.

This is a concrete example of course correction during implementation: a testable failure
changed the next engineering slice. It does not demonstrate RSI or an improvement in routing.

## The failure and the fix

Previously, deletion happened first and the audit followed. If the audit failed, neither
operation left a reliable revocation record for the keystore to consult. The probe confirmed
that restoring the saved wrapped file made its old key readable. Removing that restored
file also allowed a replacement key to be created for the same session.

Now a small private marker records “this session's key is revoked” before key-file mutation.
ADRL flushes the marker and its directory, then removes the wrapped key and known temporary
copies belonging to that session. It writes the ledger audit afterward. The marker stays
even when deletion, the audit or the process fails.

| Failure point | New behavior |
|---|---|
| Marker cannot be created | Surface failure; do not begin destructive key mutation |
| A marker exists but flushing/removal fails | Deny key access; surface failure and allow cleanup retry |
| Process dies after recording revocation | Denial survives reopen, even if the wrapped key remains |
| Key removal succeeds but its audit fails | Surface the audit failure; a restored key stays unavailable |
| Someone requests another key for that session | Refuse creation once revoked |

The product API also honors the marker. A failed audit cannot make erased payloads visible
again or permit session rebinding and new observations. The timeline's `erased` state means
the payload is unavailable through this revocation; it does not certify that physical removal
and auditing both finished successfully. The erasure service still returns an error when a
required step fails.

## Supporting mechanics

A private POSIX lock coordinates cooperating keystore readers and writers. It fails explicitly
on contention without a waiting loop. The file lock is released before waiting for the ledger
audit, so a ledger writer needing a key does not deadlock behind that same audit.

Key writes use private temporary files and atomic replacement. Their names identify the
target, allowing later create/shred operations to remove interrupted writes belonging to
that session. Unrelated session files are preserved. Initialization cleans known pending
host-secret writes. Unsafe basenames, symlink/hardlink aliases and special lock/key files
are rejected; nonblocking opens prevent a FIFO from hanging before validation.

The wrapping format, host secrets, database schema 9 and public API preview 4 are unchanged.
The checked inventory still covers 279 schema/payload fields, with three additional
filesystem metadata entries documenting the marker identity, marker version and empty lock.
Temporary files containing host secrets or wrapped keys are explicitly documented as key
material, not harmless metadata. No key bytes are added to the ledger.

## What was tested

Twenty-six new revocation cases and one product integration case cover failed audit,
failed removal, marker creation/flush failure, repeated erasure, absent and corrupt keys,
legacy audits, lock contention, audit/lock ordering, unsafe files, owned temporary copies
and a real process death after marker publication. The product case restores a wrapped
key after the failed audit and checks that the timeline remains unavailable and binding/
event submission remain forbidden. Capture access is also denied; an attempt's pending
state and terminal-capacity grant remain unchanged.

Existing focused coverage passed 165 cases. The initial new fault suite passed 23; expanded
revocation and product coverage passed all 80 cases. The first full combined run passed
**724 tests and all eleven checks**, with no declared-source drift. Lint issues were corrected;
no behavior test failed and no invariant was waived. Self-review added special-file handling
and pending-key-file cleanup before the final run.

The same assistant implemented and self-reviewed this work. Independent security review
has not occurred.

## Maturity and limits

Five owning records now document the correction: **MEM-001, MEM-005, MEM-010, OPS-001 and
TRU-001**. Their earlier wording and all 77 architectural-status/maturity fields remain intact.
**No grade is promoted.** We have stronger local evidence for erasure failure ordering, not
complete erasure qualification or task-output attribution.

The marker cannot withdraw keys or plaintext already returned to a caller. File replacement
and unlinking do not prove secure deletion from SSD blocks, old inodes, snapshots or backups.
Rolling back both the marker/audit and key files is not protected by an external anchor here.
Older binaries, hostile account owners, network filesystems, full multi-worker operation and
physical power-loss recovery are unqualified. The tests ran on the recorded Darwin build.

Crucially, this slice does not stop processes, release workspace reservations or consume
pending terminal grants. It does not change privacy pins, erasure triggers, learning authority
or the task-close rules. No real task payload, native harness task, model-service call, new
spend, live routing change, commit or deployment occurred.

## Next

W3.2b2b2 must connect erasure to actual in-memory process ownership and retain a blocked or
uncertain reservation whenever safe workspace reuse cannot be established. It must cover
restart, expiry and partial failures without restoring keys or deriving kill authority from
a saved process ID.

Complete writer containment, active plaintext leases, crash-copy recovery and durable close/
capture association still gate real task capture. Full W3 remains open. The
[journey](adrl-implementation-journey.md) and [execution state](research/adrl-execution-state.json)
record this course correction and the next bounded action.

Evidence: [manifest and pre-change probe](research/adrl-w3-2b2b1-key-revocation-2026-09-08.json),
[source diff](research/adrl-w3-2b2b1-key-revocation-2026-09-08.patch),
[keystore](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/keystore.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_key_revocation.py) and
[internal guide](/Users/arunmenon/projects/adrl-core/docs/key-revocation.md).
