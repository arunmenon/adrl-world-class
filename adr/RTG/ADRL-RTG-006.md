# ADRL-RTG-006 — Advisory LLM classifier, gated and bounded

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D3 Shadow (bake-off and shadow reports exist; the amendment adds constraints that are testable at D2 and do not lower the shadow evidence already gathered) |
| Review verdict | AMEND |
| Tenets | 2, 4 |
| Related decisions | RTG-003, RTG-007, SAF-001, SAF-002, SAF-003, LRN-006, MEM-005, FND-004 |
| Open questions | Q1, Q4, Q5 |

## Decision

The current LLM classifier is a fail-safe middle-band advisor, not a safety authority or final learned router: it runs only on turns already inside the ambiguous band, only at a rung the hard gates permit for that session, under a fixed latency and cost budget, and on any failure, timeout, or malformed output the policy takes the conservative (higher) side of the band.

1. Placement: the classifier is invoked after SAF gates and after band classification (RTG-003); it never sees a turn the rules already own and can never widen the permitted rung set. On a privacy-pinned session it runs locally or is skipped — never on cloud.
2. Budget: a versioned timeout and per-turn token cap; exceeding either is a `classifier_timeout` outcome, not a routing input. Classifier cost is charged to the turn in RTG-009 accounting so its own overhead is inside the objective it advises.
3. Fallback: the deterministic fallback for the ambiguous band is named in policy config and defaults to the *higher* rung, because the band is by construction where the rules are least sure and a false "easy" costs a failed attempt plus escalation.
4. Provenance: classifier model id, prompt version, raw label and confidence are recorded on the decision row so calibration can be measured against verified outcomes and the advisor can be retired without ambiguity when RTG-007 exists.

## Context and rationale

There is an LLM in the path today, and it is deliberately not in charge. It advises on the ambiguous middle only; it cannot open a gate, cannot override a pin, and is not the learned router of RTG-007. Its failure mode is "fall back to the deterministic rule". The amendment says three things the original left open: *where* the LLM runs (it must obey the same privacy pin as the traffic it classifies — a classifier call that sends the prompt to cloud is a route), *what it costs* (an advisor with unbounded latency in the hot path negates the negligible-overhead finding from Phase 0), and *which way the fallback falls* (the band has no "deterministic rule" of its own; it is defined as the region where the rules abstain, so the fallback must be a named conservative default). The LLM-as-judge literature confirms that a single-shot LLM classification is sensitive to prompt perturbation and biased toward familiar text, which is acceptable for an advisor that is logged and calibrated, and unacceptable for one that is trusted.

## Adversarial review (2026-09-02)

### Steelman
An LLM reading the actual request is the only cheap source of *semantic* difficulty signal in a rule system that sees request shape. Limiting it to the ambiguous band bounds both cost and blast radius; making it advisory keeps the safety property (SAF-001) intact; the bake-off and shadow reports mean its accuracy is at least measured. It is a pragmatic bridge until RTG-007.

### Attacks
1. **The classifier call is itself a route, and the decision does not say which rung it runs on.** If the advisor runs on a cloud model, then for a session that SAF-003 has just flagged, the *classification* request leaks the prompt before the "route" does. The decision says it cannot override a pin — but a cloud classifier invoked on pinned traffic *is* the leak. Placement must be stated (clause 1).
2. **"Fall back to the deterministic rule" is undefined for the middle band.** RTG-003 defines the middle band as the region where the deterministic rules do *not* decide. So on classifier failure there is no rule to fall back to unless one is named. Falling to the *lower* rung on failure means a classifier outage silently degrades quality; falling to the *higher* rung means an outage silently raises cost. Either is defensible; leaving it unnamed is not.
3. **Hot-path latency and cost are unbounded in the text.** Phase 0's "router overhead negligible" finding is about the deterministic path. An LLM call adds hundreds of milliseconds to seconds and a paid inference on every ambiguous turn. If the classifier's own cost is not charged inside the objective (RTG-005/009) the router can be net-negative on the very band it exists to improve.
4. **LLM judgments are perturbation-sensitive and biased.** A 2026 audit of LLM-as-judge on software engineering tasks found accuracy swings of 13–18 percentage points from prompt-injected biases (position, verbosity, chain-of-thought) with the code unchanged; self-preference bias tracks perplexity. A difficulty classifier reading a developer prompt is exposed to the same effects — a verbose prompt looks "hard", a terse one "easy". Acceptable only with logged provenance and measured calibration (clause 4).
5. **It creates a second, unversioned learned component that LRN-005 does not cover.** LRN-005 requires every learned artifact to version its feature schema, objective and calibration. A prompted LLM classifier with a prompt string and a model id *is* a learned artifact by any reasonable reading, but sits in RTG rather than LRN and is not held to LRN-005. Clause 4 closes the gap at the ledger level.

