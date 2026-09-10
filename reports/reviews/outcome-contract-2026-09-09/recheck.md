**Verdict: RV-01 is repaired for its stated scope. No material blockers remain. Final resolution is contingent on the concurrent full checks-2 run being green, which I have not seen.** This recheck is from reading the supplied source, tests, dispositions and logs. I ran nothing.

## Blockers from the original critique

- **None coercion: withdrawn.** RequestContext declares session and lineage as non-optional SessionId and LineageId in `src/adrl/core/types.py`. Both are NewType over str in `src/adrl/core/ids.py`, and the identity functions always return hex digests. The str() wrap is a no-op. No guard or None test is needed. This is a note, not a blocker.

- **Route divergence on continuation: demonstrated.** The parametrised continuation test now replaces the current decision's route id at the finalize boundary while the plan keeps the sticky route. The closed_turn is asserted to land on the sticky route with cascade producer and sequence 2, on both direct and forwarded paths. Under the old re-keying, the row would have landed on the altered decision route, so the test discriminates. The divergence is induced by patching rather than produced by a real continuation, and the test comment says so. That is adequate for the invariant being claimed.

## Evidence gaps from the original critique

- **Pre-seeded forwarding scope: closed.** The contract doc now states forwarding is tested with a pre-seeded counter and does not qualify cold-start forwarding. The idempotency-key collision on a no-ledger restart remains an accepted, documented limitation.

- **Inert TypeError guard: closed.** The dropped-forwarded-event test asserts that event_dropped appears and finalize_failed does not. Since the same forwarding lines execute, this shows the names resolve and the pipeline ledger is the facade. It tests the pipeline's handling of a False return, not the store's real duplicate-key behaviour. The original helper also treats False as dropped, so the assumption is consistent with existing code.

- **Idle timing: closed.** The composed test pins subsequent_turns to 100 and idle_minutes to 30, then scans one day ahead. Only idle can fire.

- **Bypassed helper: closed.** The supplied helper source performs proxy sequencing, append and dropped diagnostics only. The forwarding path omits the degraded flag from its dropped log. That is a diagnostic parity nit, not a loss of behaviour.

## Missing acceptance tests

1. **Legacy exclusion: landed.** A legacy-only closed_turn route yields empty routes_in_state, zero closed_final and censored counts, and a None projection state.
2. **Subsequent-turns and episode-boundary: landed with a scope caveat.** The subsequent-turns case sends a third user turn, so at least one turn post-dates the closed_turn regardless of clock resolution. The episode case writes the lineage event directly through the store. The dispositions correctly state this is a test-supplied signal, not a wired harness producer. The Closer trigger works; production emission of that event is not evidenced and is not claimed.
3. **Route divergence: landed** on both paths, as above.
4. **None identity: not applicable**, as above.
5. **Dropped forwarded event: landed**, with the caveat noted.
6. **Before-regression log: confirmed.** The failure is at the routes_in_state assertion in `tests/integration/e2e/test_outcome_contract.py`, with components built and both gate outcomes logged. It is not an import or fixture error. An empty list where the first route was expected is exactly the hypothesis that pre-fix rows never reached the canonical consumer.

## Remaining notes, none blocking

- **Test-expectation correction on HTTP 400.** The wire observer marks the HTTP error incomplete, which policy maps to infrastructure. The parametrised test now expects infrastructure for both 503 and 400, and the completed-400 direct test covers the unverifiable hypothesis. Both are consistent with the supplied resolver disposition. No production policy changed.
- **Proxy rows on the induced divergence** are written to the fake route and are not asserted. That is outside this finding.
- **Cold-start forwarding without ledger** remains unsupported and documented.

## Scoped verdict

Record RV-01 as repaired once checks-2 completes without failures. Readiness reports one closed_final, one censored, zero capability evidence and a blocked window. That is the correct end state for this slice. Nothing here qualifies LRN-001, promotes maturity, or claims a complete learning loop. Other retrospective findings remain open and are unaffected.