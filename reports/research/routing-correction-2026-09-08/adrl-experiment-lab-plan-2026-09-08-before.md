# ADRL Experiment Lab: evidence before fleet deployment

**Execution overlay, 2026-09-08:** [Lab A.1](../reports/adrl-lab-first-run-2026-09-08.md) now supplies a synthetic Messages workbench, versioned suite, source fingerprints, actual route/dispatch receipts and interrupted-attempt accounting. This implements part of Lab A only. The generic cross-harness experiment contract, protected task verification, real execution/archive integration and K0 builder remain open. The roadmap now starts with mixed-intent correction against this baseline, then real-task qualification. The user's bounded foreground restart does not authorize models, engine mutation, spend, learning admission or the hourly heartbeat. Original planning scope below is preserved.

8 September 2026 · Planning proposal · No runs, training admission or deployment authorized

**The next proposed engineering milestone is a controlled experiment lab that exercises real harnesses on repeatable tasks, captures attributable results in MEM, and builds an initial candidate knowledge snapshot.** It extends existing ADRL evaluation and experiment machinery.

The user proposed a simulator spanning harnesses and task types, with knowledge pinned to harness versions. That direction makes sense. The lab must distinguish what was simulated, what actually executed and the exact conditions under which its knowledge applies.

## 1. Two execution modes

| Mode | What runs | What the result can establish |
|---|---|---|
| Simulation and fault injection | Synthetic requests, controlled responses, unavailable providers, cancellation and privacy markers | Decision logic, protocol conformance, accounting, restrictions and recovery on named cases |
| Controlled task execution | A pinned real harness and actual model deployment operating on an isolated task workspace | Observed task quality, cost, latency and execution behavior under that experiment's conditions |

“Offline” means outside live developer production work. Cloud-model experiments still make network calls and incur provider charges. Stubs cannot establish that a coding model would solve a task, and old transcript substitution cannot establish what a switched model would do.

Both modes have value. Record execution mode separately from task/evidence origin. Running a real model on a synthetic or public benchmark task does not turn the result into organic developer evidence.

## 2. Reuse what ADRL already has

The [existing experiment implementation](../reports/adrl-improvement-experiment-2026-09-07.md) includes frozen proposals, baseline/candidate verifier comparisons, input fingerprints, per-trial results and an encrypted experiment archive. Its [operator contract](../../adrl-core/docs/verifier-experiments.md) explicitly limits it to curated verifier experiments; a general cross-harness task runner is still missing.

MEM-001–004 provide decision/outcome history, late corrections, exact verification and cause typing. MEM-007/008 provide projections and gated retrieval. MEM-009, LRN-002 and EVL-003 establish comparative ownership and valid execution branches. SEM-007 supplies protocol/profile admission. LRN-005 versions learned artifacts.

The lab should reuse those contracts and providers, while separately qualifying real harness execution, automatic exact-output capture, experiment recovery and the knowledge-building path. The existing runner's lack of a resume/idempotent retry API and protected holdout isolation must remain visible until addressed.

## 3. The experiment pipeline

**Question → frozen task/matrix → execution → exact-output verification → MEM evidence → comparative report → candidate knowledge snapshot → independent evaluation → scoped approval.**

The experiment begins with a question, such as: “For small parser repairs under this harness, when does a more expensive deployment improve complete-task outcomes?” It does not begin by generating an unlimited volume of traces.

Each task has a fixed repository snapshot, description, permitted tools, environment, acceptance criteria, independent verifier and resource limits. Keep task solutions and protected checks outside the agent's writable/readable scope as required by the qualification profile.

Record every planned arm and attempt, including unsupported, blocked, timed-out, interrupted, failed and indeterminate states. An interrupted run never disappears from the denominator. A retry is a new attributable attempt, with its budget and reason.

## 4. The matrix and comparison rules

Use six initial families: small edits; bug repairs; test work; multi-file refactors; mixed-intent/dependency-sensitive work; and long-context/recovery cases. Include same-request/different-context examples and stale or missing context. Task labels alone are not model capability estimates.

Start with one qualified Claude Code profile and appropriate Claude deployments. Add OpenCode under a qualified profile, including local/provider options where supported. Admit Codex/Responses through SEM-007 separately. A blank or unsupported matrix cell is reported explicitly.

**Compare models within a fixed harness/profile first.** Alternatives start from the same task/environment and valid decision-boundary state, with the same verifier and restrictions. Later branching must preserve that harness's transcript/tool state through the boundary. Execute each branch independently.

**Compare harnesses as complete systems.** The same task and repository can run through two harnesses, but their prompts, tools and trajectories may differ. A difference in success is then a harness–model system result; it does not isolate model capability. Keep harness-specific estimates before testing transfer.

Separate fixed-deployment capability experiments from end-to-end router-policy experiments. A model scorecard alone cannot demonstrate that ADRL makes good choices.

A planning example is 30 development tasks, initially across one harness and two permitted deployments: 60 executions before repeats. Adding a second qualified harness with three deployments adds 90. The total of 150 executions still represents 30 distinct task definitions and is a debugging budget, not statistical power or 150 organic labels. Freeze the affordable matrix and repetition plan before any run; reserve fresh confirmation tasks.

## 5. Capture enough to learn the right lesson

