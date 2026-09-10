# W3.2b1: Knowing which processes ADRL owns

8 September 2026. Offline engineering slice under the approved
[roadmap](adrl-implementation-roadmap-2026-09-07.md) and
[frozen process-ownership packet](waves/w3-2b-process-ownership.md).

ADRL now has a tested internal way to launch a bounded local command and clean up the
process group it owns. **All 669 tests and eleven engineering checks pass.** This includes
38 new synthetic process cases. The result improves the machinery needed for trustworthy
task evidence; it does not yet let ADRL declare that a whole workspace has stopped changing.

## Why this step matters

Suppose a coding task says it has finished, but a helper it started is still editing a file.
Taking a snapshot now could preserve a halfway state. Later, ADRL might judge that snapshot
and wrongly conclude that its routing decision worked or failed. Course correction would
then be learning from the wrong output.

The last three pieces address different parts of this problem:

| Piece | What ADRL can now establish | What it still cannot establish |
|---|---|---|
| W3.1: retained captures | An identifiable encrypted copy survives later folder edits | That it was the task's exact finished output |
| W3.2a: attempt journal | The original starting point and later close/interruption requests have durable history | That a close request means processes stopped |
| W3.2b1: process ownership | A bounded command's exit and cleanup of its owned process group can be observed | That detached or unrelated writers stopped, or that the task succeeded |

These pieces are implemented separately. The new process runner is not yet connected to
the journal, capture archive, verifier, public API or CLI.

## How the new piece works

ADRL starts a small private launcher in its own process group. The launcher starts the
approved command, reports its exit code and stays alive until cleanup. Keeping this owned
identity available matters: ADRL sends its final group signal before reaping the launcher,
and never signals the group after releasing that identity. There is no operation that
accepts a saved process ID as permission to kill something after a restart.

A private pipe connects owner and launcher. If the owner dies, pipe closure tells the
launcher to stop its group. A watchdog handles an owner that stays alive but stops
monitoring. Timeout, explicit stop and coroutine cancellation also perform cleanup.
The runner preserves cancellation semantics while waiting for its cleanup worker, including
repeated cancellation and event-loop shutdown.

Inputs are bounded and the executable's content is checked twice against the operator's
expected digest. The child gets a minimal environment plus only explicit operator-supplied
values; it inherits no private control descriptors. Standard input/output/error are discarded.
The in-memory report contains keyed request provenance, policy and source identities,
exit/cleanup observations and timing. It does not record raw command arguments, environment,
workspace paths or output. A failed signal or unconfirmed reap prevents reuse of that runner.

## What the experiments showed

The real local fixtures exercised ordinary and nonzero exits, a helper that outlives its
direct parent, a command that ignores ordinary termination, timeouts, explicit stops,
repeated cancellation, event-loop shutdown, owner death and watchdog cleanup. They also
covered bad executable pins and input bounds, a changed executable between the two checks,
malformed launcher messages, missing status, concurrent calls and reuse, environment
inheritance, and injected signal/reap failures. Failed cleanup remains visible.

One deliberate test is particularly useful: a child creates a separate session and writes
a file after the original group has been cleaned up. **That child survives.** It is a
bounded fixture that exits itself; this demonstrates the backend's limitation. Every result
therefore explicitly says that its containment scope is only the process group and that
it is ineligible for exact-close attribution and learning.

The full regression run passed all eleven checks with no declared-input drift. The unchanged
data inventory covers 273 stored fields; this slice adds no persisted fields. The generated
map now identifies 105 implementation modules citing 74 of the 77 decisions. A citation
identifies ownership, not completion of the whole decision. Database schema 8 and public
API preview 4 are unchanged.

## What improved, and what did not

We gained tested process ownership and cleanup mechanics on Python 3.12.7 on Darwin.
This is scoped offline evidence. It is not a hostile-code sandbox, a guarantee about every
descendant or editor, a secure credential boundary, Linux qualification or another harness
integration. Process creation, file hashing and scheduling can exceed configured timeouts;
no hard real-time deadline is claimed. Executable checks do not pin the full dependency tree
or defeat replacement races against an attacker controlling the account.

The embedding application must retain normal child-signal handling and avoid competing
child reapers. Detachment, outstanding kernel work and unrelated folder writers remain
outside the established boundary. Existing sandbox, active plaintext lease, erasure and
crash-leftover limitations remain open.

Five owning records now document the applied scope: **OPS-001, SAF-007, SEM-006, MEM-003
and TRU-001**. Their earlier wording remains intact. All 77 architectural-status and
maturity fields are preserved; **no grade is promoted**. In particular, a process-descendant
test does not qualify SEM-006's harness identity or privacy inheritance promises.

For adaptive improvement, the benefit is a more dependable foundation for deciding what
actually happened. We have not shown better routing or recursive self-improvement in this
slice. Those conclusions still require trustworthy outcome attribution, qualified evaluation
and controlled comparisons.

## Corrections and next steps

Preflight lint identified asynchronous fixture operations, long lines and a missing retained
task reference; these were corrected. During self-review, the worker was changed from a
separately cancellable task to a protected executor Future so loop shutdown cannot appear
to finish cleanup before the thread stops. A real shutdown fixture now covers that case.
The focused behavior runs and the first full combined run passed. No failed invariant was
waived. This was implementation and self-review by the same assistant, not independent
security review.

W3.2b1 closes as a local engineering slice. W3.2 and full W3 remain open. Next:

1. Freeze and implement the bounded admission/recovery work: reserve room for terminal
   records and coordinate erasure, process cleanup and reservation release. Quota exhaustion
   or erased pending attempts must not silently grant permission to reuse a workspace.
2. Qualify a complete writer boundary, or explicitly deny exact-close attribution where
   that boundary cannot be established. Process groups alone cannot pass this gate.
3. Bind the qualified attempt close to its reserved capture, then finish plaintext lease
   and crash recovery before real task payload capture and retained verification.

No native harness task, model-service call, new paid usage, live routing change, commit or
deployment occurred. The hourly continuation resumes from the
[execution state](research/adrl-execution-state.json), subject to the local environment being
available. The [journey](adrl-implementation-journey.md) remains the running account.

Evidence: [checks and source manifest](research/adrl-w3-2b1-process-ownership-2026-09-08.json),
[source diff](research/adrl-w3-2b1-process-ownership-2026-09-08.patch),
[internal guide](/Users/arunmenon/projects/adrl-core/docs/process-ownership.md),
[runner](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_owner.py),
[launcher](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_anchor.py) and
[process fixtures](/Users/arunmenon/projects/adrl-core/tests/unit/test_process_owner.py).
