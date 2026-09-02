# ADRL-MEM-002 — Three-state outcome lifecycle with defined close

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested for the state machine only; the closing window has never been measured against organic human corrections, so the claim "closed_final catches late evidence" is D0 |
| Review verdict | AMEND |
| Tenets | 8 |
| Related decisions | MEM-001, MEM-003, MEM-004, MEM-009, CAS-005, CAS-006, CAS-007, LRN-001, LRN-004, EVL-004 |
| Open questions | Q6 |

## Decision

Outcome lifecycle is explicit: `pending`, `closed_turn`, then `closed_final` after a configured, recorded closing window during which late retry, interruption, revert or human-correction evidence may still attach; every transition is an appended event with its own timestamp, the window and its trigger are versioned, and outcomes that have not reached `closed_final` are treated as censored — never as positive or negative — by any consumer that counts labels.

1. **The window is a parameter, not a promise.** `closed_final` is emitted by a rule with a named version (e.g. `close-v1`: N subsequent turns in the same session, or T minutes of inactivity, or an explicit episode boundary per CAS-005, whichever first). The rule id is stored on the event so a later, longer window can be applied retroactively by replay.
2. **Late evidence after `closed_final` is still appended.** If a revert, interruption or verifier result arrives after the window, it is appended as a `late_evidence` event and the label is re-derived; `closed_final` marks when the label was frozen for training, not that the truth stopped changing.
3. **Time-to-close is itself a measurement.** The distribution of (evidence timestamp − `closed_turn` timestamp) is reported in the EVL evidence pack and is the basis for choosing the window.

## Context and rationale

A turn that looks successful can stop being successful. The model answers, tests pass, the turn closes — then the developer interrupts, a retry fires, or the work is undone by hand two turns later. Closing at first success systematically over-reports the cheap rung, because the cheap rung's failures show up disproportionately as later human corrections rather than as immediate errors. Three states keep "the turn ended" separate from "the label is final".

The amendment fixes the part of the original that could not be tested: "after late retry/interruption evidence" gave no window, so no one could say whether a given label was closed too early. The delayed-feedback literature is clear that the right posture is to treat not-yet-closed examples as censored and to model the delay distribution explicitly, rather than to pick a cutoff and pretend everything after it is noise. The register itself asks whether the window is long enough to catch human corrections; the honest answer today is that the window has not been measured, because there is exactly one task with strong verification and no organic correction stream to measure against.

## Adversarial review (2026-09-02)

### Steelman
Any outcome store that closes labels at first success will overstate the cheap rung, and a two-state design (`pending`/`closed`) has no place to put a late revert. Three states with an explicit final close is the minimum that lets LRN-001 say "only final labels train" and lets MEM-003 attach verification after the fact. It is cheap to implement and the alternative — re-opening closed rows — violates MEM-001.

### Attacks
1. **"After late retry/interruption evidence" is unfalsifiable.** The text defines `closed_final` by the absence of future evidence, which is unknowable at close time. There is no window, no trigger, no version. The register's own open item ("is the window long enough to catch human corrections?") cannot be answered because nothing in the decision says what the window is. A reviewer cannot check whether a label is over-closed; a trainer cannot know the label's age.
2. **The dominant late signal for a coding agent is the human, and it is not one of the listed evidence types.** Retry and interruption are harness events the proxy can see. "The developer quietly rewrote the function next turn", "the developer reverted the commit that evening" and "CI failed an hour later" are the signals that actually distinguish a cheap-rung near-miss from a success, and none is named. The proxy sees subsequent turns and can detect an edit to the same file/hunk; whether it does is unspecified. Without this, `closed_final` is `closed_turn` with a delay.
3. **Censoring is not addressed, so `closed_turn` labels will leak into training as positives.** With a thin corpus (34 evaluated decisions, one verified task) the pressure to use `closed_turn` outcomes is enormous. The advertising delayed-feedback literature shows the right treatment is to model not-yet-converted examples as unlabeled with a delay model, not to count them as negatives (or, here, as positives). The decision must say what consumers may do with non-final labels.
4. **Interaction with sticky escalation.** Under CAS-005 an episode stays elevated after an escalation; a `closed_turn` on the local attempt followed by an escalation is a local failure, but a `closed_turn` on the frontier continuation is a frontier success only for the residual work. Which `route_id` the late evidence attaches to is governed by MEM-009 (explicit only), but the lifecycle does not say that the local outcome must be `closed_final` as a failure when the episode escalates. This is where a mis-labelled cheap-rung success would come from.
5. **Six failure types, one lifecycle.** `user_abort` and `unverifiable` (present in `outcomes.py`, absent from the decision text) are precisely the states that should never reach `closed_final` as capability evidence. The lifecycle should say that an outcome typed `user_abort` or `unverifiable` closes final only as an excluded label (MEM-004), otherwise "closed" reads as "counted".

