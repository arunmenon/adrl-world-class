# Wave 3 progress: resolving the startup mismatch

8 September 2026. We resolved the research blocker and completed all seven planned observations
in the changed experiment. **ADRL remains in Wave 3.2. The runtime launch feature is next.**

Think of this part of ADRL as a supervisor keeping a reliable record of a coding task. Before
we can trust a result, we need to know which work started, whether it stopped, and whether it
could start writing again. A message saying “finished” cannot answer all three questions.

## What changed today

The previous experiment stopped because Docker described one setting differently after startup:
false became null. We now have a research comparison that accepts precisely that change on the
observed engine, where the setting is unsupported. It still rejects changed images, commands,
permissions, networking, mounts, resource limits and other configuration differences. The
implemented stopped-container ownership code was left intact.

There are **101 passing offline checks** for the comparison and research reporting. The first
94-case run had one incorrect negative fixture: it supplied a value that was already unchanged.
We corrected that test, preserving the comparison rule. Self-review also caught embedded-client
indentation before any engine experiment. Reporting now preserves completed assertions and
records test failures separately from cleanup failures.

The new real-engine batch then passed on its first permitted identity stage and first permitted
lifecycle stage. No engine repair or repeat was needed. The old two failed runs remain failed
historical evidence; they have not been relabelled as successes.

| Observation | What happened | What ADRL must do with this knowledge |
|---|---|---|
| Identity across startup | Only the expected unsupported OOM field changed | Use a narrow, versioned execution comparison tied to original ownership |
| Stop before a delayed start | The stop was refused; releasing start still produced a late write | Prevent future starts separately from stopping existing work |
| Remove before a delayed start | The delayed start received 404 | Use confirmed exact-resource removal for the tested abort ordering |
| Lose the start reply | Work ran even though the client lost its reply | Record uncertainty; never issue a duplicate start to “try again” |
| Stop a known running fixture | Its output stayed unchanged across the scheduled late-write delay | Build a verified stopping boundary before capturing a task result |
| Restart an exited fixture | StartedAt changed and work resumed, while RestartCount stayed zero | Keep a permanent launch denial; do not rely on the restart counter |
| Client dies | The fixture kept running, then independently exited after 6.12 seconds | A lost client is not a stop mechanism; this lifetime bound applies only to the fixture |

Seven containers were created, six of them ran, and one of those was deliberately started twice:
seven successful synthetic starts in total. All seven exact container IDs and the one imported
image were confirmed absent afterward. There were no model calls, real task payloads, image
pulls, installations, daemon setting changes or new paid usage.

## What this improves, and what remains

We have better evidence for how the execution backend must behave when messages arrive late or
disappear. We can now implement one launch per admitted attempt, permanent denial of a second
launch, and different handling for a known stop versus an uncertain launch.

This is **engineering course correction**: observe a failure, identify its cause, change a
specific hypothesis, test it against unsafe alternatives, and update the decision ledger.
It is part of the discipline needed for RSI. ADRL has not yet demonstrated automatic policy
improvement, better routing or independently evaluated learning.

The runtime source is unchanged. Its **812-test, eleven-check baseline is reused after verifying
all 306 declared source hashes**, not counted as a new run. The 101 research checks and seven
engine observations are separate evidence. Schema 11, API preview 4 and runtime inventory remain
unchanged. All 77 architecture-status and maturity fields are preserved; no whole-ADR grade
increase follows from synthetic research.

The experiment does not qualify arbitrary commands, all daemon race orderings, hostile hosts,
sandbox security, physical erasure, real harness execution or exact task-close capture. The
research comparator uses evidence digests; authenticated runtime ownership remains a separate
requirement. Independent review is still pending.

## What comes next

1. Implement the internal one-shot launch, admission seal and recovery contract, with faults and
   cancellation tested. Every outcome keeps the workspace blocked and learning ineligible.
2. Qualify active-copy cleanup and safe capture of the exact output after stopping.
3. Connect that evidence to verification and the operator view, then demonstrate a real Claude
   Code task under an explicit image, network, credential and retention profile.

The shared contracts continue to serve the cross-harness product; these experiments add no
Claude-specific assumptions to task identity or evidence. No new user decision blocks the next
local implementation slice. Real-harness exposure and independent evaluation need their later
decisions. The existing hourly continuation remains the route for subsequent bounded work.

Review: [journey](adrl-implementation-journey.md),
[evidence and source hashes](research/adrl-w3-execution-identity-2026-09-08.json),
[comparison contract](waves/w3-execution-identity-v1.md),
[closed experiment bounds](waves/w3-identity-launch-experiment-v2.md),
[next implementation packet](waves/w3-isolated-launch-runtime.md),
[research code](research/execution-identity-2026-09-08/execution_identity.py),
[research driver](research/execution-identity-2026-09-08/run_probe.py).
