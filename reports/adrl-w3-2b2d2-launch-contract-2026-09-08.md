# Before ADRL can run a job, it must recognize it after startup

W3.2b2d2 progress report, 8 September 2026.

**This run found and documented a compatibility issue that must be resolved before adding
launch to ADRL.** The existing stopped-container owner compares the complete reported
configuration. Docker changes one reported field during startup on this machine, so that
comparison cannot simply be reused for an active container.

Two bounded research runs failed at this check. We stopped at the packet's two-run limit,
removed both exact fixture containers and the one imported image, and prepared the next
specific correction. **No active backend was added.** The runtime remains unchanged at its
verified **812-test, eleven-check baseline**; all 306 declared source hashes still match.

## What we tried to establish

The intended next capability is straightforward to describe: start an owned job once, know
whether it really started, stop it when authority ends, and keep only output whose history
ADRL can defend. The details matter when requests or acknowledgements arrive late.

The experiment froze six cases before running: delayed start versus kill, delayed start versus
removal, lost start acknowledgement, preserving output after a known stop, explicitly restarting
a stopped container, and losing the client while a self-terminating fixture continues.
These were small self-authored fixtures, with no network, host repository/credential/socket
mounts, real task payloads, model calls, image pulls or daemon setting changes.

**None of the six cases has a completed acceptance record from this run.** Both attempts
stopped during the first case when the cleanup identity check raised. Their logs and failed
records are retained; they are not counted as passing lifecycle evidence.

## What we learned from the failure

The second run saved inspections both before and after startup. Their complete configuration
comparison showed one difference:

| Reported setting | Before start | After start |
|---|---|---|
| `HostConfig.OomKillDisable` | `false` | `null` |

This field concerns disabling the out-of-memory killer. The selected engine reports that
control as unsupported. Docker's source supplies a false default and later clears the field
when unsupported, which explains the observed change. This does **not** establish that every
default-looking change is harmless. [Moby's configuration handling](https://raw.githubusercontent.com/moby/moby/v27.3.1/daemon/daemon_unix.go)

The first run did not retain its initial full inspection, so we cannot reconstruct its exact
configuration difference. The initial empty-port-map hypothesis was only a hypothesis; a
second run permitting that narrow representation change still failed. We have not added that
exception to the runtime.

Both containers independently exited. Using their original create receipts, we verified the
exact engine, image, name, command and every explicitly requested security/resource control,
then removed them without force and confirmed absence. This was fixture recovery, not adoption
of an unknown resource. The runtime's stricter stopped-resource contract remains unchanged.

## How the plan changes

The next packet first defines a **versioned comparison for execution**, linked to the original
unchanged preparation record. Its proposed exception is only the observed false/null pair,
only for the named engine and unsupported capability. Enabling the control, changing limits,
mounts, network, capabilities, image, command or engine must still fail. Offline altered-input
cases precede any fresh bounded engine run.

We also need better experiment records: save initial and intermediate observations before
cleanup, and preserve a primary failure separately from a cleanup failure. The two attempts
showed why an exception during cleanup must not erase the account of what preceded it.

The [proposed execution contract](waves/w3-isolated-execution-contract-v1.md) now separates two
paths:

- **Known launch and stop:** seal further launch/exec/restart admission, drain the original
  request, establish stopping, then retain output for the later capture stage.
- **Ambiguous launch:** do not retry or treat a not-running response as closure. Use a separately
  authenticated abort/discard path, or remain visibly blocked if ownership or cleanup is uncertain.

This is a proposed contract, not shipped behavior. Docker's startup code includes operations
that continue without the caller's cancellation, which is why client disappearance is insufficient.
[Moby's startup implementation](https://raw.githubusercontent.com/moby/moby/v27.3.1/daemon/start.go)
Its removal implementation provides grounds to investigate discard as a barrier against delayed
start, but those experiment cases still need to pass. [Moby's removal implementation](https://raw.githubusercontent.com/moby/moby/v27.3.1/daemon/delete.go)

## Where this leaves maturity and RSI

The prior ownership implementation remains validated within its stopped-only scope. The new
research narrows how an active backend should be built; it does not establish launch recovery,
writer containment, exact output capture, erasure or a real-harness result. All 77 architectural
status and maturity fields remain unchanged. There was no independent security review.

This is useful course correction: test an assumption, retain the failure, explain the cause,
and revise a small part of the plan. It is still human-directed engineering performed by
Codex, not demonstrated recursive self-improvement or automatic policy adoption.

Next is the [identity compatibility packet](waves/w3-2b2d2-identity-compatibility.md). Once its
specific rule passes, complete the six outstanding cases under a newly frozen, changed
experiment. Then implement the bounded execution lifecycle. Full W3 remains open, and the
existing hourly continuation can proceed with that engineering work without a new user decision.

Review trail: [running journey](adrl-implementation-journey.md),
[parent packet](waves/w3-2b2d2-launch-admission.md),
[failed experiment and limits](waves/w3-2b2d2-launch-experiment.md),
[evidence and source hashes](research/adrl-w3-2b2d2-launch-contract-2026-09-08.json),
[research driver](research/launch-recovery-2026-09-08/run_probe.py), and the unchanged
[runtime ownership guide](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
