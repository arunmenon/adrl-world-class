# ADRL-TRU-001 - Authenticated workload identity (Proposed)

| Field | Value |
|---|---|
| Bucket | TRU - Trust, Residency and Egress |
| Status | Proposed 2026-09-03 (new, from external review) |
| Maturity | D0 Design, review recommends D0 Design (the 2026-09-02 implementation resolves identity from prompt text, which this decision forbids) |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8 |
| Related decisions | SAF-008 (superseded in part), SAF-001, SAF-002, SAF-003, TRU-002, TRU-003, SEM-002, SEM-006, OPS (launcher, SCM inventory) |
| Open questions | Q2, Q5 |

## Decision

The repository and data-class identity of a lineage is established by a trusted launcher assertion tied to the organisation's SCM inventory and corroborated by a content fingerprint of the checkout; it is never derived from the system prompt, from CLAUDE.md paths, or from tool inputs or results, and a lineage whose identity is unknown or uncorroborated is local-only until an assertion arrives.

1. *Assertion*: the process that launches the harness (a wrapper, a devcontainer hook, or a managed-device agent, chosen by OPS) resolves the checkout to an SCM inventory record (repository id, default remote, classification manifest entry) and hands ADRL a signed assertion bound to the harness process and session key (SEM-002). The assertion carries the classification manifest version it was resolved against.
2. *Corroboration*: ADRL computes a content fingerprint of the checkout (a keyed digest over a manifest-declared set of files, for example the root manifest and lockfile) and compares it to the fingerprint the inventory holds; a mismatch is a `classification_conflict` lineage event and the stricter of the two classes applies.
3. *Unknown is local-only*: absent an assertion, or with an assertion whose signature or manifest version cannot be verified, the lineage's ceiling is the local rung (TRU-002) and the egress ledger records `identity_unknown`. This replaces SAF-008's "organisation default class".
4. *Prompt text is evidence, never authority*: working directories, remotes and paths observed in prompt or tool text may be recorded (keyed, per MEM-005) as corroborating evidence and may only tighten the ceiling (a restricted path prefix seen in a tool input tightens as before); they may never widen it or establish identity.
5. *Re-assertion on scope change*: a change of working directory visible to the launcher (`--add-dir`, worktree isolation for subagents) produces a new assertion; a child lineage without its own assertion inherits the parent's identity and ceiling (SEM-006).
6. The PII detector tier of SAF-008 clause 3 is unchanged and remains a SAF content control.

## Product service evidence, 2026-09-07

The local product service verifies signed, expiring launcher assertions and an exact registered workload before binding or accessing a session. Harness producer identity is derived from that binding and conveys no trusted-verifier authority. Conflicting identity is rejected on bound model traffic. This is a trusted-host pilot boundary, not remote tenancy or full-contract graduation.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

### Product service application: local product sessions

The first product API reuses the existing signed launcher assertion as its expiring credential.
Binding requires an exact registered repository match, the assertion's explicit session ID and
the supported adapter/profile pair. A credential reference identifies the assertion; it is not
a new provider credential. Renewal for the same session must retain its binding and restrictions.
The local launcher and service share a trusted host keystore; this does not establish tenant
isolation against code running as the same operating-system user. Separate child-session binding
and remote credential issuance remain outside this first service package.

Product reads and event writes require authority over the exact bound session. Harness producers
may submit observations, but cannot submit trusted verification. Bound model requests must carry
consistent identity and cannot use an unadmitted endpoint. These requirements apply to the new
product integration; legacy unbound traffic remains separately described and is not upgraded by
the presence of a product API. Implementation and test results are linked in the product service evidence above.

## Earlier foundation scope, 2026-09-07

The new Claude Code adapter supplies session and lineage correlation signals. It does not grant
repository, residency, producer or workload authority. Existing signed-launcher checks remain a
separate control; this package does not implement the proposed product credential/session service.

`GET /adrl/v1/capabilities` reports the installed distribution's implemented and planned surface.
It is not a runtime enforcement attestation or proof of authenticated workload identity. The
session and event operations listed in its preview contract are unimplemented and return 501.
The historical maturity statement above describes the earlier review baseline; this foundation
package does not reassess or graduate the full TRU-001 contract. See the
[implementation record](../../reports/adrl-product-foundation-implementation-2026-09-07.md).

