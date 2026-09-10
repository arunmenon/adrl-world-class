# ADRL milestone plan: purpose, guardrails and proof

9 September 2026. Proposed execution sequence grounded in the current product roadmap and Fable retrospective. This is a planning document, not authorization for real payloads, spend or exposure. Individual implementation packets receive Fable pre-critique and post-review. No new wave numbering system or automatic maturity promotion is introduced.

**Destination:** demonstrate that ADRL chooses models that complete developer tasks at worthwhile total cost and latency, learns responsibly from attributable outcomes, and can deliver that behavior across harnesses. We are inside P1, preparing for P2. The RV-01 outcome connection is repaired in offline scope; the rest of the learning loop is not yet qualified.

The dependency sequence is:

P0 discovery alongside engineering → P1 trustworthy evidence and routing → P2 useful first-harness comparison → P3 measured adaptation → P4 reusable integrations → P5 learned policies → P6 improvement automation → P7 RSI.

P0 can run in parallel. Later milestones are commitments to evidence, not promised calendar dates. Engineering dates should be estimated in the bounded packets after their scope, reviewers, access and dependencies are settled. Finishing later-stage components early does not complete those product milestones.

## P0: establish a problem worth solving

**Why:** a technically good router is not a product if developers cannot use it or buyers cannot move enough spend to make it worthwhile.

**Deliverable and test:** product lead leads the roadmap's proposed 12–15 interviews across at least eight organizations, gathering authorized workflow and spending evidence, alternatives and reasons to switch. Record counterexamples, including cases where native routing already solves the problem.

**Guardrails:** no customer names, savings or purchase intent inferred from hypothetical personas. No unapproved outreach, access or data collection by an agent. Keep modeled economics separate from observed costs.

**Exit:** the roadmap's proposed three organizations willing to define a trial, at least two named budget owners, and measurable pain supported by evidence. If not met, revisit the segment rather than fund broader packaging. FND-005 and EVL evaluation commitments frame what we may promise; interviews do not promote technical ADR maturity.

## P1: make the prototype's decisions and evidence dependable

There are three acceptance gates inside P1, not three new product stages.

### Gate A: trustworthy outcome interpretation

**Why:** a router learning from incorrect labels can become more confident in worse choices.

**Already done:** RV-01 now connects cascade-written outcomes to the existing explicitly invoked closer. The regression demonstrates one closed outcome, one pending outcome and no invented success. Fable critique/recheck and final source-matched checks support this narrow claim.

**Remaining deliverables:** make rule-health and learning readers consume the appropriate canonical outcome/label projections; define and honor correction precedence; distinguish task-capability failure from infrastructure, permissions, unknown results and incomplete work. Keep the feature-version admission gap explicit rather than hiding it behind a permissive conversion. Verifier calibration and learning-version admission are separate packets, not prerequisites to pretending the entire loop is complete.

**Tests:** drive a decision through the actual producers and consumers; close it; append later evidence; compare the resulting label across readers. Verify that an authorized correction has its specified effect, infrastructure failure never becomes evidence of model inability, censored rows do not count as completed capability evidence, and replay preserves lineage and order. Test verifier/correction conflicts explicitly. Duplicate delivery and restart must not create duplicate or inconsistent outcomes.

**Guardrails:** append corrections; do not rewrite history. Never infer success from HTTP 200 or task closure. A fresh synthetic ledger is diagnostic evidence, not organic training evidence. No automatic rule refresh or artifact promotion is introduced by a reader repair. New training contracts need their own compatibility and admission review.

**Exit:** the reviewed contract agrees across the consumers in scope on a frozen fault matrix; exclusions remain visible. Record unresolved readers explicitly. Owning ADRs: MEM-001/002/003/004, LRN-001/004/005, RTG-003, CAS-001 as applicable to each packet. Evidence can strengthen scoped D2; it is not real-traffic learning proof.

### Gate B: model selection follows the stated policy

**Why:** three available model tiers are not useful if the implemented decision path ignores its estimator or economic objective.

**Deliverables:** resolve the advisor/estimator fallback contract, make overrides explainable, and retain request/context signals without treating keywords as validated completion probabilities. Keep a non-learned baseline so we can tell whether later complexity helps.

**Tests:** on identical requests, controlled changes to predicted completion probabilities or costs should change the choice when the policy says they should. Test permission restrictions, unavailable destinations, ambiguity, negation, quoted task words, mixed intent and meaningful versus irrelevant context. Use independently authored cases, including cases expected to stay on frontier. Inspect the selected route and actual dispatch together.

**Guardrails:** do not tune thresholds to force a desired middle-tier percentage. No relaxed privacy restrictions, invented calibration, new downshift authority or classifier/model calls. Before evaluation, freeze the policy, expected invariants and acceptable over/under-routing error budget; predicted and measured benefit remain distinct.

**Exit:** selection responds to the declared objective, explanations match execution, and all restricted destinations remain unreachable. Actual model quality remains for P2. Owning ADRs: RTG-002/003/006, LRN-004, CAS transitions and SAF/TRU restrictions. Scoped D2 only.

### Gate C: lab reproducibility and the minimum real-task boundary

