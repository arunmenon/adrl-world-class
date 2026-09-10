# ADRL implementation roadmap: a useful product that can course-correct

**Product roadmap overlay, 2026-09-08:** the [startup plan](adrl-product-roadmap-2026-09-08.md) proposes customer/value gates governing which engineering packets earn priority. It includes request-plus-context routing and a [MEM decision-memory graph candidate](../design/adrl-context-graph-memory-proposal-2026-09-08.md). This is planning, not restart authorization. All existing evidence, behavior and exposure gates remain pending their explicit dispositions; scheduled execution stays paused.

**Latest direction, 8 September 2026: planning first.** The user requested the target adaptive routing/RSI architecture before further implementation. The [blueprint](adrl-adaptive-routing-rsi-blueprint-2026-09-08.md) is ready for disposition. Scheduled implementation is paused; W7.0a corrections and W3 custody work are held. Earlier findings and sequencing proposals below remain dated context, not authority to resume. No runtime or grade changes.

## Scheduling amendment, 8 September 2026: show routing earlier

The user's task-type challenge exposed two mixed-intent routing defects in an offline diagnostic. [Routing in action](adrl-routing-in-action-2026-09-08.md) is now the product-facing progress account. W7.0 diagnostic work can run before full W3 completion: it exercises decision logic with synthetic inputs and confers no task-quality or live-exposure evidence. [W7.0a](waves/routing-decision-quality.md), the bounded routing correction, is the immediate priority. W3.2b2e remains unfinished and deferred, with all its custody and exact-output requirements preserved.

The first real one-harness routing comparison depends on the applicable W3/W4/W6 scope, named destinations, budget, verifier and rollback. Full W5 qualification remains required for second-harness claims but is no longer a blanket scheduling prerequisite for that first comparison. The original W7 entry dependency was “W4/W5/W6; model capability admission, hardware capacity, account access and spending ceilings recorded.” This amendment narrows the harness scope only; it does not waive independence, formal evaluation or graduation gates. No wave or grade is completed by this scheduling change.


**Execution context, 2026-09-07:** the user subsequently authorized triggering the waves.
The [journey](adrl-implementation-journey.md) and [execution state](research/adrl-execution-state.json)
now track bounded local work and an hourly continuation. The proposed plan and its original
validation below are retained as planning history; authorization does not waive its gates.

7 September 2026 | Plan v1, proposed for review | Planning only; no new implementation or experiment authorized by this document

**Build a dependable shared product first, then give it increasing ability to improve within tested boundaries.** The sequence is: know what happened, check whether it worked, prove portability, enforce declared restrictions, measure routing alternatives, release a supported product, and only then expand learning and automation.

The architecture should be stable in its promises and adaptable in its methods. Privacy boundaries, truthful evidence and release authority are promises. Starting locally, a particular routing algorithm, transcript handoff, an escalation threshold and the choice of the next harness are hypotheses that evidence can change.

This is the current forward plan. Earlier reports remain historical evidence. The existing wave numbers 3–8 are preserved; wave 8 is split into protocol admission and release qualification. The recent verifier-comparison work is an early part of wave 4, not completion of that wave. W0 below is a short program reset, not a restart of implementation.

## 1. Read this plan in three passes

