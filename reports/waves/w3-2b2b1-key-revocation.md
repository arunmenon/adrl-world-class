# W3.2b2b1: Persist revocation before changing a key

Packet `W3.2b2b1-key-revocation-v1`, frozen 8 September 2026 before code changes.
Parent: [recovery and process ownership](w3-2b-process-ownership.md).
Entry: W3.2b2a, 697 passing tests. Owner: Codex implementation/self-review.

## Observed failure and course correction

A disposable pre-change probe forced the session-key shred audit to fail. The key file
had already been removed; restoring its saved wrapped bytes made the old key readable,
and deleting that restored file allowed a new key for the same session to be created.
This is a lower-level ordering hole in the intended no-resurrection contract. Correct it
before wiring process/erasure/release coordination. No actual user keys or payloads were used.

## Frozen scope

Publish a private per-session revocation marker before destructive key-file operations.
Flush the marker and its directory before proceeding. Reads, presence checks and key
creation honor the marker, including when a key file is restored or deletion/audit fails.
An existing erasure or shredded-key audit also denies access to legacy restored keys.
Record no key, raw session text beyond the existing opaque filename identity, path or reason
in marker contents; use a fixed version identifier. Marker presence is fail-closed even if
its contents are incomplete. Never remove the marker through the keystore API.

Use one private persistent POSIX advisory lock per keystore root, shared for reads and
exclusive for initialization/create/shred. Acquire nonblocking and fail explicitly on
contention; no waiting loop or retries are introduced. Reject unsafe session basenames,
symlink/special lock files and direct symlink directories. Release the lock before waiting
for the existing ledger audit, so a writer needing a key cannot deadlock behind its audit.
This coordinates cooperating current implementations, not hostile account owners, old
binaries, network filesystems or the full multi-worker runtime.

Use atomic private key-file replacement and file/directory flushing for writes. Preserve
existing key wrapping and host secrets. A revocation attempt on an absent key still creates
the marker. Retry can finish deleting a residual key and record its audit; never return a
success receipt after a failed required step. Do not claim that overwriting a file securely
erases SSD blocks, snapshots, cached plaintext or backups. If marker publication fails,
surface failure and leave key mutation unperformed; if publication partially exists, readers
remain denied and a retry can flush it before deletion.

Teach product erasure status to recognize persistent revocation even when its ledger audit
failed, preserving denial of session binding and reads. No public endpoint, schema migration,
new expiry policy, key-restoration authority, journal terminal transition or workspace/grant
release is introduced. Quota commitments and pending journal state remain unchanged.

The new filesystem metadata must be inventoried with its lifecycle and restoration limits.
Preserve old successful audit fields and content; no SQL update/delete. Raw session-key
bytes remain outside the ledger. All fixtures use disposable directories and self-authored
short-lived subprocesses; no model calls, new spend or real harness execution.

Owning clauses: MEM-010 no resurrection and erasure failure ordering; MEM-005 metadata
inventory; MEM-001 append-only audit; OPS-001 cooperating access/recovery; TRU-001 product
binding denial. Preserve all ADR wording/history/status/maturity fields through dated notes.

## Acceptance and limits

| Case | Required observation |
|---|---|
| Audit fails after key-file removal | Revocation persists; restored key reads and same-session recreation denied |
| Key removal fails after marker publication | Error surfaced; existing key inaccessible through current API |
| Process dies after marker, before deletion | Reopen denies key; retry can finish cleanup without removing revocation |
| Marker creation/flush fails | No destructive key operation; incomplete marker presence remains fail-closed |
| Missing key, repeated erase and restored key | Persistent denial; accurate removal result and retryable audit |
| Existing successful legacy audit without marker | Restored file denied by attached ledger |
| Cooperating callers contend | Explicit nonblocking failure; no competing key versions or deadlock |
| Ledger writer needs a key while audit is queued | File lock has been released before the audit wait |
| Corrupt key or unsafe path/lock | No arbitrary file operation or hidden successful erasure |
| Product and attempt/capture access after audit failure | Denial survives restart; pending quota/workspace commitment retained |

One writer; at most three failed repairs per task. Complete engineering, inventory, API/map
and register checks, publish actual failures and preserve the pre-change probe. This closes
only key-revocation ordering. W3.2b2b2 still needs in-memory process/erasure coordination and
safe reservation release. Complete writer containment, active plaintext leases, crash-copy
recovery, capture association and full W3 remain open. Marker-plus-ledger rollback, physical
power-loss testing and independent security review are not supplied by this slice.

## Disposition, 8 September 2026

Locally validated: 26 new fault cases and one product integration case; 724 total tests
and eleven engineering checks pass on the first combined run. The pre-change audit-failure
restoration/recreation probe is preserved. Nonblocking special-file opens and owned pending
key-write cleanup were added during self-review. No behavioral test failed; lint findings
were corrected. Five owning ADRs preserve prior wording and all 77 status/maturity fields.

See the [report](../adrl-w3-2b2b1-key-revocation-2026-09-08.md),
[evidence/probe](../research/adrl-w3-2b2b1-key-revocation-2026-09-08.json) and
[source diff](../research/adrl-w3-2b2b1-key-revocation-2026-09-08.patch).
This closes revocation ordering only. W3.2b2b2 process/erasure/reservation coordination,
complete writer containment and all remaining real-capture gates stay open.
