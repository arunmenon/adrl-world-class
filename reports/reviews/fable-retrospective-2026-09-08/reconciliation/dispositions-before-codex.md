# Dispositions: ADRL retrospective, 7 to 8 September 2026

Reviewer severity, confidence and original text are immutable (see `findings.md`). The implementer (Codex) fills the author-response, fix-reference and recheck columns; unresolved contested blocking findings go to the product owner. Allowed dispositions: accepted, fixed-awaiting-recheck, verified-fixed, deferred-with-reason, disputed-with-evidence, unresolved. Initial state for every row: `unresolved` (no author response yet).

| ID | Severity | Confidence | Owning ADRs | Finding | Blocks | Author response | Fix reference | Reviewer recheck | Remaining gate | Disposition |
|---|---|---|---|---|---|---|---|---|---|---|
| RV-01 | critical | high | MEM-001, MEM-002, MEM-004, LRN-001 | Live outcome events are invisible to every consumer that turns a decision into a label. | blocking |  |  |  |  | unresolved |
| RV-02 | high | high | RTG-002, RTG-003, RTG-006 | The estimator, thresholds and cost model never influence the initial route; cheap cloud is never chosen on merit. | blocking |  |  |  |  | unresolved |
| RV-03 | high | high | TRU-001, OPS-005, EVL-005 | Lab routing evidence and the 911-test result depend on the author's absolute checkout path. | blocking |  |  |  |  | unresolved |
| RV-04 | high | high | FND-005, OPS-005, RTG-001 | The lab reaches live dispatch by loading the bundle in shadow mode, and the reports do not say so. | blocking |  |  |  |  | unresolved |
| RV-05 | high | high | RTG-003, CAS-001 | Rule health and trip-wire coverage read a third event shape that no runtime producer writes. |  |  |  |  |  | unresolved |
| RV-06 | high | high | MEM-002, LRN-001 | Late human corrections update the ledger label but never reach learning examples. |  |  |  |  |  | unresolved |
| RV-07 | high | high | LRN-001, MEM-003, EVL-004 | T1 evidence is unreachable because nothing produces a verifier-precision record. |  |  |  |  |  | unresolved |
| RV-08 | high | high | LRN-004, LRN-005, LRN-008 | Every organic decision since W7.0a is untrainable and unexplorable. |  |  |  |  |  | unresolved |
| RV-09 | high | high | LRN-004, MEM-007 | The neighbour success feature reports success for verifier-failed routes. |  |  |  |  |  | unresolved |
| RV-10 | high | high | SAF-007, OPS-001, FND-005 | The isolated backend cannot host a real harness, so the roadmap's next W3 step does not lead to a real-task demonstratio | blocking |  |  |  |  | unresolved |
| RV-11 | high | high | SAF-007, MEM-003 | No code extracts output from a stopped container, so "the retained layer" is not task-output evidence. |  |  |  |  |  | unresolved |
| RV-12 | high | high | EVL-007 and each affected decision | Thirteen to sixteen historical D3 and D4 grades are displayed as current although EVL-007 says a new implementation inhe |  |  |  |  |  | unresolved |
| RV-13 | high | high | EVL-007, OPS-008 | No independent reviewer has been named in twenty-one journey entries although the W0 exit required it. | blocking |  |  |  |  | unresolved |
| RV-14 | high | high | MEM-008, MEM-005, MEM-007 | MEM-008 "runs against real traffic, 34 of 300 evaluated decisions" describes the old codebase; adrl-core never instantia |  |  |  |  |  | unresolved |
| RV-15 | high | high | LRN-007, EVL-005 | The improvement experiment's headline overstates a tautological result. |  |  |  |  |  | unresolved |
| RV-16 | high | high | RTG-003, LRN-004, EVL-002 | The routing-correction record omits that candidate 2 was fitted to the two literals that failed candidate 1, that the fr |  |  |  |  |  | unresolved |
| RV-17 | medium | high | LRN-004, RTG-003 | features-v2 introduced over-routing classes the record does not name, with no over-route budget. |  |  |  |  |  | unresolved |
| RV-18 | medium | high | RTG-003, SEM-005 | No outcome-driven adaptation is wired into the running service. |  |  |  |  |  | unresolved |
| RV-19 | medium | high | EVL-006, OPS-004 | Five frozen wave packets were amended after their hashes were recorded. |  |  |  |  |  | unresolved |
| RV-20 | medium | high | OPS-001, SAF-007, EVL-006 | Engine evidence lives only in the private state directory and the eight engine tests have been skipped in every run sinc |  |  |  |  |  | unresolved |
| RV-21 | medium | high | OPS-001 | Permanent execution fences make every supervised workspace single-use. |  |  |  |  |  | unresolved |
| RV-22 | medium | high | MEM-010, SAF-002 | Materialised plaintext copies have no durable custody record. |  |  |  |  |  | unresolved |
| RV-23 | medium | high | register rules in `R/AGENTS | INDEX rows are stale for 21 decisions although each 8 September changelog entry claims synchronisation; bucket overview  |  |  |  |  |  | unresolved |
| RV-24 | medium | high |  | Eleven Maturity fields describe defects that `C/docs/known-gaps.md` records as closed on 3 September. |  |  |  |  |  | unresolved |
| RV-25 | medium | high |  | Leadership artefacts are frozen at journey entry 014 while the program is at 021; the lab shows a synthetic endpoint wit |  |  |  |  |  | unresolved |
| RV-26 | medium | high | OPS-006, TRU-002 | The served-identity debate concerns a header the runtime does not read. |  |  |  |  |  | unresolved |
| RV-27 | medium | high | CAS-004, RTG-008 | Thinking-block binding is per model version and per exact prefix, with 400 by default for accounts created on or after 3 |  |  |  |  |  | unresolved |
| RV-28 | medium | high | SEM-004, RTG-009 | Server-side compaction arrives inside the response and its tokens sit outside top-level usage; nothing sums `usage.itera |  |  |  |  |  | unresolved |
| RV-29 | medium | high | OPS-008, EVL-009 | W3.2b2d2 closed as validated despite recorded stop-rule deviations and a self-granted exception with no owner dispositio |  |  |  |  |  | unresolved |
| RV-30 | medium | high | FND-005, OPS-001 | Roughly half of the two-day engineering built a container execution backend that no product stage requires and that the  |  |  |  |  |  | unresolved |
| RV-31 | medium | high |  | Shadow retrieval, embedding writer, instruction hasher, projection index and human-correction detector are never compose |  |  |  |  |  | unresolved |
| RV-32 | medium | high | EVL-006, OPS-004 | Validation records are overwritable and machine-bound. |  |  |  |  |  | unresolved |
| RV-33 | low | high |  |  |  |  |  |  |  | unresolved |
| RV-34 | low | high |  |  |  |  |  |  |  | unresolved |
| RV-35 | low | high |  |  |  |  |  |  |  | unresolved |
| RV-36 | low | high |  |  |  |  |  |  |  | unresolved |
| RV-37 | low | high |  |  |  |  |  |  |  | unresolved |
| RV-38 | low | high |  |  |  |  |  |  |  | unresolved |
| RV-39 | low | high |  |  |  |  |  |  |  | unresolved |
| RV-40 | low | high |  |  |  |  |  |  |  | unresolved |
