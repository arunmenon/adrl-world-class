# ADRL implementation stack (proposal, 2026-09-02)

Status: proposal for approval. Implements the register as amended on 2026-09-02 (55 ADRs, six Proposed).
Scope: a brand-new Python implementation. The prior code in `~/projects/adrl` is treated as a corpus of lessons and fixtures, not as a base.

## 1. What the ADRs force on the stack

Nine properties fall directly out of the decision text and decide most stack choices.

| Property | Source | Consequence for the stack |
|---|---|---|
| Byte-exact relay on the passthrough and frontier path, including SSE `ping` and upstream error wording | FND-001 | The HTTP layer must forward the original request bytes and stream response bytes untouched. No framework-level body model on the hot path. |
| Every request of every class is gated; routing happens once per user turn | FND-003, SAF-001, SEM-001 | A per-request pipeline with a gate stage that runs on continuations (about 15x more often than turns) with a p99 budget. |
| Pin is durable across restart, written before the pinning request is forwarded | SAF-002 | Synchronous write-through to disk on the gate path. State cannot live only in process memory. |
| Egress ledger is write-ahead, hash-chained, content-free, and not behind the fail-safe facade | SAF-009 | A second, independent store with stricter durability than the evidence ledger. |
| Evidence ledger is strictly append-only with schema versions, idempotency keys and upcasters | MEM-001 | An event store, not an ORM-managed mutable model. Single writer, WAL, `BEGIN IMMEDIATE`. |
| Rung membership and fallback groups are one shared versioned config consumed by both ADRL and the gateway | FND-002, RTG-008 | ADRL owns `rungs.yaml` and generates the LiteLLM config from it, with CI checks. |
| No re-issue after the first streamed tool content; served model recorded from the response | CAS-003, CAS-006 | The relay must observe the stream it forwards (tee), never buffer it. |
| Verification runs in an OS-enforced sandbox with no egress | SAF-007 | Seatbelt on macOS, bubblewrap on Linux, `unverifiable` elsewhere. |
| Embeddings and hashes are prompt-class data, crypto-shreddable per session | MEM-005, MEM-010 | Local keystore, per-session AES keys, keyed HMAC for hashes. |

## 2. Stack decisions

| Layer | Choice | Why this and not the default |
|---|---|---|
| Python | 3.12, managed by `uv`, lockfile checked in, pure wheels only | Same constraint as the prior repo: the Mac has no compiler. |
| HTTP server | Starlette on uvicorn, raw ASGI routes | FastAPI is Starlette plus pydantic route validation. Validation would re-serialise bodies, which FND-001 forbids on the passthrough path. Pydantic is still used, but for config and ledger records, not for the wire. |
| Upstream client | httpx async with streaming | Relays `aiter_raw()` chunks verbatim while a parallel SSE observer parses the same bytes for `tool_use` starts, `message_start.model`, and `message_delta.usage`. |
| Wire models | `json.loads` for inspection only; original bytes forwarded; re-serialisation only on the rewrite path for non-Claude rungs | Keeps the removal test (FND-001) honest: frontier traffic is bit-identical with and without ADRL. |
| Evidence ledger | SQLite via stdlib `sqlite3`, one writer thread owning the connection, hand-written numbered migrations under `user_version` | An ORM hides `UPDATE`; an event store with two tables and a CI grep for `UPDATE`/`DELETE` makes MEM-001 mechanically checkable. The single writer thread is the concurrency contract MEM-006 asks for. |
| Egress ledger | Separate SQLite file, `synchronous=FULL`, hash chain in `hashlib`, HMAC lineage ids, Ed25519 checkpoints via `cryptography` | Separate file so its availability semantics differ from the evidence ledger, as SAF-009 requires. |
| Secret detection | `detect-secrets` (Yelp) plugins, wrapped in a tiered scanner | Pure Python, per-plugin detector ids map onto SAF-003 tiers, and LiteLLM's own `detect_secrets_config` uses the same library, so the FND-002 ruleset diff is a config comparison. PII tier via Presidio as an optional extra, off by default. |
| Tokenizers | HF `tokenizers` for the local model, Anthropic `count_tokens` for calibration | SAF-006 needs a local estimate with a measured per-rung ratio, and pinned `count_tokens` must be served locally. |
| Gateway | LiteLLM proxy, config generated from `rungs.yaml` | ADRL never names a model in policy. Frontier traffic keeps the harness's model name in the body; cheap_cloud and local traffic use rung aliases because those bodies are rewritten anyway. |
| Sandbox | `sandbox-exec` Seatbelt profile on macOS, bubblewrap on Linux, behind a `SandboxRunner` port | Reuses the harness's mechanism without a Node dependency. Snapshot via `git worktree add --detach`. |
| Embeddings | `model2vec` static embeddings (NumPy only) behind an `Embedder` port; NumPy index | Shadow-only per MEM-008. Avoids torch. Can swap for an ONNX model later without touching the ledger. |
| Crypto | `cryptography` (AES-GCM per session, Ed25519 checkpoints), `hmac` from stdlib | Per-session keys in a `0600` keystore file, rotatable, shredded on erasure. |
| Config | pydantic-settings plus YAML/JSON files, each with an explicit version field | Every "versioned policy constant" in the ADRs becomes a field on a versioned config model, recorded on decision rows. |
| Telemetry | structlog JSON, `prometheus-client` metrics, OpenTelemetry GenAI semantic-convention attribute names | Q7 asks for shared telemetry with the gateway via GenAI semconv. |
| CLI | `typer` | `adrl serve`, `adrl audit --lineage`, `adrl release`, `adrl config check`, `adrl gateway-config`, `adrl verify`. |
| Learning | NumPy, scikit-learn, hand-written X-learner and isotonic/conformal calibration | LRN-003 is D0 and gated. Only the abstention harness and feature snapshots ship in v1. |
| Tests | pytest, pytest-asyncio, httpx ASGI transport, respx, hypothesis, a fake LiteLLM upstream app | No containers needed. Property tests for gate monotonicity and append-only. |
| Quality | ruff, mypy strict, pre-commit | Per the Python stack playbook. |

