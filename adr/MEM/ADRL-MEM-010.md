# ADRL-MEM-010 — Retention and erasure of ledger and derived artefacts

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Proposed 2026-09-02 (new, from adversarial review) |
| Maturity | D0 Design, review recommends D0 Design — nothing exists |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8 |
| Related decisions | MEM-001, MEM-005, MEM-007, SAF-002, SAF-003, OPS-001, EVL-009 |
| Open questions | Q5 |

## Decision

Every class of content in transaction memory has a declared retention period and an erasure procedure: prompt-class artefacts (embeddings, keyed instruction hashes, retrieval keys) are stored under per-session keys and erased by crypto-shredding; the `route_id` skeleton (timestamps, rung, failure type, event types, costs) is retained for evidence without prompt-derived content; erasure is triggered by retention expiry, a late privacy pin (MEM-005), or an explicit security/data-subject request, is itself an appended event, and forces invalidation of every projection that held the shredded content.

1. **Two storage classes.** *Evidence skeleton* — no prompt content, retained for the evidence horizon EVL needs (proposed: 24 months, reviewed annually). *Prompt-class artefacts* — retained no longer than the shorter of the retrieval usefulness horizon (proposed: 90 days) and the repository's own data-classification policy.
2. **Crypto-shredding by session.** Prompt-class rows are encrypted under a per-session key held in a local keystore; erasing a session is deleting its key and appending an `erased` event naming the session and reason. The ledger rows remain, unreadable.
3. **Erasure reaches projections.** An `erased` event invalidates any projection whose high-water mark predates it (MEM-007 clause 3); the NumPy index is rebuilt without the affected vectors before retrieval resumes.
4. **Erasure is auditable, not silent.** Counts of erased sessions and their reasons are reported in the EVL pack; an erasure that removes evidence from an evaluation window is an EVL-009 blocker for that window, never averaged away.

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

## Amendments applied

New decision — no prior text.

## Follow-ups

- [ ] Add per-session key generation and encryption of `embeddings` rows and keyed-hash columns in `memory_sqlite.py`; keystore location documented in OPS.
- [ ] Implement `erased` event type; golden test: erase session → key gone, rows unreadable, projection invalidated and rebuilt, EVL window flagged.
- [ ] Wire SAF-002 pin to trigger erasure of the session's pre-pin prompt-class rows (MEM-005 clause 2).
- [ ] Measure neighbour-age distribution in shadow retrieval and time-to-close in MEM-002 to replace the provisional 90-day / 24-month figures.
- [ ] Confirm with the company data governance which classification the embedding store falls under and whether the 24-month evidence horizon is permissible.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-02 | Proposed (adversarial review) | — |
