**Outcome: both blocking corrections are verified against source and evidence. The offline candidate is accepted in offline scope. Two small register defects remain before the taxonomy sync receipt. No live admission or maturity change is granted, and the final full suite is still a closure condition.**

**CA-01, egress provenance: verified.** The fallback in `_record_receipt` is now guarded by an experiment-is-None check, so the experiment path passes a null deployment to the egress fields. Host comes from the observation, which the receipt override fixes to the configured destination. Negative evidence is real: egress-before-fix.log fails on the intended deployment id in the served_receipt row. Positive evidence is the focused run, and the 27-test count matches the 21 unit and 6 composition tests in the shown files. The regression asserts null deployment, geo and trust zone, the direct host and proxy_observed source on the actual egress row. The CAS-006 and TRU-002 wording is now accurate for both the served event and the egress ledger. Non-experiment behaviour is untouched by the guard.

**CA-02, stop wording: verified.** The ADR and report now say any response not reporting the target model, including errors and missing identity, stops dispatch. The 429 composition test exercises two requests and asserts one upstream attempt and the stopped flag. Code path checks out: the second request passes selection on the same lineage, then the transport refuses because stopped is set.

**Nonblocking dispositions: recorded.** The report's limits section covers subagent and background refusal, unreleased lineage reservation, the synthetic bundle, forwarded native session identity, CancelledError, value-only JSON preservation and open profile integration. The header fixture now asserts both local headers are stripped and the native session header preserved. The source of forward_headers is not in the packet, so this rests on the passing test only.

**Grades unchanged: verified.** Every owning row and bucket row shows the prior grade with no promotion. The SEM-007 restoration record shows identical before and after fields with the bucket display added.

**Remaining register defects, fix before the receipt**

- **CHANGELOG lags CAS-006.** The CHANGELOG entry still reads "Model mismatch stops further dispatch" while the ADR, bucket text and report carry the corrected wording. One of the four synchronized surfaces is stale.
- **SEM-007 section heading is broken.** The placement note appears under a heading rendered as ", 2026-09-09" with no title text.
- **CAS-009 row cites the wrong evidence.** The restored bucket row is labelled "offline candidate evidence" and links the candidate report, but the candidate does not implement action-effect provenance and CAS-009 is not an owner. The row should cite the restoration disposition only. Its INDEX values cannot be confirmed from the packet, since the INDEX excerpt omits CAS-009.

**Scope nuance to record, not blocking.** The stop trigger depends on finalization running. A stream that hits the deadline before reporting identity releases the slot but may never reach the receipt override if the harness does not run the finalizer. The attempt cap still bounds total dispatch.

**Standing conditions.** Closure waits on the three register fixes, the full six-check run, and the sync receipt. Live eligibility remains blocked by the unqualified config, signed inventory and account prerequisites.