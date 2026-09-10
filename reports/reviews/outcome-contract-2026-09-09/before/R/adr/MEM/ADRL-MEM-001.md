# ADRL-MEM-001 — Append-only ledger keyed by route_id

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (the append discipline is tested; the amended clauses on schema versioning, idempotency and erasure are D0 until a test exists) |
| Review verdict | AMEND |
| Tenets | 8, 9 |
| Related decisions | MEM-002, MEM-003, MEM-005, MEM-006, MEM-007, MEM-009, MEM-010 (proposed), CAS-006, OPS-001, OPS-006, EVL-009 |
| Open questions | Q6 |

## Lab A.1 implementation evidence, 2026-09-08

The diagnostic reads actual route IDs and append-only decision/request/served events from disposable synthetic ledgers, keeping initial choice separate from continuation dispatch. A separate experiment manifest and append-only JSONL journal retain planned and interrupted cells. They are synthetic-only exports, not a new production ledger schema or extension of the encrypted verifier archive. No outcome/training label is fabricated, no developer ledger is touched and no idempotent resume service is claimed.

[Report](../../reports/adrl-lab-first-run-2026-09-08.md), [runner](../../../adrl-core/tools/run_routing_lab.py), [tests](../../../adrl-core/tests/unit/test_routing_lab.py), [run evidence](../../reports/research/routing-lab-2026-09-08/run-2/results.json), [engineering checks](../../reports/research/routing-lab-2026-09-08/engineering-checks.json), [validation](../../reports/research/routing-lab-2026-09-08/validation.json), [follow-on scope](../../reports/waves/lab-a-routing-experiment.md). All eleven checks pass: 894 tests passed, eight engine cases skipped without new authorization, 320 stable inputs. Existing 316 inputs are unchanged. Decision wording, architectural status and formal maturity are unchanged; no whole-decision promotion or real-task learning evidence.

## Decision

Transaction memory is an append-only decision/outcome/event ledger keyed by an immutable `route_id` minted at decision time; rows are never updated in place, every event carries a per-`route_id` monotonic sequence number, an idempotency key and a schema version, and the only permitted mutation of history is erasure by an explicit, logged retention or crypto-shredding action (MEM-010).

1. **Append-only, not append-oriented.** `decisions` rows are written once. All later knowledge (outcomes, verification, counterfactuals, label corrections) is a new `outcome_events` row referencing the `route_id`; a correction is an event that supersedes an earlier event by sequence number, never an `UPDATE`.
2. **Every event is versioned and idempotent.** Each event carries `schema_version` and an idempotency key (`route_id`, `event_type`, `producer`, `producer_seq`); a duplicate write is a no-op, and readers must tolerate unknown fields and upcast old versions.
3. **Erasure is the one exception, and it is itself an event.** Deleting or shredding content for retention or a data-subject request is performed by a logged erasure event that leaves the `route_id` skeleton (timestamps, rung, failure type, event types) intact so evidence counts remain auditable.

## Product service evidence, 2026-09-07

Migration 0003 adds immutable bindings, encrypted public observations and a reference-only timeline index. Producer/event-UUID idempotency returns the original acknowledgement on identical retries; changed content or reused producer sequences conflict. Gaps and late delivery are explicit. Internal outcome idempotency and historical rows are unchanged; public observations do not automatically become verified labels.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

### Product service application: public observations

Public observations use a separate append-only intake with authenticated producer/event-ID
idempotency. Identical retries return their original acknowledgement; changed content under the
same identity is a conflict. Producer sequence conflicts are explicit, and gaps/late delivery
remain visible. This does not replace the internal route/event/producer/sequence contract.
Intake payloads use the existing per-session encryption and erasure boundary. A timeline can
index original decisions, internal events and public observations without promoting a harness
report into a verified outcome or copying protected payloads into plaintext. Its sequence denotes
index order, not proof of tool execution order. Implementation and validation are linked in the product service evidence above.

## Earlier foundation evidence, 2026-09-07

New decision context can record the protocol profile and harness adapter IDs and versions,
alongside whether the request path is covered by the profile. These are additive fields in the
existing context JSON; this package makes no SQL schema migration or rewrite of ledger history.
The append discipline and internal idempotency key in the decision above remain unchanged.

The public API preview also defines typed event envelopes, including distinct reported task
closure and verification evidence shapes. The corresponding ingestion endpoints return 501:
producer authorization, durable ingestion and mapping public event UUIDs to the ledger's
idempotency contract are still required. Validating a schema does not establish trusted evidence.
See the [implementation record](../../reports/adrl-product-foundation-implementation-2026-09-07.md)
for the tested metadata and contract scope.

## Live observation pilot, 2026-09-07

