# ADRL: show the routing, then earn the improvement

**Latest direction, 8 September 2026: planning first.** The user requested the target adaptive routing/RSI architecture before further implementation. The [blueprint](adrl-adaptive-routing-rsi-blueprint-2026-09-08.md) is ready for disposition. Scheduled implementation is paused; W7.0a corrections and W3 custody work are held. Earlier findings and sequencing proposals below remain dated context, not authority to resume. No runtime or grade changes.

8 September 2026. Current implementation review and offline demonstration.

**ADRL already makes routing decisions in code. Our recent waves have mainly strengthened execution and evidence; they have not yet shown that ADRL chooses models well on real coding work.** The executive deck blurred that distinction. The sequence also put the first visible routing comparison too far behind infrastructure work. We are correcting that sequence.

The product objective remains: let different coding tools use a common engine that chooses an appropriate permitted model, responds when work gets stuck, and changes its routing policy when reliable outcomes show a better choice. A harness is the coding tool the developer uses; a model is the engine doing the reasoning. ADRL should sit between them on supported model paths.

## What we actually ran

We invoked the existing `Router`, `CascadeController`, append-only ledger and rule-health calculation. The runtime source and configuration were unchanged across all 316 inputs in the latest verified build.

- **24 task prompts**, covering mechanical edits, explanations, tests, features, debugging, concurrency, security, database changes, architecture, performance, vague requests and mixed instructions.
- **Five conditions per prompt:** ordinary; a previous edit failed; roughly 25,000 estimated context tokens; only local permitted; local and cheaper cloud permitted.
- **Two repetitions:** 240 routing evaluations, representing 120 distinct prompt/condition combinations. Repetition checks stability; it does not add new task diversity.
- **135 existing routing, cascade and learning tests passed.** The additional stress probes exposed two failed review hypotheses that those tests did not cover.
- **Zero model calls.** Requests, gate outcomes, tool observations and the small rule-health history were synthetic. No coding task was completed, no savings were measured and no live policy changed.

The interactive view displays these recorded outputs. Selecting a case changes the displayed trace; it does not call a model or execute JavaScript routing rules that imitate the backend.

## Three things “adaptive” means here

### 1. Choose differently for the task in front of us

An ordinary typo request selected **Local**. A concurrency request selected **Frontier**, the strongest configured tier. The same typo with a previous failed edit selected **Frontier**. That is task- and state-dependent routing under the current policy.

This implementation uses versioned heuristics, selected task features and a few recent-history signals. Its completion probabilities are configured estimates, not probabilities calibrated on our completed tasks. It is neither a trained production router nor a rich understanding of the entire task trajectory.

### 2. Change course while work is under way

In the cascade demonstration, a task started on **Local**. Repeated tool calls triggered a trouble signal. ADRL waited while parallel tool results were incomplete, then chose **Cheaper cloud** at the completed boundary and constructed a handoff. With an injected local-only privacy restriction, it stayed local and created no cloud handoff.

These are real controller outputs driven by invented observations. They establish that the switching mechanism operates on this fixture, not that a real model recovered the task. The broader system may have to stop when the permitted model cannot continue safely; the pinned demonstration does not establish local capability or test the complete safety pipeline.

### 3. Change the rule for future tasks

We populated a separate temporary ledger with 20 invented outcomes: 12 successful completions without escalation and eight task-capability failures. The existing rule-health calculation measured 60%, below the current 85% threshold, and withdrew the easy rule's authority. After explicitly refreshing that snapshot, the same typo request changed from **Local** to the configured uncertain-case fallback, **Frontier**. A local-only restriction still won.

This is the clearest small example of the intended course correction. It is also incomplete product integration: the running service currently computes rule health at construction; no recurring refresh is wired in. This demo invoked the refresh explicitly. It did not train a model, adopt a new policy artifact or make the invented events eligible for learning. The temporary ledger was removed after the run.

## The taxonomy, connected to the product

