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

## Decision

Transaction memory is an append-only decision/outcome/event ledger keyed by an immutable `route_id` minted at decision time; rows are never updated in place, every event carries a per-`route_id` monotonic sequence number, an idempotency key and a schema version, and the only permitted mutation of history is erasure by an explicit, logged retention or crypto-shredding action (MEM-010).

1. **Append-only, not append-oriented.** `decisions` rows are written once. All later knowledge (outcomes, verification, counterfactuals, label corrections) is a new `outcome_events` row referencing the `route_id`; a correction is an event that supersedes an earlier event by sequence number, never an `UPDATE`.
2. **Every event is versioned and idempotent.** Each event carries `schema_version` and an idempotency key (`route_id`, `event_type`, `producer`, `producer_seq`); a duplicate write is a no-op, and readers must tolerate unknown fields and upcast old versions.
3. **Erasure is the one exception, and it is itself an event.** Deleting or shredding content for retention or a data-subject request is performed by a logged erasure event that leaves the `route_id` skeleton (timestamps, rung, failure type, event types) intact so evidence counts remain auditable.

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
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: append-only made strict; added schema versioning, idempotency and logged-erasure clauses | "Transaction memory is an append-oriented decision/outcome/event ledger keyed by immutable `route_id`." |
