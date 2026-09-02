# ADRL-MEM-004 — Cause-typed labels, six types not four

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested for the enum and its unit tests; the claim that the typing is *complete* is D0 — no organic failure corpus has been coded against it |
| Review verdict | AMEND |
| Tenets | 2, 8 |
| Related decisions | CAS-001, CAS-002, CAS-006, SAF-005, SAF-006, MEM-002, MEM-003, LRN-001, LRN-003, LRN-004, EVL-004, EVL-009 |
| Open questions | Q2, Q6 |

## Decision

Training labels keep task difficulty (`task_capability`) separate from every other failure cause — `harness_dialect`, `infrastructure`, `policy_constraint`, `context_feasibility`, `user_abort` and `unverifiable` — and only `task_capability` outcomes are evidence about a rung's ability; every label carries the typing rule version, a confidence, and the trip-wire or verifier event that produced it, and a label whose cause cannot be determined is typed `unverifiable`, never defaulted to `task_capability`.

1. **The enum is versioned and open.** The list above is `failure-types-v2`. Adding a type is a new version with an upcaster (MEM-001); removing or merging types is prohibited because it would silently re-pool causes in replay.
2. **Ambiguity is a type, not a tie-break.** When a turn shows both a dialect failure (malformed edit block) and a wrong answer, the label is `harness_dialect` with `secondary=task_capability`; the primary is the cause that occurred first in the action sequence. A label with no determinable cause is `unverifiable`.
3. **Excluded types never reach the capability estimator.** `infrastructure`, `policy_constraint`, `context_feasibility`, `user_abort` and `unverifiable` are retained in the ledger (they are evidence for OPS, SAF and SEM) but are filtered before any LRN objective and reported separately in EVL.

## Context and rationale

This is the single most important decision for whether learning can ever work. "The local model failed" is usually several different statements: the task was too hard; the model could not emit the harness's exact-string edit format; the endpoint was down; the privacy pin blocked the route; the context did not fit; the developer hit Ctrl-C; nobody could tell. Only the first is evidence about capability. If the rest are pooled into it, a trained router learns to avoid the local rung for reasons unrelated to its ability — permanently and invisibly, because the training signal says "local fails here" and nothing will ever route there again to discover otherwise. CAS-002 makes the same distinction at the trip-wire layer; this decision enforces it where labels are minted.

The amendment brings the decision text into line with the code (`outcomes.py` already has six types, not four), adds the one type the code is missing and the agent-failure literature considers first-order (context/feasibility overflow), and — more importantly — makes the label carry its own provenance and confidence. A cause-clean label that cannot say which rule assigned it, at what confidence, is not cause-clean; it is a guess with a good name.

## Adversarial review (2026-09-02)

### Steelman
Every published router trained on outcome data implicitly assumes outcomes reflect model capability; in an agentic setting that assumption is false most of the time (tool errors, format failures and environment issues dominate small-model failures). Typing the cause at the source is the only cheap point to do it, and it is the only way the local rung can ever earn its way into harder work rather than being ratcheted out by infrastructure noise.