Dependencies, runtime: starlette, uvicorn, httpx, pydantic, pydantic-settings, pyyaml, structlog, prometheus-client, detect-secrets, tokenizers, cryptography, typer, numpy. Optional extras: model2vec, presidio-analyzer, scikit-learn, opentelemetry-sdk. Dev: pytest, pytest-asyncio, respx, hypothesis, ruff, mypy, pre-commit.

## 3. Package layout, one package per ADR bucket

The prior repo's `AGENTS.md` requires every task to name one primary ADRL ID. The new layout makes that structural: a module lives in the package of its primary bucket.

```
adrl/                                  new repository (src layout)
  pyproject.toml  uv.lock  .python-version
  config/
    rungs.yaml                         rung-membership-v1: rungs, members, boundaries, evidence refs   (FND-002, RTG-001)
    policy.yaml                        tau_by_rung, bands, precision thresholds, budgets              (RTG-002/003/004)
    prices.yaml                        per-rung price vectors, cache TTLs                              (RTG-009)
    provider-pairs.yaml                cross-model handoff rule table                                  (CAS-004)
    tripwires.yaml                     per-rung, per-wire thresholds                                   (CAS-001)
    repo-classification-v1.json        signed manifest                                                 (SAF-008)
    learning-contract-v1.json          feature schema, deny-list, tier rules                           (LRN-004/005)
    utility-fingerprints.yaml          versioned system-prompt shapes                                  (SEM-004)
  src/adrl/
    wire/        SEM   request parsing, six request classes, content_bearing, session key, lineage, SSE observer
    gates/       SAF   gate pipeline, repo classification, secret scanner, pin, feasibility, block contract, egress ledger, sandbox
    routing/     RTG   rung registry, band policy, cost model, advisory classifier port, decision record
    cascade/     CAS   action boundary, trip-wires, sticky state, handoff transform, escalation controller, error surfacing
    ledger/      MEM   event store, migrations, outcome lifecycle, labels, projections, facade, keystore, retention
    learning/    LRN   feature snapshot, evidence tiers, pair harness, abstention, artifact manifest, exploration logging
    proxy/             ASGI app, pipeline composition, upstream client, body rewrite, modes
    config/            versioned config models, loaders, load-time checks
    telemetry/         structlog setup, metrics, semconv attribute names
    cli/
  tests/
    fixtures/wire/     scrubbed golden requests: pre-warm, title, topic-detect, compaction, fork, parallel tool_use
    unit/  integration/  faults/  adversarial/  removal/
  tools/
    gen_litellm_config.py              rungs.yaml to LiteLLM config                                    (FND-002)
    check_config.py                    CI: rung-closed groups, 100k compaction feasibility, evidence refs
    check_ledger_discipline.py         CI: no UPDATE/DELETE, no shadow imports into live routing       (MEM-001, MEM-008)
    check_learning_contract.py         CI: deny-list, no served_rung target                            (LRN-004)
```

