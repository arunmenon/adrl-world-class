# ADRL-MEM-010 — Retention and erasure of ledger and derived artefacts

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Proposed 2026-09-02 (new, from adversarial review) · amended 2026-09-03 (proposed amendment, pending disposition) |
| Maturity | Historical review baseline: D0. Product observation erasure has scoped D2 evidence (2026-09-07); full ledger/derived-data/client-copy erasure remains incomplete |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8 |
| Related decisions | MEM-001, MEM-005, MEM-007, SAF-002, SAF-003, OPS-001, EVL-009 |
| Open questions | Q5 |

## Decision

Every field in transaction memory, as enumerated by the field-level data inventory of MEM-005 clause 5, has a declared retention period and an erasure procedure: prompt-class fields (embeddings, keyed hashes, retrieval keys, path and target evidence, command lines, verifier output) are stored encrypted under per-session keys and erased by crypto-shredding; the `route_id` skeleton (timestamps, rung, deployment id, failure type, event types, costs) is retained for evidence without prompt-derived content; erasure is triggered by retention expiry, a late privacy pin (MEM-005), or an explicit security/data-subject request, is itself an appended event, forces invalidation of every projection that held the shredded content, and is proven by an erasure test that reads every store the inventory names, including the WAL and backups, and finds no plaintext.

1. **Two storage classes.** *Evidence skeleton* — no prompt content, retained for the evidence horizon EVL needs (proposed: 24 months, reviewed annually). *Prompt-class artefacts* — retained no longer than the shorter of the retrieval usefulness horizon (proposed: 90 days) and the repository's own data-classification policy.
2. **Crypto-shredding by session.** Prompt-class rows are encrypted under a per-session key held in a local keystore; erasing a session is deleting its key and appending an `erased` event naming the session and reason. The ledger rows remain, unreadable.
3. **Erasure reaches projections.** An `erased` event invalidates any projection whose high-water mark predates it (MEM-007 clause 3); the NumPy index is rebuilt without the affected vectors before retrieval resumes.
4. **Erasure is auditable, not silent.** Counts of erased sessions and their reasons are reported in the EVL pack; an erasure that removes evidence from an evaluation window is an EVL-009 blocker for that window, never averaged away.
5. **Erasure proof.** `adrl erase --session` is followed by an erasure check that opens every inventoried store (ledger, egress ledger, verification job store, projections, WAL, the most recent backup) and asserts that no field classed `encrypted` or `keyed` for that session is readable; the check's result is appended as an `erasure_verified` event and its failure is an EVL-009 blocker.

## Product service evidence, 2026-09-07

Server-side session-key erasure covers encrypted public observation envelopes; timeline reads show them as erased, and the API refuses to recreate an erased evidence key, including when erasure preceded binding. Immutable reference skeletons remain under the existing retention design. The separate client assertion/outbox directory is not erased by the server; its retention and erasure procedure remains pilot acceptance work.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

## Session verification implementation, 2026-09-07

Session-key erasure makes local verification receipts unreadable and prevents subsequent verifier writes from recreating a key. Tests cover erasure before a run and during a check; the latter leaves an erased started record and refuses a finished receipt. Timeline skeletons remain. Local operator plans, CLI output, temporary/captured evidence and client outboxes remain separate lifecycle obligations; this is not a claim that all copies have been deleted.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Offline verifier improvement implementation, 2026-09-07

Experiment-key erasure reuses the append-only keystore audit and prevents later archive writes from recreating a shredded key. An existing CLI archive with missing master/HMAC key files is refused rather than silently re-keyed. Unit checks cover erasure and refusal to append; the actual CLI erasure exercise used a separate archive copy. All 30 skeleton records remained with unreadable payloads, while the primary archive remained readable.

Erasing a private archive does not erase exported history, source fixtures, plans, CLI output or backups. Losing the host HMAC key also prevents mapping experiment IDs back to records. These remaining-copy obligations are explicit and no regulatory erasure guarantee is inferred.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## W3.1 retained operator captures, 2026-09-08

