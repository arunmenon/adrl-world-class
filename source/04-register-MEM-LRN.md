# ADRL Decision Register — MEM, LRN

All decisions **Status: Accepted**. Source: Confluence bucket pages, updated Aug 27 2026.

---

## MEM — Memory, Evidence, Label Integrity

> This bucket is why the evidence in EVL can be believed. If the ledger is untrustworthy, every readiness claim built on it is worthless.

| ID | Decision | Maturity |
|---|---|---|
| ADRL-MEM-001 | Transaction memory is an append-oriented decision/outcome/event ledger keyed by immutable `route_id`. | D2 Tested |
| ADRL-MEM-002 | Outcome lifecycle is explicit: `pending`, `closed_turn`, then `closed_final` after late retry/interruption evidence. | D2 Tested |
| ADRL-MEM-003 | Deterministic verification enriches an outcome without overwriting observed telemetry. | D2 Tested |
| ADRL-MEM-004 | Training labels keep task difficulty separate from dialect/capability, infrastructure, privacy and policy failures. | D2 Tested |
| ADRL-MEM-005 | Raw prompts are not stored by default; embeddings and instruction hashes are suppressed for private/secret turns. | D2 Tested |
| ADRL-MEM-006 | The router uses a fail-safe memory facade and provider port; SQLite is the current local provider, not a semantic dependency. | D2 Tested |
| ADRL-MEM-007 | Derived retrieval indexes are rebuildable projections and detect cross-process database changes. | D2 Tested |
| ADRL-MEM-008 | Retrieval remains advisory/shadow until evaluated-label quantity and quality gates pass. | D3 Shadow |
| ADRL-MEM-009 | Counterfactual evidence attaches only to an explicit `route_id`; time or session proximity is never used to guess ownership. | D2 Tested |

### In plain terms

**MEM-001 — append-only, with a permanent name for every decision.** Each routing decision gets an immutable `route_id` at the moment it is made. Everything learned afterwards is appended against that ID rather than editing the original row. If outcomes could overwrite decisions, a later optimistic write could quietly rewrite history.

**MEM-002 — a turn that looks successful can stop being successful.** The model answers, tests pass, the turn closes — then the developer interrupts, or a retry fires, or the work is undone. Closing at first success would systematically over-report the cheap rung, because its failures often show up as later human corrections. Three states: `pending`, `closed_turn`, `closed_final` once late evidence can no longer arrive.

**MEM-003 — verification adds a column; it never edits the others.** Running the tests must not overwrite what was observed at the time — otherwise you lose "did the model appear to succeed but actually fail?"

**MEM-004 — the single most important decision for whether learning can ever work.** Four failures easy to collapse into one label: task too hard, model could not emit required edit format, endpoint down, policy blocked route. Only the first is evidence about capability. Otherwise the trained model learns to avoid local for reasons unrelated to local's ability — permanently and invisibly. CAS-002 enforced at the label layer.

**MEM-005 — the default is not to keep your code, and derived data counts as data.** Raw prompts not stored. For private/secret turns, embeddings and instruction hashes suppressed. Honest cost: lost learning signal on the sessions we understand least.

**MEM-006 — SQLite is a detail, and the router survives its absence.** Storage behind a facade with a provider port; fail-safe — if memory is unavailable, routing continues (degraded, unlogged).

**MEM-007 — indexes are projections, and they know when they are stale.** Anything derived for retrieval can be thrown away and rebuilt from the ledger. Cross-process detection: a benchmark run and the live router can both touch the DB.

**MEM-008 — "the system remembers similar past tasks" stays advisory until it has earned more.** Retrieval-based routing advises and is measured in shadow, cannot take authority until label quantity and quality gates pass (EVL-004 names the threshold).

**MEM-009 — no guessing by timestamp. Ever.** Counterfactual evidence binds only to an explicit `route_id`. Pairing by "same session, roughly same time" silently mis-pairs occasionally. A mis-paired counterfactual is worse than a missing one.

### Scrutinise / Open items
- MEM-001 + MEM-009 are the anti-guessing rules, and why the corpus is small. Would you relax them for volume?
- MEM-002's late-closing lifecycle — is the window long enough to catch human corrections?
- MEM-004 — is the four-way failure typing complete?
- MEM-005 — confirm the privacy default meets your bar.
- MEM-006 — verify the facade isolates SQLite; a semantic dependency on a local file store would block multi-worker future (OPS-001).
- Representative verified outcomes remain scarce: contracts solid, corpus thin.
- Counterfactual pairs expensive; usable volume very low.
- Code reality: only ONE task with strong test-based verification; 34/300 evaluated decisions for similar-task lookup; session-to-route tracking in a Python dict (single-process); automatic verification not connected to every eligible task; SDLC intent taxonomy has no version/confidence/correction history in MEM. Actual failure types in `outcomes.py`: task_capability, harness_dialect, infrastructure, policy_constraint, user_abort, unverifiable (six, not four).

