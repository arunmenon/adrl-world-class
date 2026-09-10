```json
{
  "review_id": "rv-reconciliation-2026-09-10",
  "verdict": "RV-01 verified-fixed within its tested scope; RV-02 through RV-06 unresolved on current code.",
  "summary": "RV-01 acceptance (composed proxy-and-cascade test reaching an explicit Closer; readiness counting one closed route) is met by test_outcome_contract.py, checks-2 (922 passed, 8 skipped, 324 inputs stable, hashes equal recheck-manifest) and the recheck condition. The repair is producer-to-closer/readiness only: rule_health, tripwire coverage and the learning reader still consume old shapes. Current pipeline.py differs from the reviewed hash; only the 11-test focused run, recorded from a coordinator transcript, covers that drift. No maturity change; no historical edits.",
  "reconciliations": [
    {
      "global_id": "fable-retrospective-2026-09-08:RV-01",
      "disposition": "verified-fixed",
      "scope": "Cascade and forwarded proxy outcome rows reach routes_in_state, Closer, label derivation and learning_readiness on synthetic ASGI. Not verified: adrl ledger readiness CLI, real harness, cold-start forwarding, downstream label readers (RV-05/06), any learning claim.",
      "evidence": "controller._outcome emits OUTCOME_EVENT with payload state, session/lineage HMAC; pipeline._finalize appends cascade LedgerEvent verbatim. test_composed_outcomes_close_once asserts closed_final_count==1, censored==1, no_capability_evidence blocker. before-regression.log failed at routes_in_state (recheck). checks-2 manifest status passed, changed_inputs empty, test sha b19cd9e2 unchanged in current-test.json, 11 passed on current tree."
    },
    {
      "global_id": "fable-retrospective-2026-09-08:RV-02",
      "disposition": "unresolved",
      "scope": "Initial route selection in ambiguous band.",
      "evidence": "router.py _advise returns ambiguous_fallback_rung when self._classifier is None, discarding select_rung result; no sensitivity test; no cheap-cloud-on-merit rate recorded."
    },
    {
      "global_id": "fable-retrospective-2026-09-08:RV-03",
      "disposition": "unresolved",
      "scope": "Lab and suite path dependence.",
      "evidence": "run_routing_lab.py signs RepoInventory(root=str(ROOT)); repo-classification-v1.json still matches only /Users/arunmenon/projects/adrl-core as open; default class lacks frontier. No two-path reproduction recorded."
    },
    {
      "global_id": "fable-retrospective-2026-09-08:RV-04",
      "disposition": "unresolved",
      "scope": "Bundle mode versus run mode disclosure.",
      "evidence": "run_routing_lab.execute loads bundle with routing_mode=SHADOW then builds LIVE components; write_report emits no bypass sentence. Outcome-contract report.md and test docstring disclose 'inherited SHADOW-load/LIVE admission bypass' for that review only; acceptance requires propagation to every lab table and ADR evidence note, or mode equality. One later disclosure does not satisfy it."
    },
    {
      "global_id": "fable-retrospective-2026-09-08:RV-05",
      "disposition": "unresolved",
      "scope": "Rule health and trip-wire coverage readers.",
      "evidence": "rule_health.compute_rule_health and tripwires.coverage_report still query event_type='closed_final' with verified/success payload keys; Closer writes OUTCOME_EVENT with state and label, so both readers still count nothing from runtime rows. No demotion test from cascade-written events."
    },
    {
      "global_id": "fable-retrospective-2026-09-08:RV-06",
      "disposition": "unresolved",
      "scope": "Learning reader versus label corrections.",
      "evidence": "tiers.EventNames lists outcome, verification, label, counterfactual only; append_late_evidence writes label_event with supersedes_seq that _example_from_row never reads. No test showing a reverted route labelled failure."
    }
  ],
  "findings": [
    {
      "id": "RC-01",
      "global_id": "rv-reconciliation-2026-09-10:RC-01",
      "severity": "medium",
      "kind": "evidence integrity",
      "blocking": false,
      "confidence": "high",
      "owning_adrs": ["EVL-006", "OPS-004", "MEM-001"],
      "title": "The RV-01 green full-check evidence binds to a pipeline.py hash the current tree no longer carries; only an 11-test transcript covers the drift.",
      "evidence": "comparison.json: pipeline.py reviewed 68a170c3 versus current 300069be; AGENTS.md and CLAUDE.md also differ. current-test.json capture is 'coordinator transcript, not raw pytest log', focused file only.",
      "acceptance_criteria": "Rerun the full engineering checks on the current source with a retained manifest, or record the pipeline.py diff and reason next to the RV-01 disposition.",
      "appendix_refs": "comparison.json, current-test.json, checks-2/manifest.json."
    },
    {
      "id": "RC-02",
      "global_id": "rv-reconciliation-2026-09-10:RC-02",
      "severity": "low",
      "kind": "unsupported claim",
      "blocking": false,
      "confidence": "high",
      "owning_adrs": ["MEM-004", "OPS-005"],
      "title": "RV-01 acceptance names the adrl ledger readiness CLI; the evidence exercises learning_readiness() directly.",
      "evidence": "test_outcome_contract.py calls learning_readiness(live.store); no CLI invocation or log in the review directory.",
      "acceptance_criteria": "One recorded CLI run against a composed-pipeline ledger showing closed_final_count > 0, or amend the disposition to state the function-level scope.",
      "appendix_refs": "findings.md RV-01 acceptance; report.md."
    }
  ]
}
```