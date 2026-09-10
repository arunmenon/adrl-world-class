# ADRL-TRU-003 - Egress anchoring (Proposed)

| Field | Value |
|---|---|
| Bucket | TRU - Trust, Residency and Egress |
| Status | Proposed 2026-09-03 (new, from external review) |
| Maturity | D0 Design, review recommends D0 Design (the 2026-09-02 implementation has a hash chain, a manual checkpoint method signed with the development manifest key, and a verifier that ignores signatures) |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8 |
| Related decisions | SAF-009 (superseded), SAF-002, FND-004, MEM-001, MEM-006, TRU-001, TRU-002, OPS (key custody, anchoring endpoint) |
| Open questions | Q5, Q7 |

## Decision

The egress ledger of SAF-009 is anchored outside the developer's machine and outside every key the developer's machine holds: checkpoints are produced automatically every N entries or T minutes, signed under a checkpoint key that is separate from the manifest and identity keys and is provisioned by OPS, shipped to an off-device anchor that returns an acknowledgement recorded in the ledger, and verified by a tool that checks signatures and anchors, not only the hash chain; development keys are refused unless a development flag is set; and the answer to "did this lineage's content leave the machine?" is computed from served-deployment receipts (TRU-002), never from a rung name.

1. *Separate key*: the checkpoint signing key is distinct from the manifest-signing key and from any HMAC or session key; its private half is provisioned per device by OPS and is never in the repository. A key with a development marker is accepted only when `ADRL_DEV_KEYS=1`, and the ledger records that the process ran with development keys.
2. *Automatic checkpoints*: every `egress_checkpoint_every` entries or `egress_checkpoint_seconds`, whichever first, and at clean shutdown. A missed checkpoint window is a `checkpoint_overdue` telemetry event.
3. *Off-device anchoring*: each checkpoint is shipped to the anchor endpoint (Q7: the gateway may host it) and the acknowledgement (anchor id, timestamp, signature) is appended; shipments queue offline and an unacknowledged backlog over a bound is an OPS alert, not a block.
4. *Verifier*: `adrl audit verify` checks chain integrity, checkpoint signatures against the externally pinned public key, and anchor acknowledgements; it reports the last anchored sequence so an auditor knows which suffix is unanchored.
5. *Receipt-based answer*: `lineage_left_machine` and `adrl audit --lineage` consult the served-deployment receipt's `trust_zone` and `api_base` host, not `destination_rung`.
6. SAF-009's schema, write-ahead rule, content-free rule and scope exclusion are retained unchanged.

## Context and rationale

SAF-009 asked for a ledger whose deletion or edit is "detectable by an auditor who holds only the checkpoints". That sentence carries three requirements the first implementation missed: the checkpoints must exist without anyone remembering to call a method, the auditor must hold them somewhere the logger cannot reach, and the key that signs them must be one the logger cannot use to re-sign a forged history. The implementation had a manual checkpoint method, no shipment, a verifier that compared digests but not signatures, and a checkpoint key that was the committed development manifest key, loaded unconditionally in the composition root. That is not evidence of a leaked production secret; it is the collapse of key separation, which makes the whole audit trail worthless to an auditor. Crosby and Wallach's construction assumes an untrusted logger; every clause here restores that assumption.

## Adversarial review (2026-09-03)

### Steelman
This is the difference between a log and an audit trail. Every SAF promise (pin coverage, fail-open accounting, human release, operator bypass) lands in this ledger; if the ledger can be rewritten by the person it constrains, none of the promises can be checked. The additions are small (a second key, a timer, a queue, a signature check) and turn SAF-009 from a data structure into a control.

### Attacks (self-applied)
1. **The anchor endpoint is egress.** Mitigation: checkpoints are content-free (SAF-009 clause 3), the endpoint is on the allow-list, and shipments queue offline; the anchor is also the natural place for the gateway's inventory attestation (TRU-002 attack 1).
2. **Per-device private keys are an operational burden.** Mitigation: OPS already provisions device certificates; the checkpoint key rides the same channel; rotation is a signed inventory change.
3. **A developer can still stop the process before a checkpoint.** Mitigation: clean-shutdown checkpoint plus the overdue telemetry; the anchored suffix bound tells the auditor exactly what is unproven, which is the honest answer.
4. **Receipts on the local path are proxy-observed only.** A local server reports no gateway header. Mitigation: for `local_host` deployments the receipt is the loopback `api_base` ADRL connected to, which is verifiable configuration; the inventory rule in TRU-002 clause 1 guarantees it.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P0-3, verified: `egress_checkpoint_every` is unreferenced; no caller of `checkpoint()`; the CLI verifier calls only `verify_chain()`; the composition root loads `keys/dev/manifest-signing.key` unconditionally.
- ADRL-SAF-009 (this register), clause 2 and attack 3.
- Crosby, Wallach, "Efficient Data Structures for Tamper-Evident Logging" (USENIX Security 2009) - https://www.usenix.org/conference/usenixsecurity09/technical-sessions/presentation/efficient-data-structures-tamper-evident (fetched in the 2026-09-02 review)
- GitHub Docs, "About push protection": every bypass creates an audit-log event held outside the developer's control - https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection (fetched in the 2026-09-02 review)

### Verdict
**PROPOSED (new).** Supersedes SAF-009, retaining its schema and rules by reference. Recommended for acceptance at D0; the D1 exit is the follow-ups below, and no maturity above D1 is possible until an anchor endpoint exists.

## Amendments applied

New decision; no prior text. SAF-009 status line updated to "superseded by TRU-003, pending disposition".

## Follow-ups

- [ ] OPS: checkpoint key custody (per-device provisioning, rotation, incident procedure); anchor endpoint and acknowledgement format; externally pinned public key distribution.
- [ ] Implementation: automatic checkpoints; shipment queue with acknowledgements; `adrl audit verify` checks signatures and anchors; dev-key refusal without `ADRL_DEV_KEYS=1`; `config/keys/` excluded from version control; receipt-based `lineage_left_machine`.
- [ ] Adversarial tests: delete an entry after a checkpoint (verifier fails); re-sign with the manifest key (verifier fails); run without dev flag on a dev key (process refuses); local deployment on a remote host reported as left-the-machine.
- [ ] EVL: the unanchored suffix length is reported in every evidence pack.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (external review) | none |
