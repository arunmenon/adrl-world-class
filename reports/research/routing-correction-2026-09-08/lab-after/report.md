# Routing lab: actual choices, synthetic execution

Real ADRL stages ran against a controlled in-process endpoint. No harness or model
executed a coding task. Receipt identity is synthetic. No quality or savings measured.

A continuation keeps its original route ID and initial choice. Its dispatched tier
can change through cascade or privacy enforcement. Read both columns together.

| Case | Initial choice | Dispatched tier | Endpoint received | Identity source | State |
|---|---|---|---|---|---|
| small-edit | local | local | local-qwen-7b | gateway_reported | responded |
| bug-repair | frontier | frontier | claude-fable-5-1 | gateway_reported | responded |
| test-work | frontier | frontier | claude-fable-5-1 | gateway_reported | responded |
| refactor | frontier | frontier | claude-fable-5-1 | gateway_reported | responded |
| mixed-rename | frontier | frontier | claude-fable-5-1 | gateway_reported | responded |
| mixed-explain | frontier | frontier | claude-fable-5-1 | gateway_reported | responded |
| long-context | frontier | frontier | claude-fable-5-1 | gateway_reported | responded |
| loop-detected | local | local | local-qwen-7b | gateway_reported | responded |
| loop-escalated | local | cheap_cloud | cheap-haiku-us | gateway_reported | responded |
| before-secret | frontier | frontier | claude-fable-5-1 | gateway_reported | responded |
| secret-pin | frontier | local | local-qwen-7b | gateway_reported | responded |
| pin-persists | frontier | local | local-qwen-7b | gateway_reported | responded |
| pinned-overflow | - | - | no dispatch | - | blocked |
| missing-identity | local | local | local-qwen-7b | assumed_intended | responded |
| upstream-error | frontier | frontier | claude-fable-5-1 | - | upstream_error |
| responses-unqualified | - | - | no dispatch | - | unsupported |

Planned cells: 16. Accounting: {"responded": 13, "blocked": 1, "upstream_error": 1, "unsupported": 1}.

Task definitions: [manifest](manifest.json). Every event: [journal](events.jsonl).
Full decisions/features and receipts: [results](results.json).
Fixture/config qualifications: [environment](environment.json).

These exports are curated synthetic T4 diagnostics, ineligible for learning.
The manifest retains planned cells; --inspect reports interrupted work.
