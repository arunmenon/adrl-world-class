# W3.2b: Process ownership and the completion boundary

Packet `W3.2b-process-ownership-v1`, frozen 8 September 2026 before implementation.
Parent: [attempt lifecycle packet](w3-2-attempt-lifecycle.md). Entry: [W3.2a](../adrl-w3-2a-attempt-journal-2026-09-08.md).
Owner: Codex, implementation/self-review; product owner: Arun Menon. Independent security review
is unassigned. Existing authorization covers bounded local engineering with synthetic fixtures.
No model-service calls, new paid usage, infrastructure provisioning or real task payloads.

## Three bounded pieces, with separate closure

**W3.2b1: owned process-group execution and cleanup.** Build a real internal runner for approved
local fixture commands. It owns a fresh process group through a private launcher process and
private pipes. Keep that launcher alive, or unreaped, until the final group signal has been sent;
do not signal after releasing the identity. Only the in-memory handle created by this run grants
cleanup authority. There is no restore/attach/kill API taking an arbitrary persisted PID.

The launcher detects owner-pipe closure and has a bounded watchdog. The child inherits neither
control descriptors nor the owner's environment by default. Pin the executable content before
launch, bound arguments/control frames and runtime/cleanup waits, and discard workload stdout
and stderr in this first slice. A timeout or cancellation must perform cleanup before returning
or propagating cancellation. Record launch/exit/cleanup observations separately from task success.

Process groups do not contain detached descendants or unrelated workspace writers. Therefore
every b1 result remains ineligible for exact-close attribution. Test that limitation explicitly
with a short-lived detached fixture. Group signal delivery and reaping the owned launcher do
not establish a global writer barrier. This piece adds no journal transition, retained capture,
public endpoint or CLI. It may close as tested cleanup mechanics while full W3.2 remains open.

**W3.2b2: admission and containment qualification.** Resolve terminal-record capacity reservation,
coordinated erasure/release, process identity across restart, and the execution boundary actually
needed for all admitted writers. A group-only result cannot pass this gate. Test or explicitly
reject detachment, surviving descendants and ambiguous ownership. Any stronger infrastructure
or expanded scope needs a concrete packet under the roadmap's existing approval rules.

**W3.2b3: durable close/capture association.** Once the previous boundary is evidenced, bind an
admitted attempt, its close request and reserved capture ID to that boundary. Reject captures
that predate it or belong elsewhere. Preserve earlier manual operator captures and journal
history. No new successful close, learned authority or native run follows from b1 alone.

## Limits and trust assumptions

One implementation writer and at most three failed repairs per task. B1 uses only self-authored
synthetic commands under disposable test directories. One active run per runner instance, one
workload launch per run, no retries. Versioned policy upper bounds: 60 seconds of command runtime,
10 seconds for launcher handshake, 5 seconds for launcher reaping, and 8,192 encoded launch bytes.
Use shorter fixture deadlines. A fixed bounded bootstrap/watchdog in the launcher must fail
without running an unreceived command. Platform process creation may itself outlast a timeout;
record this limitation rather than claiming a hard real-time bound.

The initial backend is POSIX and must fail explicitly on unsupported platforms or incompatible
child-reaping configuration. No hostile-code sandbox, provider credential isolation or protection
against an attacker controlling the OS account is claimed. Do not inherit secrets or write raw
argv/environment/output into evidence. The source and executable identities must be reviewable.
Only bounded self-terminating detached fixtures are used, with no arbitrary-PID cleanup.

Owning clauses: OPS-001 process ownership and limits; SAF-007 constrained execution boundary;
SEM-006 descendant scope; MEM-003 result/provenance separation; TRU-001 operator authority.
No existing pin, routing policy, erasure/graduation rule or architectural status is changed.

## Frozen b1 acceptance cases

