# Pre-wave critique dispositions

Fable 5.1 pre-review: first tool-based attempt timed out (not accepted as review); a source-embedded retry returned proceed with changes. Original outputs retained.

- Proxy forwarding identity: accepted; now append LedgerEvent verbatim, with failure logging. Direct/forwarded continuation tests retain cascade route/producer/sequence/schema.
- Plan-phase no-ledger fallback: accepted limitation. Production composition has a controller ledger; no-ledger plan persistence remains unsupported and is not claimed.
- 4xx capability leak: inspected `resolve_primary`: empty candidates already return unverifiable. No resolver change needed. Added completed-400 direct test plus HTTP 400 and 503 tests; all exclude capability evidence.
- Failure metadata: canonical constructor receives prior top-level failure_type and diagnostic secondary_type via extra, without duplicate cause candidates.
- Context identity: session and lineage HMACs supplied by RequestContext.
- Unknown success: None, no positive claim; readiness zero capability evidence.
- Restart/legacy: new canonical sequence follows old cascade sequence; legacy event bytes unchanged.

Test adjustment: first candidate expected HTTP 400 to be unverifiable. Actual wire observer marks the HTTP error incomplete, which existing policy maps to infrastructure. Preserved failed log and original test; separate completed-400 regression now exercises the precise reviewer hypothesis. This was a test-expectation correction, not a production policy change.

No retrospective severity removed. RV-01 awaits post-review. Other findings stay open. No formal maturity promotion or autonomous learning claim.

## Post-review corrections, round 1

Identity fields are non-optional SessionId/LineageId NewType(str) in core/types.py and core/ids.py; no optional coercion change is needed. Added an explicitly divergent current decision route at finalization for both direct and forwarded continuation cases. Added legacy-only exclusion, subsequent-turn and explicit episode-event triggers, and dropped-forwarded-event observability. The episode event is test-supplied through the ledger API, not a newly wired harness signal. Pinned idle rule inputs. Documented pre-seeded forwarding scope. Original _append_event performs proxy sequencing, insertion and dropped-event diagnostics only; no write-ahead behavior is lost.

The first regression failed at the empty routes_in_state assertion (before-regression.log), not import/setup. Fable did not receive the log in its first post pass; include it in the recheck. All prior logs and source snapshots remain unchanged.

## Final disposition

Fable recheck: no remaining material blocker for RV-01, subject to final checks-2. Checks-2 passed (922 tests, 8 engine skips, eleven checks) on the exact review snapshot. RV-01 verified-fixed for the specified path. Retain the nonblocking dropped-log diagnostic parity note; do not reopen runtime just for it. Other retrospective findings unchanged.
