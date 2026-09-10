# ADRL-OPS-004: Backup, restore and erasure

| Field | Value |
|---|---|
| Bucket | OPS; Platform, Runtime, Operations |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D0 Design; adrl-core has replay from events and crypto-shredding by session, but no backup procedure, and prompt-class fields still exist in plaintext rows (2026-09-03 external review, P1) |
| Review verdict | PROPOSED (new) |
| Tenets | 8 |
| Related decisions | MEM-001, MEM-005, MEM-007, MEM-010, SAF-009, OPS-001, OPS-002 |
| Open questions | Q5 |

## Decision

1. *What is backed up.* The evidence ledger and the egress ledger are backed up as SQLite online backups taken while the writer thread is paused at a transaction boundary; WAL files are never copied on their own. Projections are not backed up; they are rebuilt from the ledger (MEM-007). The keystore is backed up separately, encrypted under the host master key, and never in the same archive as the ledgers.
2. *Erasure survives backup.* Because erasure is key deletion (MEM-010), a backup of the ledger without the corresponding keystore state is unreadable for the shredded sessions; a restore therefore restores the ledger first and the keystore second, replaying `erased` events to delete any key the backup keystore still holds. A field-level data inventory (MEM-005 amendment) lists every column that may hold prompt-class content; every such column is either encrypted under a session key or keyed-hashed, so that erasure by key deletion is complete. Columns that fail this test are a blocker (EVL-009).
3. *Restore replays.* A restore reapplies events in sequence, rebuilds projections and verifies the egress chain against the last shipped checkpoint (OPS-007); a chain that does not reach a verified checkpoint marks the restored ledger `unanchored`.
4. *Retention.* Backups follow the same two horizons as the ledger (MEM-010): prompt-class keys expire with the session horizon; skeleton rows with the evidence horizon.

## Context and rationale

MEM-010 chose crypto-shredding precisely so that backups need not be rewritten. That works only if every prompt-class field is under a session key, which the 2026-09-03 external review showed is not yet true: repository evidence, workspace paths, argv plans and verifier output were stored in plaintext rows. This decision names the backup procedure and makes the field-level inventory the condition on which "erasure survives backup" rests.

## Adversarial review (2026-09-03)

### Steelman
Backing up an append-only ledger is easy; the only hard part is erasure, and key deletion solves it if and only if the inventory is complete. Making the inventory a CI-checked artifact is the cheapest way to keep it complete.

### Attacks
1. **Keyed hashes of paths are not erasable; the hash stays.** Answered: a keyed hash under the rotatable host key reveals nothing without the key; the inventory records it as `keyed`, distinct from `encrypted`, and the residual risk is stated.
2. **Pausing the writer for a backup stalls the proxy.** Answered: SQLite's online backup API copies pages incrementally; the pause is at one transaction boundary per backup step.
3. **A restored keystore reintroduces shredded keys.** Answered: clause 2 replays `erased` events after keystore restore; a golden test covers it.

### Evidence
- ADRL-MEM-010 (Proposed); crypto-shredding by session; two storage classes; erasure triggers.
- ADRL-MEM-005 (replacement); embeddings and hashes are prompt-class data; keyed hashes.
- ADRL-MEM-007; projections rebuildable from the ledger.
- 2026-09-03 external review of adrl-core, finding P1-5; plaintext workspace paths, argv and verifier output survive erasure.

### Verdict
**PROPOSED.** Names what MEM-010 assumed. Needs an owner and the field-level inventory.

## Follow-ups

- [ ] Write the field-level data inventory (`data-inventory-v1.json`): every column, its class, its protection; CI fails on a new column not in the inventory.
- [ ] Move repository evidence, workspace paths, argv and verifier output under session keys or keyed hashes in adrl-core.
- [ ] Golden test: restore a backup taken before an erasure, replay the `erased` event, assert the session's rows are unreadable.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the OPS bucket) | (none) |
