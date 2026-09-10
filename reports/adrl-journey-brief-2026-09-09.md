# ADRL journey: product position and maturity

9 September 2026. Grounded in the current execution state, roadmap, Fable retrospective and latest reviewed repair. The 324 current runtime inputs match the final passing check manifest.

**We are building and repairing the prototype at P1, preparing for P2. We have not yet demonstrated that ADRL delivers better real-task economics or improves its routing from experience.** The latest repair is useful progress because it reconnects the first part of the evidence loop. It does not complete that loop.

The product destination remains: a developer asks for work; ADRL considers the request, permitted context and previous experience; it chooses a suitable model; it records attributable results; qualified offline learning produces better routing policies. Reuse across harnesses follows evidence on the first harness. RSI comes later, when we can test whether the process that improves those policies is itself improving.

## What the journey has accomplished

We built the control and evidence foundation: request handling, privacy restrictions, routing decisions, escalation, session records and verification/capture components. One real Claude Code observation pilot supplied harness observations; it did not demonstrate ADRL controlling model selection. The APIs and integration contracts remain preview work, not proven broad harness support.

We then built a synthetic lab to make routing visible. It exposed mixed-intent problems: a request to rename something and redesign an algorithm could be treated as easy. A keyword extraction correction changed those choices in diagnostic cases. This was an engineering correction, not learned routing or demonstrated model-quality improvement. The review subsequently exposed lab portability and admission limitations that remain open.

Fable's retrospective challenged whether these pieces worked together. It found a real break: the cascade recorded outcomes using names the closing and labeling code did not recognize. It also found that an estimator's selection can be discarded and that the lab depends on the author's path. This changed our immediate priority from more infrastructure and task packs to repairing the adaptive-routing chain.

The latest completed slice repairs that outcome connection. Fable critiqued the plan, reviewed the implementation and rechecked additional tests. It found no remaining material blocker for RV-01's limited scope. Other retrospective findings remain open.

## A concrete example of what changed

The test sends two synthetic requests, including “Fix the typo in README.md.” No coding model solves the task.

| What happens | Before repair | After repair |
|---|---|---|
| First request makes a routing decision | Recorded | Recorded |
| Next user request ends the earlier turn | Written in a format the closer missed | Visible to the existing closer |
| We explicitly run the closer after the waiting window | Earlier route is not found | Earlier route closes once; the newer route remains pending |
| We ask whether the earlier task succeeded | No trustworthy result | Still unknown; closure does not invent success |

Why this matters: ADRL must distinguish “the turn ended,” “the work succeeded,” and “this proves a model is capable.” Otherwise a learner can improve the wrong behavior. MEM-002 owns closure; MEM-004 owns that distinction between useful capability evidence and other outcomes.

## Roadmap position

| Stage | Product question | Current evidence and gate |
|---|---|---|
| P0: Validate demand | Who needs this enough to adopt and pay? | No customer-validation evidence established by the review. Discovery can proceed alongside engineering. |
| P1: Visible, dependable routing | Can we see and trust what ADRL does? | Current engineering focus. Synthetic decisions and one repaired outcome connection exist; selector, lab and remaining evidence defects prevent declaring P1 complete. |
| P2: Value on one harness | Is routing worthwhile on real work? | Not demonstrated. Requires an attributed comparison against a fixed frontier baseline, with quality, total cost and latency. |
| P3: Adaptation and pilot | Does reacting to experience improve results? | Not demonstrated. Manual rule edits and existing escalation logic do not establish this. |
| P4: Reusable integrations | Does the same product work across harnesses? | Contracts exist; second-harness and protocol qualification remain open. |
| P5: Learned policies | Can admitted outcomes produce a better router? | Some machinery exists; evidence readers, calibration and version admission remain blocked. No qualified learned checkpoint demonstrated. |
| P6–P7: Improvement process and RSI | Can we improve how ADRL improves, then scale it? | Planned. Needs a measured policy-improvement loop first. |