## Live observation pilot, 2026-09-07

Observation-mode API access uses the existing signed local workload assertion, separately from Claude Code native subscription authentication. The binding mode cannot change on renewal and cannot authorize model dispatch for an observation session. A real local hook session exercised that API identity path. This does not establish remote tenancy, managed SCM corroboration or control of native cloud traffic; the trusted-host limitation remains.

The [pilot report](../../reports/adrl-live-observation-pilot-2026-09-07.md) links the applied 15-file package, 511 passing tests,
all required checks, reviewed outcomes and remaining blockers. Architectural status is unchanged;
this evidence does not promote the full decision to D3 or D4. Earlier dated sections preserve
their original implementation and planning scope.

## Session verification implementation, 2026-09-07

Verifier authority is the trusted local operator with access to the configured ledger, keystore and approved plan outside the task workspace. The CLI checks the existing signed session and exact workspace. Public harness credentials still cannot submit verification claims; tests reject both verification-shaped events and added authority fields. The same-OS-user trust boundary remains explicit, with no remote verifier credential role, tenant isolation or remote attestation.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## W3.1 retained operator captures, 2026-09-08

The capture API is available only as an internal trusted-operator library. It consumes a previously authenticated local Principal, checks the binding/workload/expiry/root and never registers a harness intake endpoint. Its schema cannot claim trusted close or verification success. This reuses the existing same-OS-user boundary; it is not a remote verifier role, signature-verification service or defense against an attacker controlling that account. No provider or learned authority is added.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

The journal consumes a previously authenticated local Principal under the existing same-OS-user trust boundary. It records local operator intent; public harness intake cannot reach this new internal API. Its schema has no success, stopped-writer or verified-result command, and every event retains unestablished attribution and false learning eligibility. This is not a remote verifier authority or proof against an attacker controlling the host account. Restart does not infer process ownership or grant signaling authority from a stored PID.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b1 owned process groups, 2026-09-08

W3.2b1 accepts explicit trusted-operator inputs and grants cleanup authority only through the in-memory launcher handle created by that run. Known incompatible child-signal handling is rejected, and the embedding process must not run a competing reaper. There is no API that turns persisted process metadata into signal authority. The executable digest is checked twice, but scripts/dependencies and hostile-account replacement races are not fully pinned. This is not a new authenticated workload assertion, SCM binding, public authority path or credential-isolation guarantee.

See the [plain-language report](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b1-process-ownership-2026-09-08.json),
[runner](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_owner.py),
[launcher](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_anchor.py),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_process_owner.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/process-ownership.md).
All 669 tests and eleven checks pass on the recorded Darwin build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved. Full W3
and exact task-close attribution remain open.

## W3.2b2b1 persistent key revocation, 2026-09-08

W3.2b2b1 makes product erasure status honor persistent keystore revocation even if the ledger shred audit failed. A composed API test restores the old wrapped file after that failure: the timeline keeps the payload unavailable, rebinding is forbidden and new observation submission is forbidden. The existing erased payload state denotes access denial, not certification of successful physical cleanup and audit completion. No new identity assertion, SCM binding, public endpoint or key-restoration authority is introduced; same-account and backup-rollback limits remain.

See the [plain-language report](../../reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md),
[checks and pre-change probe](../../reports/research/adrl-w3-2b2b1-key-revocation-2026-09-08.json),
[keystore](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/keystore.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_key_revocation.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/key-revocation.md).
All 724 tests and eleven checks pass for the recorded Darwin build. Prior wording,
architectural status and maturity fields remain unchanged. Independent security review,
process/erasure/release coordination and full W3 remain open.

## W3.2b2b2 process coordination, 2026-09-08

Coordinator admission requires a previously authenticated, readable and unexpired session, its intact v2 started attempt and the same canonical workspace as the process request. Public hooks cannot call this internal API. Closure or loss of readable authority requests stop; host-key identity changes block further admission. No arbitrary PID, caller quiescence boolean or externally supplied process report grants execution/release authority. Same-account hostile mutation and broader isolation remain unqualified.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2c writer-boundary research, 2026-09-08

