# ADRL product services: implementation and maturity

7 September 2026 | Applied locally; 506 tests and all six required checks passed

ADRL now has a working local integration service around its existing Messages pipeline. A trusted
launcher can bind a registered workload, submit durable observations and read its own decision
history through the public API. Claude Code connection files and two tool-event hooks can be
generated without editing global settings. This is API preview 2, not a stable multi-harness release.

## What is implemented

| Surface | Result |
|---|---|
| Session binding and status | Existing signed launcher assertion authenticates an explicit session and exact registered workload; renewal preserves the same identity |
| Event intake | Encrypted, append-only observations; authenticated producer identity; identical retries return the original acknowledgement; conflicting IDs/sequences fail explicitly |
| Evidence reads | Session-scoped timeline and decision explanations; known dispatch evidence is distinguished from missing evidence |
| Claude Code setup | `adrl connect claude-code` writes private connection, environment and hook files; status, flush and timeline commands are available |
| Tool observations | PostToolUse and PostToolUseFailure map to typed reports; raw tool inputs, outputs and paths are discarded; an encrypted client outbox retains pending deliveries |
| Bound request checks | Conflicting credentials and unadmitted endpoints are rejected before forwarding |

Two defects surfaced while completing these guarantees. ADRL's assertion could previously pass
through the forwarding helper to the gateway; local credential headers are now stripped and
redacted while provider credentials and unchanged request bytes are preserved. Cancellation could
also cancel the future owned by the sole ledger writer after a transaction began. The writer now
owns started transactions through completion and uses SQLite FULL synchronization for commits.

Migration 0003 adds product bindings, encrypted observations and a reference-only timeline index.
It changes no historical decision or event rows. Public observations do not automatically become
internal outcome transitions or verified labels. Harness credentials cannot submit trusted
verification events. Server erasure makes observation envelopes unreadable and the API refuses
to recreate an erased evidence key.

## Evidence and its limits

The full suite passed **506 tests in 16.17 seconds**, adding 43 cases to the 463-test foundation.
All six required checks passed: lint, formatting, strict type checking, tests, ledger discipline
and configuration checks. The data inventory check also passed for 241 fields.

The new tests cover authority failures, cross-session reads/writes, renewal, concurrent retries,
conflicting content, sequence gaps and late delivery, reopening the ledger, erasure, pagination,
unknown endpoints, original byte preservation, credential stripping, outbox retries and writer
cancellation. A separate smoke check started the real composition root on loopback and exercised
the connection CLI, status, synthetic tool-failure ingestion and timeline over real HTTP.

No real Claude Code process or model-provider call was run. The smoke test's gateway destination
was unavailable by construction; its purpose was to test the local integration service. The app
sandbox initially blocked the loopback listener; that check and the required macOS sandbox tests
ran with approved sandbox exceptions. No changes were committed or published.

All 25 changed files were applied after verifying the 258-file source baseline; the 244 untouched
original files still matched. The [validation manifest](research/adrl-product-services-2026-09-07.json)
contains hashes and test results; the [review diff](research/adrl-product-services-2026-09-07.patch)
preserves the implementation changes.

## Maturity

The local session, intake and read services now have **D2 evidence for their tested scope**. The
Messages boundary retains D2 evidence. This does not graduate the full SEM-007 or TRU-001 promise,
establish D3 shadow evidence from real work, or validate another harness. Economic value remains
unmeasured. Architectural acceptance and implementation maturity remain separate.

| Decision | Current implementation record |
|---|---|
| [FND-001](../adr/FND/ADRL-FND-001.md) | Shared product API and native model path; bound versus legacy traffic scope |
| [FND-005](../adr/FND/ADRL-FND-005.md) | Local service tests do not satisfy the two-harness/two-protocol release gate |
| [SEM-002](../adr/SEM/ADRL-SEM-002.md) | Binding uses the existing session HMAC; renewal preserves correlation and state |
| [SEM-007](../adr/SEM/ADRL-SEM-007.md) | Preview 2 services and Claude Code onboarding; Responses and live harness validation remain pending |
| [TRU-001](../adr/TRU/ADRL-TRU-001.md) | Exact registered workload/session authority; no harness-to-verifier privilege promotion |
| [CAS-007](../adr/CAS/ADRL-CAS-007.md) | Native errors for rejected bound traffic; no new model retries |
| [MEM-001](../adr/MEM/ADRL-MEM-001.md) | Separate public intake idempotency, committed acknowledgement and reference-only timeline |
| [MEM-005](../adr/MEM/ADRL-MEM-005.md) | Encrypted caller envelopes, discarded raw hook content and local credential isolation |
| [MEM-006](../adr/MEM/ADRL-MEM-006.md) | Writer survives client cancellation; storage failure never acknowledges an event |
| [MEM-010](../adr/MEM/ADRL-MEM-010.md) | Server erasure covers observation envelopes; separate client-copy lifecycle remains explicit |

## Remaining work and next action

The next milestone is a real Claude Code task with a checked result and reconciled evidence.
Select the pilot repository, approved gateway/model and authorized spend cap first. Resolve or
explicitly constrain the known health, shadow-mode ceiling and legacy-listener gaps before use.
The [setup guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md) gives the concrete
commands and supported scope.

The current limits are material:

- The API accepts root Claude Code Messages bindings on loopback. Separate child binding, automatic
  credential refresh, a resume CLI, OpenCode and Responses remain pending.
- Unbound traffic retains legacy forwarding. Stripping every identity signal can reach that path;
  this package does not create a universally enforcing listener.
- Hook coverage is limited to two tool events. Task closure, compaction, child relationships and
  independently verified results are not automatically captured by these hooks.
- Public observations do not drive the internal outcome/learning lifecycle yet. Timeline order is
  index order, and dispatch records do not expose hidden gateway retries.
- Server erasure does not erase the separate client credential/outbox directory. Its retention and
  erasure procedure must be validated before claiming end-to-end erasure.

After the first working task, run the failure scenarios, prove reuse with OpenCode and complete
Codex/Responses before freezing the product API. Record each course correction against its ADR.
