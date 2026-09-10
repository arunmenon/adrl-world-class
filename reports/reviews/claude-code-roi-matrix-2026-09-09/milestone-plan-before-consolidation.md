# ADRL milestone plan: purpose, guardrails and proof

## Product priority update: Claude Code ROI first, 2026-09-09

Arun explicitly prioritizes Claude Code as ADRL's first consumable product and tangible spend evidence as the next investment checkpoint. Cross-harness reuse remains the architecture direction; additional harness qualification, graph enrichment, learned policies and RSI follow first-harness evidence.

The immediate sequence supersedes the earlier reader-first ordering: (1) prepare a scoped Fable-reviewed compatibility spike, (2) demonstrate actual cheaper-Claude dispatch and thinking/tool continuation through ADRL, (3) if qualified, run five independently authored tasks with two arms, using frozen policy/configuration and live routing decisions, (4) report results and decide whether to invest further. Learning remains off; human-reviewed verifier outputs can label this diagnostic without completing learning-reader repairs. Repair only defects required for correct execution, attribution, verification and applicable safety controls. Register hygiene and unresolved historical dispositions remain visible; no P1 completion is implied.

Budget the compatibility spike at one hour of execution/diagnosis after packet preparation; count the attempted engineering slice within the existing six-slice ceiling. Do not silently extend a failed spike into infrastructure work. A forced cheap choice tests integration only and must not count as a merit-based routing result. Include prior thinking plus a tool/continuation request to exercise switching compatibility; a fresh one-turn answer is insufficient. Retain upstream-reported model identity with its provenance rather than treating the requested model as served proof. Review the existing non-frontier rewrite, which strips thinking/output configuration, cache markers and some tools, before applying it to another Claude deployment. Any behavior amendment must be recorded in owning FND/SEM/CAS ADRs with scoped review.

For the paired diagnostic, preregister task and initial-tree hashes, rule/configuration hashes, harness/model versions, verifier version, attempt limits and checks. Record actual decisions/reasons, upstream model, final-tree hashes, verifier results, full usage/cache categories, retries and latency for both arms. The proposed usage win is: both arms pass every mandatory check with no critical defect, and ADRL uses strictly fewer total reported input-plus-output tokens over the complete attempts. Keep any metered-cost calculation separate and use a frozen applicable rate basis without double-counting cache usage. Criteria remain proposed until their concrete packet is reviewed; the product-priority instruction does not silently sign an unseen experiment contract.

Continue to a larger evaluation if at least two tasks actually use a cheaper model and at least one achieves the paired win. Reconsider if execution control fails, no choices differ, or every cheaper choice fails verification. Incomplete attribution or usage means inconclusive. Five tasks times two arms is ten total task-arm attempts, not ten pairs. This is a feasibility continuation bar, not demonstrated population ROI or release acceptance.

Product reporting separates actual metered charges, estimated API-equivalent cost, subscription usage and fixed subscription fees. Fewer tokens do not establish a lower subscription invoice or more quota. Existing subscription access is the starting path; no silent switch to paid APIs or purchased credits. Measure setup/review/experiment effort separately so the next investment decision includes the cost of obtaining evidence.

Target user experience: reversible Claude Code connection, qualified Claude-to-Claude routing, visible decision and execution attribution, and verified task-level usage/cost reporting. This is product direction and a revised next step, not shipped support, a completed spike, new maturity, or an automation restart.


9 September 2026. Proposed execution sequence grounded in the current product roadmap and Fable retrospective. This is a planning document, not authorization for real payloads, spend or exposure. Individual implementation packets receive Fable pre-critique and post-review. No new wave numbering system or automatic maturity promotion is introduced.

**Destination:** demonstrate that ADRL chooses models that complete developer tasks at worthwhile total cost and latency, learns responsibly from attributable outcomes, and can deliver that behavior across harnesses. We are inside P1, preparing for P2. The RV-01 outcome connection is repaired in offline scope; the rest of the learning loop is not yet qualified.

The dependency sequence is:

P0 discovery alongside engineering → P1 trustworthy evidence and routing → P2 useful first-harness comparison → P3 measured adaptation → P4 reusable integrations → P5 learned policies → P6 improvement automation → P7 RSI.

P0 can run in parallel. Later milestones are commitments to evidence, not promised calendar dates. Engineering dates should be estimated in the bounded packets after their scope, reviewers, access and dependencies are settled. Finishing later-stage components early does not complete those product milestones.

