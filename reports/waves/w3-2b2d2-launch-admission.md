# W3.2b2d2: Define launch and active recovery before enabling execution

Prepared 8 September 2026 after [stopped ownership](w3-2b2d1-stopped-resource-ownership.md).
This is the next contract-design packet, not evidence that launch is implemented. Codex is
the implementer and technical self-reviewer. Independent review remains unassigned.

## Intended result

Move from a known stopped resource to a narrowly bounded synthetic execution whose launch,
stopping and recovery are explicit. Preserve every existing group/resource fence, v1 history,
erasure denial and ineligibility for exact task closure. Do not repurpose a d1 event to claim
that a task ran. Identify the owning ADRs and freeze any new versioned record/policy before code.

First inspect the current owner, append-only journal, revocation path and prior writer-boundary
observations. Produce a concrete transition/fault table and choose a reviewable slice. The
contract must resolve the following before a start operation is introduced:

1. **Launch authority:** require an authenticated exact bound ID, matching engine/configuration,
   readable started attempt and grant. Append a unique launch claim before issuing one start.
   A lost acknowledgement must not authorize a second start, recreation, exec or adoption.
2. **While active:** define who observes expiry, cancellation, revocation, closure, owner/client
   death and daemon loss. A client disappearing does not prove the container stopped. Specify
   a bounded fixture lifetime and an independent stop/recovery responsibility; no indefinite job.
3. **Stop authority:** use the original durable binding, not a name/label/PID guess. Distinguish
   a requested stop, observed exit, and confirmed complete writer termination. Do not grant
   arbitrary resource deletion or weaken configuration checks merely because state changed.
4. **No new writers:** define when launch/exec/restart admission becomes permanently closed for
   the attempt. Observing one process exit is insufficient if another code path can start work.
   State the boundary against trusted daemon/host administration and the limits of that trust.
5. **Partial failures:** cover each boundary before/after claim, start, inspection, stop and
   append; concurrent callers, repeated cancellation, owner death, key revocation, corrupted
   history, mismatched engine/configuration and valid-prefix rollback limitations.
6. **After stopping:** retain the workspace fence. No release, extraction, capture, verifier
   receipt, outcome label or learning eligibility follows in this packet. Active/plaintext
   cleanup and durable output association remain distinct gates.

If the active lifecycle cannot fit a safe bounded slice, finish its reviewable contract first
and keep start unavailable. An independent plaintext lease/crash-copy slice may proceed under
its own frozen contract. Do not hide an unbounded recovery obligation in an eventual TODO.

## Execution guardrails

Use only the already-present local engine after rechecking its identity/version. No pull,
install, network, host repository/credential/socket mounts, real harness, model call, API spend,
daemon setting change, generic kill/prune or deployment. Existing runtime invariants and native
observation scope remain unchanged. Use self-authored synthetic fixtures and the pinned explicit
seccomp profile. Prior d1 fixture resources/image were removed; do not reuse its exhausted run
accounting. Freeze a fresh finite resource/time allowance before any new daemon mutation.

At most three repair cycles and three reviewable slices per heartbeat, one writer. Preserve
dirty-source backups. After code, run the complete combined suite, check source hashes, account
for every fixture, and synchronize ADRs, index, bucket overviews, changelog, journey and state.
No architectural status/maturity promotion or independent-review claim. Real-harness image,
network, credential and retention dispositions retain their roadmap gates.

## Exit criteria

The first deliverable is a frozen versioned lifecycle/fault contract with exact acceptance cases,
resource allowance and exclusions. Any implementation must then satisfy those cases and all
eleven engineering checks. Uncertainty remains visible and blocked. Report engineering evidence
separately from full-B2/B3/W3 qualification; the full wave stays open.

## 2026-09-08 disposition: design prepared, active identity gate open

The [proposed v1 lifecycle](w3-isolated-execution-contract-v1.md) now defines claim/seal/known-stop/
ambiguous-abort ordering, one-shot denial, metadata, independent fixture lifetime and fault cases.
It is not implemented or qualified. The [bounded experiment](w3-2b2d2-launch-experiment.md)
failed twice in its first case at configuration identity comparison; zero of six cases is accepted.
The two-run allowance is closed. Both exact fixture containers and the one imported image were
removed and confirmed absent. No further daemon mutation follows from that closed packet.

The captured second before/after pair differs only in unsupported HostConfig.OomKillDisable,
false to null. Pinned source explains the change. The first empty-port-map hypothesis was
insufficient and is not a runtime exception. Continue the [identity compatibility reassessment](w3-2b2d2-identity-compatibility.md)
before a changed, freshly bounded engine run or runtime start implementation. Runtime source
is unchanged at its verified 812-test/306-input baseline. See the [report](../adrl-w3-2b2d2-launch-contract-2026-09-08.md) and
[evidence](../research/adrl-w3-2b2d2-launch-contract-2026-09-08.json). Parent d/B2/B3/W3, capture and real-harness gates remain open.

## Current disposition after changed experiment, 2026-09-08

The [new evidence](../research/adrl-w3-execution-identity-2026-09-08.json) now records 101 passing offline
research cases and seven accepted engine observations: one identity case and all six lifecycle
cases. The narrow unsupported OOM rule passed; no other normalization was required. Manual
restart changed StartedAt while RestartCount stayed zero. All seven containers and the one
image are absent. The old two failed runs remain preserved and their allowance remains closed.
The new seven-container/two-stage allowance is also closed after successful completion.

Earlier statements in this packet about uncompleted research describe its preparation state.
This disposition advances research readiness only: runtime launch/seal/recovery and the permanent
marker are still unimplemented. Continue the [runtime packet](w3-isolated-launch-runtime.md).
No public API, runtime source, status/maturity, exact-close or learning eligibility changes.

## Current prototype disposition, 2026-09-08

The [runtime prototype](../adrl-w3-isolated-launch-2026-09-08.md) now implements the scoped one-shot lifecycle,
with 861 offline tests/eight engine skips and all eleven checks passing. Schema 12 and the
370-field inventory preserve previous records/fences and false outcome eligibility. Two bounded
engine runs each had 3 passes/1 failure; the latest stopped-create reply loss remains undiagnosed.
All eight fixtures and the image are absent, including one recorded operator cleanup exception.
No automatic name adoption, independent review or full d2/B2/B3/W3 qualification follows.
Earlier statements of unimplemented behavior describe preparation state; current scope and
failures are in the [evidence](../research/adrl-w3-isolated-launch-2026-09-08.json).
The engine allowance is closed. Continue the [diagnosis packet](w3-launch-create-receipt-diagnosis.md).

## Later disposition: receipt correction and bounded d2 validation, 2026-09-08

The [current report](../adrl-w3-transport-receipts-2026-09-08.md) records execution v2, separate preparation/active I/O,
26 new offline faults and a fresh passing engine packet. Final combined results: 895 passed,
zero skipped, all eleven checks, 316 stable source inputs. Thirteen original IDs and exact
absence confirmations; the image is removed. No cleanup exception in the fresh packet.
Historical create cause remains unknown; previous observations and allowances stay preserved.
This closes the bounded d2 pinned synthetic launch/recovery slice, not full B2/B3/W3 or any
ADR grade. Continue [active-copy custody](w3-active-copy-custody.md); no new Docker allowance.
