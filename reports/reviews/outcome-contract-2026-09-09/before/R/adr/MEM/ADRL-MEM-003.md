# ADRL-MEM-003 — Verification enriches, never overwrites

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested for the non-overwrite contract; note that only one task has strong verification, so the contract has one real exercise |
| Review verdict | AMEND |
| Tenets | 8 |
| Related decisions | MEM-001, MEM-002, MEM-004, MEM-009, SAF-007, LRN-001, LRN-004, EVL-004 |
| Open questions | Q6 |

## Decision

Deterministic verification enriches an outcome without overwriting observed telemetry: each verification run is appended as its own event carrying the verifier version, the exact command, the working-tree identity it ran against and its own pass/fail/indeterminate result, so that "appeared to succeed" and "verified to succeed" remain separately queryable and a verifier that ran against a drifted tree is distinguishable from one that ran against the turn's output.

1. **Verification has provenance.** A verification event records `verifier_version`, command line, protected-path policy version (SAF-007), tree identity (commit hash or content hash of touched files) and wall-clock start/end.
2. **Verification can be wrong, so it can be repeated.** Multiple verification events per `route_id` are permitted; a flaky or environment-failed run is recorded as `indeterminate`, not as `fail`, and label derivation (MEM-004) uses the latest non-indeterminate event.
3. **Verification against a drifted tree is not verification of the turn.** If the tree identity at verification time differs from the tree identity at `closed_turn` beyond the turn's own edits, the event is flagged `tree_drift=true` and is excluded from capability labels.

## Session verification implementation, 2026-09-07

Observation-only sessions have no routing decision. The applied local verifier therefore appends session-scoped receipts without fabricating route IDs. An operator-owned plan and SHA-pinned test artifacts live outside the task workspace; execution uses a separate snapshot. Started and finished receipts record task, verifier, plan, command, executable, source/snapshot and sandbox-implementation references, individual results and timestamps. Drift, unavailable execution, timeouts and unclassified exits are indeterminate. Only declared failure exits mean failure; no automatic task acceptance, result replacement or learning admission occurs.

Two repeated verifier jobs each passed eight tests on the same repaired pilot task. This tests provenance and non-overwrite behavior; verifier precision across tasks and automatic linkage to the exact task-close output remain unproved. Existing route-based verification and label-derivation semantics remain unchanged. The earlier planning note below is retained as history.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Product application: session verification, 2026-09-07

Observation-only product sessions have no routing decision. Their independent checks therefore
need session-scoped receipts, without fabricated route IDs or automatic learning labels. The
local operator verifier runs a versioned plan on a separate snapshot and records its identity,
check provenance and pass/fail/indeterminate result. Harness-authenticated event intake cannot
submit those receipts. Started and finished records append separately, and erasure follows the
existing session-key boundary. This is a scoped application of the verification principle;
route-based verification and its learning admission rules remain unchanged. Implementation
and validation are in progress; no additional maturity is claimed by this planning note.

## Offline verifier improvement implementation, 2026-09-07

Snapshot execution is extracted into a shared executor. The bound-session wrapper still validates the product binding and appends started/finished receipts; the standalone experiment reuses the execution envelope without asserting a session or inventing a route. Invalid product verify setup now exits 2, consistently distinguishing unavailability from assertion failure at exit 1. Existing session-verification behavior is covered by the full regression suite.

The current eight-test verifier and an eleven-test candidate were run against the same seven curated examples. Three known defects were falsely accepted by the current verifier and detected by the candidate; two correct implementations and one environment failure retained their classifications. Automatic attribution to the exact task-close output and accuracy across independent task families remain unproved.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## W3.1 retained operator captures, 2026-09-08

Scoped application: an internal retained operator capture preserves source A even after the working tree becomes B. Integrity-checked materialization returns A; missing or corrupted captures never fall back to the live tree. Capture attribution is restricted to operator_capture, without verification success or learning authority. The existing product verify command still snapshots its current workspace; binding its receipt to the retained copy is W3.3 work. Exact close requires the W3.2 supervisor.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

A start stores the initial included-tree manifest, source/workspace references and versioned bounds inside encryption. This preserves the starting point through retries and later edits without storing initial file contents. It remains an operator-time observation rather than proof of a supervised pre-execution boundary. The capture library is still independent; no retained capture is yet associated with a close request or verifier receipt. W3.2b/W3.3 must supply those links before task-output attribution or outcome quality is claimed.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b1 owned process groups, 2026-09-08

W3.2b1 separates a direct command's exit code from group-signal and launcher-reaping observations in an in-memory report. It records policy and source/executable identities and keyed request provenance without raw argv, environment, workspace paths or output. Exit zero is not verified quality; cleanup is not a whole-workspace barrier. Every report has exact-close and learning eligibility false. The primitive is not yet persisted or associated with a journal attempt, retained capture or verification receipt, and no existing evidence is overwritten.

