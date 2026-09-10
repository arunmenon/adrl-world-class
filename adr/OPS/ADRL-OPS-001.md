# ADRL-OPS-001: Multi-worker consistency and the single-process constraint

| Field | Value |
|---|---|
| Bucket | OPS; Platform, Runtime, Operations |
| Status | Proposed 2026-09-03 (first capture; referenced by MEM-006, CAS-006, SEM-002 since 2026-08-27) |
| Maturity | D1 Code; adrl-core keeps sticky state and pins behind a `StateProvider` port with a SQLite adapter and declares the remaining process-local state (pending escalations, verifier consumption, parent map priming) in `docs/known-gaps.md`; no multi-process deployment has been attempted |
| Review verdict | PROPOSED (new) |
| Tenets | 6, 7, 8 |
| Related decisions | MEM-001, MEM-006, SAF-002, SEM-002, SEM-006, CAS-005, CAS-006, OPS-004 |
| Open questions | Q7 |

## Decision

ADRL runs as one process per host until every piece of routing state that must survive a decision is behind a port with a provider that tolerates concurrent processes. The single-process constraint is declared, not accidental: (1) the SQLite provider's contract is single writer, WAL, `busy_timeout`, `BEGIN IMMEDIATE`, same host, enforced by one writer thread per process and checked at startup (MEM-006); (2) every state item is classified in a versioned inventory as `port-backed` or `process-local`, and a `process-local` item names the behaviour on restart (for example `state_loss=true` per CAS-006); (3) a second worker on the same ledger is refused at startup by a lock file naming the owning process, until the inventory has no `process-local` item that affects a gate or a pin; (4) moving to multiple workers is a new version of this decision with the provider named (a server-backed store or a per-lineage sharding rule), never a configuration change.

## W0 execution baseline, 2026-09-07

W0 checked the current deployment scope and retains one implementation writer. The runtime still lacks demonstrated multi-process qualification, an enforced process-owner lock and the full state inventory required by this decision. The local check runner and hourly task continuation are development operations, not a multi-worker runtime implementation. No follow-up or maturity field is marked complete.

See the [W0 packet](../../reports/waves/w0-baseline.md), [journey](../../reports/adrl-implementation-journey.md),
[check/source evidence](../../reports/research/adrl-w0-baseline-2026-09-07.json),
[maturity inventory](../../reports/research/adrl-maturity-baseline-2026-09-07.json) and
[engineering runner](/Users/arunmenon/projects/adrl-core/tools/check_all.py).
All 556 implementation tests and eleven engineering checks pass for the recorded build. This is
scoped local evidence; prior decision wording, status and maturity remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

W3.2a transactionally permits one active journal attempt per canonical workspace across sessions on one ledger; a concurrent-start test admits exactly one. This is a data reservation, not an operating-system lock, a process supervisor or multi-worker runtime qualification. A pending attempt remains reserved after reopen. Cancellation/incomplete states do not prove writers stopped, and erasure/quota failures can preserve a blocked reservation. Real writer ownership, terminal-capacity reservation, coordinated release and process recovery remain W3.2b and later operations gates.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b1 owned process groups, 2026-09-08

W3.2b1 adds an internal single-active-run process owner and a private launcher for bounded synthetic commands. The launcher stays alive, or unreaped, until the final owned group signal; no PID restore/attach/signal API exists. Timeout, cancellation, event-loop shutdown, owner-pipe EOF and watchdog cleanup are tested. Failed signal or unconfirmed reap blocks instance reuse. This process-local primitive does not implement the runtime startup lock, full state inventory or multi-worker qualification required above. Journal terminal capacity, erasure/release coordination and restart admission remain open.

See the [plain-language report](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b1-process-ownership-2026-09-08.json),
[runner](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_owner.py),
[launcher](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_anchor.py),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_process_owner.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/process-ownership.md).
All 669 tests and eleven checks pass on the recorded Darwin build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved. Full W3
and exact task-close attribution remain open.

## W3.2b2a reserved terminal capacity, 2026-09-08