| Taxonomy bucket | Plain-language job | Connection to adaptive routing |
|---|---|---|
| FND: foundations | Preserve the product's boundaries | Shared core, harness independence and changes justified by evidence |
| SEM: semantics | Understand what kind of request this is | Distinguish a new decision from continuation, utility work and provider-specific state |
| TRU: trust | Establish who is asking and which destinations are trusted | A cheap model is not eligible just because it appears in a menu |
| SAF: safety | Decide where the data is allowed to go | Defines the set the router may choose from; learning cannot override it |
| **RTG: routing** | **Choose the model tier and explain why** | RTG-002 chooses; RTG-003 governs rules; RTG-004 checks local-first feasibility; RTG-006 handles uncertainty; RTG-009 defines relevant cost |
| **CAS: cascade** | **Respond when work gets stuck** | CAS-001 detects trouble; CAS-003 permits switching at an action boundary; CAS-004 transfers context; CAS-005 governs staying at the higher tier |
| MEM: memory and evidence | Remember what actually happened | Tie decisions, served identity, attempts and outcomes together without inventing missing evidence |
| EVL: evaluation | Determine whether a change helped | Compare against a real baseline and control rollout; passing software tests is not proof of routing benefit |
| LRN: learning | Propose a better future policy from suitable outcomes | LRN-003 contains offline estimator machinery; LRN-006 bounds uncertain predictions; LRN-007 prevents self-promotion |
| OPS: operations | Make the above observable and recoverable | Versions, diagnostics, failures and rollback must remain understandable |

The product loop is **understand → restrict → choose → act and recover → record → evaluate → revise**. RTG and CAS deliver the visible routing behaviour. MEM, EVL and LRN make improvement defensible. Safety and trust constrain every iteration.

## What the stress run revealed

| Finding | Observed behaviour | What it means |
|---|---|---|
| Mixed requests can be under-classified | “Rename a variable and redesign the concurrency algorithm…” selected Local | The first matching easy verb hid the complex work. This violates the prepared conservative-classification hypothesis; we have not measured whether a particular local model would fail. |
| An explanation can mask an implementation request | “Explain the race condition and implement a fix…” selected Local, even with a prior failed edit | The explanation classification fed a read-only lookup rule despite the request also asking for a fix. |
| Equivalent wording can change the route | “Fix the typo…” selected Local; “Correct a misspelling…” selected Frontier | The current rules are sensitive to vocabulary. Route differences need justification beyond wording. |
| The middle tier is not earning a normal role in this sample | Ordinary choices were 9 Local, 0 Cheaper cloud and 15 Frontier | With no advisor configured in this driver, ambiguous requests use Frontier. Cheaper cloud appeared in restricted-set and cascade cases. This is a diagnostic, not a representative traffic share or proof the middle tier should win. |
| Restrictions held at the component boundary | No selected tier fell outside the supplied permitted set; local-only remained local; repeated outputs were stable | Useful mechanism evidence. Gates were supplied by the fixture, so this does not prove scanning, attestation, durable pins or provider dispatch. |
| Outcome-driven demotion needs service wiring | Explicit snapshot refresh changed the route; no periodic refresh was found | W3 records alone will not make the router adapt. A deliberate, tested bridge from admissible outcomes to rule health is needed. |

Two review hypotheses failed; **240 evaluations should not be described as 240 correct decisions**. The existing tests pass, and the expanded behavioural probes expose gaps. That is exactly why task-type testing must happen early.

## How the waves should connect, and the sequencing correction

| Work | Routing question it must answer | Visible proof |
|---|---|---|
| **W7.0 diagnostic, brought forward now** | Does the router react sensibly to varied tasks, failures and restrictions? | This trace explorer and the failed-case list; next, before/after evidence for bounded corrections |
| **W3: trustworthy task output** | Which exact code and attempt are we judging? | A finished attempt linked to the exact output checked; launch/recovery alone is insufficient |
| **W4: trustworthy judgement** | Did that attempt actually solve the task? | A verifier that rejects plausible wrong fixes on fresh cases |
| **W6: controlled model path** | Did the permitted model really receive the request, with reliable recovery? | A trace from request to intended and reported destination, with restrictions and rollback demonstrated |
| **W7: real routing comparison** | Is this policy better than always using one permitted model? | Matched starting tasks executed independently under fixed-model and adaptive policies; quality, all-attempt cost, time and repairs |
| **W5 / W8A: additional harnesses** | Does the shared behaviour survive another coding tool or protocol? | The same relevant decision/evidence checks through each named integration |
| **W9: learned routing** | Can outcome-trained choices improve on the simple policy? | Fresh comparative evidence, uncertainty handling and a narrowly approved rollout |
| **W10 / W12: improvement automation / RSI** | Can we propose changes, then improve how we find worthwhile changes? | Independently assessed proposals; later, better accepted outcomes per total evaluation cost |

