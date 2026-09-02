# ADRL-MEM-006 — Memory facade, fail-safe but never silent

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested for the facade/NullProvider path; the "SQLite is not a semantic dependency" claim is D1 at best because sticky session state lives outside the facade in a process-local dict |
| Review verdict | AMEND |
| Tenets | 2, 8, 9 |
| Related decisions | MEM-001, MEM-007, MEM-009, CAS-005, CAS-006, SAF-004, OPS-001, OPS-006, EVL-009 |
| Open questions | Q7 |

## Decision

The router uses a fail-safe memory facade behind a provider port; SQLite is the current local provider, not a semantic dependency; when the provider is unavailable the router continues on the deterministic safe policy with retrieval disabled, and every unlogged decision is counted, surfaced as a degraded-mode telemetry event and excluded from evidence, so that memory loss can never be mistaken for a clean corpus.

1. **Degraded mode is observable.** The facade emits `memory_degraded` with a reason on every decision it cannot persist; the count is an OPS health signal and an EVL-009 blocker when non-zero over an evaluation window.
2. **Degraded decisions do not advise.** With no provider, MEM-008 retrieval and any learned advice are off; the deterministic policy decides alone. This is the same posture as LRN-006 abstention.
3. **All routing state that must survive a decision goes through the port.** Sticky episode state (CAS-005/006) and session-to-route tracking are provider-backed or explicitly declared process-local with a documented single-process constraint; a semantic dependency on process memory is a dependency, and it is the one that blocks OPS-001.
4. **Provider contract is concurrency-explicit.** The port declares its concurrency guarantees (single writer, WAL, busy timeout, same-host only for SQLite) so that a multi-worker deployment fails at configuration time, not with `database is locked` at runtime.

## Context and rationale

SQLite is a detail and the router survives its absence. Storage is behind a facade with a provider port; if memory is unavailable the router keeps routing rather than failing the developer's turn. That is the right priority order — a proxy that blocks coding because its evidence store is locked has confused the product with its telemetry.

The amendment fixes what "degraded, unlogged" costs. An unlogged decision is a hole in the ledger that MEM-001 promised was complete; if the hole is silent, EVL's evidence pack is computed over a corpus that quietly lost exactly the turns during which the system was under stress. The fix is not to block routing but to count and surface. The second amendment addresses the register's own worry: the facade isolates SQLite, but the code reality is that session-to-route tracking is a Python dict. That is a process-local semantic dependency sitting beside the facade, and it — not SQLite — is what makes the router single-process today.

## Adversarial review (2026-09-02)

### Steelman
A provider port with a NullProvider is textbook hexagonal design; it lets tests run without a database, lets the proxy degrade instead of fail, and keeps the door open for a server-backed store when OPS-001 arrives. The register is candid that this is a local-first, single-user deployment, and SQLite is the correct choice for it.

### Attacks
1. **"Degraded, unlogged" is a silent evidence hole.** The ledger's value (MEM-001) is completeness; EVL-009 says blockers are never averaged away. A NullProvider that swallows writes without a counter makes the corpus look cleaner exactly when the system misbehaves (disk full, lock contention, concurrent benchmark run per MEM-007). Nothing in the decision says degraded decisions are counted, surfaced or excluded.
2. **The real semantic dependency is not SQLite; it is process memory.** The register states session-to-route tracking is a Python dict and OPS-001 names a multi-worker future. Sticky escalation (CAS-005) and served-rung recording (CAS-006) depend on that dict. The facade isolating SQLite is true and beside the point: two workers would each hold their own dict, and the same session could be escalated in one and not the other — the split-brain the register worries about in Q3 for subagents, reproduced for plain sessions.
3. **SQLite's concurrency model is a semantic constraint, not a detail.** One writer at a time, same-host only (WAL needs shared memory), readers can starve checkpoints, and a deferred transaction that upgrades to a write fails immediately with `database is locked` regardless of `busy_timeout`. A benchmark run and the live router writing concurrently (the MEM-007 scenario) will hit this. Calling SQLite "not a semantic dependency" is only true if the port declares these constraints so a different provider can honour or relax them.
4. **Write-behind or write-through?** The decision is silent on whether the decision row is persisted before or after the response is served. Persisting after means a crash between serve and write loses the `route_id` the harness already received (and any later outcome event orphans); persisting before adds latency to every turn. Either is defensible; not choosing is not.
5. **Fail-safe collides with privacy pins.** If the facade is down and SAF-002's pin state is provider-backed, is the session still pinned? The decision says routing "continues"; SAF-004 says a pinned session must never reach cloud. Degraded mode must default to the most restrictive known state, and the decision does not say so. (If pin state is in the process dict, attack 2 applies instead.)