- For the direction, read sections 2–5 and the [wave map](#7-wave-map-dependencies-and-planning-horizon).
- For execution, read the [detailed wave contracts](#8-detailed-wave-contracts) and use the [wave execution packet](adrl-wave-execution-template.md).
- For architectural decisions and oversight, start with the [decision queue](#9-decisions-to-settle-before-the-dependent-implementation), then sections 10–13 and the complete ADR ownership map in appendix A.

Every future wave has an entry condition, tangible deliverables, prohibited shortcuts, evidence needed to exit, a recovery path and accountable roles. A date, code merge or green test count never substitutes for an exit condition.

## 2. Where ADRL actually stands

The latest [implementation evidence](adrl-improvement-experiment-2026-09-07.md) records 549 passing tests, 256 inventoried persisted fields and public API preview 4. The tested package's 13 source/document changes match their recorded hashes at planning time. This planning pass does not rerun the runtime suite or claim a new test result.

| Area | Implemented or observed | What that does not establish |
|---|---|---|
| Shared product foundation | Messages profile, Claude adapter, authenticated local session/event/timeline services | Stable public API, remote tenancy or another protocol |
| Claude observation | One real subscription pilot; 18 reconciled tool events | Interception of model calls, gateway privacy enforcement or routing savings |
| Independent verification | Pinned operator checks on separate snapshots, encrypted session receipts | Automatic attribution to the exact task-close output or verifier accuracy across tasks |
| Improvement comparison | Versioned local proposals, fixed cases, two verifier versions and encrypted trial history | Automatic proposal generation, adoption, independent holdouts or RSI |
| First comparison | Baseline 4/7 and candidate 7/7 correct classifications; two agreeing repeats | Population accuracy: these were seven visible variants of one task, authored with the candidate |
| Routing, pins, ledger and learning components | Substantial D1/D2 mechanisms and simulated/fault tests | A graduated live router, complete egress coverage, trained policy quality or production operations |

There is documentation drift. For example, later service documentation describes implemented handlers while an older README paragraph still says they return 501. A known-gap entry says unknown gateway models count as healthy; the actual health reader returns unknown, but the feasibility policy can retain unknown members. W0 reconciles these distinctions against code and tests instead of blindly converting old prose into a backlog.

## 3. The product destination and release boundaries

A developer should be able to choose a supported harness, connect a registered repository, run a diagnostic, understand the effective policy, and inspect what ADRL observed, prevented, chose and verified. Changing harnesses should preserve policy and evidence semantics.

The first supported product is **local, single-user and single-process**. Managed team service is a later product boundary. The local release must still support realistic concurrent sessions, restart, upgrades, erasure and explicit unsupported states. “Local” is not synonymous with “safe against code running as the same OS user.”

| Release boundary | Value delivered | Required evidence | Claims excluded |
|---|---|---|---|
| Developer preview, after W3–W5 | Reliable task records and independent checks through Claude Code and OpenCode | Common contracts, real task traces and declared observation gaps | Full model control, savings, enterprise identity |
| Local control pilot, after W6 | Enforced declared model paths, durable restrictions and understandable audit evidence | Active denial probes, fault/restart tests, named real integration and rollback | Whole-machine egress control or general routing benefit |
| Stable local product, after W8B | Installable, supported contract and version matrix across admitted harnesses/protocols | Two harnesses and two protocols actually exercised, lifecycle qualification and reviewed release scope | Universal harness compatibility or automatic learning |
| Optional learned routing, after W9 | An approved policy improves a named eligible workload slice | Admitted data, fresh comparisons, calibrated abstention and limited rollout | Gains on excluded/private/unseen populations |
| Optional managed/team product, after W11 | Organization identity, policy distribution, isolation and operations | Separate tenancy, key, concurrency and incident evidence | Inherited enterprise readiness from the local release |

Claude plus OpenCode establishes harness reuse on Messages. The intended stable matrix adds Codex on Responses, producing three named integrations and two protocol families. A functioning endpoint alone does not meet this gate. Each support claim is a tuple: **harness version + profile version + transport + deployment + integration mode + tested capabilities**.

If routing never beats a simpler allowed policy, release the useful control/evidence product with that policy and an honest scope. Learning and RSI are not prerequisites for its usefulness. Changing the existing maturity rules to express that distinction requires the explicit disposition described in DQ4 below; this plan does not silently rewrite them.

## 4. Architecture that supports many harnesses

```text
Claude Code adapter       OpenCode adapter       Codex adapter
        |                        |                     |
        +------ Product contracts: identity, events, evidence ------+
        |                        |                     |
   Messages profile        Messages profile       Responses profile
        +------------------------+---------------------+
                                 |
                  Shared policy and routing engine
                   restrictions -> choice -> dispatch
                                 |
                    Approved gateway/deployments
                                 |
                   Evidence and outcome lifecycle
                                 |
             Offline proposals -> evaluation -> release review
```

Adapters own launch/configuration, identity mapping and event translation. Profiles own native request/state/stream interpretation and admitted transformations. The shared engine owns restrictions, routing, provenance and recovery. Provider protocols remain native; we do not force opaque reasoning or tool state into a universal text transcript.

The roadmap keeps three API concerns separate:

| Surface | Current position | Planned completion and boundary |
|---|---|---|
| Native model paths | Messages implemented; Responses unregistered | W6/W8A admit exact methods, state and transports; unknown paths cannot escape a controlled listener |
| Product API | Preview 4 discovery, binding, observations, timeline and decisions | W3/W5 add task/snapshot lifecycle and adapter conformance; W8B freezes compatibility only after real reuse |
| Improvement operations | Local Python contracts and `improve` CLI | W10 may expose proposal/evaluation operations with separate roles; ordinary harness events never become authoritative verification or release requests |

New endpoint names, SDK languages and schema details are chosen in the wave design packet. An HTTP contract and executable examples come first; a small helper is added where an actual adapter needs it. No separate policy engine per harness. Capability discovery must distinguish supported-by-code, exercised-in-a-fixture and exercised-in-a-real-deployment.

## 5. Guardrails that apply to every wave

| Guardrail | Required behavior | Stop or recovery condition |
|---|---|---|
| Restrictions precede optimization | A route must satisfy authenticated policy, durable pins and deployment capabilities | Any forbidden dispatch stops the affected controlled population; quarantine and preserve evidence |
| Preserve native semantics | Preserve bytes, tool IDs, errors, cancellation and opaque state except explicitly approved profile transformations | Undeclared transformation, lost state or duplicated side effect blocks admission |
| Separate observation from enforcement | A hook reports what it saw; a successful tool event is not task success | Missing visibility is reported as unknown or unsupported, never advertised as protection |
| Preserve evidence | Append corrections, version inputs and outcomes, make erasure and backup behavior explicit | Missing, conflicting or corrupted authoritative evidence cannot be repaired by inventing success |
| Preserve evaluator independence | Candidate code cannot edit release tests, expected outcomes, admission rules or signing authority | Contamination invalidates affected evidence; obtain fresh cases and investigate access |
| Bound execution and spending | Declare scope, attempts, model calls, input/output limits, timeout, disk and spend ceilings before a run | Exhaustion or missing authority stops that run; no unlimited repair loop |
| Keep synthetic evidence distinct | Origin, verification quality and eligibility are separately visible | No silent promotion of pilot or curated records into training |
| Make rollback preserve restrictions | Revert code/config/artifacts without deleting pins, erasure tombstones or audit history | If safe backward compatibility is impossible, stop affected dispatch rather than restoring unsafe state |
| Change decisions explicitly | Reproduce, classify, disposition and update owning ADRs before completing the change | A result that challenges the contract triggers a scoped replan; tests cannot quietly redefine it |
| Limit claims to tested scope | Report version, workload, denominator, exclusions and uncertainties | A failing or untested slice stays unsupported even if a fleet average is good |

The plan does not freeze every current policy. In particular, scanner-failure availability, shadow ceilings and tolerated receipt uncertainty need an explicit workload-specific decision. Existing permissive behavior cannot be sold as strict privacy enforcement while that decision is unresolved.

A failed safety gate blocks exposure to that risk, not all unrelated engineering. Routine fixes, local checks and register synchronization can continue within approved scope. Human decisions are concentrated at policy changes, evidence admission, spending/access changes and release/graduation boundaries; they are not requested again after every reversible edit.

## 6. Evidence standards and quantitative gates

**Different gates answer different questions.** Implementation conformance can be established on named fixtures. Broad quality, savings and learned-policy authority require representative evidence and uncertainty estimates.

All numbers below are **proposed starting budgets or targets**, not measured achievements or automatic maturity thresholds. The wave packet must freeze actual values before measuring the release candidate. A missing value means the relevant release gate is not ready.

| Gate | Initial planning rule |
|---|---|
| Critical behavior | Zero violations in the named adversarial/conformance suite: no forbidden dispatch, accepted forged authority, cross-session leak, duplicate external effect or erasure resurrection. Zero observed failures is not a population guarantee |
| Event and snapshot accounting | Every diagnostic attempt has a terminal accounted state, or an explicit interruption/missing-evidence state; never disappear failed attempts from the denominator |
| Verifier calibration, W4 | Start with 30 distinct diagnostic code states across at least 3 task families and 2 repositories, including correct, broken and unavailable environments; repeat checks twice. These sizes debug measurement and do not establish a production error rate |
| Real workflow coverage, W4/W5 | Initial 20 completed/attempted organic tasks across the declared scope, retaining incomplete attempts; recruit another user before making a multi-user representativeness claim |
| Routing diagnosis, W7 | Start with 30 development tasks across narrow fixes, tests and refactors; three policies imply 90 executions before repeats. Extend according to observed uncertainty and budget; keep a fresh confirmation set |
| Quality gate | Predeclare a meaningful maximum allowed quality loss, confidence level and primary endpoint. Require the confidence bound to satisfy that margin on the admitted population; otherwise report insufficient evidence |
| Economic gate | Compare end-to-end cost at matched acceptable quality, including retries, repair, verification, model switching and inference infrastructure. Require a predeclared worthwhile improvement after uncertainty, not merely a lower point estimate |
| Release usability, W5/W8B | Initial target: setup and a diagnostic within 15 minutes once credentials, models and repository policy are prepared. Measure failures and assistance; model downloads are reported separately |
| Operational pilot, W8B | Proposed minimum: two weeks and 100 eligible task attempts across the supported matrix, both required; extend for missing cases or uncertainty. This is an operations floor, not proof of routing superiority |
| Rollback | Proposed local target: stop admitting affected work within 60 seconds of a triggered kill switch; restore a compatible approved service within 10 minutes. Prove those times or revise the service promise before release |

For quality, report false acceptance of bad code, false rejection of good code, environmental uncertainty, repeat disagreement, human repair and later reverts separately. Repeat agreement alone is not verifier precision. Keep all-attempt service reliability separate from model capability conditional on a healthy compatible run.

For experiments, group related tasks/sessions/repositories appropriately, prevent siblings crossing development and holdout boundaries, and version changes to models or harnesses. Choose the primary comparison and analysis before looking at final results; define how multiple candidates and interim looks will be handled. Do not repeatedly inspect a holdout and continue calling it untouched. Obtain statistical review before a material efficacy claim. The existing EVL evidence rules still apply until explicitly amended.

Use data minimization: preserve only the authorized task description, output, checks and environment references required for the question. A referenced file is not permission to upload it to a cloud proposer. Establish OS-level separation before promising a protected holdout; the current Seatbelt profile does not provide that boundary.

### 6A. How RSI grows across the waves

For ADRL, the proposed recursive element means improving the machinery that finds and tests future improvements. A better routing rule improves the product. A better proposer or experiment selector may improve the product's ability to improve. The second claim needs its own evidence; repeating an unchanged proposal loop does not establish it.

```text
Tasks -> trusted evidence -> proposed change -> independent test -> review
  ^                                                                 |
  +---------------------- approved, bounded change ------------------+

Later: compare changes to the proposer or experiment selector itself,
       using independently assessed downstream improvements.
```

| Waves | Improvement capability being built | What can change | Honest description |
|---|---|---|---|
| W0, W3 | Reproducible state and exact task-output evidence | Evidence plumbing and capture contracts | Foundations for improvement |
| W4 | Test whether a proposed verifier is actually better | Development verifier candidates, tested against independently owned expectations | Human-led, measured course correction; the current curated experiment is an early mechanism exercise |
| W5, W6, W8A, W8B | Establish where a change transfers and how to release/recover | Adapter/profile implementations and controlled rollout within reviewed policy | Portability and release discipline that an improvement loop must obey |
| W7 | Compare routing/cascade alternatives on actual tasks | Starting model policy, bounded escalation, handoff or allowed downshift | Evidence-led policy improvement; no claim of improving the proposer |
| W9 | Use approved outcomes to learn a better permitted choice | Versioned routing artifacts with abstention | Gated learning; underlying coding-model weight training is not required |
| W10 | Generate and evaluate bounded proposals automatically | Candidate tests, diagnostics and allowed configuration/code changes | Automated proposal loop with independent evaluation and human adoption |
| W11 | Maintain the same boundaries across organizations and integrations | Admitted team infrastructure and adapter scope | A scope extension, not automatically a step toward greater intelligence |
| W12 | Compare changes to the improvement method | Proposer, failure summarizer or experiment-selection method | An explicit test of the recursive element |

Concrete example: the current verifier missed three prepared defects. Today, a human-directed engineering process added tests and compared the candidate. W4 checks whether that benefit survives fresh independently reviewed cases. W10 could generate such a test proposal from an authorized failure packet. W12 could compare two proposal methods to determine which finds more independently accepted, durable improvements for the same total evaluation budget. Proposal count and visible-test score are insufficient; include rejected proposals, search cost and later regressions.

There are two evaluation levels when the verifier is itself a candidate. The proposed verifier checks task code. A separate assessment checks whether that verifier accepts correct code, rejects defects and preserves uncertainty. The candidate may change the former; it cannot change the latter's release cases, expected answers or acceptance rules. A proposal to alter that assessment becomes separately owned work under its own unchanged external test.

The release boundary remains explicit throughout: a proposer cannot change privacy restrictions, its grading criteria, deployment credentials or graduation authority. A reviewed improvement can feed the next cycle without granting self-deployment. W12 is optional research; trustworthy, useful adaptive behavior can arrive before any demonstrated recursive gain.

### 6B. How ADR maturity can progress

**Maturity describes how well a particular promise has been demonstrated, not how many files or tests exist.** Architectural status (Accepted/Proposed) remains separate. The current build has substantial scoped D1/D2 evidence and a limited live observation exercise; historical D3/D4 statements in older material are not inherited automatically. W0 audits the current evidence per behavior before publishing exact counts.

| Level | Plain-language meaning | Evidence required in this program |
|---|---|---|
| D0: Design | We have specified the promise | A decision and scoped contract; no working-behavior claim |
| D1: Code | The mechanism exists | An attributable implementation; qualification remains incomplete |
| D2: Tested | The behavior survives the required tests | Unit/integration/fault and relevant adversarial evidence for the named scope |
| D3: Shadow | It behaves as expected on real work while its proposed decisions do not control that work | Declared organic window, versions, coverage/exclusions, no relevant blocker and the required review |
| D4: Pilot | It has explicit approval to affect a restricted population | Applicable evaluation report, reviewed exposure boundary and exercised rollback; current routing graduation requirements still apply |
| D5: Graduated | It is approved for continued supported use in that population and configuration | Completed pilot evidence, required owner/security sign-off and operating/recovery controls |

These are ordinal evidence levels, not percentages. Do not average them into an ADRL score or interpret a level as a probability of correctness. The weakest unmet mandatory release gate blocks that release; an unrelated low-maturity optional research decision need not block it. Some ADRs may be deferred or replaced rather than pushed to D5.

The following is a **conditional evidence trajectory**, not an approved promotion schedule. An arrow requires each intervening gate and review. A named family includes only its tested clauses; broad row labels do not promote every ADR in a bucket.

| Wave | Main promises whose evidence improves | Plausible progression if its gates pass |
|---|---|---|
| W0 | FND-005, EVL-007/009: truthful scope and review process | Establish an accurate baseline; no automatic increase |
| W3–W4 | MEM-002/003: task/output/outcome integrity; EVL-004/006: verifier/evaluation quality | D1 or existing partial D2 -> complete scoped D2; D3 only after the required real-work window and review |
| W5 | SEM-002/007, TRU-001: adapter identity and shared contract | OpenCode's new scope D0/D1 -> D2; then eligible for scoped D3 evidence, without inheriting Claude's grade |
| W6 | SAF-002/008/009, TRU-002/003, OPS recovery: restrictions, dispatch and custody | Strengthen D2, then seek D3 and narrowly authorized D4 for qualified behavior; resolve DQ4 for non-routing qualification |
| W7 | RTG-004/007/009 and CAS-004/005: worthwhile routing and recovery choices | D2 -> D3 -> eligible D4 only if comparative evidence, scope, rollback and review justify exposure |
| W8A | SEM-007 and state-related SEM/CAS clauses: native Responses behavior | New protocol scope D0/D1 -> D2 -> D3; real captures alone do not complete a shadow window |
| W8B | The mandatory local-release subset across FND/SEM/SAF/TRU/MEM/OPS | Complete applicable D3/D4 evidence and seek D5 for the qualified release subset; not all 77 decisions |
| W9 | LRN-003/004/006 and supporting EVL rules: learned choice, no leakage, abstention | Unproved learner scope D0/D1 -> D2 -> D3 -> constrained D4; later D5 needs its own completed pilot |
| W10 | LRN-005/007, EVL-006: trustworthy improvement proposals and adoption control | New automated-proposer scope D0/D1 -> D2; then appropriate real-work/pilot evidence after DQ4 disposition |
| W11 | TRU-001, OPS-001/002/004 and shared-state clauses: team isolation and operations | Team scope starts with its own evidence, progresses through D2/D3/D4 and only later seeks D5; local D5 does not transfer |
| W12 | LRN/EVL/FND clauses governing comparison of improvement methods | D0 hypothesis -> D1 implementation -> D2 tested experiment mechanism; demonstrated recursive benefit and operational graduation remain separate claims |

A concrete example is **MEM-003, verification enriches history**. Existing receipt tests support scoped D2. W3 adds evidence that a later workspace edit cannot change what output was checked. W4 challenges correctness and uncertainty on fresh cases. A declared real-work window can then support D3 review for the qualified verification behavior. Limited adoption with recovery can support D4, and a completed supported-use pilot can support D5 if the applicable rules are satisfied. Each step links to the exact verifier/capture versions and covered task/harness population.

An ADR's broad promise can remain only partially proven even when one application reaches a higher level. Record the headline as partial/scoped and list unresolved clauses; do not transfer the strongest subclaim's grade to the whole decision. A new version or protocol receives an impact review: retain reusable evidence for unchanged behavior and requalify changed assumptions. A regression can suspend or lower the applicable current claim while preserving the previous version's historical evidence.

**Maturity record proposed for each behavior:** ADR ID and clause; implementation/config/profile/adapter versions; current level; covered population; evidence links; missing gates; next target; approving owner/reviewer; review date; invalidation/rollback triggers. The wave closure report should show before -> evidence added -> approved after, including unchanged/deferred/demoted entries. W0 will define the report and audit counts; it is not a dashboard already implemented by this clarification.

The program summary should show the D0–D5 distribution for the declared release subset, outstanding mandatory blockers, untested scopes and evidence freshness. Never use a mean across all 77 decisions. The aim is dependable product promises, not a cosmetically rising score.

**Existing policy issue:** EVL-007's current generic D4 ladder calls for routing-economic gains. DQ4 proposes a feature-appropriate qualification path for verification, integration and operations while retaining review and recovery. The table above makes that dependency visible; this clarification neither amends EVL-007 nor grants non-routing maturity by analogy.

## 7. Wave map, dependencies and planning horizon

Effort assumes one primary engineer with agent assistance, a product owner available for decisions, and scheduled independent evaluation/security review. These are engineering ranges, not elapsed-time promises. Reviewer availability, user recruitment, observation windows and vendor access can extend the calendar. A second engineer can overlap independent work; it cannot eliminate evidence gates.

| Wave | Outcome | Entry dependencies | Engineering range |
|---|---|---|---|
| W0 | Reproducible baseline and executable wave contracts | Current implementation | 2–3 days |
| W3 | Exact task-close output binding | W0 | 1–2 weeks |
| W4 | Trustworthy outcomes on fresh, varied tasks | W3 | 2–3 weeks, plus collection |
| W5 | OpenCode reuse and adapter kit | W3; use W4 evidence as it becomes available | 1–2 weeks |
| W6 | Controlled Messages path and recovery | W0 for offline fixes; W4/W5 before the full live matrix | 3–5 weeks |
| W7 | Measured routing/cascade choices | Relevant W3/W4/W6 for first harness; W5 for second-harness scope; funded execution inputs | 3–5 weeks, plus confirmation |
| W8A | Codex/Responses admission | W0 spike; W3/W5 contracts and W6 controls for live admission | 3–5 weeks after spike |
| W8B | Supported stable local product | W3–W6, W8A; W7 scope disposition | 2–4 weeks, plus pilot window |
| W9 | Learned routing earns narrowly scoped authority | W4/W6/W7; data and architecture gates | 4–8 weeks after suitable data exists |
| W10 | Bounded automated improvement proposals | W4 and W8B; separate evaluation access | 3–6 weeks |
| W11 | Managed team service and further harnesses | W8B plus demonstrated team demand | 6–12 weeks, separately staffed if possible |
| W12 | Test improvement of the improvement process | W10 plus sufficient independent improvement outcomes | 4–8 week research tranche; conditional |

W4 and W5 can overlap after W3. W6 offline hardening and the W8A compatibility spike can begin early, but neither may borrow unearned live admission. W9, W10 and W11 are separate branches after their prerequisites, not a requirement to finish all research before shipping. W12 depends on trustworthy improvement history, not a target month.

Allow roughly **4–8 weeks for a credible two-harness developer preview**, and **4–7 months of primary-engineer effort toward stable local scope**, with additional time possible for evidence collection and difficult protocol findings. Months 6–12 are a planning envelope for selected learning, automation or team work, not a promise that every branch will ship. The older two-to-three-week estimate concerned an initial integration pilot, not this complete product qualification.

## 8. Detailed wave contracts

### W0. Establish the baseline we will execute from

**Purpose:** make subsequent results attributable and turn this plan into small, reviewable work packets. Owner: implementation lead; review: product owner and evidence reviewer.

**Build:** preserve both repositories' uncommitted state in verified snapshots; produce build/config/dependency and evidence manifests; reconcile README, known gaps and capability declarations against code. Establish automated runs of the six required checks, data inventory, contract exports and ADR coverage. The current repository does not show a CI workflow, so portable local commands alone must not be described as a release pipeline. Create a risk/decision queue and assign the actual people for review roles. Prepare W3's packet and a time-boxed Responses state/transport spike.

**Guardrails:** preserve unrelated work, credentials and private artifacts; no model runs, installs, commits or publication merely to prepare the plan. Historical evidence retains its date and build. Development configuration is not a production inventory. An automated runner must not infer approval from a status field it can write itself.

**Exit evidence:** reproducible source snapshot; documented check results for the baseline used for implementation; current support matrix; each open blocker tied to an owner and wave; W3 acceptance/fault cases frozen before coding. Confirm which historical items are already fixed rather than duplicating them.

**Stop/recovery:** if the source differs from recorded evidence, preserve both, establish a new baseline and reassess affected tests. Missing reviewers block the associated graduation, not local implementation. No deployment rollback is needed because this wave changes no serving behavior.

**Owning decisions:** FND-005, SEM-007, EVL-007/009, OPS-001/003.

### W3. Tie verification to the exact completed task

**Purpose:** “the checks passed” must identify the code the agent actually left at a declared close boundary. Owner: product/evidence engineer; review: verifier owner.

**Entry:** W0 baseline and a trusted operator-controlled task lifecycle contract.

**Build:** separate task attempts from sessions; a session may contain several tasks and retries. Capture initial and terminal workspace manifests, task identity, parent attempt, closure source and times. Introduce an explicit close handshake that quiesces tracked writes or detects concurrent change. Capture a retained immutable snapshot; run the verifier on that snapshot, not whichever working tree exists later. Record dependencies, check artifacts, executable and configuration versions. Define close requested, snapshot captured, verification started/finished and incomplete/cancelled states without rewriting history. Distinguish process interruption from a failed task. Bound snapshot storage and define cleanup/erasure before bulk collection.

**Guardrails:** a harness's “done” event is a closure request, not trusted success. A timestamp or digest alone does not establish atomic capture. If quiescence cannot be established, describe a later operator capture and refuse exact-close attribution. Preserve child restrictions, exclude private content according to policy, reject symlink/path escapes and do not let closure fabricate route IDs. Existing receipts remain readable and ineligible for learning.

**Exit evidence:** original output A still verifies as A after the working tree becomes B; edits during capture are rejected or marked indeterminate; two tasks in one session stay distinct; duplicate/out-of-order close events, disconnect, restart, cancelled checks, missing files and erasure are accounted for. A real Claude task demonstrates the lifecycle under the named trusted local boundary.

**Stop/recovery:** any wrong-output attribution, erased payload recovery or unauthenticated closure authority blocks release. Disable automatic capture and retain explicitly scoped manual verification while repairing it. Never relabel a later snapshot as the original close.

**Owning decisions:** MEM-001/002/003/005/010, SEM-002/003/006/007, SAF-007, TRU-001, EVL-008.

### W4. Establish whether the verifier and outcomes deserve trust

**Purpose:** catch real defects without grading only the examples we designed the candidate to pass. Owner: evaluation lead; review: someone independent of the candidate author.

**Entry:** W3 snapshot attribution; approved repositories, artifact access and task definitions.

**Build:** a task catalog spanning narrow fixes, test changes and refactors across at least two repositories; development, selection and fresh confirmation partitions; correct implementations, deliberate faults and environment failures; human-written expected behavior before candidate execution. Run the initial diagnostic and organic coverage batches in section 6. Retain task repairs, reverts and disagreements. Reuse the existing proposal/comparison archive for synthetic experiments, and define a separate organic evidence contract before trying to ingest organic tasks. Reconcile evidence origin versus verification quality and training/evaluation eligibility through DQ1. Establish isolation suitable for any claimed protected evaluation.

**Guardrails:** the existing seven cases remain development fixtures. The assistant that generated a candidate cannot certify independent review of it. A frozen test set visible to the candidate is not a secret holdout. Disputed expected answers need adjudication; they are not silently revised to fit the candidate. Repeat runs do not multiply task diversity. No training admission yet.

**Exit evidence:** raw counts and error types by task family and repository; independently reviewed disagreements; calibrated failure/indeterminate semantics; a fresh comparison of the proposed eleven-test verifier; an evidence-eligibility proposal with validation cases. Demonstrate that “always pass,” “always fail,” test deletion and environment-error relabeling cannot win. Any accuracy promise needs an uncertainty bound appropriate to the requested risk, beyond the diagnostic batch.

**Stop/recovery:** contamination, ambiguous reference answers or false acceptances cause a targeted repair and fresh assessment. Keep the prior verifier with its documented limitations, or narrow the supported task family; do not hide inconvenient tasks. Preserve all failed candidates.

**Owning decisions:** MEM-002/003/004/010, LRN-001/004/005/007, EVL-002/004/005/006/009, SAF-007.

### W5. Prove the product can integrate with OpenCode

**Purpose:** show that a new harness needs an adapter rather than another ADRL implementation. Owner: integration engineer; review: core/API owner and a developer using the quickstart.

**Entry:** W3 task/evidence contract; named OpenCode version and credential path. W4's corpus can mature in parallel.

**Build:** an OpenCode connection/configuration adapter, workload/session mapping, tool/task/compaction event translation and the same task snapshot/verifier contract. Package schemas, reference events, fixtures, a contract test runner and diagnostics. Exercise simultaneous Claude and OpenCode sessions, credential expiry/renewal, restart, outbox retry, duplicate events and supported resume/child behavior. Unsupported child/resume cases must be rejected or explicitly unclaimed, not emulated by resetting identity.

OpenCode documents provider endpoint configuration and plugin events for tools and sessions. These establish integration entry points; they do not establish our adapter's completeness. Recheck behavior for the selected version. [Providers](https://opencode.ai/docs/providers/), [plugins](https://opencode.ai/docs/plugins/).

**Guardrails:** no duplicated pin, routing or outcome logic; harness identifiers alone confer no workload authority. Observation does not retroactively block a tool or prove complete network coverage. No silent event loss, cross-session reads, erasure resurrection or extra credential authority. Use provider credentials appropriate to this harness; do not transfer Claude subscription credentials into it.

**Exit evidence:** real tasks from both harnesses appear through one schema and service; the shared conformance suite passes; outbox replay yields identical acknowledgements; setup time and manual assistance are recorded against the 15-minute target. Publish coverage by integration mode. W5 establishes observation/evidence portability; full model-enforcement parity is qualified in W6.

**Stop/recovery:** if a shared field cannot express a genuine harness difference, revise the preview schema and both adapters together. Disable the unsupported feature or adapter version without discarding evidence. One working happy path does not close the wave.

**Owning decisions:** FND-001/002/005, SEM-001/002/006/007, TRU-001, MEM-001/003/006/010, OPS-005.

### W6. Make control and recovery dependable on Messages

**Purpose:** substantiate the product's model-path enforcement claim before testing routing savings. Owner: security/runtime engineer; review: security owner and gateway/operator owner.

**Entry:** W0 for offline fixes; W4 outcomes and W5 adapters for the completed live matrix. A real destination, access mode and bounded run budget must be named before live execution.

**Build in three slices:**

1. **Control boundary:** a dedicated controlled listener rejects missing/invalid identity, unsupported methods and unclassified paths. Legacy forwarding must be explicitly separated so removing headers cannot bypass policy. Decide and test repository ceilings in shadow mode, unknown/stale health eligibility, scanner failures, unsupported content and utility traffic. Configure deployed keys and signed inventory; refuse development opt-outs in released controlled mode.
2. **Continuity and custody:** test synthetic secrets in tool results, split content, compaction, restart, session resume and child return. Persist verifier-failure consumption so restart cannot re-arm old escalation. Restrict destinations before dispatch, keep pins across recovery, and test provider-bound thinking/state. Qualify sandbox access to snapshots, verifier inputs and credentials; do not run arbitrary untrusted repositories until their stronger isolation requirement is met.
3. **Dispatch and operations:** validate stream/error/cancellation preservation and the gateway's own retries after partial tool output. Reconcile intended versus reported deployment for streamed, non-streamed and fallback traffic. Test ledger/key failure, disk pressure, active denial probes, checkpoint loss, backup/restore and emergency shutdown. Demonstrate safe behavior when external anchoring is unavailable; an ordinary acknowledgement is not an independent integrity proof.

**Access course correction:** Anthropic now documents a base-URL-only gateway mode that can retain subscription login, while gateway credentials replace subscription billing. Add a bounded Claude-only compatibility spike, including required OAuth header forwarding. ADRL has not validated it; this supplies no access to other providers. Non-Claude routing is unsupported by Anthropic; use separately admitted access, preferably OpenCode, for those comparisons. [Official gateway guidance](https://code.claude.com/docs/en/llm-gateway).

**Guardrails:** never extract or repurpose subscription credentials for other providers. Do not switch off mandatory controls to make a model compatible. Missing served identity remains unknown; a gateway receipt is not proof of provider internal processing or retention. Claims cover named model paths, not tool/subprocess/telemetry traffic outside them. Unknown identity or a known pin cannot be made permissive by an outage or rollback.

**Exit evidence:** the negative-path matrix passes on named real integrations and controlled fixtures, with zero observed forbidden dispatches or duplicated external effects; each injected fault has an expected record and recovery result. Publish enforced/observed/outside-scope dimensions, receipt coverage, failure-policy table, active-probe output, backup restoration evidence and measured rollback. Review any permitted unscanned path separately before advertising its protection level.

**Stop/recovery:** block the affected controlled path, cancel future dispatch, preserve in-flight ambiguity and audit records, and restore a compatible approved version or remain stopped. A privacy failure is not repaired by sending the task directly to a cloud baseline. Observation-only availability may continue only with the agreed, visibly reduced scope.

**Owning decisions:** SAF-001–009, TRU-001/002/003, FND-001/004, SEM-004/005/006, CAS-001/003/004/006/007/009, OPS-001/002/003/004/005/006/007/008, MEM-006/010.

### W7. Find which routing choices are actually worth making

**Purpose:** compare permissible choices on completed tasks, including the cost of recovering when they fail. Owner: evaluation/routing engineer; review: evidence reviewer and product owner.

**Entry:** relevant W3/W4/W6 scope for the named harness and workload; W5 before second-harness claims. W7.0 offline diagnostics may precede those live/outcome gates. Model capability admission, hardware capacity, account access and spending ceilings are recorded before real execution. Resolve DQ1–DQ3 for any formal evaluation or graduation claim. Diagnostic runs may proceed with their explicit evidence restrictions.

**Build:** a repeatable branch runner from the same initial task state, isolated working copies, matched tools/dependencies and controlled side effects. Start with a fixed strong permitted deployment, fixed local deployment and the current heuristic. Add a deployable best-single-cloud comparator chosen on development data, and report the register's hindsight/repricing bound separately. Freeze model/deployment, effort, prices, baseline and verifier versions. Capture task success, repairs, all-attempt failures, usage/caching, time, local resource cost and human interventions.

Use the initial 30-task batch to debug comparisons, not to graduate. Then compare local-first versus direct-strong, bounded escalation versus restart, complete versus summarized handoff, and allowed downshifts at safe boundaries. Run one primary hypothesis per packet to avoid a combinatorial explosion. Include a simple deterministic rule as a serious candidate; complex learning must earn its cost.

**Guardrails:** policies may choose only eligible destinations. A hard privacy pin can make cloud comparators inapplicable; report a separate constrained stratum instead of violating policy to fill a table. Never feed one model another model's future tool outputs and call it a counterfactual. Shadow recommendations supply no unchosen outcomes. Freeze baseline selection before confirmation; keep post-hoc repricing and oracle bounds explicitly non-deployable. Subscriptions, API bills and local hardware are distinct cost bases; do not price missing usage as zero.

**Exit evidence:** actual comparative trajectories, a versioned baseline report, fresh confirmation with uncertainty, exclusion/suppression fractions and a disposition for each tested hypothesis. State whether quality is acceptable and whether net benefit is worthwhile; “insufficient” and “keep the simpler policy” are valid outcomes. A complete EVL-006 report, relevant graduation decision and tested rollback are required before expanding live routing authority.

**Stop/recovery:** stop experiments that breach budget, duplicate external effects, lose isolation or become uninterpretable after vendor changes. Revert to the approved fixed or deterministic policy within the same restrictions. If local capability is poor, narrow or suspend that slice; if switching overhead dominates, use a stable model. Neither finding invalidates the control/evidence product.

**Owning decisions:** RTG-001–009, CAS-001–009, LRN-002/004/006/008, MEM-004/009, EVL-001/002/003/006/008/009, OPS-003/005/006.

### W8A. Admit Codex and Responses without losing semantics

**Purpose:** prove that the common engine handles a genuinely different protocol and state model. Owner: protocol/integration engineer; review: security and API owners.

**Entry:** begin the state/transport spike during W0, with a proposed maximum of five engineering days before a go/no-go report. Full admission depends on W3/W5 common contracts and W6 controls. Real calls require their own account and bounded execution packet.

**Build:** capture a scrubbed real CLI corpus; design native item/tool IDs, parallel tool outputs, reasoning/compaction custody, errors, cancellation, session resume and transport behavior. Start with one approved compatible deployment and the candidate HTTP/client-carried-input scope in the [existing admission note](/Users/arunmenon/projects/adrl-core/docs/responses-admission.md). If the selected CLI genuinely needs WebSocket or opaque/server state, implement its explicit custody/control contract or narrow support; do not strip it merely to pass admission.

Official Codex configuration currently names `responses` as its supported wire API and exposes a separate WebSocket-support flag. Responses can reference prior server state, so the current request need not contain all relevant history. These facts justify a protocol-specific admission gate; they do not prove our candidate scope works. [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-reference), [Responses conversation state](https://developers.openai.com/api/docs/guides/conversation-state).

**Guardrails:** unknown referenced state is rejected before dispatch unless a trusted resolver is designed and tested. Provider-bound opaque state cannot become ordinary text or cross an incompatible deployment boundary. Request storage settings do not certify complete provider retention policy. Pinning still means an approved local path or block; incompatibility cannot be resolved by ignoring the pin. Keep supported transports and features explicit.

**Exit evidence:** real Codex task closure and verification; the shared identity/evidence matrix plus protocol-specific continuation, compaction, cancellation and foreign-lineage tests; restricted and unsupported cases rejected before dispatch. Repeat the earlier Messages suites to expose assumptions leaked into the shared engine. Publish precise support tuples and migration implications.

**Stop/recovery:** a failed spike produces a narrower contract or revised estimate, not a fictional adapter. Leave Responses unregistered and the product in preview if necessary. Disable the affected profile without changing other profiles' policies or evidence. Cross-protocol handoff is outside this first admission unless separately justified.

**Owning decisions:** SEM-001/002/003/004/005/006/007, FND-001/002/003, SAF-001/002/005/007, CAS-004/006/007, TRU-001/002, MEM-003.

### W8B. Release a supported local product

**Purpose:** a new developer can install, understand, operate and safely upgrade what we claim to support. Owner: product/release engineer; review: product owner, independent reviewer and security owner for controlled features.

**Entry:** W3–W6 and W8A; W7 findings dispositioned into the release scope. Positive routing gains are required for a routing-benefit claim, not for publishing an honestly scoped preview. Resolve DQ4 before applying a revised graduation process to non-routing features.

**Build:** a versioned installation package, pinned dependencies and license/dependency inventory; generated API contracts, adapter kit, version compatibility/deprecation policy and diagnostics. Improve the timeline/explanation experience to answer: which task/output, what policy, observed or enforced, why a destination, confirmed or unknown, what checks, and what remains uncertain. Ship quickstarts, a coverage matrix, upgrade/uninstall guidance and local retention controls. Implement operator-visible queue/backpressure, storage limits, stale/outage alerts, health plus active denial probes and a support bundle that omits sensitive payloads by default.

Qualify restart, credential rotation, upgrade with pending outboxes, interrupted migrations, backup restoration after erasure, quota/disk exhaustion, slow streams and cancellation. Enforce the supported single-process topology; scaling workers without a state-consistency design is not a tuning option. Run the declared operations pilot, initially two weeks and 100 eligible attempts, extending it for missing coverage. Use available representative users; if only one user participates, keep that limitation.

**Guardrails:** no stable label while the two-harness/two-protocol contract gate is unmet. No production development keys or hidden legacy bypass. Do not restore an old database that revives erased payloads or weakens restrictions. Code rollback must understand newer ledger/schema state; prefer forward-compatible recovery when reversal is unsafe. Do not transform a capability declaration into “tested in production.”

**Exit evidence:** reproducible package and install/upgrade/rollback results; measured setup usability and service SLOs; no open release blockers in admitted slices; completed pilot report with attempts/exclusions; compatibility and support policy; minuted release decision and any required signatures. Publish the exact supported matrix and restrictions. D3–D5 moves remain separate, recorded decisions for the relevant behaviors.

**Stop/recovery:** hold the release or remove the failing scope. Restore the last compatible package while retaining the latest restriction and erasure state; otherwise stop dispatch and provide a diagnostic. A release deadline cannot override an unknown security boundary.

**Owning decisions:** FND-001/005, SEM-007, EVL-004/007/008/009, OPS-001–008, TRU-001/003, MEM-005/006/007/010.

### W9. Let learned routing earn authority

**Purpose:** use experience only where it demonstrably improves on approved simpler rules. Owner: learning engineer; review: independent evaluator and release authority outside the training role.

**Entry:** W4/W6/W7, resolved evidence/algorithm decisions and enough admissible data. The historical working figure of 300 labels is not an automatic pass: diversity, verifier quality, suppression and representativeness remain required. New task receipts are still excluded until their eligibility contract is approved and enforced.

**Build:** enforce decision-time feature snapshots and as-of projections; train only on approved origin/quality combinations; maintain temporal/grouped partitions. Compare prompt-only features with information already available at an allowed action boundary, such as past tool results, workspace state and remaining budget; never use future outcomes. Implement and test abstention against the deterministic policy before training an estimator. Quantify whether enough decisions could benefit to justify the model and its inference/training cost. Compare simple routing rules, a pairwise outcome model and other representations only after their owning decisions allow them. Calibrate uncertainty, inspect drift and measure coverage/risk by slice. Produce a full artifact/feature/data/evaluation manifest and offline report.

**Guardrails:** do not imitate historic served-model decisions as success labels. No hidden future outcomes, leaked sibling tasks or unverified counterfactuals. Retrieval and learning cannot widen permissions. A candidate abstains outside its evidence-supported scope. The training process has no signing/deployment key. No automatic online promotion, exploration or retroactive admission of old data.

**Exit evidence:** the pre-build opportunity gate passes; admissible training/evaluation sets are audited; a fresh report beats the declared baselines at acceptable quality; calibrated abstention and rollback work. Then obtain the existing explicit graduation decision, observe shadow recommendations, and run only the approved constrained pilot. Each maturity move has its own evidence window; they are not collapsed into one successful offline score.

**Stop/recovery:** if no useful opportunity or adequate data exists, defer learning and retain deterministic routing. Drift, out-of-distribution behavior, a revoked artifact or violated risk target forces abstention to an approved policy, still constrained by privacy. Preserve the failed model's lineage and report.

**Owning decisions:** LRN-001–008, RTG-002/006/007, MEM-007/008/009/010, EVL-001–009, OPS-002/003/005.

### W10. Automate bounded improvement proposals

**Purpose:** reduce the effort of noticing gaps and preparing useful experiments, without allowing the proposer to grade or deploy itself. Owner: improvement-tools engineer; review: evaluator and product owner. W9's learned router is not required.

**Entry:** W4 evidence discipline, W8B supported local foundation, approved failure-packet data policy and separation between candidate and release evaluation access.

**Build:** permit an offline proposer to read an authorized minimal failure packet and produce a versioned hypothesis, patch/config candidate, affected ADRs, scope, predicted benefit and evaluation plan. Start with verifier additions and bounded diagnostics/configuration proposals. Execute candidates in isolated workspaces with explicit action/time/cost limits. Preserve failed proposals, parent lineage and evaluator versions. Add retry/resume semantics, admission validation and a separate control API only if actual users need them. Provide the reviewer a concise comparison and deployable diff; approved adoption uses the release path, not proposer privileges.

**Guardrails:** edit allowlists exclude privacy rules, trusted tests/answers, signing keys, release gate definitions and production state. Changes to those areas require separately owned work. No opaque reference grants artifact access; no private packet leaves the approved destination set. Keep expected answers and promotion criteria fixed for the assessment. A candidate that disables logging or changes outcome classification cannot be rewarded as cheaper or more successful.

**Exit evidence:** at least one end-to-end proposer run with independent assessment; deliberate rejection of a malicious/invalid proposal; budget exhaustion and interruption recovery; a human-reviewed useful candidate or a documented no-improvement outcome; complete lineage and ADR disposition. Compare proposer usefulness and total experiment cost with a manual/simple proposal baseline on fresh tasks before claiming productivity gains.

**Stop/recovery:** shut off proposal generation while the approved runtime continues unchanged. Contaminated cases are retired from release assessment. Repeated invalid proposals trigger a scope/prompt/tooling investigation; they do not earn more authority. Improvement discovery cost is reported even when every proposal fails.

**Owning decisions:** LRN-004/005/007, MEM-003/005/008/010, EVL-004/005/006/007/009, SAF-007, TRU-001, OPS-002/003.

### W11. Expand to teams and additional harnesses

**Purpose:** serve organizational users without pretending that the localhost trust model provides tenant isolation. Owner: platform engineer; review: security and operations owners plus pilot users.

**Entry:** W8B and demonstrated demand for a managed deployment. Select whether the product remains one service per developer with a shared control plane, or needs a shared request service. That architecture decision precedes distributed state work.

**Build:** organization-backed workload identity, per-user/tenant access boundaries, role separation, policy distribution, key custody/rotation/revocation and inventory administration. If scaling runtime workers, redesign consistency for pins, budgets, idempotency, queues and append order; test split brain and failover. Add tenant quotas, backup/restore/erasure reconciliation, remote verification authority and incident procedures. Admit further harnesses using the kit and capability matrix, prioritizing actual users and accessible control points.

**Guardrails:** no reuse of a shared host HMAC as organization membership proof. No cross-tenant artifacts, receipts or data-derived retrieval. A hook-only harness receives a limited observation contract; marketing must not call it gateway-enforced. Multi-region/residency claims require actual destinations and lifecycle evidence. Do not add every previously surveyed harness merely to increase the count.

**Exit evidence:** adversarial tenant isolation and credential revocation tests; concurrent restriction propagation; failover without weakened policy or duplicate side effects; measured service SLOs; tested erasure after backup restoration; operator runbooks and a constrained team pilot. Each new harness passes its declared conformance suite and real-task gate.

**Stop/recovery:** isolate the tenant/integration, revoke credentials, stop affected dispatch and preserve the forensic record. Keep the known local deployment option available where policy permits. If distributed invariants cannot be maintained, retain one owning process per policy domain rather than scaling unsafely.

**Owning decisions:** TRU-001/002/003, OPS-001/002/003/004/007/008, SAF-002/008/009, SEM-007, MEM-005/006/007/010, EVL-007/009.

### W12. Test the recursive element, conditionally

**Purpose:** determine whether improving the proposer or experiment selector helps ADRL discover useful changes more efficiently. Owner: research/evaluation lead; review: independently controlled evaluator and product owner.

**Entry:** W10 has accumulated enough independently assessed outcomes to compare improvement methods. Define what effect and uncertainty would justify another research tranche. A calendar milestone is not eligibility.

**Build:** compare the current improvement method with a candidate proposer, failure summarizer or experiment selector at the same allowed budget, scope and access. Use fresh task families or environments and independently assessed downstream changes. Count useful accepted improvements, their retained quality after rollout, rejected/unsafe proposals, discovery cost, time and repeatability across independent runs. Version the evaluator separately. Run one bounded research tranche before deciding whether to extend it.

**Guardrails:** no candidate controls its scoring rules, task allocation after seeing outcomes, evaluator data or release authority. More proposals or higher visible-test scores are not the objective. Count all failed-search costs. No self-modification of safety/privacy or automatic chain of promotions. A better deployed router alone is not evidence that the improvement process improved.

**Exit evidence:** a predeclared comparison supports or rejects the narrower hypothesis that the candidate improvement method is better. Only independently accepted, durable gains count. One result does not establish unlimited or accelerating improvement. Archive negative findings and choose continue, simplify or stop.

**Stop/recovery:** return to the previous proposer/manual process. The deployed product and its approved policies keep operating. If investigation stops yielding sufficient value, close this research branch without blocking product delivery.

**Owning decisions:** LRN-003/004/005/007, EVL-001/002/004/005/006/007/009, RTG-007, FND-005.

## 9. Decisions to settle before the dependent implementation

These are proposed dispositions, not amendments applied by this plan. Each goes through the owning ADRs with original text preserved. Reconcile overlapping proposals before issuing a new normative clause.

| Queue item | Recommended direction | Latest point to settle | Affected decisions |
|---|---|---|---|
| DQ1: Origin versus verification quality | Separate organic/branch/curated origin from verification quality; explicitly admit combinations for training, calibration and evaluation. Keep current exclusions until changed deliberately | W4 contract; before W7 formal evaluation and all W9 learning | LRN-001/002/003/004, MEM-002/004, EVL-002/003/004/005/006 |
| DQ2: Deployable baselines versus hindsight bounds | Select a deployable single-model baseline on development data; keep oracle/repricing analysis labeled as a bound. Actual alternatives require executions | Before W7 confirmation | EVL-001/002/003/006, RTG-005/007/009 |
| DQ3: Controlled-path availability semantics | Explicitly disposition unknown health, stale inventory, scanner failure, identity absence, shadow ceilings and receipt uncertainty by workload class | W6 admission | FND-004, SAF-001/003/006/008/009, TRU-002, OPS-005/006/008 |
| DQ4: Product release versus routing graduation | Define integration/security/operations qualification separately from economic routing gates while retaining human review and restrictions. Current EVL-007's generic ladder otherwise asks non-routing features for routing gains | Before a formal controlled/product graduation | FND-005, SEM-007, EVL-006/007/009, LRN-007 |
| DQ5: Handoff and routing hypotheses | Keep local-first, transcript carryover, sticky escalation and policy representation testable. Amend clauses only when evidence and compatibility justify alternatives | Relevant W7 experiment; algorithm choice before W9 | RTG-002/004/006/007/009, CAS-004/005/006, LRN-003 |
| DQ6: Custody and deletion of all artifact copies | Decide which identifiers/payloads need deletion versus durable audit, and how snapshots, projections, exports, outboxes and backups participate. Obtain applicable policy/legal review before any compliance claim | Before W4 corpus growth and W8B retention promise | MEM-001/005/007/010, OPS-002/004, TRU-003 |
| DQ7: Responses admission and current vendor capabilities | Set the supported transport/state/custody scope from captured behavior; allow a failed spike to revise scope or schedule | W8A spike, before registration | SEM-007, SEM-004/005/006, CAS-004/006, SAF-002/005 |
| DQ8: Team topology and authority | Choose local agents with shared administration versus shared runtime; define organization/tenant authority and consistency before distributed implementation | W11 entry | TRU-001/002/003, OPS-001/002/003/007, MEM-006 |

The [independent research review](adrl-independent-research-review-2026-09-07.md) supplies hypotheses and unresolved architecture questions. It is not an instruction to implement every paper's algorithm. A study on another workload can prioritize an ADRL experiment; it cannot replace one.

## 10. How we execute the plan over months

**Two levels of planning:** keep this roadmap stable enough to coordinate dependencies; detail only the next one or two waves into executable slices. Re-estimate later waves at their entry gates. A slice should usually produce one reviewable behavior in one to three engineering days. Do not lock six months of tasks to assumptions that the first month is intended to test.

The work packet records: problem and counterexample; exact ADR clauses; expected product behavior; allowed files/data/actions; source/config/model versions; entry prerequisites; independent acceptance cases; budgets; rollback; evidence location; owner/reviewer; and explicit pass/fail/insufficient/stop decisions. The [template](adrl-wave-execution-template.md) makes this repeatable. Proposed tracker records are in the [planning manifest](research/adrl-roadmap-plan-2026-09-07.json); they are not a deployed scheduler or policy engine.

Use distinct engineering and evidence states. Engineering progresses from proposed to ready, implementing, validated and closed. A wave may close as failed or narrowed with a documented disposition. Support/maturity is recorded separately per behavior and version; closing a development task never grants deployment authority.

**Cadence:** at each slice close, record changes, checks, failures, spend and the next uncertainty. Once a week, review blockers, coverage, data quality and the critical path. At wave boundaries, inspect the concrete evidence pack and decide advance, repeat, narrow, amend or stop. Monthly, reconsider whether later investments still serve the product. These are proposed working practices; no meetings, messages or recurring automations are scheduled by this plan.

**Limits on autonomous work:** within an approved slice, implement routine fixes, run checks and synchronize the register without repeatedly asking for permission. A proposed initial run cap is three slices or three failed repair attempts per task before reassessment. An unchanged evidence/problem state after two retries should produce a blocker report rather than more blind retries. The existing `.project/governance/autonomy.yaml` is configuration for a separate runner, not proof that such control is active; its null dollar budget is not permission for unlimited model spending. Make any future runner explicitly consume the approved packet, and test its stops.

**Review authority:** the implementation role authors the patch; the evidence reviewer challenges expected answers and comparisons; the security owner approves exposed trust/privacy changes; the product owner chooses supported scope and cost-quality tradeoffs. The artifact signer is outside the training/proposer role where the register requires it. One person can wear multiple delivery roles, but the same candidate author cannot claim independent evaluation. If an independent reviewer is unavailable, continue scoped development and withhold that graduation claim.

**Definition of implementation done:** code implements the named behavior; required six checks pass, with data inventory, contract compatibility and ADR module mapping where affected; acceptance/fault cases have evidence; new failures remain visible; documents match code; owning ADRs, index, bucket summaries and changelog are synchronized; prior text and unrelated changes survive; rollback is demonstrated for exposure changes. Run the relevant adversarial suite as a blocking release gate for controlled capabilities, regardless of any earlier publish-only CI convention.

**Replanning triggers:** a forbidden dispatch or erased-data resurrection; inability to attribute outputs; evaluator contamination; a provider/harness change that invalidates a fixture; two unsuccessful repair cycles with no new information; forecast effort growing beyond the packet's agreed tolerance; or no worthwhile gain in the primary experiment. Freeze only affected exposure, preserve the finding, classify it, propose the smallest coherent correction, assess downstream dependencies and record the new plan version. Lowering a threshold after seeing failure cannot rescue the same evaluation; require new assessment evidence.

## 11. Budget, access and capacity

The user already has Claude subscription access. Native observation has been exercised. Gateway passthrough under that subscription is only a newly documented candidate path, and multi-provider experiments require their own admitted access. No new paid calls, model downloads, infrastructure purchases or deployments are requested during this planning pass.

| Resource | Decide before use | Enforcement and evidence |
|---|---|---|
| Local engineering | Active repository snapshot, check commands, task-attempt/time cap | Preserve diffs and failures; stop loops at the packet boundary |
| Subscription runs | Native or tested passthrough mode, quota allowance and turn/runtime cap | Check active account/mode; preserve usage uncertainty; no automatic purchase/reset |
| API comparisons | Exact accounts/deployments, per-run and batch dollar/token ceilings | Preflight worst-case exposure where estimable, bound in-flight requests, reserve budget conservatively; reconcile actual billing afterward |
| Local models | Hardware memory/storage, approved source/license, runtime and energy/hosting assumptions | First perform capability/latency admission; do not assume local execution is free or automatically private |
| Experiments | Number of arms/tasks/repeats, check and proposal budgets, stopping rule | Count rejected, timed-out and repaired runs; no repeated holdout search hidden in the budget |
| Evidence storage | Snapshot/artifact size, retention period, encryption keys and backup scope | Enforce quotas and cleanup; disk exhaustion remains an explicit failure, not silent evidence loss |
| Review and users | Named independent reviewers, availability and eligible repositories/users | Make recruitment/review time a dependency; never invent representativeness |

Budget ceilings must cover concurrently admitted work; a late provider usage receipt cannot undo an overspend. Quota and cost visibility vary by access mode, so when exact monetary enforcement is unavailable, use conservative turn/token/concurrency/time limits and disclose what remains uncertain.

For W0–W5, use the existing machine and subscriptions where suitable. Do not procure a local inference server until W7's capability question, workload and estimated benefit justify it. Security/evaluation reviewers are needed before meaningful graduation, even if implementation is performed by one engineer with agents.

## 12. Program scorecard and risk register

Report capabilities and trust before economics. A concise weekly scorecard should include:

| Dimension | Measures and denominator |
|---|---|
| Integration | Tested support tuples; setup completion/time; missing/out-of-order/duplicate events per attempted session |
| Outcome trust | Exact output attribution; verified/failed/indeterminate counts; false accept/reject; disagreements and delayed repairs |
| Control | Forbidden attempts blocked; active denial probes; pin continuity; missing identity/state; receipt-confirmed and unknown fractions |
| Reliability | All-attempt completion, timeouts, partial streams, recovery time, queue age, disk and dropped-evidence count |
| Economics | Full task cost and wall time at acceptable quality; price basis and unknown usage; cost of discovering improvements |
| Adaptation | Proposed/evaluated/rejected/adopted candidates; independent confirmation; rollback; version lineage |
| Governance | Open blockers, unresolved decision changes, ADR synchronization, scope and maturity explicitly claimed |

Do not put these into one composite score that allows money saved to cancel a privacy failure.

| Risk | Earliest trigger | Primary wave / response |
|---|---|---|
| We certify the wrong code | Workspace changes between close and verification | W3: immutable capture or explicit indeterminate attribution |
| Verifier improves only on its own examples | Gains disappear on independently chosen cases | W4: separate development and confirmation; keep failed cases |
| Shared API is Claude-shaped | OpenCode requires a duplicate policy path | W5: revise shared preview contract, keep adapter logic narrow |
| Control can be bypassed | Stripping identity reaches legacy forwarding | W6: separate controlled listener and mandatory admission |
| Restrictions disappear on recovery | Restart, resume, child return or backup restores permissive state | W6/W8B: continuity tests and recovery using current restrictions |
| Gateway behavior is hidden | Missing served receipts or hidden retries after tool output | W6: explicit uncertainty; capability restriction or gateway contract change |
| Local-first hurts users | More repair/time outweighs cheaper initial inference | W7: choose direct-strong or narrower local scope |
| State/transport blocks Codex | Required opaque or server state lies outside candidate profile | W8A: implement custody or keep unsupported; do not flatten state |
| Data cannot support learning | No suitable diversity, suppressed fraction too high, unclear labels | W9: retain deterministic product, resolve data contracts |
| Proposer games evaluation | Edits tests/logs or leaks holdout data | W10: isolate authority, invalidate affected evidence, stop proposer |
| Team scaling weakens guarantees | Split brain or cross-tenant read under concurrency | W11: preserve single owner per policy domain until qualified |
| RSI becomes an expensive distraction | Search cost grows without durable useful improvements | W12: close research tranche and retain manual/simple improvement |

## 13. The first execution sequence after plan review

1. Open W0 with the latest verified source snapshot and preserve both dirty workspaces. Produce the reconciled backlog and support matrix; do not rewrite historical reports as current evidence.
2. Resolve W3's task-close capture boundary and record its acceptance cases. Agree which operating-system/user assumptions make “exact output” a defensible claim.
3. Implement the smallest W3 slice: one task attempt, trusted close request, captured snapshot and durable identity. Then add verification binding, interruption/erasure behavior and a real task demonstration in separate slices.
4. Have the evidence reviewer prepare fresh W4 cases while W3 completes. This is independent work, not authorization to spawn agents or contact anyone during this planning turn.
5. Start the OpenCode adapter against the stabilized preview contract. Run the bounded Responses design spike early enough to reveal incompatible API assumptions before stable release.
6. At the W3 close, publish what changed, what was proven, what failed, the exact ADR updates and the revised W4/W5 estimates. Continue under the approved scope; bring only new material decisions to the owner.

The immediate implementation target remains **exact task-close attribution**. The strategic target is **one trustworthy product across harnesses**. The learning and RSI branches must improve that product measurably, rather than becoming requirements that prevent it from shipping.

## 14. Evidence and source notes

This plan was grounded in the current register, the dedicated historical taxonomy overview, source and engineering instructions in `adrl-core`, preview-4 service and Responses admission documentation, the independent research review, and the latest applied experiment/source manifest. It is a planning synthesis, not another scientific adjudication or a new live validation run.

- [Current implementation and comparison](adrl-improvement-experiment-2026-09-07.md), [source/check manifest](research/adrl-improvement-experiment-2026-09-07.json).
- [Independent research review](adrl-independent-research-review-2026-09-07.md), [adaptive-improvement proposal](adrl-adaptive-improvement-proposal-2026-09-07.md).
- [Product boundary](../design/adrl-multi-harness-product-contract-2026-09-07.md), [current service behavior](/Users/arunmenon/projects/adrl-core/docs/product-services.md), [known gaps](/Users/arunmenon/projects/adrl-core/docs/known-gaps.md).
- [Historical taxonomy](../source/01-overview-tenets-taxonomy.md), [current 77-decision index](../INDEX.md).
- [Plan structure, dependencies and ADR assignment](research/adrl-roadmap-plan-2026-09-07.json), [planning validation](research/adrl-roadmap-validation-2026-09-07.json).

Official integration pages were fetched on 7 September 2026 and cited where used. Recheck them when opening the relevant wave. Specific model names, prices, subscription behavior and vendor guarantees must never be inferred from dated sample configuration. Local engineering estimates and proposed numerical targets are planning judgments, not findings from those sources.

## Appendix A. All 77 decisions have a place in the plan

This is a review and ownership assignment, not a statement that every decision needs rewriting or that its complete promise ships in its first wave. Later waves revisit affected decisions when their evidence or product scope changes. Existing statuses and maturity are unchanged.

| Decision | First accountable review wave | Other affected waves |
|---|---|---|
| [ADRL-CAS-001](../adr/CAS/ADRL-CAS-001.md) | W7 | W6 |
| [ADRL-CAS-002](../adr/CAS/ADRL-CAS-002.md) | W7 | None assigned |
| [ADRL-CAS-003](../adr/CAS/ADRL-CAS-003.md) | W7 | W6 |
| [ADRL-CAS-004](../adr/CAS/ADRL-CAS-004.md) | W7 | W6, W8A |
| [ADRL-CAS-005](../adr/CAS/ADRL-CAS-005.md) | W7 | None assigned |
| [ADRL-CAS-006](../adr/CAS/ADRL-CAS-006.md) | W7 | W6, W8A |
| [ADRL-CAS-007](../adr/CAS/ADRL-CAS-007.md) | W7 | W6, W8A |
| [ADRL-CAS-008](../adr/CAS/ADRL-CAS-008.md) | W7 | None assigned |
| [ADRL-CAS-009](../adr/CAS/ADRL-CAS-009.md) | W7 | W6 |
| [ADRL-EVL-001](../adr/EVL/ADRL-EVL-001.md) | W7 | W9, W12 |
| [ADRL-EVL-002](../adr/EVL/ADRL-EVL-002.md) | W4 | W7, W9, W12 |
| [ADRL-EVL-003](../adr/EVL/ADRL-EVL-003.md) | W7 | W9 |
| [ADRL-EVL-004](../adr/EVL/ADRL-EVL-004.md) | W4 | W8B, W9, W10, W12 |
| [ADRL-EVL-005](../adr/EVL/ADRL-EVL-005.md) | W4 | W9, W10, W12 |
| [ADRL-EVL-006](../adr/EVL/ADRL-EVL-006.md) | W4 | W7, W9, W10, W12 |
| [ADRL-EVL-007](../adr/EVL/ADRL-EVL-007.md) | W0 | W8B, W9, W10, W11, W12 |
| [ADRL-EVL-008](../adr/EVL/ADRL-EVL-008.md) | W3 | W7, W8B, W9 |
| [ADRL-EVL-009](../adr/EVL/ADRL-EVL-009.md) | W0 | W4, W7, W8B, W9, W10, W11, W12 |
| [ADRL-FND-001](../adr/FND/ADRL-FND-001.md) | W5 | W6, W8A, W8B |
| [ADRL-FND-002](../adr/FND/ADRL-FND-002.md) | W5 | W8A |
| [ADRL-FND-003](../adr/FND/ADRL-FND-003.md) | W8A | None assigned |
| [ADRL-FND-004](../adr/FND/ADRL-FND-004.md) | W6 | None assigned |
| [ADRL-FND-005](../adr/FND/ADRL-FND-005.md) | W0 | W5, W8B, W12 |
| [ADRL-LRN-001](../adr/LRN/ADRL-LRN-001.md) | W4 | W9 |
| [ADRL-LRN-002](../adr/LRN/ADRL-LRN-002.md) | W7 | W9 |
| [ADRL-LRN-003](../adr/LRN/ADRL-LRN-003.md) | W9 | W12 |
| [ADRL-LRN-004](../adr/LRN/ADRL-LRN-004.md) | W4 | W7, W9, W10, W12 |
| [ADRL-LRN-005](../adr/LRN/ADRL-LRN-005.md) | W4 | W9, W10, W12 |
| [ADRL-LRN-006](../adr/LRN/ADRL-LRN-006.md) | W9 | W7 |
| [ADRL-LRN-007](../adr/LRN/ADRL-LRN-007.md) | W4 | W9, W10, W12 |
| [ADRL-LRN-008](../adr/LRN/ADRL-LRN-008.md) | W9 | W7 |
| [ADRL-MEM-001](../adr/MEM/ADRL-MEM-001.md) | W3 | W5 |
| [ADRL-MEM-002](../adr/MEM/ADRL-MEM-002.md) | W3 | W4 |
| [ADRL-MEM-003](../adr/MEM/ADRL-MEM-003.md) | W3 | W4, W5, W8A, W10 |
| [ADRL-MEM-004](../adr/MEM/ADRL-MEM-004.md) | W4 | W7 |
| [ADRL-MEM-005](../adr/MEM/ADRL-MEM-005.md) | W3 | W8B, W10, W11 |
| [ADRL-MEM-006](../adr/MEM/ADRL-MEM-006.md) | W5 | W6, W8B, W11 |
| [ADRL-MEM-007](../adr/MEM/ADRL-MEM-007.md) | W8B | W9, W11 |
| [ADRL-MEM-008](../adr/MEM/ADRL-MEM-008.md) | W9 | W10 |
| [ADRL-MEM-009](../adr/MEM/ADRL-MEM-009.md) | W7 | W9 |
| [ADRL-MEM-010](../adr/MEM/ADRL-MEM-010.md) | W3 | W4, W5, W6, W8B, W9, W10, W11 |
| [ADRL-OPS-001](../adr/OPS/ADRL-OPS-001.md) | W0 | W6, W8B, W11 |
| [ADRL-OPS-002](../adr/OPS/ADRL-OPS-002.md) | W6 | W8B, W9, W10, W11 |
| [ADRL-OPS-003](../adr/OPS/ADRL-OPS-003.md) | W0 | W6, W7, W8B, W9, W10, W11 |
| [ADRL-OPS-004](../adr/OPS/ADRL-OPS-004.md) | W6 | W8B, W11 |
| [ADRL-OPS-005](../adr/OPS/ADRL-OPS-005.md) | W6 | W5, W7, W8B, W9 |
| [ADRL-OPS-006](../adr/OPS/ADRL-OPS-006.md) | W6 | W7, W8B |
| [ADRL-OPS-007](../adr/OPS/ADRL-OPS-007.md) | W6 | W8B, W11 |
| [ADRL-OPS-008](../adr/OPS/ADRL-OPS-008.md) | W6 | W8B, W11 |
| [ADRL-RTG-001](../adr/RTG/ADRL-RTG-001.md) | W7 | None assigned |
| [ADRL-RTG-002](../adr/RTG/ADRL-RTG-002.md) | W7 | W9 |
| [ADRL-RTG-003](../adr/RTG/ADRL-RTG-003.md) | W7 | None assigned |
| [ADRL-RTG-004](../adr/RTG/ADRL-RTG-004.md) | W7 | None assigned |
| [ADRL-RTG-005](../adr/RTG/ADRL-RTG-005.md) | W7 | None assigned |
| [ADRL-RTG-006](../adr/RTG/ADRL-RTG-006.md) | W7 | W9 |
| [ADRL-RTG-007](../adr/RTG/ADRL-RTG-007.md) | W7 | W9, W12 |
| [ADRL-RTG-008](../adr/RTG/ADRL-RTG-008.md) | W7 | None assigned |
| [ADRL-RTG-009](../adr/RTG/ADRL-RTG-009.md) | W7 | None assigned |
| [ADRL-SAF-001](../adr/SAF/ADRL-SAF-001.md) | W6 | W8A |
| [ADRL-SAF-002](../adr/SAF/ADRL-SAF-002.md) | W6 | W8A, W11 |
| [ADRL-SAF-003](../adr/SAF/ADRL-SAF-003.md) | W6 | None assigned |
| [ADRL-SAF-004](../adr/SAF/ADRL-SAF-004.md) | W6 | None assigned |
| [ADRL-SAF-005](../adr/SAF/ADRL-SAF-005.md) | W6 | W8A |
| [ADRL-SAF-006](../adr/SAF/ADRL-SAF-006.md) | W6 | None assigned |
| [ADRL-SAF-007](../adr/SAF/ADRL-SAF-007.md) | W6 | W3, W4, W8A, W10 |
| [ADRL-SAF-008](../adr/SAF/ADRL-SAF-008.md) | W6 | W11 |
| [ADRL-SAF-009](../adr/SAF/ADRL-SAF-009.md) | W6 | W11 |
| [ADRL-SEM-001](../adr/SEM/ADRL-SEM-001.md) | W5 | W8A |
| [ADRL-SEM-002](../adr/SEM/ADRL-SEM-002.md) | W3 | W5, W8A |
| [ADRL-SEM-003](../adr/SEM/ADRL-SEM-003.md) | W3 | W8A |
| [ADRL-SEM-004](../adr/SEM/ADRL-SEM-004.md) | W6 | W8A |
| [ADRL-SEM-005](../adr/SEM/ADRL-SEM-005.md) | W6 | W8A |
| [ADRL-SEM-006](../adr/SEM/ADRL-SEM-006.md) | W3 | W5, W6, W8A |
| [ADRL-SEM-007](../adr/SEM/ADRL-SEM-007.md) | W5 | W0, W3, W8A, W8B, W11 |
| [ADRL-TRU-001](../adr/TRU/ADRL-TRU-001.md) | W6 | W3, W5, W8A, W8B, W10, W11 |
| [ADRL-TRU-002](../adr/TRU/ADRL-TRU-002.md) | W6 | W8A, W11 |
| [ADRL-TRU-003](../adr/TRU/ADRL-TRU-003.md) | W6 | W8B, W11 |
