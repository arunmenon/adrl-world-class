# ADRL now coordinates stopping work and keeping its workspace blocked

8 September 2026 | W3.2b2b2 | Locally tested with synthetic tasks

**ADRL can now connect an attempt record to an owned process, request a stop when authority is
lost, and preserve a workspace block through interruption and restart.** This is a useful step
toward dependable task evidence. It is still a restricted internal mechanism for disposable
test workspaces, not the real-task execution release.

Think of an attempt record as a job ticket. Marking the ticket “cancelled” does not prove that
every tool has stopped working. ADRL now keeps a separate, durable block on the workspace so
that closing the ticket cannot accidentally authorize another supervised job there.

## What changed

Previously, the attempt journal, process owner and key-revocation mechanism had separately
tested behavior. This slice connects them through an internal coordinator:

```text
Valid attempt and workspace
            |
   Record a durable workspace block
            |
   Try one owned process launch
            |
   Observe expiry, erasure and journal closure
            |
   Request stop and drain owned group cleanup
            |
   Try to record an incomplete attempt
            |
   Keep the workspace blocked
```

The coordinator checks the authenticated workspace, original v2 attempt and reserved terminal
capacity before admission. Competing coordinators cannot launch through the same block. A lost
acknowledgement never authorizes an automatic retry. A new journal start honors the block even
after the previous journal entry becomes terminal or its session key is erased.

A separate monitor observes loss of authority while the command runs. It can request cleanup
even while the caller's event loop is occupied by an erasure audit. Erasure does not wait for
process cleanup to revoke access. After cleanup, the coordinator tries to record that the
attempt is incomplete, preserving an existing terminal entry. If expiry, erasure or database
failure prevents that record, it says the record is unavailable and retains the workspace block.

## What the tests establish

**All 759 tests and eleven engineering checks pass**, including 35 new coordination cases.
The final combined run has no change to its 300 declared source inputs. Schema 10 adds seven
inventoried fields; the inventory covers 286 schema/payload fields and 289 documented entries.
Public API preview 4 is unchanged. The module map covers 106 modules and still maps 74 of 77 ADRs.

Real local fixture processes exercise normal/nonzero exit, timeout, direct key revocation,
another erasure-service instance, failed audit, expiry, missing keys, journal closure, repeated
cancellation and actual owner-process death. Other cases check admission races, restart, lost
acknowledgements, invalid identity/grants, database faults, policy bounds and unchanged old
ciphertext/grants after migration. No user task payload or model-service call was used.

The fence stores keyed identifiers, a host-key ID, policy and timestamp. It stores no raw
workspace path, command, environment, output or PID. Changing the host HMAC identity refuses
new admission rather than silently producing a different workspace identity. The first policy
allows at most 128 permanent fences per ledger, configurable downward.

## What the failures taught us

Three retained diagnostic runs failed before the final focused run passed. We kept those
failures in the evidence instead of treating only the final result as the journey.

| Retained run | Result | Correction |
|---|---|---|
| First | 27 passed, 3 failed | Fixed a real stale-report bug: a rejected launch could inherit the previous launch's process report. Corrected two fault fixtures that implicitly committed their setup transaction. |
| Second | 32 passed, 3 failed | Distinguished a conservative “authority unavailable” stop from confirmed revocation/closure during concurrent key operations. Corrected the owner-death fixture to use the project's Python environment. |
| Third | 34 passed, 1 failed | An erasure could encounter the existing nonblocking key lock before reaching the audit being tested. Synchronized that fixture to isolate the blocked-audit condition. |
| Final focused | 35 passed | All frozen coordination cases pass after three repair cycles. |

An initial console-only diagnostic was repeated with retained logging and is not used as
validation evidence. Lint found formatting issues, which were corrected. The first complete
eleven-check run passed. No security condition or required check was waived.

Lock contention matters operationally: an erasure that fails before publishing revocation is
still a failed erasure. A monitor that cannot read authority can stop conservatively without
claiming it observed revocation. The product adds no automatic erasure retry; bounded retries
in test setup exercise the existing explicit retry contract.

## What this still cannot promise

The current runner owns a process group. Detached children and unrelated writers can remain
outside it. **There is therefore no workspace-release operation in this backend**, including
when a fence committed but launch did not occur. These permanent blocks make disposable test
execution conservative; they are not the final product's workspace workflow.

Observation is eventual. Erasure can race launch; OS, disk or database delays prevent a hard
stop-time guarantee. An erasure receipt does not certify that this observer has stopped all
writers or removed active plaintext copies. Process reports remain in memory; restart recovers
the block, not a fabricated process outcome. There is no saved-PID recovery, successful task
close, automatic capture association or learning eligibility.

Canonical path identity is not an OS filesystem lock or protection against directory aliases,
replacement, hostile database mutation or backup rollback. Complete containment, active-copy
erasure and crash-copy cleanup remain gates before real task payload capture.

## How this moves ADRL forward

This improves the reliability of the evidence-collection foundation. A future improvement loop
must distinguish completed work from interrupted or uncertain work; it must also avoid borrowing
one attempt's observations for another. We fixed one such error in this slice and added tests
that preserve that distinction.

It does not demonstrate improved routing, autonomous RSI, another harness or production safety.
Eight owning decisions now record the precise application and evidence: OPS-001,
MEM-001/002/003/005/010, SAF-007 and TRU-001. Their prior wording and all 77 architectural-status
and maturity fields remain unchanged. A passing local slice does not promote an entire ADR.

**Next:** inspect and qualify the complete writer boundary, then define a defensible release
contract. The [next packet](waves/w3-2b2c-writer-boundary.md) requires concrete evidence before
choosing a backend. If stronger infrastructure needs a user decision, prepare that choice and
continue independent active-plaintext/crash-recovery work while it is pending. Exact-close
capture association follows the relevant gates. Full W3 remains open.

Read the [running journey](adrl-implementation-journey.md),
[frozen packet](waves/w3-2b2b2-process-coordination.md),
[checks and source evidence](research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[source diff](research/adrl-w3-2b2b2-process-coordination-2026-09-08.patch) or
[runtime boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