**Why:** results that only work in one checkout or through an undisclosed admission bypass cannot support independent decisions.

**Deliverables:** explicit synthetic identity/configuration, a lab configuration whose declared mode matches its execution mode, and a minimal first-harness capture/control profile. Separate synthetic evidence references from production admission. Evaluate the narrower native-harness path before continuing container infrastructure as a supposed prerequisite.

**Tests:** replay the same frozen suite from two different absolute paths using the same declared dependencies and compare normalized decisions, reasons and dispatches. Normalization may remove only declared timestamps/run IDs, never route differences. Exercise stream cancellation, upstream errors, privacy pins and denied destinations. Before real tasks, show the executed model route is attributable to the exact captured output and verifier input.

**Guardrails:** no developer-specific identity grants hidden in defaults. No synthetic approval usable as production evidence. Observation-only integrations are labelled as such. Close actual custody/access gaps for the chosen path; do not bypass them merely by avoiding containers.

**Exit:** another reviewer can reproduce the diagnostic and audit one task's control-to-output chain; the real-task profile still needs the access/evaluation decisions below. Owning ADRs: TRU-001/002, OPS-005/006, SEM-007, MEM-003/005/010, SAF-007 and EVL-005/006. P1 closes only when its applicable controls and evidence gates are met.

## P2: prove value on the first harness

**Why:** only completed real tasks can show whether a model choice was economically useful.

**First checkpoint:** propose five tasks with two independently executed arms, ADRL-controlled choice and fixed frontier, on an authorized repository. These ten runs debug attribution and the experiment process. They do not prove savings or satisfy P2. Use Claude Code first only if its actual route-control, credential and billing profile supports the comparison; native observation alone is insufficient.

**Broader diagnostic:** the roadmap proposes thirty development tasks spanning at least three task families and two repositories, followed by separate confirmation tasks. Examples include a small edit, bug repair, test work and a more involved change. Sample size for a value claim is determined by outcome variability and the predeclared decision criterion, not by treating thirty as sufficient automatically.

**Tests and measures:** equivalent initial task/repository state, pinned harness/model/configuration versions, independently checked artifacts, complete attempts and failures, latency, retries, cache and verification/repair costs. Compare context-aware selection with request-only selection where feasible. Keep held-out confirmation tasks unseen during tuning. Use paired comparisons and report uncertainty and exclusions.

**Guardrails:** named evaluation and security owners; approved repositories, access, retention and finite run/spend limits; a frozen quality criterion and cost basis; halt on a privacy or authority breach. Do not translate subscription list-price telemetry into actual cash savings. Do not weaken the grader to rescue a policy. Planning/PRD/HLD/LLD assessments remain a separate, calibrated evaluation track. Local/current/hindsight baselines required by EVL remain visible; unavailable comparisons are not silently passed or waived.

**Exit:** quality meets the agreed criterion, complete costs show worthwhile net benefit with adequate confidence, and a buyer considers it useful. Insufficient evidence is an inconclusive result. Negative value triggers a bounded diagnosis or product rethink, not unlimited experiments. Own: EVL-001/003/004/006/007, RTG-007, MEM-003/004, OPS-006 and the qualified harness profile. A diagnostic is not D3/D4 graduation.

## P3: prove adaptation, then a repeatable pilot

**Why:** making a good initial choice and improving a task as evidence arrives are different promises.

**Test:** compare initial-choice-only routing with an otherwise equivalent policy that uses admitted progress/failure signals at safe boundaries. Include switching, handoff, cache and verification costs. Demonstrate one legitimate signal changing a later decision and independently verify whether that helped. Test stale, sparse and contradictory feedback, restart and rollback.

**Guardrails:** freeze the allowed signals and transition policy; only narrow permissions; preserve privacy pins; do not train on the current task's future outcome. Keep a fixed incumbent and a withdrawal path. Existing proposed pilot floors of two weeks and 100 eligible attempts do not substitute for quality evidence.

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

## The gate used at every implementation milestone

Codex prepares a bounded packet and source snapshot. Fable critiques it before implementation. Codex implements and records failing-before/passing-after evidence. Fable reviews the resulting source and evidence; material fixes get rechecked. Preserve original findings and disagreements. Limit correction/review loops to two rounds, or any tighter packet limit; unresolved blocking disputes go to the product owner. A missing review is pending, not passed.

Every completion report must name the product behavior, owning ADRs, tested scope, actual versus synthetic inputs, failures/skips, reviewer disposition, remaining gate and rollback/recovery plan. No calendar deadline, passing-test total or agreement between models automatically advances a D grade. Distinguish proposed acceptance targets from approved evaluation contracts.

Immediate next packet: RV-05/RV-06 reader/label consistency, independently critiqued before edits. Work on other unresolved review findings remains visible; this sequence is not a declaration that every existing blocker has been resolved.

Sources: [canonical roadmap](adrl-product-roadmap-2026-09-08.md), [journey brief](adrl-journey-brief-2026-09-09.md), [latest repair](reviews/outcome-contract-2026-09-09/report.md), [retrospective findings](/Users/arunmenon/projects/adrl-review-fable-2026-09-08/findings.md), [EVL-007 graduation rules](../adr/EVL/ADRL-EVL-007.md).
