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

## Outcome contract repair, 2026-09-09

Scoped implementation correction for RV-01: cascade pending/closed-turn events use the
existing canonical outcome contract; proxy forwarding preserves event identity. Synthetic
composed tests reach an explicitly invoked closer and readiness projection without inventing
capability evidence. Historical dialect rows remain excluded, no automatic closer or learned
admission is added, and other review blockers remain open. Formal status/maturity unchanged.
Post-review disposition is recorded in the [repair report](../../reports/reviews/outcome-contract-2026-09-09/report.md),
with code and tests in [runtime contract](../../../adrl-core/docs/outcome-contract.md).

## Decision

Outcome lifecycle is explicit: `pending`, `closed_turn`, then `closed_final` after a configured, recorded closing window during which late retry, interruption, revert or human-correction evidence may still attach; every transition is an appended event with its own timestamp, the window and its trigger are versioned, and outcomes that have not reached `closed_final` are treated as censored — never as positive or negative — by any consumer that counts labels.

1. **The window is a parameter, not a promise.** `closed_final` is emitted by a rule with a named version (e.g. `close-v1`: N subsequent turns in the same session, or T minutes of inactivity, or an explicit episode boundary per CAS-005, whichever first). The rule id is stored on the event so a later, longer window can be applied retroactively by replay.
2. **Late evidence after `closed_final` is still appended.** If a revert, interruption or verifier result arrives after the window, it is appended as a `late_evidence` event and the label is re-derived; `closed_final` marks when the label was frozen for training, not that the truth stopped changing.
3. **Time-to-close is itself a measurement.** The distribution of (evidence timestamp − `closed_turn` timestamp) is reported in the EVL evidence pack and is the basis for choosing the window.

## W3.1 retained operator captures, 2026-09-08

W3.1 records a separate attempt UUID, task reference and optional existing same-session parent attempt in the encrypted capture envelope. These are operator-declared identities and relationships, not trusted task lifecycle transitions. The slice does not infer task success, close an outcome or implement the close supervisor. W3.2 must establish and test those transitions before exact task-close attribution is claimed.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

Scoped application: the internal attempt journal records started, close_requested, cancelled and incomplete as distinct encrypted events. Starts reserve a task-attempt UUID and future capture UUID; parent validation requires the same task, session and workspace plus a terminal parent. Out-of-order and post-terminal transitions are rejected. Restart preserves pending history, with an explicit incomplete transition available when authority and quota permit. There is no successful-close state, process supervisor or automatic completion; attribution remains unestablished and learning eligibility false. W3.2b must establish writer quiescence and capture association.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b2a reserved terminal capacity, 2026-09-08

W3.2b2a introduces operator-attempt-policy-v2 for new starts: at least two event slots, one reserved terminal slot and a 1,024-byte default terminal allowance (versioned range 1,024 to 4,096), retaining the existing absolute maxima. All permitted terminal reasons must fit before admission. Close requests cannot spend reserved capacity. A lowered caller limit applies to new/nonterminal work but does not revoke the original bounded terminal grant; all active admission ceilings constrain further work. Historical v1 records keep their original quota contract, support matching-policy retry/continuation, and receive no retrospective grant; new v1 admission is refused. This remains an operator intent/interruption journal, not closed_turn/closed_final evidence, stopped-writer proof or learning admission.

See the [plain-language report](../../reports/adrl-w3-2b2a-terminal-capacity-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b2a-terminal-capacity-2026-09-08.json),
[journal](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py),
[capacity migration](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/migrations/0009_attempt_capacity.sql),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_capacity.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 697 tests and eleven checks pass for the recorded build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved.
No exact task-close, learning or full-W3 completion claim follows.

## W3.2b2b2 process coordination, 2026-09-08

A supervised fixture can now turn loss of authority or command termination into an attempted incomplete/quiescence_unavailable journal record. An existing terminal entry is preserved; failed or unreadable terminal writing is reported unavailable. A terminal event may consume its original quota grant but cannot release the separate permanent workspace fence. No successful task close, verified label or exact-close capture association is introduced.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2c writer-boundary research, 2026-09-08

The research separates process exit, namespace termination, owner-client death and a terminal task record. Only tested container termination suppressed the detached late writer; killing the client did not. A future close contract must prevent restart/new writers and durably associate the correct captured output before granting stronger attribution. Six research observations add no successful runtime close transition and release no existing fence.

