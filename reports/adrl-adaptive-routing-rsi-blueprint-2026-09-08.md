# ADRL adaptive routing and RSI: target product blueprint

**Product and memory planning update, 2026-09-08:** the [startup roadmap](adrl-product-roadmap-2026-09-08.md) adds customer/investment gates and an explicit context-to-decision design. The user clarified a [context graph in MEM](../design/adrl-context-graph-memory-proposal-2026-09-08.md) to connect experience and support evolving policies/ADRs. It is a proposed derived memory view with existing retrieval, evidence and temporal gates, not implemented learned authority. Implementation remains paused.

8 September 2026 · Draft for product disposition · Implementation sequence paused

## The answer to the direction question

**The recent execution sequence drifted in emphasis.** It made important progress on capturing and protecting evidence, but did not keep the central routing behaviour visible. The user's taxonomy already contains a more ambitious target than the current demonstrations: choose an appropriate permitted model, reconsider that choice as the task unfolds, and improve the policy using credible outcomes.

The correct response is to reconnect implementation to that target before starting another wave. The scheduled implementation run is paused. The preceding routing diagnostic and its correction packet are preserved; neither that fix nor W3 custody work should run ahead of this blueprint's disposition.

**Proposed product promise:** ADRL is a shared decision layer for coding harnesses that selects and revises model use from task state and measured capability, learns better routing policies from qualified outcomes, and eventually improves the process that discovers those policies, while preserving privacy, execution correctness and explicit release control.

“State of the art” is a design ambition here, not a performance claim. We have not shown that ADRL beats a strong fixed-model baseline on real coding work. No single published router establishes the best method for every workload.

## 1. Start from the taxonomy we already have

[RTG-007](../adr/RTG/ADRL-RTG-007.md) already describes two decisions: initial placement at the user turn, and continuing versus escalating at a safe boundary using partial trajectory, workspace/tool state and remaining budget. Its 3 September wording includes a proposed amendment pending disposition. We should resolve and operationalize it, rather than present trajectory-aware routing as a new invention.

Other existing anchors are equally central:

- **RTG-001:** local, cheaper cloud and frontier are service/economic tiers; they do not establish a universal ranking of capability. A stronger choice is specific to a task and an approved transition.
- **RTG-003:** a rule's authority can be withdrawn when qualified outcomes show that it is unreliable.
- **RTG-005/009:** completion quality, retries, latency and the cost of the remaining session matter. A cheap first call can lead to an expensive task.
- **CAS-001/003/004/005:** detect trouble, switch only at valid boundaries, preserve meaning across a handoff and control instability from repeated switching.
- **LRN-003/004/006/007:** learn comparative benefit from suitable evidence, use information available at decision time, abstain when uncertain and require explicit graduation.
- **MEM and EVL:** establish which attempt produced an outcome, whether it is trustworthy, and whether a changed policy really improved matters.

The [77-decision coverage map](research/adaptive-routing-blueprint-2026-09-08/taxonomy-map.md) assigns every existing ADR to its place in this blueprint. It is a completeness map, not 77 new scientific verdicts or maturity promotions. Stable IDs and current decision wording are retained.

## 2. Three loops, with different responsibilities

| Loop | What changes? | Example | Taxonomy ownership |
|---|---|---|---|
| **Adapt during a task** | Current choice inside an approved policy | Start locally for an eligible edit; reconsider after repeated failures; continue or switch at a safe boundary | SEM, TRU, SAF, RTG, CAS |
| **Improve across tasks** | The versioned routing policy | Verified results show that one class of parser work needs a different starting model or escalation rule | MEM, LRN, EVL, OPS |
| **Improve the improvement process: RSI** | How candidate improvements are discovered and assessed | A new failure-analysis or experiment-selection method finds more durable routing improvements for the same total budget | LRN, EVL, FND, OPS |

The first loop can act automatically within its approved limits. The second can automatically collect, analyse and propose, while a newly authoritative policy still needs the register's graduation path. The third proposes changes to the machinery used by the second loop; it must be evaluated against that previous machinery. A system that merely updates thresholds is adaptive, but that alone is not evidence of recursive improvement.

