# Fable post-review dispositions

Original post-review.md and source/ are immutable first-review evidence. Reviewer session 4142beb3-97ac-4fcb-a1b8-60fc2fb6cbcf reported Fable 5.1, with an auxiliary Haiku metadata entry. No tools or tests were run by reviewer. IDs below are coordinator-assigned to the original unnumbered findings.

- CA-01, blocking, egress provenance: accepted and reproduced. egress-before-fix.log fails on intended deployment in served_receipt. Experiment mode now skips that legacy fallback. The regression checks null deployment/geo/trust plus direct host and proxy_observed source in the actual egress row. Awaiting recheck.
- CA-02, blocking, stop wording: accepted. CAS-006/report now state that any response not reporting target identity, including errors, stops the client. A composed 429 test checks that no second HTTP attempt occurs. Awaiting recheck.
- CA-03, nonblocking, subagent/background restriction: accepted limitation; another lineage or an unlisted model is rejected. No multi-agent harness compatibility claim.
- CA-04, nonblocking, lineage reservation before dispatch: accepted conservative limitation; a prepared but locally blocked first lineage consumes that process's binding. No automatic reset/reuse.
- CA-05, nonblocking, header fixture: fixed fixture verifies both local headers are removed, native x-claude-code-session-id and OAuth/beta are preserved. Native session identity is deliberately forwarded under the existing protocol contract, not claimed to be a secret-bearing local assertion.
- CA-06, nonblocking, synthetic bundle: accepted. The fixture bypasses full configuration loading with synthetic objects, although constructor checks are exercised. Its full inventory/member validity is not established; it must not be used as a live admission artifact.
- CA-07, nonblocking, deadline cancellation: accepted limitation. Cancellation may reach a slow consumer as CancelledError; no uniform TimeoutError promise for all consumers. Slot release/closure occurs on unwinding. Live stream behavior remains a qualification gate.
- CA-08, nonblocking, encoding: accepted. Model-only means JSON-value preservation apart from model, not identical whitespace/escaping on rewritten bodies. Normal passthrough bytes are unchanged.
- CA-09, architecture placement: acknowledged in SEM-007. Candidate collaborator currently lives in proxy; production profile integration remains outstanding and is not called complete.
- CA-10, overview rows: user asked for a plain explanation, then replied "try now" after the exact no-promotion restoration question. Restored existing INDEX values only and preserved the human disposition. No canonical status/maturity/verdict change.

Code acceptance remains scoped to an offline candidate. Live launch, production contract, meaningful model selection, savings and learning remain unproved. This correction is round one; one further review/correction round remains under the skill cap if a material finding requires it.

## Recheck disposition

CA-01/02 verified fixed by Fable recheck.md. Full six checks passed on corrected runtime: 949 passed, 8 skipped. The recheck requested exact root CHANGELOG stop wording and a CAS-009 restoration-only citation; both are corrected. The reported broken SEM-007 heading was an excerpt-generation defect in recheck-input.txt, not the actual ADR or frozen source; the literal source heading is supplied in final review. No source heading was changed unnecessarily. Stop-on-missing-identity depends on finalization; an abandoned stream may be bounded by the attempt/deadline controls without setting stopped. This is a retained launch qualification limit, not a closed capability.

Final documentation recheck accepted the corrections in final-review.md, session d86aa362-9432-4636-bf4a-509d45a4a39c. No remaining blocking finding for the offline slice; launch limitations remain. Eight skipped tests are unapproved engine execution tests, not new adapter skips. Runtime/source hashes were compared by coordinator; reviewer did not execute checks.