The earlier roadmap made completed W5 a dependency of W7. That is too broad for the first one-harness routing experiment. **Offline diagnostics can run immediately. A bounded real experiment needs the relevant W3/W4/W6 scope for its named harness and workload; it need not wait for full second-harness qualification.** Cross-harness product claims still need W5/W8A. This narrows scheduling dependencies without waiving evidence or safety requirements.

W3 remains unfinished and necessary for reliable exact-output attribution. We are preserving that work, while changing the immediate priority to the newly observed routing defects. The [next packet](waves/routing-decision-quality.md) and [execution state](research/adrl-execution-state.json) capture that correction.

## What you should expect to see next

1. **Before/after routing behaviour:** mixed instructions no longer win easy-case authority merely because an easy verb appears first. Include fresh paraphrases and negative cases, not only the examples that exposed the problem. Record the policy/feature version and every changed route.
2. **A complete request-to-dispatch rehearsal:** use the actual router and controller behind the Messages API with a synthetic endpoint. Show chosen versus dispatched tier, rather than a fixed-router test double. This can proceed offline. It still will not measure model quality.
3. **One bounded real coding comparison:** start with named repository copies and narrow task families such as mechanical edits, parser fixes and small features. Freeze the task starting state and verifier. Compare separately executed fixed-model and adaptive arms. Show the selected model, actual outcome, extra attempts, time and accounted cost together. Access, destinations and run budget must be concrete before model calls; existing subscription observation is not evidence of a working routing integration.
4. **One evidence-driven course correction:** admit qualified outcomes, refresh rule health under an explicit versioned contract, repeat a previously tested task family on fresh examples, and show the changed decision and its consequence. Then decide whether a learned estimator is warranted.

RSI is not a prerequisite to useful adaptive routing. First the product must make sensible decisions, observe consequences and support a measured change. Improving the improvement method comes after that loop works.

## Maturity and evidence

No architectural status or maturity grade is promoted here. This adds scoped offline evidence and identifies new limitations. The historical 895-test full-build result remains valid for the unchanged runtime; this turn ran the smaller 135-test set and the separate decision probes. An implementation can become better understood while its readiness assessment becomes more cautious.

The first demonstration invocation failed because the research driver omitted the event schema argument. The driver was corrected and then completed; no runtime repair was involved. The stress input file was frozen before the matrix run. All current findings and raw traces remain available below.

- [Raw results, feature snapshots and decision contexts](research/routing-demonstration-2026-09-08/results.json)
- [Frozen task prompts and review hypotheses](research/routing-demonstration-2026-09-08/stress-cases.json)
- [Runnable demonstration](research/routing-demonstration-2026-09-08/run_demo.py)
- [Run summary](research/routing-demonstration-2026-09-08/run.log) and [135-test output](research/routing-demonstration-2026-09-08/targeted-tests.log)
- [Unchanged runtime baseline](research/routing-demonstration-2026-09-08/runtime-baseline.json)
- [Router implementation](../../adrl-core/src/adrl/routing/router.py), [feature extraction](../../adrl-core/src/adrl/routing/features.py), [rule health](../../adrl-core/src/adrl/routing/rule_health.py), [cascade controller](../../adrl-core/src/adrl/cascade/controller.py), [service composition](../../adrl-core/src/adrl/app.py)

To repeat the demonstration from the current checkout:

```bash
/Users/arunmenon/projects/adrl-core/.venv/bin/python /Users/arunmenon/projects/adrl-world-class/reports/research/routing-demonstration-2026-09-08/run_demo.py
```

This uses the current configuration and checks it against the recorded 316-input baseline. After a runtime correction, preserve this baseline and create a versioned comparison driver/result rather than overwriting the original finding.
