# W3.1: Keep the output we mean to inspect

8 September 2026. Engineering slice: locally validated. Full W3 remains open.

ADRL can now retain an encrypted copy of a workspace through an internal operator API. If the
working folder changes afterward, that copy still contains the original output. This removes
one source of confusion before we connect the retained copy to verification.

| Situation | What happens now | What it proves |
|---|---|---|
| Capture output A, then edit the folder into B | The retained copy still restores A with its original fingerprint | Later edits cannot silently replace this captured input |
| Change files while capture scans them | Observed inconsistencies reject the capture | These tested races do not create a successful capture |
| Retry the same capture | Identical inputs return the original record; changed inputs conflict | Retries cannot overwrite history |
| Lose the acknowledgement after commit | The stable capture ID finds the committed record | Recovery need not create a duplicate |
| Erase the session key | New reads and captures are denied | The archive follows the session's erasure boundary |
| Corrupt or lose retained content | Reading fails; there is no fallback to today's folder | An unavailable capture cannot quietly become a different output |

This is a capture made when the operator asks for it. It does not yet prove what a task left at
its earlier completion time. Repeated scans and a matching fingerprint cannot establish that
all writers had stopped. The trusted close supervisor remains W3.2, and verification/CLI/timeline
binding plus a real Claude task demonstration remain W3.3.

## What was built

The implementation stores each complete capture as one encrypted database record. It reuses the
existing bound session key and creates no new key, route or learning label. Task attempts have
separate IDs from sessions; two tasks can share a session without sharing capture identity. A
parent attempt reference must name an existing capture in the same session. This is an operator
declaration, not the trusted task lifecycle that the next slice will implement.

Atomic database commit avoids a separate partially written payload file. The record includes
the request, policy, source reference, paths, permissions and file bytes inside encryption. The
plaintext database fields contain keyed identities and an append-order skeleton. Schema version
7 adds one table; a migration test confirms an existing version-6 receipt still decrypts afterward.
The public API remains preview 4, with no new HTTP operation or CLI command.

The input scanner opens files relative to directory descriptors and rejects symlinks, special
files, hard links, unsafe paths, reserved verifier paths and observed drift. It enforces count
and byte bounds. Two scans must agree. These checks support trusted local fixtures; they do not
qualify arbitrary hostile repositories or prove an atomic task-close boundary.

## Guardrails that remain visible

The versioned policy caps a capture at 10,000 entries and 100,000,000 source bytes, with at most
three captures per session and 500,000,000 ciphertext-plus-nonce bytes across the capture table.
These can be lowered. Quotas are checked in the write transaction and count erased ciphertext
too. SQLite/WAL overhead is outside that logical byte count, and encoding/scanning requires more
memory than the raw content size. No bulk collector is enabled.

An operator may materialize a private temporary copy. It is removed on ordinary exit, exceptions
and Python cancellation. Killing the process may leave it behind. Key erasure cannot withdraw
an object already returned in memory or a plaintext copy already leased to a caller. New access
is denied; the active copy is cleaned when its context exits. Active-copy coordination, startup
leftover cleanup and a reviewed retention/recovery operation remain prerequisites for real task
capture. Physical storage remnants, backups and operator-made copies have no new erasure promise.

All runs in this slice used synthetic fixtures, and the capture fixture removes its disposable
state afterward. No model-service calls, actual user payload capture, new paid usage, provider
configuration change or live routing deployment occurred. The archive trusts a previously
authenticated local principal under the existing same-OS-user boundary; it is not a remote
verifier credential service or an independent security review.

## Evidence and maturity

The full suite passes **593 tests**, up from the prior 556. Thirty-six new capture cases and one
additional migration test cover the new mechanism. All **eleven engineering checks pass**,
including typing, ledger discipline, configuration, inventory, API export and ADR coverage.
The data inventory accounts for **263 fields**. There are 102 implementation modules citing
known ADRs; 74 of 77 ADRs have a citing module. The three intentionally unmapped decisions remain
EVL-001, EVL-008 and RTG-007. Mapping still says nothing about a whole decision's maturity.

Initial lint probes found synchronous path calls inside an async function and a long test SQL
literal. Both were corrected before the combined check run. The focused behavioral tests and
the first full combined run passed. No failed invariant was waived.

This supplies scoped offline evidence for retained-capture mechanics. **No ADR maturity grade
or architectural status is promoted.** The nine owning records preserve their prior wording
and name the implemented application and limits. The next meaningful maturity step needs the
completed lifecycle and actual outcome evidence, not a larger test count alone.

See the [wave packet](waves/w3-task-capture.md), [running journey](adrl-implementation-journey.md),
[check/source evidence](research/adrl-w3-1-operator-captures-2026-09-08.json),
[source diff](research/adrl-w3-1-operator-captures-2026-09-08.patch),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_capture.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
