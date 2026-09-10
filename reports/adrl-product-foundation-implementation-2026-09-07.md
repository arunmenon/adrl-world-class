# ADRL product foundation: first implementation package

7 September 2026 | Implemented and applied; all required checks passed

The first implementation package makes the existing Messages path an explicit protocol component
and adds a separate product API namespace. It supplies a concrete foundation for the Claude Code,
OpenCode and Codex sequence, without claiming that the additional integrations already work.

## What changed

- **A protocol interface and Messages implementation.** The pipeline delegates parsing,
  classification, rewrite serialization, response observation, native response rendering and its
  boundary interpretation. Original request bytes remain authoritative on the unchanged path.
- **A harness identity interface.** The Claude Code adapter extracts correlation signals; the
  existing resolver still derives session and lineage identities. Repository authority remains
  with the workload gates. Existing resolver entry points remain compatible.
- **Versioned evidence.** New pipeline decision contexts record the profile ID/version, adapter
  ID/version and whether the operation belongs to the advertised endpoint set.
- **A working discovery endpoint.** `GET /adrl/v1/capabilities` describes shipped profiles,
  adapters and limits. It reports distribution capabilities, not runtime enforcement or verified
  provider health.
- **Executable API preview schemas.** The generated OpenAPI document covers discovery, session
  binding/status, typed events, timeline reading and decision explanation. Only discovery has a
  handler. The other product operations return 501, and their payloads cannot fall through to the
  model gateway.
- **A Responses admission decision.** The compatibility spike starts with HTTP streaming and
  client-carried state. Referenced server state, opaque state without custody rules and other
  unimplemented features are admission blockers. Nothing is silently removed to make a request
  appear compatible.

## Validation

The full implementation suite passed: **463 tests in 13.17 seconds**, including the macOS sandbox
tests. The unmodified baseline had 428 tests; this package adds 35 cases. Session identity checks
use recorded outputs from the unmodified implementation with synthetic fixture inputs. Existing
regressions cover byte preservation, streamed events, native errors, pin behavior, routing and
the composed system.

All six repository-required checks passed: Ruff lint, Ruff formatting, strict mypy, pytest,
ledger discipline and configuration checks. The configuration check passed nine checks and
verified the manifest signature; its existing unused EU residency-class limitation remains.
Additional data-inventory validation passed for 215 documented fields. The learning-contract
check passed with zero manifests, which establishes no trained-artifact validation.

The first sandboxed baseline run had two environment-related failures: nested macOS sandbox
execution and a temporary credential probe were denied by the app sandbox. The seven sandbox
tests passed after permission was granted; the final complete suite also ran with that permission.

A post-application smoke check exposed an import cycle masked by the initial test import order.
Native response rendering was moved into the profile package, three fresh-process regressions
were added, and all six checks were rerun. The final applied source also passed standalone
discovery, schema, proxy and composition-root import checks.

The source repository was snapshotted before editing. All 242 original source/config/document
files were unchanged at the final pre-application comparison. Changes were prepared and tested
in an isolated copy because `adrl-core` is outside this task's writable roots. Application used
per-file baseline hashes and verified all 25 changed files afterward. The 233 untouched original
files also match their baseline hashes. No commit or paid provider run was made.

## What this enables next

The next package can implement the authenticated session/event services and reproducible Claude
Code onboarding against explicit schemas. OpenCode then tests whether its lifecycle differences
fit the same engine. Codex still requires a native Responses corpus, state handling, gate/cascade
coverage and real CLI validation before admission.

The gates, feature extraction and cascade still contain Messages assumptions. Unknown provider
endpoints retain legacy forwarding, explicitly outside profile guarantees. Those are remaining
release blockers, not problems that a profile interface alone resolves. API compatibility remains
in preview until two harnesses and two protocols validate it.

## Review files

- [Protocol boundary and implementation limits](/Users/arunmenon/projects/adrl-core/docs/protocol-boundary.md)
- [Generated API preview](/Users/arunmenon/projects/adrl-core/api/adrl-api-v1-preview.json)
- [Responses admission decision](/Users/arunmenon/projects/adrl-core/docs/responses-admission.md)
- [Messages profile record](/Users/arunmenon/projects/adrl-world-class/profiles/anthropic-messages-v1.yaml)
- [Test and change manifest](/Users/arunmenon/projects/adrl-world-class/reports/research/adrl-product-foundation-2026-09-07.json)
