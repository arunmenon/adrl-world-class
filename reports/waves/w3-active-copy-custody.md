# W3.2b2e next: account for active plaintext copies and interrupted cleanup

Prepared 8 September 2026. Enter only after the execution transport v2 packet has passed and all
of its fixtures/image are confirmed absent in the execution state. Read both AGENTS.md, the
journey, current state and the latest evidence before editing. Do not restart completed Docker
experiments. No engine mutation is authorized by this packet.

## Why this comes next

The internal backend can establish who created and started a pinned synthetic fixture and how
it was stopped or discarded. That does not explain every temporary copy of task content. A
future verifier will need decrypted workspace material; cancellation, erasure or a dead owner
must not leave unaccounted copies or turn unknown cleanup into a success receipt.

First map the current implementation, including operator captures, materialization, verifier
workspace copies, archive staging, key access/revocation and container-layer retention. Distinguish
already implemented encrypted storage, temporary plaintext, content remaining in process memory,
physical blocks/backups and planned real-harness data. Do not invent an erasure guarantee for
storage outside ADRL's control.

## First bounded deliverable

1. Produce a source-linked copy/custodian/lifetime/cleanup table and a concrete counterexample
   from the existing offline tests or a new bounded synthetic fault. Confirm which historical
   gaps still exist and avoid duplicating working cleanup.
2. Freeze the smallest useful lease/custody contract before runtime edits: exact owned root,
   authority and versioned capacity/size/time bounds, admission ordering, erasure denial,
   independent recovery responsibility after owner death, safe path validation and append-only
   audit behavior. State what happens if cleanup or its acknowledgement fails. An old path,
   name, PID or incomplete record must not grant arbitrary deletion authority.
3. If the correction fits existing authorized scope, implement it with synthetic bytes and local
   temporary fixtures. Preserve unrelated work and verify a backup. If it changes the trust or
   retention authority governed by a decision queue item, make the proposal concrete and keep
   dependent exposure blocked while continuing independent source review or offline fault work.

Initial owners to inspect: MEM-001/002/003/005/010, SAF-007 and TRU-001, with OPS-001 for concurrent
custody. Confirm actual ownership before any code change; add secondary ADRs only when real.
No architectural status or maturity changes are authorized. Prior wording/research remains.

## Acceptance and guardrails

For the chosen bounded implementation, cover normal use/cleanup, exceptions, repeated cancellation,
owner process death, erasure before/during materialization, concurrent/reopened recovery, quota
exhaustion, missing/corrupt history and unsafe path substitution. Assert no key recreation, no
cross-session access and no success claim after uncertain cleanup. Independent cleanup must not
require decrypting erased content. Document memory, scheduling, host-administrator, snapshot and
physical-block limitations separately.

No real repository payload, model call, new spend, image pull/import, install, daemon change,
network/credential exposure, live routing, deployment, commit, fence release, automatic learning
or independent-review claim. One writer, no agents, at most three slices and three failed repair
attempts per bounded task; no unchanged retries. Full W3/B2/B3, exact capture and learning remain
open until their own criteria pass. The synthetic launch result is not a real-harness guarantee.

Run the module map and all eleven checks for runtime changes, with stable source hashes and the
updated data inventory. Synchronize owning ADRs, index, buckets, changelog, journey and state;
verify local links, all 77 index rows, preserved maturity/status and unrelated files. Documentation
alone may reuse checks only if their tested runtime hashes still match.

## Subsequent steps

Safe bounded extraction and exact stop/capture association come after copy custody. Then the
verifier and operator timeline/CLI can identify the exact captured output. A real Claude Code
profile still needs explicit image, network, credential and retention dispositions; independent
reviewers and the roadmap's later policy decisions remain human gates. No new user input blocks
this first offline inventory and contract work.
