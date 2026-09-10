**Outcome: the offline implementation is sound within its declared scope. Scoped acceptance of the code as an offline candidate, with changes requested before taxonomy closure. No live admission or human graduation is granted. The SEM-007 and CAS-009 overview rows remain an explicit closure blocker, and the final full suite run is not yet evidence.**

**Verified against source**

- Selection runs after fallback, pin, rung, transform and permitted-set checks, and before write-ahead egress, as FND-003 claims.
- The target must exist in the permitted set and equal the catalog entry, with frontier rung, Anthropic provider, direct host and non-local zone. TRU-002 text is accurate.
- Transport reserves an attempt before any await, refuses non-POST, foreign origins, query strings, oversize bodies, foreign models, API-key headers and over-cap output before HTTP. Redirects are not followed, health forwards nothing, and the single-active slot is released on close or deadline.
- SHADOW and OFF are refused at construction. The unqualified current config fails the evidence check.
- Duplicate keys, existing assistant history and initial tool results are refused at selection.

**Blocking for closure (claim accuracy)**

- **Egress receipt row contradicts CAS-006 text.** The served ledger event carries a null deployment id, and the test asserts that. But `_record_receipt` in pipeline.py falls back to the intended deployment when the observed id is null. The egress served_receipt row therefore records the intended deployment id, trust zone and geo under a proxy_observed source. The register line "deployment, geography and trust receipt fields stay unknown" is false for the egress ledger. Either restrict the fallback in experiment mode or correct the CAS-006 and TRU-002 wording. Add an assertion on the egress row.
- **Stop trigger is broader than stated.** On any 4xx response or any body without a model, the observation is assumed_intended with the source model. The receipt override then sets stopped because it does not equal the target. A single overloaded or rate-limit response permanently halts the process. This is acceptable for a bounded experiment, but the "model mismatch stops further dispatch" text should say "any response not reporting the target model, including upstream errors". The served event on that path records the source model, flagged only by the source field.

**Changes requested (non-blocking, record in the report)**

- **Subagent and background lineages.** Selection binds to one lineage hmac. Every subagent request and every background Haiku call is refused with an error to the harness. The report does not mention this. It changes what a live step could observe.
- **Lineage binds before dispatch.** The selection sets its lineage on prepare, but the pipeline can still block afterwards on the catalog check or egress ledger. A never-dispatched lineage then excludes all others for the process.
- **Header-name fixture absent.** The pre-review asked for an offline check that the session identity header is stripped. The unit test only covers the workload assertion header. Add the fixture before any credential-bearing run.
- **Composition bundle is not loadable.** The qualify path replaces the inventory with one deployment. That bundle would fail the endpoint inventory check for enabled rung members with no deployment. The constructor only runs the evidence check. State that the composition evidence used a bundle the full checker rejects.
- **Deadline cancellation surface.** The stream timeout wraps yields, so when the harness is the slow party the cancel lands in the consumer task as a bare CancelledError rather than TimeoutError. The slot is still released. Document it.
- **Encoding drift.** Re-serialization escapes non-ASCII and compacts whitespace. Semantics are preserved and the byte limit is applied post-rewrite. Note that the byte-exact claim is semantic, not literal.

**Taxonomy ownership**

Ownership mapping is defensible. One tension to record: SEM-007 states native model semantics belong to profiles, yet the model rewrite lives in the proxy module and bypasses the profile's serialize method. Either the SEM-007 line should acknowledge this as a scoped exception or the rewrite should move behind the profile in a later slice. FND-001, FND-003, FND-005, TRU-002, CAS-006 and CAS-007 entries preserve prior wording and grades. CAS-009 is absent from every mapping and the overview; that omission stands as reported.

**Standing blockers**

Taxonomy closure waits on the SEM-007 and CAS-009 overview rows, the two claim corrections above, the final full suite result, and the taxonomy sync receipt. Live eligibility remains blocked by the real config, signed inventory and account prerequisites, unchanged by this slice.