Training the underlying coding model is not required for any of these first product milestones. The initial objects of improvement are ADRL's rules, estimators, calibration, permitted transition choices and experiment process.

## 3. The target runtime decision

At a new user turn, ADRL asks: **Which permitted deployment is most likely to finish this work acceptably within the user's constraints?** At an eligible later boundary it asks: **Given what has happened, is continuing still better than switching or stopping?**

The state should contain the following, only where the harness/profile can supply it reliably and privacy rules permit processing it:

| State | Why it can change the decision |
|---|---|
| Task intent, scope and mixed instructions | A request can contain both a small edit and difficult design work; the easiest keyword must not decide the whole task |
| Current stage and observed progress | Reading, implementing and recovering may have different needs; inferred stages must carry uncertainty |
| Recent edits, tool outcomes and verifier signals | Repetition or a trustworthy failed check changes the value of continuing |
| Current deployment, cache and context state | Switching can lose cached context or require an incompatible transformation |
| Workspace identity and known side effects | A model change cannot safely replay actions that already happened |
| Remaining task budget and latency tolerance | More expensive reasoning may be worthwhile early and unaffordable late |
| Measured capability by task slice | Model names and broad tiers alone do not tell us which deployment is suitable |
| Evidence freshness and missing inputs | A missing or stale measurement should produce uncertainty, not fabricated confidence |

The allowed action set is deliberately narrower than “do anything an agent can do”:

1. **Initial dispatch** to an eligible deployment.
2. **Continue** on the current deployment.
3. **Switch** along a qualified transition, at a safe boundary, under the applicable context and side-effect rules.
4. **Abstain** from a learned recommendation and use the approved deterministic fallback inside the same restrictions.
5. **Stop or surface a typed failure** when the allowed options cannot continue safely.

Changing tools, rewriting the user's task, granting new credentials or deploying arbitrary agents is outside this core routing action set. Downshifting within an episode is also outside the current CAS-005 contract; it can be a separately proposed experiment, not a silently added runtime option.

## 4. Separate the fixed restrictions from the adaptable policy

The request path is:

**Harness/profile → semantic and identity state → permitted deployments → routing choice → controlled dispatch/continuation → observations.**

SAF and TRU establish permission and feasibility before routing. An optimizer cannot exchange a privacy breach for a higher quality score. At dispatch, the chosen deployment must still be eligible; stale advice cannot override a new pin or a changed inventory. Evidence must distinguish intended destination, reported served destination and unknown identity.

Within that boundary, the selector should support competing strategies behind one decision contract:

- Fixed-model and simple rule policies as explicit baselines and fallbacks.
- A measured capability table or lightweight outcome-based scorer.
- A learned comparative-benefit estimator with calibrated abstention.
- A trajectory-conditioned continue/switch estimator at eligible boundaries.

These are candidates to compare, not a promise to build every algorithm. A contextual bandit, causal learner or reinforcement-learning policy must earn its additional data, exploration and operational costs. Keep model inventory, state representation, scoring, action selection and outcome signals separable so we can replace a weak method without rebuilding the entire product.

**Objective proposal for disposition:** enforce privacy and execution constraints as hard limits; then meet a declared task-quality requirement while reducing total completion cost, time and repair effort. Preserve the existing RTG-005 weighted objective as a baseline until its relation to this quality-constrained objective is explicitly resolved. Do not change weights or acceptable quality merely because a candidate otherwise loses.

## 5. What research supports, and what it does not

This is a focused primary-source design check, not a fresh exhaustive literature review. The following findings inform candidate choices; none qualifies ADRL itself.

