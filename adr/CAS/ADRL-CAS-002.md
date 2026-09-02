# ADRL-CAS-002 — Typed failures, versioned enum, measured attribution

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (typing is implemented and tested; attribution precision against human labels is not yet reported and is added as a gate before these labels feed LRN) |
| Review verdict | AMEND |
| Tenets | 8 |
| Related decisions | CAS-001, CAS-006, CAS-007, MEM-002, MEM-004, LRN-001, SAF-004, RTG-008, EVL-004 |
| Open questions | Q6, Q7 |

## Decision

Failures are typed as task capability, harness dialect, infrastructure, policy constraint, context feasibility, user abort, or unverifiable — the six types implemented in `outcomes.py` plus `context_feasibility`, together versioned as `failure-types-v2` (MEM-004) — with a versioned precedence rule for ambiguous cases, an explicit `unverifiable` default rather than a guessed cause, and a measured attribution precision against human labels before any type is used as a training signal.

1. Precedence when several causes are plausible: `policy_constraint` > `context_feasibility` > `infrastructure` > `harness_dialect` > `task_capability`; a failure that cannot be placed with the rule is `unverifiable`, never `task_capability` by default (the poisoning direction MEM-004 guards against).
2. `infrastructure` includes gateway-internal failover and within-rung model substitution (RTG-008 clause 2), rate limits and timeouts; a context-window rejection or a request that could not fit the rung's window is `context_feasibility` (a SAF-006 signal, never a capability signal); a timeout on a slow local engine is `infrastructure` unless a verifier shows the partial output was wrong.
3. `harness_dialect` is scoped to *format* failures (schema-invalid tool call, exact-string edit that does not match, malformed JSON) and carries the harness id and tool name; whether the *same* model would have succeeded with a different dialect is a counterfactual question (LRN-002), not an inference made at typing time.
4. Attribution precision (agreement with `tools/sem_label.py` human labels) is reported per type on the scorecard; a type below threshold is excluded from LRN training data (LRN-001) until re-qualified.

## Context and rationale

"The local model failed" is usually several different statements. Bad answer (capability). Could not emit the exact-string edit format (dialect). Endpoint down (infrastructure). Privacy pin blocked the route (policy). If all are recorded as "task too hard for local", the training signal in MEM/LRN is poisoned at the source. The amendment brings the register into line with the code (six types, not four — `user_abort` and `unverifiable` exist and matter) and adds the one type the code is missing, `context_feasibility`, so that a request the rung could not physically hold is never scored as the rung being too weak, states which way ambiguity resolves (toward *not* blaming capability, because that is the error that permanently and invisibly biases a learned router against local), and makes attribution accuracy a measured property rather than an assumption. Typing is a judgment made by code from partial evidence; it can be wrong in exactly the way it exists to prevent.

## Adversarial review (2026-09-02)

### Steelman
Cause-clean labels are the difference between a router that learns capability and a router that learns the outage calendar; MEM-004 enforces this at the label layer and CAS-002 at the source. Six types with an `unverifiable` escape hatch is the honest shape. The literature on agent failure taxonomies (MAST, SWE-agent) confirms that failure classes with different causes need different owners.

### Attacks
1. **The register and the code disagree.** The decision names four types; tenet 8 names five (adds privacy); `outcomes.py` implements six (`task_capability, harness_dialect, infrastructure, policy_constraint, user_abort, unverifiable`). A decision that does not match the ledger schema it governs is not the decision in force. The text must match the code, and `user_abort` in particular is a first-class outcome for MEM-002's late-closing lifecycle.
2. **Attribution is itself a judgment and its error rate is unmeasured.** A local model that times out on a 60k-token prefill: infrastructure, or capability (it could not handle the context)? An exact-string edit that fails on mixed whitespace: dialect (format) or capability (the model did not read the file carefully)? The register's own non-claim says the mixed-whitespace dialect is untested on the production model — so today's most common local failure is one whose type is uncertain. Without a precedence rule and a measured precision, the "poison" the decision prevents just moves from the label to the typer.
3. **`harness_dialect` invites a counterfactual that typing cannot answer.** "Could not emit the exact-string edit format" is only *dialect* if the model would have succeeded with a different format. That is an LRN-002 paired experiment, not something a post-call typer can know; typing it as dialect *exonerates* the model as surely as typing it as capability *convicts* it. Clause 3 scopes the type to observable format failure and leaves the counterfactual to LRN.
4. **Gateway-side substitution is invisible and would be mistyped.** If the gateway fails over within a rung (RTG-008) and the substitute model fails, ADRL types the failure against the rung it *intended*, not the model that served; CAS-006 fixes the rung record but not the cause type. Clause 2 makes within-rung substitution explicitly `infrastructure`.
5. **Ownership of `infrastructure` straddles Q7.** A typed infrastructure failure "reaches the correct owner" only if the gateway team receives it; the register says shared telemetry is the lean but no channel is named. The type is correct; the routing of the signal to its owner is unimplemented and should be a follow-up, not a claim.

