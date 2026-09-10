# W3.2b2d2 next: implement bounded one-shot isolated execution

Prepared 8 September 2026 after the [identity and launch research](../adrl-w3-execution-identity-2026-09-08.md).
The changed experiment passed one identity case and six lifecycle cases; all seven containers
and the one image are absent. The research allowance is closed. The runtime still cannot start
containers. This packet advances the existing W3.2b2d2 slice, not a new completed product wave.

## Implementation objective

Give the internal optional backend one durable opportunity to launch an admitted synthetic
fixture, then seal further launches and either retain a known stopped resource or discard an
ambiguous one. Every result keeps the workspace blocked, exact-close false and learning false.
Use the [proposed execution contract](w3-isolated-execution-contract-v1.md), supplemented by the
observed [comparison contract](w3-execution-identity-v1.md). No public start API or real harness
payload; native observation and shared product contracts retain their existing scope.

Owners: OPS-001; MEM-001/002/003/005/010, SAF-007 and TRU-001. One writer; no agents, paid calls,
installs, image pulls, daemon changes, live routing, policy promotion or commits. Preserve dirty
source and verify backups. Read both AGENTS.md and current state before changing runtime.

## Concrete decisions to carry into code

- Preserve d1 stopped records, raw configuration HMAC and non-force/no-start behavior. Add a
  separate execution history/coordinator, not a reinterpretation of old bound events.
- First admission authenticates the original bound event and exact never-started inspection.
  Create a versioned HMAC of the execution projection and engine capability/fixture profile,
  linked to the original event/MAC. Subsequent recovery compares current projections to that
  authenticated reference. Do not persist raw commands, paths, engine addresses or inspections
  in the product ledger. The research SHA comparator alone grants no runtime ownership.
- Only the observed unsupported OomKillDisable false/null mapping is eligible for the pinned
  profile. Retain every other stable configuration field and original Id/Created. Missing,
  malformed or changed evidence refuses admission/recovery. State and StartedAt need separate
  lifecycle checks; RestartCount zero is not evidence of no manual restart.
- Use a private permanent marker directory at FileKeyStore.root / launch-denials-v1, with an
  independently named .launch-denial.lock. Proposed file name: authenticated resource operation
  key plus .denied; fixed contents adrl-launch-denial-v1 followed by a newline. Versioned maximum
  64 bytes/marker, 32 markers/histories, eight execution events/resource, 4096 bytes/event.
  Inventory these linkable metadata fields before closure. They survive content-key erasure.
- Under a nonblocking local marker lock, validate private ownership/mode, refuse symlink/unsafe
  roots, enforce capacity and exclusive marker creation. Any existing/partial marker denies
  launch. File and directory fsync precede dispatch. Release this lock before ledger waits;
  never hold a keystore lock while waiting for the ledger. Markers are never removed and alone
  never grant cleanup authority. Root recreation/whole-storage rollback remains unqualified.
- Prevalidate identity/key/attempt/grant; create durable marker; append a unique authenticated
  launch claim while rechecking admission; only that original caller may send start once. Failed
  marker/claim acknowledgement blocks retry. No recovery caller may resume dispatch from a
  claim, recreated wrapper object, saved PID, name or label.
- Require an explicitly admitted self-authored fixture manifest with pinned image, executable/
  archive SHA, exact argv, supported engine profile and independent lifetime. Do not make the
  seven-second fixture timer an arbitrary-command timeout promise.
- Serialize claim/ack/seal/stop/discard transitions in a separately authenticated append-only
  history. Freeze the exact event fields, legal transitions, quota reservation and fault matrix
  before editing code. API acknowledgement and durable event acknowledgement are different.
- Track and drain the sole dispatch worker, including repeated cancellation. Known launch plus
  durable seal plus observed matching StartedAt/exit may retain the layer. Ambiguous launch,
  owner loss or erasure uses authenticated seal/discard or visible uncertainty. A stop-before-
  start response cannot justify retaining output. No restart/exec operation is offered.
- Host-authenticated cleanup may survive content-key erasure. Define and test emergency cleanup
  when audit appends fail: never invent a durable event, never retry uncertain launch, never
  let failed bookkeeping itself prevent independently authorized owned-resource cleanup.

## Required acceptance and limits

Offline tests must cover competing callers, marker-only/claim-only faults, lost start/ack/seal/
discard replies, ledger-only valid-prefix rollback with retained marker, corrupt/missing history,
host-key change, revoked/expired/closed attempt, invalid grant, key erasure while active, daemon
unavailability, unexpected engine/configuration/StartedAt drift, repeated cancellation, owner
death, logical capacity and storage failure. Assert at most one dispatched start and permanent
fencing after every outcome. Mark complete-storage rollback and hostile host/daemon as limits.

If code starts a real engine fixture, freeze a fresh finite acceptance packet after the offline
contract/tests are ready. Reuse only the verified local synthetic archive/profile, account for
every issued create/start/import, and confirm cleanup. Do not rerun the closed research batch.
At most three repair cycles; stop unchanged failure retries and prepare a specific reassessment.

Run the module map and all eleven runtime checks for implementation changes, with recorded
stable source hashes and data inventory. Synchronize owning ADRs, index, four bucket overviews,
changelog, journey and state, preserving prior text and all 77 status/maturity fields. No runtime
component alone closes W3.2 or W3, and no independent review has yet occurred.

## Following work

Active-copy leases and erasure; safe output extraction; exact stop/capture association; verifier
and operator timeline/CLI; explicit image/network/credentials/retention profile for a real
Claude Code demonstration. OpenCode follows shared-contract qualification. Trustworthy outcome
data precedes improvement proposals, independent comparison and any approved policy adoption.

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
