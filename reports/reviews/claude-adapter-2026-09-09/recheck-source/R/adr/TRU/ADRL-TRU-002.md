# ADRL-TRU-002 - Permitted deployment set (Proposed)

| Field | Value |
|---|---|
| Bucket | TRU - Trust, Residency and Egress |
| Status | Proposed 2026-09-03 (new, from external review) |
| Maturity | D0 Design, review recommends D0 Design (the 2026-09-02 implementation tightens a set of rung labels; nothing compares a deployment's geography or host to policy) |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 7 |
| Related decisions | FND-002 (amended), RTG-008, RTG-001 (amended), SAF-001, SAF-002, SAF-004, SAF-006, SAF-008 (superseded in part), CAS-006, TRU-001, TRU-003, RTG-009 |
| Open questions | Q1, Q2, Q7 |

## Decision

The object that the gates tighten and that routing chooses from is the permitted deployment set: a subset of a signed, versioned endpoint inventory in which every entry names a deployment id, its rung, provider, `api_base`, trust zone, geography and data-use profile; a rung is the economic tier of a deployment, not a security boundary, and no policy, pin, residency rule or fallback may be expressed in terms of a rung alone.

1. *Inventory*: `deployment-inventory-v1` is signed by security and shared with the gateway generator (FND-002). An entry is `{deployment_id, rung, provider, api_base, trust_zone, geo, data_use_profile, evidence_ref}`. A `local` rung entry must have a loopback or unix-socket `api_base` and `trust_zone: local_host`; the configuration checker rejects any other local entry.
2. *Tightening*: TRU-001 identity, residency, the SAF-002 pin and SAF-006 feasibility each remove deployments, never rungs: a pin removes every deployment whose `trust_zone` is not `local_host`; a residency tag removes every deployment whose `geo` does not match; a data-class restriction removes every deployment whose `data_use_profile` is not approved for the class. The set is monotone within a lineage (SAF-001).
3. *Gateway contract*: the gateway generator emits one model group per deployment and fallback groups only within the permitted-set-closed subsets that ADRL names per request (a pinned lineage's group contains only `local_host` deployments); alias fallback lists must be subsets of the inventory. This replaces "rung-closed" in FND-002 and RTG-008 with "deployment-set-closed".
4. *Receipt*: every dispatch yields a served-deployment receipt (`deployment_id`, provider, `api_base` host, `geo`, `trust_zone`, source in {gateway_reported, proxy_observed, assumed_intended}) recorded on the outcome row (CAS-006) and in the egress ledger (TRU-003). An `assumed_intended` receipt on a pinned or residency-tagged lineage is a gate failure for the next request until a reported receipt arrives.
5. *Routing inside the set*: RTG chooses among the permitted deployments by rung economics (RTG-002, RTG-009); cost and cache identity are keyed by deployment id, because caches and signatures are per endpoint.

## Context and rationale

FND-002 bound the gateway to serve a request only from "the capability rung ADRL selected" and made rung membership shared configuration. That was the right split for economics and the wrong object for safety. "Local" in SAF-002, SAF-004 and SAF-005 means "the content does not leave this machine"; "in-region" in SAF-008 means "this endpoint is in this geography". Both are properties of an endpoint. The implementation showed what happens when they are expressed as a rung name: a local model group whose `api_base` was changed to an external HTTPS host passed every configuration check, the egress ledger reported its traffic as never having left the machine because the destination rung was `local`, and residency was a field that nothing read. Making the deployment entry the unit of policy closes all three at once: the local entry is loopback by construction, residency is a filter on `geo`, and the ledger records what was served, not what was intended.

## Adversarial review (2026-09-03)

### Steelman
Every hard property in SAF becomes checkable configuration: the local rung cannot silently become remote, residency becomes a set difference, the gateway's fallback groups become provably closed, and the egress ledger records receipts rather than intentions. It keeps the FND-002 split intact (ADRL still does not pick a model), it keeps RTG's three rungs as economic tiers, and it gives RTG-009 the per-endpoint cache identity it already needed.

### Attacks (self-applied)
1. **Receipts can be forged by the gateway.** The served-model header is written by the gateway. Mitigation: the gateway is inside the trust boundary for economics but not for residency; for residency-tagged and pinned lineages, `proxy_observed` evidence (the resolved `api_base` host ADRL connected to, TLS peer) is required alongside the header, and the gateway's own inventory attestation is a Q7 contract item.
2. **Inventory churn breaks routing.** Endpoints change daily. Mitigation: the inventory is versioned; ADRL and the generator refuse to run on mismatched versions; adding a deployment is a signed change, as SAF-008 required for the manifest.
3. **Deployment-level policy explodes the configuration.** Mitigation: policy is written against attributes (`trust_zone`, `geo`, `data_use_profile`), not deployment ids; the set is computed.
4. **Cache-aware cost is now per deployment and thin.** Mitigation: RTG-009 already needed this; a deployment with no cost history uses its rung's price vector and is labelled as such.
5. **`assumed_intended` on a pinned lineage blocks everything after a restart.** Mitigation: clause 4 fails only until one reported receipt arrives; a local deployment that never reports identity is a configuration error surfaced at start.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P0-1, verified: `residency` is carried but never read; a local group repointed at `https://exfil.example.com/v1` passes all eight configuration checks; `lineage_left_machine` filters on `destination_rung != 'local'`.
- ADRL-FND-002 and ADRL-RTG-008 (this register): "rung membership of every endpoint is a shared, versioned configuration" and "served identity reported on every response"; both are kept and re-keyed to deployments.
- AWS Bedrock cross-region inference documentation: geographic versus global inference profiles are endpoint properties - https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html (fetched in the 2026-09-02 review)
- LiteLLM, "Fallbacks (Provider Failover)": fallback groups are lists of model groups, so closure is a property of the generated configuration - https://docs.litellm.ai/docs/proxy/reliability (fetched in the 2026-09-02 review)
- "Bounded Agents" (arXiv 2608.15888): monotone delegated authority as the shape of a permitted set - https://arxiv.org/abs/2608.15888 (cited by the 2026-09-03 external review; not independently fetched)

### Verdict
**PROPOSED (new).** Supersedes the residency half of SAF-008 (clause 2) and amends FND-002, RTG-008 and RTG-001. Attack 1 sets the Q7 contract item; attacks 2 to 5 shape the design. Recommended for acceptance at D0.

## Amendments applied

New decision; no prior text. FND-002 and RTG-001 amended in place on 2026-09-03 to cite this decision; RTG-008 to be amended on disposition.

## Follow-ups

- [ ] Security and the gateway team: publish `deployment-inventory-v1` (schema above) and its signing key; generator consumes it; CI rejects a local entry that is not loopback or unix-socket.
- [ ] Implementation: `PermittedSet` becomes a set of deployment ids computed from attributes; pins, residency, data class and feasibility tighten it; routing chooses among entries; egress and outcome rows carry the receipt.
- [ ] Adversarial tests: local entry with a remote host rejected at load; residency-eu lineage never dispatched to a `geo: us` deployment; pinned lineage after restart with `assumed_intended` receipt blocked until reported; gateway header naming a deployment outside the request's set is an `infrastructure` event and a gate failure for pinned lineages.
- [ ] RTG-009: key cache state by deployment id.
- [ ] Q7: gateway attestation of its inventory version on every response.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-09 | <!-- taxonomy-sync:claude-adapter:ADRL-TRU-002 --> [Offline candidate](../../reports/reviews/claude-adapter-2026-09-09/report.md); Configured target must match the inventory catalog and the actual permitted deployment set, with frontier rung, Anthropic provider, direct api.anthropic.com host and non-local trust zone. Pinned and fallback requests are refused. The transport fixes its origin and refuses redirects. This does not qualify a signed live profile or workspace. | Prior decision wording preserved; no grade change |
| 2026-09-03 | Proposed (external review) | none |


## Claude initial-choice candidate, 2026-09-09

<!-- taxonomy-sync:claude-adapter:ADRL-TRU-002 --> Configured target must match the inventory catalog and the actual permitted deployment set, with frontier rung, Anthropic provider, direct api.anthropic.com host and non-local trust zone. Pinned and fallback requests are refused. The transport fixes its origin and refuses redirects. This does not qualify a signed live profile or workspace. [Evidence and limits](../../reports/reviews/claude-adapter-2026-09-09/report.md). Formal grades and status unchanged.