| Record | Minimum information |
|---|---|
| Experiment | Question, owner, proposed ADR impact, baseline/candidate IDs, matrix, limits and stopping rule |
| Task/context | Origin, task family, repository/content identity, initial state, acceptance criteria, permitted context and missingness |
| Environment | Harness binary/package version, config and prompt/tool definitions, protocol/adapter version, runtime image, hardware where relevant |
| Deployment | Provider/model identity, model revision when available, local quantization/config, token limits, sampling, cache and pricing basis |
| Attempt/decision | Experiment/task/arm/attempt identity; exact pre-decision features, policy and permitted set; selected and reported served deployment |
| Outcome | Exact output identity, checks/verifier version, pass/fail/indeterminate, typed cause, full costs, duration, repair and late corrections |
| Knowledge | Evidence references, supported conditions, uncertainty, exclusions, extractor/graph/feature versions and candidate approval state |

Use actual ADRL route IDs when ADRL made a decision. A harness-only run retains experiment/attempt identity and cannot fabricate an ADRL decision or route-bound counterfactual pair. Preserve native harness observations and ADRL choices as separately attributable facts.

Store only authorized information under the existing inventory and retention rules. A task graph or derived embedding is subject to those controls. Candidate/model-generated explanations cannot substitute for recorded decision reasons.

## 6. What the first knowledge snapshot contains

Call the first artifact **K0, a lab-derived candidate snapshot**. It may contain:

- Empirical capability profiles by task/context slice and exact supported harness/deployment conditions.
- Linked evidence for successes, failures and uncertainty, including counterexamples and later corrections.
- Candidate rules or comparative features for investigation, with their evidence and transfer limits.
- Optional graph projections connecting task/context, decisions and outcomes, compared with the existing structured/vector retrieval.
- A manifest listing data, feature/extractor, verifier, protocol, adapter, policy and model identities, plus approval state and expiration/requalification conditions.

K0 is useful for research, diagnosis and preparing the first shadow policy. It is not automatically a trained, approved live router. Nor does every experiment justify a durable rule: a sparse slice should remain uncertain.

The current LRN-001 contract restricts the estimator objective to T1 organic evidence and allows specified weaker uses of T2–T4 with declared provenance. EVL-005 keeps simulator/benchmark evidence outside organic gates. The existing T1/T5 inconsistency remains pending disposition.

Therefore, lab results can populate research memory and descriptive knowledge, and support explicitly permitted weak-signal work. Turning them into an authoritative learned checkpoint requires a scoped admission decision, the relevant organic evaluation and graduation. Do not change a label to make the initial corpus pass.

## 7. Pin knowledge to conditions, then qualify transfer

A snapshot needs a compatibility matrix covering **harness/version + adapter/protocol + task/context scope + deployment/revision + tools/config + feature/verifier/policy versions**. Local-model evidence also needs the relevant hardware and quantization conditions.

An immutable snapshot can contain multiple separately qualified profiles. This is stronger than declaring one global “best model.” A new harness version begins as unqualified for affected behavior until compatibility and task regression evidence support it.

Pin what is actually controllable. A provider may expose a moving alias without an immutable model revision. Record that uncertainty, the reported identity and observation window; apply freshness/requalification rules. A manifest cannot freeze an opaque provider backend.

Preserve a distinct fresh compatibility set for version upgrades. Diagnose which changed dimension could invalidate knowledge, and re-run the relevant conformance and task slices. Distribution checks compatibility before activation and retains approved fallback/rollback.

## 8. Bounded delivery slices

| Slice | Deliverable | Exit proof |
|---|---|---|
| Lab A: specification and simulated run | Frozen experiment/task/version contracts, one real-router synthetic run, complete accounting | Decisions, receipts and negative cases are inspectable; no quality/savings claim |
| Lab B: one real harness | Qualified isolation, exact-output capture, task verifier and fixed-deployment comparisons | Complete attributable outcomes with full costs and declared limitations |
| Lab C: second harness and context diversity | Same task contract, separately qualified adapter/profile and expanded matrix | Cross-harness system comparison; no unsupported transfer claim |
| Lab D: K0 candidate snapshot | Descriptive capability/evidence package and compatibility manifest | Reproducible derivation, no leakage, explicit provenance and research/shadow status |
| Lab E: qualified learned checkpoint | Admitted learning data, independent later evaluation and release packet | Existing evidence/graduation gates pass for the named cohort |

Lab A/B extend P1/P2 in the product roadmap; Lab C aligns with the second-harness work; Lab D can precede fleet deployment. Lab E remains gated by the learning/evaluation requirements. No thousands-laptop rollout is necessary to start collecting controlled evidence.

Do not build a general simulation platform before proving one complete task-to-evidence-to-K0 path. Real payload execution retains the open custody/erasure, exact-close, verifier separation and concrete harness-profile prerequisites. Paid execution needs a finite approved budget.

## 9. Where RSI enters

The lab first evaluates routing policies using a fixed, versioned experiment process. Later, an improver can propose better failure grouping, candidate generation, graph queries or experiment selection.

The recursive comparison asks whether a revised improver finds more durable routing benefit for the same total budget. It cannot win by selecting only easier evaluation tasks, rewriting protected expected outcomes or hiding failed experiments. Keep independent confirmation and include all search, model, evaluation and reviewer costs.

Generating more experiments is not the outcome. Producing a better qualified checkpoint, and demonstrating that it helps later developer work, is the outcome.

## 10. Disposition and current status

This proposal adds a concrete route from the existing MEM/evaluation foundation to initial knowledge. It changes no runtime, ADR decision text, maturity, evidence eligibility or release authority.

Before implementation, dispose of the experiment identity/evidence contract and first harness profile. Before using K0 for learned authority, resolve the relevant LRN/EVL admission conflicts. Keep the implementation heartbeat paused until a bounded restart is directed.

Related plans: [product roadmap](../reports/adrl-product-roadmap-2026-09-08.md), [MEM/context architecture](adrl-context-graph-memory-proposal-2026-09-08.md), [existing engineering roadmap](../reports/adrl-implementation-roadmap-2026-09-07.md).