### Evidence
- O. Chapelle, "Modeling delayed feedback in display advertising" (KDD 2014) — conversions arrive long after clicks, short windows mislabel future conversions as negatives; treats unconverted clicks as unlabeled and fits a joint conversion + exponential-delay model (survival analysis). Direct support for attack 3 and for clause 3's "measure time-to-close" — https://dl.acm.org/doi/10.1145/2623330.2623634 (PDF: http://wnzhang.net/share/rtb-papers/delayed-feedback.pdf)
- (authors not captured) "Learning under label delay on streaming tabular data" (arXiv 2409.10111, 2024) — empirical study of delayed labels in fraud/credit streams; finds batch learners (XGBoost) competitive with instance-incremental methods under delay and stresses that delay must be modelled explicitly; supports treating the window as a first-class parameter — https://www.arxiv.org/abs/2409.10111
- OpenLineage, "Object Model" — run events progress START → COMPLETE with FAIL/ABORT alternatives and the client keeps the same `runId` across state updates; an external example of a lifecycle expressed as appended state events rather than mutable status — https://openlineage.io/docs/spec/object-model/
- GitClear, "AI Copilot Code Quality: 2025 Data Suggests 4x Growth in Code Clones" (2025) — 211M changed lines 2020–2024; documents rising clone rates and falling refactoring share in AI-assisted code but does not give a two-week revert/churn figure in the fetched page, so it is cited only for the direction (post-authoring rework is a real signal), not a magnitude — https://www.gitclear.com/ai_assistant_code_quality_2025_research
- No direct literature found on human-correction latency for coding-agent output; reasoning from first principles for attack 2.

### Verdict
**AMEND.** Attack 1 is decisive on its own: a lifecycle whose final state is defined by the non-arrival of unknown future evidence cannot be tested, and the register's own open item concedes this. Attacks 2 and 3 show what the text needs — named late-evidence sources including human correction, a versioned window, and a censoring rule for non-final labels — and the delayed-feedback literature supplies the model. Attack 4 is handled by cross-referencing CAS-005 and MEM-009 in the rationale and by follow-up tests rather than new text. Attack 5 is answered by MEM-004's amendment (excluded label types) and clause 2 here. The state machine itself is sound and stays.

## Amendments applied

- Replaced "after late retry/interruption evidence" with "after a configured, recorded closing window during which late retry, interruption, revert or human-correction evidence may still attach".
- Added: every transition is an appended event; window and trigger are versioned (clause 1).
- Added clause 2: evidence after `closed_final` is appended as `late_evidence` and the label is re-derived; `closed_final` is a freeze point, not a truth claim.
- Added: non-final outcomes are censored for any label-counting consumer (ties to LRN-001, EVL-004).
- Added clause 3: time-to-close distribution is a reported measurement.

## Follow-ups

- [ ] Implement `close-v1` with explicit parameters (N turns / T minutes / episode boundary) and store the rule id on every `closed_final` event.
- [ ] Add a human-correction detector to the proxy: subsequent turn edits the same file/hunk the routed turn edited, or a `git revert`/`checkout --` touching it within the window; emit `late_evidence`.
- [ ] Golden test: local attempt `closed_turn` → escalation in the same episode → assert the local outcome reaches `closed_final` as a capability-typed failure and the frontier outcome is a separate `route_id`.
- [ ] Golden test: a `closed_turn` outcome must be excluded from any label count in `learning_readiness.py`; a `late_evidence` event after `closed_final` must flip the derived label.
- [ ] Report the time-to-close histogram (and the fraction of labels that flip after `closed_turn`) in the next EVL pack; use it to set the window rather than guessing.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: closing window made explicit, versioned and measured; human correction named as evidence; non-final labels censored | "Outcome lifecycle is explicit: `pending`, `closed_turn`, then `closed_final` after late retry/interruption evidence." |
