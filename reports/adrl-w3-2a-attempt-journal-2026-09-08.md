# W3.2a: Remember what a task actually claimed

8 September 2026. Engineering slice locally validated. W3.2 and full W3 remain open.

ADRL now has an encrypted task-attempt journal. It remembers the initial included workspace,
records a request to close, and preserves cancellation or interruption as later events. A retry
cannot quietly replace the starting point, and an interruption cannot become a successful result.

| Situation | Tested behavior |
|---|---|
| Start, edit the folder, resend the same start request | Return the original manifest and time |
| Reuse the request ID with a different task, capture ID, policy or workspace | Conflict; preserve the original record |
| Request close before start or after interruption | Reject the invalid transition |
| Restart while close is pending | Keep the pending history and workspace reservation |
| Two sessions start in one workspace simultaneously | Admit one journal attempt; reject the other |
| Lose an acknowledgement after commit | Recover the original record using the same request ID |
| Restore an old key after its erasure was logged | Continue denying access |

The first slice contains no success, verified-result or stopped-writer state. Every event retains
`unestablished` attribution and false learning eligibility. These are statements of operator
intent and interruption. The next slice must prove the process boundary before a close can mean
that all owned writers have stopped.

## What was implemented

The internal `AttemptJournal` uses the existing authenticated local session and its evidence key.
It reserves an attempt ID and future capture ID, records an optional terminal parent for the same
task/session/workspace, and stores a versioned initial manifest and policy. The manifest contains
names, modes and hashes; file contents are not added to the journal.

Migration 0008 adds an encrypted append-only event table. An initial record and its later events
retain a per-attempt sequence. Request identity, valid transitions, resource limits and workspace
reservation are checked inside the serialized SQLite write transaction. Headers are checked
against their authenticated payload. Missing starts, sequence gaps and corrupt records are
rejected on read. This is not externally anchored protection against someone rolling back the
whole database or removing its suffix.

The existing capture library remains independent. Its manual captures are not yet associated
with this journal's close requests, and a journal reservation is not an operating-system lock.
The public API stays preview 4. There is no new CLI, HTTP endpoint, process launcher, native
harness execution, trusted verification result or learned authority.

## What the fault cases taught us

Restart must preserve uncertainty. A pending close remains pending until an explicit permitted
transition is appended. No timer marks it completed, and no persisted PID grants permission to
kill a process after restart. A parent reference requires an actual terminal journal attempt;
even terminal journal state does not prove its processes stopped.

Quota and erasure are part of recovery. The versioned upper bounds are three attempts per session,
eight events per attempt, 8,000,000 encoded bytes per event and 32,000,000 ciphertext-plus-nonce
bytes across this table. Erased ciphertext still counts; SQLite/WAL overhead is outside that
logical quota. If capacity is exhausted, a final interruption event can be blocked. If an
unfinished attempt's key is erased, its reservation can remain blocked too. The implementation
keeps that uncertainty visible instead of releasing the workspace automatically.

Before real execution, the supervisor must reserve capacity for terminal records and coordinate
erasure, process termination and reservation release. W3.1's active-copy erasure and crash-leftover
cleanup gates also remain open. These are explicit next requirements, not completed operations
claims. Tests use synthetic fixtures and remove their disposable state afterward.

## Evidence and disposition

The complete suite passes **631 tests**, up from 593: 37 new journal cases and one migration
compatibility case. All **eleven engineering checks pass**. The inventory accounts for **273
fields**. Existing schema-7 captures remain readable through migration to version 8, and existing
verification receipts still decrypt. There are 103 modules citing known ADRs; 74 of 77 ADRs have
a citing module. The three unmapped decisions remain EVL-001, EVL-008 and RTG-007.

Initial lint probes found long SQL strings, an unused test import and regex literals needing
explicit raw-string notation. Those were corrected before the combined run. A documentation
patch was rejected because one context line did not exist; no part was applied, and the corrected
patch succeeded. Focused tests and the first full combined run passed. No failing invariant was
waived, and no model calls, actual user payload capture, new paid usage or routing changes occurred.

Nine owning ADRs now describe the scoped implementation and its limits. **Every architectural
status and maturity field remains unchanged.** This adds offline evidence for the journal, not
completion of the process supervisor, task-close attribution, outcome quality or cross-harness
qualification.

Advance to **W3.2b**: freeze a concrete process-owner and writer-containment contract, then test
descendants, cancellation, restart and capture association. If that boundary cannot be proved
for a case, keep attribution unestablished or mark the attempt incomplete. Full W3 also requires
copy/erasure recovery, retained verifier/CLI/timeline binding and a bounded native Claude task.

See the [packet](waves/w3-2-attempt-lifecycle.md), [journey](adrl-implementation-journey.md),
[checks/source evidence](research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[source diff](research/adrl-w3-2a-attempt-journal-2026-09-08.patch),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
