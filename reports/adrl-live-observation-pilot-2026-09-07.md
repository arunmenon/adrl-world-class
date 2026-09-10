# ADRL: the first live subscription pilot

**Later implementation, 2026-09-07:** [independent session verification](adrl-session-verification-2026-09-07.md)
is now applied in API preview 4, with 532 passing tests. Two verifier jobs each passed eight
checks on the existing repaired task and added receipts to a copied timeline. Earlier figures
and outstanding-work lists below describe the original report date/stage; the linked update
contains the current scope and next steps.

7 September 2026 | Applied implementation and two real Claude Code sessions

**ADRL has now observed a real coding task through its product API while Claude Code used your Max subscription.** The run captured every executed tool call in the checked trace, including a failed test run. We also completed a concrete course-correction cycle: an initially plausible fix passed the existing tests, failed independent compatibility checks, and was repaired successfully.

This moves the project beyond offline-only integration evidence. Model routing and privacy enforcement still need their own live validation. An observation connection is useful, but it does not put ADRL in control of the model request.

## What we ran

The work used an isolated subset of dataset-validator: one user, one repository, one task family, two engineered sessions on 7 September. The original repository was not edited. This is a feasibility exercise, not a representative sample of development work or an evaluation of a routing policy.

| Run | Claude Code | Assignment | Independent result | Wall time | Reported API-equivalent cost |
|---|---|---|---|---|---|
| Native baseline | 2.1.260 | Fix two template-rendering failures | 4 existing tests passed; review rejected the fix because formatter compatibility regressed | 54.1 seconds | $0.1172 |
| ADRL observation and repair | 2.1.263 | Correct the reviewed fix with explicit compatibility requirements | All 8 tests passed; literal JSON output and the diff were checked separately | 96.9 seconds | $0.1749 |

Both sessions selected `claude-sonnet-5` at high effort. Claude also reported `claude-haiku-4-5-20251001` usage. Those are harness-reported model identities and usage figures, not provider endpoint receipts. Claude reported no overage use in either trace. The combined $0.2921 figure is an API-equivalent estimate, not an additional subscription charge or invoice reconciliation.

The installed CLI updated between runs. Together with the new feedback, changed starting code and expanded tests, that makes these runs unsuitable for a latency, cost or instrumentation-overhead comparison. Pin the executable version as well as the model and verifier for the next matched experiment. Neither run used a local model.

The earlier authentication failure was an environment artifact: sandboxed status could not see the saved macOS login. A status check with normal access confirmed the native Claude Max account. Its credentials stayed inside Claude Code; ADRL used a separate local workload assertion.

## What the first fix taught us

The original templates used literal JSON braces that Python's formatter tried to interpret as placeholders. Claude initially replaced the formatter with a simpler regular expression. This fixed the examples covered by the four existing tests, but broke previously valid behavior:

- Escaped braces substituted a value that should have stayed literal.
- A format such as `{score:.1f}` remained unrendered.
- Follow-up verification also required a missing formatted variable to raise an error.

The repair restored Python's native formatter and escaped the literal braces in the two templates. The four original tests and four compatibility tests now pass. Tests and task instructions were unchanged by the repair agent, and a separate output inspection confirmed that JSON examples and supplied values survive rendering.

The [reviewed task patch](research/dataset-validator-pilot-fix-2026-09-07.patch) is preserved for inspection. It is applied only in the [pilot copy](/private/tmp/adrl-claude-pilot-9x3n90aj/run-02-observe-repair), not in the original dataset-validator checkout. This is evidence for keeping independent verification separate from a harness's success message; it is not evidence that one model family is unreliable.

## What ADRL captured

| Observation measure | Result and denominator |
|---|---|
| Executed tool calls in the instrumented trace | 18 |
| Corresponding ADRL events | 18 of 18; tool references reconciled individually |
| Reported tool outcomes | 17 completed, 1 failed |
| Hook command failures | 0 of 18 |
| Undelivered outbox events after flush | 0 |
| Model requests received by ADRL | 0, as intended for observation mode |
| ADRL routing decisions created | 0 |
| Trusted learning labels created | 0 |