W3.2b2a calculates stored bytes plus all pending terminal grants inside the serialized ledger transaction. Distinct-workspace concurrent admission cannot overspend a scarce quota, and a caller offering a larger budget cannot consume a smaller active admission commitment. Terminal appends use the original bounded grant even if a later caller limit is lower. Grants survive restart and retain erased pending commitments. These local transactional tests do not qualify mixed old/new runtime writers, multiple runtime processes, process locks or the full state inventory. Process ownership, erasure/release coordination and complete writer containment remain separate gates.

See the [plain-language report](../../reports/adrl-w3-2b2a-terminal-capacity-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b2a-terminal-capacity-2026-09-08.json),
[journal](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py),
[capacity migration](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/migrations/0009_attempt_capacity.sql),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_capacity.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 697 tests and eleven checks pass for the recorded build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved.
No exact task-close, learning or full-W3 completion claim follows.

## W3.2b2b1 persistent key revocation, 2026-09-08

W3.2b2b1 uses a private persistent POSIX file lock for cooperating keystore access: shared reads and exclusive initialization/create/shred/rotation, with nonblocking contention failure and no retry loop. It releases that lock before ledger audit waits and uses private atomic writes with targeted cleanup of owned interrupted-write files. The local crash fixture preserves revocation after owner death. This is not the runtime process-owner startup lock, full state inventory, mixed-version/network-filesystem support or multi-worker qualification. Active-process erasure coordination and safe workspace release remain later recovery work.

See the [plain-language report](../../reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md),
[checks and pre-change probe](../../reports/research/adrl-w3-2b2b1-key-revocation-2026-09-08.json),
[keystore](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/keystore.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_key_revocation.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/key-revocation.md).
All 724 tests and eleven checks pass for the recorded Darwin build. Prior wording,
architectural status and maturity fields remain unchanged. Independent security review,
process/erasure/release coordination and full W3 remain open.

## W3.2b2b2 process coordination, 2026-09-08

An internal coordinator now serializes a durable workspace fence before one supervised synthetic launch. Competing coordinators and later journal starts honor that block across terminal events, erasure and restart. A protected worker drains cancellation and a separate monitor observes lost authority; no PID-based recovery or workspace-release API exists. This is scoped fixture coordination, not full multi-worker runtime or complete writer-boundary qualification.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2c writer-boundary research, 2026-09-08

The W3.2b2c research fixture found that a daemon-owned container outlives a killed Docker CLI client. Durable create/start intent, exact resource/engine/configuration identity, ambiguous-acknowledgement handling and restart recovery are therefore prerequisites to the proposed isolated backend. The existing local engine is available, but no runtime owner/cleanup bridge or multi-worker qualification is added. Existing permanent workspace fences remain untouched.

