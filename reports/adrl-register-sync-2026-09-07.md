# Decision register synchronization

7 September 2026 | Product foundation implementation

The implementation was already recorded under SEM-007. This synchronization also updates the
system boundary, release gate, related decision records, bucket overviews, main index and change
history. It makes the same implementation status visible from the taxonomy's normal entry points.

| Decision | What is recorded | Disposition and evidence limit |
|---|---|---|
| [FND-001](../adr/FND/ADRL-FND-001.md) | Shared ADRL engine, harness adapters, protocol profiles and a separate product API | Product direction clarified; current model-traffic support remains Messages |
| [FND-005](../adr/FND/ADRL-FND-005.md) | First stable product interface requires two harnesses and two protocols | Application of the existing measured-scope rule; gate remains unmet |
| [SEM-007](../adr/SEM/ADRL-SEM-007.md) | Messages extraction, adapter/profile interfaces, Responses admission choice | D2 evidence for the extracted Messages boundary; full cross-protocol contract remains Proposed and incomplete |
| [SEM-002](../adr/SEM/ADRL-SEM-002.md) | Claude Code correlation extraction and unchanged session/lineage derivation | Implementation refactor with baseline identity comparisons; no new authentication authority |
| [CAS-007](../adr/CAS/ADRL-CAS-007.md) | Native Messages response rendering moved into the protocol package | Existing error and retry policy retained; import-order defect corrected and tested |
| [MEM-001](../adr/MEM/ADRL-MEM-001.md) | Profile/adapter versions added to new decision context; typed public event preview | Existing history and append rules retained; public ingestion and its idempotency mapping remain unimplemented |
| [TRU-001](../adr/TRU/ADRL-TRU-001.md) | Correlation, authenticated workload identity and distribution discovery have separate roles | No claim that the new adapter or capability endpoint establishes workload authority |

SEM-001/003/004/006, CAS-003/004 and the SAF decisions remain dependencies of the extracted path.
Their policy clauses were not changed by this package. Retained regression tests are evidence
against implementation regression, not a new research disposition or blanket maturity upgrade.

The evidence is the [implementation record](/Users/arunmenon/projects/adrl-world-class/reports/adrl-product-foundation-implementation-2026-09-07.md)
and its [manifest](/Users/arunmenon/projects/adrl-world-class/reports/research/adrl-product-foundation-2026-09-07.json):
463 tests passed, all six required checks passed, and all 25 changed implementation files still
match the tested hashes at this synchronization. No runtime code or database history was changed
by this documentation pass.

The [synchronization validation](research/adrl-register-sync-validation-2026-09-07.json) confirms
that all 77 decision files appear exactly once in the index, the new local links resolve, and
the historical decision changelogs and original taxonomy body are preserved.

The original taxonomy remains available as a historical source, with a dated note directing readers
to the current register. This pass does not accept all pending proposals or publish changes back
to Confluence or the Claude-hosted artifacts.