## P0: establish a problem worth solving

**Why:** a technically good router is not a product if developers cannot use it or buyers cannot move enough spend to make it worthwhile.

**Deliverable and test:** product lead leads an initial budget of 12 discovery conversations, seeking coverage across at least eight organizations, gathering authorized workflow and spending evidence, alternatives and reasons to switch. Record counterexamples, including cases where native routing already solves the problem.

**Guardrails:** no customer names, savings or purchase intent inferred from hypothetical personas. No unapproved outreach, access or data collection by an agent. Keep modeled economics separate from observed costs.

**Exit:** the roadmap's proposed three organizations willing to define a trial, at least two named budget owners, and measurable pain supported by evidence. If not met, revisit the segment rather than fund broader packaging. FND-005 and EVL evaluation commitments frame what we may promise; interviews do not promote technical ADR maturity.

**Discovery budget and stop:** checkpoint after eight conversations: if no plausible buyer controls the relevant spend, revise targeting before using the remaining four. At twelve, no confirmed spend-controlling buyer means stop expanding this buyer hypothesis and replan the segment/value proposition. A confirmed buyer is a person whose budget authority and controllable workflow are documented, not inferred from a job title. If a buyer exists but the trial-interest exit is unmet, report that as incomplete; any extension toward the older 12–15 target requires an explicit revised discovery plan. Record who was contacted and what was learned; do not substitute repeated friendly conversations for independent evidence.

## P1: make the prototype's decisions and evidence dependable

There are three acceptance gates inside P1, not three new product stages.

### Gate A: trustworthy outcome interpretation

**Why:** a router learning from incorrect labels can become more confident in worse choices.

**Already done:** RV-01 now connects cascade-written outcomes to the existing explicitly invoked closer. The regression demonstrates one closed outcome, one pending outcome and no invented success. Evidence is in [the repair review folder](reviews/outcome-contract-2026-09-09/report.md), [Fable recheck](reviews/outcome-contract-2026-09-09/recheck.md), and [the recheck source manifest](reviews/outcome-contract-2026-09-09/recheck-manifest.json). SHA-256 of that manifest: `2d6a5f7ee07eb021fe27d5e9d6cd1bbd0004f6002d6a9a0b4fd378ea76da682c`. Fable recheck session: `f47c78bb-b7bb-4462-ac0f-6361ad990242`, a separate local reviewer session from the external retrospective session. [Final checks](reviews/outcome-contract-2026-09-09/checks-2/manifest.json) match all 324 source hashes in that manifest. The reviewer read code/logs; it did not run tests or establish formal human graduation.

**Remaining deliverables:** make rule-health and learning readers consume the appropriate canonical outcome/label projections; define and honor correction precedence; distinguish task-capability failure from infrastructure, permissions, unknown results and incomplete work. Keep the feature-version admission gap explicit rather than hiding it behind a permissive conversion. Verifier calibration and learning-version admission are separate packets, not prerequisites to pretending the entire loop is complete.

**Tests:** drive a decision through the actual producers and consumers; close it; append later evidence; compare the resulting label across readers. Verify that an authorized correction has its specified effect, infrastructure failure never becomes evidence of model inability, censored rows do not count as completed capability evidence, and replay preserves lineage and order. Test verifier/correction conflicts explicitly. Duplicate delivery and restart must not create duplicate or inconsistent outcomes.

**Guardrails:** append corrections; do not rewrite history. Never infer success from HTTP 200 or task closure. A fresh synthetic ledger is diagnostic evidence, not organic training evidence. No automatic rule refresh or artifact promotion is introduced by a reader repair. New training contracts need their own compatibility and admission review.

**Exit:** the reviewed contract agrees across the consumers in scope on a frozen fault matrix; exclusions remain visible. Record unresolved readers explicitly. Owning ADRs: MEM-001/002/003/004, LRN-001/004/005, RTG-003, CAS-001 as applicable to each packet. Evidence can strengthen scoped D2; it is not real-traffic learning proof.

**Register hygiene is part of Gate A, not an optional reporting cleanup.** Inventory all 77 current decisions against the historical baseline and runtime evidence. Review the reported historical D3/D4 carry-over, 21 stale INDEX rows and 11 fields describing previously fixed defects; these counts are reviewer findings to verify, not assumptions that every proposed replacement grade is correct. Apply EVL-007's no-inheritance rule per decision: retain historical wording with its date/source, distinguish the present implementation's supported scope, and leave formal grade disposition explicit.

