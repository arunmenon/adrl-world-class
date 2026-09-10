# ADRL-RTG-003 — Rules own clear cases, measured

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D3 Shadow (band split has shadow evidence; per-band rule precision on verified outcomes is not yet reported and is added as a gate) |
| Review verdict | AMEND |
| Tenets | 4 |
| Related decisions | RTG-006, RTG-007, LRN-006, MEM-004, EVL-004, SEM-001 |
| Open questions | Q4 |

## Current implementation evidence, 2026-09-08: routing diagnostic

The diagnostic reproduced two mixed-intent clear-local misclassifications and a typo paraphrase route difference. A separate synthetic ledger with 12/20 successful closed outcomes demoted the local rule at the current 85% threshold; explicit snapshot refresh changed the same typo from local to frontier. The service constructs a health snapshot at startup; no recurring refresh is wired. Outcome admission, duplicate handling, minimum-observation configuration and refresh provenance need review before operational adaptation. Synthetic events confer no learning eligibility.

[Report](../../reports/adrl-routing-in-action-2026-09-08.md) · [raw traces](../../reports/research/routing-demonstration-2026-09-08/results.json) · [next correction packet](../../reports/waves/routing-decision-quality.md). The focused 135 routing/cascade/learning tests pass; all 316 runtime inputs match the previous full build. Architectural status, maturity and decision wording are unchanged.

## W7.0a scoped application and evidence, 2026-09-08

The scoped clear-case application now uses features-v2: strongest recognized intent wins over an earlier easy match; mechanical repair and small-edit phrase overlaps are preserved. Existing class scores, rule predicates, band precedence and precision thresholds are unchanged. Both easy-keyword masking defects are corrected, with conservative lexical false positives explicitly reported. No outcome-driven rule-health refresh or measured precision claim is added.

[Report](../../reports/adrl-routing-correction-2026-09-08.md), [implementation guide](../../../adrl-core/docs/routing-features.md), [code diff](../../reports/research/routing-correction-2026-09-08/implementation.patch), [tests](../../../adrl-core/tests/unit/routing/test_mixed_intent.py), [all route changes](../../reports/research/routing-correction-2026-09-08/route-changes-final.md), [checks](../../reports/research/routing-correction-2026-09-08/checks-final/manifest.json), [validation](../../reports/research/routing-correction-2026-09-08/validation.json). Final validation: 159 focused tests; all eleven checks; 911 passed, eight engine cases skipped; 322 stable inputs. One initial candidate failed an existing sticky-cascade test and over-routed the flag case; both were repaired without changing the original suite. Decision text/status/formal maturity stay unchanged; named offline behavior only, no organic qualification or full-decision promotion.

## Decision

Deterministic rules own clear cases; learned intelligence is reserved for the ambiguous middle — where "clear" is a versioned band definition whose per-band precision on verified outcomes is measured and published, and a band whose measured precision falls below its threshold is reclassified as ambiguous rather than left to the rules.

1. Band boundaries (features, thresholds, rule ids) are versioned in `router/policy.py` config and recorded on every decision row, so the population of "clear" cases can be re-derived after a rule change.
2. Each clear band carries a rule-precision gate: fraction of verified outcomes on which the rule's rung completed without escalation. Rule health (`router/rule_health.py`) reports it per band; a band under threshold loses its "clear" status and enters the advisor's scope (RTG-006) until re-qualified.
3. The size of the ambiguous band is a published, dated measurement, not a fixed assumption; the bar for building any learned component (RTG-007/LRN-003) is stated in terms of that band's size and realisable gain (Q4).

## Context and rationale

Most decisions are not close calls. "Fix this typo" and "design our multi-region failover" do not need a model to adjudicate. Measured on real traffic, only a small minority of turns are genuinely ambiguous; that sets a ceiling on how much a learned router can ever add. The benchmark literature agrees from the other direction: across 400k+ routing outcomes, learned routers' gains come from coarse domain structure and several — including a commercial router — fail to beat the best single model. So rules-first is well supported.

What the original sentence did not say is who decides what "clear" means. If the rules define their own clear band, the claim "rules own clear cases" is true by construction and cannot be wrong. The amendment makes clearness an *earned* property: a band is clear while its rule's precision on verified outcomes stays above threshold, and it stops being clear when it does not. That keeps tenet 4 falsifiable and gives the ambiguous band a measured size, which is what Q4 needs.

## Adversarial review (2026-09-02)

### Steelman
Deterministic rules are cheap, auditable, and cannot be prompt-injected; they fail predictably and can be tested with fixtures. The Phase 0 corpus shows the ambiguous band is a minority, and independent benchmarks show learned routers realise most of their value from coarse structure that rules capture equally well. Reserving the expensive, variable component for the residual is the right allocation.