| Primary source | Relevant finding | Implication for ADRL |
|---|---|---|
| [RouteLLM, revised February 2025](https://arxiv.org/abs/2406.18665) | Trained routers can exploit comparative preference data to trade response quality and cost | Include a lightweight learned comparison as a candidate; coding-task success still needs its own outcomes |
| [LLMRouterBench, January 2026](https://arxiv.org/abs/2601.07206) | Model complementarity exists, yet several routing methods do not reliably beat simple baselines | A strong fixed model and a simple policy must remain serious competitors |
| [LLMRouter, August 2026](https://arxiv.org/html/2608.06867v1) | Provides a modular sequential formulation and reports gains for learned routing in its benchmark; no method wins everywhere, and extra routing rounds do not consistently help | Separate state, model representation, scorer, choice and learning signal; compare methods under ADRL's workload and total budget |
| [The Replay Gap, August 2026](https://arxiv.org/abs/2608.08239) | Model switches changed subsequent agent trajectories, undermining evaluation that stitches substitutions into old logs | Use independently executed branches from the same valid state for causal switching claims; an offline decision trace is only a mechanism check |
| [Darwin Gödel Machine, March 2026 revision](https://arxiv.org/html/2505.22954v3) | Demonstrates empirically evaluated code changes to an agent and an archive of alternatives; also discusses objective hacking and incomplete evaluation | Version and compare candidate improvers, keep assessment independent of the candidate, retain failures and account for search cost |
| [AlphaEvolve, June 2025 white paper](https://arxiv.org/abs/2506.13131) | Uses evaluator feedback and evolutionary code changes to improve algorithms | Automated improvement is most credible when success can be tested externally; this does not establish an automatic solution to agentic routing |

My synthesis is that ADRL should be **trajectory-capable, evidence-driven and method-independent**. It should not assume that a learned policy, more switches or a self-editing agent is automatically superior. The two 2026 routing benchmarks evaluate different settings and reach different performance conclusions; we should not select whichever headline matches our preference.

## 6. The evidence-to-policy loop must be a product feature

For every eligible completed task, connect the decision-time state and policy version to actual execution, exact output, independent checks, all attempts, late corrections and cost. A clean-looking assistant response is not enough. Infrastructure errors, user interruption and policy restrictions must remain distinguishable from model inability.

The learning pipeline then:

1. Admits only evidence that satisfies the relevant MEM/LRN/EVL rules; pending, ambiguous, private or synthetic records retain their separate treatment.
2. Diagnoses whether the problem is classification, capability, transition cost, execution compatibility, environment failure or a bad verifier.
3. Proposes one scoped change against a frozen incumbent policy.
4. Evaluates on fresh, later and session-separated evidence, using valid branches when comparing choices that alter execution.
5. Produces a graduation packet with uncertainty, exclusions, regression results and rollback.
6. Releases only within the approved population, monitors drift and withdraws authority if conditions fail.

A learner should not be rewarded for copying the heuristic's own labels. Nor should repeatedly inspecting the same “holdout” turn it into development data without acknowledgement. Synthetic fixtures remain useful for mechanisms and adversarial coverage; they cannot silently satisfy organic-evidence requirements.

**Minimum visible product loop:** “Here was the old choice and reason; here is the qualified evidence that challenged it; here is the candidate; here is the comparison; here is the adopted or rejected change; here is its owning ADR.” W3/W4 should deliver exactly the evidence required for this loop, with broader infrastructure work justified separately.

## 7. RSI: precisely what can improve itself

The initial improver should be simple and versioned: ingest an authorized failure packet, diagnose the cause, propose a bounded policy/code experiment, and emit a reviewable candidate. Later, the improver may propose changes to:

- Its method of grouping and explaining failures.
- Which experiments it chooses under a fixed evaluation budget.
- Candidate policy rules, feature representations or scoring methods within an approved search space.
- Its own proposal prompts or bounded implementation methods.

The recursive test compares **improver A versus improver B**, starting from the same incumbent, comparable failure information and the same total budget. Measure independently accepted, durable routing gains per total cost, including unsuccessful proposals, model use, evaluation and human review. Use multiple task families and later confirmation. More generated patches or a better score on cases the improver has seen is insufficient.

The improver cannot approve its own live promotion, increase its budget, broaden data access, relax SAF/TRU restrictions or rewrite the protected evaluation standard used to judge it. It may propose better verifier tests in a separate track, but the candidate policy cannot succeed by weakening its own judge. Evaluator improvements themselves need separate validation and disposition.

This is controlled software-level RSI. We are not promising autonomous foundation-model training or an unlimited self-improving system.

## 8. A reusable product surface across harnesses

The shared engine should use common contracts while adapters preserve each harness's wire semantics. The names below describe proposed responsibilities; they are not claims that new public endpoints already exist.

| Contract | Product responsibility |
|---|---|
| Capability/profile discovery | Declare supported protocol, identity, observable state, controllable actions and unsupported features |
| Workload/session binding | Authenticate a workload and preserve lineage, policy and constraints |
| Decision and explanation | Accept a versioned state snapshot; return chosen permitted action, actual reason, uncertainty or missingness, versions and attribution ID |
| Execution observation | Receive attributed outcomes and served identity with source provenance; an untrusted hook cannot manufacture a verified label |
| Task completion and evidence | Associate exact output and verifier result with the right attempt; record pending/indeterminate outcomes honestly |
| Policy lifecycle | Propose, evaluate, approve, activate and roll back policy versions through a separately authorized control surface |

A gateway-capable integration can exercise the full model-choice loop. A hook-only integration can contribute observations and display advice but cannot claim ADRL controlled a model request it could not intercept. An unsupported state/protocol profile should fail explicitly rather than flattening away essential reasoning or tool state.

Start with one qualified Messages integration. Use another harness to test whether the contracts truly generalize, then admit Responses separately. The shared product design starts now; full multi-harness claims follow actual qualification.

## 9. Existing ADR tensions to dispose of before implementation

These are proposed clarifications or experiments, not changes already adopted.

| Topic | ADRs | Recommended disposition |
|---|---|---|
| Initial versus mid-task decisions | FND-003, SEM-003, RTG-007, CAS-003 | Resolve the pending RTG-007 amendment. Keep user-turn placement and explicitly permitted safe-boundary reconsideration; avoid rerouting every HTTP request |
| Model capability and transition graph | RTG-001/008, TRU-002, CAS-004 | Retain economic tiers, but qualify concrete deployments and transition edges per task/profile; do not infer capability from tier rank |
| Completion objective | RTG-002/005/009, LRN-003 | Align local turn estimates with complete-task benefit and total cost; dispose of quality floors versus weights explicitly |
| Rules and learned authority | RTG-003/006/007, LRN-006, MEM-008 | Retain current authority gates initially; fix rule-health measurement/refresh and uncertainty. Broader learned authority needs a separate empirical disposition |
| Local-first, stickiness and downshift | RTG-004, CAS-004/005 | Keep current behaviour as a baseline. Compare only qualified alternatives; adopt a changed transition policy only if evidence warrants amending these decisions |
| Operational adaptation and drift | RTG-001/003, LRN-005/006, OPS-003 | Specify admissible outcome sources, snapshot refresh, observation minimums, duplicate handling and model-change requalification |
| RSI ownership and graduation | LRN-005/007, EVL-006/007/009, FND-005 | Version the improver and its search budget; independently compare improvers; preserve explicit promotion. Propose a new ADR only if these existing owners cannot state a coherent contract |
| Evidence infrastructure scope | MEM-001/002/003/005/010, SAF-007 | Complete the minimum trustworthy output/verification path required by the first routing trial; record why any larger isolation or custody extension is necessary |

## 10. Proposed milestones, with a routing demonstration at each exit

| Milestone | Work and relationship to existing waves | Exit demonstration | Stop or course-correct when |
|---|---|---|---|
| **1. Agree the target** | This blueprint, the 77-ADR map and dispositions above; no code work ahead of the discussion | One task walkthrough through all three loops; clear list of fixed and adaptable elements | A proposed feature has no taxonomy owner or measurable product purpose |
| **2. Make decisions understandable** | Resume the bounded W7.0 correction only after disposition; connect real router/controller to a synthetic Messages endpoint | Varied and adversarial tasks show state → permitted choices → chosen action → dispatched action; all before/after changes published | The explanation does not match actual selection, permission is violated, or uncertainty is disguised as confidence |
| **3. Prove the first useful routing loop** | Relevant W3 output attribution, W4 verifier quality and W6 controlled-path scope for one harness; then a narrow W7 comparison | Fixed and adaptive policies independently execute the same starting tasks; show outcome, total effort, time and cost | No interpretable baseline, unreliable verifier, unqualified destination, budget breach or lost side-effect accounting |
| **4. Earn policy adaptation** | Rule-health refresh and qualified evidence; conditional W9 comparative learner with abstention | One evidence-backed policy change improves fresh cases, or a documented rejection keeps the simpler policy | Data gate fails, drift invalidates calibration, held-out gains disappear or quality is traded away beyond the agreed limit |
| **5. Automate improvement proposals** | W10 with a restricted proposal/experiment process | An authorized failure yields a candidate, independent assessment and an accepted or rejected disposition linked to ADRs | The proposer can change its judge, hide failed attempts, enlarge access or self-deploy |
| **6. Test the recursive gain** | W12 compares the improvement process itself | A candidate improver yields more durable accepted routing benefit for equal total budget on fresh work | Extra complexity merely increases proposal count, reviewer work or benchmark overfitting |

**Cross-harness track:** W5 and W8A validate the common contracts alongside this sequence when their entry conditions are met. The first one-harness routing trial need not wait for full second-harness support. Stable release still follows FND-005 and W8B qualification; team/tenancy work stays conditional under W11.

For the first real diagnostic, use narrow task families such as edits, parser fixes and small features, then broaden deliberately to concurrency, security, multi-file work, ambiguous instructions, multilingual/paraphrased requests, long context, provider failure and resumed/child lineages. A development set discovers problems; a fresh confirmation set assesses the proposed remedy. The old roadmap's 30-task diagnostic figure remains a planning starting point, not sufficient statistical evidence by itself.

## 11. What maturity means here

The current programme has tested infrastructure and component routing behaviour. The new 240-decision matrix exposed two prepared mixed-intent failures; it did not execute models. Historical D3 notes in individual ADRs retain their dated scope and do not establish a current learned or trajectory-aware product.

For each affected decision, record four separate facts: direction accepted/proposed; behaviour implemented; evidence actually observed; and formal maturity disposition. One wave cannot increase all four automatically.

| Capability | Evidence needed before calling it more mature |
|---|---|
| Routing mechanism | Correct and explainable selections, boundary behaviour and negative cases for a named profile |
| Routing benefit | Qualified real task outcomes compared with meaningful baselines, including costs and failures |
| Adaptation | A traceable policy change justified by admissible evidence and confirmed on fresh work |
| Learned routing | Adequate data, no leakage, calibration/abstention, comparative gains and approved exposure |
| RSI | Controlled comparison of improvers showing durable downstream gains beyond ordinary policy improvement |

Retain the EVL-007 D1–D5 process: tested scope, organic shadow evidence, bounded approved live exposure and completed pilot are different steps. Planning, module counts and raw test counts do not create a portfolio maturity percentage. No grade changes with this blueprint.

## 12. Decisions for the product discussion

My recommended starting position is:

1. **Adopt the three-loop product target**, with RTG-007 as the architectural anchor and its pending amendment explicitly disposed of.
2. **Keep constraints and graduation fixed while methods adapt.** Automatic runtime routing is allowed inside an approved policy; new policy/improver authority follows the existing release path.
3. **Start with clear, measured routing and a complete task comparison.** Earn a learned scorer and then a temporal estimator through the register's gates; do not equate complexity with progress.
4. **Make every implementation milestone show a routing consequence.** Keep required evidence work, but justify it against the next demonstrable loop.

The next action is discussion and disposition of this target, not another implementation slice. The implementation heartbeat is paused; W7.0a and W3 are held with their evidence intact.

Supporting records: [current routing diagnostic](adrl-routing-in-action-2026-09-08.md), [all-ADR coverage map](research/adaptive-routing-blueprint-2026-09-08/taxonomy-map.md), [source manifest](research/adaptive-routing-blueprint-2026-09-08/sources.json), [execution state](research/adrl-execution-state.json).
