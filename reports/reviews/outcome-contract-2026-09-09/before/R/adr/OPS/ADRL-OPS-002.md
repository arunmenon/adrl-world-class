# ADRL-OPS-002: Key custody and rotation

| Field | Value |
|---|---|
| Bucket | OPS; Platform, Runtime, Operations |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D0 Design; adrl-core has a file keystore for the host HMAC key and per-session keys, but the manifest-signing development key also signs egress checkpoints and is loaded unconditionally (2026-09-03 external review, P0) |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8 |
| Related decisions | SEM-002, SAF-002, SAF-008, SAF-009, MEM-005, MEM-010, LRN-005, LRN-007, EVL-007, OPS-007 |
| Open questions | Q5, Q7 |

## Decision

ADRL uses four key classes, each with a named custodian, a storage location, a rotation rule and a compromise procedure, recorded in a versioned key inventory:

| Key | Purpose | Custodian | Storage | Rotation |
|---|---|---|---|---|
| Host HMAC secret | Session and lineage identities at rest (SEM-002), keyed instruction hashes (MEM-005), span hashes (SAF-003) | Host owner | Local keystore, mode 0600 | Rotatable; rotation is a projection rebuild (MEM-007) and the old key is retained read-only for the evidence horizon |
| Per-session data keys | Encrypt prompt-class artefacts; shredded on erasure (MEM-010) | ADRL process | Local keystore, wrapped by a host master key | Never rotated; deleted on erasure |
| Manifest signing key | Signs `repo-classification` manifests (SAF-008) and graduation records (EVL-007) | Security, outside the training team | Hardware or managed KMS; never on a developer host | Annual or on compromise; public key pinned in config |
| Checkpoint signing key | Signs egress-ledger checkpoints (SAF-009) | Security, distinct from the manifest key | Same as above, distinct key pair | Same; public key pinned in the auditor's verifier, not in the proxy |

Development keys exist only under a `config/keys/dev` path that is gitignored, are refused by the proxy unless `ADRL_ALLOW_DEV_KEYS=1` is set, and cause a startup warning that is itself recorded in the egress ledger. The proxy never holds a private signing key for checkpoints in a production profile; it produces the checkpoint digest and a separate signer process signs and ships it (OPS-007).

## Context and rationale

The 2026-09-03 external review found the adrl-core composition root loading the committed-on-disk development key for both manifest verification and checkpoint signing, and called it a collapse of key separation and auditor trust. It is not a leaked secret; it is a missing decision. This decision assigns custody per key class and separates the two signing keys because their trust relationships differ: the manifest key is trusted by the proxy, the checkpoint key is trusted by an auditor who must not trust the proxy.

## Adversarial review (2026-09-03)

### Steelman
Four key classes with different custodians is the smallest partition that matches the trust boundaries the SAF decisions draw. Refusing dev keys by default is a one-line check that closes the P0.

### Attacks
1. **A KMS on a developer laptop is unrealistic.** Answered: the laptop holds only the host HMAC secret and session keys; signing keys are used by security's signer, not by the proxy.
2. **Rotating the host HMAC secret breaks every lineage identity.** Answered: rotation keeps the old key read-only; new lineages use the new key; the projection rebuild is the documented cost.
3. **A separate signer process is one more thing to run.** Answered: it is the auditor's independence; a proxy that signs its own audit trail is not audited.

### Evidence
- ADRL-SAF-009 (Proposed); hash-chained ledger with periodic signed checkpoints shipped off-device; HMAC keys per deployment.
- ADRL-MEM-010 (Proposed); per-session keys in a local keystore; erasure by key deletion.
- ADRL-SEM-002; HMAC of the session key with a per-deployment secret; raw values never stored.
- 2026-09-03 external review of adrl-core, finding P0-3; development key loaded unconditionally for checkpoint signing.

### Verdict
**PROPOSED.** Closes a P0 the register had no home for. Needs security as owner.

## Follow-ups

- [ ] Gitignore `config/keys/` in adrl-core; move the dev keys under a flag; startup refuses them without `ADRL_ALLOW_DEV_KEYS`.
- [ ] Split the checkpoint key from the manifest key; the proxy holds only public keys in production.
- [ ] Write `key-inventory-v1.json` and the compromise runbook (OPS-007).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the OPS bucket) | (none) |