### Evidence
- ADRL context pack, "Known code-reality facts" — `outcomes.py` failure types: `task_capability, harness_dialect, infrastructure, policy_constraint, user_abort, unverifiable` (attack 1).
- ADRL Evidence & Readiness — "Real files with mixed whitespace — where the exact-string edit dialect actually breaks — remain untested on the production model" (attack 2).
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2025) — 14 failure modes in 3 categories, built with inter-annotator agreement on 150+ traces; demonstrates that failure typing needs a human-labelled agreement measure, which clause 4 adds (attack 2) — https://arxiv.org/abs/2503.13657
- Yang et al., "SWE-agent" (NeurIPS 2024) — distinguishes "cascading failed edits" (format/interface) from "incorrect implementation" (capability) as separate failure classes and shows interface design (linting) moves the boundary between them, i.e. the dialect/capability split is real but interface-dependent (attack 3) — https://arxiv.org/html/2405.15793
- OpenTelemetry GenAI conventions — `gen_ai.response.model` / `gen_ai.provider.name` give the served identity needed to type within-rung substitution as infrastructure (attack 4) — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ (registry page now marked "moved to the OpenTelemetry GenAI semantic conventions repository", https://github.com/open-telemetry/semantic-conventions-genai)
- Temporal, "What is idempotency?" (engineering blog) — distinguishes transient (retryable) from application failures as a routing-to-owner concern; general precedent for typed failure handling (steelman) — https://temporal.io/blog/idempotency-and-durable-execution

### Verdict
**AMEND.** Attack 1 is a plain defect: the Accepted text names four types and the ledger has six. Attack 2 lands and is the substantive change: the typer's precision must be measured and ambiguity must resolve *away* from `task_capability`, because that is the only direction that poisons learning permanently. Attack 3 lands and is answered by scoping dialect to observable format failure. Attack 4 lands and is answered by clause 2. Attack 5 is a Q7 follow-up. The decision's purpose — each signal to its owner, no poisoning at source — is right and stands.

## Amendments applied
- Replaced the four-type list with the six types implemented in code plus `context_feasibility`, versioned as `failure-types-v2` shared with MEM-004.
- Added a versioned precedence rule with `unverifiable` as the default for unplaceable failures (clause 1).
- Scoped `infrastructure` to include gateway substitution and context/rate/timeouts (clause 2) and `harness_dialect` to observable format failure (clause 3).
- Added attribution-precision measurement and the LRN exclusion gate (clause 4).

## Follow-ups
- [ ] Update the Confluence register and `docs/adr-index.md` to `failure-types-v2`; add `context_feasibility` to `outcomes.py`; add a schema test that the enum in `outcomes.py` matches this ADR and MEM-004.
- [ ] Implement the precedence rule in `outcomes.py`; golden tests for each pairwise ambiguity (timeout+wrong output; dialect failure+pin; abort mid-tool).
- [ ] Human-label a stratified sample with `tools/sem_label.py`; publish per-type precision/recall on the scorecard; set the LRN exclusion threshold.
- [ ] Agree with the gateway team the channel by which `infrastructure`-typed outcomes reach gateway telemetry (Q7).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: `failure-types-v2` (six code types + `context_feasibility`, shared with MEM-004); precedence rule; `unverifiable` default; attribution precision gate | "Failures are typed as task difficulty, model dialect/capability, infrastructure, or policy so each signal reaches the correct owner." |