See the [plain-language report](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md),
[experiment and source evidence](../../reports/research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[fixture source](../../reports/research/writer-boundary-2026-09-08/probe.go),
[frozen packet](../../reports/waves/w3-2b2c-writer-boundary.md) and
[next ownership packet](../../reports/waves/w3-2b2d-resource-ownership.md).
The corrected research run completed six bounded observations, including negative controls.
The previously passing 759-test/eleven-check runtime source is unchanged; all 300 declared
hashes were reverified, not rerun. This research changes no runtime behavior, architectural
status, maturity, release authority or whole-W3 completion claim. Prior wording is retained.

## W3.2b2d1 stopped resource ownership, 2026-09-08

The stopped-resource owner serializes one durable create claim per authenticated operation and one permanent fence per workspace on the existing ledger. Matching bound retries recover by exact engine/resource/configuration identity; a lost create receipt cannot authorize adoption or another create. Store reopen and removal-acknowledgement recovery are tested. This is local synthetic resource coordination, not the complete runtime startup-lock/state inventory or multi-worker deployment qualification.

See the [plain-language report](../../reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.json),
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[unit cases](/Users/arunmenon/projects/adrl-core/tests/unit/test_resource_owner.py),
[local engine cases](/Users/arunmenon/projects/adrl-core/tests/integration/test_resource_engine.py)
and [runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
All 812 tests and eleven engineering checks pass, with 306 declared source hashes unchanged
during the run. This supports the scoped tested behavior only. Prior decision wording,
architectural status and maturity fields remain unchanged; full B2/B3 and W3 remain open.

## W3.2b2d2 launch-contract research and identity gate, 2026-09-08

W3.2b2d2 inspected launch/kill/removal ordering and attempted two bounded research runs. Both stopped during their first case on configuration identity mismatch, so zero of six intended lifecycle cases have accepted records. The next design separates a one-shot launch claim and permanent denial marker, admission sealing, known-launch stopping and ambiguous-launch discard. These are proposed mechanisms, not runtime capabilities. A stopped-state observation or client exit alone cannot discharge an in-flight daemon operation; active recovery remains gated.

See the [plain-language progress report](../../reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md),
[failed-run/source evidence](../../reports/research/adrl-w3-2b2d2-launch-contract-2026-09-08.json),
[proposed execution contract](../../reports/waves/w3-isolated-execution-contract-v1.md),
[next identity packet](../../reports/waves/w3-2b2d2-identity-compatibility.md), and the unchanged
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py) and
[runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
No runtime source changed: the 812-test/eleven-check baseline is reused with all 306 declared
hashes verified. No new passing runtime run is claimed. Prior wording, architectural status
and maturity remain unchanged. Active launch, full d/B2/B3 and W3 remain open.

## W3.2 execution identity and launch research, 2026-09-08

The changed research batch completed one identity and six lifecycle cases. A stop before a delayed start did not prevent later work; a manual restart changed StartedAt while RestartCount remained zero; client death left the fixture running until its own exit. These observations support durable one-shot launch and explicit recovery requirements, but no runtime launch, admission seal, marker, startup lock or multi-worker qualification is implemented by this research.

See the [plain-language report](../../reports/adrl-w3-execution-identity-2026-09-08.md),
[research evidence](../../reports/research/adrl-w3-execution-identity-2026-09-08.json),
[comparator](../../reports/research/execution-identity-2026-09-08/execution_identity.py),
[offline cases](../../reports/research/execution-identity-2026-09-08/test_execution_identity.py),
[driver](../../reports/research/execution-identity-2026-09-08/run_probe.py) and
[next runtime packet](../../reports/waves/w3-isolated-launch-runtime.md).
101 offline research cases and seven engine observations pass. The unchanged runtime's
812-test/eleven-check baseline is reused with 306 verified hashes. Prior decision text and
all status/maturity fields are preserved; no grade promotion, independent review or full-W3
completion follows.

## W3.2 one-shot fixture runtime prototype, 2026-09-08

An internal fixture coordinator now publishes permanent launch denial, claims a unique authenticated launch, records acknowledgement/sealing, drains cancellation and supports known stopping or operator recovery. A separate nonblocking recovery lock serializes cleanup; an issued discard only reconciles absence. This is scoped synthetic execution, not the complete runtime startup lock or multi-worker promise. Current-build engine qualification remains open after a lost stopped-create receipt.

See the [report](../../reports/adrl-w3-isolated-launch-2026-09-08.md),
[checks and failed-run evidence](../../reports/research/adrl-w3-isolated-launch-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[pinned transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[permanent markers](/Users/arunmenon/projects/adrl-core/src/adrl/core/launch_markers.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_isolated_execution.py),
[runtime guide](/Users/arunmenon/projects/adrl-core/docs/isolated-execution.md) and
[next diagnosis packet](../../reports/waves/w3-launch-create-receipt-diagnosis.md).
Final offline validation: 861 passed, eight opt-in engine cases skipped, all eleven checks;
315 declared hashes stable. Two engine invocations each had three passes and one failure.
The allowance is closed and all eight fixtures/image are absent. All prior wording and
77 status/maturity fields are preserved. No independent review, grade promotion or full-W3
completion follows.

## W3.2 receipt correction and pinned-engine validation, 2026-09-08

Execution v2 separates stopped preparation from active I/O without mutating the stopped owner. All active inspection/profile/start/kill/discard/recovery requests use a tighter validated view. The pinned synthetic normal and recovery workflow now passes the fresh finite engine packet. This does not implement the runtime startup lock, general watchdog or multi-worker deployment promise.

See the [plain-language report](../../reports/adrl-w3-transport-receipts-2026-09-08.md),
[checks and cleanup evidence](../../reports/research/adrl-w3-transport-receipts-2026-09-08.json),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[versioned execution policy](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[receipt fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_create_receipt.py) and
[next custody packet](../../reports/waves/w3-active-copy-custody.md).
Final validation: 895 passed, zero skipped, all eleven checks, 316 stable source inputs;
13 original create receipts and absence confirmations, one image removed. The bounded d2
synthetic lifecycle slice closes. Full B2/B3/W3, real-harness and independent qualification
remain open. Prior wording and all 77 architectural status/maturity fields are preserved.

## Context and rationale

The review found that the multi-worker blocker was never SQLite but the process-local Python dict holding session-to-route and pin state (MEM-006, SEM-002, SAF-002). The adrl-core build moved sticky and pin state behind a port, and its own known-gaps file lists what is still process-local. This decision makes the inventory a versioned artifact and the single-process rule an enforced startup check, so that "we will go multi-worker later" cannot happen by starting two processes.

## Adversarial review (2026-09-03)

### Steelman
A declared constraint with a startup lock is safer than an undeclared one that works until the second process starts. The inventory turns "is it safe to run two?" into a lookup.

### Attacks
1. **A per-developer laptop never needs two workers, so this is ceremony.** Answered: the lock costs one file; the inventory is what makes the later move reviewable.
2. **Pins are port-backed but the pin cache is per process, so two processes can disagree for one request.** Answered: that is exactly the class of item the inventory must mark `process-local` with a stated race window; the startup lock prevents the disagreement today.
3. **SQLite's WAL already allows concurrent readers, so the constraint is over-strict.** Answered: readers are fine; the constraint is on writers and on the in-memory caches that shadow the ledger.

### Evidence
- ADRL-MEM-006 (amended); "This dict, not SQLite, is the OPS-001 multi-worker blocker"; provider concurrency contract.
- ADRL-CAS-006; `state_loss=true` on restart when sticky state is unavailable.
- SQLite, "Write-Ahead Logging" (official docs), as cited in ADRL-MEM-001; one writer at a time, all processes on the same host.
- adrl-core `docs/known-gaps.md` (2026-09-02); remaining process-local items.

### Verdict
**PROPOSED.** Names the constraint every neighbouring decision assumed. Needs an owner and the first state inventory.

## Follow-ups

- [ ] Write `state-inventory-v1.json` listing every state item, its class and its restart behaviour; CI fails when a new module holds state not in the inventory.
- [ ] Startup lock file with owning pid; second process exits with a named error.
- [ ] Golden test: pin visible across two `PinRegistry` instances on one store (already in adrl-core) plus a documented race window measurement.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded versioned creation/active transport separation and passing pinned-engine lifecycle acceptance | Prior decision/evidence preserved; bounded d2 closes, full W3 and grades unchanged |
| 2026-09-08 | Recorded W3.2 fixture launch prototype, offline checks, engine failures and operator cleanup exception | Prior decision/evidence preserved; engine workflow remains unqualified, no status/maturity promotion |
| 2026-09-08 | Recorded W3.2 identity correction and seven accepted bounded launch observations | Prior wording and failed evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d2 failed launch probes, source-explained identity gate and proposed lifecycle | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d1 stopped ownership, acknowledgement recovery and explicit limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2b2 stop coordination, permanent workspace blocking and failure evidence | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2b1 key-revocation ordering fix, fault evidence and remaining recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2a versioned terminal capacity, compatibility and recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b1 process ownership and tested cleanup limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-07 | Recorded W0 baseline, repeatable checks and explicit remaining gates | Prior decision wording and evidence preserved; no architecture or maturity change |
| 2026-09-03 | Proposed (first capture of the OPS bucket) | (none) |
