# ADRL-SEM-005 — Episode boundaries, enumerated and measured

| Field | Value |
|---|---|
| Bucket | SEM — Interaction Semantics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (correct; but the decision is unfalsifiable until boundary precision/recall is measured in shadow — see follow-ups) |
| Review verdict | AMEND |
| Tenets | 6 |
| Related decisions | CAS-005, SEM-004, SAF-002, FND-003, MEM-002 |
| Open questions | Q5 |

## Decision

Episode boundaries are conservative semantic events, drawn from an enumerated signal list, that may release escalation hysteresis and nothing else; every candidate boundary is logged with its signal so that boundary precision and release rate are measurable.

1. Enumerated signals, in decreasing confidence: new session key (SEM-002); harness `/clear`; the harness's own topic-detection call returning a new-topic verdict *and* the next user turn referencing no open tool state; a user turn following a completed verification (tests passed, MEM-002 `closed_turn`) that names a different file set. Compaction alone is not a boundary.
2. A boundary releases the escalation ratchet (CAS-005) only; it never releases a privacy pin (SAF-002), never resets the SAF gate state, and never resets the session key.
3. Two shadow metrics gate any tightening or loosening of the signal list: *false-boundary rate* (boundaries followed within N turns by a trip-wire escalation back to the prior rung) and *release rate* (fraction of escalated sessions that ever come back down).

## Context and rationale

Once work escalates to frontier it stays there (CAS-005), but it cannot stay elevated forever. An episode boundary — a conservative signal that you have genuinely moved on — is the only event allowed to release that. Conservative deliberately: a false boundary silently drops a hard task back to local mid-flight.

The amendment addresses the register's own worry: "so conservative a rung is never lowered in practice?" As written, the decision cannot be wrong — any missed boundary is "conservative", any false one is "a semantic event we misjudged" — and a decision that cannot be wrong cannot be tuned. The fix is to enumerate the signals, log every candidate, and define the two rates that would tell you the list is too tight or too loose. It also names the cheapest signal available: Claude Code already asks a small model "is this a new topic?" on each user turn and receives a JSON verdict; ADRL sees that call on the wire and can read it instead of building a segmenter. Finally, the amendment states in the decision what the register says elsewhere: a boundary releases hysteresis, never a pin.

## Adversarial review (2026-09-02)

### Steelman
Stickiness without release is a one-way cost ratchet; release without a boundary is oscillation. A conservative boundary is the right asymmetry because the cost of a false release (a hard task silently degraded mid-flight, cache cold, possibly a cross-vendor handoff) is far higher than the cost of a missed one (a few cheap turns billed at frontier). Tenet 6 is implemented exactly here.

### Attacks
1. **Unfalsifiable as written.** "Conservative semantic events" names no event. Without an enumerated list and a logged candidate stream there is no way to compute how often a boundary fires, how often it is wrong, or whether the ratchet ever releases — and the register admits it does not know. The decision needs a measurement contract to be a decision rather than an intention.
2. **Topic segmentation is genuinely hard and mechanical detectors are error-prone.** Recent unsupervised dialogue topic segmentation work reports error rates (Pk) around 11% on the easy DialSeg711 benchmark and around 35% on Doc2Dial — and coding sessions are harder than either (long tool loops, coreference to files, "now do the same for the other service"). A home-grown heuristic on coding transcripts will not beat those numbers, so *every* mechanical boundary needs a second, cheap confirmation (sub-clause 1's conjunctions).
3. **The harness already computes the signal.** Sung's trace shows Claude Code issuing a topic-detection request that returns `isNewTopic` and a short title. This is a model-produced verdict, free to ADRL, aligned with the harness's own notion of topic. Building an independent segmenter and ignoring this is wasted effort; relying on it alone is over-trust (it is a 2–3-word-title heuristic, not a task-boundary detector). Use it as a candidate with confirmation.
4. **Boundary vs pin ambiguity.** SAF-002 says a pin is never released; SEM-005 says a boundary "may release escalation hysteresis". An engineer could plausibly implement boundary handling as "reset session state" — which would release the pin. The two decisions should not depend on the reader inferring the difference; sub-clause 2 states it.
5. **Compaction is a tempting false boundary.** After compaction the cache prefix is cold anyway (FND-003 attack 5), so switching down is "free" from a cache perspective — but the task has not changed; it has merely been summarised. Treating compaction as a boundary would drop a hard task to local at the exact moment the model's memory is weakest. Excluded explicitly.
6. **Release rate zero is a silent cost bug.** If the ratchet never releases, a developer whose first task of the day was hard pays frontier prices for eight hours of trivial edits. That is not "conservative", it is "off", and nothing in the register today would show it. The release-rate metric exists to make this visible.

### Evidence
- "An Unsupervised Dialogue Topic Segmentation Model Based on Utterance Rewriting" (arXiv 2409.07672, 2024) — reports 11.42% Pk / 12.97% WindowDiff on DialSeg711 and 35.17% / 38.49% on Doc2Dial as state of the art for unsupervised segmentation; bears on attack 2 — https://arxiv.org/abs/2409.07672
- George Sung, "Tracing Claude Code's LLM Traffic" (Medium, 2026) — Claude Code issues a topic-detection request returning JSON with `isNewTopic`; bears on attack 3 — https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5
- Anthropic, "Prompt caching" (Claude Platform docs) — prefix-exact, per-model (implied, not stated) cache; after compaction the prefix is new; bears on attack 5 — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Google SRE, "Canarying Releases" (SRE Workbook) — choose a small set of attributable SLIs and evaluate over enough time; methodological support for sub-clause 3's two rates — https://sre.google/workbook/canarying-releases/

### Verdict
**AMEND.** Attack 1 is decisive: the decision is correct in intent and unfalsifiable in form. Attacks 2 and 3 shape the enumerated list — mechanical segmentation alone is not reliable enough, and the harness's own verdict is the best single candidate signal. Attack 4 is a cross-decision safety clarification that costs one sentence. Attacks 5 and 6 supply the exclusion and the metric. The conservative posture is preserved; what changes is that "conservative" becomes a measured property rather than a mood.

## Amendments applied

- Added "drawn from an enumerated signal list" and "and nothing else" to the decision sentence; added the logging requirement.
- Added sub-clause 1 enumerating candidate signals with confirmation conjunctions; compaction explicitly excluded.
- Added sub-clause 2 stating boundaries release hysteresis only, never pins, gate state or session key.
- Added sub-clause 3 defining false-boundary rate and release rate as the tuning metrics.

## Follow-ups

- [ ] Log every candidate boundary (signal, session, turn index) from `router/episode.py` into the ledger in shadow; label a sample with `tools/sem_label.py`; report false-boundary rate and release rate.
- [ ] Parse the harness topic-detection response on the wire and feed `isNewTopic` into `router/episode.py` as a candidate signal (SEM-004 follow-up).
- [ ] Golden test: pinned + escalated session hits a boundary → escalation ratchet released, pin unchanged, session key unchanged.
- [ ] Golden test: compaction event → no boundary emitted.
- [ ] Decide thresholds for the two rates before measuring (FND-005 pre-registration follow-up).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: signals enumerated; pin never released; boundary metrics defined | "Episode boundaries are conservative semantic events that may release escalation hysteresis." |
