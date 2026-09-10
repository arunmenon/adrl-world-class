# ADRL: the first routing lab is running

8 September 2026. Lab A.1, a bounded offline implementation slice.

**We can now run a repeatable experiment and see what ADRL chose, what it actually
dispatched, and what happened to that request.** This is a concrete first step on
the [product roadmap](adrl-product-roadmap-2026-09-08.md) toward learning better
routing from evidence.

Open the [routing table](research/routing-lab-2026-09-08/run-2/report.md) to see it
in action. ADRL's actual gates, router, cascade controller and ledgers run. The
input client and response endpoint are synthetic: no coding model or real harness
executed a task in this experiment.

## What we can see now

| Situation | What actually happened | Why this matters |
|---|---|---|
| Fix a README typo | Selected local; endpoint received the local alias | Simple work can take the inexpensive path |
| Same typo request, much larger context | Selected and dispatched frontier | The request alone does not determine the route; context influences it |
| Refactor a module | Selected and dispatched frontier | The current heuristic distinguishes some harder tasks |
| Repeated tool activity during the typo task | Started local, then dispatched cheap cloud at a later boundary | Adaptation can happen as work unfolds; the original decision and later dispatch remain separately visible |
| A synthetic secret appears in a tool result | Frontier lineage switches to local; next clean result stays local | Privacy constrains the available choices even when the task is difficult |
| Pinned request exceeds local capacity | Blocked before endpoint dispatch | A restriction does not silently become cloud permission |
| Endpoint omits model identity | Receipt says assumed intended | We can see where identity evidence is missing |

These are observations of routing behavior. They do not establish model competence,
task completion, provider receipt reliability or financial savings. The static
health view and in-process streaming fixture do not qualify real network behavior.

## The first course correction is already clear

Two earlier counterexamples still reproduce through the complete Messages path:

- “Rename a variable and redesign the concurrency algorithm in worker.py” selects local.
- “Explain the race condition and implement a fix in worker.py” selects local.

In both cases a simple-action match appears to mask harder requested work. The lab
preserves these weaknesses; this implementation changes no routing policy. The next
bounded correction should make their treatment explicit and show all resulting
route changes, including regressions, on the same cases and fresh paraphrases.
Only subsequent model experiments can establish which model actually succeeds.

## What was built

The [developer workbench](../../adrl-core/tools/run_routing_lab.py) accepts a frozen
[synthetic suite](../../adrl-core/artifacts/lab/routing-suite-v1.json), creates fresh
disposable ledgers, runs the existing composition and exports a readable report.
Every run gets its own ID and source/config/suite fingerprints. Initial choice,
current dispatch, feature snapshots and receipt provenance remain inspectable.

There are 16 planned cells: 15 submitted Messages requests and one explicitly
unsupported Responses cell. Of those requests, 13 received synthetic successful
responses, one was blocked and one received a synthetic upstream error. Fourteen
requests reached the controlled endpoint. Ten distinct ADRL decision IDs were
created; continuations reuse their original decision. **These are not 16 completed
coding tasks or independent training examples.**

An append-only experiment journal retains every planned attempt. Interrupted work
appears as indeterminate or not started when inspected; reruns use new directories.
Synthetic outputs never enter a developer ledger or become learning labels. The
existing encrypted verifier-experiment archive remains separate. This initial tool
does not yet provide a general cross-harness runner, resume service or K0 package.

The [operator guide](../../adrl-core/docs/routing-lab.md) includes the exact command.
[Run manifest](research/routing-lab-2026-09-08/run-2/manifest.json),
[raw results](research/routing-lab-2026-09-08/run-2/results.json) and
[qualification report](research/routing-lab-2026-09-08/validation.json) retain the evidence.

Verification: seven focused runner tests passed, and all eleven engineering checks
passed on 320 stable inputs: 894 tests passed and eight engine cases stayed skipped
without a new engine allowance. The original 316 runtime inputs are unchanged;
four new workbench/suite/test/guide files were added. Schema 12 and API preview 4
remain unchanged. [Full check evidence](research/routing-lab-2026-09-08/engineering-checks.json).

## How this advances maturity

EVL-005 gains a reusable, source-bound synthetic diagnostic with separate reporting.
RTG-002 gains inspectable evidence connecting current choices to dispatch. MEM-001
provides the actual route/event history used by the export. SEM-007's tested scope
remains the Messages fixture; the unsupported cell grants no Responses capability.

This improves the ability to detect, explain and retest routing defects. It does
not improve the router's judgment yet. All 77 decision texts, architectural statuses
and formal maturity fields remain unchanged. No organic-evidence gate or broader
D3/D4/D5 claim follows from this lab exercise.

## What comes next on the same roadmap

1. **Correct and compare routing.** Apply the bounded mixed-intent correction, retain
   conservative restrictions and publish before/after evidence. Owner: RTG/LRN.
2. **Complete a real-task evidence path.** Finish the existing custody/exact-output
   prerequisites and qualify a Claude Code profile with a verifier and a finite,
   approved model-run budget. Measure task outcomes, repair effort, cost and latency.
   Owners: MEM/SAF/SEM/EVL.
3. **Expand and build K0.** Add a separately qualified OpenCode profile and build
   descriptive knowledge by task/context/harness/model version. Graph enrichment
   remains a candidate projection of MEM. Lab evidence keeps its provenance.
4. **Evaluate learned routing, then RSI.** Admit appropriate evidence, compare
   candidate checkpoints on fresh tasks and distribute only approved compatible
   packages. Later test whether an improved offline learning process itself produces
   better routing for the same total budget. Owners: LRN/EVL/RTG.

The present slice is complete only within Lab A.1; the rest of Lab A and later
phases retain their gates. The hourly automation stays paused. No model call,
Docker mutation, spending, deployment, learned authority or commit occurred.

An initial diagnostic export lost its source-manifest field through a duplicate
JSON key. It is [retained and disqualified](research/routing-lab-2026-09-08/run-1/QUALIFICATION.md).
The corrected run and a regression check preserve source identity. See the
[execution packet](waves/lab-a-routing-experiment.md) for the bounded scope.