Captures reuse the bound session key and never create one. Erasure is rechecked before append and on reads; restoring an old wrapped key cannot bypass an intact erasure audit. Tests also exercise erasure before queued append. Erased ciphertext remains and still consumes quota. Already returned objects and active plaintext leases cannot be retroactively withdrawn; context exit cleans temporary copies, but process death can leave them behind. Active-lease coordination, startup reconciliation, broader copy policy and retention recovery remain blockers before actual task payload capture. This does not resolve DQ6 or establish physical deletion.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

The attempt journal reuses the session key and rechecks erasure before queued append and fresh access. An intact erasure audit defeats restoration of an old wrapped key. Erased ciphertext remains counted against quota. Erasing a pending attempt can leave its workspace reservation blocked, and quota exhaustion can prevent appending a terminal event; neither is silently converted into released ownership. Terminal-record capacity reservation and coordinated erasure/release remain prerequisites for real execution. This synthetic-fixture slice does not resolve DQ6, active plaintext leases or physical deletion.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b2a reserved terminal capacity, 2026-09-08

W3.2b2a reserves logical quota for a terminal record without bypassing erasure, credential expiry or integrity checks. Erasing a pending attempt leaves its commitment charged and journal workspace reservation blocked; the grant does not restore a key or silently authorize release. Schema 9 preserves old encrypted rows, and v1 records are not retroactively granted capacity. Coordinated process cleanup, erasure and reservation release remain the next gate before real supervised execution; active plaintext leases, crash leftovers, physical storage failure and wider erasure qualification remain open.

See the [plain-language report](../../reports/adrl-w3-2b2a-terminal-capacity-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b2a-terminal-capacity-2026-09-08.json),
[journal](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py),
[capacity migration](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/migrations/0009_attempt_capacity.sql),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_capacity.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 697 tests and eleven checks pass for the recorded build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved.
No exact task-close, learning or full-W3 completion claim follows.

## W3.2b2b1 persistent key revocation, 2026-09-08

A W3.2b2b1 fault probe reproduced an ordering hole: deleting the wrapped key before its failed shred audit permitted restored-key reads and replacement-key creation for the same session. The keystore now publishes and flushes persistent revocation before mutation. Reads/presence checks deny revoked keys and creation raises KeyRevokedError; an attached legacy erased/shredded audit also denies restored files. Marker/removal/audit failure and process death retain explicit failure/denial; retry can finish logical file cleanup without removing revocation. No process-stop, physical-block/backup erasure, cached-key recall, workspace/grant release or whole-keystore rollback protection is claimed. This implements the intended no-resurrection rule without changing erasure triggers or privacy pins.

See the [plain-language report](../../reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md),
[checks and pre-change probe](../../reports/research/adrl-w3-2b2b1-key-revocation-2026-09-08.json),
[keystore](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/keystore.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_key_revocation.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/key-revocation.md).
All 724 tests and eleven checks pass for the recorded Darwin build. Prior wording,
architectural status and maturity fields remain unchanged. Independent security review,
process/erasure/release coordination and full W3 remain open.

## W3.2b2b2 process coordination, 2026-09-08

The running coordinator observes persistent revocation, expiry and unreadable authority to request owned-group cleanup, including direct keystore revocation or another erasure-service instance. Erasure does not wait for an encrypted terminal record or group cleanup. A revocation can race launch; receipts do not certify process or plaintext cleanup. Pre-marker key contention remains a surfaced erasure failure, and the observer may honestly report authority_unavailable before seeing revocation. No key recreation or workspace release follows.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2c writer-boundary research, 2026-09-08

A container writable layer is another plaintext storage location. The experiment used only synthetic text and removed/reconciled its eight containers and two images; it is not a production erasure design. Ledger key revocation alone cannot erase an execution workspace, active descriptor or other plaintext copy. Before real payloads, the proposed backend must cover retained layers/exports, cleanup failure, crash leftovers and recovery authority after content-key erasure.

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

Host-authenticated ownership evidence survives session-key erasure so a trusted local operator can remove an already-bound never-started object without recovering a content key. Erased access cannot authorize a new create, while revocation can still race a previously admitted daemon request. Cleanup metadata is pseudonymous/linkable and deliberately retained. Non-force removal plus observed absence does not prove physical, snapshot, backup or active plaintext erasure. Real-data retention and active/crash copy cleanup remain separate gates.

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

