# ADRL-MEM-005 — Prompt-derived artefacts are prompt-class data

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Superseded 2026-09-02 (see replacement) · replacement amended 2026-09-03 (proposed amendment, pending disposition) |
| Maturity | D2 Tested, review recommends D1 Code for the replacement — the suppression path is tested, but the replacement's storage-class, retention and late-pin clauses have no implementation |
| Review verdict | REJECT |
| Tenets | 2, 8 |
| Related decisions | SAF-002, SAF-003, SAF-005, MEM-001, MEM-007, MEM-008, MEM-010 (proposed), LRN-004, OPS-001 |
| Open questions | Q5 |

## Decision

Raw prompts are never stored in the ledger; prompt-derived artefacts (embeddings, instruction hashes, any retrieval key computed from prompt content, and every field that can locate or reproduce prompt content: repository paths, remotes, tool targets, command lines, verifier output, working-directory evidence) are classified as prompt-class data under a field-level data inventory, are stored only keyed or encrypted under the same access, retention and erasure controls as the prompt itself would be, and are not produced at all for private, secret or privacy-pinned turns, including turns earlier in a session that is later pinned.

1. **Embeddings are the prompt, statistically.** The embedding store is treated as a lossy copy of the corpus: same access control as source code, per-session encryption or crypto-shreddable keys (MEM-010), a retention period, and no export outside the host without the same review a source export would get.
2. **Pin suppression is retroactive within the session.** When SAF-002 pins a session at turn *k*, embeddings and instruction hashes already written for turns 1…*k−1* of that session are shredded, because the scanner (SAF-003) is precision-limited and the secret may have been present earlier.
3. **Hashes are pseudonyms, not anonymisation.** Instruction hashes are keyed (HMAC with a host-local secret) so an attacker with the database cannot dictionary-match short or common instructions; the key is rotatable and rotation is recorded as a projection rebuild (MEM-007).
4. **Opt-in raw storage is a separate decision.** If any raw prompt retention is ever wanted (for debugging or labelling), it requires its own ADR with a named owner, scope and retention; this decision does not grant a "by default" exception.
5. **Field-level inventory.** `data-inventory-v1` lists every column and JSON payload key the ledger, the egress ledger, the verification job store, the WAL, backups and projections can hold, with a class (`skeleton`, `keyed`, `encrypted`, `forbidden`) and the erasure mechanism that reaches it; a schema test fails when a field is written that the inventory does not list, and no field may be `raw` if it can contain a path, an argument, a command line, tool output or free text.

## Product service evidence, 2026-09-07

Public caller envelopes use the existing per-session encryption boundary. Tool hooks discard raw input, output, error text and paths before producing observations. ADRL credential headers are withheld from the gateway and redacted in recorded header views. The client connection and encrypted outbox have a separate lifecycle, so server erasure alone does not cover all client copies.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

## Session verification implementation, 2026-09-07

The complete session verification receipt is encrypted under the existing session key. Task, source/snapshot, plan, command and output references remain inside that encrypted envelope; command output tails are represented by keyed references, not raw logs. The persistence inventory covers 249 fields. Operator plans, temporary code snapshots, CLI output and exported evidence are separate copies with their own retention responsibilities. This scoped addition does not complete the broader prompt-derived-artifact lifecycle.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Offline verifier improvement implementation, 2026-09-07

Proposals, expected answers, source paths, fixed input digests, plans, trial receipts and assessments are encrypted as full experiment evidence envelopes. Clear fields are limited to sequence, namespaced keyed identity, event type, keyed record identity, nonce and timestamp. The persisted-field inventory now covers 256 fields.

Published local evidence exports deliberately preserve the curated proposal, fixtures and complete history for review. These copies, temporary snapshots, plans, CLI output and backups have separate retention. Encryption and source hashing are scoped storage/provenance measures, not a claim of anonymity or full prompt-derived-artifact lifecycle completion.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## W3.1 retained operator captures, 2026-09-08

The complete capture request, raw attempt/task identifiers, source/workspace references, policy, paths, modes and file bytes are session-key encrypted. Only keyed capture/session/attempt identities and an append skeleton are plaintext. Count/size limits are versioned, and the table-wide ciphertext-plus-nonce quota includes erased records. The inventory now accounts for 263 fields. In-memory objects and temporary materializations are separate copies with explicit lifetime limits; only synthetic fixtures use this internal slice.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

Raw commands, task/attempt/capture IDs, initial manifest paths/hashes, reasons and policy are session-key encrypted. Session/attempt/event/workspace pseudonyms and phase/sequence/time form the authenticated append skeleton. The canonical workspace pseudonym is host-keyed to support journal admission across sessions. No new plaintext materialization or file-content archive is introduced. The inventory accounts for 273 fields. Limits bound encoded events and logical ciphertext-plus-nonce bytes; SQLite/WAL overhead and external copies retain their separate scope.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b2a reserved terminal capacity, 2026-09-08