### Evidence
- SQLite, "Write-Ahead Logging" (official docs) — readers and writers do not block each other but there is only one writer; all processes must be on the same host (shared memory); a long-running reader prevents checkpoints and the WAL can grow without bound; attack 3 — https://www.sqlite.org/wal.html
- tenthousandmeters.com, "SQLite concurrent writes and 'database is locked' errors" (engineering blog) — `busy_timeout` does not help when a deferred read transaction upgrades to a write while another writer holds the lock (immediate `SQLITE_BUSY`); `BEGIN IMMEDIATE` avoids the upgrade failure; application-level locking outperforms SQLite's file locking under many writers; attack 3 — https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/
- SQLite, "PRAGMA data_version" (official pragma docs) — change detection is per-connection and covers other processes; cited here because it is the cheapest way for the facade to know another writer touched the file (also MEM-007) — https://www.sqlite.org/pragma.html
- D. Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NIPS 2015) — undeclared consumers, hidden feedback loops and configuration debt; an unobservable degraded mode is an undeclared consumer of the evidence corpus (attack 1) — https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- E. Breck et al., "The ML Test Score: A Rubric for ML Production Readiness" (IEEE BigData 2017) — "training and serving are not skewed" and "data invariants hold for inputs" as monitoring tests; a silent gap in logged decisions is a training/serving skew source (attack 1) — https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/

### Verdict
**AMEND.** Attacks 1 and 2 land squarely: the decision's fail-safe path is invisible to evidence, and the thing it claims not to depend on (SQLite) is not the thing it actually depends on (process memory). Attack 3 is answered by making the port's concurrency contract explicit rather than by changing providers now. Attack 4 is a follow-up decision that must be recorded. Attack 5 is answered by a rationale note and a golden test; the decision text's "deterministic safe policy" already implies most-restrictive-known, but the test must exist. The facade design stands; the "not a semantic dependency" claim is downgraded to D1 until the dict is behind the port.

## Amendments applied

- Added: degraded mode continues on the deterministic safe policy with retrieval disabled; every unlogged decision is counted, surfaced as telemetry and excluded from evidence (clause 1, 2).
- Added clause 3: routing state that must survive a decision (sticky episode state, session-to-route map) goes through the port or is explicitly declared process-local with a single-process constraint.
- Added clause 4: the provider port declares its concurrency guarantees; misconfiguration fails at startup.

## Follow-ups

- [ ] Golden test: NullProvider active → decision served, `memory_degraded` counter incremented, telemetry event emitted, and `learning_readiness.py` reports the window as blocked (EVL-009).
- [ ] Golden test: provider unavailable on a pinned session → route stays local-only (SAF-004); if pin state is provider-backed, degraded mode must treat "unknown" as pinned.
- [ ] Move session-to-route and sticky episode state behind `MemoryProvider` (or a separate `StateProvider` port); document the single-process constraint in OPS-001 until done.
- [ ] Set `PRAGMA journal_mode=WAL`, `busy_timeout`, and use `BEGIN IMMEDIATE` for all write transactions in `memory_sqlite.py`; fault test with a concurrent benchmark writer.
- [ ] Record the write-through vs write-behind choice for the decision row (recommend write-through for `decisions`, write-behind for `outcome_events`) and test crash-between-serve-and-write.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: degraded mode made observable and excluded from evidence; process-local state declared a dependency; provider concurrency contract required | "The router uses a fail-safe memory facade and provider port; SQLite is the current local provider, not a semantic dependency." |
