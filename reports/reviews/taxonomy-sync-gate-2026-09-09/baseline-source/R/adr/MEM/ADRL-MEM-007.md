# ADRL-MEM-007 — Projections are rebuildable and versioned

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested, conditional on a rebuild-equivalence test existing; if cross-process detection relies on file mtime it is D1 |
| Review verdict | AMEND |
| Tenets | 8 |
| Related decisions | MEM-001, MEM-005, MEM-006, MEM-008, LRN-004, LRN-005, OPS-001 |
| Open questions | — |

## Context-graph planning note, 2026-09-08

A context graph is proposed as a versioned derived view of decision experience, authorized task context and reviewed improvements. The candidate extends projection identity to the relevant source/context versions and distinguishes when a fact applied from when it became known. Its rebuild, stale-state, temporal and erasure behavior must be qualified. This is a proposed application, not a new provider, implemented graph or maturity claim. See the [proposal](../../design/adrl-context-graph-memory-proposal-2026-09-08.md) and [product roadmap](../../reports/adrl-product-roadmap-2026-09-08.md). Current decision wording, status and maturity are unchanged.

## Decision

Derived retrieval indexes are rebuildable projections of the ledger, each stamped with the ledger high-water mark, the embedding-model version and the projection-code version it was built from; a projection is invalid — and retrieval abstains — when any stamp mismatches, and cross-process ledger changes are detected through the database connection (`PRAGMA data_version` or an equivalent provider primitive), never by file timestamps.

1. **Identity of a projection = (ledger position, embedding model, projection code).** Changing the local embedding model or the projection code invalidates every existing index; an incremental refresh must produce a byte-equivalent (or metric-equivalent, within a declared tolerance) result to a full rebuild, and a test asserts this.
2. **Stale is a state, not an error.** When the ledger has advanced past the projection's high-water mark, the projection is `stale`; MEM-008 retrieval may serve stale results only if it labels them so, and never for evidence.
3. **Shredded content leaves projections.** An erasure event (MEM-001/MEM-010) forces a rebuild or targeted removal of the affected vectors; a projection that still holds a shredded embedding is invalid.
4. **Rebuild has a budget.** Full rebuild time at the current ledger size is recorded in the EVL pack; when it exceeds a declared bound, snapshotting is introduced as an OPS decision.

## Context and rationale

Anything derived for retrieval can be thrown away and rebuilt from the ledger. That is what makes the ledger the source of truth and the NumPy index disposable: if the embedding model changes, the ledger does not. The second half of the original — "detect cross-process database changes" — exists because a benchmark run and the live router can both touch `router-memory.db`, and an index that does not know the ledger moved will happily retrieve against yesterday.

The amendment makes the projection's identity explicit. "Rebuildable" is only meaningful if you can say what a rebuild is a rebuild *of*: which ledger position, which embedding model, which projection code. Without those stamps, a projection can be simultaneously "rebuilt" and wrong (built by old code, or with the old encoder), and the LRN-004 leakage rule cannot be enforced for retrieval features because nobody can say which rows the index contained at decision time. The amendment also pins the detection mechanism: SQLite's WAL keeps recent commits in the `-wal` file, so the main database file's mtime is not a reliable change signal; the engine provides a per-connection counter for exactly this purpose.

## Adversarial review (2026-09-02)

### Steelman
CQRS-style rebuildable projections are the standard companion to an append-only log and remove a whole class of "the index and the truth disagree" bugs. Detecting cross-process changes is a real, specific need in this deployment (benchmarks and live router share a file) and the decision names it rather than assuming a single writer.

