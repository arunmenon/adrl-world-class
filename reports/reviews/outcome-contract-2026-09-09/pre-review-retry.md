**Verdict: proceed, with three scoped changes.** The hypothesis is confirmed by the source. The cascade emits events whose event_type is the state string, while every consumer filters on event_type equal to "outcome" and reads the state from the payload. Consumers affected: outcome projection, routes in closed_turn for the Closer, label derivation, readiness counting, and the human correction detector.

**Material blockers**

- **The proxy forwarding path cannot preserve the contract as written.** In the finalize excerpt, forwarded outcome events are re-keyed to the current decision's route id and appended through a helper that takes only type and payload. The event's own route id, producer, producer sequence and schema version are discarded. For continuation requests the sticky route differs from the decision route, so closed_turn rows would be attributed to the wrong route. Fix is minimal: append the LedgerEvent verbatim on that path. Otherwise the plan's "retaining producer sequence and route attribution" claim is false for that path.
- **Plan-phase outcome events never reach the proxy fallback.** The plan method emits directly to the controller's ledger and does not return its events. With no controller ledger, pending and closed_turn(next_user_turn) rows are silently lost. Either require the ledger to be wired into the controller in production and test that composition, or record this fallback gap as an open item. Do not claim the fallback path is verified for plan-phase events.
- **Possible capability-label leak on 4xx failures.** In the failure observer, a completed response with status 400 to 499 that is not 429, not context-related, not policy-constrained and not assumed_intended produces an empty candidate list before primary resolution. The source of that resolver is not supplied. If its empty-list default is task_capability, a client-side or auth error becomes a capability failure at 0.6 confidence once the repair makes the row visible. Verify before merging and cover with a test. This is inside the stated failure-label preservation scope.

**Scope corrections**

- **Carry the top-level failure_type into the canonical payload.** Label derivation reads both the causes list and a top-level failure_type key. Keep the existing top-level key through the extra fields, or use one cause candidate, but not both, to avoid duplicate candidates. Secondary type is diagnostic only and is not read by labels.
- **Populate lineage_hmac on the cascade outcome payload.** The Closer's trigger reads session and lineage from the payload, then falls back to the decisions table. The lineage HMAC is already on the request context and is a keyed value, not raw content. Without it or a decision row, the idle trigger still works but subsequent-turn and episode-boundary triggers do not. Session HMAC only if the context already exposes it.
- **Do not set harness_reported_success to False.** Leave it None on both pending and closed_turn. Only True is read, so None is the correct "unknown".

**Behaviour the tests must capture, since it follows from the code as-is**

- A successful turn emits no closed_turn at observe time. The route only closes on the next user turn. So route B in the two-turn test remains pending and censored.
- A terminal failure emits closed_turn immediately, and a second closed_turn without failure_type on the next user turn. Label derivation scans all outcome payloads, so the cause survives, but assert it.
- Old-dialect rows never appear in the readiness route set at all, not even as censored, because that query selects routes by the "outcome" event type. Document that alongside the replay limit.

**Required tests**

1. Failing-before test: composed proxy, cascade and store, two user turns, assert a persisted row with event_type "outcome" and state closed_turn on route A. This fails on the current tree.
2. After repair: route A shows pending then closed_turn, route B shows pending only. Assert producer is "cascade", sequence is contiguous, schema version is set.
3. Closer invoked with a time beyond the idle window closes route A once. Invoke twice and assert exactly one closed_final row and one label row.
4. Readiness after closure: closed_final_count one, censored_count one, capability evidence zero, window blocked with the no-capability-evidence blocker. Label result is "excluded" with unverifiable type.
5. Terminal upstream failure with status 503, then a next user turn, then closure. Label is excluded with infrastructure type, never task_capability.
6. Completed status 400 failure. Label must not be task_capability. This test decides whether the third blocker is real.
7. Continuation request path where sticky route differs from decision route. Assert observe-phase outcome rows land on the sticky route, on both the direct and forwarding paths.
8. Restart seeding: pre-populate old-dialect cascade rows on a route, construct a fresh controller, assert new outcome rows do not collide on producer sequence.
9. Fixture tests that assert the old event_type string change only that assertion, and keep their failure evidence checks.

**Out of scope, correctly.** Human correction detection needs touched_paths the cascade never supplies. Verification precedence, replay of old rows, and background closer activation stay open.

**Net.** The repair is the right shape and small. Change the forwarding path to append verbatim, add lineage_hmac to the payload, and settle the empty-candidate default before calling the label preservation claim closed. Readiness after this slice reports a closed count with a blocked window, which is the honest outcome.