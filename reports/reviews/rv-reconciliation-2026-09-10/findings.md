# New reconciliation review findings

## rv-reconciliation-2026-09-10:RC-01 — The RV-01 green full-check evidence binds to a pipeline.py hash the current tree no longer carries; only an 11-test transcript covers the drift.

comparison.json: pipeline.py reviewed 68a170c3 versus current 300069be; AGENTS.md and CLAUDE.md also differ. current-test.json capture is 'coordinator transcript, not raw pytest log', focused file only.

Acceptance: Rerun the full engineering checks on the current source with a retained manifest, or record the pipeline.py diff and reason next to the RV-01 disposition.

## rv-reconciliation-2026-09-10:RC-02 — RV-01 acceptance names the adrl ledger readiness CLI; the evidence exercises learning_readiness() directly.

test_outcome_contract.py calls learning_readiness(live.store); no CLI invocation or log in the review directory.

Acceptance: One recorded CLI run against a composed-pipeline ledger showing closed_final_count > 0, or amend the disposition to state the function-level scope.