Migration 0004 adds immutable integration_mode to product sessions; earlier bindings retain gateway semantics. Existing preview-2 encrypted event envelopes remain readable/deliverable without rewriting history. One live observation run durably recorded 18 individually reconciled tool events, with zero pending outbox entries after flush. No routing decision or trusted learning label was created. The inventory scanner now detects added migration columns; all 242 fields are classified.

The [pilot report](../../reports/adrl-live-observation-pilot-2026-09-07.md) links the applied 15-file package, 511 passing tests,
all required checks, reviewed outcomes and remaining blockers. Architectural status is unchanged;
this evidence does not promote the full decision to D3 or D4. Earlier dated sections preserve
their original implementation and planning scope.

## Session verification implementation, 2026-09-07

Migration 0005 adds product_verifications with separate encrypted started/finished rows, keyed to the existing product session rather than a fabricated route. A reference-only timeline projection includes the receipts without changing the prior observations. The copied pilot timeline retained all 18 tool events and added four records for two verifier jobs. Re-execution creates a new job; interrupted jobs can retain only a started receipt. No existing route, internal outcome or event is rewritten.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Offline verifier improvement implementation, 2026-09-07

Migration 0006 adds improvement_records: append-only encrypted started, trial and finished events. A separate namespaced experiment identity reuses key storage without creating a harness session. The final run retained 30 records: one start, 28 trials and one assessment. Reopening through a separate CLI process returned the same history. There were zero product sessions/events/verifications, routing decisions or outcome events in this experiment archive.

Interrupted runs can retain only a start or partial trials; retries start a new experiment rather than rewriting prior results. No resume/idempotent retry protocol is implemented, and a failed initial append can leave an orphan key. Local operator access is not remote tamper-proof attestation.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## W3.1 retained operator captures, 2026-09-08

Scoped application: retained operator captures append once per bound session/capture identity, with a distinct unique attempt identity. Migration 0007 commits the whole encrypted capture in one transaction. Identical retries preserve the original capture time; changed identity or content conflicts. Failed transactions leave no complete capture, and a lost acknowledgement can be reconciled through the stable ID. No historical record or route is fabricated or rewritten. Schema-6 verification evidence still decrypts after migration.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

Migration 0008 adds encrypted append-only operator attempt events with per-attempt sequence and per-session request identity. Identical requests return their original records even after later phases, while changed commands conflict. A start retry preserves its original initial manifest rather than reassigning the starting point to later edits. Failed transactions leave no partial event; lost acknowledgements reconcile by the same ID. Existing schema-7 captures and older verification receipts remain readable. No route or outcome is fabricated or rewritten.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b2a reserved terminal capacity, 2026-09-08

W3.2b2a atomically appends a v2 attempt start and a terminal-capacity grant. Every later append accounts for stored encrypted bytes plus pending grants. Terminal consumption is inferred from the appended terminal event; the grant is not rewritten or deleted. Duplicate acknowledgements do not charge twice, and injected transaction failures leave no partial grant or consumption. Schema 9 preserves v1 ciphertext/nonces and adds no mutable counter. This is logical quota accounting, not disk allocation or an externally anchored tamper guarantee.

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

W3.2b2b1 preserves the append-only key audit while adding a filesystem revocation marker before key mutation. A failed audit remains an error, but no longer permits the tested restored-key read or same-session recreation. The file lock is released before waiting on the ledger writer; the audit-lock ordering fixture exercises a real queued key read. Filesystem revocation and SQL audit are separate resources, not an atomic cross-store transaction or an external tamper anchor. Repeated shred requests may append another audit without removing revocation.

See the [plain-language report](../../reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md),
[checks and pre-change probe](../../reports/research/adrl-w3-2b2b1-key-revocation-2026-09-08.json),
[keystore](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/keystore.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_key_revocation.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/key-revocation.md).
All 724 tests and eleven checks pass for the recorded Darwin build. Prior wording,
architectural status and maturity fields remain unchanged. Independent security review,
process/erasure/release coordination and full W3 remain open.

## W3.2b2b2 process coordination, 2026-09-08

Schema 10 adds append-only execution fences. Admission binds four keyed identifiers, host HMAC key ID, policy JSON and timestamp to an existing intact v2 start and its terminal grant. No row is updated/deleted to release a workspace. Old schema-9 ciphertext and grants remain byte-identical in migration tests. Lost admission acknowledgement never authorizes replay; untrusted database mutation or whole-state rollback is not qualified.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2d1 stopped resource ownership, 2026-09-08