### Attacks
1. **The decision text and the code disagree, and the text is wrong.** The register says four causes; `outcomes.py` has six (`user_abort`, `unverifiable` added). The two extra types are the ones most likely to be mislabelled as capability failures — an interrupted turn looks like a failed turn; an unverifiable turn gets whatever the observer guessed. A decision whose enumerated set is stale in its own repo cannot claim its typing is complete.
2. **Context/feasibility overflow has no home.** SAF-005/006 remove rungs whose context cannot hold the request *before* routing; but a turn that starts feasible can overflow mid-episode as tool output accumulates. In a recent long-horizon coding benchmark, context overflow was the single largest failure mode for one frontier model (35.6%) and tool errors the largest for a small open model (42%). Under the four-way scheme this is either "infrastructure" (wrong: the endpoint was fine) or "task_capability" (wrong: the rung's window, not its reasoning, failed). It needs its own type because the correct owner is SEM/SAF (context budgeting), not LRN.
3. **The label has no provenance or confidence, so it cannot be audited or re-derived.** The register notes the SDLC intent taxonomy has "no version/confidence/correction history in MEM"; the same is true of failure types. Confident-learning methods for finding label errors need a per-label noisy-label model; a bare enum value cannot be re-scored. If the typing rule changes (and it just did, four → six), previously minted labels cannot be re-typed without the originating event.
4. **Mixed causes are common and the decision offers no precedence.** A local model that emits a malformed edit block *and* would have produced the wrong edit is the normal case, not the edge case; the failure taxonomies for agent systems put "task verification" and "specification/format" failures alongside reasoning failures precisely because they co-occur. Without a stated precedence (first-occurring cause wins; secondary recorded) two annotators — or two versions of `tripwires.py` — will type the same trace differently.
5. **Default-to-capability is the failure mode, and nothing forbids it.** When no trip-wire fires and no verifier runs, the natural implementation typing is "the model answered, so any later failure is capability". The decision must say the default is `unverifiable`, or the corpus will be dominated by confident, wrong capability labels — which the label-error literature shows is enough to flip which model looks better.
6. **Is `harness_dialect` really not capability?** A counter-attack from the other side: the ability to follow the exact-string edit format *is* a capability of the model on this harness, and the register admits mixed-whitespace edits on the production local model are untested. If dialect failures are excluded from the capability estimator, the estimator will over-recommend a local rung that cannot actually drive Claude Code. The answer is that dialect is a (rung × harness) property, learnable separately and fixable by prompt/format engineering, so it should not be pooled — but it must still gate the local rung's eligibility per harness (RTG/CAS), and the decision should say that exclusion from the *estimator* is not exclusion from *routing policy*.

### Evidence
- M. Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2503.13657, 2025) — MAST taxonomy: 14 failure modes in 3 categories (system design, inter-agent misalignment, task verification) from 1,600+ annotated traces across 7 frameworks, κ=0.88 inter-annotator agreement; shows verification/format failures are a distinct, large class from reasoning failures (attacks 2, 4) — https://arxiv.org/abs/2503.13657
- Scale AI, "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" (arXiv 2509.16941, 2025) — per-model failure breakdown: Claude Sonnet 4 context overflow 35.6% primary failure; Qwen3-32B tool-error rate 42%; frontier models fail on wrong solutions, small models on operational mechanics (tool use, syntax, context); directly supports a `context_feasibility` type and the dialect/capability split (attacks 2, 6) — https://arxiv.org/html/2509.16941v1
- C. Northcutt, L. Jiang, I. Chuang, "Confident Learning: Estimating Uncertainty in Dataset Labels" (JAIR 2021) — estimates the joint of noisy and true labels under class-conditional noise to find and prune label errors; needs per-example predicted probabilities, i.e. a label confidence, which the bare enum lacks (attack 3) — https://arxiv.org/abs/1911.00068
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021) — ≥3.3% average test-set label error; on ImageNet with corrected labels, ResNet-18 outperforms ResNet-50 "if the prevalence of originally mislabeled test examples increases by just 6%"; a few percent of mis-typed capability labels is enough to invert a rung comparison (attack 5) — https://arxiv.org/abs/2103.14749
- OpenAI, "Introducing SWE-bench Verified" (2024) — 68.3% of samples had a severe issue (underspecified, invalid tests, env failures); "the verifier failed" is frequently not "the model failed" (attack 5, and MEM-003) — https://openai.com/index/introducing-swe-bench-verified/
- X. Zhou et al., "TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks" (arXiv 2412.14161, 2024) — best agent completes 30% of tasks autonomously; long-horizon tasks remain out of reach. Fetched abstract does not enumerate failure categories, so it is cited only for the horizon effect — https://arxiv.org/abs/2412.14161

### Verdict
**AMEND.** Attack 1 is a plain text/code mismatch and must be fixed. Attacks 2, 3 and 5 land and are each structural: a missing feasibility type, no per-label provenance/confidence, and no safe default. Attack 4 is answered by a precedence rule (clause 2). Attack 6 is a genuine tension; the amendment resolves it by distinguishing "excluded from the capability estimator" from "excluded from routing eligibility", which keeps CAS-002's ownership routing intact. The four-way typing was not complete; the six-way typing in code is closer but still lacks feasibility and provenance.

## Amendments applied

- Enumerated seven types (six from `outcomes.py` plus `context_feasibility`) in the decision text; declared the set versioned as `failure-types-v2`.
- Added: every label carries rule version, confidence and originating event id.
- Added: undeterminable cause → `unverifiable`, never `task_capability` by default.
- Added precedence rule for mixed causes (first-occurring primary, secondary recorded).
- Added clause 3: excluded types retained for OPS/SAF/SEM but filtered before any LRN objective; rationale states that exclusion from the estimator is not exclusion from routing policy.

## Follow-ups

- [ ] Add `context_feasibility` to `outcomes.py`; write the v1→v2 upcaster and a replay test.
- [ ] Add `label_rule_version`, `label_confidence`, `source_event_id`, `secondary_type` to the label projection; golden test that a label with no trip-wire and no verifier is `unverifiable`.
- [ ] Golden test for precedence: trace with malformed edit block followed by wrong edit → primary `harness_dialect`, secondary `task_capability`.
- [ ] Hand-code 100 organic failures (when they exist) against `failure-types-v2` with two annotators; report κ and the residual "other" rate. If "other" > 5%, the enum is still incomplete.
- [ ] Confirm `learning_readiness.py` counts only `task_capability` outcomes toward the EVL-004 threshold and reports excluded-type counts separately.
- [ ] RTG/CAS: confirm that `harness_dialect` failure rates per (rung, harness) feed local-rung eligibility even though they are excluded from the estimator.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: enum expanded to match code plus `context_feasibility`; labels carry version/confidence/provenance; precedence and safe-default rules added | "Training labels keep task difficulty separate from dialect/capability, infrastructure, privacy and policy failures." |