The two self-authored fixtures independently exited; exact original create receipts, engine/image/name/command and all explicitly requested controls were verified before non-force removal and absence confirmation. The sole imported image was removed. This fixture recovery does not qualify active-process/plaintext erasure or a general cleanup bypass. Proposed active cleanup remains separable from erased session keys but is not implemented.

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

The changed experiment supports exact-owned discard for its delayed/lost-start orderings. It does not implement host-authenticated active cleanup after content-key erasure, permanent launch denial or active plaintext leases. Those mechanisms remain in the next runtime packet. Fixture removal leaves permanent workspace fences unchanged and makes no physical-erasure or retention-policy claim.

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

The fixture prototype can discard an authenticated active resource after content-key erasure and can separately report audit failure while attempting independently authorized emergency cleanup. Repeated ordinary recovery does not reissue a recorded discard. This does not settle active plaintext leases, physical erasure, real-payload retention or full owner/host-death guarantees. Permanent fences remain blocked and both outcome eligibility flags stay false.

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

The fresh current-source engine cases demonstrate host-authenticated discard after active content-key erasure and recovery after owner death for the pinned fixture. Original-create cancellation still drains its worker. This does not establish active plaintext-copy erasure, physical erasure, real-payload retention or a general independent watchdog. Permanent denial and false outcome eligibility remain.

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

MEM-001 makes the ledger immutable and MEM-005 (as replaced) makes the embedding store a lossy copy of the company source code and developer intent. Together those two decisions, without this one, describe a system that accumulates prompt-equivalent data forever with no lawful or operational way to remove it. That is untenable for a payments company on three independent grounds: data-subject rights (developers are data subjects; the instruction stream is personal data), security incident response ("a production key was in a fixture file that the model read; where did it go?"), and the SAF-002 late-pin case, where turns embedded before a pin fired must be removed under an immutable-row rule.

Event-sourcing practice has converged on the answer: keep personal content out of the stream or encrypt it under per-subject keys and shred the key; rebuild projections afterwards. Applying that here is cheap at current scale (one SQLite file, one NumPy index) and becomes very expensive later if the ledger has grown without the key structure. This is a Phase 1 decision that should be made before the corpus is large enough to matter.

## Adversarial review (2026-09-02)

### Steelman
This decision is the missing complement to MEM-001 and MEM-005: immutability plus prompt-class data plus no erasure path is a compliance and incident-response gap, and the standard mitigation (crypto-shredding with per-subject keys, projection rebuild) is well understood and fits the existing architecture (append-only ledger, rebuildable projections) with minimal disruption.

### Attacks
1. **Shredding removes evidence, which EVL-009 says must never be averaged away.** If a security erasure removes 40% of a month's sessions, that month's readiness numbers are no longer what they were. Answered by clause 4: erasure that touches an evaluation window is a blocker for that window and the skeleton (which carries rung, failure type and cost) survives, so cost/reliability evidence is preserved and only retrieval/learning content is lost.
2. **Per-session keys are a key-management burden on a developer laptop.** A local keystore that is lost makes the whole prompt-class store unreadable — which is the safe failure, and equivalent to "the index was rebuilt from nothing". Acceptable at current scale; must be revisited under OPS-001 when the store is shared.
3. **Retention periods are guesses.** 90 days for retrieval usefulness and 24 months for evidence are proposals with no data. Answered: they are declared as proposals to be replaced by measured numbers (time-to-close distribution from MEM-002; retrieval neighbour-age distribution from MEM-008 shadow logs).
4. **Encryption adds latency to the embedding path.** Symmetric encryption of a vector row is microseconds; the retrieval index is rebuilt in plaintext in memory from decrypted rows and is itself ephemeral. Not a material cost.

