# OPS: Platform, Runtime, Operations

**Product planning, 2026-09-08:** The plan starts with a qualified private installation and funds scale only after repeatability; graph representation does not imply adopting new infrastructure. See the [startup roadmap](../../reports/adrl-product-roadmap-2026-09-08.md) and [context-graph proposal](../../design/adrl-context-graph-memory-proposal-2026-09-08.md). Implementation remains paused; decision text, architectural status and maturity are unchanged.

**Planning checkpoint, 2026-09-08:** the user requested the target adaptive routing/RSI architecture before further implementation. [Blueprint](../../reports/adrl-adaptive-routing-rsi-blueprint-2026-09-08.md) and [all-ADR map](../../reports/research/adaptive-routing-blueprint-2026-09-08/taxonomy-map.md) are proposals for disposition. Implementation continuation is paused; no decision wording, status or maturity is changed by the blueprint.

**W3.2 current pinned-engine validation, 2026-09-08:** [receipt and transport correction](../../reports/adrl-w3-transport-receipts-2026-09-08.md)
separates stopped preparation from active I/O while preserving original ownership and v1 history.
895 tests and all eleven checks pass, with zero skips and 316 stable inputs. All thirteen
fixtures and the image are absent; no new cleanup exception. The bounded d2 synthetic lifecycle
closes; active-copy custody is next. Full W3, real-harness/independent qualification and all
architectural status/maturity fields remain unchanged. Inventory: 371 fields/381 entries.


**W3.2 runtime prototype, 2026-09-08:** [one-shot fixture execution](../../reports/adrl-w3-isolated-launch-2026-09-08.md).
Permanent launch denial, authenticated lifecycle and serialized recovery are implemented;
861 offline tests and eleven checks pass, with eight engine cases skipped. Two bounded engine
runs each had 3 passes/1 failure; lost stopped-create receipt diagnosis remains open. All eight
fixtures and one image are absent, including one documented operator-cleanup exception.
Schema 12 inventories 370 fields/380 entries. Eight ADRs preserve prior text and every grade;
no exact-close, learning, real-harness or full-W3 qualification.


**W3.2 identity research, 2026-09-08:** [resolved startup comparison](../../reports/adrl-w3-execution-identity-2026-09-08.md).
101 offline cases and seven new engine observations passed; all seven fixtures and one image
were removed. One-shot runtime launch, sealing and recovery are the next implementation slice.
The 812-test runtime baseline is reused after verifying 306 hashes. Eight ADRs preserve prior
text and all grades; full W3 remains open.


**W3.2b2d2 research, 2026-09-08:** [launch identity gate](../../reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md).
The proposed claim/seal/stop/abort lifecycle remains gated by execution-identity compatibility; no active runtime operation was added. The two-run research allowance closed after two failures.
The unchanged 812-test baseline is reused with 306 verified hashes. Eight ADRs preserve prior text and grades; full W3 stays open.


**W3.2b2d1 update, 2026-09-08:** [stopped ownership](../../reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md).
One durable create claim and permanent fence coordinate a stopped local fixture resource. Lost create acknowledgement stays uncertain; restart/removal recovery needs the original authenticated binding. Full multi-process runtime and active lifecycle qualification remain open.
All 812 tests and eleven checks pass. Seven owning ADRs preserve prior wording, status and maturity; full W3 remains open.


**W3.2b2c research, 2026-09-08:** [writer-boundary observations](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md).
Docker-client death left daemon-owned work running, making durable resource identity and recovery the next prerequisite. No production backend or multi-worker qualification is added.
Six synthetic observations are separate from the unchanged 759-test runtime baseline. No status, maturity or release promotion.


**W3.2b2b2 update, 2026-09-08:** [process coordination](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md).
Durable admission now connects the attempt and process owner, with concurrent/restart refusal, cancellation draining and eventual authority monitoring. The group-only backend never releases its workspace; broader runtime locking and whole-writer qualification remain open.
All 759 tests and eleven checks pass. Prior status/maturity fields remain unchanged; full W3 remains open.


**W3.2b2b1 update, 2026-09-08:** [key revocation](../../reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md).
Cooperating keystore locks and audit ordering are tested, including process death after revocation. Full runtime locking and process/erasure/release coordination remain open.
All 724 tests and eleven checks pass. No status or maturity promotion; full W3 stays open.

**W3.2b2a update, 2026-09-08:** [reserved terminal capacity](../../reports/adrl-w3-2b2a-terminal-capacity-2026-09-08.md).
Shared admission accounts for pending terminal commitments and active ceilings; quota grant consumption is append-only. This does not qualify process release or multiple runtime writers.
All 697 tests and eleven checks pass; 279 fields inventoried. No status or maturity
promotion. Coordinated erasure/process/release and full W3 remain open.

**W3.2b1 update, 2026-09-08:** [owned process groups](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md).
Single-owner exit, cancellation and owner-loss cleanup are tested; admission, restart and journal recovery remain open.
All 669 tests and eleven checks pass. No architectural-status or maturity promotion;
full W3 and exact task-close attribution remain open.

