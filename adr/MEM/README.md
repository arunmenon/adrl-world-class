# MEM — Memory, Evidence, Label Integrity

**Core question:** What happened, and can we trust the record?
**Owns / does not own:** Owns the decision/outcome ledger, outcome lifecycle, verification provenance, label typing, prompt-derived artefact handling, retrieval projections and counterfactual ownership. Does not own choosing a route (RTG/CAS), training a model (LRN), or the readiness gates that consume its evidence (EVL).

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-MEM-001 | Append-only ledger keyed by route_id | AMEND | D2 → D2 (new clauses D0) | "Append-oriented" permits in-place edits; no schema versioning, idempotency or erasure rule |
| ADRL-MEM-002 | Three-state outcome lifecycle with defined close | AMEND | D2 → D2 (state machine) / D0 (window) | `closed_final` defined by absence of unknown future evidence is unfalsifiable; human correction unnamed; no censoring rule |
| ADRL-MEM-003 | Verification enriches, never overwrites | AMEND | D2 → D2 | Verification events lack verifier version, tree identity and an `indeterminate` result; SAF-007 blocks become capability failures |
| ADRL-MEM-004 | Cause-typed labels, six types not four | AMEND | D2 → D2 (enum) / D0 (completeness) | Text says four, code has six; no `context_feasibility`; labels carry no provenance/confidence; no safe default |
| ADRL-MEM-005 | Prompt-derived artefacts are prompt-class data | REJECT | D2 → D1 (replacement) | Embeddings are invertible (92% exact at 32 tokens; zero-shot with black-box encoder); late pins leave pre-pin embeddings; hashes unkeyed |
| ADRL-MEM-006 | Memory facade, fail-safe but never silent | AMEND | D2 → D2 (facade) / D1 ("not a semantic dependency") | Degraded mode is an invisible evidence hole; the real semantic dependency is the process-local session dict, not SQLite |
| ADRL-MEM-007 | Projections are rebuildable and versioned | AMEND | D2 → D2 (conditional on rebuild-equivalence test) | No projection identity (ledger position, embedding model, code); detection mechanism unspecified and mtime is wrong under WAL; index is a LRN-004 leak |
| ADRL-MEM-008 | Retrieval stays advisory until gated | APPROVE | D3 → D3 | Text grants no authority path and defers thresholds to EVL-004; attacks land on EVL-004's gate definition |
| ADRL-MEM-009 | Counterfactuals bind only to explicit route_id | APPROVE | D2 → D2 | Explicit binding is necessary (PROV, OpenLineage) and should not be relaxed for volume; sufficiency belongs to LRN-002 |
| ADRL-MEM-010 | Retention and erasure of ledger and derived artefacts | PROPOSED (new) | — → D0 | MEM-001 immutability + MEM-005 prompt-class data with no erasure path is untenable for a payments company |

Tally: 2 APPROVE, 6 AMEND, 1 REJECT, 1 PROPOSED.

## Cross-cutting findings

1. **The bucket's promise is "the record can be trusted"; its two load-bearing words — "append-only" and "cause-clean" — were both under-specified in ways the code has already exposed.** MEM-001 said "append-oriented"; MEM-004 said four failure types while `outcomes.py` has six. Both are fixed by amendment, but the pattern (decision text lagging code) should trigger a register rule: any enum or state set named in a decision is versioned and the decision cites the version.

2. **Derived data is data, and the register only half-believed it.** MEM-005's rationale states the principle; its decision stores embeddings for every non-private turn. The inversion literature (Morris et al. 2023: 92% exact recovery at 32 tokens; zero-shot inversion in 2025 with only black-box encoder access — and ADRL ships the encoder) makes the embedding store a lossy copy of the company source code. This is the one REJECT in the bucket. Its consequences ripple: MEM-001 needs a logged-erasure exception, MEM-007 needs erasure to invalidate projections, and the bucket needs MEM-010 (retention and erasure) which did not exist. The SAF-002 late-pin case (secret detected at turn *k*, turns 1…*k−1* already embedded and immutable) is the concrete hole.

3. **Every "evidence" claim has an invisible denominator.** Degraded memory (MEM-006) drops decisions silently; privacy suppression (MEM-005) removes sensitive turns from retrieval and pairing; subagent traffic (SEM-006, D0) has no route identity; stale projections (MEM-007) measure a different system. None of these was counted. Amendments make each one a reported quantity and, where it touches an evaluation window, an EVL-009 blocker.

4. **The retrieval index is a leakage path for LRN-004.** A kNN projection built over the whole ledger contains outcomes from sessions later than the decision being evaluated. Without a ledger high-water mark on the projection (MEM-007 amendment) an "as-of" rebuild is impossible and offline retrieval metrics are optimistic by construction.

