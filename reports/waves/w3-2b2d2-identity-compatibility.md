# W3.2b2d2 next: Resolve execution identity compatibility

Prepared 8 September 2026 after two failed bounded launch-recovery research runs. Both exact
fixture containers and the single imported image were removed. The previous two-run allowance
is closed; this packet is a reassessment with an identified cause, not another unchanged retry.
Runtime remains at 812 tests, schema 11, API preview 4 and 306 verified declared inputs.

## The concrete issue

The retained before/after inspections in the second run differ only in
`HostConfig.OomKillDisable`: false before start, null after start. Every explicitly requested
control matched. The selected Docker 27.3.1/API 1.47/Linux/cgroup-v2 engine reports
`OomKillDisable=false`. Moby's Unix configuration code supplies a false default, then clears
the field during resource validation when the kernel does not support it. The first repair's
empty-PortBindings hypothesis was not sufficient and is not a qualified runtime exception.

Do not weaken d1's original stopped-resource digest or change its no-start contract. Define
a separate versioned execution identity projection and bind it to the authenticated original
raw record plus the selected engine/capability profile. Restrict the candidate normalization
to false/null for this one unsupported field; true, missing/malformed evidence, unknown profile,
engine/capability change and all other security/configuration drift must refuse admission.

## First deliverable, before any daemon mutation

1. Inspect the current runtime and retained raw inspections/source references from the
   [d2 evidence](../research/adrl-w3-2b2d2-launch-contract-2026-09-08.json).
2. Freeze a small data/projection contract, comparison algorithm and explicit negative cases.
   Use offline fixtures derived from the recorded pair, preserve their origin and add altered
   image/command/creation time/engine/ports/mounts/capabilities/seccomp/resource-limit controls.
3. Validate the rule and data inventory without exposing start. Do not add an unused interface
   and mark the entire backend done. If runtime code changes, identify its real caller/scope,
   run all eleven checks and synchronize the owning ADRs before closing that slice.
4. Review the research driver: persist initial state and intermediate case results before
   cleanup, preserve primary failure separately from cleanup failure, and account for create
   acknowledgement loss. These two runs lost completed case reporting when cleanup raised.

## Subsequent bounded engine validation

Only after the offline identity cases pass, freeze a new finite resource/time allowance and
changed driver hash. Start with one create/start/inspect/stop/inspect case proving the exact
expected transformation on the pinned engine, with no other comparison exceptions. Account
for its original receipt and cleanup. Then, within that explicitly frozen allowance, complete
the six outstanding launch/stop/discard negative controls. Stop on any new mismatch or unresolved
cleanup; do not widen normalization to make an unexplained case pass.

Use only self-authored independently terminating fixtures, existing local engine, explicit
seccomp and no network/host mounts/pulls/installs/model calls/real payloads. Nothing here grants
production forced deletion or arbitrary execution. At most three repair cycles and one writer;
the previous research batch is not rerun unchanged. Preserve dirty work and failed evidence.

## What follows

After identity compatibility and the outstanding engine cases pass, implement the
[isolated execution contract v1](w3-isolated-execution-contract-v1.md) in a reviewable bounded
slice: permanent one-shot denial, authenticated claim/seal, known-launch stopping and explicit
ambiguous-launch abort. Keep old histories/fences, scope all metadata, and retain false exact-close
and learning eligibility. Active/plaintext erasure, B3 output capture and real-harness profiles
remain later gates. No maturity/status promotion or independent-review claim is authorized.

## Current disposition after changed experiment, 2026-09-08

The [new evidence](../research/adrl-w3-execution-identity-2026-09-08.json) now records 101 passing offline
research cases and seven accepted engine observations: one identity case and all six lifecycle
cases. The narrow unsupported OOM rule passed; no other normalization was required. Manual
restart changed StartedAt while RestartCount stayed zero. All seven containers and the one
image are absent. The old two failed runs remain preserved and their allowance remains closed.
The new seven-container/two-stage allowance is also closed after successful completion.

Earlier statements in this packet about uncompleted research describe its preparation state.
This disposition advances research readiness only: runtime launch/seal/recovery and the permanent
marker are still unimplemented. Continue the [runtime packet](w3-isolated-launch-runtime.md).
No public API, runtime source, status/maturity, exact-close or learning eligibility changes.