Schema 11 appends a five-phase authenticated resource metadata history and links it to the permanent execution fence. Fence and intent commit atomically; create/remove issue events precede daemon mutation, and failure leaves visible pending state. No UPDATE/DELETE path, terminal outcome, capture association or fence release is added. Logical event bounds do not preallocate physical storage. Interior corruption/gaps are detected; valid-prefix/suffix or whole-database/key rollback still lacks an independent anchor.

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

The proposed active lifecycle adds separate append-only claim/seal/stop/discard evidence without reinterpreting stopped-resource history. A permanent launch-denial marker is proposed to prevent replay after ledger-only prefix rollback; it is not implemented and whole-storage/key rollback remains unqualified. Two research cleanup failures retained failed records rather than being converted into successful outcomes. No runtime schema, ledger producer or existing digest changed.

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

New evidence consists of private synthetic inspections, exact resource receipts, profile/digest references and separately recorded case/cleanup outcomes. These are local research artifacts, not new product ledger fields. The future execution history must authenticate its projection against the original bound event. Runtime schema 11 and append-only behavior are unchanged; ledger-only rollback denial via a permanent marker is still planned.

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

Schema 12 adds a separately authenticated append-only launch history without reinterpreting old stopped records, ciphertext or grants. Bound-event MAC, engine/projection/fixture HMACs, immutable fields and phase order are verified. Permanent filesystem denial prevents another launch after ledger-only rollback when the marker survives. Whole-store/marker/key rollback and root replacement remain unqualified. Logical metadata bounds do not preallocate disk.

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

Execution v2 adds one inventoried policy field to authenticated launch payloads; schema 12 remains. V1 histories preserve their original MAC/profile meaning and bytes, including records without the new field, and recovery uses the authenticated historical policy. No row rewrite, ledger diagnostic field, fence release or whole-storage rollback claim is added.

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

Each routing decision gets a permanent name at the moment it is made and everything learned afterwards is appended against that name. The reason is not tidiness: if outcomes could overwrite decisions, a later optimistic write (a retry that "succeeded", a verifier that ran against a different working tree) could quietly rewrite what the router actually saw and did, and the evidence in EVL would then be a story rather than a record. The ledger is the thing the readiness claims stand on.

The amendment closes three gaps that the original one-liner left open. "Append-oriented" admitted in-place edits by omission, and the rest of MEM (002, 003, 009) only works if in-place edits are impossible. Event-sourced stores are known to fail in practice on schema evolution, duplicate delivery and erasure rather than on the append rule itself, so those three are now part of the decision. Erasure is called out explicitly because an immutable ledger that holds prompt-derived artefacts (MEM-005) has no lawful way to forget without it, and "we cannot delete it" is not an acceptable answer for a payments company's source code and developer data.

## Adversarial review (2026-09-02)

### Steelman
An immutable, route-keyed event log is the standard answer to "can the record be trusted": it makes every later claim reproducible from primary events, makes label corrections auditable rather than silent, and lets MEM-007 treat everything derived as a throw-away projection. It is also the cheapest possible schema for a single-process SQLite deployment. Tenet 8 ("every decision is tied to an immutable `route_id`") is essentially this decision restated.

