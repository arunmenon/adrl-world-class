# ADRL-MEM-005 — Prompt-derived artefacts are prompt-class data

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Superseded 2026-09-02 (see replacement) |
| Maturity | D2 Tested, review recommends D1 Code for the replacement — the suppression path is tested, but the replacement's storage-class, retention and late-pin clauses have no implementation |
| Review verdict | REJECT |
| Tenets | 2, 8 |
| Related decisions | SAF-002, SAF-003, SAF-005, MEM-001, MEM-007, MEM-008, MEM-010 (proposed), LRN-004, OPS-001 |
| Open questions | Q5 |

## Decision

Raw prompts are never stored in the ledger; prompt-derived artefacts — embeddings, instruction hashes and any retrieval key computed from prompt content — are classified as prompt-class data and are stored only under the same access, retention and erasure controls as the prompt itself would be, and are not produced at all for private, secret or privacy-pinned turns, including turns earlier in a session that is later pinned.

1. **Embeddings are the prompt, statistically.** The embedding store is treated as a lossy copy of the corpus: same access control as source code, per-session encryption or crypto-shreddable keys (MEM-010), a retention period, and no export outside the host without the same review a source export would get.
2. **Pin suppression is retroactive within the session.** When SAF-002 pins a session at turn *k*, embeddings and instruction hashes already written for turns 1…*k−1* of that session are shredded, because the scanner (SAF-003) is precision-limited and the secret may have been present earlier.
3. **Hashes are pseudonyms, not anonymisation.** Instruction hashes are keyed (HMAC with a host-local secret) so an attacker with the database cannot dictionary-match short or common instructions; the key is rotatable and rotation is recorded as a projection rebuild (MEM-007).
4. **Opt-in raw storage is a separate decision.** If any raw prompt retention is ever wanted (for debugging or labelling), it requires its own ADR with a named owner, scope and retention; this decision does not grant a "by default" exception.

## Context and rationale

The default is not to keep your code, and derived data counts as data. The original decision got the second half of that sentence right for private and secret turns and wrong for everything else: it stored embeddings of every non-private prompt as if a vector were not a prompt. The embedding-inversion literature has closed that gap — 32-token inputs are recovered exactly 92% of the time from a state-of-the-art encoder, and zero-shot methods now do it with only black-box encoder access, which any holder of `router-memory.db` plus the local embedding model has. Instruction hashes fare no better: a hash of a short developer instruction is a pseudonym that falls to a dictionary of common instructions, not an anonymisation.

The replacement keeps the intent — no raw prompts, suppress for sensitive turns — and adds the consequence: the embedding store is a lossy copy of the company source code and developer intent and must be handled as one. It also closes the late-pin hole: SAF-002 pins a session one-way from the moment a secret is detected, but the turns before detection were already embedded and, under MEM-001, those rows are immutable. The honest cost stated in the original ("lost learning signal on the sessions we understand least") remains and gets slightly larger.

## Adversarial review (2026-09-02)

### Steelman
Not storing raw prompts is the right default and suppressing derived artefacts for flagged turns is more than most systems do; SAF-003's "a vector built from your prompt is still your prompt, statistically" shows the authors understood the risk. The decision is tested (`memory_facade.py` removes raw instructions, hashes normal ones, skips embeddings for private tasks) and the honest acknowledgement of lost signal is exemplary.

### Attacks
1. **The decision contradicts its own rationale.** The rationale says derived data counts as data; the decision stores derived data for every non-private turn. Embeddings of ordinary coding prompts at the company contain file paths, function names, business logic, ticket text and frequently the surrounding code. Inversion recovers this. The distinction the decision draws (private vs not) is a scanner output, and SAF-003 is at D3 precisely because its precision is not established — so the unprivileged embedding store contains everything the scanner missed.
2. **The attacker model is weak.** Inversion attacks in the literature assume black-box access to the encoder. ADRL's encoder is a local model shipped with the router; anyone with read access to `router-memory.db` (a file on a developer laptop, or on a shared host under OPS-001) has both. This is a stronger attacker position than the papers assume, not weaker.
3. **Late pin, immutable ledger.** SAF-002 makes the pin one-way for the rest of the session; nothing un-embeds the turns before the pin. Under MEM-001 those rows are immutable and under MEM-007 they are already in the NumPy index. The most common way a secret enters a session is "it was in a file the model read three turns ago"; the pin fires late and the embedding survives.
4. **Instruction hashes are re-identifiable.** Unkeyed hashes of instructions like "fix the failing test", "add logging", "update the README" are trivially dictionary-matched; hashes of unique instructions are unique identifiers linking sessions. Hashing low-entropy inputs is widely understood not to anonymise them. The decision treats "hash" as a privacy control; it is at best a pseudonym and needs a key.
5. **"By default" is a hole.** "Raw prompts are not stored by default" implies a non-default. Who can turn it on, for what, for how long, and where is it logged? At a payments company an undocumented opt-in for storing developer prompts is a PCI/data-governance finding waiting to happen.
6. **No retention, no erasure.** Combined with MEM-001's immutability, the embedding store grows forever and has no deletion path. A security incident ("that repo had a leaked production key in a fixture file for two weeks") has no procedure. This is the gap MEM-010 (proposed) fills; MEM-005 must at least reference it.