Code map: MEM-001 `memory_ports.py`, `memory_sqlite.py`. MEM-002 `OutcomeEvent`, SQLite lifecycle checks. MEM-003 `verifier.py`, `live_verification.py`. MEM-004 `outcomes.py`. MEM-005 `memory_facade.py`. MEM-006 `MemoryProvider`, `RouterMemory`, `NullProvider` (`memory_null.py`, `chain.py`). MEM-007 SQLite embeddings + NumPy. MEM-008 `shadow_retrieval.py`. MEM-009 `counterfactual.py`, `live_verification.py`. Graph-lite `graph_lite.py` (nodes/edges tables; not built in any active DB).

---

## LRN — Learning and Adaptation

> This is deliberately the least mature bucket. Three of seven decisions are D0 — the estimator is unbuilt and the learned router holds no authority.

| ID | Decision | Maturity |
|---|---|---|
| ADRL-LRN-001 | Verified, cause-clean outcomes outrank heuristic proxy labels for training. | D2 Tested |
| ADRL-LRN-002 | Counterfactual training data uses paired local/frontier attempts from the same sanitised snapshot. | D2 Tested |
| ADRL-LRN-003 | Train a calibrated utility estimator for marginal frontier gain, not a classifier that imitates current heuristic routes. | **D0 Design** |
| ADRL-LRN-004 | Learned models may use only information available before the routing decision; outcome and future-session leakage are prohibited. | D2 Tested |
| ADRL-LRN-005 | Every learned artifact versions its feature schema, data snapshot, objective, calibration, thresholds and policy compatibility. | D2 Tested |
| ADRL-LRN-006 | Uncertain or out-of-distribution predictions abstain to the deterministic safe policy. | **D0 Design** |
| ADRL-LRN-007 | Learning may propose policy updates, but deployment requires offline evaluation and explicit graduation; no autonomous online promotion. | **D0 Design** |

### In plain terms

**LRN-001 — a small number of trustworthy labels beats a large number of plausible ones.** Proxy signals — the turn did not error, so call it a success — are abundant and quietly wrong. Verified means a deterministic check actually ran; cause-clean means the failure was about capability. Fewer, better labels.

**LRN-002 — to learn what frontier buys, you have to run the same task twice.** A usable training example is a pair: same sanitised snapshot, attempted on both rungs, verified the same way. Expensive and slow. The honest reason this bucket sits at D0 — a shortage of legitimate pairs.

**LRN-003 — do not build a model that imitates the rules you already have.** Supervised learning on past routing decisions clones today's heuristics. The target instead is a utility estimator: for this specific task, how much does frontier actually improve the outcome? Much harder. Entirely unbuilt.

**LRN-004 — no peeking at the future.** Features must be available at the moment of the decision. A feature derived from how the turn turned out will make offline metrics look superb and live performance collapse.

**LRN-005 — a model artifact you cannot reproduce is a liability.** Every artifact carries feature schema, data snapshot, objective, calibration, thresholds, policy compatibility. Makes "roll back the router" a real operation.

**LRN-006 — the model must be allowed to say "I don't know."** On a request unlike anything in training, or with low confidence, the estimator abstains and the deterministic policy decides. D0, unbuilt. Until it exists, no learned component should hold authority.

**LRN-007 — no model promotes itself.** Deployment requires offline evaluation against baselines and an explicit human graduation step (EVL-006/007). No metric threshold auto-promotes.

### Scrutinise / Open items
- LRN-003 is the crux — is utility estimation the right target, and is the ambiguous band large enough to repay it? (Q4)
- LRN-002 — would you accept a weaker pairing standard to get volume? (We would not, but argue it.)
- LRN-006 being D0 means the safety property that justifies a learned router does not yet exist. Should abstention be built before the estimator?
- LRN-004 — how is leakage enforced, not just stated?
- Where should the bar sit for introducing a learned component at all? (Q4)
- Counterfactual pair volume very low.
- Calibration and abstention thresholds undefined pending data.

Code map: `router/learning_contract.py`, `config/learning-contract-v1.json`, `router/learning_readiness.py`, `config/readiness-score-v1.json`, `router/counterfactual.py`.
