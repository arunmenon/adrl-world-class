# Proposed isolated execution contract v1

Prepared 8 September 2026 from W3.2b2d2 source review and two failed bounded research runs.
This freezes the intended lifecycle and failure semantics. It is **not implemented or qualified**.
The [identity compatibility gate](w3-2b2d2-identity-compatibility.md) must pass before a runtime
start operation is introduced. Parent: [launch admission](w3-2b2d2-launch-admission.md).

## Product boundary

One internal optional backend acts on an existing bound session, readable v2 started attempt,
intact terminal grant and authenticated stopped-resource binding. It does not infer a task from
a harness's done message. Shared identity, attempt, capture and evidence contracts remain the
product surface across harnesses; native observation retains its existing scope.

The first active implementation accepts only an explicitly admitted self-authored fixture
manifest: immutable image ID, archive/executable hash, exact command/arguments, engine/version/
capability profile, seccomp pin and bounded independent fixture lifetime. The existing probe's
seven-second self-termination is specific to that reviewed program, not a timeout guarantee for
an arbitrary command. Do not expose general model/harness execution through a fixture parameter.
No networking, host repository/credential/socket mounts, image pull or public start endpoint.

Owners: OPS-001, MEM-001/002/003/005/010, SAF-007 and TRU-001. Independent evaluation/security
review remains unassigned. Privacy pins, routing, erasure and graduation policies remain intact.

## Identity has a preparation stage and an execution stage

Preserve the original stopped-resource event and full raw configuration digest unchanged.
Before launch, require that exact original binding and never-started state. Bind a separate
versioned execution-identity projection to the original event/MAC, engine and fixture manifest.
This projection must retain all original configuration fields except explicitly reviewed,
capability-specific representational changes. It must never become a vague subset of convenient
fields or a generic null/default normalization.

The concrete unresolved case is HostConfig.OomKillDisable: the captured second run changed
`false` to `null` across start, while every explicitly requested control stayed unchanged.
Moby 27.3.1 supplies a false default during adaptation and clears the field when the kernel
does not support the control. The selected engine reports that capability false. The proposed
exception is limited to this field, this engine/API/Linux/cgroup-v2 profile and the recorded
unsupported capability. `true`, missing/malformed evidence, another engine/profile, changed
memory/swap/CPU/process limits, capabilities, seccomp, mounts, network, image or command must
still fail. Offline and fresh bounded engine acceptance must establish the exact rule before use.

The failed empty-PortBindings hypothesis is not evidence that another exception is needed.
Do not carry it into runtime merely because it appeared in the research repair. Preserve raw
before/after evidence and the projection version so a reviewer can see what was normalized.

## Proposed state and side-effect order

New execution records must be separate from d1's stopped-resource history. Do not reinterpret
an old bound/removed event as evidence of an active lifecycle. A migration may add append-only
tables; old ciphertext, grants, fences, v1 records and APIs remain readable with their old scope.

| Durable event or condition | Allowed next action | What it does not prove |
|---|---|---|
| Exact stopped binding; no execution claim | Validate current attempt/key/grant and admitted fixture | That launch is authorized after a later revocation |
| Durable one-shot launch claim | The original claim owner may issue one start request | That the request reached the daemon or work began |
| Start acknowledged | Record exact response/state and first StartedAt | Task success or a stable output boundary |
| Admission sealed | Deny all later launch/exec/restart claims for this attempt | That an already-issued request is cancelled |
| Known launch, sealed admission, observed exit | Retain the layer only under the complete stopping contract | Exact-close capture, release, verification or learning |
| Ambiguous launch or failed ownership observation | Seal, then take the owned abort/discard path if identity permits | An acceptable retained task output |
| Discard issued | Remove only the original authenticated exact resource | Confirmed removal or physical erasure |
| Exact bound ID confirmed absent | Record discarded/removed; keep workspace blocked | Task completion or permission to reuse the workspace |

The first start must receive the expected Engine API response and bind its observed launch
time. An already-running response is not evidence of a fresh authorized launch. No retry,
restart, recreation, query-by-name adoption or PID recovery follows from a lost response.

Admission sealing and daemon dispatch are not one transaction. A sealed flag alone cannot
prevent a request already released by another thread/process from reaching the daemon. The
owner must track and drain its dispatch worker. Recovery without trustworthy completion of
that request uses abort/discard, not an observed-created/exited state as permission to capture.

## Durable one-shot denial and concurrency

Append a unique launch claim under serialized ledger admission. Bound it to the original
resource, policy, identity projection and attempt. Reject a competing caller, changed retry,
closed attempt, erased/expired identity or corrupt/missing grant before dispatch.

A ledger hash chain does not detect rollback to a valid earlier prefix. The proposed first
implementation also publishes a permanent private launch-denial marker before any start can
be sent, following the existing revocation-marker ordering pattern. Its keyed filename names
the resource operation; its fixed versioned contents contain no task payload. Exclusive create,
file and directory durability precede dispatch. Presence, even partial, denies another launch.
The marker never grants cleanup authority by itself and is never removed on success or failure.