### Attacks
1. **"Append-oriented" is not "append-only".** The original wording permits in-place updates as long as they are not the norm. MEM-002's lifecycle (`pending` → `closed_turn` → `closed_final`) is exactly the kind of state that gets implemented as `UPDATE outcomes SET status=...`, and MEM-003's "enrich without overwriting" is unenforceable if the storage layer allows overwrites at all. The code map lists `decisions`, `outcomes`, `outcome_events` and `embeddings` tables; the existence of a separate `outcomes` table alongside `outcome_events` suggests a mutable current-state row exists next to the log. The decision text must forbid the mutable row from being a source of truth.
2. **No schema-evolution or duplicate-delivery rule.** The failure-type enum has already drifted (four in the decision text, six in `outcomes.py` — MEM-004). An append-only ledger with no `schema_version` on events cannot be replayed once the enum, the verifier output shape, or the SDLC intent taxonomy changes. Likewise the proxy retries and transport fallbacks (CAS-006) mean the same outcome can be reported twice; without an idempotency key the ledger double-counts exactly the events that matter most for cost and reliability.
3. **Immutability collides with erasure and retention.** The ledger will hold instruction hashes and embeddings of developer prompts (MEM-005), which the literature shows are prompt-equivalent. There is no decision anywhere in MEM on retention periods or on how a data-subject or security request ("that session contained a production credential — remove it") is honoured. Event-sourcing practice has three known answers (store PII outside the log by reference, crypto-shred with per-subject keys, rewrite the stream) and each requires projection rebuilds. The register is silent on all three.
4. **Rebuild cost is unbounded and untested.** MEM-007 promises every index is rebuildable from the ledger. Nothing says how long a full replay takes or whether snapshots exist. At current volume it is trivial; the decision is being made for the multi-worker future (OPS-001), where the same promise needs a bound.
5. **The `route_id` is only immutable if it is minted before anything can fail.** If memory is unavailable (MEM-006's fail-safe path) the decision is "unlogged" — the `route_id` either does not exist or exists only in the proxy's process memory. Later outcome events for that turn then have nothing to attach to and are either dropped or orphaned. The ledger's completeness therefore depends on MEM-006, and the decision does not say so.

### Evidence
- Microsoft Azure Architecture Center, "Event Sourcing pattern" (Microsoft Learn) — lists the standard issues with immutable event stores: events must be versioned/upcast rather than edited, delivery is at-least-once so handlers must be idempotent, replay cost needs snapshots, and personal data must be kept outside the stream or crypto-shredded for GDPR; bears on attacks 2, 3 and 4 — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- M. Rook, "Forget me please? Event sourcing and the GDPR" (blog, 2017) — walks through crypto-shredding, direct deletion and stream rewriting for erasure in an append-only store, and notes that none of them updates projections automatically; bears on attack 3 — https://www.michielrook.nl/2017/11/forget-me-please-event-sourcing-gdpr/
- OpenLineage, "Object Model" (spec docs) — a run/job/dataset lineage standard where every state update carries the same `runId` (UUIDv7 recommended) and events are correlated by id rather than time, with START/COMPLETE/FAIL/ABORT states; a useful external analogue for `route_id` plus event types — https://openlineage.io/docs/spec/object-model/
- W3C, "PROV-DM: The PROV Data Model" (W3C Recommendation, 2013) — entities, activities and agents with explicit `wasGeneratedBy` / `wasDerivedFrom` relations; derivation must be asserted, not inferred from a chain of usage; supports keying all evidence to an explicit identifier (also MEM-009) — https://www.w3.org/TR/prov-dm/
- SQLite, "Write-Ahead Logging" (official docs) — one writer at a time, all processes must be on the same host, and a long-running reader can starve checkpoints so the WAL grows without bound; bears on attack 4 and on the OPS-001 future — https://www.sqlite.org/wal.html

### Verdict
**AMEND.** Attacks 1–3 land: the decision's spirit is right and Tenet 8 depends on it, but as written it neither forbids in-place mutation nor says anything about the three ways append-only stores actually break in production (schema drift, duplicates, erasure). Attack 4 is a follow-up rather than a text change at current scale. Attack 5 is real but belongs to MEM-006, which is amended to make the unlogged path observable. The retention/erasure gap is large enough to warrant its own decision (MEM-010, proposed) rather than a sub-clause here; this decision only establishes that erasure is the sole permitted mutation and that it is itself logged.

## Amendments applied

- "append-oriented" → "append-only"; added that `route_id` is minted at decision time and rows are never updated in place.
- Added clause 1 making corrections supersession events, and stating that the mutable `outcomes` current-state row (if retained) is a projection, not a source of truth.
- Added clause 2: per-event `schema_version`, idempotency key and tolerant/upcasting readers.
- Added clause 3: erasure as the single permitted mutation, performed by a logged event that preserves the `route_id` skeleton; points to MEM-010.

## Follow-ups

- [ ] Golden test: attempt `UPDATE`/`DELETE` on `decisions` and `outcome_events` through the provider port and assert it is rejected (or that the port exposes no such method); confirm the `outcomes` table is written only by a projection routine.
- [ ] Add `schema_version` and idempotency key columns to `outcome_events`; test that replaying the same outcome twice (simulating a proxy retry) produces one event.
- [ ] Write an upcaster for the four→six failure-type change and a test that a v1 event with `failure_type` from the old set replays correctly.
- [ ] Measure full-replay time of all projections at 10×, 100× and 1000× current ledger size and record the numbers in the EVL evidence pack; decide whether snapshots are needed before OPS-001.
- [ ] Draft ADRL-MEM-010 (retention and erasure) — see bucket README.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Added scoped Lab A.1 synthetic workbench evidence and limitations | Prior decision wording, status, maturity and dated evidence retained |
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
| 2026-09-07 | Recorded applied observation mode and the first live subscription pilot | Decision policy and status unchanged; prior evidence was offline or synthetic, with observation-only launch still planned |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-09-07 | Recorded additive profile/adapter context and the public event schema preview; ingestion and idempotency mapping remain pending | Decision text unchanged; no product API preview evidence previously recorded |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: append-only made strict; added schema versioning, idempotency and logged-erasure clauses | "Transaction memory is an append-oriented decision/outcome/event ledger keyed by immutable `route_id`." |