W3.2b2a inventories six new schema-9 fields: the authenticated capacity-version header; existing keyed session, attempt and start-event references; and reserved-byte/admission-ceiling metadata. The full v2 policy remains inside the encrypted start event. No raw paths, arguments, environment, source contents or new plaintext materialization is added. The checked inventory now accounts for 279 fields. Grant metadata and existing keyed references remain after key shredding; no anonymization, new retention disposition or complete backup/active-copy erasure proof is claimed.

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

W3.2b2b1 documents three filesystem metadata entries beyond the existing 279 schema/payload fields: revocation identity, a fixed version marker and an empty coordination lock. Production filenames reuse the existing session pseudonym; marker contents include no key, raw path, reason or task material. Atomic-write temporary files can contain raw host secrets or wrapped session keys and are explicitly described as key material, not harmless metadata. Identity-scoped pending-file cleanup is tested, while cached plaintext, snapshots, backups and full restoration/erasure qualification remain open.

See the [plain-language report](../../reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md),
[checks and pre-change probe](../../reports/research/adrl-w3-2b2b1-key-revocation-2026-09-08.json),
[keystore](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/keystore.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_key_revocation.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/key-revocation.md).
All 724 tests and eleven checks pass for the recorded Darwin build. Prior wording,
architectural status and maturity fields remain unchanged. Independent security review,
process/erasure/release coordination and full W3 remain open.

## W3.2b2b2 process coordination, 2026-09-08

Execution-fence metadata contains only four keyed identifiers, host key ID, bounded operational policy and timestamp, adding seven classified fields. It contains no raw path, command, environment, output, task label, PID or plaintext capture. Session erasure leaves the block intact. Keyed metadata is not claimed anonymous; existing retention limits, active-copy obligations and rollback limitations remain.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2d1 stopped resource ownership, 2026-09-08

New ledger records contain host/session-keyed references, resource/image IDs, timestamps, policy and MACs. Raw workspace paths, argv, environment and profile JSON stay out of this new history. The field inventory now includes every ResourceEvent and nested ResourcePolicy field. The engine still holds stopped-container configuration and a synthetic writable layer; this is not a claim that all daemon-side data is encrypted or erasable, nor approval for real payload retention.

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

Research retained raw synthetic before/after inspections and showed that a future execution-identity projection must be versioned and linked to the unchanged raw preparation record. The projection, capability metadata and permanent denial marker are proposed only; no new runtime plaintext or ledger field was introduced. Existing inventory remains 325 checked fields/328 documented entries. Future additions require their own field-level inventory and retention scope.

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

All seven originally receipted disposable containers and the one imported image were confirmed absent. Private synthetic research records remain for review and are linkable. Resource removal does not demonstrate active-copy, cache, snapshot, backup or physical erasure. Runtime content-key handling, product metadata inventory and erasure policy are unchanged.

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

Execution metadata, permanent denial and separate recovery locks survive content-key erasure for host-authenticated cleanup. The inventory now checks 370 fields and documents 380 entries; references, resource IDs, times and filesystem metadata remain linkable. Eight synthetic fixtures and one image were removed, including one explicitly documented operator exception for a never-started unreceipted candidate. No physical, snapshot, backup or arbitrary active-copy erasure claim follows.

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

The inventory adds active_request_seconds: 371 checked fields and 381 documented entries. Closed transport causes stay transient or in private synthetic diagnostics; no raw error text or task content enters the product ledger. Thirteen fixtures and the one image were removed using original receipts, with no operator exception in this packet. Active copies, snapshots, physical blocks and retention policy remain separate limits.

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

The default is not to keep your code, and derived data counts as data. The original decision got the second half of that sentence right for private and secret turns and wrong for everything else: it stored embeddings of every non-private prompt as if a vector were not a prompt. The embedding-inversion literature has closed that gap — 32-token inputs are recovered exactly 92% of the time from a state-of-the-art encoder, and zero-shot methods now do it with only black-box encoder access, which any holder of `router-memory.db` plus the local embedding model has. Instruction hashes fare no better: a hash of a short developer instruction is a pseudonym that falls to a dictionary of common instructions, not an anonymisation.

The replacement keeps the intent — no raw prompts, suppress for sensitive turns — and adds the consequence: the embedding store is a lossy copy of the company source code and developer intent and must be handled as one. It also closes the late-pin hole: SAF-002 pins a session one-way from the moment a secret is detected, but the turns before detection were already embedded and, under MEM-001, those rows are immutable. The honest cost stated in the original ("lost learning signal on the sessions we understand least") remains and gets slightly larger.