Only the original caller that created the marker and committed the claim may dispatch once.
Marker-only or claim-only recovery remains uncertain and cannot launch. This deliberately
allows a blocked prelaunch failure. Restoring only old ledger rows while retaining newer markers
must not recreate launch authority. Restoring both marker and database/key state, malicious
host administration and lost/replaced storage roots remain outside this qualification.

Freeze and inventory the concrete marker root, lock ordering and logical capacity before code.
Use at most the existing 32 resource histories, at most eight bounded execution events per
resource, at most 4,096 bytes per event, and a versioned marker-size limit. These are logical
ceilings, not preallocated disk or a hard scheduling guarantee. No process-global mutable PID
table or cleanup shortcut may substitute for durable ownership.

## Normal stopping and abort recovery are distinct

**Known launch:** first seal future admission; finish/drain the sole dispatch; request stopping
when needed and observe the exact resource exit. Verify execution identity, the bound StartedAt,
no unexpected restart/paused/dead state and the declared private-writer boundary. A zero restart
count alone is insufficient; the planned manual-restart negative control is still uncompleted.
Any uncertainty moves to abort or a visible block. Retention does not yet grant exact-close
attribution: B3 must bind safe capture to this evidence under its own acceptance cases.

**Ambiguous launch, owner death or revocation:** seal further admission and authenticate the
original resource independently of session content keys. The proposed destructive abort path
may force-remove that exact disposable fixture, then confirm absence. Do not preserve its
output as if launch/close were known. An identity mismatch, changed engine or unavailable daemon
prevents a successful cleanup claim; retain a blocked/uncertain record and escalate only the
dependent recovery action. Never kill or remove a candidate discovered by name, label or PID.

Moby's source marks removal in progress, checks that condition during startup and marks the
object dead during removal. That supports the proposed discard barrier by source inference;
it is not a proof of every ordering, and the planned delayed-start/discard observations have
not passed. Require these acceptance cases before using forced discard in runtime.

If a seal/terminal audit append fails after an original launch claim exists, do not let the
failed audit prevent an independently authorized emergency stop/discard attempt. Preserve the
audit failure and uncertain disposition; never invent a durable event. Freeze and test the exact
ordering, worker draining and recovery responsibilities before introducing this exception path.

## Independent lifetime and copy custody

The active owner observes cancellation, expiry, revocation, journal closure and daemon/identity
failure from outside the caller's event loop. Repeated cancellation must drain protected work.
Host-client loss cannot withdraw a start already accepted by the daemon. The first allowed
fixture therefore has its own bounded lifetime inside the container; its observed termination
is not a general watchdog for future harnesses or an erasure-completion receipt.

No real task payload can enter this backend until a suitable independent lifetime/stop mechanism,
active/plaintext lease erasure, process-death leftovers and container/output retention are
qualified. No privacy pin is released. Every outcome keeps the permanent workspace fence,
exact-close eligibility false and learning eligibility false. Erasure-compatible host cleanup
metadata remains linkable and does not settle DQ6 or claim physical block/backup deletion.

## Fault table to implement and test

| Fault or ordering | Required disposition |
|---|---|
| Wrong session/workspace, missing grant, closed/erased/expired attempt | No marker/claim/dispatch authority |
| Two callers compete | At most one marker owner and one dispatched start |
| Crash after marker, before claim | Block; no retry/adoption; exact owned cleanup remains separately assessed |
| Claim committed, response/ack append lost | No second start; sealed abort or visible uncertain recovery |
| Stop arrives before a delayed start | Never infer closure merely from a not-running response |
| Start worker stalls or caller dies | Independent fixture lifetime plus recorded recovery obligation |
| Another start after observed exit | Deny through marker/claim/seal; treat outside-adapter interference as out of scope or mismatch |
| Expected version-specific OOM field transformation | Accept only after the identity gate proves the narrow rule |
| Any unexpected configuration/engine/StartedAt change | Refuse retained-output qualification and arbitrary cleanup |
| Revocation while active; audit store unavailable | Preserve key denial; attempt only authenticated stop/discard; do not require a content key |
| Lost discard response | Reconcile only absence of the previously bound exact ID |
| Partial/truncated/corrupt history, marker, or host-key change | No new dispatch; no invented terminal result |
| Ledger-only prefix rollback with newer marker present | No replayed start |
| Complete storage/marker/key rollback | Explicitly unqualified; no false detection claim |

The six engine observations in the [experiment packet](w3-2b2d2-launch-experiment.md) remain
uncompleted after two failed runs. The next packet resolves the observed identity failure
first, then freezes a changed, finite follow-up experiment. Do not silently restart the same
failed batch or describe source review as passing runtime acceptance.

## Sources and qualification

Pinned primary implementation sources: Moby 27.3.1
[start](https://raw.githubusercontent.com/moby/moby/v27.3.1/daemon/start.go),
[removal](https://raw.githubusercontent.com/moby/moby/v27.3.1/daemon/delete.go),
[kill](https://raw.githubusercontent.com/moby/moby/v27.3.1/daemon/kill.go), and
[Unix configuration handling](https://raw.githubusercontent.com/moby/moby/v27.3.1/daemon/daemon_unix.go).
Source inspection explains proposed ordering and the observed normalization; it does not
replace adapter tests, independent security review or real-harness qualification. No grade
or architecture-status change follows. Full d/B2/B3 and W3 remain open.

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