See the [plain-language report](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md),
[experiment and source evidence](../../reports/research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[fixture source](../../reports/research/writer-boundary-2026-09-08/probe.go),
[frozen packet](../../reports/waves/w3-2b2c-writer-boundary.md) and
[next ownership packet](../../reports/waves/w3-2b2d-resource-ownership.md).
The corrected research run completed six bounded observations, including negative controls.
The previously passing 759-test/eleven-check runtime source is unchanged; all 300 declared
hashes were reverified, not rerun. This research changes no runtime behavior, architectural
status, maturity, release authority or whole-W3 completion claim. Prior wording is retained.

## W3.2b2d1 stopped resource ownership, 2026-09-08

The history distinguishes intent, issued create, inspected binding, issued removal and observed absence. A bound retry does not create a new resource; issued-but-unbound work stays uncertain. All events remain workspace-blocked, exact-close ineligible and learning ineligible. Neither a stopped resource nor its removal supplies a task success, verifier result or training label. Durable task-close/capture/outcome association remains open.

See the [plain-language report](../../reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.json),
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[unit cases](/Users/arunmenon/projects/adrl-core/tests/unit/test_resource_owner.py),
[local engine cases](/Users/arunmenon/projects/adrl-core/tests/integration/test_resource_engine.py)
and [runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
All 812 tests and eleven engineering checks pass, with 306 declared source hashes unchanged
during the run. This supports the scoped tested behavior only. Prior decision wording,
architectural status and maturity fields remain unchanged; full B2/B3 and W3 remain open.

## W3.2b2d2 launch-contract research and identity gate, 2026-09-08

Both attempted launch-recovery experiments failed during cleanup identity comparison, and their intermediate case results were not durably completed. Accepted observation count remains zero of six; source review and partial inspections are not outcome labels. The proposed lifecycle distinguishes request acknowledgement, sealed admission, observed exit and discarded resource. None grants exact-close or learning eligibility, and no active lifecycle event producer exists yet.

See the [plain-language progress report](../../reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md),
[failed-run/source evidence](../../reports/research/adrl-w3-2b2d2-launch-contract-2026-09-08.json),
[proposed execution contract](../../reports/waves/w3-isolated-execution-contract-v1.md),
[next identity packet](../../reports/waves/w3-2b2d2-identity-compatibility.md), and the unchanged
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py) and
[runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
No runtime source changed: the 812-test/eleven-check baseline is reused with all 306 declared
hashes verified. No new passing runtime run is claimed. Prior wording, architectural status
and maturity remain unchanged. Active launch, full d/B2/B3 and W3 remain open.

## W3.2 execution identity and launch research, 2026-09-08

The driver now persists intermediate assertions and records primary and cleanup failures separately. A case is accepted only after both assertions and exact-ID cleanup succeed. Seven new observations passed, while both older failed runs retain their failed status. Research SHA references are not authenticated runtime ownership or task-success receipts. Durable execution provenance and exact-close association remain planned.

See the [plain-language report](../../reports/adrl-w3-execution-identity-2026-09-08.md),
[research evidence](../../reports/research/adrl-w3-execution-identity-2026-09-08.json),
[comparator](../../reports/research/execution-identity-2026-09-08/execution_identity.py),
[offline cases](../../reports/research/execution-identity-2026-09-08/test_execution_identity.py),
[driver](../../reports/research/execution-identity-2026-09-08/run_probe.py) and
[next runtime packet](../../reports/waves/w3-isolated-launch-runtime.md).
101 offline research cases and seven engine observations pass. The unchanged runtime's
812-test/eleven-check baseline is reused with 306 verified hashes. Prior decision text and
all status/maturity fields are preserved; no grade promotion, independent review or full-W3
completion follows.

## W3.2 one-shot fixture runtime prototype, 2026-09-08

Launch history now distinguishes claim, acknowledgement, seal, stopped, discard-issued and discarded, linked to original resource ownership. A lost reply does not authorize another launch; reports distinguish failed execution and audit failure from observed cleanup. Only the exact container inspection can confirm absence; a discovered name is not runtime binding. The unreceipted test candidate required a separately recorded operator-maintenance exception, with uncertainty preserved.

See the [report](../../reports/adrl-w3-isolated-launch-2026-09-08.md),
[checks and failed-run evidence](../../reports/research/adrl-w3-isolated-launch-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[pinned transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[permanent markers](/Users/arunmenon/projects/adrl-core/src/adrl/core/launch_markers.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_isolated_execution.py),
[runtime guide](/Users/arunmenon/projects/adrl-core/docs/isolated-execution.md) and
[next diagnosis packet](../../reports/waves/w3-launch-create-receipt-diagnosis.md).
Final offline validation: 861 passed, eight opt-in engine cases skipped, all eleven checks;
315 declared hashes stable. Two engine invocations each had three passes and one failure.
The allowance is closed and all eight fixtures/image are absent. All prior wording and
77 status/maturity fields are preserved. No independent review, grade promotion or full-W3
completion follows.

## W3.2 receipt correction and pinned-engine validation, 2026-09-08

Safe transport-cause classification now reaches private synthetic receipt diagnostics while owner uncertainty remains generic and fenced. Offline delayed/invalid/oversized/encoded/disconnected replies prove that a created resource need not have a valid original receipt. No create reissue or name adoption follows. All thirteen current engine creates returned original IDs and have exact absence confirmations; the historical missing cause remains unknown.

See the [plain-language report](../../reports/adrl-w3-transport-receipts-2026-09-08.md),
[checks and cleanup evidence](../../reports/research/adrl-w3-transport-receipts-2026-09-08.json),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[versioned execution policy](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[receipt fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_create_receipt.py) and
[next custody packet](../../reports/waves/w3-active-copy-custody.md).
Final validation: 895 passed, zero skipped, all eleven checks, 316 stable source inputs;
13 original create receipts and absence confirmations, one image removed. The bounded d2
synthetic lifecycle slice closes. Full B2/B3/W3, real-harness and independent qualification
remain open. Prior wording and all 77 architectural status/maturity fields are preserved.

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

- 2026-09-09: Record scoped outcome contract repair and evidence; retain prior decision/status/maturity.

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded versioned creation/active transport separation and passing pinned-engine lifecycle acceptance | Prior decision/evidence preserved; bounded d2 closes, full W3 and grades unchanged |
| 2026-09-08 | Recorded W3.2 fixture launch prototype, offline checks, engine failures and operator cleanup exception | Prior decision/evidence preserved; engine workflow remains unqualified, no status/maturity promotion |
| 2026-09-08 | Recorded W3.2 identity correction and seven accepted bounded launch observations | Prior wording and failed evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d2 failed launch probes, source-explained identity gate and proposed lifecycle | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d1 stopped ownership, acknowledgement recovery and explicit limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2b2 stop coordination, permanent workspace blocking and failure evidence | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2a versioned terminal capacity, compatibility and recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: closing window made explicit, versioned and measured; human correction named as evidence; non-final labels censored | "Outcome lifecycle is explicit: `pending`, `closed_turn`, then `closed_final` after late retry/interruption evidence." |