### Evidence
- Microsoft Azure Architecture Center, "Event Sourcing pattern" — for "right to be forgotten": store personal data outside the stream by reference, or crypto-shred with per-subject keys; both require projection rebuilds — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- M. Rook, "Forget me please? Event sourcing and the GDPR" (2017) — compares crypto-shredding, direct deletion and stream rewriting; notes key-management burden and that projections must be rebuilt — https://www.michielrook.nl/2017/11/forget-me-please-event-sourcing-gdpr/
- J. Morris et al., "Text Embeddings Reveal (Almost) As Much As Text" (EMNLP 2023) — why embeddings are in scope for erasure at all — https://arxiv.org/abs/2310.06816
- (authors not captured) "Rethinking the Privacy of Text Embeddings: A Reproducibility Study" (arXiv 2507.07700, 2025) — quantisation/noise as complementary mitigation for stored embeddings — https://arxiv.org/abs/2507.07700

### Verdict
**PROPOSED (new).** The bucket needs this decision for MEM-001 and MEM-005 to be jointly tenable; the attacks are operational and answered by clauses 1–4. Recommend acceptance at D0 with the retention periods marked provisional.

## Adversarial review (2026-09-03)

### Steelman
Crypto-shredding by session is the standard event-sourcing answer and the implementation built it for embeddings.

### Attacks
1. **Shredding one key erases only what that key encrypts.** Classification and verification rows were plaintext; the `erased` event claimed unreadability the stores did not have.
2. **WAL and backups are stores too.** A WAL frame or a backup taken before shredding still holds the ciphertext, which is fine, and any plaintext field, which is not.
3. **An unproven erasure is a claim.** Without a test that reads the stores after shredding, MEM-010 clause 2's "ledger rows remain, unreadable" is unverifiable.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P1-5, verified.

### Verdict
**AMEND (proposed).** Scope bound to the field-level inventory; erasure proof added as clause 5. Pending disposition.

## Amendments applied

New decision — no prior text.
- 2026-09-03: scope bound to `data-inventory-v1`; skeleton gains the deployment id; erasure proof (clause 5) covering WAL and backups.

## Follow-ups

- [ ] Add per-session key generation and encryption of `embeddings` rows and keyed-hash columns in `memory_sqlite.py`; keystore location documented in OPS.
- [ ] Implement `erased` event type; golden test: erase session → key gone, rows unreadable, projection invalidated and rebuilt, EVL window flagged.
- [ ] Wire SAF-002 pin to trigger erasure of the session's pre-pin prompt-class rows (MEM-005 clause 2).
- [ ] Measure neighbour-age distribution in shadow retrieval and time-to-close in MEM-002 to replace the provisional 90-day / 24-month figures.
- [ ] Confirm with the company data governance which classification the embedding store falls under and whether the 24-month evidence horizon is permissible.
- [ ] 2026-09-03: implement the erasure check over every inventoried store; golden test: erase a session, then grep every store including WAL and a fresh backup for any plaintext locating field.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded versioned creation/active transport separation and passing pinned-engine lifecycle acceptance | Prior decision/evidence preserved; bounded d2 closes, full W3 and grades unchanged |
| 2026-09-08 | Recorded W3.2 fixture launch prototype, offline checks, engine failures and operator cleanup exception | Prior decision/evidence preserved; engine workflow remains unqualified, no status/maturity promotion |
| 2026-09-08 | Recorded W3.2 identity correction and seven accepted bounded launch observations | Prior wording and failed evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d2 failed launch probes, source-explained identity gate and proposed lifecycle | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d1 stopped ownership, acknowledgement recovery and explicit limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2b2 stop coordination, permanent workspace blocking and failure evidence | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2b1 key-revocation ordering fix, fault evidence and remaining recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2a versioned terminal capacity, compatibility and recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-09-07 | Distinguished tested server observation erasure from the full retention contract | Maturity: D0 Design, review recommends D0 Design — nothing exists |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-09-02 | Proposed (adversarial review) | — |
| 2026-09-03 | Amended (proposed, external review): inventory-bound scope and erasure proof | "Every class of content in transaction memory has a declared retention period and an erasure procedure: prompt-class artefacts (embeddings, keyed instruction hashes, retrieval keys) are stored under per-session keys and erased by crypto-shredding; the `route_id` skeleton (timestamps, rung, failure type, event types, costs) is retained for evidence without prompt-derived content; erasure is triggered by retention expiry, a late privacy pin (MEM-005), or an explicit security/data-subject request, is itself an appended event, and forces invalidation of every projection that held the shredded content." |