See the [plain-language report](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b1-process-ownership-2026-09-08.json),
[runner](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_owner.py),
[launcher](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_anchor.py),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_process_owner.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/process-ownership.md).
All 669 tests and eleven checks pass on the recorded Darwin build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved. Full W3
and exact task-close attribution remain open.

## W3.2b2b2 process coordination, 2026-09-08

The coordinator preserves process observations separately from task conclusions. Every report keeps exact-close and learning eligibility false, and a rejected launch no longer borrows the previous launch's process report. Reports remain in memory; restart recovers only the durable workspace block, not an invented process outcome. Verification enrichment, retained captures and task-close association still need their remaining qualification.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2c writer-boundary research, 2026-09-08

Disposable host negative controls showed that mode 0400 and renaming a file do not revoke an already-open write descriptor. A stopped-container output copy was stable through the tested late-write window, but trusted daemon administration can still alter it. The proposed backend needs explicit stop/admission sealing, safe extraction and immutable artifact association before verification. The current capture/verification implementation is unchanged.

See the [plain-language report](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md),
[experiment and source evidence](../../reports/research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[fixture source](../../reports/research/writer-boundary-2026-09-08/probe.go),
[frozen packet](../../reports/waves/w3-2b2c-writer-boundary.md) and
[next ownership packet](../../reports/waves/w3-2b2d-resource-ownership.md).
The corrected research run completed six bounded observations, including negative controls.
The previously passing 759-test/eleven-check runtime source is unchanged; all 300 declared
hashes were reverified, not rerun. This research changes no runtime behavior, architectural
status, maturity, release authority or whole-W3 completion claim. Prior wording is retained.

## W3.2b2d2 launch-contract research and identity gate, 2026-09-08

The proposed close boundary separates known-launch stopping, where retained output may later enter B3 capture, from ambiguous-launch abort, where output must not be represented as a trusted completed task. The six relevant engine cases remain outstanding after two failed attempts. No capture/verification path changed; task-close attribution and active/plaintext custody remain open.

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

The known-start/kill/exit fixture produced two unchanged bounded reads across the scheduled late-write delay. The manual-restart control then demonstrated why an exited state or zero restart counter alone cannot justify task-close attribution. These are synthetic file observations; no verified task outcome, capture association, held-out evaluation or learning label was created.

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

A known acknowledged launch may reach a sealed, matching observed exit and retain its layer, while uncertain startup uses owned discard or remains uncertain. All exact-close and learning flags stay false. There is still no safe output extraction, immutable capture association, verified task-success outcome or learning label from this backend. Final engine workflow qualification also remains open after stopped-create reply loss.

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

Current pinned-engine known launch, sealed stop and failure recovery now pass, but no task-success outcome follows. Original receipt custody and policy compatibility improve the future evidence boundary; safe extraction and exact stop/capture association are still absent. Every workspace remains blocked and exact-close/learning eligibility stays false.

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

Running the tests must not overwrite what was observed at the time. If the verifier's result replaced the observed telemetry, the ledger would lose the single most useful signal for a router: "the model appeared to succeed but actually failed" — the case where the cheap rung is confidently wrong and no trip-wire fires. Keeping the observation and the verification as separate columns (now: separate events) is what makes that signal exist.

The amendment adds what "verification" needs to carry to be believable. A verifier is code execution against a working tree, and both the code and the tree change: tests are flaky, environments fail, and a developer keeps editing after the turn closes. Without the verifier's own provenance, a `verified=fail` event cannot be distinguished from "the tests were broken", "the environment was down" or "someone changed the file afterwards" — and every one of those would be recorded as a capability failure of the rung that served the turn.

## Adversarial review (2026-09-02)

### Steelman
Separating observation from verification is cheap, obviously correct, and required by MEM-001's append rule anyway. It preserves the "silent failure" signal that motivates the whole learned-router effort, and it gives EVL a way to measure label precision (observed vs verified) rather than assume it.

### Attacks
1. **The verifier is not ground truth; it is another noisy instrument with no recorded provenance.** Flaky tests are common (a large share caused by async waits and concurrency), and benchmark curation shows that a majority of "verified" coding tasks had invalid or over-specific tests before human review. A verification event with no verifier version, command or environment identity cannot be audited, so a verifier bug silently becomes a capability label. The decision says verification enriches; it does not say what an enrichment must contain.
2. **Verification runs after the turn, against whatever tree exists then.** The register admits automatic verification is "not connected to every eligible task" and `live_verification.py` runs post hoc. By the time it runs, the developer (or a later turn on a different rung) may have edited the same files. A pass then credits the wrong rung; a fail then blames the wrong rung. The decision must bind verification to a tree identity, or MEM-009's "explicit `route_id` only" rule is satisfied in form and violated in substance.
3. **"Enrich" hides a state transition.** MEM-002's lifecycle has no state for "verified"; verification may arrive before or after `closed_final`. If it arrives after, clause 2 of MEM-002 (late evidence re-derives the label) applies; if the decision does not say so, an implementation will reasonably treat `closed_final` as terminal and drop the verification. The two decisions need an explicit seam.
4. **One task.** The code reality is that exactly one task has strong test-based verification. The non-overwrite contract is tested, but the decision's value proposition — a stream of observed-vs-verified pairs — has a sample size of one task. Claiming D2 for the contract is fair; claiming any evidence about label precision from it is not.
5. **Verifier under SAF-007 may be constrained into indeterminacy.** Protected-path and execution policy can prevent the verifier from running the real test suite (e.g. tests that touch a payments sandbox, secrets, or network). The result is then neither pass nor fail. Without an `indeterminate` outcome the policy-blocked run will be recorded as a failure — a policy failure masquerading as capability, which is exactly what MEM-004 exists to prevent.

### Evidence
- Q. Luo, F. Hariri, L. Eloussi, D. Marinov, "An Empirical Analysis of Flaky Tests" (FSE 2014) — 201 flaky-test fixes across 51 Apache projects; async wait (45%), concurrency (20%) and test-order dependency (12%) account for 77%; supports attack 1 and clause 2 — https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf
- OpenAI, "Introducing SWE-bench Verified" (2024) — 93 professional developers screened 1,699 SWE-bench samples; 68.3% had at least one severe issue (underspecified statement, over-specific/invalid tests, environment failures); GPT-4o resolved 33.2% on the verified subset vs 16% on the original. Shows that "the tests passed/failed" is itself an unreliable label without curation; attack 1 — https://openai.com/index/introducing-swe-bench-verified/
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021 Datasets & Benchmarks) — average ≥3.3% label errors across 10 benchmark test sets, ≥6% on ImageNet val; small error rates change model rankings. Bears on attack 4: ranking rungs on a thin, noisy verified set is unstable — https://arxiv.org/abs/2103.14749
- W3C, "PROV-DM" — activities `used` entities and `generated` new ones; a verification run is an activity whose inputs (tree, verifier) should be recorded as used entities, which is what clause 1 asks — https://www.w3.org/TR/prov-dm/