Both PostToolUse and PostToolUseFailure were exercised by real Claude Code behavior. The failed event was the pre-repair test run. The timeline's final sequence is 18. The local ADRL assertion was absent from Claude's captured stream and generated model environment. ADRL's hook mapper discards raw tool input, output and error text; its outbox stores encrypted typed observations.

Coverage is limited to this one instrumented session. Permission denials, pre-execution validation, compaction, child sessions, provider retries and complete model egress are not covered by this result. The native baseline had one denied shell-command variant; the observation run had no permission denials. A successful tool call is not automatically an accepted engineering result.

Outcome verification was performed outside the public event API. Public harness credentials still cannot submit trusted verification, and these experiment results were not promoted into the learning corpus. Both sessions are excluded from organic policy-quality and savings metrics. Confidence intervals, routing request-class denominators and counterfactual policy effects are unavailable; there were zero matched policy pairs.

## What changed in the product

API preview 3 adds `integration_mode`, with `gateway` and `observe` values. The mode is part of the immutable session binding. A session cannot be relabelled between the two modes.

```bash
python -m adrl.cli.main connect claude-code --mode observe \
  --repo "$ADRL_PILOT_REPO" --output "$ADRL_CONNECTION" \
  --server http://127.0.0.1:8788
```

Observation setup emits the session identifier and local hook settings without installing an Anthropic base URL or ADRL credential in model headers. The caller must still check native Claude configuration for stale gateway overrides. Session status explicitly marks model interception, content inspection, dispatch enforcement and served destination as unavailable. Requests sent to ADRL's model path under that observation binding are rejected.

Migration 0004 adds the binding mode; existing bindings retain gateway semantics. Preview-3 session clients must be upgraded together. Existing preview-2 encrypted event envelopes remain readable and deliverable without changing their identity. The data-inventory checker now also discovers columns added by migration; a regression test proves that omitting the new field from the inventory fails the check.

The applied package changes 15 files: 12 existing files and 3 additions. The other 257 files in the captured source baseline were preserved. **All 511 tests and all six required checks passed.** The inventory check covers 242 fields. The [implementation diff](research/adrl-observation-mode-2026-09-07.patch) and [evidence manifest](research/adrl-live-observation-pilot-2026-09-07.json) record source hashes, validation and run results. Work remains uncommitted.

## Maturity and decisions

The model path and general product services retain their scoped D2 evidence. There is now one bounded live observation result, not a general D3 or D4 graduation. The distribution capability response remains conservative; it does not advertise full harness qualification from one hook pilot. FND-005's two-harness/two-protocol release gate remains unmet.

The register records the result under FND-005 (measured scope), SEM-007 (integration coverage), TRU-001 (local binding authority), MEM-001 (durable mode and event history), and EVL-008 (denominators and exclusions). Architectural statuses and the stable IDs remain unchanged. No routing threshold, privacy policy or learned authority changed.

Open blockers remain: live gateway interception and control tests; unbound legacy forwarding; gateway health and shadow-ceiling gaps; automatic trusted outcome capture; child/compaction coverage; client-side retention lifecycle; OpenCode reuse; and an admitted Responses runtime. The observation pilot does not remove these blockers.

## Next concrete work

1. Add independent task-result capture with its own authority and snapshot/version references, so verification can join the timeline without trusting a harness's success claim.
2. Run a small set of new tasks with the same pinned Claude executable, model, effort and verifier. Check delivery and false-success cases before drawing quality conclusions.
3. Exercise disconnection/retry and restart during actual harness work, then test the same observation API through OpenCode.
4. Resolve the named gateway blockers and configure approved provider access before testing local routing, secret gating or economic improvements.

The pilot service and Claude sessions started for this exercise have stopped. The isolated evidence and working copies remain available locally; no production service was deployed.