## 4. Request pipeline

Every request follows one path. Stages are ports with one production adapter each, so shadow mode and fault injection swap adapters rather than branch.

1. Ingress: read full body bytes, `json.loads` a read-only view, capture headers.
2. Classify (SEM-001): path, final block type, `max_tokens`, tool-list presence, fingerprint, `x-claude-code-*` headers. Emit `request_class`, `content_bearing`, `interaction_mode`.
3. Identity (SEM-002, SEM-006): session key by preference order, HMAC at rest, lineage = session plus agent chain. Acquire the per-lineage lock so three parallel siblings cannot lose writes.
4. Gates (SAF-001), in order, each shrinking the permitted set: repo class ceiling (SAF-008), new-content secret scan (SAF-003), feasibility (SAF-006). Pin write-through to both ledgers before anything is forwarded. Gate exception resolves per FND-004 by pin state and failure class.
5. Egress ledger write-ahead (SAF-009). Append failure on a pinned lineage is a gate failure.
6. Route or inherit (FND-003, SEM-003): user turn gets a fresh decision inside the permitted set (RTG-002/003, RTG-004 cascade feasibility, RTG-006 advisory only in the ambiguous band); every other class inherits the sticky route. Mint `route_id`, write the decision row with features snapshot, estimator, policy and objective versions.
7. Cascade checks (CAS-001/003/005): is this an action boundary, did the previous response fire a trip-wire, is escalation sticky. Escalation applies the provider-pair transform (CAS-004) and appends the handoff note.
8. Dispatch (FND-001, FND-002): frontier path forwards original bytes and the harness's model name; other rungs get the rewrite (strip `thinking`, `cache_control`, beta fields; set rung alias) and go to the gateway with rung-closed fallback groups. Exactly one attempt (CAS-007).
9. Relay and observe: stream bytes back untouched while the observer records first streamed `tool_use`, served model and provider (`x-litellm-model-id` header first, then `message_start.model`, else `assumed_intended`), usage including cache tokens (RTG-009).
10. Outcome events (MEM-002/003/004): `pending` on send, `closed_turn` at the next boundary, `closed_final` by `close-v1`, typed with `failure-types-v2` and the precedence rule.

Modes are per subsystem, not global: `gates: enforce | observe`, `routing: off | shadow | live`, `fallback: off | shadow | live`. The first deployment target is gates enforced, routing shadow, which matches the register's own posture (live routing blocked).

## 5. Ledger schema (first cut)

Evidence ledger `adrl.db`:

- `decisions(route_id PK, ts, session_hmac, lineage_hmac, request_class, content_bearing, permitted_set, decided_rung, estimator, estimator_version, policy_version, objective_version, cascade_feasible, cascade_reason, features_json, propensity, explore_version, schema_version)`
- `events(seq PK, route_id, event_type, producer, producer_seq, ts, schema_version, payload_json, UNIQUE(route_id, event_type, producer, producer_seq))`
- `lineage_events(seq PK, lineage_hmac, event_type, ts, payload_json)` for `pinned`, `released`, `classified`, `boundary_candidate`
- `embeddings(route_id, session_hmac, ciphertext, embedder_version)` and `session_keys(session_hmac, wrapped_key, created_ts, erased_ts)`
- `projections(name, high_water_seq, embedder_version, code_version, state)`

Egress ledger `egress.db`:

- `egress_events(seq PK, prev_digest, ts, lineage_hmac, request_class, content_bearing, destination_rung, deployment_tag, gate_verdicts_json, detector_tier, span_hashes_json, bytes_out, actor, reason, digest)`
- `checkpoints(seq, digest, signature, ts, shipped_ts)`

No `UPDATE` or `DELETE` statement exists in `src/`. Erasure is key deletion plus an `erased` event. The `outcomes` current-state view is a projection routine, never written by hand.

## 6. Decisions the ADRs leave to the implementer, with the default taken here

