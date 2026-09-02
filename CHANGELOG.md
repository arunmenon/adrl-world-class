# Changelog

## 2026-09-02 — Adversarial architecture review

- Converted the 49-decision register (FND, SEM, SAF, RTG, CAS, MEM, LRN) into one ADR file per decision under `adr/<BUCKET>/`.
- Reviewed every decision: 8 approved unchanged, 38 amended in place, 3 rejected and replaced in place (FND-004, SAF-007, MEM-005). Original text preserved verbatim in each file's changelog.
- Proposed 6 new decisions: SAF-008 (repository classification / residency / PII gate), SAF-009 (tamper-evident egress ledger), RTG-009 (session-marginal, cache-aware cost accounting), CAS-008 (escalation scope under subagents), MEM-010 (retention and erasure), LRN-008 (logged exploration in the ambiguous band).
- Recommended 10 maturity changes (9 down, 1 up); see `INDEX.md`.
- Reconciled cross-bucket seams: `failure-types-v2` shared by CAS-002 and MEM-004; CAS-008 interim aligned to SEM-006; RTG-007/LRN-003 given one shared definition of utility.
- Fact-checked 25 load-bearing citations against live sources; corrected 12 evidence lines that overstated or mislabelled a source.
- Added `REVIEW-LOG.md`, `INDEX.md`, `BIBLIOGRAPHY.md`, bucket `README.md`s, and `source/` (register reconstruction and review instructions).
