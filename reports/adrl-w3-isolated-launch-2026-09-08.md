# Wave 3: the one-shot execution prototype is implemented

8 September 2026. ADRL now has an internal prototype that can launch the admitted synthetic
fixture once, record what happened, stop known work and recover an uncertain run. **Offline
verification passes. Complete real-engine qualification remains open because one create reply
was lost. We are still in Wave 3.2.**

## What we built, in plain language

Previously, ADRL could create a stopped container and remember which one it owned. It could not
start that container through the new supervised backend. This implementation adds the next part
of that lifecycle, limited to our self-authored test program.

Before starting, ADRL checks the original ownership record, task/session authority, image layer,
command, engine and security settings. It then leaves a permanent “do not launch again” marker
and writes an authenticated launch claim. Only the original caller may send the start request.
A restarted process cannot turn that old claim into another launch.

After the daemon acknowledges startup, ADRL records its exact start time and seals further
launch admission. A separate worker watches authority, cancellation and the fixture deadline.
Known work can be stopped and its container layer retained. When startup is uncertain, the
recovery path attempts to discard the exact authenticated fixture and confirm absence.

| Situation | Implemented response | Remaining limit |
|---|---|---|
| Two callers try to launch | Permanent marker and unique claim allow at most one dispatch | Host/storage rollback is outside this guarantee |
| Start reply disappears | No second start; owned recovery or visible uncertainty | A lost create reply has no original resource binding |
| Caller is cancelled repeatedly | The worker drains before the call finishes cancelling | Scheduling and I/O are not hard real-time bounds |
| Owner process dies | Durable claim survives; later operator recovery can discard | Owner death does not itself stop daemon-owned work |
| Content key is erased | Host-authenticated cleanup can still operate | No claim about physical blocks, snapshots or arbitrary active copies |
| Cleanup audit fails | Report the audit failure separately from observed cleanup | No invented terminal event or exactly-once network promise |
| An old discard is already issued | Reconcile exact absence; a present resource stays uncertain | No automatic reissued DELETE from that history |

Every outcome keeps the workspace blocked and remains ineligible for exact-close attribution
and learning. There is no public start endpoint, general command runner, network access or real
harness workload in this slice. The original stopped-resource history remains separate.

## Evidence, including the failures

The final required run passed **861 tests and all eleven checks**, with **315 declared source
hashes unchanged throughout the run**. Eight opt-in engine tests were deliberately skipped
because their engine allowance had closed. These counts are not directly comparable with the
previous 812-test run, which included four engine tests. There are **53 new offline cases** in
the new launch test module, including the experiment stop guard.

The new ledger schema is 12. The inventory covers 370 checked fields and 380 documented entries,
including permanent marker and recovery-lock metadata. The module map covers 111 implementation
modules and the same 74 of 77 ADRs; the public API remains preview 4.

Real-engine validation used two four-case invocations, the allowed maximum:

| Run | Result | What failed |
|---|---|---|
| First runtime build | 3 passed, 1 failed | Erasure cleanup succeeded, but the final relaunch-denial test expected the wrong exception class |
| Corrected runtime build | 3 passed, 1 failed | The first stopped-container create lost its original reply before any launch; the other three runtime fault cases passed |

The first assertion was corrected. Self-review also added recovery serialization and an
issued-discard no-reissue check. The second failure remains unresolved. Docker did create a
never-started resource, but its full ID did not reach the original receipt logger. A timeout is
a plausible explanation, **not a proved cause**: the underlying exception was not retained.
The prior successful research experiments are separate evidence and do not erase this failure.

There was also a test-runner mistake: without fail-fast enabled, the remaining three engine
cases ran after that uncertain create. We recorded the deviation and added a tested fixture
guard that halts the batch on an unreceipted create. Future engine runs also require maxfail=1.
Creation intent now retains timestamp, the synthetic request body and bounded error information.

Offline verification caught a stale compatibility-test expectation of schema 11. Two existing
assertions were updated to 12, retaining all their checks that old session data survives.
An edit guard initially expected one occurrence and stopped the edit; an unchanged check run
started and was interrupted. Its cancelled record is preserved. The final corrected run passed.
The earlier focused unit failure was a test calling the attempt journal with the wrong arguments;
that fixture was corrected. No failed or cancelled run is presented as a passing build.

## Cleanup and ownership

Eight creates were issued. Seven original client receipts have exact absence confirmations.
Seven synthetic fixtures started; the eighth never started. The unreceipted candidate matched
the fsynced unique create intent, this batch's image, creation interval and every requested
command/security/resource control.

We removed that one exact stopped candidate non-force as a documented operator-maintenance
exception under the existing disposable-fixture cleanup authorization. This exception did not
bind it into runtime ownership or add automatic name-based adoption. The original uncertainty
is preserved. **All eight fixtures and the one imported image are confirmed absent.** There
were no real task payloads, model calls, image pulls, installations, daemon changes or new spend.

## A cleanup bug corrected during self-review

A 404 from the engine-info endpoint could previously be mistaken for evidence that a container
was absent. Both the new execution path and the existing stopped-owner path now distinguish
those cases. Only a 404 from the exact container inspection can confirm absence. Regression
tests cover that distinction; malformed exited states and changed start timestamps also refuse
cleanup/retained-output qualification.

## Maturity, RSI and the next step

This moves ADRL from researched launch semantics to an implemented, fault-tested internal
prototype. It adds the operational evidence needed before task outputs can become trustworthy
learning data. It does not yet demonstrate better routing or automatic recursive improvement.

Eight owning ADRs now record the implementation, evidence, failures and remaining gates. All 77
status and maturity fields remain unchanged. Scoped offline evidence is stronger; complete
engine qualification, independent security review, exact task-close capture and real-harness
operation are still open.

Next, diagnose the missing create receipt offline, including the relationship between the
stopped-creation timeout and the shorter active-execution timeout. Preserve the original-ID
requirement and test stop rule. A fresh finite engine allowance can follow a concrete supported
correction, beginning with stopped creation alone. Then finish current-build launch/stop
qualification, active-copy cleanup, exact-output capture and a real Claude Code demonstration.

No new user decision blocks the next offline diagnosis. The existing hourly continuation remains
active. The cross-harness direction is unchanged: shared task, identity and evidence contracts
stay central; this optional execution backend remains behind those contracts.

Review: [journey](adrl-implementation-journey.md),
[checks, failures and source evidence](research/adrl-w3-isolated-launch-2026-09-08.json),
[source diff](research/adrl-w3-isolated-launch-2026-09-08.patch),
[next diagnosis packet](waves/w3-launch-create-receipt-diagnosis.md),
[runtime guide](/Users/arunmenon/projects/adrl-core/docs/isolated-execution.md).