| Question | Default in v1 | Recorded where |
|---|---|---|
| Empty-but-valid response for cosmetic utility on a pinned session | Non-streamed `message` with one empty text block, `stop_reason: end_turn`, `usage` zeros | `gates/block.py`, SEM-004 |
| `count_tokens` on a pinned session | Local tokenizer estimate times the rung ratio, returned in Anthropic shape | `gates/feasibility.py`, SEM-001 |
| Pre-warm before any sticky route exists | Forward unchanged to the harness's requested model (no decision yet); it is not a boundary | `proxy/pipeline.py`, FND-003 |
| Block form | `capability_rejected: prompt_too_long` token plus the vendor's too-long phrase, both in the message | `gates/block.py`, SAF-005 |
| `close-v1` parameters | 3 subsequent turns or 30 minutes idle or episode boundary | `config/policy.yaml`, MEM-002 |
| Local attempt budget unit | Tool calls (default 12) with a wall-clock cap | `config/policy.yaml`, RTG-004 |
| Tree identity | Content hash of touched files, plus HEAD commit | `ledger/verification.py`, MEM-003 |
| Default repository class for unknown repos | `default`: cheap_cloud ceiling, no residency constraint, release permitted | `config/repo-classification-v1.json`, SAF-008 |
| Sticky state location | Behind a `StateProvider` port with a SQLite adapter; in-memory cache rebuilt on start with `state_loss=true` when a lineage is unknown | `ledger/state.py`, MEM-006, CAS-006 |
| Hook sidecar for `PostToolUseFailure` | Not in v1; wire-shape discrimination only, gap recorded | CAS-001 follow-up |
| Retention figures | 90 days prompt-class, 24 months skeleton | `config/policy.yaml`, MEM-010 |

Every default is a versioned config field, so changing one is a config version bump, not a code change.

## 7. Build phases

Each phase ends with a measured check, not with component presence (FND-005).

| Phase | Delivers | Exit check |
|---|---|---|
| 1 Transparent skeleton | Proxy, classification, identity, byte-exact relay with observer, both ledgers, config models, CLI skeleton, fake gateway for tests | Removal test passes: golden traffic is byte-identical with and without ADRL. All six classes classified on fixtures. |
| 2 Gates | Secret scanner with tiers, durable pin, audited release, repo classification, feasibility, block contract, fail-open matrix | Pin survives SIGKILL. Fault-injection matrix from FND-004 passes. Adversarial suite from SAF-001 runs (results published, not required to pass). |
| 3 Routing and cascade | Rung registry, bands, cost model, sticky state, trip-wires, boundary, provider-pair transform, escalation, LiteLLM config generator and CI checks | Parallel-tool replay cases from CAS-003 pass. Provider-pair replay returns 2xx on every pair. Config checks fail on a cross-rung group. |
| 4 Evidence | Outcome lifecycle, labels with precedence, sandboxed verifier, projections, keystore and erasure | Pin at turn 4 shreds turns 1 to 3 and rebuilds the index. Sandbox fault tests pass. Incremental equals full rebuild. |
| 5 Learning scaffolding | Feature snapshot column, tier assignment, pair harness, abstention harness with stub estimator, exploration logging | CI rejects a manifest with `served_rung` as target. Non-explored turns log propensity 1.0. |

Phases 1 to 3 are the runtime. Phases 4 and 5 are the flywheel and can follow once shadow traffic exists.

## 8. Risks worth naming now

- The gateway contract (served identity header, retry budget, alias subsets) is pending agreement with the gateway team. v1 implements it as config with `assumed_intended` as the fallback.
- Utility fingerprints are corpus-derived and break on harness upgrades. They are versioned and header detection is preferred; the divergence counter is a first-class metric.
- The RTG-009 episode-length estimator needs a shadow corpus. v1 ships a constant estimator with its version recorded, so cost figures are labelled and replaceable.
- `detect-secrets` precision has to be measured on representative traffic before tiers are trusted. v1 ships provisional tiers and a measurement tool.

## 9. As built (2026-09-02)

The implementation lives at `~/projects/adrl-core`. Every choice in section 2 was kept. Additions made during the build: `config/detectors.yaml` (detector tiers with provisional precision), `config/gateway-endpoints.yaml` (generator input), `docs/adr-module-map.md` (generated from module docstrings by `tools/adr_module_map.py` against the register; on 2026-09-03 the register holds 77 decisions, 73 are cited by at least one module, and the honest unmapped list is EVL-001, EVL-008, RTG-007 and SEM-007, which have no implementing code yet), and `docs/known-gaps.md` (what the first build leaves open, by ADR). Defaults from section 6 were recorded as config fields as promised. The end-to-end suite under `tests/integration/e2e/` exercises the composed system with real stages against a fake gateway, including pin on a leaked key, restart durability, trip-wire escalation with handoff, and the byte-identical removal test in shadow mode.
