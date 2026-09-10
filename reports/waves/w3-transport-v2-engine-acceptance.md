# Fresh bounded engine acceptance for execution transport v2

Frozen 8 September 2026 after all eleven offline checks passed: 887 tests, eight explicit engine
skips, 316 stable source inputs. The [transport correction](w3-create-receipt-transport-v2.md)
has reproducible offline evidence; the historical missing receipt still has an unknown cause.
This is a new finite packet. Every previous engine allowance remains closed.

## Fixed scope and sequence

Use the already installed explicit local Docker socket and the same pinned 27.3.1/API 1.47 Linux
arm64 engine/capability profile. Verify the retained two-entry synthetic tar and its binary hash,
import it once with a unique tag/label, and verify the exact single-layer image. No pulls, builds,
installs, daemon changes, host mounts, network, real task payload, credentials, model calls,
new spending, live routing or commits. One writer. No agents or independent-review claim.

Maximum one image import and thirteen container creates; no retry or repair in this packet.
Run sequentially, advancing only after success and exact original-receipt absence confirmations:

1. One stopped-ownership normal case: original create receipt, full validation and non-force
   cleanup. No start. One invocation, one container.
2. Four launch cases: normal start/stop then discard; lost start acknowledgement; active content-
   key erasure; owner process death after startup and authenticated reopened discard. One
   invocation, four containers. Permanent fences, no second launch, false outcome eligibility.
3. One combined eleven-check invocation with all eight opt-in engine cases enabled. Eight more
   containers, four synthetic starts. This broadens the validation only after the correction and
   narrower real-engine checks pass. The ordinary suite remains source-hash checked.

Use PYTEST_ADDOPTS=--maxfail=1 for every invocation, including the combined runner, plus the
existing tested teardown halt after an original create has no receipt. Each stage has a durable
issued marker, is never reissued, records its result and verifies exact cumulative create count.
Any failed assertion, unreceipted create, mismatched identity, source drift or incomplete cleanup
stops the packet. Unused headroom does not permit another invocation. Keep all failed evidence.

## Ownership and timing

The original fixture wrapper fsyncs synthetic intent/body/time before each create and fsyncs the
original full ID immediately on return. It records a closed transport cause on uncertainty. Only
that original receipt grants fixture cleanup custody. No lookup/name/label adoption and no new
operator cleanup exception are included. Runtime discard still requires authenticated history.
Confirm every exact originally receipted ID absent, then remove the one uniquely tagged/labelled
image non-force and confirm absence. A lost original receipt keeps its uncertainty; do not infer
absence or invent a binding.

Stopped I/O retains ResourcePolicy's ten-second default; active I/O uses execution v2's at-most-
two-second separate view (a tighter inherited bound remains tighter). Response cap 131072 bytes,
ledger wait fifteen seconds, image import fifteen seconds, owner subprocess five seconds,
fixture independent exit seven seconds. Per-phase timeouts and elapsed-response rejection are
not hard wall-clock scheduling guarantees. Stage subprocess timeout is 240 seconds, with
combined checks retaining their own bounded process-group timeout handling.

Freeze current source, contract and exact orchestration script hashes before import. Verify them
before every stage. Preserve dirty source and prior records. On completion synchronize eight
owning ADRs, four buckets, index/changelog/journey/state and source/check/cleanup evidence.
Passing this packet establishes only current pinned synthetic-engine observations. Active-copy
erasure, exact safe output capture, real harness qualification, independent review, full W3 and
all architectural status/maturity promotions remain outside this packet.

## Closed with passing evidence, 2026-09-08

All three prescribed stages passed without a retry: 1 stopped case, 4 launch cases, then
895 tests/zero skips and all eleven combined checks. All thirteen original IDs have exact
absence confirmations and the single image is removed. Eight synthetic starts; no original
receipt loss, operator exception or source drift. The allowance is closed and grants no further
invocation/import. See [report](../adrl-w3-transport-receipts-2026-09-08.md) and [evidence](../research/adrl-w3-transport-receipts-2026-09-08.json).