An engineering label such as W3 or W7 names a work package, not a completed product stage. Work on later components has not put us at P7.

## What this means for taxonomy maturity

The taxonomy is our set of architectural commitments. The roadmap describes which customer outcomes we pursue and in what order. Maturity records how convincingly each commitment has been demonstrated.

In plain language, D1 means code exists; D2 means the promised behavior has appropriate tests; D3 needs evidence from real traffic without affecting execution; D4 needs a qualified limited pilot; D5 requires the defined graduation evidence and approvals. EVL-007 contains the actual gates. These apply to individual decisions and tested scopes, not to the product as a single average score.

| Taxonomy area | What we can substantiate now | What is not yet substantiated |
|---|---|---|
| MEM-001/002: decision and outcome records | The latest composed offline test connects cascade-written events to explicit closure; route/event identity is preserved. Stronger scoped D2 evidence. | Historical-row recovery, automatic closing and the full real-traffic lifecycle. |
| MEM-004: meaningful outcome labels | Unknown results and tested infrastructure failures stay outside capability evidence. | Correct behavior across all correction/readiness/learning consumers and organic failure types. |
| RTG-002/003/006: model selection | Diagnostic decisions and a lexical correction exist. | The shipped decision path reliably honors the intended estimator/economic policy; better real-task choices. |
| LRN-001/004/005: learning evidence and versions | Features and compatibility safeguards exist. | An admitted, trustworthy outcome-to-learning pipeline and a better checkpoint derived from it. |
| CAS and SAF/TRU: transitions and restrictions | Numerous scoped tests support parts of these controls. | Whole-bucket or production safety qualification; a passed case is not blanket readiness. |
| FND-005 / SEM-007: product integration | Preview APIs and a Messages-oriented implementation exist. | Stable cross-harness interoperability and Responses qualification. |
| EVL-007: evidence and graduation | A real Fable critique/recheck now accompanies this repair. | Formal graduation or replacement of required human/evaluation/security roles. |

**No formal maturity grades were raised by this repair. That does not mean zero progress:** a previously disconnected behavior now has source-backed integration evidence and a reviewer disposition. The register still needs a separate reconciliation of historical grades and stale fields. Historical D3/D4 values must not be read as proof for this new implementation, and the reviewer's suggested grades are recommendations, not automatic promotions.

## What happens next

1. Repair the remaining label-reader connections, especially rule-health consumption and corrections (RV-05/RV-06). Keep verifier calibration and learning-version admission explicit.
2. Make the selector follow its declared policy and make the lab reproducible without hidden admission assumptions (RV-02/03/04). Do not tune simply to force a desired model-tier distribution.
3. Run a bounded real-task comparison on the first qualified harness. Demonstrate actual model control, attributable output and independently assessed quality; native observation alone is insufficient.
4. Only then claim adaptation, expand harness qualification and pursue learned checkpoints, context-graph gains or RSI on measured evidence.

Each substantive slice follows: plan, Fable critique, implementation and tests, Fable evidence review, corrections/recheck, then roadmap and ADR evidence update. This is development discipline, not product RSI.

**A defensible leadership statement:** “We have a working technical foundation and a repeatable way to inspect routing. Independent review exposed important integration defects, and the first critical defect is repaired. Our next investment milestone is a controlled demonstration of routing value on real developer tasks. Savings, broad harness support and self-improvement remain hypotheses.”

Validation is supporting evidence: the final build has 922 passing tests, eight skipped engine cases and eleven passing engineering checks. These are software checks, not 922 solved coding tasks. Fable reviewed source and logs; it did not independently execute those tests.

Sources: [product roadmap](adrl-product-roadmap-2026-09-08.md), [journey](adrl-implementation-journey.md), [execution state](research/adrl-execution-state.json), [repair and critiques](reviews/outcome-contract-2026-09-09/report.md), [formal maturity gates](../adr/EVL/ADRL-EVL-007.md), [Fable retrospective](/Users/arunmenon/projects/adrl-review-fable-2026-09-08/review.md).
