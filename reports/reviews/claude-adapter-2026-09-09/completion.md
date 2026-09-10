# Claude adapter: offline slice complete

ADRL can now make a forced initial Claude model choice through its actual pipeline while preserving the other JSON request fields. The composed test asks for the source Claude model, forwards Sonnet, and records the model reported by the synthetic provider. It also proves the experiment is refused in SHADOW/OFF or with the current unqualified LIVE configuration. This is not a real Claude run or evidence of savings.

A dedicated direct client enforces finite request/output/byte/time limits, one active response, permitted operation/model checks, no redirects and no automatic retries. It has no normal startup switch. The target must be permitted by the gates and match the inventory. Native session identity is preserved; local assertion/session headers are removed.

Fable's independent review caught a misleading egress receipt. We reproduced it, fixed it, and added an assertion on the actual egress row. Fable verified that correction and the stop-condition wording, then checked the remaining documentation corrections. Original findings and disagreements are retained.

Validation: **949 passed, 8 engine tests skipped; all six required engineering checks passed.** There are 27 focused candidate tests. The taxonomy checker itself passed 19 tests. All 428 declared source hashes match final review, and all canonical ADR status/maturity/verdict fields are unchanged. Seven owning decisions and their index/bucket/changelog entries are synchronized. The two missing overview rows were restored using existing INDEX values after the owner's disposition.

The local taxonomy closure [passed](taxonomy-check-final-2.log). Original receipt: [/Users/arunmenon/projects/.adrl-execution-state/claude-adapter-final-20260909.json](/Users/arunmenon/projects/.adrl-execution-state/claude-adapter-final-20260909.json); [copy](receipt-copy.json). An earlier closure attempt used the wrong JSON key for empty review blockers and failed; the record was corrected without changing reviewer dispositions. The earlier missing-row failure is also retained.

**Where we are:** P1, one of the six budgeted engineering slices attempted and closed in offline scope. No ADRL task-model attempts, paid API use, live activation, policy learning or automation restart occurred. Reviewer calls used the existing Claude collaboration path; their CLI usage metadata is separate from task evidence.

**Next:** qualify the isolated live experiment profile: legitimate configuration/inventory/workspace, restart-safe run allowance, native harness confinement and account overflow disposition. Validate native request query/output settings rather than silently removing or reducing them. Then test actual Claude initial selection and compare verified task quality and complete usage under a frozen policy. Mid-session switching, subagents, background model calls, production protocol-profile integration and learning remain outside this slice.

The candidate is deliberately restrictive: other lineages/models and any query string are refused; a prepared lineage remains reserved even if later blocked; counters are process-local. Responses not reporting the target model stop further dispatch when finalized, including upstream errors. Abandoned streams may rely on attempt/deadline caps without setting the stop flag. These limitations remain live-launch gates, not completed capabilities.

Owners: **FND-001/003/005, SEM-007, TRU-002, CAS-006/007**. Independent [code recheck](recheck.md), [final documentation acceptance](final-review.md), [dispositions](dispositions.md), [raw checks](recheck-checks/checks.json), [implementation detail](report.md). Formal maturity change: **none**.