| Case | Expected observation |
|---|---|
| Bounded command exits 0 or nonzero | Preserve exit code without treating it as verified quality |
| Direct child exits while same-group descendant still runs | Cleanup stops the tested late writer; retain scope limitation |
| Command ignores ordinary termination | Bounded forced group cleanup and launcher reaping |
| Timeout, explicit stop, coroutine cancellation | Cleanup occurs before completion/cancellation propagates |
| Owner process dies | Control-pipe EOF triggers launcher cleanup in the tested fixture |
| Bad executable hash/path, oversized input or invalid environment | Reject before workload launch |
| Failed launcher/protocol | No completion claim; cleanup remains tied to owned handle |
| Repeated or concurrent use | No second active run in one instance; no signaling a released group |
| Detached short-lived writer | Escape limitation observed and exact-close eligibility remains false |
| Parent environment contains a canary | Child sees only explicitly supplied environment plus documented minimal defaults |
| Post-restart persisted process metadata | No API turns it into signal authority |
| Required checks and source/ADR sync | All checks pass; relevant prior text and all maturity fields preserved |

Run the complete engineering suite and record actual failures and exclusions. Publish the
evidence and update the journey after b1; keep b2/b3 and full W3 open. The initial platform probe
on this machine found Python 3.12.7 on Darwin without `os.waitid` or `pidfd_open`; that motivates
an owned launcher rather than relying on a portable non-reaping wait facility.

## B1 disposition, 8 September 2026

W3.2b1 is locally validated: 38 new real synthetic process cases, 669 total passing tests
and eleven passing engineering checks. The deliberate detached writer survives, and all
reports retain group-only scope and false exact-close/learning eligibility. Self-review
corrected a loop-shutdown cancellation risk before the complete check run. Five owning
ADRs retain prior wording and all 77 status/maturity fields remain unchanged.

See the [report](../adrl-w3-2b1-process-ownership-2026-09-08.md),
[evidence](../research/adrl-w3-2b1-process-ownership-2026-09-08.json) and
[source diff](../research/adrl-w3-2b1-process-ownership-2026-09-08.patch).
No journal/capture association or real task capture was added. B2 and B3 remain open.
Before coding B2, freeze the bounded terminal-capacity and erasure/release contract and
its fault cases. Complete writer containment must be separately qualified; B1's group
observations do not grant it. No arbitrary-PID recovery, new infrastructure or paid
execution is implied by this disposition.

## B2a disposition, 8 September 2026

The [terminal-capacity subpacket](w3-2b2a-terminal-capacity.md) is locally validated:
697 passing tests, eleven checks and 279 inventoried fields. New v2 journal starts reserve
one terminal slot and bounded bytes; old v1 records retain their original quota contract.
This closes only capacity reservation. Erasure/process/reservation release, complete
writer containment and B3 capture association remain open. Freeze B2b's failure-ordering
and recovery contract before coding; a pending erased grant is still charged and blocked.

## B2b1 course correction, 8 September 2026

Preparing recovery exposed a key-removal-before-audit resurrection path in a disposable
fault probe. The [key-revocation subpacket](w3-2b2b1-key-revocation.md) is now locally
validated: 724 tests and eleven checks pass. Persistent revocation precedes key mutation
and denies restored-key reads/recreation after the tested failures. This does not signal
processes or release workspace/capacity reservations. Resume B2b2's bounded coordination
contract before code; full B2/B3 and W3 remain open.

## B2b2 disposition, 8 September 2026

The [coordination subpacket](w3-2b2b2-process-coordination.md) is locally validated with
759 passing tests and eleven checks. A durable fence now connects admission, in-memory process
ownership and eventual erasure/expiry/closure monitoring. Terminal records and restart never
release a supervised workspace. No group result qualifies all-writer quiescence. Continue the
[writer-boundary investigation](w3-2b2c-writer-boundary.md), keeping complete containment,
active plaintext/crash recovery and B3 capture association open.

## B2c investigation disposition, 8 September 2026

The [writer-boundary experiment](w3-2b2c-writer-boundary.md) completed six bounded observations
using the existing local Docker engine and synthetic host files. It supports an optional
isolated-container candidate while showing that client death and file mode/path changes are
not writer-stop barriers. Runtime remains unchanged at 759 passing tests with verified hashes;
no permanent fence was released and full B2/B3/W3 remain open. Continue
[durable resource ownership](w3-2b2d-resource-ownership.md), retaining the remaining capture and
plaintext-erasure gates.