### Attacks
1. **"Clear" is defined by the rules, so the decision is unfalsifiable.** Nothing in the text says how a case *becomes* clear or stops being clear. A rule that routes every request under 4k tokens to local is "owning a clear case" by fiat even if half of those turns escalate. Without a measured precision per band, tenet 4 is a tautology.
2. **The minority-band finding is from a single-user, workflow-heavy corpus.** The Evidence page says directional findings only; magnitudes not transferable. An enterprise population with more design/debug turns and fewer mechanical edits could have a materially larger ambiguous band, which changes the Q4 calculus. The decision must carry the measurement as dated evidence, not as a premise.
3. **Clear bands drift with model releases.** A band that was clear for local model v1 (e.g. "single-file exact-string edit") may be unclear for v2 with a different edit dialect, and clearer for a stronger cheap-cloud model. Rules are static; the capability landscape is not. No re-qualification mechanism is stated.
4. **Deterministic ≠ correct, and the rules see only request-shape features.** `features.py` extracts quick features (size, tool mix, keywords). SWE-agent's analysis shows 52% of unresolved instances are *incorrect implementations* with no surface signature; RouterBench's oracle gap shows that even good routers miss the "lone correct model" cases. Cheap features cannot see semantic difficulty, so some "clear-easy" turns are hard. That is acceptable only if the miss rate is measured (clause 2).

### Evidence
- LLMRouterBench (arXiv 2026) — "several recent routing methods, even including the commercial router OpenRouter, do not outperform a simple baseline (the Best Single model)"; gains come from "coarse-grained domain structure" (steelman, attack 4) — https://arxiv.org/html/2601.07206v1
- Hu et al., "RouterBench" (arXiv 2024) — "none of the routing algorithms significantly outperform the baseline Zero router"; oracle consistently exceeds all routers (attack 4) — https://arxiv.org/abs/2403.12031
- Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data" (ICLR 2025) — routers trained on Arena data performed near-random on MMLU because "most MMLU questions being out-of-distribution"; router quality tracks benchmark–dataset similarity, i.e. band definitions do not transfer across distributions (attacks 2, 3) — https://arxiv.org/abs/2406.18665
- Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering" (NeurIPS 2024) — 52.0% of unresolved instances are Incorrect/Overly-specific Implementation, a failure class invisible to request-shape features (attack 4) — https://arxiv.org/html/2405.15793
- No direct literature found on the fraction of *coding-agent* turns that are genuinely ambiguous for routing; the only external data points are vendor claims (GitHub Copilot, Not Diamond) that routing "based on task" works, without published band sizes. Reasoning from first principles and the project's own corpus (attack 2).

### Verdict
**AMEND.** Attack 1 lands: as written, the decision cannot be wrong, which violates the project's own FND-005 stance. Attacks 2 and 3 land together: the band split is real evidence but of a single corpus and a single model generation, so the decision must carry it as a dated measurement with a re-qualification path. Attack 4 is answered by the design (rules-first is *supposed* to miss semantic difficulty and rely on escalation) but only if the miss rate is measured, which is exactly clause 2. The principle — rules first, learning in the residual — is strongly supported by independent benchmarks and stands.

## Amendments applied
- Added "where 'clear' is a versioned band definition whose per-band precision on verified outcomes is measured and published".
- Added clause 1 (versioned bands recorded on decision rows).
- Added clause 2 (rule-precision gate; demotion of under-performing bands to the ambiguous band).
- Added clause 3 (ambiguous-band size is a dated measurement that sets the bar for RTG-007).

## Follow-ups
- [ ] Extend `router/rule_health.py` to emit per-band precision on `closed_final` verified outcomes; add the threshold to versioned policy config.
- [ ] Golden test: a band whose synthetic precision drops below threshold is routed through `llm_classifier.py` on the next decision.
- [ ] Publish the ambiguous-band share with corpus provenance (single-user shadow) and re-measure on the first pilot population before any RTG-007 build decision.
- [ ] Re-run band qualification whenever the `local` or `cheap_cloud` registry entry changes model.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded W7.0a scoped feature/compatibility application and before/after evidence | Prior decision text and dated evidence retained; features-v1 used first-match classification and exploration lacked this explicit live-feature/contract check |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: "clear" made a measured, versioned, revocable property; ambiguous-band size made a dated measurement | "Deterministic rules own clear cases; learned intelligence is reserved for the ambiguous middle." |
| 2026-09-08 | Added scoped offline routing-diagnostic evidence and limitations; behaviour and grades unchanged | Decision wording retained unchanged; prior implementation/research notes preserved. |
