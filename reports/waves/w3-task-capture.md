# W3: Preserve the output we mean to verify

**Execution update, 2026-09-08:** [W3.1 is locally validated](../adrl-w3-1-operator-captures-2026-09-08.md).
It implements internal operator-time capture on synthetic fixtures; 593 tests and eleven checks
pass. Full W3 remains open. W3.2 is next, followed by active-copy/crash recovery and the W3.3
verification/CLI/native-task demonstration gates. The original scope and acceptance cases below
are preserved; an internal component does not close those later gates.

Packet `W3-task-capture-v1`, frozen 7 September 2026 before W3 implementation.
Parent: [roadmap W3](../adrl-implementation-roadmap-2026-09-07.md). Dependency:
[W0 local engineering baseline](w0-baseline.md). Implementation owner: Codex. Product owner:
Arun Menon. Technical self-review is not independent outcome/security review.

## What we are trying to make true

Suppose Claude produces output A, then someone edits the same folder into B. A later check must
still inspect A when its receipt says A. Today the verifier makes a temporary snapshot at the
time the operator invokes it; that is useful but cannot prove what the earlier task left behind.

The user authorized this wave under the roadmap. No additional approval is needed for these
offline implementation slices. Existing status/maturity, raw-data handling, verifier authority,
learning exclusions and live exposure restrictions remain in force.

## Capture and trust boundary fixed before coding

1. A task attempt is distinct from its bound session. Give it an opaque attempt ID and optional
   parent attempt; do not invent a route ID for observation-only work.
2. The first slice supports **explicit local operator capture** of a declared workspace. Record
   this as `operator_capture`, with the capture-time source identity. It must never advertise
   exact task-close attribution. A harness's completion report remains only an observation.
3. Exact close requires a subsequent trusted local supervisor contract: tracked writers are
   quiesced, a close request belongs to that attempt, and boundary/drift failures become
   incomplete or indeterminate. A timestamp, repeated digest or operator assertion alone
   cannot upgrade the manual capture into proof of exact close. Arbitrary same-user processes
   and hostile repositories are outside the initial boundary.
4. Retain a bounded encrypted snapshot using the existing bound session's erasure lifecycle.
   Snapshot material must not become plaintext ledger fields or an untracked permanent copy.
   Rebinding, duplicates, interrupted writes and erasure must not resurrect retained content.
5. Execute reviewed verifier plans against the retained copy; bind the receipt to its attempt,
   capture identity, plan/artifact/executable versions and actual snapshot. Checks may report
   pass, fail or indeterminate; a failed setup is not a failed code assertion.
6. Preserve existing receipts and their interpretation. Retained-capture results are initially
   review-only and ineligible for learned authority. No new public contract without an explicit
   compatible extension or preview revision plus fixture/export checks.

These are scoped applications of MEM-001/002/003/005/010, SEM-002/003/006/007, SAF-007, TRU-001
and EVL-008. Any contradiction requiring a decision change is recorded before dependent code.

## Bounded slices

| Slice | Deliverable | Closure limit |
|---|---|---|
| W3.1 | Durable encrypted operator capture, immutable identity, materialization, erasure and drift rejection | No exact-close claim, automatic capture, model run or public API promise |
| W3.2 | Task-attempt lifecycle and trusted close supervisor; append-only transitions and recovery | Failed quiescence stays incomplete; no fabricated closure |
| W3.3 | Verifier binding, timeline/CLI surface, compatibility and real Claude observation demonstration | Wave closes only after actual lifecycle evidence and register synchronization |

Use existing file/byte defaults as upper bounds: 10,000 files and 100 MiB per capture. The first
manual-capture test population is synthetic local fixtures; retain no more than three captures
per fixture run and remove the disposable test state afterward. Before bulk or native task
capture, add and test an aggregate retention limit, size accounting and cleanup/recovery policy.
No actual user payload is captured merely by running the unit tests. No paid API calls, installs,
network destinations or new infrastructure. One writer, at most three failed repair attempts
per task. Individual verifier checks retain their explicit timeout of at most 600 seconds.

Temporary plaintext exists only for materialization/execution and must be cleaned on normal
completion, exceptions and cancellation. Crash leftovers need startup reconciliation before
their path is enabled for real task data. Logical erasure and cleanup must state what filesystem
or backup guarantees they do not provide; do not quietly declare physical secure deletion.

## Acceptance cases frozen before implementation

| Case | Expected result | Required slice |
|---|---|---|
| Retain A, change workspace to B | Materialized/verified output remains A; receipt names A | W3.1 / W3.3 |
| Edit while copying or missing file | Reject or indeterminate capture; no success attribution | W3.1 |
| Symlink, traversal, special file, oversized input | Reject before treating it as a valid retained snapshot | W3.1 |
| Two task attempts in one session | Distinct capture/lifecycle identities and receipts | W3.1 / W3.2 |
| Duplicate capture/close | Idempotent same request, explicit conflict for changed content | W3.1 / W3.2 |
| Wrong session or erased session | Deny access/capture; no new key or recovered plaintext | W3.1 |
| Restart after interrupted capture | No partial object advertised as complete; recover or mark incomplete | W3.1 / W3.2 |
| Corrupted or missing retained content | Integrity failure; never fall back to the current workspace | W3.1 / W3.3 |
| Cancel verification or disconnect at close | Append incomplete/cancelled state, preserve prior events | W3.2 / W3.3 |
| Out-of-order/harness-authored closure or success | Cannot acquire trusted terminal/verification authority | W3.2 |
| Quiescence unavailable | Keep `operator_capture` or incomplete; no exact-close label | W3.2 |
| Erase retained output and retry old capture/read | Payload unavailable; no resurrection; remaining skeleton explicit | All |
| Native Claude observation task | Same lifecycle works with recorded harness/build/task and bounded usage | W3.3 |

These tests establish mechanics, not verifier precision or general coding quality. Fresh
independent cases belong to W4. All six required checks, inventory, API compatibility and ADR
mapping run before an implementation slice closes. Update exact owning clauses, the index,
bucket summaries, changelog, journey and source evidence. Target: scoped D2 for the tested
behavior; actual grades remain unchanged unless separately dispositioned under the register.

## Stop and next action

Wrong-output attribution, erased-content recovery or closure authority from an untrusted hook
stops the affected feature. Keep explicitly scoped manual verification available while repairing
it, without relaxing pins or evidence eligibility. After the attempt limit, publish the failed
case and next decision instead of repeating indefinitely.

Next: inspect existing session-key storage and snapshot code, choose the smallest compatible
encrypted capture representation, and implement W3.1 against these frozen cases. Full W3 stays
open until W3.2/W3.3 and the real demonstration are evidenced.
