# W3.2b2d2 next: diagnose lost create receipt before renewed engine qualification

Prepared 8 September 2026 after implementation and two bounded runtime engine invocations.
Read the [runtime report](../adrl-w3-isolated-launch-2026-09-08.md),
[evidence](../research/adrl-w3-isolated-launch-2026-09-08.json), both AGENTS.md and current state.
Do not restart completed research or treat the prototype as a completed W3 launch backend.

## Current evidence and closed allowance

Runtime now contains pinned fixture-only execution, permanent launch denial, authenticated
claim/ack/seal/stop/discard history, serialized recovery and retained uncertainty. Schema 12
preserves old records/fences; the API remains preview 4. Unit fault cases cover these behaviors.
Real-engine run 1: three passed, one final assertion expected the wrong exception after successful
erasure cleanup. That assertion was corrected. Run 2: three passed, while its first stopped-create
call lost the original response before runtime launch. No third engine run occurred.

The second failure has no retained underlying exception type. A timeout under the two-second
transport budget is plausible, not established. The selected daemon did create a never-started
resource, but no full ID reached the original client receipt logger. Do not infer that a create
timeout means no resource exists or that a discovered name restores runtime binding authority.

Eight creates were issued; seven client receipts were confirmed absent. One never-started
candidate matching the original unique intent/name/image/creation interval and every declared
control was removed non-force through a documented one-off operator maintenance exception.
The image was removed too. The original uncertainty remains; no runtime adoption was added.
The first failed case did not halt pytest, so three later cases ran despite the intended stop
rule. A tested fixture teardown guard now stops on unreceipted creates and persists timestamp,
request body, error type and bounded error code. Further engine runs must also use maxfail=1.

The preceding two-focused-run/16-container/one-image allowance is closed. Unused numerical
headroom does not authorize another invocation or image import. Current owned resources: zero.

## First bounded deliverable: offline diagnosis and a reviewable correction

1. Inspect retained executed source snapshots, create-issued/receipt records, stage timestamps,
   candidate inspection and the transport exception handling. State what is proved versus inferred.
2. Reproduce create-response loss with the existing local Unix-socket fixture, including response
   timeout, malformed response, response-size/deadline refusal and delayed acknowledgement.
   Preserve bounded cause classification without raw daemon messages, paths or task data in the
   product ledger. Verify the new test stop guard prevents a later daemon case after uncertainty.
3. Review the coupling of stopped preparation and active execution I/O budgets. D1 originally
   permitted longer stopped-create I/O; the launch transport needs <=2 seconds. Decide whether
   distinct explicitly versioned transport profiles are appropriate, based on reproducible
   evidence. Do not simply increase every timeout or widen an identity comparison to pass a test.
4. Preserve one-shot creation/launch and permanent fences under lost replies. If improved original
   response custody is proposed, define exactly who receives/persists the original daemon ID,
   what happens if that receipt never arrives and how worker draining/owner death is handled.
   The one-off operator cleanup exception is not an automatic product adoption rule.
5. Freeze the concrete correction, data inventory and fault cases before runtime changes. Run
   all eleven checks for changes. Preserve all failed/cancelled check attempts and source hashes.

Only after the identified cause or a concrete supported correction is ready may a new finite
engine packet be frozen. Start with stopped-create/receipt/cleanup alone, no active workload;
record every issue/return and stop at first uncertainty. Then separately qualify the current
normal launch/stop path and four runtime fault cases. No unbounded retry loop, model call, pull,
install, network, real payload, daemon settings, new spending or broad cleanup. One writer,
no agents, at most three failed repair attempts per bounded task.

## Completion and later gates

Synchronize owning OPS-001, MEM-001/002/003/005/010, SAF-007 and TRU-001, index, four buckets,
changelog, journey and state. Preserve every prior decision and all 77 status/maturity fields.
Keep runtime implementation, offline testing, engine observations and independent qualification
separate. Full W3.2b2d2/B2/B3/W3 remain open until their acceptance criteria actually pass.

Later: active-copy/lease erasure, safe extraction and exact stop/capture association, verifier and
operator CLI/timeline, then a real Claude Code profile and demonstration. No new user decision
blocks this offline diagnosis. Any proposal to change product ownership/trust authority must be
made concrete in the owning ADRs and assessed against the roadmap's applicable decision gates.

## Later disposition: receipt correction and bounded d2 validation, 2026-09-08

The [current report](../adrl-w3-transport-receipts-2026-09-08.md) records execution v2, separate preparation/active I/O,
26 new offline faults and a fresh passing engine packet. Final combined results: 895 passed,
zero skipped, all eleven checks, 316 stable source inputs. Thirteen original IDs and exact
absence confirmations; the image is removed. No cleanup exception in the fresh packet.
Historical create cause remains unknown; previous observations and allowances stay preserved.
This closes the bounded d2 pinned synthetic launch/recovery slice, not full B2/B3/W3 or any
ADR grade. Continue [active-copy custody](w3-active-copy-custody.md); no new Docker allowance.