The candidate isolated backend must bind the local engine, durable creation intent, exact resource identity and original security/configuration evidence. A name, label, saved host PID or caller-supplied stopped boolean alone is not recovery or release authority. The synthetic container had no host repository/credential/socket mounts and ran without effective capabilities; trusted host/daemon administrators remain outside the qualification. No public trust boundary is widened.

See the [plain-language report](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md),
[experiment and source evidence](../../reports/research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[fixture source](../../reports/research/writer-boundary-2026-09-08/probe.go),
[frozen packet](../../reports/waves/w3-2b2c-writer-boundary.md) and
[next ownership packet](../../reports/waves/w3-2b2d-resource-ownership.md).
The corrected research run completed six bounded observations, including negative controls.
The previously passing 759-test/eleven-check runtime source is unchanged; all 300 declared
hashes were reverified, not rerun. This research changes no runtime behavior, architectural
status, maturity, release authority or whole-W3 completion claim. Prior wording is retained.

## W3.2b2d1 stopped resource ownership, 2026-09-08

Cleanup authority derives from an authenticated original intent, exact returned full ID, bound local engine, creation time and complete inspected configuration digest. Names, labels, saved host PIDs and an erased content key alone grant no authority. Corrupt rows, interior gaps, changed configuration/fence or host-key rotation refuse cleanup. Trusted local operator/host/daemon boundaries, valid-prefix rollback and whole-database/key rollback remain explicit limitations; there is no unauthenticated remote cleanup surface.

See the [plain-language report](../../reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.json),
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[unit cases](/Users/arunmenon/projects/adrl-core/tests/unit/test_resource_owner.py),
[local engine cases](/Users/arunmenon/projects/adrl-core/tests/integration/test_resource_engine.py)
and [runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
All 812 tests and eleven engineering checks pass, with 306 declared source hashes unchanged
during the run. This supports the scoped tested behavior only. Prior decision wording,
architectural status and maturity fields remain unchanged; full B2/B3 and W3 remain open.

## W3.2b2d2 launch-contract research and identity gate, 2026-09-08

A future active owner must preserve the original authenticated stopped binding while applying a separately versioned, capability-specific execution identity comparison. Names, labels or merely default-looking changes cannot grant cleanup or launch authority. The observed false/null OOM-control transformation has a concrete source explanation; its candidate exception and the proposed one-shot/abort authority still require acceptance tests. Runtime trust boundaries and stopped-only authority remain unchanged.

See the [plain-language progress report](../../reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md),
[failed-run/source evidence](../../reports/research/adrl-w3-2b2d2-launch-contract-2026-09-08.json),
[proposed execution contract](../../reports/waves/w3-isolated-execution-contract-v1.md),
[next identity packet](../../reports/waves/w3-2b2d2-identity-compatibility.md), and the unchanged
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py) and
[runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
No runtime source changed: the 812-test/eleven-check baseline is reused with all 306 declared
hashes verified. No new passing runtime run is claimed. Prior wording, architectural status
and maturity remain unchanged. Active launch, full d/B2/B3 and W3 remain open.

## W3.2 execution identity and launch research, 2026-09-08

A complete original inspection and pinned engine/capability profile govern the research comparator. Only unsupported OomKillDisable false/null is normalized; changes to other controls or identity fail. The seven successful synthetic observations justify a scoped engineering next step, not trusting a done message, daemon restart counter or raw research digest as a verified task boundary. Host/daemon trust and independent-review limits remain explicit.

See the [plain-language report](../../reports/adrl-w3-execution-identity-2026-09-08.md),
[research evidence](../../reports/research/adrl-w3-execution-identity-2026-09-08.json),
[comparator](../../reports/research/execution-identity-2026-09-08/execution_identity.py),
[offline cases](../../reports/research/execution-identity-2026-09-08/test_execution_identity.py),
[driver](../../reports/research/execution-identity-2026-09-08/run_probe.py) and
[next runtime packet](../../reports/waves/w3-isolated-launch-runtime.md).
101 offline research cases and seven engine observations pass. The unchanged runtime's
812-test/eleven-check baseline is reused with 306 verified hashes. Prior decision text and
all status/maturity fields are preserved; no grade promotion, independent review or full-W3
completion follows.

## W3.2 one-shot fixture runtime prototype, 2026-09-08

Runtime execution references are now host-authenticated against the original stopped binding, exact configuration projection and pinned engine/fixture profile. Malformed exit state, changed StartedAt or unsafe identity changes refuse qualification/cleanup. A 404 from engine-info cannot become an absence receipt. A lost original create reply remains unbound; the one-off operator cleanup was not adopted into runtime authority. Independent qualification and full workflow acceptance remain open.

See the [report](../../reports/adrl-w3-isolated-launch-2026-09-08.md),
[checks and failed-run evidence](../../reports/research/adrl-w3-isolated-launch-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[pinned transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[permanent markers](/Users/arunmenon/projects/adrl-core/src/adrl/core/launch_markers.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_isolated_execution.py),
[runtime guide](/Users/arunmenon/projects/adrl-core/docs/isolated-execution.md) and
[next diagnosis packet](../../reports/waves/w3-launch-create-receipt-diagnosis.md).
Final offline validation: 861 passed, eight opt-in engine cases skipped, all eleven checks;
315 declared hashes stable. Two engine invocations each had three passes and one failure.
The allowance is closed and all eight fixtures/image are absent. All prior wording and
77 status/maturity fields are preserved. No independent review, grade promotion or full-W3
completion follows.

## W3.2 receipt correction and pinned-engine validation, 2026-09-08

Original full-ID custody, strict engine/projection binding and one-shot authority survive the timeout correction. V1 history is read under its recorded profile, rather than silently granted v2 semantics. The new finite engine packet passed without unreceipted resources or operator adoption. The previous failure remains unexplained and independent review is still unassigned.

See the [plain-language report](../../reports/adrl-w3-transport-receipts-2026-09-08.md),
[checks and cleanup evidence](../../reports/research/adrl-w3-transport-receipts-2026-09-08.json),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[versioned execution policy](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[receipt fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_create_receipt.py) and
[next custody packet](../../reports/waves/w3-active-copy-custody.md).
Final validation: 895 passed, zero skipped, all eleven checks, 316 stable source inputs;
13 original create receipts and absence confirmations, one image removed. The bounded d2
synthetic lifecycle slice closes. Full B2/B3/W3, real-harness and independent qualification
remain open. Prior wording and all 77 architectural status/maturity fields are preserved.

## Context and rationale

SAF-008 correctly observed that where the code lives is known before the first prompt with lookup-table precision. It then keyed the lookup on values the harness composes from files in the developer's checkout: the environment block of the system prompt, the CLAUDE.md path, the git remote as printed by a tool. Those are exactly the values a developer who wants to route restricted code to a cheap cloud rung would edit, and the implementation confirmed the consequence: identity was a regex over prompt text with substring matching, and an unmatched repository fell to a default class that permits a cloud rung. A signed manifest cannot protect restricted code if its lookup key is attacker-controlled.

The correction is the one used by every workload-identity system: identity is asserted by a component that the subject does not control and that has an authoritative inventory to check against. For a developer laptop that component is the launcher, which OPS already controls for telemetry and sandbox configuration, and the inventory is SCM. Corroboration by content fingerprint catches the two failure modes an assertion alone leaves open: a stale inventory and a checkout copied to an unregistered path. Making unknown identity local-only rather than default-class follows the register's own rule for pins: the safe state must not depend on a later judgement.

## Adversarial review (2026-09-03)

### Steelman
This is the only design under which the classification manifest's signature means anything. Every other input to the gate is either content (scanned by SAF-003 with measured precision) or configuration signed by security; identity was the one input that was neither, and it is the input that gates the highest-consequence repositories. A launcher assertion is cheap, is already the mechanism by which OPS injects sandbox and telemetry settings, and moves the trust boundary to where it can be audited.

### Attacks (self-applied, as this is a proposal)
1. **The launcher is bypassable.** A developer can run the harness binary directly. Mitigation: without an assertion the lineage is local-only, which is safe; OPS may additionally require the assertion for gateway access (the gateway rejects sessions with no assertion id), which converts bypass into denial rather than leakage.
2. **Content fingerprints drift with every commit.** A digest over the whole tree changes constantly. Mitigation: the fingerprint covers a manifest-declared stable set (root manifest, lockfile, a marker file), is versioned with the manifest, and a mismatch tightens rather than blocks.
3. **Subagent worktrees and monorepos.** A worktree checkout of a restricted monorepo directory has the parent's identity; TRU-001 inherits identity down the lineage and lets restricted path prefixes tighten further, exactly as SAF-008 clause 1 and its attack 3 already provided.
4. **The assertion becomes a new secret.** A signed assertion bound to a session key could be replayed to another session. Mitigation: bind to the harness process identity and session HMAC, short validity, and record the assertion id in the egress ledger (TRU-003) so replay is visible.
5. **Local-only for unknown identity will push developers to disable ADRL** (the Q5 argument). Mitigation: unknown identity is an OPS onboarding defect, not a steady state; the register accepts the cost, as it did for pins, because the alternative is unauditable.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P0-2, verified: `gates/repo_class.py` derives identity by regex over the system prompt and the first 4000 characters of tool text with substring matching; unknown repositories fall to a default class permitting `cheap_cloud`.
- ADRL-SAF-008 (this register), attack 1: "Repository identity is spoofable from the harness side"; the mitigation proposed there (corroborate with content fingerprints) was not implemented and is insufficient alone because the fingerprint compares against a manifest keyed by the same spoofable identity.
- Microsoft Learn, "Learn about sensitivity labels" (Purview): labels are applied to containers by policy, not read from the content's own claims - https://learn.microsoft.com/en-us/purview/sensitivity-labels (fetched in the 2026-09-02 review)
- Debenedetti et al., CaMeL (arXiv 2503.18813): control decisions are taken from trusted sources, never from data the untrusted party can shape - https://arxiv.org/abs/2503.18813 (cited by the 2026-09-03 external review; not independently fetched)

### Verdict
**PROPOSED (new).** Supersedes the identity half of SAF-008 (clauses 1 and 4, and attack 1's mitigation). Self-applied attacks 1 and 5 bound the cost; 2 to 4 shape the design. Recommended for acceptance at D0 with the follow-ups as the D1 exit.

## Amendments applied

New decision; no prior text. SAF-008 status line updated to "superseded in part by TRU-001, pending disposition".

## Follow-ups

- [ ] OPS: choose the launcher mechanism (wrapper script, devcontainer hook or device agent) and define the assertion schema (repository id, manifest version, session HMAC, process id, validity, signature).
- [ ] Security: publish the SCM inventory endpoint and the fingerprint file set per repository class in `repo-classification-v2.json`.
- [ ] Implementation: remove prompt-text identity resolution from the gate; keep prompt-observed paths as keyed, tighten-only evidence; unknown identity ceiling = local; `identity_unknown` and `classification_conflict` egress events.
- [ ] Adversarial tests: system prompt claiming an unrestricted working directory while the assertion names a restricted repository (assertion wins); no assertion (local-only); replayed assertion from another session (rejected, egress event); fingerprint mismatch (stricter class).
- [ ] Gateway: optionally reject sessions whose requests carry no assertion id (Q7).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded versioned creation/active transport separation and passing pinned-engine lifecycle acceptance | Prior decision/evidence preserved; bounded d2 closes, full W3 and grades unchanged |
| 2026-09-08 | Recorded W3.2 fixture launch prototype, offline checks, engine failures and operator cleanup exception | Prior decision/evidence preserved; engine workflow remains unqualified, no status/maturity promotion |
| 2026-09-08 | Recorded W3.2 identity correction and seven accepted bounded launch observations | Prior wording and failed evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d2 failed launch probes, source-explained identity gate and proposed lifecycle | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d1 stopped ownership, acknowledgement recovery and explicit limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2b2 stop coordination, permanent workspace blocking and failure evidence | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2b1 key-revocation ordering fix, fault evidence and remaining recovery limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b1 process ownership and tested cleanup limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-09-07 | Recorded applied observation mode and the first live subscription pilot | Decision policy and status unchanged; prior evidence was offline or synthetic, with observation-only launch still planned |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-09-07 | Recorded the distinction between correlation, workload authority and distribution discovery; no new credential service or maturity claim | Decision text and Proposed status unchanged; no product discovery scope note previously recorded |
| 2026-09-03 | Proposed (external review) | none |