**Hygiene tests and exit:** build a read-only checker that (1) covers every ADR exactly once in INDEX and its bucket table, (2) compares displayed status/maturity with the canonical current fields, and (3) checks each dated implementation/evidence section against an explicit mapping to INDEX, bucket summary, changelog and a valid evidence link. Equivalent grouped summaries may satisfy mapping; merely containing the date does not. Test missing rows, stale evidence mapping, contradictory grade display and broken links. A human evidence pass is still needed: a script cannot establish D3/D4 from wording. Resolve or explicitly disposition every current-grade conflict and amend misleading self-review wording before P1 completion. Keep prior evidence immutable.

### Gate B: model selection follows the stated policy

**Why:** three available model tiers are not useful if the implemented decision path ignores its estimator or economic objective.

**Deliverables:** resolve the advisor/estimator fallback contract, make overrides explainable, and retain request/context signals without treating keywords as validated completion probabilities. Keep a non-learned baseline so we can tell whether later complexity helps.

**Estimator disposition:** the current linear band heuristic remains an uncalibrated baseline. The frozen review reports zero middle-tier-on-merit choices in 720 decisions, not evidence of middle-tier economics. Do not carry middle-tier savings into P2 assumptions while that remains true. The selection packet must either introduce a versioned recalibration/replacement with documented assumptions and threshold-reachability tests, or explicitly document that this baseline cannot select the middle tier on merit and restrict its product/economic claims accordingly. Changing numerical outputs is not empirical calibration without outcome evidence.

**Tests:** on identical requests, controlled changes to predicted completion probabilities or costs should change the choice when the policy says they should. Test permission restrictions, unavailable destinations, ambiguity, negation, quoted task words, mixed intent and meaningful versus irrelevant context. Use independently authored cases, including cases expected to stay on frontier. Inspect the selected route and actual dispatch together.

**Guardrails:** do not tune thresholds to force a desired middle-tier percentage. No relaxed privacy restrictions, invented calibration, new downshift authority or classifier/model calls. Before evaluation, freeze the policy, expected invariants and acceptable over/under-routing error budget; predicted and measured benefit remain distinct.

**Positive acceptance bar:** a golden integration test must replace the estimator with a declared constant estimator, hold request, allowed destinations, costs and configuration fixed, and change at least one initial decision. Record the exact case and before/after reason; the constant is chosen before evaluation, not after seeing a desired answer. If the selected scope intentionally excludes the estimator, it cannot pass this bar as the promised estimator-driven router.

Publish a dated middle-tier-on-merit measurement on the original frozen prompts with policy/source hashes, numerator and denominator, and per-case traces. Report distinct prompt/condition cells separately from repeats. “On merit” means initial selection by the declared policy while frontier was also permitted and available; exclude forced fallback, restriction ceilings and later cascade escalation. Compare with the frozen zero baseline. A positive rate is a reachability check, not proof of optimality; zero requires the explicit restricted estimator/economic disposition above, not hidden threshold tuning.

**Exit:** the golden sensitivity test passes, tier reachability and the dated merit rate are reported with the estimator disposition, explanations match execution, and all restricted destinations remain unreachable. Actual model quality remains for P2. Owning ADRs: RTG-002/003/006, LRN-004, CAS transitions and SAF/TRU restrictions. Scoped D2 only.

### Gate C: lab reproducibility and the minimum real-task boundary

**Why:** results that only work in one checkout or through an undisclosed admission bypass cannot support independent decisions.

**Deliverables:** explicit synthetic identity/configuration, a lab configuration whose declared mode matches its execution mode, and a minimal first-harness capture/control profile. Separate synthetic evidence references from production admission. Evaluate the narrower native-harness path before continuing container infrastructure as a supposed prerequisite.

**Tests:** replay the same frozen suite from two different absolute paths using the same declared dependencies and compare normalized decisions, reasons and dispatches. Normalization may remove only declared timestamps/run IDs, never route differences. Exercise stream cancellation, upstream errors, privacy pins and denied destinations. Before real tasks, show the executed model route is attributable to the exact captured output and verifier input.

