# ADRL now checks the whole request for stronger routing signals

8 September 2026. W7.0a, bounded offline implementation.

**The first routing correction is implemented.** An easy word such as “rename” or
“explain” no longer hides a stronger action elsewhere in the same request. The
existing router uses the strongest recognized signal, while preserving familiar
small-edit phrases. No model, price threshold or safety permission was changed.

| Request | Before | After |
|---|---|---|
| Rename a variable and redesign the concurrency algorithm | Local | Frontier |
| Explain the race condition and implement a fix | Local | Frontier |
| Correct a misspelling in README | Frontier | Local |
| Fix a typo, rename a variable, or add a flag | Local | Local |

The first two changes also appear in the [full dispatch report](research/routing-correction-2026-09-08/lab-final/report.md): the controlled endpoint actually received the frontier request. Privacy pins still force local; repeated tool activity still escalates at a boundary; pinned overflow stays blocked. This is real ADRL code with synthetic requests/responses, not a model-quality experiment.

## What changed in the taxonomy's implementation

**LRN-004 supplies a more faithful feature snapshot.** Previously the extractor
stopped at the first matching easy class. Now it compares all recognized signals.
It understands a few mechanical phrases as units: “fix the second typo” remains
mechanical, and “add a flag” is not double-counted as general implementation. A
separate later action still participates. The previously incomplete concurrency
expression now recognizes “concurrency” and “concurrent.”

**RTG-002/003 use that snapshot through the existing rules and selector.** The
thresholds, class scores, cost model and band tie-breaking did not change. Stronger
features prevent the clear-local rule from claiming the two mixed requests.
RTG-006's optional advisor still has its existing scope; no classifier endpoint
was configured or measured here.

**LRN-005/008 protect compatibility.** New decisions carry `features-v2`; historical
v1 rows remain intact. The current learning contract stays v1, so its existing
version check rejects new v2 training rows until separately qualified. Exploration
startup now rejects a learning-contract/live-feature mismatch. Ordinary routing
without an exploration artifact remains available. This adds no learned authority.

See the [implementation guide](../../adrl-core/docs/routing-features.md),
[feature extraction](../../adrl-core/src/adrl/routing/features.py),
[compatibility guard](../../adrl-core/src/adrl/app.py) and
[regression tests](../../adrl-core/tests/unit/routing/test_mixed_intent.py).

## What the comparison says, including limits

We preserved the original 24 prompts, five conditions and two repeats. We also
froze 12 additional cases before changing code, with the same five conditions and
two repeats. The before/final comparison therefore contains 720 component decisions
over 180 distinct prompt/condition combinations. These are synthetic probes, not
720 completed tasks or independent samples.

Seven original condition cells and 18 fresh condition cells changed their selected
tier. On ordinary original prompts, local selections changed from 9 to 8 and
frontier from 15 to 16; none selected cheap cloud initially. The lab still shows
cheap-cloud escalation later. [Every changed cell](research/routing-correction-2026-09-08/route-changes-final.md) is published, with [before](research/routing-correction-2026-09-08/before.json) and [after](research/routing-correction-2026-09-08/after-final.json) feature and decision traces. No supplied-permission or repeat invariant failed.

This remains a lexical heuristic. “Rename the variable called `redesign`” and “Do
not redesign anything; only rename this variable” now route conservatively to
frontier. “Explain how to implement a scheduler” does too, despite possibly being
an explanation-only request. These are acknowledged false-positive/ambiguous
cases, not evidence that local models cannot handle them. Unrecognized wording
can still be missed. Semantic interpretation and real task outcomes remain work
for later waves; this correction is not a state-of-the-art learned router.

## What verification caught

The first candidate passed the focused tests but over-routed “add a flag.” The full
suite also caught an unwanted change in the existing sticky-cascade scenario:
“Now fix the second typo” selected frontier. We retained that failed candidate and
corrected both phrase overlaps without changing the old tests or frozen task cases.
The expanded focused run passes 159 tests. The final full run passed all eleven checks: 911 tests passed and eight engine
cases stayed skipped on 322 stable inputs. See the
[qualification record](research/routing-correction-2026-09-08/validation.json).

The initial candidate's source, matrices and failed check are preserved under
[candidate 1](research/routing-correction-2026-09-08/candidate-1/) and
[checks 1](research/routing-correction-2026-09-08/checks-1/manifest.json).
This was one substantive repair cycle. No thresholds were tuned to achieve a
preferred routing distribution, and no engine experiment was authorized.

## Where we go next

This is the first practical course correction in the new lab loop:
**observe a weak decision → amend its implementation → replay the same cases →
check for regressions → record the evidence in the taxonomy.** It is manual
evidence-driven improvement, not autonomous RSI.

The next prerequisite for useful model comparisons is the existing W3 custody and
exact-output capture work. Then qualify a bounded Claude Code task experiment with
fixed acceptance checks and access/cost limits. That supplies outcomes for learning
which route is useful, beyond checking whether a rule fires. A separately qualified
second harness, K0 snapshot, learned-checkpoint evaluation and later RSI remain on
the [product roadmap](adrl-product-roadmap-2026-09-08.md).

Architectural statuses and all 77 formal maturity fields remain unchanged. The
named behavior gains scoped offline evidence; no organic gate, D3/D4/D5 promotion,
real-model quality, savings or live deployment is established. Hourly automation
remains paused. No models, paid calls, real harnesses, containers or commits were used.