5. **The process-local dict, not SQLite, is the multi-worker blocker.** The register's open item asks whether the facade isolates SQLite; it does, and it does not matter. Session-to-route and sticky-episode state (CAS-005/006) live in a Python dict outside the port. OPS-001 is blocked there. SQLite's own constraints (single writer, same-host WAL, deferred-transaction upgrade failures) are real but declarable through the port contract (MEM-006 clause 4).

6. **Conflicts with other buckets recorded:** MEM-004 vs CAS-002 (four-way typing in both; both need the six/seven-way set); MEM-003 vs SAF-007 (policy-blocked verification must be `indeterminate`, not `fail`); MEM-006 vs SAF-004 (degraded memory on a pinned session must stay pinned); MEM-008 vs EVL-004 (quantity gate needs a representativeness condition and a suppressed-fraction report); MEM-002 vs CAS-005 (local outcome must close final as a failure when the episode escalates).

**Proposed new decision:** ADRL-MEM-010 — Retention and erasure of ledger and derived artefacts (status Proposed; file written).

## Sources consulted

- Microsoft Azure Architecture Center, "Event Sourcing pattern" — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- M. Rook, "Forget me please? Event sourcing and the GDPR" (2017) — https://www.michielrook.nl/2017/11/forget-me-please-event-sourcing-gdpr/
- OpenLineage, "Object Model" — https://openlineage.io/docs/spec/object-model/
- W3C, "PROV-DM: The PROV Data Model" — https://www.w3.org/TR/prov-dm/
- SQLite, "Write-Ahead Logging" — https://www.sqlite.org/wal.html
- SQLite, "PRAGMA statements" (`data_version`) — https://www.sqlite.org/pragma.html
- tenthousandmeters.com, "SQLite concurrent writes and 'database is locked' errors" — https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/
- O. Chapelle, "Modeling delayed feedback in display advertising" (KDD 2014) — https://dl.acm.org/doi/10.1145/2623330.2623634 ; PDF http://wnzhang.net/share/rtb-papers/delayed-feedback.pdf
- "Learning under label delay on streaming tabular data" (arXiv 2409.10111, 2024) — https://www.arxiv.org/abs/2409.10111
- GitClear, "AI Copilot Code Quality: 2025 Data Suggests 4x Growth in Code Clones" — https://www.gitclear.com/ai_assistant_code_quality_2025_research
- Q. Luo, F. Hariri, L. Eloussi, D. Marinov, "An Empirical Analysis of Flaky Tests" (FSE 2014) — https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf
- OpenAI, "Introducing SWE-bench Verified" (2024) — https://openai.com/index/introducing-swe-bench-verified/
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021) — https://arxiv.org/abs/2103.14749
- C. Northcutt, L. Jiang, I. Chuang, "Confident Learning: Estimating Uncertainty in Dataset Labels" (JAIR 2021) — https://arxiv.org/abs/1911.00068
- M. Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2503.13657, 2025) — https://arxiv.org/abs/2503.13657
- Scale AI, "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" (arXiv 2509.16941, 2025) — https://arxiv.org/html/2509.16941v1
- "TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks" (arXiv 2412.14161, 2024) — https://arxiv.org/abs/2412.14161
- J. Morris, V. Kuleshov, V. Shmatikov, A. Rush, "Text Embeddings Reveal (Almost) As Much As Text" (EMNLP 2023) — https://arxiv.org/abs/2310.06816
- "Rethinking the Privacy of Text Embeddings: A Reproducibility Study" (arXiv 2507.07700, 2025) — https://arxiv.org/abs/2507.07700
- "Universal Zero-shot Embedding Inversion" (arXiv 2504.00147, 2025) — https://arxiv.org/abs/2504.00147
- "ALGEN: Few-shot Inversion Attacks on Textual Embeddings using Alignment and Generation" (arXiv 2502.11308, 2025; search result only) — https://arxiv.org/abs/2502.11308
- L. Demir, A. Kumar, M. Cunche, C. Lauradoux, "The Pitfalls of Hashing for Privacy" (IEEE Comm. Surveys & Tutorials, 2018; title/venue only, full text not fetched) — https://ieeexplore.ieee.org/abstract/document/8023740/
- D. Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NIPS 2015) — https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- E. Breck et al., "The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction" (IEEE BigData 2017) — https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
- S. Kaufman, S. Rosset, C. Perlich, O. Stitelman, "Leakage in Data Mining: Formulation, Detection, and Avoidance" (ACM TKDD 2012) — https://dl.acm.org/doi/10.1145/2382577.2382579
- I. Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data" (arXiv 2406.18665, 2024) — https://arxiv.org/abs/2406.18665
- S. Chen et al., "RouterDC: Query-Based Router by Dual Contrastive Learning" (NeurIPS 2024) — https://arxiv.org/abs/2409.19886
- Q. Hu et al., "RouterBench: A Benchmark for Multi-LLM Routing Systems" (arXiv 2403.12031, 2024) — https://arxiv.org/pdf/2403.12031
- "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World" (arXiv 2608.08239, 2026) — https://arxiv.org/html/2608.08239