**Guardrails:** no developer-specific identity grants hidden in defaults. No synthetic approval usable as production evidence. Observation-only integrations are labelled as such. Close actual custody/access gaps for the chosen path; do not bypass them merely by avoiding containers.

**Exit:** another reviewer can reproduce the diagnostic and audit one task's control-to-output chain; the real-task profile still needs the access/evaluation decisions below. Owning ADRs: TRU-001/002, OPS-005/006, SEM-007, MEM-003/005/010, SAF-007 and EVL-005/006. P1 closes only when its applicable controls and evidence gates are met.

## P2: prove value on the first harness

**Why:** only completed real tasks can show whether a model choice was economically useful.

**First checkpoint:** five independently authored tasks with two independently executed arms, ADRL-controlled choice and fixed frontier, on an authorized repository. The implementer may clarify the contract but does not write the evaluation tasks or their reference answers. Use Claude Code first only if its actual route-control, credential and billing profile supports the comparison; native observation alone is insufficient.

**Pre-run contrast gate:** freeze the task set, router/policy and dependency versions. In a dry selection pass, at least two of the five tasks must select a permitted, actually available cheaper tier on the router arm, with frontier available for comparison. A nominal tier label with no controllable deployment does not count. If all tasks choose frontier, do not spend ten runs comparing identical arms. Return to the selection/design gate; do not tune the router on these five tasks to manufacture contrast. Purposefully selecting contrasting cases makes this a diagnostic sample, not a representative savings estimate.

Before execution, the named human evaluation reviewer approves the frozen quality criterion, verifier/version, critical-defect rules and handling of indeterminate results. Both arms use the exact same harness version, tools, permission/mode profile and equivalent initial repository state. Record model/deployment versions and any unavoidable difference. Use native harness execution plus W3.1 capture and snapshot verification; attribution remains `operator_capture`, not an unsupported container-owned task-close claim. Prove selected model control separately and link route, attempt, capture and verifier input. Learning stays off.

**Required result wording:** “Ten diagnostic runs for attribution and experiment-process validation; not an efficacy or savings estimate.” Retain per-run cost/usage facts but do not publish a generalized savings headline from these selected cases.

**Broader diagnostic:** the roadmap proposes thirty development tasks spanning at least three task families and two repositories, followed by separate confirmation tasks. Examples include a small edit, bug repair, test work and a more involved change. Sample size for a value claim is determined by outcome variability and the predeclared decision criterion, not by treating thirty as sufficient automatically.

**Tests and measures:** equivalent initial task/repository state, pinned harness/model/configuration versions, independently checked artifacts, complete attempts and failures, latency, retries, cache and verification/repair costs. Compare context-aware selection with request-only selection where feasible. Keep held-out confirmation tasks unseen during tuning. Use paired comparisons and report uncertainty and exclusions.

**Guardrails:** named evaluation and security owners; approved repositories, access, retention and finite run/spend limits; a frozen quality criterion and cost basis; halt on a privacy or authority breach. Do not translate subscription list-price telemetry into actual cash savings. Do not weaken the grader to rescue a policy. Planning/PRD/HLD/LLD assessments remain a separate, calibrated evaluation track. Local/current/hindsight baselines required by EVL remain visible; unavailable comparisons are not silently passed or waived.

**Exit:** quality meets the agreed criterion, complete costs show worthwhile net benefit with adequate confidence, and a buyer considers it useful. Insufficient evidence is an inconclusive result. Negative value triggers a bounded diagnosis or product rethink, not unlimited experiments. Own: EVL-001/003/004/006/007, RTG-007, MEM-003/004, OPS-006 and the qualified harness profile. A diagnostic is not D3/D4 graduation.

## P3: prove adaptation, then a repeatable pilot

**Why:** making a good initial choice and improving a task as evidence arrives are different promises.

**Test:** compare initial-choice-only routing against (a) trajectory-aware escalation and (b) a separately authorized downshift-capable policy. The downshift arm tests the research-motivated hypothesis that a stronger initial model can hand simpler later work to a cheaper permitted model; it is not assumed to win. Freeze when each transition is eligible, carryover/context conditions and matched task starts. Include switching, handoff, cache and verification costs. Demonstrate one legitimate signal changing a later decision and independently verify whether that helped. Test stale, sparse and contradictory feedback, restart and rollback.