## Adversarial review (2026-09-02)

### Steelman
Not storing raw prompts is the right default and suppressing derived artefacts for flagged turns is more than most systems do; SAF-003's "a vector built from your prompt is still your prompt, statistically" shows the authors understood the risk. The decision is tested (`memory_facade.py` removes raw instructions, hashes normal ones, skips embeddings for private tasks) and the honest acknowledgement of lost signal is exemplary.

### Attacks
1. **The decision contradicts its own rationale.** The rationale says derived data counts as data; the decision stores derived data for every non-private turn. Embeddings of ordinary coding prompts at the company contain file paths, function names, business logic, ticket text and frequently the surrounding code. Inversion recovers this. The distinction the decision draws (private vs not) is a scanner output, and SAF-003 is at D3 precisely because its precision is not established — so the unprivileged embedding store contains everything the scanner missed.
2. **The attacker model is weak.** Inversion attacks in the literature assume black-box access to the encoder. ADRL's encoder is a local model shipped with the router; anyone with read access to `router-memory.db` (a file on a developer laptop, or on a shared host under OPS-001) has both. This is a stronger attacker position than the papers assume, not weaker.
3. **Late pin, immutable ledger.** SAF-002 makes the pin one-way for the rest of the session; nothing un-embeds the turns before the pin. Under MEM-001 those rows are immutable and under MEM-007 they are already in the NumPy index. The most common way a secret enters a session is "it was in a file the model read three turns ago"; the pin fires late and the embedding survives.
4. **Instruction hashes are re-identifiable.** Unkeyed hashes of instructions like "fix the failing test", "add logging", "update the README" are trivially dictionary-matched; hashes of unique instructions are unique identifiers linking sessions. Hashing low-entropy inputs is widely understood not to anonymise them. The decision treats "hash" as a privacy control; it is at best a pseudonym and needs a key.
5. **"By default" is a hole.** "Raw prompts are not stored by default" implies a non-default. Who can turn it on, for what, for how long, and where is it logged? At a payments company an undocumented opt-in for storing developer prompts is a PCI/data-governance finding waiting to happen.
6. **No retention, no erasure.** Combined with MEM-001's immutability, the embedding store grows forever and has no deletion path. A security incident ("that repo had a leaked production key in a fixture file for two weeks") has no procedure. This is the gap MEM-010 (proposed) fills; MEM-005 must at least reference it.

### Evidence
- J. Morris, V. Kuleshov, V. Shmatikov, A. Rush, "Text Embeddings Reveal (Almost) As Much As Text" (EMNLP 2023; arXiv 2310.06816) — iterative correction-and-re-embed (Vec2Text) recovers 92% of 32-token inputs exactly and extracts full names from clinical-note embeddings; attacks 1, 2 — https://arxiv.org/abs/2310.06816
- (authors not captured) "Rethinking the Privacy of Text Embeddings: A Reproducibility Study of 'Text Embeddings Reveal (Almost) As Much As Text'" (arXiv 2507.07700, 2025) — replicates Vec2Text in- and out-of-domain, including recovery of password-like strings; finds Gaussian noise and especially quantisation mitigate inversion; supports both the threat and the mitigation options — https://arxiv.org/abs/2507.07700
- (authors not captured) "Universal Zero-shot Embedding Inversion" (arXiv 2504.00147, 2025) — ZSInvert recovers key semantic content with only black-box encoder access and no per-encoder training, far fewer queries than Vec2Text; attack 2 — https://arxiv.org/abs/2504.00147
- (authors not captured) "ALGEN: Few-shot Inversion Attacks on Textual Embeddings using Alignment and Generation" (ACL 2025; arXiv 2502.11308) — few-shot inversion via embedding-space alignment; appears in search results with matching title, not fetched; cited for existence of the few-shot regime only — https://arxiv.org/abs/2502.11308
- Microsoft Azure Architecture Center, "Event Sourcing pattern" — recommends keeping personal data out of the immutable stream by reference or crypto-shredding with per-subject keys; the pattern the replacement adopts for embeddings (attack 6) — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- L. Demir, A. Kumar, M. Cunche, C. Lauradoux, "The Pitfalls of Hashing for Privacy" (IEEE Communications Surveys & Tutorials, 2018) — title and venue confirmed from search results; the full text could not be fetched (access denied), so it is cited only as the standard reference that hashing enumerable identifiers is not anonymisation; attack 4 otherwise argued from first principles — https://ieeexplore.ieee.org/abstract/document/8023740/