### Verdict
**AMEND.** The core rule (never overwrite observation) is right and stays verbatim in spirit. Attacks 1, 2 and 5 land: a verification event with no provenance, no tree binding and no indeterminate result is a label-noise generator, and the SAF-007 interaction produces policy failures typed as capability failures. Attack 3 is fixed by cross-reference to the amended MEM-002. Attack 4 does not change the text but caps what the D2 label means.

## Amendments applied

- Added: each verification run is its own appended event (not a column on the outcome), with verifier version, command, tree identity and result (clause 1).
- Added `indeterminate` as a verification result for flaky/env/policy-blocked runs; label derivation uses latest non-indeterminate event (clause 2).
- Added `tree_drift` flag and exclusion from capability labels when the tree at verification time differs from the tree at `closed_turn` beyond the turn's own edits (clause 3).
- Rationale updated to state the seam with MEM-002 (verification after `closed_final` is late evidence).

## Follow-ups

- [ ] Extend `verifier.py` / `live_verification.py` output with `verifier_version`, command, tree identity, policy version and `indeterminate`; golden test that a SAF-007 path block produces `indeterminate`, not `fail`.
- [ ] Golden test: edit a verified file after `closed_turn`, run verification, assert `tree_drift=true` and that MEM-004 label derivation ignores it.
- [ ] Golden test: verification arriving after `closed_final` produces a `late_evidence` event and re-derives the label (seam with MEM-002).
- [ ] Report observed-vs-verified disagreement rate per rung in the EVL pack; until ≥2 tasks have strong verification, mark the number as anecdotal.
- [ ] Re-run each verification twice on the one strongly-verified task to measure its own flake rate before it is used as a label source.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded versioned creation/active transport separation and passing pinned-engine lifecycle acceptance | Prior decision/evidence preserved; bounded d2 closes, full W3 and grades unchanged |
| 2026-09-08 | Recorded W3.2 fixture launch prototype, offline checks, engine failures and operator cleanup exception | Prior decision/evidence preserved; engine workflow remains unqualified, no status/maturity promotion |
| 2026-09-08 | Recorded W3.2 identity correction and seven accepted bounded launch observations | Prior wording and failed evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d2 failed launch probes, source-explained identity gate and proposed lifecycle | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2b2 stop coordination, permanent workspace blocking and failure evidence | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b1 process ownership and tested cleanup limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: verification events carry provenance, tree identity and an indeterminate result; drifted-tree runs excluded from capability labels | "Deterministic verification enriches an outcome without overwriting observed telemetry." |