**Guardrails:** the current sticky-up-only policy remains the incumbent. Downshift requires explicit experimental disposition of RTG-004/CAS-004/CAS-005 and its safety tests before execution; adding an arm to this plan does not authorize it. Freeze the primary-paper claim and applicability in the pre-wave packet. If downshift is not admitted, report P3 coverage as escalation-only, not as a complete adaptation comparison. Freeze allowed signals and transition policy; only narrow permissions; preserve privacy pins; do not train on the current task's future outcome. Keep a fixed incumbent and a withdrawal path. Existing proposed pilot floors of two weeks and 100 eligible attempts do not substitute for quality evidence.

**Exit:** adaptation shows durable net value, and an approved limited pilot meets its evaluation and commercial gates. RTG-003/007, CAS-003/004/005, MEM-004/007/008, LRN-004/005 and EVL-007 own the evidence. D3 and D4 require their actual shadow/pilot gates and approvals.

## P4: prove reuse across harnesses

**Why:** the intended product must integrate without rewriting its intelligence and evidence model for every harness.

**Test:** qualify a second harness, proposed OpenCode, against the same task and evidence contracts. Keep harness mode, effective permissions, model capabilities and protocol separate. Test identity, streaming, cancellation, state continuity, errors, capture and upgrades. Responses/Codex requires its own protocol admission.

**Guardrails and exit:** unsupported combinations stay explicit. Two adapter files are not proof of support. The roadmap's two-harness/two-protocol gate and integrator usability test must be met before a stable API claim. FND-005, SEM-007, TRU-001 and MEM provenance own this work.

## P5: produce a genuinely better learned checkpoint

**Why:** replace or augment handcrafted choices only when learning improves them.

**Test:** train from admitted outcomes; compare a small capability table/estimator with the current policy and fixed baselines on unseen repositories, sessions and later time periods. Measure calibration, abstention, coverage and total inference/evaluation cost. Separately test context-graph retrieval against simpler retrieval and no retrieval. Pin evidence, feature, model and harness compatibility.

**Guardrails and exit:** no future-outcome leakage, cross-developer export without authorization, or synthetic-to-organic relabeling. A signed compatible candidate must pass independent qualification and rollback checks. Release authority remains outside the learner. LRN-001–008, MEM-005/007/008/010, RTG-007 and EVL gates apply. If learning adds no net benefit, retain the simpler router.

## P6–P7: improve the improvement process, then test RSI

**Why:** automation is worthwhile if it reduces the total cost of obtaining durable improvements.

**P6 test:** compare manual improvement cycles with automated failure grouping and candidate proposals, including rejected candidates and reviewer effort. **P7 test:** compare improver A and B starting from the same incumbent with equivalent permitted evidence and equal total budgets; judge their resulting policies on independent fresh tasks and later windows.

**Guardrails:** the improver cannot change its own judge, protected holdout, permission rules, privacy controls, budget or release authority. A verifier change is independently evaluated. Preserve failed searches and stop if evaluation/review cost erases gains.

**Exit:** repeated independently accepted routing benefit per total improvement cost, not one successful self-edit. RSI may be rejected while the underlying routing product remains valuable. LRN-007, EVL-002/006/007/009 and OPS-002/007 own the relevant authority and evidence.

## Human ownership and unresolved historical decisions

| Responsibility | Named owner / state | First required action |
|---|---|---|
| Product and authorization decisions | Arun Menon | Disposition the two historical issues below and approve applicable P2 scope/budget. |
| Implementation, evidence and handoff | Codex | Prepare bounded packets; preserve failures and reconcile findings. |
| Independent model critique | Claude Fable 5.1, recorded session per review | Critique plan and source/evidence; no human graduation authority. |
| Human evaluation reviewer | Arun Menon, named by the user on 2026-09-09; assisted by coding agents | Review the agent-prepared P2 quality/verifier packet and record the criteria disposition before runs. |
| Human security reviewer | Arun Menon, named by the user on 2026-09-09; assisted by coding agents | Review the agent-prepared access/custody/retention/rollback packet and record the security disposition before runs. |