### Evidence
- "Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering" (arXiv 2026) — prompt-injected biases moved judge accuracy by 13–18 pp on code repair/generation with the code unchanged; recommends reporting bias sensitivity alongside accuracy (attack 4) — https://arxiv.org/html/2604.16790v1
- Wataoka et al., "Self-Preference Bias in LLM-as-a-Judge" (NeurIPS 2024 workshop) — judges rate lower-perplexity text higher regardless of author, i.e. familiarity, not quality (attack 4) — https://arxiv.org/abs/2410.21819
- Shi et al., "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge" (arXiv 2024) — position bias is systematic across judge models (attack 4) — https://arxiv.org/abs/2406.07791
- Ong et al., "RouteLLM" (ICLR 2025) — a causal-LLM router (Llama-3-8B) is one of four router types; performance depends on training-data similarity to the deployment distribution, so an un-finetuned advisor's calibration must be measured in-domain (attack 4, clause 4) — https://arxiv.org/abs/2406.18665
- ADRL register SAF-003: "Secret detection occurs before routing and suppresses prompt-derived embeddings and identifiers" — a cloud classifier call is a prompt-derived artefact leaving the machine (attack 1).
- Anthropic, "Prompt caching" — a classifier call with a different system prompt shares no cache with the routed request, so its cost is full-price input on the turn's transcript unless it sees only a summary (attack 3) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching

### Verdict
**AMEND.** Attack 1 is the serious one: the decision's "cannot override a pin" is true of the classifier's *output* but not of its *invocation*, and the text must bind placement to the gates. Attack 2 lands: the fallback must be named, and this review recommends the higher side of the band as default with the rationale in clause 3. Attack 3 lands and is answered by clause 2 plus charging the classifier's cost in RTG-009. Attacks 4 and 5 are answered by making provenance and calibration recorded, which is the minimum for an advisor whose known biases are documented. The decision's spirit — an advisor, not an authority — is correct and stands.

## Amendments applied
- Added "only at a rung the hard gates permit for that session, under a fixed latency and cost budget, and on any failure, timeout, or malformed output the policy takes the conservative (higher) side of the band".
- Added clauses 1–4: placement after gates and local-only on pinned sessions; budget and cost accounting; named conservative fallback; provenance on decision rows.

## Follow-ups
- [ ] Golden test: pinned session + ambiguous band → classifier request is sent to the local backend or skipped; a cloud backend call is a test failure.
- [ ] Golden test: classifier timeout → decision row has `classifier_timeout` and route = configured fallback rung.
- [ ] Add classifier model id, prompt hash, label, confidence to the decision schema; publish calibration (reliability diagram) against `closed_final` verified outcomes on the shadow scorecard.
- [ ] Measure classifier p50/p95 added latency and per-turn cost in shadow; set the budget from the measurement.
- [ ] Decide (RTG/LRN owners) whether the prompted classifier is subject to LRN-005 artifact versioning; record the disposition.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: placement bound to gates and pins; latency/cost budget; named conservative fallback; provenance logging | "The current LLM classifier is a fail-safe middle-band advisor, not a safety authority or final learned router." |
