# Wave 3: creation, launch and recovery now pass the bounded engine checks

8 September 2026. **The synthetic launch/recovery slice is complete. We are still in Wave 3:**
ADRL can now demonstrate this narrow lifecycle on the selected local Docker engine, with its
failure controls intact. The next step is accounting for temporary plaintext copies before
safe task-output capture. This is not yet a real Claude Code run through the isolated backend.

## The course correction, in plain language

Imagine asking a workshop to prepare a workbench, then supervising the work done on it. Preparing
the bench and supervising an active job need different response budgets. Our first implementation
forced both to use the short active-work timeout. If preparation took longer, ADRL could stop
waiting even though the workbench had already been created.

We reproduced exactly that mechanism offline: a reply delayed by 2.25 seconds was lost with a
two-second budget; the existing ten-second preparation budget received and validated the original
ID. Execution policy v2 now gives active requests a separate, tighter client. Creating the stopped
resource keeps its existing preparation budget. Neither policy's maximum was increased.

The earlier real failure still has an unknown underlying cause. Its 2.76-second batch-to-creation
interval includes test setup and cannot prove a request timeout. Passing the corrected workflow
does not retrospectively prove the hypothesis. The earlier failure and cleanup exception remain
in the [historical report](adrl-w3-isolated-launch-2026-09-08.md).

## What changed and what stayed protected

| Area | Current implemented behavior | Practical significance |
|---|---|---|
| Creation receipt | Original client receives the full ID; validation still precedes binding | A slower legitimate reply can complete within the existing preparation budget |
| Active execution | Separate versioned I/O bound, at most two seconds, including inspection and recovery | Preparation no longer forces active supervision to wait ten seconds |
| Missing reply | The attempt stays fenced and unbound; no second create or name adoption | Uncertainty cannot accidentally grant ownership or another launch |
| Diagnosis | Closed transport-cause codes in transient errors/private fixture logs; raw messages suppressed | A future failure can identify the transport category without new task data in the ledger |
| Older records | V1 hashes and coupled admission meaning are retained; recovery reads the event's policy | Opening old history with the new coordinator does not rewrite or silently reinterpret it |
| Cancellation | Original create worker drains and may retain only its genuine returned binding | Cancelling the caller is not mistaken for cancelling the daemon's creation |

These are HTTP phase timeouts with elapsed-response rejection, not a hard wall-clock watchdog
for a whole sequence. The fixed synthetic fixture still has its own independent lifetime.
Permanent launch/workspace fences, strict engine/configuration checks and false exact-close and
learning flags remain. No public API, routing authority or privacy-pin release was added.

## Evidence from this run

All checks passed without a failed repair or an unchanged retry in this packet.

| Check | Result |
|---|---|
| Initial focused offline run | 78 passed; the final full suite also includes the subsequently added empty-response deadline case |
| Full offline checks | 887 passed, eight opt-in Docker cases skipped; all eleven checks passed |
| First fresh Docker stage | One stopped create/receipt/cleanup case passed; no launch |
| Second Docker stage | All four launch cases passed: normal stop, lost start acknowledgement, active key erasure, owner death |
| Final full checks with Docker enabled | **895 passed, zero skipped; all eleven checks passed** |
| Source attribution | 316 declared source inputs stable; the full Docker run used the same source as the offline run |
| Cleanup | 13 creates, 13 original ID receipts and 13 exact absence confirmations; one imported image removed |

There are 26 new offline cases. The difference between 887 and 895 is the eight existing opt-in
engine cases being enabled, not eight more new tests. Across the fresh engine stages, eight
synthetic workloads started; none used a real task, harness credential or model. Fail-fast and
the unreceipted-create teardown guard were enabled. No retry, missing receipt, operator cleanup
exception, image pull, installation, daemon change, network exposure, new paid usage, commit or
deployment occurred. The finite thirteen-create/one-image allowance is now closed.

The data inventory checks 371 fields and documents 381 entries, adding the versioned active I/O
bound. Schema 12, public API preview 4 and the 111-module map to 74 of 77 ADRs are unchanged.

## What this means for maturity and RSI

This is useful operational progress: the current implementation now survives its declared
synthetic lifecycle and failure cases on the selected engine. We can move past the repeated
creation/launch qualification gate to the next storage-custody problem.

It does **not** raise all ADR maturity scores. Eight owning records now link this narrower
implementation and evidence; all 77 architectural status/maturity fields and prior wording are
preserved. This run had implementer self-review, not an independent reviewer. Real-harness
qualification, exact task-close evidence, full W3/B2/B3 and production readiness remain open.

The adaptive loop here is concrete: record a failure, distinguish facts from hypotheses,
reproduce a mechanism, change a versioned policy, test faults, qualify the current workflow,
and write the result back to the decision ledger. This is engineering course correction.
It is not autonomous policy promotion, model training or demonstrated better routing quality.

## Next

The [next packet](waves/w3-active-copy-custody.md) maps where decrypted task copies can exist,
who owns them and how cleanup behaves after cancellation, erasure or owner death. It begins
with offline source review and synthetic faults; no new Docker experiment is authorized there.
After that come safe extraction, durable association between stopping and captured output,
verifier/timeline tooling, then an explicitly scoped real Claude Code profile. A second harness
will build on the shared contracts rather than receive separate core decision logic.

No user decision currently blocks that offline work. Independent reviewers and the real-harness
image/network/credential/retention choices remain later human gates.

See the [journey](adrl-implementation-journey.md), [checks/source/cleanup evidence](research/adrl-w3-transport-receipts-2026-09-08.json),
[implementation diff](research/adrl-w3-transport-receipts-2026-09-08.patch), [frozen correction](waves/w3-create-receipt-transport-v2.md)
and [closed engine packet](waves/w3-transport-v2-engine-acceptance.md).