### Attacks
1. **"Rebuildable" without identity is unfalsifiable.** Nothing says what a projection records about its own construction. If the local embedding model is upgraded (the register says embeddings are via a local model + NumPy), old vectors and new vectors will coexist in one index with different geometry; retrieval silently degrades. The decision must bind projections to the embedding-model version and to the ledger position.
2. **Detection mechanism unspecified — and the obvious one is wrong.** In WAL mode recent commits live in `router-memory.db-wal`; polling the main file's mtime misses them. SQLite provides `PRAGMA data_version`, which changes when *another* connection (including another process) commits — but it is per-connection, so the check must be made on the same long-lived connection, which a facade that opens connections per call will not have. The decision should say which primitive is used.
3. **Retrieval projections are a leakage vector for LRN-004.** A kNN index built from the whole ledger contains outcomes of sessions that happened *after* the decision being trained on. Offline evaluation of retrieval-advised routing (MEM-008) on historical decisions will then use neighbours from the future — a textbook leak that makes offline numbers look good. Without a ledger high-water mark on the projection, a time-respecting rebuild ("index as of decision time") is impossible to construct.
4. **Rebuild cost and no snapshots.** Trivial today; the decision is written for the multi-worker future and says nothing about a bound. Event-sourcing guidance is explicit that replay cost must be managed with snapshots once streams grow.
5. **Erasure is not propagated.** MEM-005 (replacement) and MEM-010 shred embeddings; MEM-001 makes erasure a logged event. A projection built before the erasure still holds the vector in the NumPy array on disk or in memory. Rebuildable does not mean rebuilt; the decision must make erasure a forced invalidation.
6. **Stale projections and shadow retrieval.** MEM-008 runs retrieval in shadow against real traffic. If the projection is stale relative to the ledger, the shadow measurement is of a different system than the one that would serve. Staleness has to be a visible state in the shadow log or the D3 claim for MEM-008 rests on an unmeasured variable.

### Evidence
- SQLite, "PRAGMA data_version" (official pragma docs) — value changes between two calls on the same connection iff another connection (same or different process) committed; unchanged for the connection's own commits; only meaningful within one connection; attack 2 — https://www.sqlite.org/pragma.html
- SQLite, "Write-Ahead Logging" — commits are appended to the WAL file and only reach the main database at checkpoint; checkpoints can be starved by long readers; implies mtime of the main file is not a change signal (attack 2) — https://www.sqlite.org/wal.html
- Microsoft Azure Architecture Center, "Event Sourcing pattern" — projections are eventually consistent; replay cost grows with stream length and snapshots are the standard mitigation; erasure/crypto-shredding requires projection rebuilds; attacks 4, 5 — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- S. Kaufman, S. Rosset, C. Perlich, O. Stitelman, "Leakage in Data Mining: Formulation, Detection, and Avoidance" (ACM TKDD 2012) — "no-time-machine" legitimacy: features must be observable at prediction time; recommends learn-predict separation with legitimacy tagging; a retrieval index containing future rows violates it (attack 3) — https://dl.acm.org/doi/10.1145/2382577.2382579
- M. Rook, "Forget me please? Event sourcing and the GDPR" (2017) — none of the erasure strategies update projections automatically; projections must be rebuilt (attack 5) — https://www.michielrook.nl/2017/11/forget-me-please-event-sourcing-gdpr/

### Verdict
**AMEND.** Attacks 1–3 and 5 land: a projection without identity stamps cannot be shown to be a correct rebuild, the detection mechanism is unstated and the naive one is wrong under WAL, the index is a leakage path for LRN-004, and erasure does not reach it. Attack 4 is a budget follow-up. Attack 6 is addressed by making staleness a labelled state. The decision's intent — projections are disposable, the ledger is truth — is fully preserved.

## Amendments applied

- Added identity stamps (ledger high-water mark, embedding-model version, projection-code version) and invalidation on mismatch; retrieval abstains on invalid projection (clause 1).
- Specified detection via the database connection (`PRAGMA data_version` or provider equivalent), never file timestamps.
- Added `stale` as a labelled state; stale results never count as evidence (clause 2).
- Added erasure-forced invalidation (clause 3) and a rebuild-time budget (clause 4).

## Follow-ups

- [ ] Golden test: full rebuild vs incremental refresh of the NumPy index produce equal vectors (or cosine distance < declared tolerance) for the same ledger position.
- [ ] Golden test: write to the ledger from a second process; assert the facade detects it via `data_version` on its long-lived connection and marks the projection `stale`.
- [ ] Implement "index as of ledger position N" rebuild and use it for any offline evaluation of retrieval-advised routing (LRN-004 follow-up).
- [ ] Golden test: erasure event → affected vectors absent from the projection after refresh; projection built before erasure is reported invalid.
- [ ] Record full-rebuild wall time in the EVL pack; declare the bound that triggers snapshotting.
- [ ] Verify `memory_sqlite.py` keeps one long-lived connection per process for `data_version` to be meaningful; if it opens per call, use a different primitive (e.g. a ledger sequence counter row).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: projections carry identity stamps, staleness is a state, detection mechanism specified, erasure propagates | "Derived retrieval indexes are rebuildable projections and detect cross-process database changes." |