Both roles are now assigned to the same named person, not two independent people. Coding agents prepare criteria, author tasks independently of the implementer, inspect evidence and propose dispositions; Arun owns the final human decision. Record agent identities, conflicts and the user's actual decision, not a presumed sign-off from silence or naming the roles. Reviewer appointments are complete; P2 criteria/security/run dispositions are still pending. Routine offline repair can proceed within existing authority. EVL-007's later outside-team review and graduation requirements remain distinct and are not waived by this appointment. If Arun does not meet a later independence requirement, that gate needs another qualified reviewer or an explicitly approved amendment before exposure.

**Owner decision 1 — historical “validated” labels (RV-13):** proposed disposition is to preserve each result and log, but identify it as technical self-review and its exact tested scope, without independent acceptance or inherited graduation. Keep the documented disagreement over whether W0 prohibited local engineering; do not erase contrary scope text. Review each of the 21 entries before applying the qualification. Product-owner disposition remains pending; Codex does not unilaterally clear the reviewer's blocking claim.

**Owner decision 2 — W3.2b2d2 deviations (RV-29):** proposed disposition is to retain its pinned synthetic engineering evidence, mark the stop-rule/maintenance exceptions explicitly, and withhold a policy-compliant closure claim or use as real-harness qualification until the product owner dispositions the deviations. Do not retroactively call a self-granted exception authorized. Park container expansion outside the critical path to the first P2 diagnostic. Owner disposition remains pending and visible at the P1 trust gate.

## Effort budget and mandatory replanning

Starting with the next authorized slice, allow **six additional bounded engineering slices** to reach the first ten attributed P2 diagnostic outcomes or stop and replan. RV-01 is already complete and is not counted again. Intended allocation: reader consistency; selector; portable lab; register hygiene; native capture/control qualification and dry run; ten-run diagnostic. This is a resource ceiling, not a claim each item fits one slice. Security-critical dependencies may require more work, which triggers replanning rather than a shortcut.

Each attempted slice counts, including unsuccessful work; renaming or splitting a slice does not reset the counter. Cap correction/review rounds at two per slice or the tighter existing limit. Record planned/used slices, attempts, model-review usage and remaining budget in the journey. Reviewer/approval waiting does not justify starting unrelated new infrastructure. At the end of slice two, missing criteria/security dispositions or access must be escalated as an explicit product decision; the reviewer roles themselves are now assigned. At slice six, absent ten attributed outcomes means no seventh slice without an explicit revised plan: continue with a justified larger budget, narrow the pilot, or stop. An approval block cannot be treated as approval merely because the budget is exhausted.

The ten runs themselves have a hard budget of ten top-level task-arm attempts; failed or interrupted attempts are retained and consume it. Tool/model calls and any within-attempt repairs have separate declared limits and cost accounting in the packet. If ten attempts do not yield ten attributable terminal records, stop for diagnosis and request a separately bounded retry packet rather than silently replacing failures. Cost/usage ceilings are fixed in the P2 packet after confirming the subscription/control profile; this planning budget does not authorize API billing. Discovery has the separate twelve-conversation budget above.

## The gate used at every substantive implementation milestone

Routine review is scoped to changed behavior and its dependencies. Small documentation or mechanical edits use proportionate checks; they do not trigger a full retrospective. Full roadmap/all-ADR review happens at milestone or explicit retrospective checkpoints.

Codex prepares a bounded packet and source snapshot. Fable critiques it before implementation. Codex implements and records failing-before/passing-after evidence. Fable reviews the resulting source and evidence; material fixes get rechecked. Preserve original findings and disagreements. Limit correction/review loops to two rounds, or any tighter packet limit; unresolved blocking disputes go to the product owner. A missing review is pending, not passed.

Every completion report must name the product behavior, owning ADRs, tested scope, actual versus synthetic inputs, failures/skips, reviewer disposition, remaining gate and rollback/recovery plan. No calendar deadline, passing-test total or agreement between models automatically advances a D grade. Distinguish proposed acceptance targets from approved evaluation contracts.

Immediate next packet: RV-05/RV-06 reader/label consistency, independently critiqued before edits. Work on other unresolved review findings remains visible; this sequence is not a declaration that every existing blocker has been resolved.

Sources: [canonical roadmap](adrl-product-roadmap-2026-09-08.md), [journey brief](adrl-journey-brief-2026-09-09.md), [latest repair](reviews/outcome-contract-2026-09-09/report.md), [retrospective findings](/Users/arunmenon/projects/adrl-review-fable-2026-09-08/findings.md), [EVL-007 graduation rules](../adr/EVL/ADRL-EVL-007.md).