### Verdict
**REJECT.** Attack 1 is fatal to the decision as written: it rests on a distinction (raw vs derived) that its own rationale rejects and that the inversion literature has dissolved, and the tested implementation faithfully implements the flawed distinction. Attacks 2–4 show the practical consequences are worse in this deployment than in the papers (local encoder, immutable ledger, late pins, unkeyed hashes). Attack 5 is a governance hole. The replacement keeps every safety property the original had, reclassifies embeddings and hashes as prompt-class data, makes pin suppression retroactive within the session, keys the hashes, and hands retention/erasure to MEM-010. The cost — slightly more lost learning signal and an encryption/shredding path — is the price of the tenet.

## Adversarial review (2026-09-03)

### Steelman
The replacement correctly named embeddings and hashes as prompt-class data and made suppression retroactive; the implementation encrypted embeddings per session and keyed instruction hashes.

### Attacks
1. **The list of prompt-class fields was not exhaustive.** The implementation stored raw working directories, remotes and touched paths in classification events, raw workspace paths, argv plans and up to 400 characters of verifier stdout and stderr in verification rows, none of which the session key covers; erasure shredded the key and left them readable.
2. **"Derived from prompt content" is the wrong test.** Verifier output is derived from the workspace, not the prompt, and can contain code or secrets just the same; the test must be "can locate or reproduce content".
3. **Unlisted fields drift in silently.** Every new payload key is a new leak unless a schema test binds writes to an inventory.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P1-5, verified: `repo_class.py` evidence payloads, `verification.py` job and event payloads, `erasure.py` scope.

### Verdict
**AMEND (proposed).** Replacement text widened to a field-level inventory with a schema test; MEM-010 carries the erasure proof. Pending disposition.

## Amendments applied

- Superseded. Replacement text above. Concretely: "not stored by default" → "never stored" with a separate-ADR path for any exception; embeddings and hashes reclassified as prompt-class data with the same access/retention/erasure controls; suppression extended to pre-pin turns of a pinned session; instruction hashes must be keyed; reference to MEM-010 for retention and erasure.
- 2026-09-03: prompt-class definition widened to every locating or reproducing field; clause 5 adds `data-inventory-v1` and a schema test binding writes to it.

## Follow-ups

- [ ] Run Vec2Text or a zero-shot inversion against a sample of ADRL's own embeddings (local encoder, local DB) and report exact-match and semantic-recovery rates in the EVL pack; this is the number that justifies the reclassification.
- [ ] Evaluate quantisation/noise on stored embeddings (per the reproducibility study) against retrieval quality in `shadow_retrieval.py`; if retrieval survives 8-bit quantisation, adopt it as defence in depth.
- [ ] Implement retroactive shredding on pin: golden test — embed turns 1–3, pin at turn 4, assert turns 1–3 have no embedding rows and the NumPy index is rebuilt without them.
- [ ] Replace unkeyed instruction hashes with HMAC under a host-local key; golden test that the same instruction hashes differently on two hosts.
- [ ] Remove or explicitly document any code path that stores raw instructions; grep `memory_facade.py` and the proxy for raw-prompt persistence and add a CI assertion.
- [ ] Draft ADRL-MEM-010 (retention and erasure).
- [ ] 2026-09-03: publish `data-inventory-v1` covering `decisions`, `events`, `lineage_events`, `verification_jobs`, `egress_events`, projections, WAL and backups; convert repository evidence, workspace paths, argv and verifier output to keyed or encrypted fields; schema test for unlisted fields.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded versioned creation/active transport separation and passing pinned-engine lifecycle acceptance | Prior decision/evidence preserved; bounded d2 closes, full W3 and grades unchanged |
| 2026-09-08 | Recorded W3.2 fixture launch prototype, offline checks, engine failures and operator cleanup exception | Prior decision/evidence preserved; engine workflow remains unqualified, no status/maturity promotion |
| 2026-09-08 | Recorded W3.2 identity correction and seven accepted bounded launch observations | Prior wording and failed evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d2 failed launch probes, source-explained identity gate and proposed lifecycle | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d1 stopped ownership, acknowledgement recovery and explicit limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2b2 stop coordination, permanent workspace blocking and failure evidence | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2b1 key-revocation ordering fix, fault evidence and remaining recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2a versioned terminal capacity, compatibility and recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Superseded: embeddings and hashes reclassified as prompt-class data; retroactive pin suppression; keyed hashes; no default exception | "Raw prompts are not stored by default; embeddings and instruction hashes are suppressed for private/secret turns." |
| 2026-09-03 | Amended (proposed, external review): field-level data inventory; locating fields are prompt-class | "Raw prompts are never stored in the ledger; prompt-derived artefacts — embeddings, instruction hashes and any retrieval key computed from prompt content — are classified as prompt-class data and are stored only under the same access, retention and erasure controls as the prompt itself would be, and are not produced at all for private, secret or privacy-pinned turns, including turns earlier in a session that is later pinned." |