### Evidence
- J. Morris, V. Kuleshov, V. Shmatikov, A. Rush, "Text Embeddings Reveal (Almost) As Much As Text" (EMNLP 2023; arXiv 2310.06816) — iterative correction-and-re-embed (Vec2Text) recovers 92% of 32-token inputs exactly and extracts full names from clinical-note embeddings; attacks 1, 2 — https://arxiv.org/abs/2310.06816
- (authors not captured) "Rethinking the Privacy of Text Embeddings: A Reproducibility Study of 'Text Embeddings Reveal (Almost) As Much As Text'" (arXiv 2507.07700, 2025) — replicates Vec2Text in- and out-of-domain, including recovery of password-like strings; finds Gaussian noise and especially quantisation mitigate inversion; supports both the threat and the mitigation options — https://arxiv.org/abs/2507.07700
- (authors not captured) "Universal Zero-shot Embedding Inversion" (arXiv 2504.00147, 2025) — ZSInvert recovers key semantic content with only black-box encoder access and no per-encoder training, far fewer queries than Vec2Text; attack 2 — https://arxiv.org/abs/2504.00147
- (authors not captured) "ALGEN: Few-shot Inversion Attacks on Textual Embeddings using Alignment and Generation" (ACL 2025; arXiv 2502.11308) — few-shot inversion via embedding-space alignment; appears in search results with matching title, not fetched; cited for existence of the few-shot regime only — https://arxiv.org/abs/2502.11308
- Microsoft Azure Architecture Center, "Event Sourcing pattern" — recommends keeping personal data out of the immutable stream by reference or crypto-shredding with per-subject keys; the pattern the replacement adopts for embeddings (attack 6) — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- L. Demir, A. Kumar, M. Cunche, C. Lauradoux, "The Pitfalls of Hashing for Privacy" (IEEE Communications Surveys & Tutorials, 2018) — title and venue confirmed from search results; the full text could not be fetched (access denied), so it is cited only as the standard reference that hashing enumerable identifiers is not anonymisation; attack 4 otherwise argued from first principles — https://ieeexplore.ieee.org/abstract/document/8023740/

### Verdict
**REJECT.** Attack 1 is fatal to the decision as written: it rests on a distinction (raw vs derived) that its own rationale rejects and that the inversion literature has dissolved, and the tested implementation faithfully implements the flawed distinction. Attacks 2–4 show the practical consequences are worse in this deployment than in the papers (local encoder, immutable ledger, late pins, unkeyed hashes). Attack 5 is a governance hole. The replacement keeps every safety property the original had, reclassifies embeddings and hashes as prompt-class data, makes pin suppression retroactive within the session, keys the hashes, and hands retention/erasure to MEM-010. The cost — slightly more lost learning signal and an encryption/shredding path — is the price of the tenet.

## Amendments applied

- Superseded. Replacement text above. Concretely: "not stored by default" → "never stored" with a separate-ADR path for any exception; embeddings and hashes reclassified as prompt-class data with the same access/retention/erasure controls; suppression extended to pre-pin turns of a pinned session; instruction hashes must be keyed; reference to MEM-010 for retention and erasure.

## Follow-ups

- [ ] Run Vec2Text or a zero-shot inversion against a sample of ADRL's own embeddings (local encoder, local DB) and report exact-match and semantic-recovery rates in the EVL pack; this is the number that justifies the reclassification.
- [ ] Evaluate quantisation/noise on stored embeddings (per the reproducibility study) against retrieval quality in `shadow_retrieval.py`; if retrieval survives 8-bit quantisation, adopt it as defence in depth.
- [ ] Implement retroactive shredding on pin: golden test — embed turns 1–3, pin at turn 4, assert turns 1–3 have no embedding rows and the NumPy index is rebuilt without them.
- [ ] Replace unkeyed instruction hashes with HMAC under a host-local key; golden test that the same instruction hashes differently on two hosts.
- [ ] Remove or explicitly document any code path that stores raw instructions; grep `memory_facade.py` and the proxy for raw-prompt persistence and add a CI assertion.
- [ ] Draft ADRL-MEM-010 (retention and erasure).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Superseded: embeddings and hashes reclassified as prompt-class data; retroactive pin suppression; keyed hashes; no default exception | "Raw prompts are not stored by default; embeddings and instruction hashes are suppressed for private/secret turns." |