**W3.2a update, 2026-09-08:** the [internal attempt journal](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md)
records encrypted starts, close requests and interruption, preserving original initial state
through retries. All 631 tests and eleven checks pass. Journal reservation is not a process
lock; supervisor/capture association and recovery remain open. No status or maturity promotion.

**W0 execution baseline, 2026-09-07:** [local engineering checks](../../reports/waves/w0-baseline.md)
now record source identity, individual failures and contract/ADR coverage. All 556 tests and
eleven checks pass. The [journey](../../reports/adrl-implementation-journey.md) tracks bounded
continuation. Status/maturity and broader release gates remain unchanged; historical notes follow.

**Core question:** How is the system operated, observed and rolled back?
**Owns / does not own:** Owns state backends, health, observability, CI, budgets, deployment, rollback, key custody and operator controls. Does not own semantic routing policy or the safety gates' content.

Not captured in the 2026-08-27 source pack; known until 2026-09-03 only by cross-reference (OPS-001, OPS-006). This is the first capture. Every decision is Proposed and needs an owner and a disposition before entering the canonical register. Three decisions (OPS-002, OPS-003, OPS-007) answer P0 findings of the 2026-09-03 external review of adrl-core; two (OPS-004, OPS-005) answer P1 findings.

## First capture (2026-09-03)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-OPS-001 | Multi-worker consistency and the single-process constraint | PROPOSED (new) | (none) → D1 | The blocker is process-local state, not SQLite; declare it, inventory it, lock a second worker out |
| ADRL-OPS-002 | Key custody and rotation | PROPOSED (new) | (none) → D0 | Four key classes with custodians; checkpoint and manifest keys separated; dev keys refused by default |
| ADRL-OPS-003 | Endpoint inventory, rollout and change control | PROPOSED (new) | (none) → D0 | Signed inventory with trust zone and geography; `local` must mean on this host |
| ADRL-OPS-004 | Backup, restore and erasure | PROPOSED (new) | (none) → D0 | Crypto-shredding survives backup only if every prompt-class column is under a key; field-level inventory |
| ADRL-OPS-005 | Shadow-mode semantics per subsystem | PROPOSED (new) | (none) → D1 | Observe mode must have no authority; shadow findings in their own namespace |
| ADRL-OPS-006 | Record the served identity, not the intended one | PROPOSED (new) | (none) → D2 | Implemented and tested for rung and model in adrl-core; extended to deployment, zone and geography |
| ADRL-OPS-007 | Audit-anchor availability, rollback and incident response | PROPOSED (new) | (none) → D0 | Automatic signed checkpoints shipped off-host; unanchored windows are blockers; five runbooks |
| ADRL-OPS-008 | Fail-open SLOs, alerting and bypass audit | PROPOSED (new) | (none) → D1 | The operational half of FND-004; pre-registered thresholds; alerts in the egress ledger |

Tally: 8 PROPOSED.

## Cross-cutting findings

1. **Three of the review's P0 findings were OPS decisions that did not exist.** "Local" as a label (OPS-003), the development key signing the audit trail (OPS-002) and the missing anchor (OPS-007) are all operational objects the SAF decisions assumed. The code implemented what SAF-008, SAF-009 and FND-002 said, and they said "rung". The correction belongs in both places; these decisions are the register half.

2. **Trust zone and geography are attributes of a deployment, not a rung** (OPS-003, OPS-006). The permitted set that SAF gates shrink should be a set of deployments carrying zone and geography, with the rung as one attribute; FND-002 needs an amendment to say so, and TRU (proposed by the external review) is the natural owner of the policy side.

3. **Observation must not have authority** (OPS-005). Gate observe mode that writes durable pins is a design error, not a bug; the fix is a namespace, not a flag check.

4. **Erasure is only as complete as the data inventory** (OPS-004). MEM-010's crypto-shredding is correct and insufficient until every prompt-class column is enumerated and protected.

5. **The proxy must never sign its own audit trail** (OPS-002, OPS-007). Manifest verification and checkpoint signing use different keys held by different parties; the proxy holds only public keys in production.

6. **Dependencies on EVL.** The `unanchored` window, the `assumed_intended` share, the fail-open rate and the shadow-namespace exclusions are all EVL-009 blockers or EVL-008 scorecard sections; the two buckets were captured together for that reason.

## Sources consulted

- Register files: `source/01-overview-tenets-taxonomy.md`, `REVIEW-LOG.md`, ADRL-FND-002, ADRL-FND-004, ADRL-SEM-002, ADRL-SAF-001, ADRL-SAF-002, ADRL-SAF-003, ADRL-SAF-004, ADRL-SAF-008, ADRL-SAF-009, ADRL-RTG-001, ADRL-RTG-008, ADRL-CAS-006, ADRL-MEM-001, ADRL-MEM-005, ADRL-MEM-006, ADRL-MEM-007, ADRL-MEM-010, ADRL-LRN-004, ADRL-LRN-005, ADRL-LRN-007.
- SQLite, "Write-Ahead Logging" (official docs), as cited in ADRL-MEM-001; https://www.sqlite.org/wal.html
- 2026-09-02 conformance review and 2026-09-03 external review of adrl-core (internal; findings quoted by number in each decision).
- adrl-core `docs/known-gaps.md` (2026-09-02).
