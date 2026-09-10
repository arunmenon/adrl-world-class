Independently reconcile original fable-retrospective-2026-09-08 findings RV-01 through RV-06. This is review-ledger evidence reconciliation, not implementation. Determine each disposition using original acceptance criteria, original Fable RV-01 recheck (conditional on checks-2), actual retained final check logs/source hashes and current relevant code. Current focused regression 11 passed recorded honestly by coordinator. Do not infer every consumer is repaired. RV-02/03/04/05/06 may remain unresolved; code improvements are not requested. Original hashes preserved, no historical finding edits or owner waivers. For RV-04 distinguish disclosure in one later report from required propagation. For RV-01 distinguish scoped producer-to-closer/readiness repair from complete learning. Respond JSON only, max 650 words: review_id rv-reconciliation-2026-09-10; verdict; summary; reconciliations array with global_id, disposition (verified-fixed or unresolved or disputed-with-evidence), scope, evidence; findings array for NEW review issues only (id,global_id,severity,kind,blocking,confidence,owning_adrs,title,evidence,acceptance_criteria,appendix_refs). Do not assign new IDs to old findings. Name exact global IDs verified. No tools, no delegation, no maturity promotion, no permission or live experiment. This is the independent critical-review skill applied to a bounded reconciliation.

FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/recheck.md
**Verdict: RV-01 is repaired for its stated scope. No material blockers remain. Final resolution is contingent on the concurrent full checks-2 run being green, which I have not seen.** This recheck is from reading the supplied source, tests, dispositions and logs. I ran nothing.

## Blockers from the original critique

- **None coercion: withdrawn.** RequestContext declares session and lineage as non-optional SessionId and LineageId in `src/adrl/core/types.py`. Both are NewType over str in `src/adrl/core/ids.py`, and the identity functions always return hex digests. The str() wrap is a no-op. No guard or None test is needed. This is a note, not a blocker.

- **Route divergence on continuation: demonstrated.** The parametrised continuation test now replaces the current decision's route id at the finalize boundary while the plan keeps the sticky route. The closed_turn is asserted to land on the sticky route with cascade producer and sequence 2, on both direct and forwarded paths. Under the old re-keying, the row would have landed on the altered decision route, so the test discriminates. The divergence is induced by patching rather than produced by a real continuation, and the test comment says so. That is adequate for the invariant being claimed.

## Evidence gaps from the original critique

- **Pre-seeded forwarding scope: closed.** The contract doc now states forwarding is tested with a pre-seeded counter and does not qualify cold-start forwarding. The idempotency-key collision on a no-ledger restart remains an accepted, documented limitation.

- **Inert TypeError guard: closed.** The dropped-forwarded-event test asserts that event_dropped appears and finalize_failed does not. Since the same forwarding lines execute, this shows the names resolve and the pipeline ledger is the facade. It tests the pipeline's handling of a False return, not the store's real duplicate-key behaviour. The original helper also treats False as dropped, so the assumption is consistent with existing code.

- **Idle timing: closed.** The composed test pins subsequent_turns to 100 and idle_minutes to 30, then scans one day ahead. Only idle can fire.

- **Bypassed helper: closed.** The supplied helper source performs proxy sequencing, append and dropped diagnostics only. The forwarding path omits the degraded flag from its dropped log. That is a diagnostic parity nit, not a loss of behaviour.

## Missing acceptance tests

1. **Legacy exclusion: landed.** A legacy-only closed_turn route yields empty routes_in_state, zero closed_final and censored counts, and a None projection state.
2. **Subsequent-turns and episode-boundary: landed with a scope caveat.** The subsequent-turns case sends a third user turn, so at least one turn post-dates the closed_turn regardless of clock resolution. The episode case writes the lineage event directly through the store. The dispositions correctly state this is a test-supplied signal, not a wired harness producer. The Closer trigger works; production emission of that event is not evidenced and is not claimed.
3. **Route divergence: landed** on both paths, as above.
4. **None identity: not applicable**, as above.
5. **Dropped forwarded event: landed**, with the caveat noted.
6. **Before-regression log: confirmed.** The failure is at the routes_in_state assertion in `tests/integration/e2e/test_outcome_contract.py`, with components built and both gate outcomes logged. It is not an import or fixture error. An empty list where the first route was expected is exactly the hypothesis that pre-fix rows never reached the canonical consumer.

## Remaining notes, none blocking

- **Test-expectation correction on HTTP 400.** The wire observer marks the HTTP error incomplete, which policy maps to infrastructure. The parametrised test now expects infrastructure for both 503 and 400, and the completed-400 direct test covers the unverifiable hypothesis. Both are consistent with the supplied resolver disposition. No production policy changed.
- **Proxy rows on the induced divergence** are written to the fake route and are not asserted. That is outside this finding.
- **Cold-start forwarding without ledger** remains unsupported and documented.

## Scoped verdict

Record RV-01 as repaired once checks-2 completes without failures. Readiness reports one closed_final, one censored, zero capability evidence and a blocked window. That is the correct end state for this slice. Nothing here qualifies LRN-001, promotes maturity, or claims a complete learning loop. Other retrospective findings remain open and are unaffected.
FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/post-review.md
**Verdict: RV-01 is materially repaired, with one conditional blocker and four evidence gaps to close before the review round is marked resolved.** The cascade now emits canonical `outcome` rows, the proxy forwards them verbatim, and the composed test reaches the Closer and readiness without inventing success. The test counts and the before-regression log are author-supplied and I did not run them. The critique below is from reading the diff and supplied source.

## Blockers

- **Conditional: None identity is coerced to the string "None".** In the new `_outcome` helper in `src/adrl/cascade/controller.py`, session and lineage are passed as `str(ctx.session_hmac)` and `str(ctx.lineage_hmac)`. If either field on RequestContext can be None, the payload carries a truthy "None". The Closer's `_session_of` in `src/adrl/ledger/outcomes.py` only falls back to the decisions row when the value is None, so the fallback is defeated, the idle trigger keys off a phantom session, and the human correction detector joins on a literal "None". The composed test asserts equality with the decision row, so the fixture path is fine. Verify the type. If it is optional, guard with `None if x is None else str(x)` and add a test with a None session. If non-optional, record that and this drops to a note.

- **Route attribution on continuations is asserted but not demonstrated.** The continuation test in `tests/integration/e2e/test_outcome_contract.py` asserts the closed_turn lands on the first decision's route. It never asserts that the continuation's own decision row has a different route id. If continuations inherit the route, the old re-keying would also have placed the row correctly, and the test proves producer, sequence and schema only. Add an explicit assertion that the second decision's route id differs from the sticky route, or construct the divergence directly. Until then the dispositions line "retain cascade route" is over-claimed.

## Verification gaps that do not block

- **The forwarded fallback test is a hybrid state, not the fallback.** The test removes the controller ledger after the first turn, so the producer counter was seeded while the ledger existed. A controller composed without a ledger from the start would seed from 1 with no visibility into stored rows. The plan-phase pending row is lost on that path, which is the accepted limitation. Because all states now share the `outcome` event type, sequence reuse after a restart with a missing or failed ledger read collides on the idempotency key and is silently dropped by the pipeline append. Under the old dialect, pending and closed_turn did not collide. The doc note "Observe-phase forwarding is tested" should say it is tested with a pre-seeded counter.

- **The broad exception handler in the proxy finalize makes the new TypeError guard inert.** Any error on the new forwarding lines, including an AttributeError if the pipeline ledger is None or a NameError from a missing import, is logged as finalize_failed and swallowed. The forwarded test passing is the only evidence the names resolve. Consider asserting no finalize_failed log in the forwarded test.

- **The idle-trigger assertion depends on CloseRule defaults and timestamp strictness.** The Closer counts user turns with `ts>` the closed_turn timestamp. Route A's closed_turn is written during the second turn's plan, before that turn's decision row. Whether the second decision counts depends on clock resolution and the default subsequent_turns value. The test asserts the trigger name "idle" without pinning the rule. Pass an explicit CloseRule with subsequent_turns above one to remove the timing dependence.

- **The `_append_event` helper was bypassed, not replaced.** I do not have its source. Confirm it performed no side effect beyond persistence, such as write-ahead ordering or metrics, that the cascade rows now skip.

## Missing acceptance tests

1. **Legacy exclusion from readiness.** The contract doc states old state-valued rows never enter readiness, even as censored. No test seeds a route with only legacy rows and asserts it is absent from readiness routes and from routes_in_state. The restart test adds a canonical pending, so that route does enter.
2. **Subsequent-turns and episode-boundary triggers.** The session and lineage HMACs were added so these triggers work. Only idle is exercised. Add a composed test with N user turns after closed_turn asserting the subsequent_turns trigger, and one with an episode boundary event.
3. **Route divergence on continuation** as described above, on both direct and forwarded paths.
4. **None session or lineage** as described above, if the type permits it.
5. **Dropped forwarded event.** Force the pipeline append to return False and assert the dropped counter and warning, so a duplicate-key collision is observable rather than silent.
6. **Before-regression log content.** I cannot see the log. Confirm it fails on the assertion for a persisted `outcome` row with closed_turn state, not on a fixture or import error, or it does not evidence the hypothesis.

## Things that check out

- **Cause retention.** The terminal closed_turn carries a top-level failure_type, the next-turn closed_turn carries none, and label derivation scans all outcome payloads. The parametrised 503 and 400 tests assert this end to end.
- **Completed 400 is decisive.** If the empty-candidate default were task_capability, the label assertion would fail. The disposition on resolve_primary is corroborated by the test, not just by inspection.
- **Idempotent closure.** Second scan returns empty because the latest outcome row is closed_final, and the closed_final producer sequence is derived from the rule id. One label row is asserted.
- **Unknown success stays unknown.** harness_reported_success is None on both transitions, and readiness reports one closed_final with zero capability evidence and the no-capability-evidence blocker.
- **Sequence seeding across the dialect change.** The legacy seeding test covers 77 to 78 and the seed counts by producer regardless of event type, so post-restart collisions on mixed-dialect routes are avoided when the ledger read succeeds.
- **Fixture assertion changes** in the controller integration test change only the event-type selection and keep partial-stream and infrastructure evidence checks.

## Scoped verdict

RV-01 can be recorded as repaired once the None coercion is verified or guarded and the continuation route-divergence assertion is added. The legacy-exclusion and subsequent-turns tests should land in the same correction round because they back claims already written into the contract doc. Nothing here promotes maturity or qualifies LRN-001. Readiness after this slice honestly reports a closed count with a blocked window, and that is the correct end state for this scope. Other retrospective findings remain open and are not addressed by this review.
FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/report.md
# Outcome connection repair

9 September 2026. Product P1/P2 prerequisite, RV-01. Fable post-review and correction recheck complete for RV-01.

Before: a real cascade decision produced state-valued events that closing/readiness
consumers never selected. After: canonical outcome events retain state, cause and
identity, and the proxy preserves returned event identity. The composed regression
now reaches an explicitly invoked closer: one closed result, one pending result,
zero capability evidence. A closed task is not automatically a successful task.

Evidence: [before regression](before-regression.log), [first focused attempt](focused-1.log),
[focused passing run](focused-2.log), [pre-review](pre-review-retry.md),
[dispositions](dispositions.md), [packet](packet.md), [source baseline](before-manifest.json).

Eleven new integration cases cover composed closure/idempotency, HTTP 400/503 cause
retention, completed-400 exclusion, direct and forwarded continuation persistence,
and legacy sequence seeding. Two old controller assertions now select canonical
outcome state; their failure/stream evidence assertions remain intact.

Limits: synthetic ASGI only, inherited SHADOW-load/LIVE-fixture admission bypass,
explicit Closer invocation, no real harness, no background adaptation, no migration
of old event dialect, no feature-contract admission and no formal maturity change.
Production plan-phase persistence requires the controller ledger. Other retrospective
blockers remain open. This repair is the first connection in the evidence loop, not
proof that ADRL learns or routes better.

All eleven engineering checks passed: 918 passed, 8 engine tests skipped; source manifest stable. See [checks](checks-1/manifest.json), [implementation diff](implementation.patch), and [after snapshot](after-manifest.json). This was the first candidate; final evidence below supersedes its count.

## Final reviewed result

Fable 5.1 independently critiqued the plan, reviewed the implementation, and rechecked one correction round. [Final critique](recheck.md) finds no remaining material blocker for RV-01, conditional on green final checks. [Final checks](checks-2/manifest.json) meet that condition: 922 passed, 8 engine tests skipped, all eleven checks passed, 324 source inputs stable and matching the review snapshot. The reviewer read source and logs but did not run tests itself.

The critique changed the work: preserve forwarded LedgerEvent identity; prove deliberately divergent route attribution; test legacy-only exclusion and context-based close triggers; pin timing assumptions; check dropped-event observability and completed-400 classification. Cold-start forwarding without a controller ledger remains unsupported; tested forwarding uses pre-seeded sequence state. Episode trigger tests supply a ledger signal, not a newly wired harness producer. A dropped-log diagnostic parity nit remains nonblocking.

RV-01 is fixed within this tested scope. Other retrospective findings remain open, including health/correction consumers and learning admission. No formal maturity promotion, real-model task result or automatic learning claim follows. Next work should repair the remaining label-reader contracts before claiming the whole evidence loop, then address routing selection and lab reproducibility.

FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/completion-validation.json
{
  "runtime_hashes_match": 324,
  "all_77_status_maturity_fields_unchanged": true,
  "index_unique_ADRs": 77,
  "link_files_checked": 16,
  "broken_links": [],
  "all_three_completed_review_responses_report_fable_5_1": true,
  "reviewer_tests_executed": false,
  "checks": "checks-2/manifest.json",
  "scope": "RV-01 only"
}

FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/checks-2/manifest.json
{
  "active_check": null,
  "changed_inputs": [],
  "checks": [
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "-m",
        "ruff",
        "check",
        "src",
        "tests",
        "tools"
      ],
      "elapsed_seconds": 0.048,
      "exit_code": 0,
      "log": "lint.log",
      "name": "lint",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "-m",
        "ruff",
        "format",
        "--check",
        "src",
        "tests",
        "tools"
      ],
      "elapsed_seconds": 0.045,
      "exit_code": 0,
      "log": "format.log",
      "name": "format",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "-m",
        "mypy"
      ],
      "elapsed_seconds": 0.426,
      "exit_code": 0,
      "log": "types.log",
      "name": "types",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "-m",
        "pytest",
        "-q"
      ],
      "elapsed_seconds": 59.875,
      "exit_code": 0,
      "log": "tests.log",
      "name": "tests",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "tools/check_ledger_discipline.py"
      ],
      "elapsed_seconds": 0.147,
      "exit_code": 0,
      "log": "ledger.log",
      "name": "ledger",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "-m",
        "adrl.cli.main",
        "config",
        "check"
      ],
      "elapsed_seconds": 0.421,
      "exit_code": 0,
      "log": "config.log",
      "name": "config",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "tools/check_data_inventory.py"
      ],
      "elapsed_seconds": 0.077,
      "exit_code": 0,
      "log": "inventory.log",
      "name": "inventory",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "tools/check_learning_contract.py"
      ],
      "elapsed_seconds": 0.046,
      "exit_code": 0,
      "log": "learning.log",
      "name": "learning",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "tools/export_api_contract.py",
        "--out",
        "api/adrl-api-v1-preview.json",
        "--check"
      ],
      "elapsed_seconds": 0.137,
      "exit_code": 0,
      "log": "api_contract.log",
      "name": "api_contract",
      "status": "passed"
    },
    {
      "argv": [
        "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
        "tools/adr_module_map.py",
        "--register",
        "/Users/arunmenon/projects/adrl-world-class/adr",
        "--check"
      ],
      "elapsed_seconds": 0.192,
      "exit_code": 0,
      "log": "adr_map.log",
      "name": "adr_map",
      "status": "passed"
    },
    {
      "decision_count": 77,
      "duplicate_index_rows": [],
      "missing_from_index": [],
      "name": "register_index",
      "status": "passed",
      "unknown_index_rows": []
    }
  ],
  "environment_scope": "Inherited environment; secret values and private keys not recorded",
  "excluded_scope": "Private keys, .env files, caches, runtime data and Git internals",
  "finished_at": "2026-09-08T18:47:55.701686+00:00",
  "installed_packages": [
    "Jinja2==3.1.6",
    "MarkupSafe==3.0.3",
    "PyYAML==6.0.3",
    "Pygments==2.21.0",
    "adrl==0.1.0",
    "annotated-doc==0.0.5",
    "annotated-types==0.8.0",
    "anyio==4.14.2",
    "ast_serialize==0.8.0",
    "certifi==2026.7.22",
    "cffi==2.1.1",
    "cfgv==3.5.0",
    "charset-normalizer==3.5.1",
    "click==8.5.0",
    "cloudpickle==3.1.2",
    "cryptography==50.0.1",
    "detect-secrets==1.5.0",
    "distlib==0.4.3",
    "filelock==3.32.5",
    "fsspec==2026.7.0",
    "googleapis-common-protos==1.75.2",
    "grpcio==1.83.1",
    "h11==0.16.0",
    "hf-xet==1.6.0",
    "httpcore==1.0.9",
    "httptools==0.8.0",
    "httpx==0.28.1",
    "huggingface_hub==1.29.0",
    "hypothesis==6.167.1",
    "identify==2.6.19",
    "idna==3.19",
    "iniconfig==2.3.0",
    "joblib==1.6.0",
    "librt==0.15.0",
    "markdown-it-py==4.2.0",
    "mdurl==0.1.2",
    "model2vec==0.9.0",
    "mypy==2.3.1",
    "mypy_extensions==1.1.0",
    "narwhals==2.25.0",
    "nodeenv==1.10.0",
    "numpy==2.5.2",
    "opentelemetry-api==1.44.0",
    "opentelemetry-exporter-otlp-proto-common==1.44.0",
    "opentelemetry-exporter-otlp-proto-grpc==1.44.0",
    "opentelemetry-exporter-otlp-proto-http==1.44.0",
    "opentelemetry-exporter-otlp==1.44.0",
    "opentelemetry-proto==1.44.0",
    "opentelemetry-sdk==1.44.0",
    "opentelemetry-semantic-conventions==0.65b0",
    "packaging==26.3",
    "pathspec==1.1.1",
    "platformdirs==4.11.7",
    "pluggy==1.6.0",
    "pre_commit==4.6.2",
    "prometheus_client==0.26.0",
    "protobuf==7.36.1",
    "pycparser==3.0",
    "pydantic-settings==2.15.0",
    "pydantic==2.13.5",
    "pydantic_core==2.46.5",
    "pytest-asyncio==1.4.0",
    "pytest==9.1.1",
    "python-discovery==1.6.0",
    "python-dotenv==1.2.3",
    "requests==2.34.2",
    "respx==0.23.1",
    "rich==15.0.0",
    "ruff==0.16.5",
    "safetensors==0.8.0",
    "scikit-learn==1.9.0",
    "scipy==1.18.1",
    "shellingham==1.5.4",
    "sortedcontainers==2.4.0",
    "starlette==1.6.0",
    "structlog==26.1.0",
    "threadpoolctl==3.6.0",
    "tokenizers==0.23.1",
    "tqdm==4.70.0",
    "typer==0.27.2",
    "types-PyYAML==6.0.12.20260815",
    "typing-inspection==0.4.4",
    "typing_extensions==4.16.0",
    "urllib3==2.7.0",
    "uvicorn==0.52.4",
    "uvloop==0.22.1",
    "virtualenv==21.7.8",
    "watchfiles==1.2.0",
    "websockets==17.1"
  ],
  "per_check_timeout_seconds": 120,
  "platform": "macOS-26.3-arm64-arm-64bit",
  "python": "3.12.7 (main, Oct  9 2024, 15:28:06) [Clang 14.0.0 (clang-1400.0.29.202)]",
  "python_executable": "/Users/arunmenon/projects/adrl-core/.venv/bin/python",
  "release_authority": false,
  "schema_version": "adrl-engineering-checks-v1",
  "source_after": {
    ".gitignore": {
      "bytes": 251,
      "mode": 420,
      "sha256": "5a46e538a34a4bc94faa64f0af2a0918926e4213251a60e851eaf41922db02b3"
    },
    "AGENTS.md": {
      "bytes": 3633,
      "mode": 420,
      "sha256": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490"
    },
    "CLAUDE.md": {
      "bytes": 3633,
      "mode": 420,
      "sha256": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490"
    },
    "README.md": {
      "bytes": 13374,
      "mode": 420,
      "sha256": "dda387731ad435a2937414c8d35d3f2b51cb08841291013620571c731a554c29"
    },
    "api/adrl-api-v1-preview.json": {
      "bytes": 52939,
      "mode": 420,
      "sha256": "5a3f2c5401acd73d3a30a89fb24c94660d9a2b7c9f625b4a7c6acef987d03757"
    },
    "artifacts/lab/routing-suite-v1.json": {
      "bytes": 2503,
      "mode": 420,
      "sha256": "dfe4125445ace13eb6fbe064b0ed52576df5a71ddaeebe2568cc93fb047dc7a9"
    },
    "config/detectors.yaml": {
      "bytes": 3049,
      "mode": 420,
      "sha256": "d7e504d17341680bcfbf8bc9f76c435aa1bfc45bf53efbf208305604364d2f55"
    },
    "config/endpoint-inventory-v1.json": {
      "bytes": 1929,
      "mode": 420,
      "sha256": "67d18715549c041215deca75f0002bf486ce946b55a593a6e7d815c3e291212e"
    },
    "config/endpoint-inventory-v1.sig": {
      "bytes": 89,
      "mode": 420,
      "sha256": "e8a78202b9ff2985ec0fe9cc7287c01c434a27466a2445ac8a35fe56bc1aa762"
    },
    "config/keys/dev/README.md": {
      "bytes": 934,
      "mode": 420,
      "sha256": "1f2001f55f04ae0c577e723a7d70205cab0c194d99ad337f5c72c63265ee918a"
    },
    "config/keys/dev/checkpoint-signing.pub": {
      "bytes": 113,
      "mode": 420,
      "sha256": "54c0986810789840eaede4560aa9cfbab945ed5a494fd3b83a071e82460adb2c"
    },
    "config/keys/dev/manifest-signing.pub": {
      "bytes": 113,
      "mode": 420,
      "sha256": "aa93b81e39a6986964f8f574eb71c9a3510f07881a553eef24b199e536292655"
    },
    "config/learning-contract-v1.json": {
      "bytes": 1529,
      "mode": 420,
      "sha256": "8cfdf6a5f27f3f80839d6874831859dc0b6d71ed31440a9f33e385f0ee5ec58c"
    },
    "config/policy.yaml": {
      "bytes": 1486,
      "mode": 420,
      "sha256": "fd7522fda0c1d1c9fb1d096e603b8b3df2d981894658012e4ae2fa08439dc9bc"
    },
    "config/prices.yaml": {
      "bytes": 539,
      "mode": 420,
      "sha256": "07fd0c8da1cce030d210f82aabfb785b81d51b3b7e5dddedb848dd2584744dd5"
    },
    "config/provider-pairs.yaml": {
      "bytes": 1877,
      "mode": 420,
      "sha256": "032a460e3e2eae0b6715a82c1a0beb60d590b7f78bf0a485245bbb6e3a3d5175"
    },
    "config/repo-classification-v1.json": {
      "bytes": 1241,
      "mode": 420,
      "sha256": "47d7790c3eb71be692b74332a2e01de3b19011b10609722fdaf413279cf97b42"
    },
    "config/repo-classification-v1.sig": {
      "bytes": 89,
      "mode": 420,
      "sha256": "3487b15e06f60da66bfac3ed6dc4aa70e7091779b0c10a7f46d05380bdb70d5b"
    },
    "config/rungs.yaml": {
      "bytes": 1597,
      "mode": 420,
      "sha256": "39c0b9521d9e8ccbb0b4750bed1fc90a95be9f4427d4d0cb94d7f8d56c79935e"
    },
    "config/tripwires.yaml": {
      "bytes": 696,
      "mode": 420,
      "sha256": "201d15de3d6115f46c0ac7fe5eeda91011701f63e781e88b6f8b269238dea4db"
    },
    "config/trusted-tool-servers.yaml": {
      "bytes": 797,
      "mode": 420,
      "sha256": "b750cb935bdb7547a2b1ded6278df1cf14e8ef59f26a9ec95905bc0edd3dbd7a"
    },
    "config/utility-fingerprints.yaml": {
      "bytes": 950,
      "mode": 420,
      "sha256": "ef9d86f19f39342f3359e7e1fc7551a7ea0a56756ff77e0f8f010905f383411a"
    },
    "docs/adr-module-map.md": {
      "bytes": 31183,
      "mode": 420,
      "sha256": "1ae7ad9678422e94a9903581d99e12d51888a8bbdf5feb0ea1e1a2e4d0af39e4"
    },
    "docs/attempt-coordination.md": {
      "bytes": 6572,
      "mode": 420,
      "sha256": "0d129f7afdec81d426656a994b1fdf988eb98d43438d65fa93fbb3fa0d221490"
    },
    "docs/attempt-lifecycle.md": {
      "bytes": 9442,
      "mode": 420,
      "sha256": "bbc398599c579392deb4020de3f98c65e71445418763755f5ea0b2a84cd2cd28"
    },
    "docs/data-inventory.md": {
      "bytes": 37783,
      "mode": 420,
      "sha256": "867f8510b6103079ef1e01b67a5307012087b0ff86800d4e7cfec6111d08eea7"
    },
    "docs/egress-anchoring.md": {
      "bytes": 5172,
      "mode": 420,
      "sha256": "d79a9f636a2b091b943cbd9caaf7e514a102309a4aabe6eec24f15a9e48f9444"
    },
    "docs/engineering-checks.md": {
      "bytes": 2339,
      "mode": 420,
      "sha256": "f62b353c39b9ddffdcc1f137535beed0afcef15fdb5e7dd5607b9c15d3fa6144"
    },
    "docs/isolated-execution.md": {
      "bytes": 8298,
      "mode": 420,
      "sha256": "c5ae8f71c16386eb516afcd5eedb29d5f9a88d756b51472d743e5798b5d55247"
    },
    "docs/key-revocation.md": {
      "bytes": 6111,
      "mode": 420,
      "sha256": "d51f135f6586589d2698612ce5680494c6ed06f7031812005af8d2434ef174a9"
    },
    "docs/known-gaps.md": {
      "bytes": 15171,
      "mode": 420,
      "sha256": "421651ee56e55db65b0857f67cad915480f17a67994aa9eba8f477a79a2970aa"
    },
    "docs/operator-captures.md": {
      "bytes": 5873,
      "mode": 420,
      "sha256": "62f7acf78ee0be3922c538ad03276252999c213e0c77ded03a3bfc95007caecc"
    },
    "docs/outcome-contract.md": {
      "bytes": 1796,
      "mode": 420,
      "sha256": "873d412f0735ae7501515c08687fbd4fc276eca213f2b99f6bd017312d1f5815"
    },
    "docs/process-ownership.md": {
      "bytes": 5470,
      "mode": 420,
      "sha256": "f2e6810a2cfc67b4d6918367ebb17adf0c9f21401cb600dcca58cc643e8f4d8c"
    },
    "docs/product-services.md": {
      "bytes": 14964,
      "mode": 420,
      "sha256": "f20f331de15c5083c557eb9f26406957a9eee6542451ae902aa5d0f25ae30d02"
    },
    "docs/protocol-boundary.md": {
      "bytes": 4006,
      "mode": 420,
      "sha256": "b5469f938dc2e96bc059dd812c388e0f6fb5219333d7d76f96f81da8ec2ccf38"
    },
    "docs/responses-admission.md": {
      "bytes": 3909,
      "mode": 420,
      "sha256": "f4ad3cf11226661c08c0f5dbc054a6f17ef8fa49faca3be1a8fc41a2fac3aaa8"
    },
    "docs/routing-features.md": {
      "bytes": 2267,
      "mode": 420,
      "sha256": "ca328c13ebdbcbee3208b4bcbda6d7967b0c32a247f04e3f1300d42c70f6d577"
    },
    "docs/routing-lab.md": {
      "bytes": 3920,
      "mode": 420,
      "sha256": "cb4e0b14204354e061fb1fdde4bffd1bf0949498aeab1bd7ddbb7ffb47e1171d"
    },
    "docs/stopped-resource-ownership.md": {
      "bytes": 7389,
      "mode": 420,
      "sha256": "b21ccc8c1a6b44895fd82b03e80afd610b10f9cb1b9a1649c3d26fb1d0dcc7cf"
    },
    "docs/verifier-experiments.md": {
      "bytes": 6216,
      "mode": 420,
      "sha256": "1a1c04c2cc2480b4d2c3da48586f1415fe69069ef9301cf60b3a7f74cb415aad"
    },
    "pyproject.toml": {
      "bytes": 1764,
      "mode": 420,
      "sha256": "5a124bb958e981557d4a3f62b28843f348ca306e4e31876a7ebc907dd95b4001"
    },
    "src/adrl/__init__.py": {
      "bytes": 82,
      "mode": 420,
      "sha256": "f1de990ba880b21895f4888c739207ca4c3c16b222c0933a2b26aa4a03cce8c0"
    },
    "src/adrl/api/__init__.py": {
      "bytes": 77,
      "mode": 420,
      "sha256": "02d1a3f2332e8662f52c584a15c490ba068b58294f970536391f0ca9d2bcedef"
    },
    "src/adrl/api/auth.py": {
      "bytes": 2944,
      "mode": 420,
      "sha256": "d666e1fa36b41d16448143eed404a7ccb0fde0cf6d32e70747df89b85da1bc3d"
    },
    "src/adrl/api/client.py": {
      "bytes": 6717,
      "mode": 420,
      "sha256": "7679bff2e7f5afc32800d9bc8bffe5bc7908ddf7c634036cd08bcc9ac18cbd4e"
    },
    "src/adrl/api/contracts.py": {
      "bytes": 10507,
      "mode": 420,
      "sha256": "35036e9782944730250846999f5dcd6e690717d7751e2275463696ff4e26a461"
    },
    "src/adrl/api/http.py": {
      "bytes": 4934,
      "mode": 420,
      "sha256": "c129cbd845d04583af3f566099117ba58e7fa12cc75694cc7f60a9161e3f8bd1"
    },
    "src/adrl/api/schema.py": {
      "bytes": 6151,
      "mode": 420,
      "sha256": "e839e85d32982463056a5bedeb21ed99c1ede5602f38acb922fd970a27044581"
    },
    "src/adrl/api/service.py": {
      "bytes": 15425,
      "mode": 420,
      "sha256": "add6130fe1b3fe65fe37b2179a025f59aa07c315d14a6a7ea648aed43f5f8818"
    },
    "src/adrl/api/store.py": {
      "bytes": 12008,
      "mode": 420,
      "sha256": "9527d95565df58003469be2ea62514d8cb13fdce8b87295e4a06b6c76b366dd8"
    },
    "src/adrl/app.py": {
      "bytes": 15403,
      "mode": 420,
      "sha256": "ee397176ddcd305a1b5c70eb551a06e98b2065a076fa04593edb9da724a7741a"
    },
    "src/adrl/cascade/__init__.py": {
      "bytes": 300,
      "mode": 420,
      "sha256": "bc8b4bd3f53c5cbf7dc8ed81ee1ed9719c01d7ae158a11ec29263efa2e08c582"
    },
    "src/adrl/cascade/boundary.py": {
      "bytes": 3431,
      "mode": 420,
      "sha256": "66839b708bc041b4f26aa74d9facde2ea9e367a9263c492a90e3d3ef12fc98e2"
    },
    "src/adrl/cascade/controller.py": {
      "bytes": 26677,
      "mode": 420,
      "sha256": "fedef16cf2a4ce239f8c7c07eb27331b6bdeb5656735b84ab925f707adbe0a1d"
    },
    "src/adrl/cascade/handoff.py": {
      "bytes": 12784,
      "mode": 420,
      "sha256": "7a6e066343ac3fd87a63f1dd1ddecda6aa29269f28dc9ec13da88aad106b747c"
    },
    "src/adrl/cascade/sticky.py": {
      "bytes": 5423,
      "mode": 420,
      "sha256": "28346143b50492f80c41aff7ce044ff27447bb335146bf236b37500c58f711cf"
    },
    "src/adrl/cascade/tripwires.py": {
      "bytes": 16071,
      "mode": 420,
      "sha256": "c91eb8b1feeaf8e62f0ae5866d76205f3e3fe8a627d29885b893d70d1829c728"
    },
    "src/adrl/cli/__init__.py": {
      "bytes": 74,
      "mode": 420,
      "sha256": "aa78bc2cbcd04512b0ce732a5272efb78c4f9bb95daa7d7d59c0b4e7485575b4"
    },
    "src/adrl/cli/improvement.py": {
      "bytes": 4845,
      "mode": 420,
      "sha256": "916f93bad7c38e57b0626dcea70e833a02ad3487d4aaa8a91970339e10421963"
    },
    "src/adrl/cli/ledger_commands.py": {
      "bytes": 9857,
      "mode": 420,
      "sha256": "4d78faf44948f73928cba50f0fba8b4c0c2a32bb05250f1f7b121a784a5045fb"
    },
    "src/adrl/cli/main.py": {
      "bytes": 18764,
      "mode": 420,
      "sha256": "b155525971ee910191cccf609bcf2760c1f19a170fb00c6de8907ee567429322"
    },
    "src/adrl/cli/product.py": {
      "bytes": 11150,
      "mode": 420,
      "sha256": "048db7e3d777a32b57badea048e37fb3cc0774ecabfdeefc5eff927e53ff02c5"
    },
    "src/adrl/config/__init__.py": {
      "bytes": 287,
      "mode": 420,
      "sha256": "3803eb7d9d9190983da2058ca3d85a56d1bf2386d94d3743b3fd445760585bf7"
    },
    "src/adrl/config/checks.py": {
      "bytes": 11700,
      "mode": 420,
      "sha256": "de6b5ba06701c0deeddde05ba9f9bbe057a507e58107cfb4f5fd56568b277cc6"
    },
    "src/adrl/config/loaders.py": {
      "bytes": 6206,
      "mode": 420,
      "sha256": "fe0ad675a1d6b49648c7b9c3a2c7ba813b3abcc421d204a35309cfc066896792"
    },
    "src/adrl/config/models.py": {
      "bytes": 14108,
      "mode": 420,
      "sha256": "baf7f4346711468102c2644787cc0f275ee84e70972a51d2482bcfd648b94dd0"
    },
    "src/adrl/config/settings.py": {
      "bytes": 3538,
      "mode": 420,
      "sha256": "4a4daad400b9786e32edead3c7ad41e117e39459f93e915b83651b237a1d98b6"
    },
    "src/adrl/core/__init__.py": {
      "bytes": 2225,
      "mode": 420,
      "sha256": "2e4be193ed644ada5559624553d72d9f5c6d4a98dded8b7e974692146ab0e983"
    },
    "src/adrl/core/attempt_coordinator.py": {
      "bytes": 10359,
      "mode": 420,
      "sha256": "08d43e990442e2d55c5785fbf86b016b3ba1d07864c536723d2b1de8a00c61c2"
    },
    "src/adrl/core/container_control.py": {
      "bytes": 14795,
      "mode": 420,
      "sha256": "15942e04fe83bfc419b2c4913505ab0df01909a429f6c86096a2430936282e69"
    },
    "src/adrl/core/enums.py": {
      "bytes": 7138,
      "mode": 420,
      "sha256": "fa1a86d4c6ecc321ff7baf945aec440b8cb9a9a3937d78c3b9c9ffb435bf9bc7"
    },
    "src/adrl/core/errors.py": {
      "bytes": 4007,
      "mode": 420,
      "sha256": "4a9b11ae4fa527a813e800ebff00c2edfc04d2dd8cea0b0d6d7cfa7e1916bfff"
    },
    "src/adrl/core/execution_control.py": {
      "bytes": 9539,
      "mode": 420,
      "sha256": "435b1b28c2219e8b571c5895ff7d9b359356cefb594e3eae734a99a006c52a49"
    },
    "src/adrl/core/ids.py": {
      "bytes": 2294,
      "mode": 420,
      "sha256": "903b7c34cbae920f9a00edffcfa57e56d866090004925f712f90d7f00167f9e2"
    },
    "src/adrl/core/isolated_execution.py": {
      "bytes": 20808,
      "mode": 420,
      "sha256": "d8d994b245ae30f9b535c18a0f6fbddf67c45bc88ce76f37e0f6c5b6b1edba5e"
    },
    "src/adrl/core/launch_markers.py": {
      "bytes": 4486,
      "mode": 420,
      "sha256": "b3d95e9b7a7ba00e0f2f0cfee122aa7ce261eb2639e1fd29af314e5ddbd8c75f"
    },
    "src/adrl/core/ports.py": {
      "bytes": 6623,
      "mode": 420,
      "sha256": "8e0380c0b7d01e3b81bb3e6e499c6608b71522fd83f1e508d721a90b2ebf2c6d"
    },
    "src/adrl/core/process_anchor.py": {
      "bytes": 5134,
      "mode": 420,
      "sha256": "7e30ca14f22cef0787d3381eee8f9db75814813961bea4a1bb94984b5b68ca14"
    },
    "src/adrl/core/process_owner.py": {
      "bytes": 13491,
      "mode": 420,
      "sha256": "be67390cc95dbea608a1cf170e9452fc787730e2a60fc44825b58fcefa7d94c4"
    },
    "src/adrl/core/resource_owner.py": {
      "bytes": 21451,
      "mode": 420,
      "sha256": "5398a355ac7571929203e81eef8efcbc9436cf5452d3e3ee4c1440581b3d68f9"
    },
    "src/adrl/core/types.py": {
      "bytes": 13725,
      "mode": 420,
      "sha256": "1378a303072abce0c1257c6c1b346991b83dbeee204e51d5a8560c2e2f57e1b1"
    },
    "src/adrl/gates/__init__.py": {
      "bytes": 447,
      "mode": 420,
      "sha256": "0566861be1abd45018586c80ea2455a144e4fc8ef6e14f60a27f9d02cf2dbb23"
    },
    "src/adrl/gates/block.py": {
      "bytes": 7604,
      "mode": 420,
      "sha256": "b4fbf137ccfda62d36babb611bd875fc8e96ed835fc03373cca0b66b00174c7e"
    },
    "src/adrl/gates/cli.py": {
      "bytes": 10168,
      "mode": 420,
      "sha256": "aebd8c3eb7a3e53351eb3eb6ba88c0335fbbb27e94de225a6f9c8410bc601ef8"
    },
    "src/adrl/gates/content.py": {
      "bytes": 8213,
      "mode": 420,
      "sha256": "788bd77d75fe741557cfcc3a1d34c7d6c3bb0dd0f56f1ca9b0153407f7f8b194"
    },
    "src/adrl/gates/coverage.py": {
      "bytes": 2638,
      "mode": 420,
      "sha256": "e5ea97fa70fc83eec31b65285b4e7df464f69507284fda90075c867b6313bfd3"
    },
    "src/adrl/gates/deployments.py": {
      "bytes": 8218,
      "mode": 420,
      "sha256": "4657f74d3f2aefeb4c4c3c007d5d97ba67635475df500c8479278129295203c2"
    },
    "src/adrl/gates/detectors.py": {
      "bytes": 1887,
      "mode": 420,
      "sha256": "9a36fa3fd5e1385988f15f7a8845300b751e4aac6383deca1a7306e1bdb3935a"
    },
    "src/adrl/gates/egress.py": {
      "bytes": 6078,
      "mode": 420,
      "sha256": "68d6eec54dac44da14bfdc6e9f74110a0e9a451d389aa6fff31f40f3cba2da43"
    },
    "src/adrl/gates/feasibility.py": {
      "bytes": 8301,
      "mode": 420,
      "sha256": "53bee77bbe27ebec7fedc8e8be813823b86b322d56af653dab79909501cf5ad6"
    },
    "src/adrl/gates/measure.py": {
      "bytes": 4199,
      "mode": 420,
      "sha256": "ddb1c238ee1b05b4a28d3ed10418ee2c6e8ebdd6ccb7be6b8f9cd787c4fd19a0"
    },
    "src/adrl/gates/pin.py": {
      "bytes": 17576,
      "mode": 420,
      "sha256": "525972e0f191b92c92ecd483a76619806da51f63124987cfe82857aa1986f9d1"
    },
    "src/adrl/gates/pipeline.py": {
      "bytes": 24986,
      "mode": 420,
      "sha256": "7c33d96afd92a23913d5877482fb56fa25252979c11d458be25012b7d9bf7603"
    },
    "src/adrl/gates/repo_class.py": {
      "bytes": 14810,
      "mode": 420,
      "sha256": "ea362f101fc267fa00f0ebc373ff57f020aa7113d384e7c65f33974d6d651624"
    },
    "src/adrl/gates/sandbox.py": {
      "bytes": 9961,
      "mode": 420,
      "sha256": "2726fe38e484eaf8402f3bd04e648ebd257dc1f0e47f0cd7d0f2c417ced9714b"
    },
    "src/adrl/gates/secrets.py": {
      "bytes": 12884,
      "mode": 420,
      "sha256": "cd60482c0bec4d4fce167283a4d9e629df220bd65458a285a772cfeacd372796"
    },
    "src/adrl/gates/suppression.py": {
      "bytes": 1372,
      "mode": 420,
      "sha256": "e191a45a9a4d39c620de57fef049685f1bc47beb7981bd29082277ac508274d0"
    },
    "src/adrl/gates/workload.py": {
      "bytes": 12152,
      "mode": 420,
      "sha256": "06190e43f32cdabfb1b3b70466f3b0b1982b8898924dac9c29572d126c27c29c"
    },
    "src/adrl/learning/__init__.py": {
      "bytes": 300,
      "mode": 420,
      "sha256": "87db4b96f6dc2ed884dedcfd80956d2deebed4e7e219960f44b91b96bdbe6244"
    },
    "src/adrl/learning/abstention.py": {
      "bytes": 11124,
      "mode": 420,
      "sha256": "04c7f7c58ad90da533854f186e3348f3f0a9a6975a28c1a7acfe3e391bd57119"
    },
    "src/adrl/learning/artifacts.py": {
      "bytes": 8598,
      "mode": 420,
      "sha256": "b619ab050dfea6317521551de7ed56b188e28a10da9dab488f9b9950145d4be0"
    },
    "src/adrl/learning/dataset.py": {
      "bytes": 14278,
      "mode": 420,
      "sha256": "9e6ec8fcae5b78b07e1de0e874b338bc0233cab69bb8f39e78c3235bec0fa192"
    },
    "src/adrl/learning/estimator.py": {
      "bytes": 11107,
      "mode": 420,
      "sha256": "40a8c0fb0453cf47c52e96b32d5eaadb3000d2a38e1300e3e9224211360b332c"
    },
    "src/adrl/learning/explore.py": {
      "bytes": 9761,
      "mode": 420,
      "sha256": "1c57f911fe66cf38f7e95744971395388a9791d8a527870eb16a352b2ca01189"
    },
    "src/adrl/learning/improvement.py": {
      "bytes": 12577,
      "mode": 420,
      "sha256": "21cd27a5d31a66797574e2f02ea3fc4e4ea48b6150343ef301a9289ae8b80c81"
    },
    "src/adrl/learning/pairs.py": {
      "bytes": 10477,
      "mode": 420,
      "sha256": "73283b6c0af83c409d37d4fecce3d31437de7a65aca66ea1e0ff53efeb276160"
    },
    "src/adrl/learning/readiness.py": {
      "bytes": 6395,
      "mode": 420,
      "sha256": "947d22d853c3bed68521ee2d005947696bce404034e5819dfc0f697533e55aea"
    },
    "src/adrl/learning/tiers.py": {
      "bytes": 15732,
      "mode": 420,
      "sha256": "6d0a17d8a57179e13544a75bde5144ae93343e21c966b71eebdaf0fdbbb1fca8"
    },
    "src/adrl/ledger/__init__.py": {
      "bytes": 708,
      "mode": 420,
      "sha256": "634cb0cb9f669d0a256abeb6e63a003685026f6edecce46d4e4ee77676d5761b"
    },
    "src/adrl/ledger/anchoring.py": {
      "bytes": 9218,
      "mode": 420,
      "sha256": "024913a90f513ae8583d409d03a77dbffb00a367f207b12bd5a762c97879fbed"
    },
    "src/adrl/ledger/attempts.py": {
      "bytes": 30054,
      "mode": 420,
      "sha256": "76e85c5028df2f05c0e8d3f680078e84230952f85a0534a21776842251e2b0ae"
    },
    "src/adrl/ledger/capture.py": {
      "bytes": 18652,
      "mode": 420,
      "sha256": "ef644fa690e69bb718f00534aec19aaf55d541bbf38f7249bf854da7e8bebaed"
    },
    "src/adrl/ledger/counterfactual.py": {
      "bytes": 1950,
      "mode": 420,
      "sha256": "43c9b8345e855257ea9f727205ca678c58be995dea1c8234dc15132ece501922"
    },
    "src/adrl/ledger/crypto.py": {
      "bytes": 1064,
      "mode": 420,
      "sha256": "01730ca1c51e4cfcd48beef49b744e4d0cdca4c6996b09c77fb7a219e791ebb6"
    },
    "src/adrl/ledger/egress.py": {
      "bytes": 25954,
      "mode": 420,
      "sha256": "43a05c01cb284d6c53c2b79b0be906e4f9a291788f7932cc85cc13a639a1feac"
    },
    "src/adrl/ledger/embeddings.py": {
      "bytes": 9564,
      "mode": 420,
      "sha256": "f766d1ddeec3e5742182cd4c468483769c382cf9fbbc76667c3a90a1e7f2b64c"
    },
    "src/adrl/ledger/erasure.py": {
      "bytes": 3851,
      "mode": 420,
      "sha256": "82298f397b3c752d3983f5415f09b59e59de5bc14fd246460bebf75bb03803f5"
    },
    "src/adrl/ledger/events.py": {
      "bytes": 9937,
      "mode": 420,
      "sha256": "91880f121e9e30cfe4684305135b9a99258a974cbdb87a0870eaa537db6a2cd3"
    },
    "src/adrl/ledger/facade.py": {
      "bytes": 9020,
      "mode": 420,
      "sha256": "2bb55f817fa889b92fb87ee67932a0a07a1821bdc73d7c9e0dabb6e40d89e892"
    },
    "src/adrl/ledger/improvement.py": {
      "bytes": 3780,
      "mode": 420,
      "sha256": "21e2dc8f8d26af7177a5a5c0cd64102b1154a2368784dd71432861a9aafbdedf"
    },
    "src/adrl/ledger/keystore.py": {
      "bytes": 10727,
      "mode": 420,
      "sha256": "7317110097fceaef34a69fb3fbeff3d0e27db17e0508e88b8063abf812c44d12"
    },
    "src/adrl/ledger/labels.py": {
      "bytes": 7515,
      "mode": 420,
      "sha256": "be1f1b089e477fb0a3ab6076b754e858f24950d27dcad5c4cba2b86dc6ac361f"
    },
    "src/adrl/ledger/migrations/0001_initial.sql": {
      "bytes": 3161,
      "mode": 420,
      "sha256": "5c0e582136caf827307f3f8a08098f9eb5c05be599a469a1b7fb0472a776e835"
    },
    "src/adrl/ledger/migrations/0002_evidence.sql": {
      "bytes": 889,
      "mode": 420,
      "sha256": "177647eb19f86c6d286720bb47891d8d73178435e4e44e7daf8326a0e2a99bcb"
    },
    "src/adrl/ledger/migrations/0003_product.sql": {
      "bytes": 1365,
      "mode": 420,
      "sha256": "0689c91906d06152af09937eb2758f7891c14a7456542632d19b40567b0f30b6"
    },
    "src/adrl/ledger/migrations/0004_integration_mode.sql": {
      "bytes": 292,
      "mode": 420,
      "sha256": "f34bc9fab14caad2ed8b85e716a0fd984a1061649cc5f015f2c2ff9236d93bf9"
    },
    "src/adrl/ledger/migrations/0005_session_verification.sql": {
      "bytes": 533,
      "mode": 420,
      "sha256": "854c5ab5137417effded2b1d12317eb3b34ef89fceb9ab044486dcd242a210ac"
    },
    "src/adrl/ledger/migrations/0006_improvement.sql": {
      "bytes": 484,
      "mode": 420,
      "sha256": "b194c62ee650354af4b5f7cbf9ab4d17d226572f9b514dba5fe679bdc9f24f5f"
    },
    "src/adrl/ledger/migrations/0007_captures.sql": {
      "bytes": 529,
      "mode": 420,
      "sha256": "e45cd62b7e45fe68227440490b78b7e42a2ebc731d1ee88aba31c40909c8a719"
    },
    "src/adrl/ledger/migrations/0008_attempts.sql": {
      "bytes": 778,
      "mode": 420,
      "sha256": "d78df82450565671d96d2c9648c493f490ab81ec0fde8061b269c66c49a98d12"
    },
    "src/adrl/ledger/migrations/0009_attempt_capacity.sql": {
      "bytes": 736,
      "mode": 420,
      "sha256": "0e534507e02da25c7f0e6b9d5c1e7408e8c8b17831166bca534895baf4a1e8f6"
    },
    "src/adrl/ledger/migrations/0010_execution_fences.sql": {
      "bytes": 564,
      "mode": 420,
      "sha256": "d352e2cd587a330c0403e76ee6656e9838a21c7cbc3253b9b44938b759e48555"
    },
    "src/adrl/ledger/migrations/0011_resource_ownership.sql": {
      "bytes": 684,
      "mode": 420,
      "sha256": "3f1828853c85aa555b1e588d458ec6180ed2c9377faa1057a62e6ef307673ecf"
    },
    "src/adrl/ledger/migrations/0012_launch_history.sql": {
      "bytes": 540,
      "mode": 420,
      "sha256": "2b4a4146f2e1dd5731cd75ac8990864f11f339a4f3b129e846585ae54122bb5d"
    },
    "src/adrl/ledger/migrations/__init__.py": {
      "bytes": 969,
      "mode": 420,
      "sha256": "f01702f0272a85680c14f0773562a7efd919f830b1cbea48b773f1f3ff5135ff"
    },
    "src/adrl/ledger/outcomes.py": {
      "bytes": 16010,
      "mode": 420,
      "sha256": "87ed8af4d5d244af77eadb36d8edc44fb3e62f86c1dbb02f921bcde772cba409"
    },
    "src/adrl/ledger/projections.py": {
      "bytes": 10289,
      "mode": 420,
      "sha256": "1d21a9a3921eb0d1fd09e95c2e5db2ee6f24649afc8cc0b8221f6d975c8048ee"
    },
    "src/adrl/ledger/readiness.py": {
      "bytes": 4588,
      "mode": 420,
      "sha256": "43677204359845245b952c5a26c567db7b61994ea95fbcedf2b187bff56bd204"
    },
    "src/adrl/ledger/replay.py": {
      "bytes": 2185,
      "mode": 420,
      "sha256": "a317c2a83252cdaeff25721bf9b3ba3006deac2a5bc217f9b931a9d7c5cf3676"
    },
    "src/adrl/ledger/retention.py": {
      "bytes": 2911,
      "mode": 420,
      "sha256": "a5530bf46282ae0f93b7b473e1518b66c44289f71e759aa67fb7d045b90a42d1"
    },
    "src/adrl/ledger/session_verification.py": {
      "bytes": 14522,
      "mode": 420,
      "sha256": "e6f5efbc51107337ea75c4a363c4c520d04da76ae021ddf45dca06c76e96bb9e"
    },
    "src/adrl/ledger/shadow_retrieval.py": {
      "bytes": 3978,
      "mode": 420,
      "sha256": "03961c21ddafa3d69426280db1fc7122568b6bc0433e1dd2ea45fb8876edae79"
    },
    "src/adrl/ledger/state.py": {
      "bytes": 5981,
      "mode": 420,
      "sha256": "3b797bd74e4c2fa94f456fcbfced6f95388810ce628bef88873c4a6423765ef0"
    },
    "src/adrl/ledger/store.py": {
      "bytes": 10978,
      "mode": 420,
      "sha256": "4bef263447219212d3e8b3262d0666abdc20ed9832d15777595eae1621ea35c2"
    },
    "src/adrl/ledger/upcast.py": {
      "bytes": 3852,
      "mode": 420,
      "sha256": "6af7243a7c4ccd55fda7014617644a3a6d735ba1c4a6f8bfc67bca8522868732"
    },
    "src/adrl/ledger/verification.py": {
      "bytes": 23436,
      "mode": 420,
      "sha256": "c2846a6a8cdf0b1c1c479e71cda691dc8a70d11db9d708056ec87c7ddac313a3"
    },
    "src/adrl/proxy/__init__.py": {
      "bytes": 177,
      "mode": 420,
      "sha256": "49436b67b95b630642b80f88850ebfc37c1dad4c52f1b51834b766e89f112a1b"
    },
    "src/adrl/proxy/asgi.py": {
      "bytes": 6662,
      "mode": 420,
      "sha256": "491c8a431380483eff035d136749a9c13c7738ad613f75ee879fdd929ee23640"
    },
    "src/adrl/proxy/errors.py": {
      "bytes": 940,
      "mode": 420,
      "sha256": "6208b8f4b9f2442a33ea8022419fd22903dab91079e4de256edf755d6bdf4a36"
    },
    "src/adrl/proxy/fallback.py": {
      "bytes": 6479,
      "mode": 420,
      "sha256": "04919e7e581ca96a82c9ee99d7ad5527ae36f17853b39ca476dd0c8a97307e35"
    },
    "src/adrl/proxy/observe_only.py": {
      "bytes": 7214,
      "mode": 420,
      "sha256": "bf7adbbe6807ec5db6165a041597e4a8df3324061324632b6c1f87072d3138e3"
    },
    "src/adrl/proxy/pipeline.py": {
      "bytes": 48117,
      "mode": 420,
      "sha256": "68a170c352ad7793113626002be84608f9c656740280156405682040407b152f"
    },
    "src/adrl/proxy/stages.py": {
      "bytes": 3091,
      "mode": 420,
      "sha256": "53513de35680401ec134a0d360b84b894fe6fdbd6be2c3c6c42356b836a4174a"
    },
    "src/adrl/proxy/upstream.py": {
      "bytes": 4592,
      "mode": 420,
      "sha256": "cbfc2436d9f3e87813a392e3839b4388d34b8d4c17194cce3c5f0bba84ec98d2"
    },
    "src/adrl/routing/__init__.py": {
      "bytes": 215,
      "mode": 420,
      "sha256": "ec71c7c97beb192638a74734a09c8f3d6501adad3dfd30261411e7c6e4ed859b"
    },
    "src/adrl/routing/advisor.py": {
      "bytes": 7687,
      "mode": 420,
      "sha256": "cbd31e1919d24546641003bd2b4d232d56986f94c189f0b61729816031443450"
    },
    "src/adrl/routing/cascade_feasibility.py": {
      "bytes": 2764,
      "mode": 420,
      "sha256": "ee8359e5655ee51319727ed4611be04ba5c76f81b02982b67a823b99ec494f97"
    },
    "src/adrl/routing/cost.py": {
      "bytes": 7081,
      "mode": 420,
      "sha256": "428e3894b10fd2dd214294da49aa78f2251c987715b3a2d59c4833e4e1e074d0"
    },
    "src/adrl/routing/features.py": {
      "bytes": 12371,
      "mode": 420,
      "sha256": "7de44ffd52b490d33b2f66f632d964c6df57f8a7ea31d34783db973db926b205"
    },
    "src/adrl/routing/policy.py": {
      "bytes": 6822,
      "mode": 420,
      "sha256": "a5d9bd9a9da8b48ee76cfe13cfd7f3a1cccb5ceb542d3178f5f3f294a48c4b60"
    },
    "src/adrl/routing/registry.py": {
      "bytes": 4732,
      "mode": 420,
      "sha256": "18ad3fc453d67c11fe8cd783ee2cfb596b03d12f4ece21cf7b672813e0365dae"
    },
    "src/adrl/routing/router.py": {
      "bytes": 10268,
      "mode": 420,
      "sha256": "36666f3e9a6944a9974d35b906e0bf231014f96798ba65dbb8670dfa19f24045"
    },
    "src/adrl/routing/rule_health.py": {
      "bytes": 3590,
      "mode": 420,
      "sha256": "c9843b350c36731bf5778b900b107d231181be794a88ec9b12cb91a49d2daa8b"
    },
    "src/adrl/routing/side_effects.py": {
      "bytes": 16243,
      "mode": 420,
      "sha256": "d617fa3d9ba2d8b93c4cf8d32571fe795ec979f40e21bce057b45b275d74699e"
    },
    "src/adrl/telemetry/__init__.py": {
      "bytes": 607,
      "mode": 420,
      "sha256": "cbf0dc80c108a2a5c0714c67a2588efe136d3969f0cdf31f70de3abb7ba7308a"
    },
    "src/adrl/telemetry/logging.py": {
      "bytes": 1538,
      "mode": 420,
      "sha256": "4fb1d7fb6d9d6f14439c5344f7021ed95edfa0ec5a865a136e26b6f1fd074e07"
    },
    "src/adrl/telemetry/metrics.py": {
      "bytes": 3025,
      "mode": 420,
      "sha256": "db03f5ff99a8cc0b476933315ea4ef00366bb432f47b7bbbf2f89a4dd38a1b34"
    },
    "src/adrl/telemetry/semconv.py": {
      "bytes": 926,
      "mode": 420,
      "sha256": "f03aab966149fe22a9fcda33a0097bbab9b144d4609014e4acf79bb14fec0dde"
    },
    "src/adrl/wire/__init__.py": {
      "bytes": 855,
      "mode": 420,
      "sha256": "530b1c1bba4f681b33433510837137e5d6d0e4653cb3544a4a2548d0de4da695"
    },
    "src/adrl/wire/adapters.py": {
      "bytes": 2187,
      "mode": 420,
      "sha256": "0f8abd8962d3a2ffeb8be2f7a9d060caa47b908e5a8fc2e177eb691144489600"
    },
    "src/adrl/wire/classify.py": {
      "bytes": 8548,
      "mode": 420,
      "sha256": "7abbce3cc0ba508bddea588bb81dcc55c6a7b88e3cbd2506e118dbc503c90b90"
    },
    "src/adrl/wire/identity.py": {
      "bytes": 7789,
      "mode": 420,
      "sha256": "61a3e71e6fb97617e82f3095750041607edbaa9eff43bf4f4f7c97f9a8ac2e5b"
    },
    "src/adrl/wire/observe.py": {
      "bytes": 11180,
      "mode": 420,
      "sha256": "a8a9e237b1cf6397597dfda4762f0e65507d7b2fbe09e8bdfa3970c35d928cca"
    },
    "src/adrl/wire/parse.py": {
      "bytes": 8112,
      "mode": 420,
      "sha256": "f4c7c61438e50c8b91ab08ff927dbb17d5887802949ff3ac27925c0d9fcef28e"
    },
    "src/adrl/wire/profiles/__init__.py": {
      "bytes": 54,
      "mode": 420,
      "sha256": "d4e7de031920d9e6d223384e9a097aa4c2ed50cd6259c70a1e6e60957a37fab2"
    },
    "src/adrl/wire/profiles/base.py": {
      "bytes": 3867,
      "mode": 420,
      "sha256": "928dc02f1909b939f71adcf70244d507b3bb1c122799339f50e7ef40f2077ad8"
    },
    "src/adrl/wire/profiles/messages.py": {
      "bytes": 5875,
      "mode": 420,
      "sha256": "be738637186caf85ef47745679e9d94dd34cff05cb51ed3005fbc7e0fa70524f"
    },
    "src/adrl/wire/profiles/messages_responses.py": {
      "bytes": 2609,
      "mode": 420,
      "sha256": "8a8d1d188144c834d4ec82e90dffc7e2842c893771b9da278ea032e2be239ee3"
    },
    "src/adrl/wire/rewrite.py": {
      "bytes": 2924,
      "mode": 420,
      "sha256": "eb49c51565003b70432666f557b33ce7c89064d630fdd448b15254198d8fe468"
    },
    "tests/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/adversarial/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/adversarial/conftest.py": {
      "bytes": 256,
      "mode": 420,
      "sha256": "096d1351989fa02d36f10c725853624ca8f1df24f83de5da9ee26bcbf07916ee"
    },
    "tests/adversarial/test_saf_suite.py": {
      "bytes": 4535,
      "mode": 420,
      "sha256": "d7a1d978c4dfecf3b54816a63d824f54eb2bb1c7531982cd28501478b9984cda"
    },
    "tests/adversarial/test_tru_suite.py": {
      "bytes": 4881,
      "mode": 420,
      "sha256": "a55949985c2269dcc29902af7dc95b1402b0e39731bb11c075f7466341d5b2e0"
    },
    "tests/conftest.py": {
      "bytes": 8701,
      "mode": 420,
      "sha256": "0998e7620ac04588746ca1b2f22ee5a2626e869cd8ce507708758430df81b9b9"
    },
    "tests/fixtures/launch_owner.py": {
      "bytes": 1397,
      "mode": 420,
      "sha256": "00d61d8eb0ff5f00b9b783e9e044f436f148461c8a8bb5ef1851daa9bb34da48"
    },
    "tests/fixtures/profiles/identity-v1.json": {
      "bytes": 1706,
      "mode": 420,
      "sha256": "39314dc7c49f415a368afe544570b8099d4215f223a5b3242a33a8678fae2aec"
    },
    "tests/fixtures/seccomp-v27.3.1.json": {
      "bytes": 12828,
      "mode": 420,
      "sha256": "9c1025c88ccaa517b648da571961838744ea2137f176bfe6a48b21294cae9c76"
    },
    "tests/fixtures/wire/compaction.json": {
      "bytes": 1259,
      "mode": 420,
      "sha256": "e13eee45e9d5b2cdf845b50fd1f2431878f01b64ba732dc00dabc41a91d01bf9"
    },
    "tests/fixtures/wire/continuation.json": {
      "bytes": 2820,
      "mode": 420,
      "sha256": "9208f708a25d64bff9020d0d792154fcbbba41a6c34c7a2131933ab036ea9c1d"
    },
    "tests/fixtures/wire/count_tokens.json": {
      "bytes": 1709,
      "mode": 420,
      "sha256": "0413c1d9033d9f2eecddf50b57b8d93e35d7beb02aa9152e7759b584938b7b4f"
    },
    "tests/fixtures/wire/escalation_parallel_tools.json": {
      "bytes": 1580,
      "mode": 420,
      "sha256": "2fa413954c24c338474854aed7d448876ed15f822ea99fc7c8416a55637511d1"
    },
    "tests/fixtures/wire/fork_subagent.json": {
      "bytes": 3250,
      "mode": 420,
      "sha256": "651b2b01ac64afcff23b6bd933fa86cd5d1d8e4e82590668e42968167bbd98bc"
    },
    "tests/fixtures/wire/metadata_only_user_turn.json": {
      "bytes": 1991,
      "mode": 420,
      "sha256": "6d2d342bbaf769aa7a4d9135f822cf7dedb4ec77e35ff0b4d8333b563bac41f2"
    },
    "tests/fixtures/wire/nested_subagent.json": {
      "bytes": 2150,
      "mode": 420,
      "sha256": "0e0e881ff882e443fbe3b414e7836897d70ab925603e74bd8184d0e63ccd5b2c"
    },
    "tests/fixtures/wire/parallel_tools_full.json": {
      "bytes": 3105,
      "mode": 420,
      "sha256": "505559666a116132c2cc492b7158c7b968f0da783646fa87350f7ba13481928f"
    },
    "tests/fixtures/wire/parallel_tools_partial.json": {
      "bytes": 2951,
      "mode": 420,
      "sha256": "d56eaa6e53ea1eacf36329c0892a8263bbfcb2c86d1ddd8e84a4d9e974d2e737"
    },
    "tests/fixtures/wire/pre_warm.json": {
      "bytes": 1896,
      "mode": 420,
      "sha256": "55bcf0673ed5aa3b3c7948d2d8b8fc1da4106c037c493d3c1da5fbf3164c5f55"
    },
    "tests/fixtures/wire/title.json": {
      "bytes": 928,
      "mode": 420,
      "sha256": "023640c7088508eeda108c1a774c012d1beccb5e0d728e1a1c05bed7cbc6224d"
    },
    "tests/fixtures/wire/topic_detect.json": {
      "bytes": 972,
      "mode": 420,
      "sha256": "3245b7021cd98b8b98c86a23713e8d7aea02cbbda0ad366fb4d3b4538dc42ae9"
    },
    "tests/fixtures/wire/user_turn.json": {
      "bytes": 2025,
      "mode": 420,
      "sha256": "0cab3bfbf06c45aab1e1be8f019159aaced9aed31e56f10be68c8292ef7c2816"
    },
    "tests/integration/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/cascade/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/cascade/conftest.py": {
      "bytes": 465,
      "mode": 420,
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/integration/cascade/test_controller.py": {
      "bytes": 12943,
      "mode": 420,
      "sha256": "5d86e61671de29a2082f223cdd8f641097842fd7ba5476ca286f2f6d66175759"
    },
    "tests/integration/cascade/test_review_defects.py": {
      "bytes": 6454,
      "mode": 420,
      "sha256": "857c1c1aeba37e29c5694d4414f06408409b2a92c2758c6ec227d46d94bc0b70"
    },
    "tests/integration/e2e/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/e2e/conftest.py": {
      "bytes": 7966,
      "mode": 420,
      "sha256": "90ab6359a3907e1d13920a3391133d385b0f6fc0d70e8cb62e8b7b29c595ca9c"
    },
    "tests/integration/e2e/test_composed_system.py": {
      "bytes": 10368,
      "mode": 420,
      "sha256": "28fa67ba5b497c4d9e8d89c78c5895e21b465e5bd8efcadf037266c2c76f55e6"
    },
    "tests/integration/e2e/test_outcome_contract.py": {
      "bytes": 9500,
      "mode": 420,
      "sha256": "b19cd9e234079e3076b966113b89dbb41f074922342ed0d0e639155baa48cc1b"
    },
    "tests/integration/e2e/test_pin_failure.py": {
      "bytes": 1793,
      "mode": 420,
      "sha256": "c974d6d2d3e09e24bd5547c3dc9334125e3b2273ff6017b2fb80ec58969d509a"
    },
    "tests/integration/e2e/test_product_services.py": {
      "bytes": 29411,
      "mode": 420,
      "sha256": "329a6b4071da40f87675375f530a3993a2cfb69b953468d611fc5692fc7dc963"
    },
    "tests/integration/e2e/test_review_defects.py": {
      "bytes": 5973,
      "mode": 420,
      "sha256": "f17cf912128501843517d4e134ae2c6664bb5be490197d8fe4c5200bc876ebfd"
    },
    "tests/integration/e2e/test_tru.py": {
      "bytes": 5645,
      "mode": 420,
      "sha256": "42652efc6d9484aba196e25d37a483226e1321e18855c6622ffa89a97ac4d081"
    },
    "tests/integration/e2e/test_trust_wiring.py": {
      "bytes": 3771,
      "mode": 420,
      "sha256": "43ae74ee8e66dde0b90bfbaee0a9bfbf8f082d036a2211a6c0afcfe0e9a950aa"
    },
    "tests/integration/gates/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/gates/conftest.py": {
      "bytes": 134,
      "mode": 420,
      "sha256": "925ed24d508f2058d26f5ce6f8de4d629500919b1abf96dbc4810fece3574b74"
    },
    "tests/integration/gates/test_pin_durability.py": {
      "bytes": 2549,
      "mode": 420,
      "sha256": "7007829914677d64e694b934c6868026e3cfaf62359ad6dcc746129c0863b5c4"
    },
    "tests/integration/ledger/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/proxy/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/proxy/conftest.py": {
      "bytes": 11824,
      "mode": 420,
      "sha256": "fe8bf67e23465d0597654bdfa93b50949fa6c7730eacc303870916b2f33192fd"
    },
    "tests/integration/proxy/test_fault_matrix.py": {
      "bytes": 7061,
      "mode": 420,
      "sha256": "683cecea87149979ae4f5f6888c62b418c874912120543640f433724a73a14a1"
    },
    "tests/integration/proxy/test_pinned.py": {
      "bytes": 6419,
      "mode": 420,
      "sha256": "36e97c508af175b32be4bb234cf9a54d0f3539415cecad24689da9092adb08f4"
    },
    "tests/integration/proxy/test_profiles.py": {
      "bytes": 1990,
      "mode": 420,
      "sha256": "46ff3d92a6ffbd8885b25e52a6e67a357276365caab866035e51bf55bfa2b48e"
    },
    "tests/integration/proxy/test_removal.py": {
      "bytes": 3352,
      "mode": 420,
      "sha256": "b488d5eb5ee8e6d5b6e6ca0baa1dd8d6d52b2be54e25a54690814e222a710473"
    },
    "tests/integration/proxy/test_routing_paths.py": {
      "bytes": 4494,
      "mode": 420,
      "sha256": "24e668347d358f36f7e080cfbc73a4cfaccdc1c84f46c10fa13a58bae4afc655"
    },
    "tests/integration/test_cli.py": {
      "bytes": 1088,
      "mode": 420,
      "sha256": "46a4da25d892d293447514428c8efb2c7029c42c8c643bbf8b8005956d5a49dd"
    },
    "tests/integration/test_cli_verify_snapshot.py": {
      "bytes": 3196,
      "mode": 420,
      "sha256": "56a6ef0e166aa8cee3254945d9d4df74ef5120ed0ac11925f7bb181c2cf74b14"
    },
    "tests/integration/test_launch_engine.py": {
      "bytes": 4846,
      "mode": 420,
      "sha256": "32f2f683e5dddb63e047c86f2cb1aadfac51046701765915b4bb176ffc26cc84"
    },
    "tests/integration/test_resource_engine.py": {
      "bytes": 7381,
      "mode": 420,
      "sha256": "a66c6e187c1012f6e39297abdc88af1c74de0d64cee3097940770cc1be18104f"
    },
    "tests/unit/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/cascade/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/cascade/conftest.py": {
      "bytes": 465,
      "mode": 420,
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/unit/cascade/test_boundary_tripwires.py": {
      "bytes": 5500,
      "mode": 420,
      "sha256": "1e1ea158cc979a2b435a2976075d231f6e7574e3b20130aca301d870c020f53f"
    },
    "tests/unit/cascade/test_handoff_sticky.py": {
      "bytes": 7453,
      "mode": 420,
      "sha256": "e9d6624337d29e7c11fd0ff24d79a1617210df1a5885f06bc5b270838138407f"
    },
    "tests/unit/gates/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/gates/conftest.py": {
      "bytes": 8009,
      "mode": 420,
      "sha256": "f39063ec22ae5c3762b8666971bf32f5c3fd47ffe958b6b2c42b4642d17a9108"
    },
    "tests/unit/gates/test_block.py": {
      "bytes": 3025,
      "mode": 420,
      "sha256": "05d72a875190cf71fdc694b209501dc0a2905a70a29ff949f3ca75d183a749c6"
    },
    "tests/unit/gates/test_content.py": {
      "bytes": 1909,
      "mode": 420,
      "sha256": "f0cf9ad15796159748e3b67450eb02839d220db129119daaace39b85700dbc23"
    },
    "tests/unit/gates/test_coverage.py": {
      "bytes": 1364,
      "mode": 420,
      "sha256": "ffbcf9882584c6acec0d7afd83a2b28bec32e059bff9848ba31e9e0203bde2c1"
    },
    "tests/unit/gates/test_egress_writer.py": {
      "bytes": 1958,
      "mode": 420,
      "sha256": "f6e83d902381ebdd6d062181bad53e7db6be6a3d3de13d13d3f5ec460c209f0f"
    },
    "tests/unit/gates/test_feasibility.py": {
      "bytes": 2515,
      "mode": 420,
      "sha256": "5caa1fb734c321de0f8b096aba41a41cfcb340ac12314508fbba8bb8fca7e92b"
    },
    "tests/unit/gates/test_observe_mode.py": {
      "bytes": 2856,
      "mode": 420,
      "sha256": "b31f9ccd6f8c5f84ca8d3871045c412e3ca755335eb5e5ce286323c8272c7ea5"
    },
    "tests/unit/gates/test_pin.py": {
      "bytes": 3440,
      "mode": 420,
      "sha256": "2edfc3a5ba67f7859e25192dc467cb905a87918118631f657c4f78a3585696e7"
    },
    "tests/unit/gates/test_pin_write_failure.py": {
      "bytes": 7973,
      "mode": 420,
      "sha256": "ce3e9c056dd09485b0590bc9b7b69bd28c1df2a13df462f59d7b0b6dacf84121"
    },
    "tests/unit/gates/test_pipeline.py": {
      "bytes": 8158,
      "mode": 420,
      "sha256": "d3cd972b9ca4cef20b93502bfdd7f4b3ea2b451220400963d094641768c8d1af"
    },
    "tests/unit/gates/test_repo_class.py": {
      "bytes": 6087,
      "mode": 420,
      "sha256": "b39eeb5693390c34ae0b369c3059a5d0b010d923e7ec759902a135fb2744092f"
    },
    "tests/unit/gates/test_sandbox.py": {
      "bytes": 3647,
      "mode": 420,
      "sha256": "5aac4a4702a151be6b738ac07aa41b9eec9acad03b5e22fee80c7ef71366877b"
    },
    "tests/unit/gates/test_secrets.py": {
      "bytes": 2976,
      "mode": 420,
      "sha256": "229b8dfa52ac3afded7c8f4727437d1049768c04d0f1f4fe9dcbc354219ad628"
    },
    "tests/unit/gates/test_workload.py": {
      "bytes": 4911,
      "mode": 420,
      "sha256": "47caab4f52becb3f5875cd982cb3797490ed930f9e4075d1d131a84e8002c554"
    },
    "tests/unit/learning/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/learning/conftest.py": {
      "bytes": 3944,
      "mode": 420,
      "sha256": "d9b57452143653991a05cf299a0d7bf073d79ae0a5647ce5cb99e993035e937e"
    },
    "tests/unit/learning/test_abstention.py": {
      "bytes": 3255,
      "mode": 420,
      "sha256": "3c14a5d6fc3d3410ed6fd742e9a4bb69aa6cc5e947a7586a849e085a73998d78"
    },
    "tests/unit/learning/test_artifacts.py": {
      "bytes": 4747,
      "mode": 420,
      "sha256": "f1f12afada374f40dc97e1ec0d1cc980b5a475d9cfc356cb30c500fc04a68d64"
    },
    "tests/unit/learning/test_dataset.py": {
      "bytes": 4293,
      "mode": 420,
      "sha256": "0875f9736aa544e5d89c82dc423ad8234df1894661e02a1a13b482f3b78ef936"
    },
    "tests/unit/learning/test_estimator.py": {
      "bytes": 2626,
      "mode": 420,
      "sha256": "67e5ca8963d4180cf2073fd3ee7e25e19f395805d99335e9b72727fad0b0d5aa"
    },
    "tests/unit/learning/test_explore.py": {
      "bytes": 3935,
      "mode": 420,
      "sha256": "b6909e90235924c026308e1bdfe26ea4c09ed106fa82cae3d1e3b63fa50e15c2"
    },
    "tests/unit/learning/test_improvement.py": {
      "bytes": 11949,
      "mode": 420,
      "sha256": "dd35b6f67bce6c75f26cfe476cd4464fb12f05e6a069999e36268a00452b1043"
    },
    "tests/unit/learning/test_pairs.py": {
      "bytes": 3200,
      "mode": 420,
      "sha256": "7c1ec762db521691164d94af5e8e879ec385a2ad947d4a60c6564cdc96500fe2"
    },
    "tests/unit/learning/test_readiness.py": {
      "bytes": 1061,
      "mode": 420,
      "sha256": "387ee35f6f6a392e5bb5a90ceb83a6a02f5be7c0dc71fb3587b6240b539e3757"
    },
    "tests/unit/learning/test_tiers.py": {
      "bytes": 4387,
      "mode": 420,
      "sha256": "696facc4b378c2c41a5be805f001196296d327d405ec4dac04a1bdf6debc7597"
    },
    "tests/unit/ledger/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/ledger/conftest.py": {
      "bytes": 3911,
      "mode": 420,
      "sha256": "010a76aad8e5d6b20585639ac45bbb42af795997bdc5622f8588206a62d6bf12"
    },
    "tests/unit/ledger/test_anchoring.py": {
      "bytes": 10465,
      "mode": 420,
      "sha256": "9f7a35b6ff66453013fc9a9a9f21bbf198d11c642e2787c55e5870ac9d169f08"
    },
    "tests/unit/ledger/test_data_inventory.py": {
      "bytes": 5266,
      "mode": 420,
      "sha256": "e08fe724b6bc84252c52cd383dccf3e24f94864d37a3a0ce8cf7b48911f7b2b1"
    },
    "tests/unit/ledger/test_events_and_labels.py": {
      "bytes": 5444,
      "mode": 420,
      "sha256": "f98a02f30e5dda2e65a62c1a98dd674f314a593a469bc2de250b36019b155741"
    },
    "tests/unit/ledger/test_outcomes.py": {
      "bytes": 6281,
      "mode": 420,
      "sha256": "92887f3c22fe9eb30d1e9b3762aef47967a11ad30bc523446c8ee9a2457eaca8"
    },
    "tests/unit/ledger/test_privacy_artefacts.py": {
      "bytes": 9366,
      "mode": 420,
      "sha256": "6e5bb64c39a75e64efb492cd3d5aadf8347db223015bd8acfc57a74b56fff647"
    },
    "tests/unit/ledger/test_state_counterfactual_shadow.py": {
      "bytes": 5217,
      "mode": 420,
      "sha256": "1d95ca1664ce9d1154d11b783fc1e1316d9029b4f1bc59b41ece6e574536e23e"
    },
    "tests/unit/ledger/test_verification.py": {
      "bytes": 8662,
      "mode": 420,
      "sha256": "e0ce2701e710e312595d76655b96f3778e498cf97ffdf71bad6032f8e2b30a94"
    },
    "tests/unit/proxy/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/proxy/test_fallback.py": {
      "bytes": 2021,
      "mode": 420,
      "sha256": "fe2104131ec80366485a03abb87d57feac7870b9ad8034d65856d15c7277cdae"
    },
    "tests/unit/routing/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/routing/conftest.py": {
      "bytes": 465,
      "mode": 420,
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/unit/routing/helpers.py": {
      "bytes": 4132,
      "mode": 420,
      "sha256": "734c48d9848c452adf3099874c0e1a0c198cf9132472e42bbe51c8b71849a219"
    },
    "tests/unit/routing/test_cost_policy.py": {
      "bytes": 6070,
      "mode": 420,
      "sha256": "5719bf0fc5618cd9c1cec8cbb240862cd29e440da4a01558416283d44458538d"
    },
    "tests/unit/routing/test_gateway_config.py": {
      "bytes": 3939,
      "mode": 420,
      "sha256": "a0da57f4bea464fc3734f779c0bd4f9ff319f927527f57c8bb84444b45483cbb"
    },
    "tests/unit/routing/test_mixed_intent.py": {
      "bytes": 3926,
      "mode": 420,
      "sha256": "7f55b41a8b880fcc9bb1c2365957cdbb5bd64cb7cb23d94c4bcea068933a5fad"
    },
    "tests/unit/routing/test_registry_features.py": {
      "bytes": 5109,
      "mode": 420,
      "sha256": "735b0211b50d8bacbb721519cd391833d650ab2bd0fb565ff8cbc54262f695da"
    },
    "tests/unit/routing/test_router.py": {
      "bytes": 7175,
      "mode": 420,
      "sha256": "6125b94e23395072b1e505a94d1c3ec26a638a9eb5acce5648872e62f071fa75"
    },
    "tests/unit/routing/test_side_effects.py": {
      "bytes": 6479,
      "mode": 420,
      "sha256": "33664bee279c24694789663aeb51afb6c8a241e530209eae0bca64374e771749"
    },
    "tests/unit/test_api_contract.py": {
      "bytes": 5572,
      "mode": 420,
      "sha256": "e88641a573a983f7494df8352fc0ff82408e93288ec13fdbf68e700cbf578e74"
    },
    "tests/unit/test_attempt_capacity.py": {
      "bytes": 18369,
      "mode": 420,
      "sha256": "dd1d91f5284f09ae7ee19ecb5bb10d6286bec82c75c6421e865aa04167c74584"
    },
    "tests/unit/test_attempt_coordinator.py": {
      "bytes": 24679,
      "mode": 420,
      "sha256": "62a7eca2ee0266fb95e8e1cbda2d93be2d9559d201c673f6eb2655dbfd181dc1"
    },
    "tests/unit/test_attempts.py": {
      "bytes": 18897,
      "mode": 420,
      "sha256": "4d54d16b9dec725d6a8a2b5f33dabd2fda214fe2019ff2a86d6ecbfef55c4096"
    },
    "tests/unit/test_capture.py": {
      "bytes": 18506,
      "mode": 420,
      "sha256": "8e46474960cc3f1574b884840e0b39f439b17cc8e2e57904ad8ad5146d438a7f"
    },
    "tests/unit/test_config.py": {
      "bytes": 3394,
      "mode": 420,
      "sha256": "8cb002b9206a441ca3730270a60335ec36646903a8ccbc3ad0c8344cb48b07e4"
    },
    "tests/unit/test_core.py": {
      "bytes": 4809,
      "mode": 420,
      "sha256": "d0172ff5a0d7ed7319b9595a9bf9381d903c16fab4ec37a1ec800729d57d2416"
    },
    "tests/unit/test_create_receipt.py": {
      "bytes": 13947,
      "mode": 420,
      "sha256": "c705d8845e740dc65d452caeaf0b18c419c3aa4cb5f1b8e995620ec2bed43c8f"
    },
    "tests/unit/test_data_inventory_migration.py": {
      "bytes": 1057,
      "mode": 420,
      "sha256": "94e45373f18f8d2254a515775493fc186a78873c5f39285701f34ee92522bf5e"
    },
    "tests/unit/test_egress.py": {
      "bytes": 2739,
      "mode": 420,
      "sha256": "cf8f778fab58fcc4dd05d03ae6ed6a8cadef183c8fec4a47492cd2522e169011"
    },
    "tests/unit/test_engineering_tools.py": {
      "bytes": 4620,
      "mode": 420,
      "sha256": "0e2dc01cd0abebbb61104f744dcf71a2eae4f848289b9f7718752008e9f35436"
    },
    "tests/unit/test_isolated_execution.py": {
      "bytes": 28810,
      "mode": 420,
      "sha256": "a7ded1c4fc3c9f1c5fec11a350a076368fcf99c2544836da70793db4b5ab8a25"
    },
    "tests/unit/test_key_revocation.py": {
      "bytes": 13543,
      "mode": 420,
      "sha256": "88406cb70059b4e1b272669d3c6d558e607415f0dd581991de46d9f57bd19cf8"
    },
    "tests/unit/test_ledger_cancellation.py": {
      "bytes": 1171,
      "mode": 420,
      "sha256": "e3e9fe83e60f06cd7892398b339f7db98373cccb3e7a8695cff35ab877c6f36b"
    },
    "tests/unit/test_ledger_store.py": {
      "bytes": 5798,
      "mode": 420,
      "sha256": "a4a8f03c183e99ba90d7bc9dd7f89d734dff2a9fa43d1e79d776dac58c81e4e5"
    },
    "tests/unit/test_process_owner.py": {
      "bytes": 18017,
      "mode": 420,
      "sha256": "2abc2f9d680caaec1335badc9e0f4face39b8666daf1ea0a6bcd894101fdc4cc"
    },
    "tests/unit/test_product_client.py": {
      "bytes": 7405,
      "mode": 420,
      "sha256": "053582512b7a5ea715eb1b608ca601b1d215689f3b90ad39363bc430653f6bf9"
    },
    "tests/unit/test_product_migration.py": {
      "bytes": 3908,
      "mode": 420,
      "sha256": "df0a92e1c28c709442da4255c9632e9547b258ce47464937d2ae07af2fb39392"
    },
    "tests/unit/test_resource_owner.py": {
      "bytes": 24404,
      "mode": 420,
      "sha256": "e272079c97194e2a266bc376d0768a7d60c269a86458d38345739425cc30627f"
    },
    "tests/unit/test_routing_lab.py": {
      "bytes": 5478,
      "mode": 420,
      "sha256": "1e6252edcdbddddd93dcd5ec01479a5f04274582932586d9078a969555f269da"
    },
    "tests/unit/tru/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/tru/conftest.py": {
      "bytes": 293,
      "mode": 420,
      "sha256": "4e44fc41ac69e6a3641ba8ef2a72c78fc9cb8cdcb3f67f6f44e066d4dc6606e4"
    },
    "tests/unit/tru/test_deployments.py": {
      "bytes": 11941,
      "mode": 420,
      "sha256": "7fac080d29e32ca58865522f89d9d88d1945b0e39f1b0a4ac5cb27eda34de388"
    },
    "tests/unit/wire/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/wire/conftest.py": {
      "bytes": 1366,
      "mode": 420,
      "sha256": "2d022311296d129cd0d0fb8cc478c8c7d5d9e19dbeefcd9672090669092bde3e"
    },
    "tests/unit/wire/test_classify.py": {
      "bytes": 4038,
      "mode": 420,
      "sha256": "024df892a7ee443aaaacf602a7e81ac5ce984d2c34d9b84adef197641a8aab0a"
    },
    "tests/unit/wire/test_identity.py": {
      "bytes": 4582,
      "mode": 420,
      "sha256": "dc9cc6919b150a86522f29663255a9194368b579c525d778ab673e221b0de88d"
    },
    "tests/unit/wire/test_observe.py": {
      "bytes": 5165,
      "mode": 420,
      "sha256": "fd8d16f55c56a8c3155531495cee04c22866eaa822b2b63e9c931b5ee8d90fa3"
    },
    "tests/unit/wire/test_parse.py": {
      "bytes": 2348,
      "mode": 420,
      "sha256": "99badc52c64d96a0fb8c0c9699226eba184a4fd68f11f04cbffbb1cfbbbd8e50"
    },
    "tests/unit/wire/test_profiles.py": {
      "bytes": 3123,
      "mode": 420,
      "sha256": "e9afac4d2c1dff6a52d4a75e33b3f206913572e0f61dc9bcabdd151272807391"
    },
    "tests/unit/wire/test_rewrite.py": {
      "bytes": 1730,
      "mode": 420,
      "sha256": "ca91d55a0e36402bb3c0a80f0a100ee714c520df140a2586993f39e7a4aba096"
    },
    "tools/adr_module_map.py": {
      "bytes": 4684,
      "mode": 420,
      "sha256": "32b3088a50690481cf6b12b2e2e36ec2d32e9e5f606a2a4925dc13d28290b349"
    },
    "tools/check_all.py": {
      "bytes": 8357,
      "mode": 420,
      "sha256": "38b2a09a6686ee8923634f9ab25e35d80c0016ef5829e2028590ed1326919280"
    },
    "tools/check_config.py": {
      "bytes": 2299,
      "mode": 420,
      "sha256": "c4483f2c6998f75dd5c4a59d8a8fd7dc50ce509981d191046fb9685e51bc87bb"
    },
    "tools/check_data_inventory.py": {
      "bytes": 6258,
      "mode": 420,
      "sha256": "98d73890d3b4bcab0904cc4236e4e0bc7894f07f9fb164e3eda987681e705ee7"
    },
    "tools/check_learning_contract.py": {
      "bytes": 2587,
      "mode": 420,
      "sha256": "ae72d6162c1834ff8273b55de89d994628b15806451a4921adfac5db9045c724"
    },
    "tools/check_ledger_discipline.py": {
      "bytes": 2330,
      "mode": 420,
      "sha256": "751b6b350f3aaf5ffbfe6ebbd007e1ca752b9a91b737ce0e97f0176fa924b2dc"
    },
    "tools/export_api_contract.py": {
      "bytes": 880,
      "mode": 420,
      "sha256": "f3a2a54e7b82c145d5c1aff0059d408c75dd52543ff9b0d7832de7bfef476020"
    },
    "tools/gen_dev_keys.py": {
      "bytes": 2570,
      "mode": 420,
      "sha256": "10c267560a3396c27f4f9df920fc40dd41b0a08a0d4423ec876c940d22859423"
    },
    "tools/gen_litellm_config.py": {
      "bytes": 8609,
      "mode": 420,
      "sha256": "64be40a877345d6da762eb061bcb13d06013ba8bbdf045d6eece5532a58e3139"
    },
    "tools/run_routing_lab.py": {
      "bytes": 21189,
      "mode": 420,
      "sha256": "6dace633d24fa4d185c418c9a070c14dbce53361057d9a78a00dc93c33946ff7"
    },
    "uv.lock": {
      "bytes": 158986,
      "mode": 420,
      "sha256": "8da7c7f9497ecdc071768eadf85535232c1d92f9eb74ff6244b74d6b4fe61cd0"
    }
  },
  "source_before": {
    ".gitignore": {
      "bytes": 251,
      "mode": 420,
      "sha256": "5a46e538a34a4bc94faa64f0af2a0918926e4213251a60e851eaf41922db02b3"
    },
    "AGENTS.md": {
      "bytes": 3633,
      "mode": 420,
      "sha256": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490"
    },
    "CLAUDE.md": {
      "bytes": 3633,
      "mode": 420,
      "sha256": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490"
    },
    "README.md": {
      "bytes": 13374,
      "mode": 420,
      "sha256": "dda387731ad435a2937414c8d35d3f2b51cb08841291013620571c731a554c29"
    },
    "api/adrl-api-v1-preview.json": {
      "bytes": 52939,
      "mode": 420,
      "sha256": "5a3f2c5401acd73d3a30a89fb24c94660d9a2b7c9f625b4a7c6acef987d03757"
    },
    "artifacts/lab/routing-suite-v1.json": {
      "bytes": 2503,
      "mode": 420,
      "sha256": "dfe4125445ace13eb6fbe064b0ed52576df5a71ddaeebe2568cc93fb047dc7a9"
    },
    "config/detectors.yaml": {
      "bytes": 3049,
      "mode": 420,
      "sha256": "d7e504d17341680bcfbf8bc9f76c435aa1bfc45bf53efbf208305604364d2f55"
    },
    "config/endpoint-inventory-v1.json": {
      "bytes": 1929,
      "mode": 420,
      "sha256": "67d18715549c041215deca75f0002bf486ce946b55a593a6e7d815c3e291212e"
    },
    "config/endpoint-inventory-v1.sig": {
      "bytes": 89,
      "mode": 420,
      "sha256": "e8a78202b9ff2985ec0fe9cc7287c01c434a27466a2445ac8a35fe56bc1aa762"
    },
    "config/keys/dev/README.md": {
      "bytes": 934,
      "mode": 420,
      "sha256": "1f2001f55f04ae0c577e723a7d70205cab0c194d99ad337f5c72c63265ee918a"
    },
    "config/keys/dev/checkpoint-signing.pub": {
      "bytes": 113,
      "mode": 420,
      "sha256": "54c0986810789840eaede4560aa9cfbab945ed5a494fd3b83a071e82460adb2c"
    },
    "config/keys/dev/manifest-signing.pub": {
      "bytes": 113,
      "mode": 420,
      "sha256": "aa93b81e39a6986964f8f574eb71c9a3510f07881a553eef24b199e536292655"
    },
    "config/learning-contract-v1.json": {
      "bytes": 1529,
      "mode": 420,
      "sha256": "8cfdf6a5f27f3f80839d6874831859dc0b6d71ed31440a9f33e385f0ee5ec58c"
    },
    "config/policy.yaml": {
      "bytes": 1486,
      "mode": 420,
      "sha256": "fd7522fda0c1d1c9fb1d096e603b8b3df2d981894658012e4ae2fa08439dc9bc"
    },
    "config/prices.yaml": {
      "bytes": 539,
      "mode": 420,
      "sha256": "07fd0c8da1cce030d210f82aabfb785b81d51b3b7e5dddedb848dd2584744dd5"
    },
    "config/provider-pairs.yaml": {
      "bytes": 1877,
      "mode": 420,
      "sha256": "032a460e3e2eae0b6715a82c1a0beb60d590b7f78bf0a485245bbb6e3a3d5175"
    },
    "config/repo-classification-v1.json": {
      "bytes": 1241,
      "mode": 420,
      "sha256": "47d7790c3eb71be692b74332a2e01de3b19011b10609722fdaf413279cf97b42"
    },
    "config/repo-classification-v1.sig": {
      "bytes": 89,
      "mode": 420,
      "sha256": "3487b15e06f60da66bfac3ed6dc4aa70e7091779b0c10a7f46d05380bdb70d5b"
    },
    "config/rungs.yaml": {
      "bytes": 1597,
      "mode": 420,
      "sha256": "39c0b9521d9e8ccbb0b4750bed1fc90a95be9f4427d4d0cb94d7f8d56c79935e"
    },
    "config/tripwires.yaml": {
      "bytes": 696,
      "mode": 420,
      "sha256": "201d15de3d6115f46c0ac7fe5eeda91011701f63e781e88b6f8b269238dea4db"
    },
    "config/trusted-tool-servers.yaml": {
      "bytes": 797,
      "mode": 420,
      "sha256": "b750cb935bdb7547a2b1ded6278df1cf14e8ef59f26a9ec95905bc0edd3dbd7a"
    },
    "config/utility-fingerprints.yaml": {
      "bytes": 950,
      "mode": 420,
      "sha256": "ef9d86f19f39342f3359e7e1fc7551a7ea0a56756ff77e0f8f010905f383411a"
    },
    "docs/adr-module-map.md": {
      "bytes": 31183,
      "mode": 420,
      "sha256": "1ae7ad9678422e94a9903581d99e12d51888a8bbdf5feb0ea1e1a2e4d0af39e4"
    },
    "docs/attempt-coordination.md": {
      "bytes": 6572,
      "mode": 420,
      "sha256": "0d129f7afdec81d426656a994b1fdf988eb98d43438d65fa93fbb3fa0d221490"
    },
    "docs/attempt-lifecycle.md": {
      "bytes": 9442,
      "mode": 420,
      "sha256": "bbc398599c579392deb4020de3f98c65e71445418763755f5ea0b2a84cd2cd28"
    },
    "docs/data-inventory.md": {
      "bytes": 37783,
      "mode": 420,
      "sha256": "867f8510b6103079ef1e01b67a5307012087b0ff86800d4e7cfec6111d08eea7"
    },
    "docs/egress-anchoring.md": {
      "bytes": 5172,
      "mode": 420,
      "sha256": "d79a9f636a2b091b943cbd9caaf7e514a102309a4aabe6eec24f15a9e48f9444"
    },
    "docs/engineering-checks.md": {
      "bytes": 2339,
      "mode": 420,
      "sha256": "f62b353c39b9ddffdcc1f137535beed0afcef15fdb5e7dd5607b9c15d3fa6144"
    },
    "docs/isolated-execution.md": {
      "bytes": 8298,
      "mode": 420,
      "sha256": "c5ae8f71c16386eb516afcd5eedb29d5f9a88d756b51472d743e5798b5d55247"
    },
    "docs/key-revocation.md": {
      "bytes": 6111,
      "mode": 420,
      "sha256": "d51f135f6586589d2698612ce5680494c6ed06f7031812005af8d2434ef174a9"
    },
    "docs/known-gaps.md": {
      "bytes": 15171,
      "mode": 420,
      "sha256": "421651ee56e55db65b0857f67cad915480f17a67994aa9eba8f477a79a2970aa"
    },
    "docs/operator-captures.md": {
      "bytes": 5873,
      "mode": 420,
      "sha256": "62f7acf78ee0be3922c538ad03276252999c213e0c77ded03a3bfc95007caecc"
    },
    "docs/outcome-contract.md": {
      "bytes": 1796,
      "mode": 420,
      "sha256": "873d412f0735ae7501515c08687fbd4fc276eca213f2b99f6bd017312d1f5815"
    },
    "docs/process-ownership.md": {
      "bytes": 5470,
      "mode": 420,
      "sha256": "f2e6810a2cfc67b4d6918367ebb17adf0c9f21401cb600dcca58cc643e8f4d8c"
    },
    "docs/product-services.md": {
      "bytes": 14964,
      "mode": 420,
      "sha256": "f20f331de15c5083c557eb9f26406957a9eee6542451ae902aa5d0f25ae30d02"
    },
    "docs/protocol-boundary.md": {
      "bytes": 4006,
      "mode": 420,
      "sha256": "b5469f938dc2e96bc059dd812c388e0f6fb5219333d7d76f96f81da8ec2ccf38"
    },
    "docs/responses-admission.md": {
      "bytes": 3909,
      "mode": 420,
      "sha256": "f4ad3cf11226661c08c0f5dbc054a6f17ef8fa49faca3be1a8fc41a2fac3aaa8"
    },
    "docs/routing-features.md": {
      "bytes": 2267,
      "mode": 420,
      "sha256": "ca328c13ebdbcbee3208b4bcbda6d7967b0c32a247f04e3f1300d42c70f6d577"
    },
    "docs/routing-lab.md": {
      "bytes": 3920,
      "mode": 420,
      "sha256": "cb4e0b14204354e061fb1fdde4bffd1bf0949498aeab1bd7ddbb7ffb47e1171d"
    },
    "docs/stopped-resource-ownership.md": {
      "bytes": 7389,
      "mode": 420,
      "sha256": "b21ccc8c1a6b44895fd82b03e80afd610b10f9cb1b9a1649c3d26fb1d0dcc7cf"
    },
    "docs/verifier-experiments.md": {
      "bytes": 6216,
      "mode": 420,
      "sha256": "1a1c04c2cc2480b4d2c3da48586f1415fe69069ef9301cf60b3a7f74cb415aad"
    },
    "pyproject.toml": {
      "bytes": 1764,
      "mode": 420,
      "sha256": "5a124bb958e981557d4a3f62b28843f348ca306e4e31876a7ebc907dd95b4001"
    },
    "src/adrl/__init__.py": {
      "bytes": 82,
      "mode": 420,
      "sha256": "f1de990ba880b21895f4888c739207ca4c3c16b222c0933a2b26aa4a03cce8c0"
    },
    "src/adrl/api/__init__.py": {
      "bytes": 77,
      "mode": 420,
      "sha256": "02d1a3f2332e8662f52c584a15c490ba068b58294f970536391f0ca9d2bcedef"
    },
    "src/adrl/api/auth.py": {
      "bytes": 2944,
      "mode": 420,
      "sha256": "d666e1fa36b41d16448143eed404a7ccb0fde0cf6d32e70747df89b85da1bc3d"
    },
    "src/adrl/api/client.py": {
      "bytes": 6717,
      "mode": 420,
      "sha256": "7679bff2e7f5afc32800d9bc8bffe5bc7908ddf7c634036cd08bcc9ac18cbd4e"
    },
    "src/adrl/api/contracts.py": {
      "bytes": 10507,
      "mode": 420,
      "sha256": "35036e9782944730250846999f5dcd6e690717d7751e2275463696ff4e26a461"
    },
    "src/adrl/api/http.py": {
      "bytes": 4934,
      "mode": 420,
      "sha256": "c129cbd845d04583af3f566099117ba58e7fa12cc75694cc7f60a9161e3f8bd1"
    },
    "src/adrl/api/schema.py": {
      "bytes": 6151,
      "mode": 420,
      "sha256": "e839e85d32982463056a5bedeb21ed99c1ede5602f38acb922fd970a27044581"
    },
    "src/adrl/api/service.py": {
      "bytes": 15425,
      "mode": 420,
      "sha256": "add6130fe1b3fe65fe37b2179a025f59aa07c315d14a6a7ea648aed43f5f8818"
    },
    "src/adrl/api/store.py": {
      "bytes": 12008,
      "mode": 420,
      "sha256": "9527d95565df58003469be2ea62514d8cb13fdce8b87295e4a06b6c76b366dd8"
    },
    "src/adrl/app.py": {
      "bytes": 15403,
      "mode": 420,
      "sha256": "ee397176ddcd305a1b5c70eb551a06e98b2065a076fa04593edb9da724a7741a"
    },
    "src/adrl/cascade/__init__.py": {
      "bytes": 300,
      "mode": 420,
      "sha256": "bc8b4bd3f53c5cbf7dc8ed81ee1ed9719c01d7ae158a11ec29263efa2e08c582"
    },
    "src/adrl/cascade/boundary.py": {
      "bytes": 3431,
      "mode": 420,
      "sha256": "66839b708bc041b4f26aa74d9facde2ea9e367a9263c492a90e3d3ef12fc98e2"
    },
    "src/adrl/cascade/controller.py": {
      "bytes": 26677,
      "mode": 420,
      "sha256": "fedef16cf2a4ce239f8c7c07eb27331b6bdeb5656735b84ab925f707adbe0a1d"
    },
    "src/adrl/cascade/handoff.py": {
      "bytes": 12784,
      "mode": 420,
      "sha256": "7a6e066343ac3fd87a63f1dd1ddecda6aa29269f28dc9ec13da88aad106b747c"
    },
    "src/adrl/cascade/sticky.py": {
      "bytes": 5423,
      "mode": 420,
      "sha256": "28346143b50492f80c41aff7ce044ff27447bb335146bf236b37500c58f711cf"
    },
    "src/adrl/cascade/tripwires.py": {
      "bytes": 16071,
      "mode": 420,
      "sha256": "c91eb8b1feeaf8e62f0ae5866d76205f3e3fe8a627d29885b893d70d1829c728"
    },
    "src/adrl/cli/__init__.py": {
      "bytes": 74,
      "mode": 420,
      "sha256": "aa78bc2cbcd04512b0ce732a5272efb78c4f9bb95daa7d7d59c0b4e7485575b4"
    },
    "src/adrl/cli/improvement.py": {
      "bytes": 4845,
      "mode": 420,
      "sha256": "916f93bad7c38e57b0626dcea70e833a02ad3487d4aaa8a91970339e10421963"
    },
    "src/adrl/cli/ledger_commands.py": {
      "bytes": 9857,
      "mode": 420,
      "sha256": "4d78faf44948f73928cba50f0fba8b4c0c2a32bb05250f1f7b121a784a5045fb"
    },
    "src/adrl/cli/main.py": {
      "bytes": 18764,
      "mode": 420,
      "sha256": "b155525971ee910191cccf609bcf2760c1f19a170fb00c6de8907ee567429322"
    },
    "src/adrl/cli/product.py": {
      "bytes": 11150,
      "mode": 420,
      "sha256": "048db7e3d777a32b57badea048e37fb3cc0774ecabfdeefc5eff927e53ff02c5"
    },
    "src/adrl/config/__init__.py": {
      "bytes": 287,
      "mode": 420,
      "sha256": "3803eb7d9d9190983da2058ca3d85a56d1bf2386d94d3743b3fd445760585bf7"
    },
    "src/adrl/config/checks.py": {
      "bytes": 11700,
      "mode": 420,
      "sha256": "de6b5ba06701c0deeddde05ba9f9bbe057a507e58107cfb4f5fd56568b277cc6"
    },
    "src/adrl/config/loaders.py": {
      "bytes": 6206,
      "mode": 420,
      "sha256": "fe0ad675a1d6b49648c7b9c3a2c7ba813b3abcc421d204a35309cfc066896792"
    },
    "src/adrl/config/models.py": {
      "bytes": 14108,
      "mode": 420,
      "sha256": "baf7f4346711468102c2644787cc0f275ee84e70972a51d2482bcfd648b94dd0"
    },
    "src/adrl/config/settings.py": {
      "bytes": 3538,
      "mode": 420,
      "sha256": "4a4daad400b9786e32edead3c7ad41e117e39459f93e915b83651b237a1d98b6"
    },
    "src/adrl/core/__init__.py": {
      "bytes": 2225,
      "mode": 420,
      "sha256": "2e4be193ed644ada5559624553d72d9f5c6d4a98dded8b7e974692146ab0e983"
    },
    "src/adrl/core/attempt_coordinator.py": {
      "bytes": 10359,
      "mode": 420,
      "sha256": "08d43e990442e2d55c5785fbf86b016b3ba1d07864c536723d2b1de8a00c61c2"
    },
    "src/adrl/core/container_control.py": {
      "bytes": 14795,
      "mode": 420,
      "sha256": "15942e04fe83bfc419b2c4913505ab0df01909a429f6c86096a2430936282e69"
    },
    "src/adrl/core/enums.py": {
      "bytes": 7138,
      "mode": 420,
      "sha256": "fa1a86d4c6ecc321ff7baf945aec440b8cb9a9a3937d78c3b9c9ffb435bf9bc7"
    },
    "src/adrl/core/errors.py": {
      "bytes": 4007,
      "mode": 420,
      "sha256": "4a9b11ae4fa527a813e800ebff00c2edfc04d2dd8cea0b0d6d7cfa7e1916bfff"
    },
    "src/adrl/core/execution_control.py": {
      "bytes": 9539,
      "mode": 420,
      "sha256": "435b1b28c2219e8b571c5895ff7d9b359356cefb594e3eae734a99a006c52a49"
    },
    "src/adrl/core/ids.py": {
      "bytes": 2294,
      "mode": 420,
      "sha256": "903b7c34cbae920f9a00edffcfa57e56d866090004925f712f90d7f00167f9e2"
    },
    "src/adrl/core/isolated_execution.py": {
      "bytes": 20808,
      "mode": 420,
      "sha256": "d8d994b245ae30f9b535c18a0f6fbddf67c45bc88ce76f37e0f6c5b6b1edba5e"
    },
    "src/adrl/core/launch_markers.py": {
      "bytes": 4486,
      "mode": 420,
      "sha256": "b3d95e9b7a7ba00e0f2f0cfee122aa7ce261eb2639e1fd29af314e5ddbd8c75f"
    },
    "src/adrl/core/ports.py": {
      "bytes": 6623,
      "mode": 420,
      "sha256": "8e0380c0b7d01e3b81bb3e6e499c6608b71522fd83f1e508d721a90b2ebf2c6d"
    },
    "src/adrl/core/process_anchor.py": {
      "bytes": 5134,
      "mode": 420,
      "sha256": "7e30ca14f22cef0787d3381eee8f9db75814813961bea4a1bb94984b5b68ca14"
    },
    "src/adrl/core/process_owner.py": {
      "bytes": 13491,
      "mode": 420,
      "sha256": "be67390cc95dbea608a1cf170e9452fc787730e2a60fc44825b58fcefa7d94c4"
    },
    "src/adrl/core/resource_owner.py": {
      "bytes": 21451,
      "mode": 420,
      "sha256": "5398a355ac7571929203e81eef8efcbc9436cf5452d3e3ee4c1440581b3d68f9"
    },
    "src/adrl/core/types.py": {
      "bytes": 13725,
      "mode": 420,
      "sha256": "1378a303072abce0c1257c6c1b346991b83dbeee204e51d5a8560c2e2f57e1b1"
    },
    "src/adrl/gates/__init__.py": {
      "bytes": 447,
      "mode": 420,
      "sha256": "0566861be1abd45018586c80ea2455a144e4fc8ef6e14f60a27f9d02cf2dbb23"
    },
    "src/adrl/gates/block.py": {
      "bytes": 7604,
      "mode": 420,
      "sha256": "b4fbf137ccfda62d36babb611bd875fc8e96ed835fc03373cca0b66b00174c7e"
    },
    "src/adrl/gates/cli.py": {
      "bytes": 10168,
      "mode": 420,
      "sha256": "aebd8c3eb7a3e53351eb3eb6ba88c0335fbbb27e94de225a6f9c8410bc601ef8"
    },
    "src/adrl/gates/content.py": {
      "bytes": 8213,
      "mode": 420,
      "sha256": "788bd77d75fe741557cfcc3a1d34c7d6c3bb0dd0f56f1ca9b0153407f7f8b194"
    },
    "src/adrl/gates/coverage.py": {
      "bytes": 2638,
      "mode": 420,
      "sha256": "e5ea97fa70fc83eec31b65285b4e7df464f69507284fda90075c867b6313bfd3"
    },
    "src/adrl/gates/deployments.py": {
      "bytes": 8218,
      "mode": 420,
      "sha256": "4657f74d3f2aefeb4c4c3c007d5d97ba67635475df500c8479278129295203c2"
    },
    "src/adrl/gates/detectors.py": {
      "bytes": 1887,
      "mode": 420,
      "sha256": "9a36fa3fd5e1385988f15f7a8845300b751e4aac6383deca1a7306e1bdb3935a"
    },
    "src/adrl/gates/egress.py": {
      "bytes": 6078,
      "mode": 420,
      "sha256": "68d6eec54dac44da14bfdc6e9f74110a0e9a451d389aa6fff31f40f3cba2da43"
    },
    "src/adrl/gates/feasibility.py": {
      "bytes": 8301,
      "mode": 420,
      "sha256": "53bee77bbe27ebec7fedc8e8be813823b86b322d56af653dab79909501cf5ad6"
    },
    "src/adrl/gates/measure.py": {
      "bytes": 4199,
      "mode": 420,
      "sha256": "ddb1c238ee1b05b4a28d3ed10418ee2c6e8ebdd6ccb7be6b8f9cd787c4fd19a0"
    },
    "src/adrl/gates/pin.py": {
      "bytes": 17576,
      "mode": 420,
      "sha256": "525972e0f191b92c92ecd483a76619806da51f63124987cfe82857aa1986f9d1"
    },
    "src/adrl/gates/pipeline.py": {
      "bytes": 24986,
      "mode": 420,
      "sha256": "7c33d96afd92a23913d5877482fb56fa25252979c11d458be25012b7d9bf7603"
    },
    "src/adrl/gates/repo_class.py": {
      "bytes": 14810,
      "mode": 420,
      "sha256": "ea362f101fc267fa00f0ebc373ff57f020aa7113d384e7c65f33974d6d651624"
    },
    "src/adrl/gates/sandbox.py": {
      "bytes": 9961,
      "mode": 420,
      "sha256": "2726fe38e484eaf8402f3bd04e648ebd257dc1f0e47f0cd7d0f2c417ced9714b"
    },
    "src/adrl/gates/secrets.py": {
      "bytes": 12884,
      "mode": 420,
      "sha256": "cd60482c0bec4d4fce167283a4d9e629df220bd65458a285a772cfeacd372796"
    },
    "src/adrl/gates/suppression.py": {
      "bytes": 1372,
      "mode": 420,
      "sha256": "e191a45a9a4d39c620de57fef049685f1bc47beb7981bd29082277ac508274d0"
    },
    "src/adrl/gates/workload.py": {
      "bytes": 12152,
      "mode": 420,
      "sha256": "06190e43f32cdabfb1b3b70466f3b0b1982b8898924dac9c29572d126c27c29c"
    },
    "src/adrl/learning/__init__.py": {
      "bytes": 300,
      "mode": 420,
      "sha256": "87db4b96f6dc2ed884dedcfd80956d2deebed4e7e219960f44b91b96bdbe6244"
    },
    "src/adrl/learning/abstention.py": {
      "bytes": 11124,
      "mode": 420,
      "sha256": "04c7f7c58ad90da533854f186e3348f3f0a9a6975a28c1a7acfe3e391bd57119"
    },
    "src/adrl/learning/artifacts.py": {
      "bytes": 8598,
      "mode": 420,
      "sha256": "b619ab050dfea6317521551de7ed56b188e28a10da9dab488f9b9950145d4be0"
    },
    "src/adrl/learning/dataset.py": {
      "bytes": 14278,
      "mode": 420,
      "sha256": "9e6ec8fcae5b78b07e1de0e874b338bc0233cab69bb8f39e78c3235bec0fa192"
    },
    "src/adrl/learning/estimator.py": {
      "bytes": 11107,
      "mode": 420,
      "sha256": "40a8c0fb0453cf47c52e96b32d5eaadb3000d2a38e1300e3e9224211360b332c"
    },
    "src/adrl/learning/explore.py": {
      "bytes": 9761,
      "mode": 420,
      "sha256": "1c57f911fe66cf38f7e95744971395388a9791d8a527870eb16a352b2ca01189"
    },
    "src/adrl/learning/improvement.py": {
      "bytes": 12577,
      "mode": 420,
      "sha256": "21cd27a5d31a66797574e2f02ea3fc4e4ea48b6150343ef301a9289ae8b80c81"
    },
    "src/adrl/learning/pairs.py": {
      "bytes": 10477,
      "mode": 420,
      "sha256": "73283b6c0af83c409d37d4fecce3d31437de7a65aca66ea1e0ff53efeb276160"
    },
    "src/adrl/learning/readiness.py": {
      "bytes": 6395,
      "mode": 420,
      "sha256": "947d22d853c3bed68521ee2d005947696bce404034e5819dfc0f697533e55aea"
    },
    "src/adrl/learning/tiers.py": {
      "bytes": 15732,
      "mode": 420,
      "sha256": "6d0a17d8a57179e13544a75bde5144ae93343e21c966b71eebdaf0fdbbb1fca8"
    },
    "src/adrl/ledger/__init__.py": {
      "bytes": 708,
      "mode": 420,
      "sha256": "634cb0cb9f669d0a256abeb6e63a003685026f6edecce46d4e4ee77676d5761b"
    },
    "src/adrl/ledger/anchoring.py": {
      "bytes": 9218,
      "mode": 420,
      "sha256": "024913a90f513ae8583d409d03a77dbffb00a367f207b12bd5a762c97879fbed"
    },
    "src/adrl/ledger/attempts.py": {
      "bytes": 30054,
      "mode": 420,
      "sha256": "76e85c5028df2f05c0e8d3f680078e84230952f85a0534a21776842251e2b0ae"
    },
    "src/adrl/ledger/capture.py": {
      "bytes": 18652,
      "mode": 420,
      "sha256": "ef644fa690e69bb718f00534aec19aaf55d541bbf38f7249bf854da7e8bebaed"
    },
    "src/adrl/ledger/counterfactual.py": {
      "bytes": 1950,
      "mode": 420,
      "sha256": "43c9b8345e855257ea9f727205ca678c58be995dea1c8234dc15132ece501922"
    },
    "src/adrl/ledger/crypto.py": {
      "bytes": 1064,
      "mode": 420,
      "sha256": "01730ca1c51e4cfcd48beef49b744e4d0cdca4c6996b09c77fb7a219e791ebb6"
    },
    "src/adrl/ledger/egress.py": {
      "bytes": 25954,
      "mode": 420,
      "sha256": "43a05c01cb284d6c53c2b79b0be906e4f9a291788f7932cc85cc13a639a1feac"
    },
    "src/adrl/ledger/embeddings.py": {
      "bytes": 9564,
      "mode": 420,
      "sha256": "f766d1ddeec3e5742182cd4c468483769c382cf9fbbc76667c3a90a1e7f2b64c"
    },
    "src/adrl/ledger/erasure.py": {
      "bytes": 3851,
      "mode": 420,
      "sha256": "82298f397b3c752d3983f5415f09b59e59de5bc14fd246460bebf75bb03803f5"
    },
    "src/adrl/ledger/events.py": {
      "bytes": 9937,
      "mode": 420,
      "sha256": "91880f121e9e30cfe4684305135b9a99258a974cbdb87a0870eaa537db6a2cd3"
    },
    "src/adrl/ledger/facade.py": {
      "bytes": 9020,
      "mode": 420,
      "sha256": "2bb55f817fa889b92fb87ee67932a0a07a1821bdc73d7c9e0dabb6e40d89e892"
    },
    "src/adrl/ledger/improvement.py": {
      "bytes": 3780,
      "mode": 420,
      "sha256": "21e2dc8f8d26af7177a5a5c0cd64102b1154a2368784dd71432861a9aafbdedf"
    },
    "src/adrl/ledger/keystore.py": {
      "bytes": 10727,
      "mode": 420,
      "sha256": "7317110097fceaef34a69fb3fbeff3d0e27db17e0508e88b8063abf812c44d12"
    },
    "src/adrl/ledger/labels.py": {
      "bytes": 7515,
      "mode": 420,
      "sha256": "be1f1b089e477fb0a3ab6076b754e858f24950d27dcad5c4cba2b86dc6ac361f"
    },
    "src/adrl/ledger/migrations/0001_initial.sql": {
      "bytes": 3161,
      "mode": 420,
      "sha256": "5c0e582136caf827307f3f8a08098f9eb5c05be599a469a1b7fb0472a776e835"
    },
    "src/adrl/ledger/migrations/0002_evidence.sql": {
      "bytes": 889,
      "mode": 420,
      "sha256": "177647eb19f86c6d286720bb47891d8d73178435e4e44e7daf8326a0e2a99bcb"
    },
    "src/adrl/ledger/migrations/0003_product.sql": {
      "bytes": 1365,
      "mode": 420,
      "sha256": "0689c91906d06152af09937eb2758f7891c14a7456542632d19b40567b0f30b6"
    },
    "src/adrl/ledger/migrations/0004_integration_mode.sql": {
      "bytes": 292,
      "mode": 420,
      "sha256": "f34bc9fab14caad2ed8b85e716a0fd984a1061649cc5f015f2c2ff9236d93bf9"
    },
    "src/adrl/ledger/migrations/0005_session_verification.sql": {
      "bytes": 533,
      "mode": 420,
      "sha256": "854c5ab5137417effded2b1d12317eb3b34ef89fceb9ab044486dcd242a210ac"
    },
    "src/adrl/ledger/migrations/0006_improvement.sql": {
      "bytes": 484,
      "mode": 420,
      "sha256": "b194c62ee650354af4b5f7cbf9ab4d17d226572f9b514dba5fe679bdc9f24f5f"
    },
    "src/adrl/ledger/migrations/0007_captures.sql": {
      "bytes": 529,
      "mode": 420,
      "sha256": "e45cd62b7e45fe68227440490b78b7e42a2ebc731d1ee88aba31c40909c8a719"
    },
    "src/adrl/ledger/migrations/0008_attempts.sql": {
      "bytes": 778,
      "mode": 420,
      "sha256": "d78df82450565671d96d2c9648c493f490ab81ec0fde8061b269c66c49a98d12"
    },
    "src/adrl/ledger/migrations/0009_attempt_capacity.sql": {
      "bytes": 736,
      "mode": 420,
      "sha256": "0e534507e02da25c7f0e6b9d5c1e7408e8c8b17831166bca534895baf4a1e8f6"
    },
    "src/adrl/ledger/migrations/0010_execution_fences.sql": {
      "bytes": 564,
      "mode": 420,
      "sha256": "d352e2cd587a330c0403e76ee6656e9838a21c7cbc3253b9b44938b759e48555"
    },
    "src/adrl/ledger/migrations/0011_resource_ownership.sql": {
      "bytes": 684,
      "mode": 420,
      "sha256": "3f1828853c85aa555b1e588d458ec6180ed2c9377faa1057a62e6ef307673ecf"
    },
    "src/adrl/ledger/migrations/0012_launch_history.sql": {
      "bytes": 540,
      "mode": 420,
      "sha256": "2b4a4146f2e1dd5731cd75ac8990864f11f339a4f3b129e846585ae54122bb5d"
    },
    "src/adrl/ledger/migrations/__init__.py": {
      "bytes": 969,
      "mode": 420,
      "sha256": "f01702f0272a85680c14f0773562a7efd919f830b1cbea48b773f1f3ff5135ff"
    },
    "src/adrl/ledger/outcomes.py": {
      "bytes": 16010,
      "mode": 420,
      "sha256": "87ed8af4d5d244af77eadb36d8edc44fb3e62f86c1dbb02f921bcde772cba409"
    },
    "src/adrl/ledger/projections.py": {
      "bytes": 10289,
      "mode": 420,
      "sha256": "1d21a9a3921eb0d1fd09e95c2e5db2ee6f24649afc8cc0b8221f6d975c8048ee"
    },
    "src/adrl/ledger/readiness.py": {
      "bytes": 4588,
      "mode": 420,
      "sha256": "43677204359845245b952c5a26c567db7b61994ea95fbcedf2b187bff56bd204"
    },
    "src/adrl/ledger/replay.py": {
      "bytes": 2185,
      "mode": 420,
      "sha256": "a317c2a83252cdaeff25721bf9b3ba3006deac2a5bc217f9b931a9d7c5cf3676"
    },
    "src/adrl/ledger/retention.py": {
      "bytes": 2911,
      "mode": 420,
      "sha256": "a5530bf46282ae0f93b7b473e1518b66c44289f71e759aa67fb7d045b90a42d1"
    },
    "src/adrl/ledger/session_verification.py": {
      "bytes": 14522,
      "mode": 420,
      "sha256": "e6f5efbc51107337ea75c4a363c4c520d04da76ae021ddf45dca06c76e96bb9e"
    },
    "src/adrl/ledger/shadow_retrieval.py": {
      "bytes": 3978,
      "mode": 420,
      "sha256": "03961c21ddafa3d69426280db1fc7122568b6bc0433e1dd2ea45fb8876edae79"
    },
    "src/adrl/ledger/state.py": {
      "bytes": 5981,
      "mode": 420,
      "sha256": "3b797bd74e4c2fa94f456fcbfced6f95388810ce628bef88873c4a6423765ef0"
    },
    "src/adrl/ledger/store.py": {
      "bytes": 10978,
      "mode": 420,
      "sha256": "4bef263447219212d3e8b3262d0666abdc20ed9832d15777595eae1621ea35c2"
    },
    "src/adrl/ledger/upcast.py": {
      "bytes": 3852,
      "mode": 420,
      "sha256": "6af7243a7c4ccd55fda7014617644a3a6d735ba1c4a6f8bfc67bca8522868732"
    },
    "src/adrl/ledger/verification.py": {
      "bytes": 23436,
      "mode": 420,
      "sha256": "c2846a6a8cdf0b1c1c479e71cda691dc8a70d11db9d708056ec87c7ddac313a3"
    },
    "src/adrl/proxy/__init__.py": {
      "bytes": 177,
      "mode": 420,
      "sha256": "49436b67b95b630642b80f88850ebfc37c1dad4c52f1b51834b766e89f112a1b"
    },
    "src/adrl/proxy/asgi.py": {
      "bytes": 6662,
      "mode": 420,
      "sha256": "491c8a431380483eff035d136749a9c13c7738ad613f75ee879fdd929ee23640"
    },
    "src/adrl/proxy/errors.py": {
      "bytes": 940,
      "mode": 420,
      "sha256": "6208b8f4b9f2442a33ea8022419fd22903dab91079e4de256edf755d6bdf4a36"
    },
    "src/adrl/proxy/fallback.py": {
      "bytes": 6479,
      "mode": 420,
      "sha256": "04919e7e581ca96a82c9ee99d7ad5527ae36f17853b39ca476dd0c8a97307e35"
    },
    "src/adrl/proxy/observe_only.py": {
      "bytes": 7214,
      "mode": 420,
      "sha256": "bf7adbbe6807ec5db6165a041597e4a8df3324061324632b6c1f87072d3138e3"
    },
    "src/adrl/proxy/pipeline.py": {
      "bytes": 48117,
      "mode": 420,
      "sha256": "68a170c352ad7793113626002be84608f9c656740280156405682040407b152f"
    },
    "src/adrl/proxy/stages.py": {
      "bytes": 3091,
      "mode": 420,
      "sha256": "53513de35680401ec134a0d360b84b894fe6fdbd6be2c3c6c42356b836a4174a"
    },
    "src/adrl/proxy/upstream.py": {
      "bytes": 4592,
      "mode": 420,
      "sha256": "cbfc2436d9f3e87813a392e3839b4388d34b8d4c17194cce3c5f0bba84ec98d2"
    },
    "src/adrl/routing/__init__.py": {
      "bytes": 215,
      "mode": 420,
      "sha256": "ec71c7c97beb192638a74734a09c8f3d6501adad3dfd30261411e7c6e4ed859b"
    },
    "src/adrl/routing/advisor.py": {
      "bytes": 7687,
      "mode": 420,
      "sha256": "cbd31e1919d24546641003bd2b4d232d56986f94c189f0b61729816031443450"
    },
    "src/adrl/routing/cascade_feasibility.py": {
      "bytes": 2764,
      "mode": 420,
      "sha256": "ee8359e5655ee51319727ed4611be04ba5c76f81b02982b67a823b99ec494f97"
    },
    "src/adrl/routing/cost.py": {
      "bytes": 7081,
      "mode": 420,
      "sha256": "428e3894b10fd2dd214294da49aa78f2251c987715b3a2d59c4833e4e1e074d0"
    },
    "src/adrl/routing/features.py": {
      "bytes": 12371,
      "mode": 420,
      "sha256": "7de44ffd52b490d33b2f66f632d964c6df57f8a7ea31d34783db973db926b205"
    },
    "src/adrl/routing/policy.py": {
      "bytes": 6822,
      "mode": 420,
      "sha256": "a5d9bd9a9da8b48ee76cfe13cfd7f3a1cccb5ceb542d3178f5f3f294a48c4b60"
    },
    "src/adrl/routing/registry.py": {
      "bytes": 4732,
      "mode": 420,
      "sha256": "18ad3fc453d67c11fe8cd783ee2cfb596b03d12f4ece21cf7b672813e0365dae"
    },
    "src/adrl/routing/router.py": {
      "bytes": 10268,
      "mode": 420,
      "sha256": "36666f3e9a6944a9974d35b906e0bf231014f96798ba65dbb8670dfa19f24045"
    },
    "src/adrl/routing/rule_health.py": {
      "bytes": 3590,
      "mode": 420,
      "sha256": "c9843b350c36731bf5778b900b107d231181be794a88ec9b12cb91a49d2daa8b"
    },
    "src/adrl/routing/side_effects.py": {
      "bytes": 16243,
      "mode": 420,
      "sha256": "d617fa3d9ba2d8b93c4cf8d32571fe795ec979f40e21bce057b45b275d74699e"
    },
    "src/adrl/telemetry/__init__.py": {
      "bytes": 607,
      "mode": 420,
      "sha256": "cbf0dc80c108a2a5c0714c67a2588efe136d3969f0cdf31f70de3abb7ba7308a"
    },
    "src/adrl/telemetry/logging.py": {
      "bytes": 1538,
      "mode": 420,
      "sha256": "4fb1d7fb6d9d6f14439c5344f7021ed95edfa0ec5a865a136e26b6f1fd074e07"
    },
    "src/adrl/telemetry/metrics.py": {
      "bytes": 3025,
      "mode": 420,
      "sha256": "db03f5ff99a8cc0b476933315ea4ef00366bb432f47b7bbbf2f89a4dd38a1b34"
    },
    "src/adrl/telemetry/semconv.py": {
      "bytes": 926,
      "mode": 420,
      "sha256": "f03aab966149fe22a9fcda33a0097bbab9b144d4609014e4acf79bb14fec0dde"
    },
    "src/adrl/wire/__init__.py": {
      "bytes": 855,
      "mode": 420,
      "sha256": "530b1c1bba4f681b33433510837137e5d6d0e4653cb3544a4a2548d0de4da695"
    },
    "src/adrl/wire/adapters.py": {
      "bytes": 2187,
      "mode": 420,
      "sha256": "0f8abd8962d3a2ffeb8be2f7a9d060caa47b908e5a8fc2e177eb691144489600"
    },
    "src/adrl/wire/classify.py": {
      "bytes": 8548,
      "mode": 420,
      "sha256": "7abbce3cc0ba508bddea588bb81dcc55c6a7b88e3cbd2506e118dbc503c90b90"
    },
    "src/adrl/wire/identity.py": {
      "bytes": 7789,
      "mode": 420,
      "sha256": "61a3e71e6fb97617e82f3095750041607edbaa9eff43bf4f4f7c97f9a8ac2e5b"
    },
    "src/adrl/wire/observe.py": {
      "bytes": 11180,
      "mode": 420,
      "sha256": "a8a9e237b1cf6397597dfda4762f0e65507d7b2fbe09e8bdfa3970c35d928cca"
    },
    "src/adrl/wire/parse.py": {
      "bytes": 8112,
      "mode": 420,
      "sha256": "f4c7c61438e50c8b91ab08ff927dbb17d5887802949ff3ac27925c0d9fcef28e"
    },
    "src/adrl/wire/profiles/__init__.py": {
      "bytes": 54,
      "mode": 420,
      "sha256": "d4e7de031920d9e6d223384e9a097aa4c2ed50cd6259c70a1e6e60957a37fab2"
    },
    "src/adrl/wire/profiles/base.py": {
      "bytes": 3867,
      "mode": 420,
      "sha256": "928dc02f1909b939f71adcf70244d507b3bb1c122799339f50e7ef40f2077ad8"
    },
    "src/adrl/wire/profiles/messages.py": {
      "bytes": 5875,
      "mode": 420,
      "sha256": "be738637186caf85ef47745679e9d94dd34cff05cb51ed3005fbc7e0fa70524f"
    },
    "src/adrl/wire/profiles/messages_responses.py": {
      "bytes": 2609,
      "mode": 420,
      "sha256": "8a8d1d188144c834d4ec82e90dffc7e2842c893771b9da278ea032e2be239ee3"
    },
    "src/adrl/wire/rewrite.py": {
      "bytes": 2924,
      "mode": 420,
      "sha256": "eb49c51565003b70432666f557b33ce7c89064d630fdd448b15254198d8fe468"
    },
    "tests/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/adversarial/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/adversarial/conftest.py": {
      "bytes": 256,
      "mode": 420,
      "sha256": "096d1351989fa02d36f10c725853624ca8f1df24f83de5da9ee26bcbf07916ee"
    },
    "tests/adversarial/test_saf_suite.py": {
      "bytes": 4535,
      "mode": 420,
      "sha256": "d7a1d978c4dfecf3b54816a63d824f54eb2bb1c7531982cd28501478b9984cda"
    },
    "tests/adversarial/test_tru_suite.py": {
      "bytes": 4881,
      "mode": 420,
      "sha256": "a55949985c2269dcc29902af7dc95b1402b0e39731bb11c075f7466341d5b2e0"
    },
    "tests/conftest.py": {
      "bytes": 8701,
      "mode": 420,
      "sha256": "0998e7620ac04588746ca1b2f22ee5a2626e869cd8ce507708758430df81b9b9"
    },
    "tests/fixtures/launch_owner.py": {
      "bytes": 1397,
      "mode": 420,
      "sha256": "00d61d8eb0ff5f00b9b783e9e044f436f148461c8a8bb5ef1851daa9bb34da48"
    },
    "tests/fixtures/profiles/identity-v1.json": {
      "bytes": 1706,
      "mode": 420,
      "sha256": "39314dc7c49f415a368afe544570b8099d4215f223a5b3242a33a8678fae2aec"
    },
    "tests/fixtures/seccomp-v27.3.1.json": {
      "bytes": 12828,
      "mode": 420,
      "sha256": "9c1025c88ccaa517b648da571961838744ea2137f176bfe6a48b21294cae9c76"
    },
    "tests/fixtures/wire/compaction.json": {
      "bytes": 1259,
      "mode": 420,
      "sha256": "e13eee45e9d5b2cdf845b50fd1f2431878f01b64ba732dc00dabc41a91d01bf9"
    },
    "tests/fixtures/wire/continuation.json": {
      "bytes": 2820,
      "mode": 420,
      "sha256": "9208f708a25d64bff9020d0d792154fcbbba41a6c34c7a2131933ab036ea9c1d"
    },
    "tests/fixtures/wire/count_tokens.json": {
      "bytes": 1709,
      "mode": 420,
      "sha256": "0413c1d9033d9f2eecddf50b57b8d93e35d7beb02aa9152e7759b584938b7b4f"
    },
    "tests/fixtures/wire/escalation_parallel_tools.json": {
      "bytes": 1580,
      "mode": 420,
      "sha256": "2fa413954c24c338474854aed7d448876ed15f822ea99fc7c8416a55637511d1"
    },
    "tests/fixtures/wire/fork_subagent.json": {
      "bytes": 3250,
      "mode": 420,
      "sha256": "651b2b01ac64afcff23b6bd933fa86cd5d1d8e4e82590668e42968167bbd98bc"
    },
    "tests/fixtures/wire/metadata_only_user_turn.json": {
      "bytes": 1991,
      "mode": 420,
      "sha256": "6d2d342bbaf769aa7a4d9135f822cf7dedb4ec77e35ff0b4d8333b563bac41f2"
    },
    "tests/fixtures/wire/nested_subagent.json": {
      "bytes": 2150,
      "mode": 420,
      "sha256": "0e0e881ff882e443fbe3b414e7836897d70ab925603e74bd8184d0e63ccd5b2c"
    },
    "tests/fixtures/wire/parallel_tools_full.json": {
      "bytes": 3105,
      "mode": 420,
      "sha256": "505559666a116132c2cc492b7158c7b968f0da783646fa87350f7ba13481928f"
    },
    "tests/fixtures/wire/parallel_tools_partial.json": {
      "bytes": 2951,
      "mode": 420,
      "sha256": "d56eaa6e53ea1eacf36329c0892a8263bbfcb2c86d1ddd8e84a4d9e974d2e737"
    },
    "tests/fixtures/wire/pre_warm.json": {
      "bytes": 1896,
      "mode": 420,
      "sha256": "55bcf0673ed5aa3b3c7948d2d8b8fc1da4106c037c493d3c1da5fbf3164c5f55"
    },
    "tests/fixtures/wire/title.json": {
      "bytes": 928,
      "mode": 420,
      "sha256": "023640c7088508eeda108c1a774c012d1beccb5e0d728e1a1c05bed7cbc6224d"
    },
    "tests/fixtures/wire/topic_detect.json": {
      "bytes": 972,
      "mode": 420,
      "sha256": "3245b7021cd98b8b98c86a23713e8d7aea02cbbda0ad366fb4d3b4538dc42ae9"
    },
    "tests/fixtures/wire/user_turn.json": {
      "bytes": 2025,
      "mode": 420,
      "sha256": "0cab3bfbf06c45aab1e1be8f019159aaced9aed31e56f10be68c8292ef7c2816"
    },
    "tests/integration/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/cascade/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/cascade/conftest.py": {
      "bytes": 465,
      "mode": 420,
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/integration/cascade/test_controller.py": {
      "bytes": 12943,
      "mode": 420,
      "sha256": "5d86e61671de29a2082f223cdd8f641097842fd7ba5476ca286f2f6d66175759"
    },
    "tests/integration/cascade/test_review_defects.py": {
      "bytes": 6454,
      "mode": 420,
      "sha256": "857c1c1aeba37e29c5694d4414f06408409b2a92c2758c6ec227d46d94bc0b70"
    },
    "tests/integration/e2e/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/e2e/conftest.py": {
      "bytes": 7966,
      "mode": 420,
      "sha256": "90ab6359a3907e1d13920a3391133d385b0f6fc0d70e8cb62e8b7b29c595ca9c"
    },
    "tests/integration/e2e/test_composed_system.py": {
      "bytes": 10368,
      "mode": 420,
      "sha256": "28fa67ba5b497c4d9e8d89c78c5895e21b465e5bd8efcadf037266c2c76f55e6"
    },
    "tests/integration/e2e/test_outcome_contract.py": {
      "bytes": 9500,
      "mode": 420,
      "sha256": "b19cd9e234079e3076b966113b89dbb41f074922342ed0d0e639155baa48cc1b"
    },
    "tests/integration/e2e/test_pin_failure.py": {
      "bytes": 1793,
      "mode": 420,
      "sha256": "c974d6d2d3e09e24bd5547c3dc9334125e3b2273ff6017b2fb80ec58969d509a"
    },
    "tests/integration/e2e/test_product_services.py": {
      "bytes": 29411,
      "mode": 420,
      "sha256": "329a6b4071da40f87675375f530a3993a2cfb69b953468d611fc5692fc7dc963"
    },
    "tests/integration/e2e/test_review_defects.py": {
      "bytes": 5973,
      "mode": 420,
      "sha256": "f17cf912128501843517d4e134ae2c6664bb5be490197d8fe4c5200bc876ebfd"
    },
    "tests/integration/e2e/test_tru.py": {
      "bytes": 5645,
      "mode": 420,
      "sha256": "42652efc6d9484aba196e25d37a483226e1321e18855c6622ffa89a97ac4d081"
    },
    "tests/integration/e2e/test_trust_wiring.py": {
      "bytes": 3771,
      "mode": 420,
      "sha256": "43ae74ee8e66dde0b90bfbaee0a9bfbf8f082d036a2211a6c0afcfe0e9a950aa"
    },
    "tests/integration/gates/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/gates/conftest.py": {
      "bytes": 134,
      "mode": 420,
      "sha256": "925ed24d508f2058d26f5ce6f8de4d629500919b1abf96dbc4810fece3574b74"
    },
    "tests/integration/gates/test_pin_durability.py": {
      "bytes": 2549,
      "mode": 420,
      "sha256": "7007829914677d64e694b934c6868026e3cfaf62359ad6dcc746129c0863b5c4"
    },
    "tests/integration/ledger/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/proxy/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/proxy/conftest.py": {
      "bytes": 11824,
      "mode": 420,
      "sha256": "fe8bf67e23465d0597654bdfa93b50949fa6c7730eacc303870916b2f33192fd"
    },
    "tests/integration/proxy/test_fault_matrix.py": {
      "bytes": 7061,
      "mode": 420,
      "sha256": "683cecea87149979ae4f5f6888c62b418c874912120543640f433724a73a14a1"
    },
    "tests/integration/proxy/test_pinned.py": {
      "bytes": 6419,
      "mode": 420,
      "sha256": "36e97c508af175b32be4bb234cf9a54d0f3539415cecad24689da9092adb08f4"
    },
    "tests/integration/proxy/test_profiles.py": {
      "bytes": 1990,
      "mode": 420,
      "sha256": "46ff3d92a6ffbd8885b25e52a6e67a357276365caab866035e51bf55bfa2b48e"
    },
    "tests/integration/proxy/test_removal.py": {
      "bytes": 3352,
      "mode": 420,
      "sha256": "b488d5eb5ee8e6d5b6e6ca0baa1dd8d6d52b2be54e25a54690814e222a710473"
    },
    "tests/integration/proxy/test_routing_paths.py": {
      "bytes": 4494,
      "mode": 420,
      "sha256": "24e668347d358f36f7e080cfbc73a4cfaccdc1c84f46c10fa13a58bae4afc655"
    },
    "tests/integration/test_cli.py": {
      "bytes": 1088,
      "mode": 420,
      "sha256": "46a4da25d892d293447514428c8efb2c7029c42c8c643bbf8b8005956d5a49dd"
    },
    "tests/integration/test_cli_verify_snapshot.py": {
      "bytes": 3196,
      "mode": 420,
      "sha256": "56a6ef0e166aa8cee3254945d9d4df74ef5120ed0ac11925f7bb181c2cf74b14"
    },
    "tests/integration/test_launch_engine.py": {
      "bytes": 4846,
      "mode": 420,
      "sha256": "32f2f683e5dddb63e047c86f2cb1aadfac51046701765915b4bb176ffc26cc84"
    },
    "tests/integration/test_resource_engine.py": {
      "bytes": 7381,
      "mode": 420,
      "sha256": "a66c6e187c1012f6e39297abdc88af1c74de0d64cee3097940770cc1be18104f"
    },
    "tests/unit/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/cascade/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/cascade/conftest.py": {
      "bytes": 465,
      "mode": 420,
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/unit/cascade/test_boundary_tripwires.py": {
      "bytes": 5500,
      "mode": 420,
      "sha256": "1e1ea158cc979a2b435a2976075d231f6e7574e3b20130aca301d870c020f53f"
    },
    "tests/unit/cascade/test_handoff_sticky.py": {
      "bytes": 7453,
      "mode": 420,
      "sha256": "e9d6624337d29e7c11fd0ff24d79a1617210df1a5885f06bc5b270838138407f"
    },
    "tests/unit/gates/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/gates/conftest.py": {
      "bytes": 8009,
      "mode": 420,
      "sha256": "f39063ec22ae5c3762b8666971bf32f5c3fd47ffe958b6b2c42b4642d17a9108"
    },
    "tests/unit/gates/test_block.py": {
      "bytes": 3025,
      "mode": 420,
      "sha256": "05d72a875190cf71fdc694b209501dc0a2905a70a29ff949f3ca75d183a749c6"
    },
    "tests/unit/gates/test_content.py": {
      "bytes": 1909,
      "mode": 420,
      "sha256": "f0cf9ad15796159748e3b67450eb02839d220db129119daaace39b85700dbc23"
    },
    "tests/unit/gates/test_coverage.py": {
      "bytes": 1364,
      "mode": 420,
      "sha256": "ffbcf9882584c6acec0d7afd83a2b28bec32e059bff9848ba31e9e0203bde2c1"
    },
    "tests/unit/gates/test_egress_writer.py": {
      "bytes": 1958,
      "mode": 420,
      "sha256": "f6e83d902381ebdd6d062181bad53e7db6be6a3d3de13d13d3f5ec460c209f0f"
    },
    "tests/unit/gates/test_feasibility.py": {
      "bytes": 2515,
      "mode": 420,
      "sha256": "5caa1fb734c321de0f8b096aba41a41cfcb340ac12314508fbba8bb8fca7e92b"
    },
    "tests/unit/gates/test_observe_mode.py": {
      "bytes": 2856,
      "mode": 420,
      "sha256": "b31f9ccd6f8c5f84ca8d3871045c412e3ca755335eb5e5ce286323c8272c7ea5"
    },
    "tests/unit/gates/test_pin.py": {
      "bytes": 3440,
      "mode": 420,
      "sha256": "2edfc3a5ba67f7859e25192dc467cb905a87918118631f657c4f78a3585696e7"
    },
    "tests/unit/gates/test_pin_write_failure.py": {
      "bytes": 7973,
      "mode": 420,
      "sha256": "ce3e9c056dd09485b0590bc9b7b69bd28c1df2a13df462f59d7b0b6dacf84121"
    },
    "tests/unit/gates/test_pipeline.py": {
      "bytes": 8158,
      "mode": 420,
      "sha256": "d3cd972b9ca4cef20b93502bfdd7f4b3ea2b451220400963d094641768c8d1af"
    },
    "tests/unit/gates/test_repo_class.py": {
      "bytes": 6087,
      "mode": 420,
      "sha256": "b39eeb5693390c34ae0b369c3059a5d0b010d923e7ec759902a135fb2744092f"
    },
    "tests/unit/gates/test_sandbox.py": {
      "bytes": 3647,
      "mode": 420,
      "sha256": "5aac4a4702a151be6b738ac07aa41b9eec9acad03b5e22fee80c7ef71366877b"
    },
    "tests/unit/gates/test_secrets.py": {
      "bytes": 2976,
      "mode": 420,
      "sha256": "229b8dfa52ac3afded7c8f4727437d1049768c04d0f1f4fe9dcbc354219ad628"
    },
    "tests/unit/gates/test_workload.py": {
      "bytes": 4911,
      "mode": 420,
      "sha256": "47caab4f52becb3f5875cd982cb3797490ed930f9e4075d1d131a84e8002c554"
    },
    "tests/unit/learning/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/learning/conftest.py": {
      "bytes": 3944,
      "mode": 420,
      "sha256": "d9b57452143653991a05cf299a0d7bf073d79ae0a5647ce5cb99e993035e937e"
    },
    "tests/unit/learning/test_abstention.py": {
      "bytes": 3255,
      "mode": 420,
      "sha256": "3c14a5d6fc3d3410ed6fd742e9a4bb69aa6cc5e947a7586a849e085a73998d78"
    },
    "tests/unit/learning/test_artifacts.py": {
      "bytes": 4747,
      "mode": 420,
      "sha256": "f1f12afada374f40dc97e1ec0d1cc980b5a475d9cfc356cb30c500fc04a68d64"
    },
    "tests/unit/learning/test_dataset.py": {
      "bytes": 4293,
      "mode": 420,
      "sha256": "0875f9736aa544e5d89c82dc423ad8234df1894661e02a1a13b482f3b78ef936"
    },
    "tests/unit/learning/test_estimator.py": {
      "bytes": 2626,
      "mode": 420,
      "sha256": "67e5ca8963d4180cf2073fd3ee7e25e19f395805d99335e9b72727fad0b0d5aa"
    },
    "tests/unit/learning/test_explore.py": {
      "bytes": 3935,
      "mode": 420,
      "sha256": "b6909e90235924c026308e1bdfe26ea4c09ed106fa82cae3d1e3b63fa50e15c2"
    },
    "tests/unit/learning/test_improvement.py": {
      "bytes": 11949,
      "mode": 420,
      "sha256": "dd35b6f67bce6c75f26cfe476cd4464fb12f05e6a069999e36268a00452b1043"
    },
    "tests/unit/learning/test_pairs.py": {
      "bytes": 3200,
      "mode": 420,
      "sha256": "7c1ec762db521691164d94af5e8e879ec385a2ad947d4a60c6564cdc96500fe2"
    },
    "tests/unit/learning/test_readiness.py": {
      "bytes": 1061,
      "mode": 420,
      "sha256": "387ee35f6f6a392e5bb5a90ceb83a6a02f5be7c0dc71fb3587b6240b539e3757"
    },
    "tests/unit/learning/test_tiers.py": {
      "bytes": 4387,
      "mode": 420,
      "sha256": "696facc4b378c2c41a5be805f001196296d327d405ec4dac04a1bdf6debc7597"
    },
    "tests/unit/ledger/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/ledger/conftest.py": {
      "bytes": 3911,
      "mode": 420,
      "sha256": "010a76aad8e5d6b20585639ac45bbb42af795997bdc5622f8588206a62d6bf12"
    },
    "tests/unit/ledger/test_anchoring.py": {
      "bytes": 10465,
      "mode": 420,
      "sha256": "9f7a35b6ff66453013fc9a9a9f21bbf198d11c642e2787c55e5870ac9d169f08"
    },
    "tests/unit/ledger/test_data_inventory.py": {
      "bytes": 5266,
      "mode": 420,
      "sha256": "e08fe724b6bc84252c52cd383dccf3e24f94864d37a3a0ce8cf7b48911f7b2b1"
    },
    "tests/unit/ledger/test_events_and_labels.py": {
      "bytes": 5444,
      "mode": 420,
      "sha256": "f98a02f30e5dda2e65a62c1a98dd674f314a593a469bc2de250b36019b155741"
    },
    "tests/unit/ledger/test_outcomes.py": {
      "bytes": 6281,
      "mode": 420,
      "sha256": "92887f3c22fe9eb30d1e9b3762aef47967a11ad30bc523446c8ee9a2457eaca8"
    },
    "tests/unit/ledger/test_privacy_artefacts.py": {
      "bytes": 9366,
      "mode": 420,
      "sha256": "6e5bb64c39a75e64efb492cd3d5aadf8347db223015bd8acfc57a74b56fff647"
    },
    "tests/unit/ledger/test_state_counterfactual_shadow.py": {
      "bytes": 5217,
      "mode": 420,
      "sha256": "1d95ca1664ce9d1154d11b783fc1e1316d9029b4f1bc59b41ece6e574536e23e"
    },
    "tests/unit/ledger/test_verification.py": {
      "bytes": 8662,
      "mode": 420,
      "sha256": "e0ce2701e710e312595d76655b96f3778e498cf97ffdf71bad6032f8e2b30a94"
    },
    "tests/unit/proxy/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/proxy/test_fallback.py": {
      "bytes": 2021,
      "mode": 420,
      "sha256": "fe2104131ec80366485a03abb87d57feac7870b9ad8034d65856d15c7277cdae"
    },
    "tests/unit/routing/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/routing/conftest.py": {
      "bytes": 465,
      "mode": 420,
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/unit/routing/helpers.py": {
      "bytes": 4132,
      "mode": 420,
      "sha256": "734c48d9848c452adf3099874c0e1a0c198cf9132472e42bbe51c8b71849a219"
    },
    "tests/unit/routing/test_cost_policy.py": {
      "bytes": 6070,
      "mode": 420,
      "sha256": "5719bf0fc5618cd9c1cec8cbb240862cd29e440da4a01558416283d44458538d"
    },
    "tests/unit/routing/test_gateway_config.py": {
      "bytes": 3939,
      "mode": 420,
      "sha256": "a0da57f4bea464fc3734f779c0bd4f9ff319f927527f57c8bb84444b45483cbb"
    },
    "tests/unit/routing/test_mixed_intent.py": {
      "bytes": 3926,
      "mode": 420,
      "sha256": "7f55b41a8b880fcc9bb1c2365957cdbb5bd64cb7cb23d94c4bcea068933a5fad"
    },
    "tests/unit/routing/test_registry_features.py": {
      "bytes": 5109,
      "mode": 420,
      "sha256": "735b0211b50d8bacbb721519cd391833d650ab2bd0fb565ff8cbc54262f695da"
    },
    "tests/unit/routing/test_router.py": {
      "bytes": 7175,
      "mode": 420,
      "sha256": "6125b94e23395072b1e505a94d1c3ec26a638a9eb5acce5648872e62f071fa75"
    },
    "tests/unit/routing/test_side_effects.py": {
      "bytes": 6479,
      "mode": 420,
      "sha256": "33664bee279c24694789663aeb51afb6c8a241e530209eae0bca64374e771749"
    },
    "tests/unit/test_api_contract.py": {
      "bytes": 5572,
      "mode": 420,
      "sha256": "e88641a573a983f7494df8352fc0ff82408e93288ec13fdbf68e700cbf578e74"
    },
    "tests/unit/test_attempt_capacity.py": {
      "bytes": 18369,
      "mode": 420,
      "sha256": "dd1d91f5284f09ae7ee19ecb5bb10d6286bec82c75c6421e865aa04167c74584"
    },
    "tests/unit/test_attempt_coordinator.py": {
      "bytes": 24679,
      "mode": 420,
      "sha256": "62a7eca2ee0266fb95e8e1cbda2d93be2d9559d201c673f6eb2655dbfd181dc1"
    },
    "tests/unit/test_attempts.py": {
      "bytes": 18897,
      "mode": 420,
      "sha256": "4d54d16b9dec725d6a8a2b5f33dabd2fda214fe2019ff2a86d6ecbfef55c4096"
    },
    "tests/unit/test_capture.py": {
      "bytes": 18506,
      "mode": 420,
      "sha256": "8e46474960cc3f1574b884840e0b39f439b17cc8e2e57904ad8ad5146d438a7f"
    },
    "tests/unit/test_config.py": {
      "bytes": 3394,
      "mode": 420,
      "sha256": "8cb002b9206a441ca3730270a60335ec36646903a8ccbc3ad0c8344cb48b07e4"
    },
    "tests/unit/test_core.py": {
      "bytes": 4809,
      "mode": 420,
      "sha256": "d0172ff5a0d7ed7319b9595a9bf9381d903c16fab4ec37a1ec800729d57d2416"
    },
    "tests/unit/test_create_receipt.py": {
      "bytes": 13947,
      "mode": 420,
      "sha256": "c705d8845e740dc65d452caeaf0b18c419c3aa4cb5f1b8e995620ec2bed43c8f"
    },
    "tests/unit/test_data_inventory_migration.py": {
      "bytes": 1057,
      "mode": 420,
      "sha256": "94e45373f18f8d2254a515775493fc186a78873c5f39285701f34ee92522bf5e"
    },
    "tests/unit/test_egress.py": {
      "bytes": 2739,
      "mode": 420,
      "sha256": "cf8f778fab58fcc4dd05d03ae6ed6a8cadef183c8fec4a47492cd2522e169011"
    },
    "tests/unit/test_engineering_tools.py": {
      "bytes": 4620,
      "mode": 420,
      "sha256": "0e2dc01cd0abebbb61104f744dcf71a2eae4f848289b9f7718752008e9f35436"
    },
    "tests/unit/test_isolated_execution.py": {
      "bytes": 28810,
      "mode": 420,
      "sha256": "a7ded1c4fc3c9f1c5fec11a350a076368fcf99c2544836da70793db4b5ab8a25"
    },
    "tests/unit/test_key_revocation.py": {
      "bytes": 13543,
      "mode": 420,
      "sha256": "88406cb70059b4e1b272669d3c6d558e607415f0dd581991de46d9f57bd19cf8"
    },
    "tests/unit/test_ledger_cancellation.py": {
      "bytes": 1171,
      "mode": 420,
      "sha256": "e3e9fe83e60f06cd7892398b339f7db98373cccb3e7a8695cff35ab877c6f36b"
    },
    "tests/unit/test_ledger_store.py": {
      "bytes": 5798,
      "mode": 420,
      "sha256": "a4a8f03c183e99ba90d7bc9dd7f89d734dff2a9fa43d1e79d776dac58c81e4e5"
    },
    "tests/unit/test_process_owner.py": {
      "bytes": 18017,
      "mode": 420,
      "sha256": "2abc2f9d680caaec1335badc9e0f4face39b8666daf1ea0a6bcd894101fdc4cc"
    },
    "tests/unit/test_product_client.py": {
      "bytes": 7405,
      "mode": 420,
      "sha256": "053582512b7a5ea715eb1b608ca601b1d215689f3b90ad39363bc430653f6bf9"
    },
    "tests/unit/test_product_migration.py": {
      "bytes": 3908,
      "mode": 420,
      "sha256": "df0a92e1c28c709442da4255c9632e9547b258ce47464937d2ae07af2fb39392"
    },
    "tests/unit/test_resource_owner.py": {
      "bytes": 24404,
      "mode": 420,
      "sha256": "e272079c97194e2a266bc376d0768a7d60c269a86458d38345739425cc30627f"
    },
    "tests/unit/test_routing_lab.py": {
      "bytes": 5478,
      "mode": 420,
      "sha256": "1e6252edcdbddddd93dcd5ec01479a5f04274582932586d9078a969555f269da"
    },
    "tests/unit/tru/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/tru/conftest.py": {
      "bytes": 293,
      "mode": 420,
      "sha256": "4e44fc41ac69e6a3641ba8ef2a72c78fc9cb8cdcb3f67f6f44e066d4dc6606e4"
    },
    "tests/unit/tru/test_deployments.py": {
      "bytes": 11941,
      "mode": 420,
      "sha256": "7fac080d29e32ca58865522f89d9d88d1945b0e39f1b0a4ac5cb27eda34de388"
    },
    "tests/unit/wire/__init__.py": {
      "bytes": 0,
      "mode": 420,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/wire/conftest.py": {
      "bytes": 1366,
      "mode": 420,
      "sha256": "2d022311296d129cd0d0fb8cc478c8c7d5d9e19dbeefcd9672090669092bde3e"
    },
    "tests/unit/wire/test_classify.py": {
      "bytes": 4038,
      "mode": 420,
      "sha256": "024df892a7ee443aaaacf602a7e81ac5ce984d2c34d9b84adef197641a8aab0a"
    },
    "tests/unit/wire/test_identity.py": {
      "bytes": 4582,
      "mode": 420,
      "sha256": "dc9cc6919b150a86522f29663255a9194368b579c525d778ab673e221b0de88d"
    },
    "tests/unit/wire/test_observe.py": {
      "bytes": 5165,
      "mode": 420,
      "sha256": "fd8d16f55c56a8c3155531495cee04c22866eaa822b2b63e9c931b5ee8d90fa3"
    },
    "tests/unit/wire/test_parse.py": {
      "bytes": 2348,
      "mode": 420,
      "sha256": "99badc52c64d96a0fb8c0c9699226eba184a4fd68f11f04cbffbb1cfbbbd8e50"
    },
    "tests/unit/wire/test_profiles.py": {
      "bytes": 3123,
      "mode": 420,
      "sha256": "e9afac4d2c1dff6a52d4a75e33b3f206913572e0f61dc9bcabdd151272807391"
    },
    "tests/unit/wire/test_rewrite.py": {
      "bytes": 1730,
      "mode": 420,
      "sha256": "ca91d55a0e36402bb3c0a80f0a100ee714c520df140a2586993f39e7a4aba096"
    },
    "tools/adr_module_map.py": {
      "bytes": 4684,
      "mode": 420,
      "sha256": "32b3088a50690481cf6b12b2e2e36ec2d32e9e5f606a2a4925dc13d28290b349"
    },
    "tools/check_all.py": {
      "bytes": 8357,
      "mode": 420,
      "sha256": "38b2a09a6686ee8923634f9ab25e35d80c0016ef5829e2028590ed1326919280"
    },
    "tools/check_config.py": {
      "bytes": 2299,
      "mode": 420,
      "sha256": "c4483f2c6998f75dd5c4a59d8a8fd7dc50ce509981d191046fb9685e51bc87bb"
    },
    "tools/check_data_inventory.py": {
      "bytes": 6258,
      "mode": 420,
      "sha256": "98d73890d3b4bcab0904cc4236e4e0bc7894f07f9fb164e3eda987681e705ee7"
    },
    "tools/check_learning_contract.py": {
      "bytes": 2587,
      "mode": 420,
      "sha256": "ae72d6162c1834ff8273b55de89d994628b15806451a4921adfac5db9045c724"
    },
    "tools/check_ledger_discipline.py": {
      "bytes": 2330,
      "mode": 420,
      "sha256": "751b6b350f3aaf5ffbfe6ebbd007e1ca752b9a91b737ce0e97f0176fa924b2dc"
    },
    "tools/export_api_contract.py": {
      "bytes": 880,
      "mode": 420,
      "sha256": "f3a2a54e7b82c145d5c1aff0059d408c75dd52543ff9b0d7832de7bfef476020"
    },
    "tools/gen_dev_keys.py": {
      "bytes": 2570,
      "mode": 420,
      "sha256": "10c267560a3396c27f4f9df920fc40dd41b0a08a0d4423ec876c940d22859423"
    },
    "tools/gen_litellm_config.py": {
      "bytes": 8609,
      "mode": 420,
      "sha256": "64be40a877345d6da762eb061bcb13d06013ba8bbdf045d6eece5532a58e3139"
    },
    "tools/run_routing_lab.py": {
      "bytes": 21189,
      "mode": 420,
      "sha256": "6dace633d24fa4d185c418c9a070c14dbce53361057d9a78a00dc93c33946ff7"
    },
    "uv.lock": {
      "bytes": 158986,
      "mode": 420,
      "sha256": "8da7c7f9497ecdc071768eadf85535232c1d92f9eb74ff6244b74d6b4fe61cd0"
    }
  },
  "source_root": "/Users/arunmenon/projects/adrl-core",
  "source_scope": {
    "directories": [
      "src",
      "tests",
      "tools",
      "config",
      "docs",
      "api",
      "artifacts"
    ],
    "root_files": [
      "pyproject.toml",
      "uv.lock",
      "README.md",
      "AGENTS.md",
      "CLAUDE.md",
      ".gitignore"
    ]
  },
  "started_at": "2026-09-08T18:46:54.093185+00:00",
  "status": "passed"
}

FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/checks-2/tests.log
........................................................................ [  7%]
........................................................................ [ 15%]
....................................ssssssss............................ [ 23%]
........................................................................ [ 30%]
........................................................................ [ 38%]
........................................................................ [ 46%]
........................................................................ [ 54%]
........................................................................ [ 61%]
........................................................................ [ 69%]
........................................................................ [ 77%]
........................................................................ [ 85%]
........................................................................ [ 92%]
..................................................................       [100%]
922 passed, 8 skipped in 59.03s

FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/recheck-manifest.json
{
  "source": {
    ".gitignore": {
      "sha256": "5a46e538a34a4bc94faa64f0af2a0918926e4213251a60e851eaf41922db02b3"
    },
    "AGENTS.md": {
      "sha256": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490"
    },
    "CLAUDE.md": {
      "sha256": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490"
    },
    "README.md": {
      "sha256": "dda387731ad435a2937414c8d35d3f2b51cb08841291013620571c731a554c29"
    },
    "api/adrl-api-v1-preview.json": {
      "sha256": "5a3f2c5401acd73d3a30a89fb24c94660d9a2b7c9f625b4a7c6acef987d03757"
    },
    "artifacts/lab/routing-suite-v1.json": {
      "sha256": "dfe4125445ace13eb6fbe064b0ed52576df5a71ddaeebe2568cc93fb047dc7a9"
    },
    "config/detectors.yaml": {
      "sha256": "d7e504d17341680bcfbf8bc9f76c435aa1bfc45bf53efbf208305604364d2f55"
    },
    "config/endpoint-inventory-v1.json": {
      "sha256": "67d18715549c041215deca75f0002bf486ce946b55a593a6e7d815c3e291212e"
    },
    "config/endpoint-inventory-v1.sig": {
      "sha256": "e8a78202b9ff2985ec0fe9cc7287c01c434a27466a2445ac8a35fe56bc1aa762"
    },
    "config/keys/dev/README.md": {
      "sha256": "1f2001f55f04ae0c577e723a7d70205cab0c194d99ad337f5c72c63265ee918a"
    },
    "config/keys/dev/checkpoint-signing.pub": {
      "sha256": "54c0986810789840eaede4560aa9cfbab945ed5a494fd3b83a071e82460adb2c"
    },
    "config/keys/dev/manifest-signing.pub": {
      "sha256": "aa93b81e39a6986964f8f574eb71c9a3510f07881a553eef24b199e536292655"
    },
    "config/learning-contract-v1.json": {
      "sha256": "8cfdf6a5f27f3f80839d6874831859dc0b6d71ed31440a9f33e385f0ee5ec58c"
    },
    "config/policy.yaml": {
      "sha256": "fd7522fda0c1d1c9fb1d096e603b8b3df2d981894658012e4ae2fa08439dc9bc"
    },
    "config/prices.yaml": {
      "sha256": "07fd0c8da1cce030d210f82aabfb785b81d51b3b7e5dddedb848dd2584744dd5"
    },
    "config/provider-pairs.yaml": {
      "sha256": "032a460e3e2eae0b6715a82c1a0beb60d590b7f78bf0a485245bbb6e3a3d5175"
    },
    "config/repo-classification-v1.json": {
      "sha256": "47d7790c3eb71be692b74332a2e01de3b19011b10609722fdaf413279cf97b42"
    },
    "config/repo-classification-v1.sig": {
      "sha256": "3487b15e06f60da66bfac3ed6dc4aa70e7091779b0c10a7f46d05380bdb70d5b"
    },
    "config/rungs.yaml": {
      "sha256": "39c0b9521d9e8ccbb0b4750bed1fc90a95be9f4427d4d0cb94d7f8d56c79935e"
    },
    "config/tripwires.yaml": {
      "sha256": "201d15de3d6115f46c0ac7fe5eeda91011701f63e781e88b6f8b269238dea4db"
    },
    "config/trusted-tool-servers.yaml": {
      "sha256": "b750cb935bdb7547a2b1ded6278df1cf14e8ef59f26a9ec95905bc0edd3dbd7a"
    },
    "config/utility-fingerprints.yaml": {
      "sha256": "ef9d86f19f39342f3359e7e1fc7551a7ea0a56756ff77e0f8f010905f383411a"
    },
    "docs/adr-module-map.md": {
      "sha256": "1ae7ad9678422e94a9903581d99e12d51888a8bbdf5feb0ea1e1a2e4d0af39e4"
    },
    "docs/attempt-coordination.md": {
      "sha256": "0d129f7afdec81d426656a994b1fdf988eb98d43438d65fa93fbb3fa0d221490"
    },
    "docs/attempt-lifecycle.md": {
      "sha256": "bbc398599c579392deb4020de3f98c65e71445418763755f5ea0b2a84cd2cd28"
    },
    "docs/data-inventory.md": {
      "sha256": "867f8510b6103079ef1e01b67a5307012087b0ff86800d4e7cfec6111d08eea7"
    },
    "docs/egress-anchoring.md": {
      "sha256": "d79a9f636a2b091b943cbd9caaf7e514a102309a4aabe6eec24f15a9e48f9444"
    },
    "docs/engineering-checks.md": {
      "sha256": "f62b353c39b9ddffdcc1f137535beed0afcef15fdb5e7dd5607b9c15d3fa6144"
    },
    "docs/isolated-execution.md": {
      "sha256": "c5ae8f71c16386eb516afcd5eedb29d5f9a88d756b51472d743e5798b5d55247"
    },
    "docs/key-revocation.md": {
      "sha256": "d51f135f6586589d2698612ce5680494c6ed06f7031812005af8d2434ef174a9"
    },
    "docs/known-gaps.md": {
      "sha256": "421651ee56e55db65b0857f67cad915480f17a67994aa9eba8f477a79a2970aa"
    },
    "docs/operator-captures.md": {
      "sha256": "62f7acf78ee0be3922c538ad03276252999c213e0c77ded03a3bfc95007caecc"
    },
    "docs/outcome-contract.md": {
      "sha256": "873d412f0735ae7501515c08687fbd4fc276eca213f2b99f6bd017312d1f5815"
    },
    "docs/process-ownership.md": {
      "sha256": "f2e6810a2cfc67b4d6918367ebb17adf0c9f21401cb600dcca58cc643e8f4d8c"
    },
    "docs/product-services.md": {
      "sha256": "f20f331de15c5083c557eb9f26406957a9eee6542451ae902aa5d0f25ae30d02"
    },
    "docs/protocol-boundary.md": {
      "sha256": "b5469f938dc2e96bc059dd812c388e0f6fb5219333d7d76f96f81da8ec2ccf38"
    },
    "docs/responses-admission.md": {
      "sha256": "f4ad3cf11226661c08c0f5dbc054a6f17ef8fa49faca3be1a8fc41a2fac3aaa8"
    },
    "docs/routing-features.md": {
      "sha256": "ca328c13ebdbcbee3208b4bcbda6d7967b0c32a247f04e3f1300d42c70f6d577"
    },
    "docs/routing-lab.md": {
      "sha256": "cb4e0b14204354e061fb1fdde4bffd1bf0949498aeab1bd7ddbb7ffb47e1171d"
    },
    "docs/stopped-resource-ownership.md": {
      "sha256": "b21ccc8c1a6b44895fd82b03e80afd610b10f9cb1b9a1649c3d26fb1d0dcc7cf"
    },
    "docs/verifier-experiments.md": {
      "sha256": "1a1c04c2cc2480b4d2c3da48586f1415fe69069ef9301cf60b3a7f74cb415aad"
    },
    "pyproject.toml": {
      "sha256": "5a124bb958e981557d4a3f62b28843f348ca306e4e31876a7ebc907dd95b4001"
    },
    "src/adrl/__init__.py": {
      "sha256": "f1de990ba880b21895f4888c739207ca4c3c16b222c0933a2b26aa4a03cce8c0"
    },
    "src/adrl/api/__init__.py": {
      "sha256": "02d1a3f2332e8662f52c584a15c490ba068b58294f970536391f0ca9d2bcedef"
    },
    "src/adrl/api/auth.py": {
      "sha256": "d666e1fa36b41d16448143eed404a7ccb0fde0cf6d32e70747df89b85da1bc3d"
    },
    "src/adrl/api/client.py": {
      "sha256": "7679bff2e7f5afc32800d9bc8bffe5bc7908ddf7c634036cd08bcc9ac18cbd4e"
    },
    "src/adrl/api/contracts.py": {
      "sha256": "35036e9782944730250846999f5dcd6e690717d7751e2275463696ff4e26a461"
    },
    "src/adrl/api/http.py": {
      "sha256": "c129cbd845d04583af3f566099117ba58e7fa12cc75694cc7f60a9161e3f8bd1"
    },
    "src/adrl/api/schema.py": {
      "sha256": "e839e85d32982463056a5bedeb21ed99c1ede5602f38acb922fd970a27044581"
    },
    "src/adrl/api/service.py": {
      "sha256": "add6130fe1b3fe65fe37b2179a025f59aa07c315d14a6a7ea648aed43f5f8818"
    },
    "src/adrl/api/store.py": {
      "sha256": "9527d95565df58003469be2ea62514d8cb13fdce8b87295e4a06b6c76b366dd8"
    },
    "src/adrl/app.py": {
      "sha256": "ee397176ddcd305a1b5c70eb551a06e98b2065a076fa04593edb9da724a7741a"
    },
    "src/adrl/cascade/__init__.py": {
      "sha256": "bc8b4bd3f53c5cbf7dc8ed81ee1ed9719c01d7ae158a11ec29263efa2e08c582"
    },
    "src/adrl/cascade/boundary.py": {
      "sha256": "66839b708bc041b4f26aa74d9facde2ea9e367a9263c492a90e3d3ef12fc98e2"
    },
    "src/adrl/cascade/controller.py": {
      "sha256": "fedef16cf2a4ce239f8c7c07eb27331b6bdeb5656735b84ab925f707adbe0a1d"
    },
    "src/adrl/cascade/handoff.py": {
      "sha256": "7a6e066343ac3fd87a63f1dd1ddecda6aa29269f28dc9ec13da88aad106b747c"
    },
    "src/adrl/cascade/sticky.py": {
      "sha256": "28346143b50492f80c41aff7ce044ff27447bb335146bf236b37500c58f711cf"
    },
    "src/adrl/cascade/tripwires.py": {
      "sha256": "c91eb8b1feeaf8e62f0ae5866d76205f3e3fe8a627d29885b893d70d1829c728"
    },
    "src/adrl/cli/__init__.py": {
      "sha256": "aa78bc2cbcd04512b0ce732a5272efb78c4f9bb95daa7d7d59c0b4e7485575b4"
    },
    "src/adrl/cli/improvement.py": {
      "sha256": "916f93bad7c38e57b0626dcea70e833a02ad3487d4aaa8a91970339e10421963"
    },
    "src/adrl/cli/ledger_commands.py": {
      "sha256": "4d78faf44948f73928cba50f0fba8b4c0c2a32bb05250f1f7b121a784a5045fb"
    },
    "src/adrl/cli/main.py": {
      "sha256": "b155525971ee910191cccf609bcf2760c1f19a170fb00c6de8907ee567429322"
    },
    "src/adrl/cli/product.py": {
      "sha256": "048db7e3d777a32b57badea048e37fb3cc0774ecabfdeefc5eff927e53ff02c5"
    },
    "src/adrl/config/__init__.py": {
      "sha256": "3803eb7d9d9190983da2058ca3d85a56d1bf2386d94d3743b3fd445760585bf7"
    },
    "src/adrl/config/checks.py": {
      "sha256": "de6b5ba06701c0deeddde05ba9f9bbe057a507e58107cfb4f5fd56568b277cc6"
    },
    "src/adrl/config/loaders.py": {
      "sha256": "fe0ad675a1d6b49648c7b9c3a2c7ba813b3abcc421d204a35309cfc066896792"
    },
    "src/adrl/config/models.py": {
      "sha256": "baf7f4346711468102c2644787cc0f275ee84e70972a51d2482bcfd648b94dd0"
    },
    "src/adrl/config/settings.py": {
      "sha256": "4a4daad400b9786e32edead3c7ad41e117e39459f93e915b83651b237a1d98b6"
    },
    "src/adrl/core/__init__.py": {
      "sha256": "2e4be193ed644ada5559624553d72d9f5c6d4a98dded8b7e974692146ab0e983"
    },
    "src/adrl/core/attempt_coordinator.py": {
      "sha256": "08d43e990442e2d55c5785fbf86b016b3ba1d07864c536723d2b1de8a00c61c2"
    },
    "src/adrl/core/container_control.py": {
      "sha256": "15942e04fe83bfc419b2c4913505ab0df01909a429f6c86096a2430936282e69"
    },
    "src/adrl/core/enums.py": {
      "sha256": "fa1a86d4c6ecc321ff7baf945aec440b8cb9a9a3937d78c3b9c9ffb435bf9bc7"
    },
    "src/adrl/core/errors.py": {
      "sha256": "4a9b11ae4fa527a813e800ebff00c2edfc04d2dd8cea0b0d6d7cfa7e1916bfff"
    },
    "src/adrl/core/execution_control.py": {
      "sha256": "435b1b28c2219e8b571c5895ff7d9b359356cefb594e3eae734a99a006c52a49"
    },
    "src/adrl/core/ids.py": {
      "sha256": "903b7c34cbae920f9a00edffcfa57e56d866090004925f712f90d7f00167f9e2"
    },
    "src/adrl/core/isolated_execution.py": {
      "sha256": "d8d994b245ae30f9b535c18a0f6fbddf67c45bc88ce76f37e0f6c5b6b1edba5e"
    },
    "src/adrl/core/launch_markers.py": {
      "sha256": "b3d95e9b7a7ba00e0f2f0cfee122aa7ce261eb2639e1fd29af314e5ddbd8c75f"
    },
    "src/adrl/core/ports.py": {
      "sha256": "8e0380c0b7d01e3b81bb3e6e499c6608b71522fd83f1e508d721a90b2ebf2c6d"
    },
    "src/adrl/core/process_anchor.py": {
      "sha256": "7e30ca14f22cef0787d3381eee8f9db75814813961bea4a1bb94984b5b68ca14"
    },
    "src/adrl/core/process_owner.py": {
      "sha256": "be67390cc95dbea608a1cf170e9452fc787730e2a60fc44825b58fcefa7d94c4"
    },
    "src/adrl/core/resource_owner.py": {
      "sha256": "5398a355ac7571929203e81eef8efcbc9436cf5452d3e3ee4c1440581b3d68f9"
    },
    "src/adrl/core/types.py": {
      "sha256": "1378a303072abce0c1257c6c1b346991b83dbeee204e51d5a8560c2e2f57e1b1"
    },
    "src/adrl/gates/__init__.py": {
      "sha256": "0566861be1abd45018586c80ea2455a144e4fc8ef6e14f60a27f9d02cf2dbb23"
    },
    "src/adrl/gates/block.py": {
      "sha256": "b4fbf137ccfda62d36babb611bd875fc8e96ed835fc03373cca0b66b00174c7e"
    },
    "src/adrl/gates/cli.py": {
      "sha256": "aebd8c3eb7a3e53351eb3eb6ba88c0335fbbb27e94de225a6f9c8410bc601ef8"
    },
    "src/adrl/gates/content.py": {
      "sha256": "788bd77d75fe741557cfcc3a1d34c7d6c3bb0dd0f56f1ca9b0153407f7f8b194"
    },
    "src/adrl/gates/coverage.py": {
      "sha256": "e5ea97fa70fc83eec31b65285b4e7df464f69507284fda90075c867b6313bfd3"
    },
    "src/adrl/gates/deployments.py": {
      "sha256": "4657f74d3f2aefeb4c4c3c007d5d97ba67635475df500c8479278129295203c2"
    },
    "src/adrl/gates/detectors.py": {
      "sha256": "9a36fa3fd5e1385988f15f7a8845300b751e4aac6383deca1a7306e1bdb3935a"
    },
    "src/adrl/gates/egress.py": {
      "sha256": "68d6eec54dac44da14bfdc6e9f74110a0e9a451d389aa6fff31f40f3cba2da43"
    },
    "src/adrl/gates/feasibility.py": {
      "sha256": "53bee77bbe27ebec7fedc8e8be813823b86b322d56af653dab79909501cf5ad6"
    },
    "src/adrl/gates/measure.py": {
      "sha256": "ddb1c238ee1b05b4a28d3ed10418ee2c6e8ebdd6ccb7be6b8f9cd787c4fd19a0"
    },
    "src/adrl/gates/pin.py": {
      "sha256": "525972e0f191b92c92ecd483a76619806da51f63124987cfe82857aa1986f9d1"
    },
    "src/adrl/gates/pipeline.py": {
      "sha256": "7c33d96afd92a23913d5877482fb56fa25252979c11d458be25012b7d9bf7603"
    },
    "src/adrl/gates/repo_class.py": {
      "sha256": "ea362f101fc267fa00f0ebc373ff57f020aa7113d384e7c65f33974d6d651624"
    },
    "src/adrl/gates/sandbox.py": {
      "sha256": "2726fe38e484eaf8402f3bd04e648ebd257dc1f0e47f0cd7d0f2c417ced9714b"
    },
    "src/adrl/gates/secrets.py": {
      "sha256": "cd60482c0bec4d4fce167283a4d9e629df220bd65458a285a772cfeacd372796"
    },
    "src/adrl/gates/suppression.py": {
      "sha256": "e191a45a9a4d39c620de57fef049685f1bc47beb7981bd29082277ac508274d0"
    },
    "src/adrl/gates/workload.py": {
      "sha256": "06190e43f32cdabfb1b3b70466f3b0b1982b8898924dac9c29572d126c27c29c"
    },
    "src/adrl/learning/__init__.py": {
      "sha256": "87db4b96f6dc2ed884dedcfd80956d2deebed4e7e219960f44b91b96bdbe6244"
    },
    "src/adrl/learning/abstention.py": {
      "sha256": "04c7f7c58ad90da533854f186e3348f3f0a9a6975a28c1a7acfe3e391bd57119"
    },
    "src/adrl/learning/artifacts.py": {
      "sha256": "b619ab050dfea6317521551de7ed56b188e28a10da9dab488f9b9950145d4be0"
    },
    "src/adrl/learning/dataset.py": {
      "sha256": "9e6ec8fcae5b78b07e1de0e874b338bc0233cab69bb8f39e78c3235bec0fa192"
    },
    "src/adrl/learning/estimator.py": {
      "sha256": "40a8c0fb0453cf47c52e96b32d5eaadb3000d2a38e1300e3e9224211360b332c"
    },
    "src/adrl/learning/explore.py": {
      "sha256": "1c57f911fe66cf38f7e95744971395388a9791d8a527870eb16a352b2ca01189"
    },
    "src/adrl/learning/improvement.py": {
      "sha256": "21cd27a5d31a66797574e2f02ea3fc4e4ea48b6150343ef301a9289ae8b80c81"
    },
    "src/adrl/learning/pairs.py": {
      "sha256": "73283b6c0af83c409d37d4fecce3d31437de7a65aca66ea1e0ff53efeb276160"
    },
    "src/adrl/learning/readiness.py": {
      "sha256": "947d22d853c3bed68521ee2d005947696bce404034e5819dfc0f697533e55aea"
    },
    "src/adrl/learning/tiers.py": {
      "sha256": "6d0a17d8a57179e13544a75bde5144ae93343e21c966b71eebdaf0fdbbb1fca8"
    },
    "src/adrl/ledger/__init__.py": {
      "sha256": "634cb0cb9f669d0a256abeb6e63a003685026f6edecce46d4e4ee77676d5761b"
    },
    "src/adrl/ledger/anchoring.py": {
      "sha256": "024913a90f513ae8583d409d03a77dbffb00a367f207b12bd5a762c97879fbed"
    },
    "src/adrl/ledger/attempts.py": {
      "sha256": "76e85c5028df2f05c0e8d3f680078e84230952f85a0534a21776842251e2b0ae"
    },
    "src/adrl/ledger/capture.py": {
      "sha256": "ef644fa690e69bb718f00534aec19aaf55d541bbf38f7249bf854da7e8bebaed"
    },
    "src/adrl/ledger/counterfactual.py": {
      "sha256": "43c9b8345e855257ea9f727205ca678c58be995dea1c8234dc15132ece501922"
    },
    "src/adrl/ledger/crypto.py": {
      "sha256": "01730ca1c51e4cfcd48beef49b744e4d0cdca4c6996b09c77fb7a219e791ebb6"
    },
    "src/adrl/ledger/egress.py": {
      "sha256": "43a05c01cb284d6c53c2b79b0be906e4f9a291788f7932cc85cc13a639a1feac"
    },
    "src/adrl/ledger/embeddings.py": {
      "sha256": "f766d1ddeec3e5742182cd4c468483769c382cf9fbbc76667c3a90a1e7f2b64c"
    },
    "src/adrl/ledger/erasure.py": {
      "sha256": "82298f397b3c752d3983f5415f09b59e59de5bc14fd246460bebf75bb03803f5"
    },
    "src/adrl/ledger/events.py": {
      "sha256": "91880f121e9e30cfe4684305135b9a99258a974cbdb87a0870eaa537db6a2cd3"
    },
    "src/adrl/ledger/facade.py": {
      "sha256": "2bb55f817fa889b92fb87ee67932a0a07a1821bdc73d7c9e0dabb6e40d89e892"
    },
    "src/adrl/ledger/improvement.py": {
      "sha256": "21e2dc8f8d26af7177a5a5c0cd64102b1154a2368784dd71432861a9aafbdedf"
    },
    "src/adrl/ledger/keystore.py": {
      "sha256": "7317110097fceaef34a69fb3fbeff3d0e27db17e0508e88b8063abf812c44d12"
    },
    "src/adrl/ledger/labels.py": {
      "sha256": "be1f1b089e477fb0a3ab6076b754e858f24950d27dcad5c4cba2b86dc6ac361f"
    },
    "src/adrl/ledger/migrations/0001_initial.sql": {
      "sha256": "5c0e582136caf827307f3f8a08098f9eb5c05be599a469a1b7fb0472a776e835"
    },
    "src/adrl/ledger/migrations/0002_evidence.sql": {
      "sha256": "177647eb19f86c6d286720bb47891d8d73178435e4e44e7daf8326a0e2a99bcb"
    },
    "src/adrl/ledger/migrations/0003_product.sql": {
      "sha256": "0689c91906d06152af09937eb2758f7891c14a7456542632d19b40567b0f30b6"
    },
    "src/adrl/ledger/migrations/0004_integration_mode.sql": {
      "sha256": "f34bc9fab14caad2ed8b85e716a0fd984a1061649cc5f015f2c2ff9236d93bf9"
    },
    "src/adrl/ledger/migrations/0005_session_verification.sql": {
      "sha256": "854c5ab5137417effded2b1d12317eb3b34ef89fceb9ab044486dcd242a210ac"
    },
    "src/adrl/ledger/migrations/0006_improvement.sql": {
      "sha256": "b194c62ee650354af4b5f7cbf9ab4d17d226572f9b514dba5fe679bdc9f24f5f"
    },
    "src/adrl/ledger/migrations/0007_captures.sql": {
      "sha256": "e45cd62b7e45fe68227440490b78b7e42a2ebc731d1ee88aba31c40909c8a719"
    },
    "src/adrl/ledger/migrations/0008_attempts.sql": {
      "sha256": "d78df82450565671d96d2c9648c493f490ab81ec0fde8061b269c66c49a98d12"
    },
    "src/adrl/ledger/migrations/0009_attempt_capacity.sql": {
      "sha256": "0e534507e02da25c7f0e6b9d5c1e7408e8c8b17831166bca534895baf4a1e8f6"
    },
    "src/adrl/ledger/migrations/0010_execution_fences.sql": {
      "sha256": "d352e2cd587a330c0403e76ee6656e9838a21c7cbc3253b9b44938b759e48555"
    },
    "src/adrl/ledger/migrations/0011_resource_ownership.sql": {
      "sha256": "3f1828853c85aa555b1e588d458ec6180ed2c9377faa1057a62e6ef307673ecf"
    },
    "src/adrl/ledger/migrations/0012_launch_history.sql": {
      "sha256": "2b4a4146f2e1dd5731cd75ac8990864f11f339a4f3b129e846585ae54122bb5d"
    },
    "src/adrl/ledger/migrations/__init__.py": {
      "sha256": "f01702f0272a85680c14f0773562a7efd919f830b1cbea48b773f1f3ff5135ff"
    },
    "src/adrl/ledger/outcomes.py": {
      "sha256": "87ed8af4d5d244af77eadb36d8edc44fb3e62f86c1dbb02f921bcde772cba409"
    },
    "src/adrl/ledger/projections.py": {
      "sha256": "1d21a9a3921eb0d1fd09e95c2e5db2ee6f24649afc8cc0b8221f6d975c8048ee"
    },
    "src/adrl/ledger/readiness.py": {
      "sha256": "43677204359845245b952c5a26c567db7b61994ea95fbcedf2b187bff56bd204"
    },
    "src/adrl/ledger/replay.py": {
      "sha256": "a317c2a83252cdaeff25721bf9b3ba3006deac2a5bc217f9b931a9d7c5cf3676"
    },
    "src/adrl/ledger/retention.py": {
      "sha256": "a5530bf46282ae0f93b7b473e1518b66c44289f71e759aa67fb7d045b90a42d1"
    },
    "src/adrl/ledger/session_verification.py": {
      "sha256": "e6f5efbc51107337ea75c4a363c4c520d04da76ae021ddf45dca06c76e96bb9e"
    },
    "src/adrl/ledger/shadow_retrieval.py": {
      "sha256": "03961c21ddafa3d69426280db1fc7122568b6bc0433e1dd2ea45fb8876edae79"
    },
    "src/adrl/ledger/state.py": {
      "sha256": "3b797bd74e4c2fa94f456fcbfced6f95388810ce628bef88873c4a6423765ef0"
    },
    "src/adrl/ledger/store.py": {
      "sha256": "4bef263447219212d3e8b3262d0666abdc20ed9832d15777595eae1621ea35c2"
    },
    "src/adrl/ledger/upcast.py": {
      "sha256": "6af7243a7c4ccd55fda7014617644a3a6d735ba1c4a6f8bfc67bca8522868732"
    },
    "src/adrl/ledger/verification.py": {
      "sha256": "c2846a6a8cdf0b1c1c479e71cda691dc8a70d11db9d708056ec87c7ddac313a3"
    },
    "src/adrl/proxy/__init__.py": {
      "sha256": "49436b67b95b630642b80f88850ebfc37c1dad4c52f1b51834b766e89f112a1b"
    },
    "src/adrl/proxy/asgi.py": {
      "sha256": "491c8a431380483eff035d136749a9c13c7738ad613f75ee879fdd929ee23640"
    },
    "src/adrl/proxy/errors.py": {
      "sha256": "6208b8f4b9f2442a33ea8022419fd22903dab91079e4de256edf755d6bdf4a36"
    },
    "src/adrl/proxy/fallback.py": {
      "sha256": "04919e7e581ca96a82c9ee99d7ad5527ae36f17853b39ca476dd0c8a97307e35"
    },
    "src/adrl/proxy/observe_only.py": {
      "sha256": "bf7adbbe6807ec5db6165a041597e4a8df3324061324632b6c1f87072d3138e3"
    },
    "src/adrl/proxy/pipeline.py": {
      "sha256": "68a170c352ad7793113626002be84608f9c656740280156405682040407b152f"
    },
    "src/adrl/proxy/stages.py": {
      "sha256": "53513de35680401ec134a0d360b84b894fe6fdbd6be2c3c6c42356b836a4174a"
    },
    "src/adrl/proxy/upstream.py": {
      "sha256": "cbfc2436d9f3e87813a392e3839b4388d34b8d4c17194cce3c5f0bba84ec98d2"
    },
    "src/adrl/routing/__init__.py": {
      "sha256": "ec71c7c97beb192638a74734a09c8f3d6501adad3dfd30261411e7c6e4ed859b"
    },
    "src/adrl/routing/advisor.py": {
      "sha256": "cbd31e1919d24546641003bd2b4d232d56986f94c189f0b61729816031443450"
    },
    "src/adrl/routing/cascade_feasibility.py": {
      "sha256": "ee8359e5655ee51319727ed4611be04ba5c76f81b02982b67a823b99ec494f97"
    },
    "src/adrl/routing/cost.py": {
      "sha256": "428e3894b10fd2dd214294da49aa78f2251c987715b3a2d59c4833e4e1e074d0"
    },
    "src/adrl/routing/features.py": {
      "sha256": "7de44ffd52b490d33b2f66f632d964c6df57f8a7ea31d34783db973db926b205"
    },
    "src/adrl/routing/policy.py": {
      "sha256": "a5d9bd9a9da8b48ee76cfe13cfd7f3a1cccb5ceb542d3178f5f3f294a48c4b60"
    },
    "src/adrl/routing/registry.py": {
      "sha256": "18ad3fc453d67c11fe8cd783ee2cfb596b03d12f4ece21cf7b672813e0365dae"
    },
    "src/adrl/routing/router.py": {
      "sha256": "36666f3e9a6944a9974d35b906e0bf231014f96798ba65dbb8670dfa19f24045"
    },
    "src/adrl/routing/rule_health.py": {
      "sha256": "c9843b350c36731bf5778b900b107d231181be794a88ec9b12cb91a49d2daa8b"
    },
    "src/adrl/routing/side_effects.py": {
      "sha256": "d617fa3d9ba2d8b93c4cf8d32571fe795ec979f40e21bce057b45b275d74699e"
    },
    "src/adrl/telemetry/__init__.py": {
      "sha256": "cbf0dc80c108a2a5c0714c67a2588efe136d3969f0cdf31f70de3abb7ba7308a"
    },
    "src/adrl/telemetry/logging.py": {
      "sha256": "4fb1d7fb6d9d6f14439c5344f7021ed95edfa0ec5a865a136e26b6f1fd074e07"
    },
    "src/adrl/telemetry/metrics.py": {
      "sha256": "db03f5ff99a8cc0b476933315ea4ef00366bb432f47b7bbbf2f89a4dd38a1b34"
    },
    "src/adrl/telemetry/semconv.py": {
      "sha256": "f03aab966149fe22a9fcda33a0097bbab9b144d4609014e4acf79bb14fec0dde"
    },
    "src/adrl/wire/__init__.py": {
      "sha256": "530b1c1bba4f681b33433510837137e5d6d0e4653cb3544a4a2548d0de4da695"
    },
    "src/adrl/wire/adapters.py": {
      "sha256": "0f8abd8962d3a2ffeb8be2f7a9d060caa47b908e5a8fc2e177eb691144489600"
    },
    "src/adrl/wire/classify.py": {
      "sha256": "7abbce3cc0ba508bddea588bb81dcc55c6a7b88e3cbd2506e118dbc503c90b90"
    },
    "src/adrl/wire/identity.py": {
      "sha256": "61a3e71e6fb97617e82f3095750041607edbaa9eff43bf4f4f7c97f9a8ac2e5b"
    },
    "src/adrl/wire/observe.py": {
      "sha256": "a8a9e237b1cf6397597dfda4762f0e65507d7b2fbe09e8bdfa3970c35d928cca"
    },
    "src/adrl/wire/parse.py": {
      "sha256": "f4c7c61438e50c8b91ab08ff927dbb17d5887802949ff3ac27925c0d9fcef28e"
    },
    "src/adrl/wire/profiles/__init__.py": {
      "sha256": "d4e7de031920d9e6d223384e9a097aa4c2ed50cd6259c70a1e6e60957a37fab2"
    },
    "src/adrl/wire/profiles/base.py": {
      "sha256": "928dc02f1909b939f71adcf70244d507b3bb1c122799339f50e7ef40f2077ad8"
    },
    "src/adrl/wire/profiles/messages.py": {
      "sha256": "be738637186caf85ef47745679e9d94dd34cff05cb51ed3005fbc7e0fa70524f"
    },
    "src/adrl/wire/profiles/messages_responses.py": {
      "sha256": "8a8d1d188144c834d4ec82e90dffc7e2842c893771b9da278ea032e2be239ee3"
    },
    "src/adrl/wire/rewrite.py": {
      "sha256": "eb49c51565003b70432666f557b33ce7c89064d630fdd448b15254198d8fe468"
    },
    "tests/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/adversarial/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/adversarial/conftest.py": {
      "sha256": "096d1351989fa02d36f10c725853624ca8f1df24f83de5da9ee26bcbf07916ee"
    },
    "tests/adversarial/test_saf_suite.py": {
      "sha256": "d7a1d978c4dfecf3b54816a63d824f54eb2bb1c7531982cd28501478b9984cda"
    },
    "tests/adversarial/test_tru_suite.py": {
      "sha256": "a55949985c2269dcc29902af7dc95b1402b0e39731bb11c075f7466341d5b2e0"
    },
    "tests/conftest.py": {
      "sha256": "0998e7620ac04588746ca1b2f22ee5a2626e869cd8ce507708758430df81b9b9"
    },
    "tests/fixtures/launch_owner.py": {
      "sha256": "00d61d8eb0ff5f00b9b783e9e044f436f148461c8a8bb5ef1851daa9bb34da48"
    },
    "tests/fixtures/profiles/identity-v1.json": {
      "sha256": "39314dc7c49f415a368afe544570b8099d4215f223a5b3242a33a8678fae2aec"
    },
    "tests/fixtures/seccomp-v27.3.1.json": {
      "sha256": "9c1025c88ccaa517b648da571961838744ea2137f176bfe6a48b21294cae9c76"
    },
    "tests/fixtures/wire/compaction.json": {
      "sha256": "e13eee45e9d5b2cdf845b50fd1f2431878f01b64ba732dc00dabc41a91d01bf9"
    },
    "tests/fixtures/wire/continuation.json": {
      "sha256": "9208f708a25d64bff9020d0d792154fcbbba41a6c34c7a2131933ab036ea9c1d"
    },
    "tests/fixtures/wire/count_tokens.json": {
      "sha256": "0413c1d9033d9f2eecddf50b57b8d93e35d7beb02aa9152e7759b584938b7b4f"
    },
    "tests/fixtures/wire/escalation_parallel_tools.json": {
      "sha256": "2fa413954c24c338474854aed7d448876ed15f822ea99fc7c8416a55637511d1"
    },
    "tests/fixtures/wire/fork_subagent.json": {
      "sha256": "651b2b01ac64afcff23b6bd933fa86cd5d1d8e4e82590668e42968167bbd98bc"
    },
    "tests/fixtures/wire/metadata_only_user_turn.json": {
      "sha256": "6d2d342bbaf769aa7a4d9135f822cf7dedb4ec77e35ff0b4d8333b563bac41f2"
    },
    "tests/fixtures/wire/nested_subagent.json": {
      "sha256": "0e0e881ff882e443fbe3b414e7836897d70ab925603e74bd8184d0e63ccd5b2c"
    },
    "tests/fixtures/wire/parallel_tools_full.json": {
      "sha256": "505559666a116132c2cc492b7158c7b968f0da783646fa87350f7ba13481928f"
    },
    "tests/fixtures/wire/parallel_tools_partial.json": {
      "sha256": "d56eaa6e53ea1eacf36329c0892a8263bbfcb2c86d1ddd8e84a4d9e974d2e737"
    },
    "tests/fixtures/wire/pre_warm.json": {
      "sha256": "55bcf0673ed5aa3b3c7948d2d8b8fc1da4106c037c493d3c1da5fbf3164c5f55"
    },
    "tests/fixtures/wire/title.json": {
      "sha256": "023640c7088508eeda108c1a774c012d1beccb5e0d728e1a1c05bed7cbc6224d"
    },
    "tests/fixtures/wire/topic_detect.json": {
      "sha256": "3245b7021cd98b8b98c86a23713e8d7aea02cbbda0ad366fb4d3b4538dc42ae9"
    },
    "tests/fixtures/wire/user_turn.json": {
      "sha256": "0cab3bfbf06c45aab1e1be8f019159aaced9aed31e56f10be68c8292ef7c2816"
    },
    "tests/integration/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/cascade/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/cascade/conftest.py": {
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/integration/cascade/test_controller.py": {
      "sha256": "5d86e61671de29a2082f223cdd8f641097842fd7ba5476ca286f2f6d66175759"
    },
    "tests/integration/cascade/test_review_defects.py": {
      "sha256": "857c1c1aeba37e29c5694d4414f06408409b2a92c2758c6ec227d46d94bc0b70"
    },
    "tests/integration/e2e/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/e2e/conftest.py": {
      "sha256": "90ab6359a3907e1d13920a3391133d385b0f6fc0d70e8cb62e8b7b29c595ca9c"
    },
    "tests/integration/e2e/test_composed_system.py": {
      "sha256": "28fa67ba5b497c4d9e8d89c78c5895e21b465e5bd8efcadf037266c2c76f55e6"
    },
    "tests/integration/e2e/test_outcome_contract.py": {
      "sha256": "b19cd9e234079e3076b966113b89dbb41f074922342ed0d0e639155baa48cc1b"
    },
    "tests/integration/e2e/test_pin_failure.py": {
      "sha256": "c974d6d2d3e09e24bd5547c3dc9334125e3b2273ff6017b2fb80ec58969d509a"
    },
    "tests/integration/e2e/test_product_services.py": {
      "sha256": "329a6b4071da40f87675375f530a3993a2cfb69b953468d611fc5692fc7dc963"
    },
    "tests/integration/e2e/test_review_defects.py": {
      "sha256": "f17cf912128501843517d4e134ae2c6664bb5be490197d8fe4c5200bc876ebfd"
    },
    "tests/integration/e2e/test_tru.py": {
      "sha256": "42652efc6d9484aba196e25d37a483226e1321e18855c6622ffa89a97ac4d081"
    },
    "tests/integration/e2e/test_trust_wiring.py": {
      "sha256": "43ae74ee8e66dde0b90bfbaee0a9bfbf8f082d036a2211a6c0afcfe0e9a950aa"
    },
    "tests/integration/gates/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/gates/conftest.py": {
      "sha256": "925ed24d508f2058d26f5ce6f8de4d629500919b1abf96dbc4810fece3574b74"
    },
    "tests/integration/gates/test_pin_durability.py": {
      "sha256": "7007829914677d64e694b934c6868026e3cfaf62359ad6dcc746129c0863b5c4"
    },
    "tests/integration/ledger/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/proxy/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/integration/proxy/conftest.py": {
      "sha256": "fe8bf67e23465d0597654bdfa93b50949fa6c7730eacc303870916b2f33192fd"
    },
    "tests/integration/proxy/test_fault_matrix.py": {
      "sha256": "683cecea87149979ae4f5f6888c62b418c874912120543640f433724a73a14a1"
    },
    "tests/integration/proxy/test_pinned.py": {
      "sha256": "36e97c508af175b32be4bb234cf9a54d0f3539415cecad24689da9092adb08f4"
    },
    "tests/integration/proxy/test_profiles.py": {
      "sha256": "46ff3d92a6ffbd8885b25e52a6e67a357276365caab866035e51bf55bfa2b48e"
    },
    "tests/integration/proxy/test_removal.py": {
      "sha256": "b488d5eb5ee8e6d5b6e6ca0baa1dd8d6d52b2be54e25a54690814e222a710473"
    },
    "tests/integration/proxy/test_routing_paths.py": {
      "sha256": "24e668347d358f36f7e080cfbc73a4cfaccdc1c84f46c10fa13a58bae4afc655"
    },
    "tests/integration/test_cli.py": {
      "sha256": "46a4da25d892d293447514428c8efb2c7029c42c8c643bbf8b8005956d5a49dd"
    },
    "tests/integration/test_cli_verify_snapshot.py": {
      "sha256": "56a6ef0e166aa8cee3254945d9d4df74ef5120ed0ac11925f7bb181c2cf74b14"
    },
    "tests/integration/test_launch_engine.py": {
      "sha256": "32f2f683e5dddb63e047c86f2cb1aadfac51046701765915b4bb176ffc26cc84"
    },
    "tests/integration/test_resource_engine.py": {
      "sha256": "a66c6e187c1012f6e39297abdc88af1c74de0d64cee3097940770cc1be18104f"
    },
    "tests/unit/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/cascade/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/cascade/conftest.py": {
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/unit/cascade/test_boundary_tripwires.py": {
      "sha256": "1e1ea158cc979a2b435a2976075d231f6e7574e3b20130aca301d870c020f53f"
    },
    "tests/unit/cascade/test_handoff_sticky.py": {
      "sha256": "e9d6624337d29e7c11fd0ff24d79a1617210df1a5885f06bc5b270838138407f"
    },
    "tests/unit/gates/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/gates/conftest.py": {
      "sha256": "f39063ec22ae5c3762b8666971bf32f5c3fd47ffe958b6b2c42b4642d17a9108"
    },
    "tests/unit/gates/test_block.py": {
      "sha256": "05d72a875190cf71fdc694b209501dc0a2905a70a29ff949f3ca75d183a749c6"
    },
    "tests/unit/gates/test_content.py": {
      "sha256": "f0cf9ad15796159748e3b67450eb02839d220db129119daaace39b85700dbc23"
    },
    "tests/unit/gates/test_coverage.py": {
      "sha256": "ffbcf9882584c6acec0d7afd83a2b28bec32e059bff9848ba31e9e0203bde2c1"
    },
    "tests/unit/gates/test_egress_writer.py": {
      "sha256": "f6e83d902381ebdd6d062181bad53e7db6be6a3d3de13d13d3f5ec460c209f0f"
    },
    "tests/unit/gates/test_feasibility.py": {
      "sha256": "5caa1fb734c321de0f8b096aba41a41cfcb340ac12314508fbba8bb8fca7e92b"
    },
    "tests/unit/gates/test_observe_mode.py": {
      "sha256": "b31f9ccd6f8c5f84ca8d3871045c412e3ca755335eb5e5ce286323c8272c7ea5"
    },
    "tests/unit/gates/test_pin.py": {
      "sha256": "2edfc3a5ba67f7859e25192dc467cb905a87918118631f657c4f78a3585696e7"
    },
    "tests/unit/gates/test_pin_write_failure.py": {
      "sha256": "ce3e9c056dd09485b0590bc9b7b69bd28c1df2a13df462f59d7b0b6dacf84121"
    },
    "tests/unit/gates/test_pipeline.py": {
      "sha256": "d3cd972b9ca4cef20b93502bfdd7f4b3ea2b451220400963d094641768c8d1af"
    },
    "tests/unit/gates/test_repo_class.py": {
      "sha256": "b39eeb5693390c34ae0b369c3059a5d0b010d923e7ec759902a135fb2744092f"
    },
    "tests/unit/gates/test_sandbox.py": {
      "sha256": "5aac4a4702a151be6b738ac07aa41b9eec9acad03b5e22fee80c7ef71366877b"
    },
    "tests/unit/gates/test_secrets.py": {
      "sha256": "229b8dfa52ac3afded7c8f4727437d1049768c04d0f1f4fe9dcbc354219ad628"
    },
    "tests/unit/gates/test_workload.py": {
      "sha256": "47caab4f52becb3f5875cd982cb3797490ed930f9e4075d1d131a84e8002c554"
    },
    "tests/unit/learning/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/learning/conftest.py": {
      "sha256": "d9b57452143653991a05cf299a0d7bf073d79ae0a5647ce5cb99e993035e937e"
    },
    "tests/unit/learning/test_abstention.py": {
      "sha256": "3c14a5d6fc3d3410ed6fd742e9a4bb69aa6cc5e947a7586a849e085a73998d78"
    },
    "tests/unit/learning/test_artifacts.py": {
      "sha256": "f1f12afada374f40dc97e1ec0d1cc980b5a475d9cfc356cb30c500fc04a68d64"
    },
    "tests/unit/learning/test_dataset.py": {
      "sha256": "0875f9736aa544e5d89c82dc423ad8234df1894661e02a1a13b482f3b78ef936"
    },
    "tests/unit/learning/test_estimator.py": {
      "sha256": "67e5ca8963d4180cf2073fd3ee7e25e19f395805d99335e9b72727fad0b0d5aa"
    },
    "tests/unit/learning/test_explore.py": {
      "sha256": "b6909e90235924c026308e1bdfe26ea4c09ed106fa82cae3d1e3b63fa50e15c2"
    },
    "tests/unit/learning/test_improvement.py": {
      "sha256": "dd35b6f67bce6c75f26cfe476cd4464fb12f05e6a069999e36268a00452b1043"
    },
    "tests/unit/learning/test_pairs.py": {
      "sha256": "7c1ec762db521691164d94af5e8e879ec385a2ad947d4a60c6564cdc96500fe2"
    },
    "tests/unit/learning/test_readiness.py": {
      "sha256": "387ee35f6f6a392e5bb5a90ceb83a6a02f5be7c0dc71fb3587b6240b539e3757"
    },
    "tests/unit/learning/test_tiers.py": {
      "sha256": "696facc4b378c2c41a5be805f001196296d327d405ec4dac04a1bdf6debc7597"
    },
    "tests/unit/ledger/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/ledger/conftest.py": {
      "sha256": "010a76aad8e5d6b20585639ac45bbb42af795997bdc5622f8588206a62d6bf12"
    },
    "tests/unit/ledger/test_anchoring.py": {
      "sha256": "9f7a35b6ff66453013fc9a9a9f21bbf198d11c642e2787c55e5870ac9d169f08"
    },
    "tests/unit/ledger/test_data_inventory.py": {
      "sha256": "e08fe724b6bc84252c52cd383dccf3e24f94864d37a3a0ce8cf7b48911f7b2b1"
    },
    "tests/unit/ledger/test_events_and_labels.py": {
      "sha256": "f98a02f30e5dda2e65a62c1a98dd674f314a593a469bc2de250b36019b155741"
    },
    "tests/unit/ledger/test_outcomes.py": {
      "sha256": "92887f3c22fe9eb30d1e9b3762aef47967a11ad30bc523446c8ee9a2457eaca8"
    },
    "tests/unit/ledger/test_privacy_artefacts.py": {
      "sha256": "6e5bb64c39a75e64efb492cd3d5aadf8347db223015bd8acfc57a74b56fff647"
    },
    "tests/unit/ledger/test_state_counterfactual_shadow.py": {
      "sha256": "1d95ca1664ce9d1154d11b783fc1e1316d9029b4f1bc59b41ece6e574536e23e"
    },
    "tests/unit/ledger/test_verification.py": {
      "sha256": "e0ce2701e710e312595d76655b96f3778e498cf97ffdf71bad6032f8e2b30a94"
    },
    "tests/unit/proxy/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/proxy/test_fallback.py": {
      "sha256": "fe2104131ec80366485a03abb87d57feac7870b9ad8034d65856d15c7277cdae"
    },
    "tests/unit/routing/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/routing/conftest.py": {
      "sha256": "0c9512429a443e67b9b8ee0a9303c94fb4d2e060da9985bf8df0f537693e724e"
    },
    "tests/unit/routing/helpers.py": {
      "sha256": "734c48d9848c452adf3099874c0e1a0c198cf9132472e42bbe51c8b71849a219"
    },
    "tests/unit/routing/test_cost_policy.py": {
      "sha256": "5719bf0fc5618cd9c1cec8cbb240862cd29e440da4a01558416283d44458538d"
    },
    "tests/unit/routing/test_gateway_config.py": {
      "sha256": "a0da57f4bea464fc3734f779c0bd4f9ff319f927527f57c8bb84444b45483cbb"
    },
    "tests/unit/routing/test_mixed_intent.py": {
      "sha256": "7f55b41a8b880fcc9bb1c2365957cdbb5bd64cb7cb23d94c4bcea068933a5fad"
    },
    "tests/unit/routing/test_registry_features.py": {
      "sha256": "735b0211b50d8bacbb721519cd391833d650ab2bd0fb565ff8cbc54262f695da"
    },
    "tests/unit/routing/test_router.py": {
      "sha256": "6125b94e23395072b1e505a94d1c3ec26a638a9eb5acce5648872e62f071fa75"
    },
    "tests/unit/routing/test_side_effects.py": {
      "sha256": "33664bee279c24694789663aeb51afb6c8a241e530209eae0bca64374e771749"
    },
    "tests/unit/test_api_contract.py": {
      "sha256": "e88641a573a983f7494df8352fc0ff82408e93288ec13fdbf68e700cbf578e74"
    },
    "tests/unit/test_attempt_capacity.py": {
      "sha256": "dd1d91f5284f09ae7ee19ecb5bb10d6286bec82c75c6421e865aa04167c74584"
    },
    "tests/unit/test_attempt_coordinator.py": {
      "sha256": "62a7eca2ee0266fb95e8e1cbda2d93be2d9559d201c673f6eb2655dbfd181dc1"
    },
    "tests/unit/test_attempts.py": {
      "sha256": "4d54d16b9dec725d6a8a2b5f33dabd2fda214fe2019ff2a86d6ecbfef55c4096"
    },
    "tests/unit/test_capture.py": {
      "sha256": "8e46474960cc3f1574b884840e0b39f439b17cc8e2e57904ad8ad5146d438a7f"
    },
    "tests/unit/test_config.py": {
      "sha256": "8cb002b9206a441ca3730270a60335ec36646903a8ccbc3ad0c8344cb48b07e4"
    },
    "tests/unit/test_core.py": {
      "sha256": "d0172ff5a0d7ed7319b9595a9bf9381d903c16fab4ec37a1ec800729d57d2416"
    },
    "tests/unit/test_create_receipt.py": {
      "sha256": "c705d8845e740dc65d452caeaf0b18c419c3aa4cb5f1b8e995620ec2bed43c8f"
    },
    "tests/unit/test_data_inventory_migration.py": {
      "sha256": "94e45373f18f8d2254a515775493fc186a78873c5f39285701f34ee92522bf5e"
    },
    "tests/unit/test_egress.py": {
      "sha256": "cf8f778fab58fcc4dd05d03ae6ed6a8cadef183c8fec4a47492cd2522e169011"
    },
    "tests/unit/test_engineering_tools.py": {
      "sha256": "0e2dc01cd0abebbb61104f744dcf71a2eae4f848289b9f7718752008e9f35436"
    },
    "tests/unit/test_isolated_execution.py": {
      "sha256": "a7ded1c4fc3c9f1c5fec11a350a076368fcf99c2544836da70793db4b5ab8a25"
    },
    "tests/unit/test_key_revocation.py": {
      "sha256": "88406cb70059b4e1b272669d3c6d558e607415f0dd581991de46d9f57bd19cf8"
    },
    "tests/unit/test_ledger_cancellation.py": {
      "sha256": "e3e9fe83e60f06cd7892398b339f7db98373cccb3e7a8695cff35ab877c6f36b"
    },
    "tests/unit/test_ledger_store.py": {
      "sha256": "a4a8f03c183e99ba90d7bc9dd7f89d734dff2a9fa43d1e79d776dac58c81e4e5"
    },
    "tests/unit/test_process_owner.py": {
      "sha256": "2abc2f9d680caaec1335badc9e0f4face39b8666daf1ea0a6bcd894101fdc4cc"
    },
    "tests/unit/test_product_client.py": {
      "sha256": "053582512b7a5ea715eb1b608ca601b1d215689f3b90ad39363bc430653f6bf9"
    },
    "tests/unit/test_product_migration.py": {
      "sha256": "df0a92e1c28c709442da4255c9632e9547b258ce47464937d2ae07af2fb39392"
    },
    "tests/unit/test_resource_owner.py": {
      "sha256": "e272079c97194e2a266bc376d0768a7d60c269a86458d38345739425cc30627f"
    },
    "tests/unit/test_routing_lab.py": {
      "sha256": "1e6252edcdbddddd93dcd5ec01479a5f04274582932586d9078a969555f269da"
    },
    "tests/unit/tru/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/tru/conftest.py": {
      "sha256": "4e44fc41ac69e6a3641ba8ef2a72c78fc9cb8cdcb3f67f6f44e066d4dc6606e4"
    },
    "tests/unit/tru/test_deployments.py": {
      "sha256": "7fac080d29e32ca58865522f89d9d88d1945b0e39f1b0a4ac5cb27eda34de388"
    },
    "tests/unit/wire/__init__.py": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "tests/unit/wire/conftest.py": {
      "sha256": "2d022311296d129cd0d0fb8cc478c8c7d5d9e19dbeefcd9672090669092bde3e"
    },
    "tests/unit/wire/test_classify.py": {
      "sha256": "024df892a7ee443aaaacf602a7e81ac5ce984d2c34d9b84adef197641a8aab0a"
    },
    "tests/unit/wire/test_identity.py": {
      "sha256": "dc9cc6919b150a86522f29663255a9194368b579c525d778ab673e221b0de88d"
    },
    "tests/unit/wire/test_observe.py": {
      "sha256": "fd8d16f55c56a8c3155531495cee04c22866eaa822b2b63e9c931b5ee8d90fa3"
    },
    "tests/unit/wire/test_parse.py": {
      "sha256": "99badc52c64d96a0fb8c0c9699226eba184a4fd68f11f04cbffbb1cfbbbd8e50"
    },
    "tests/unit/wire/test_profiles.py": {
      "sha256": "e9afac4d2c1dff6a52d4a75e33b3f206913572e0f61dc9bcabdd151272807391"
    },
    "tests/unit/wire/test_rewrite.py": {
      "sha256": "ca91d55a0e36402bb3c0a80f0a100ee714c520df140a2586993f39e7a4aba096"
    },
    "tools/adr_module_map.py": {
      "sha256": "32b3088a50690481cf6b12b2e2e36ec2d32e9e5f606a2a4925dc13d28290b349"
    },
    "tools/check_all.py": {
      "sha256": "38b2a09a6686ee8923634f9ab25e35d80c0016ef5829e2028590ed1326919280"
    },
    "tools/check_config.py": {
      "sha256": "c4483f2c6998f75dd5c4a59d8a8fd7dc50ce509981d191046fb9685e51bc87bb"
    },
    "tools/check_data_inventory.py": {
      "sha256": "98d73890d3b4bcab0904cc4236e4e0bc7894f07f9fb164e3eda987681e705ee7"
    },
    "tools/check_learning_contract.py": {
      "sha256": "ae72d6162c1834ff8273b55de89d994628b15806451a4921adfac5db9045c724"
    },
    "tools/check_ledger_discipline.py": {
      "sha256": "751b6b350f3aaf5ffbfe6ebbd007e1ca752b9a91b737ce0e97f0176fa924b2dc"
    },
    "tools/export_api_contract.py": {
      "sha256": "f3a2a54e7b82c145d5c1aff0059d408c75dd52543ff9b0d7832de7bfef476020"
    },
    "tools/gen_dev_keys.py": {
      "sha256": "10c267560a3396c27f4f9df920fc40dd41b0a08a0d4423ec876c940d22859423"
    },
    "tools/gen_litellm_config.py": {
      "sha256": "64be40a877345d6da762eb061bcb13d06013ba8bbdf045d6eece5532a58e3139"
    },
    "tools/run_routing_lab.py": {
      "sha256": "6dace633d24fa4d185c418c9a070c14dbce53361057d9a78a00dc93c33946ff7"
    },
    "uv.lock": {
      "sha256": "8da7c7f9497ecdc071768eadf85535232c1d92f9eb74ff6244b74d6b4fe61cd0"
    }
  },
  "scope": "Code unchanged since first passing full checks; added tests and clarified docs; final checks-2 in progress"
}
FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/outcome-contract-2026-09-09/reviewer-metadata.json
{
  "pre-review-retry": {
    "session_id": "08a48586-41ab-479b-90ac-b049ca24e840",
    "requested_model": "claude-fable-5-1",
    "model_usage": {
      "claude-haiku-4-5-20251001": {
        "inputTokens": 21166,
        "outputTokens": 20,
        "cacheReadInputTokens": 0,
        "cacheCreationInputTokens": 0,
        "webSearchRequests": 0,
        "costUSD": 0.021266,
        "contextWindow": 200000,
        "maxOutputTokens": 32000,
        "thinkingTokens": 0,
        "canonicalModel": "claude-haiku-4-5",
        "provider": "firstParty",
        "costBasis": "list"
      },
      "claude-fable-5-1": {
        "inputTokens": 2,
        "outputTokens": 6667,
        "cacheReadInputTokens": 0,
        "cacheCreationInputTokens": 30152,
        "webSearchRequests": 0,
        "costUSD": 0.9364100000000001,
        "contextWindow": 1000000,
        "maxOutputTokens": 64000,
        "thinkingTokens": 4890,
        "canonicalModel": "claude-fable-5-1",
        "provider": "firstParty",
        "costBasis": "list"
      }
    },
    "is_error": false,
    "scope": "source/log review, no reviewer test execution"
  },
  "post-review": {
    "session_id": "65a8ba88-755e-468c-b03f-968da6e729f3",
    "requested_model": "claude-fable-5-1",
    "model_usage": {
      "claude-haiku-4-5-20251001": {
        "inputTokens": 34055,
        "outputTokens": 16,
        "cacheReadInputTokens": 0,
        "cacheCreationInputTokens": 0,
        "webSearchRequests": 0,
        "costUSD": 0.034135,
        "contextWindow": 200000,
        "maxOutputTokens": 32000,
        "thinkingTokens": 0,
        "canonicalModel": "claude-haiku-4-5",
        "provider": "firstParty",
        "costBasis": "list"
      },
      "claude-fable-5-1": {
        "inputTokens": 2,
        "outputTokens": 10311,
        "cacheReadInputTokens": 3219,
        "cacheCreationInputTokens": 44199,
        "webSearchRequests": 0,
        "costUSD": 1.40035475,
        "contextWindow": 1000000,
        "maxOutputTokens": 64000,
        "thinkingTokens": 8082,
        "canonicalModel": "claude-fable-5-1",
        "provider": "firstParty",
        "costBasis": "list"
      }
    },
    "is_error": false,
    "scope": "source/log review, no reviewer test execution"
  },
  "recheck": {
    "session_id": "f47c78bb-b7bb-4462-ac0f-6361ad990242",
    "requested_model": "claude-fable-5-1",
    "model_usage": {
      "claude-haiku-4-5-20251001": {
        "inputTokens": 14378,
        "outputTokens": 20,
        "cacheReadInputTokens": 0,
        "cacheCreationInputTokens": 0,
        "webSearchRequests": 0,
        "costUSD": 0.014478,
        "contextWindow": 200000,
        "maxOutputTokens": 32000,
        "thinkingTokens": 0,
        "canonicalModel": "claude-haiku-4-5",
        "provider": "firstParty",
        "costBasis": "list"
      },
      "claude-fable-5-1": {
        "inputTokens": 2,
        "outputTokens": 4829,
        "cacheReadInputTokens": 3219,
        "cacheCreationInputTokens": 18147,
        "webSearchRequests": 0,
        "costUSD": 0.60521475,
        "contextWindow": 1000000,
        "maxOutputTokens": 64000,
        "thinkingTokens": 3290,
        "canonicalModel": "claude-fable-5-1",
        "provider": "firstParty",
        "costBasis": "list"
      }
    },
    "is_error": false,
    "scope": "source/log review, no reviewer test execution"
  }
}

FILE /Users/arunmenon/projects/adrl-core/src/adrl/cascade/controller.py
"""ADRL-CAS-003: plan dispatch, observe responses, escalate at boundaries.

Secondary: ADRL-CAS-001/004/005/006/007/008, ADRL-SEM-006, ADRL-MEM-001/002/004.
ADRL makes exactly one attempt per request and never re-issues a request whose response had
begun streaming tool content; terminal failures are Anthropic error objects, never synthetic
assistant content.
"""

from __future__ import annotations

import itertools
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import structlog

from adrl.cascade.boundary import assess_boundary
from adrl.cascade.handoff import (
    TransformResult,
    latest_assistant_has_thinking,
    needs_thinking_suppression,
    transform,
)
from adrl.cascade.sticky import (
    MemoryStateProvider,
    escalate,
    family_of_model,
    mark_state_loss,
    new_sticky,
    release_ratchet,
    sticky_record,
    with_served,
)
from adrl.cascade.tripwires import TRIPWIRE_EVENT, TripwireEvaluator, WireClass, WireHit
from adrl.config.loaders import ConfigBundle
from adrl.config.models import ProviderPairRule
from adrl.config.settings import Settings
from adrl.core.enums import (
    EpisodeSignal,
    FailureType,
    OutcomeState,
    RequestClass,
    Rung,
    VerificationResult,
    resolve_primary,
)
from adrl.core.errors import VENDOR_PROMPT_TOO_LONG_PHRASE, ErrorCode, render_error
from adrl.core.ids import LineageId, RouteId
from adrl.core.ports import LedgerPort, StateProvider, StickyState
from adrl.core.types import Decision, HandoffNote, LedgerEvent, PermittedSet, RequestContext
from adrl.ledger.events import VERIFIER_FAILED_EVENT, OutcomeFields, outcome_event
from adrl.routing.registry import RungRegistry
from adrl.routing.side_effects import (
    UNTRUSTED,
    TrustPolicy,
    executed_side_effects_since_turn_start,
    load_trust_policy,
)
from adrl.telemetry.metrics import EVENT_DROPPED_TOTAL

if TYPE_CHECKING:
    from adrl.gates.pipeline import GateOutcome
    from adrl.wire.observe import ResponseObservation

log = structlog.get_logger(__name__)

PRODUCER = "cascade"
ESCALATION_EVENT = "escalation"
INFRASTRUCTURE_EVENT = "infrastructure"
POLICY_CONSTRAINT_EVENT = "policy_constraint"
SUBAGENT_EVENT = "subagent_passthrough"
BOUNDARY_CANDIDATE_EVENT = "boundary_candidate"


@dataclass(frozen=True, slots=True)
class DispatchPlan:
    rung: Rung
    is_boundary: bool
    escalated: bool
    from_rung: Rung | None
    handoff: HandoffNote | None
    pair_rule: ProviderPairRule | None
    block: ErrorCode | None
    sticky: StickyState
    route_id: RouteId = field(default=RouteId(""))
    transform: TransformResult | None = None
    subagent: bool = False
    state_loss: bool = False
    policy_constrained: bool = False
    pinned: bool = False
    thinking_suppressed: bool = False
    """The request must go out without the thinking parameter (ADRL-CAS-004 handoff rule)."""
    deployment_id: str | None = None
    """Attested deployment chosen for dispatch (ADRL-SAF-008); set by the proxy."""
    model_alias: str | None = None
    """Model name sent to the gateway for that deployment; None on the frontier passthrough."""

    @property
    def body(self) -> dict[str, Any] | None:
        """Transformed transcript when an escalation handoff applied; None means original bytes."""
        return self.transform.body if self.transform is not None else None


@dataclass(frozen=True, slots=True)
class CascadeEvents:
    fired: tuple[WireHit, ...]
    events: tuple[LedgerEvent, ...]
    sticky: StickyState
    infrastructure_event: bool = False
    escalation_pending: bool = False
    surfaced_error: dict[str, Any] | None = None
    failure_type: FailureType | None = None
    emitted: bool = False

    @property
    def fired_wires(self) -> tuple[str, ...]:
        """Wire names, as the proxy's CascadeEventsLike stage protocol reads them."""
        return tuple(hit.wire.value for hit in self.fired)

    @property
    def outcome_events(self) -> tuple[LedgerEvent, ...]:
        """Events the proxy must append; empty when the controller already appended them."""
        return () if self.emitted else self.events


@dataclass(frozen=True, slots=True)
class PendingEscalation:
    route_id: RouteId
    from_rung: Rung
    hits: tuple[WireHit, ...]


class CascadeController:
    """Process-local pending-escalation map; sticky state through the StateProvider port."""

    def __init__(
        self,
        bundle: ConfigBundle,
        state: StateProvider,
        *,
        registry: RungRegistry | None = None,
        ledger: LedgerPort | None = None,
        evaluator: TripwireEvaluator | None = None,
        trust: TrustPolicy | None = None,
        now: Any = None,
    ) -> None:
        self._bundle = bundle
        self._trust = trust or UNTRUSTED
        self._state = state
        self._registry = registry or RungRegistry(bundle.rungs)
        self._ledger = ledger
        self._evaluator = evaluator or TripwireEvaluator(bundle.tripwires, bundle.policy)
        self._now = now or (lambda: datetime.now(UTC))
        self._pending: dict[LineageId, PendingEscalation] = {}
        self._seq: dict[RouteId, itertools.count[int]] = {}
        self._verifier_consumed: dict[LineageId, int] = {}

    @classmethod
    def from_components(
        cls,
        *,
        bundle: ConfigBundle,
        settings: Settings,
        ledger: LedgerPort | None,
        state: StateProvider | None,
    ) -> CascadeController:
        """Build the controller from config; an absent state provider means process-local."""
        if state is None:
            log.warning("cascade_state_process_local", detail="sticky state lost on restart")
            state = MemoryStateProvider()
        return cls(
            bundle,
            state,
            registry=RungRegistry(bundle.rungs),
            ledger=ledger,
            evaluator=TripwireEvaluator(bundle.tripwires, bundle.policy),
            trust=load_trust_policy(settings.config_dir),
        )

    # events ----------------------------------------------------------------------------

    async def _seed_seq(self, route_id: RouteId) -> None:
        """Continue the producer sequence from the ledger so a restart never reuses a key."""
        if route_id in self._seq or not route_id:
            return
        start = 1
        if self._ledger is not None:
            try:
                stored = await self._ledger.read_events(route_id)
            except Exception as exc:
                log.warning("seq_seed_failed", error=type(exc).__name__)
                stored = []
            highest = max((e.producer_seq for e in stored if e.producer == PRODUCER), default=0)
            start = highest + 1
        self._seq[route_id] = itertools.count(start)

    def _event(self, route_id: RouteId, event_type: str, payload: Mapping[str, Any]) -> LedgerEvent:
        counter = self._seq.setdefault(route_id, itertools.count(1))
        return LedgerEvent(
            route_id=route_id,
            event_type=event_type,
            producer=PRODUCER,
            producer_seq=next(counter),
            payload=dict(payload),
        )

    def _outcome(
        self,
        ctx: RequestContext,
        route_id: RouteId,
        state: OutcomeState,
        payload: Mapping[str, Any],
    ) -> LedgerEvent:
        counter = self._seq.setdefault(route_id, itertools.count(1))
        return outcome_event(
            route_id,
            state,
            PRODUCER,
            next(counter),
            OutcomeFields(
                session_hmac=str(ctx.session_hmac),
                lineage_hmac=str(ctx.lineage_hmac),
                served_rung=payload.get("rung"),
                extra=payload,
            ),
        )

    async def _emit(self, events: list[LedgerEvent]) -> None:
        if self._ledger is None:
            return
        for event in events:
            stored = await self._ledger.append_event(event)
            if not stored:
                EVENT_DROPPED_TOTAL.labels(producer=PRODUCER).inc()
                log.warning(
                    "event_dropped",
                    route_id=str(event.route_id),
                    event_type=event.event_type,
                    producer_seq=event.producer_seq,
                )

    # plan ------------------------------------------------------------------------------

    async def plan(
        self, ctx: RequestContext, decision: Decision, gate: GateOutcome, sticky: StickyState | None
    ) -> DispatchPlan:
        events: list[LedgerEvent] = []
        boundary = assess_boundary(ctx.json)
        permitted = gate.permitted
        if sticky is not None:
            await self._seed_seq(sticky.route_id)
        await self._seed_seq(decision.route_id)
        if gate.block is not None or permitted.is_empty:
            block = gate.block or ErrorCode.PINNED_CLOUD_DENIED
            base = sticky or new_sticky(
                ctx.lineage_hmac, decision.route_id, decision.rung, previous=None
            )
            return DispatchPlan(
                base.rung,
                boundary.is_boundary,
                False,
                None,
                None,
                None,
                block,
                base,
                decision.route_id,
            )

        if ctx.is_subagent:
            plan = await self._plan_subagent(
                ctx, decision, gate, sticky, boundary.is_boundary, events
            )
            return replace(plan, pinned=gate.pinned)

        if ctx.request_class is RequestClass.USER_TURN:
            plan = await self._plan_user_turn(ctx, decision, gate, sticky, boundary, events)
        else:
            plan = await self._plan_inherit(ctx, decision, gate, sticky, boundary, events)
        await self._emit(events)
        return replace(plan, pinned=gate.pinned)

    async def _plan_user_turn(
        self,
        ctx: RequestContext,
        decision: Decision,
        gate: GateOutcome,
        sticky: StickyState | None,
        boundary: Any,
        events: list[LedgerEvent],
    ) -> DispatchPlan:
        permitted = gate.permitted
        if sticky is not None:
            events.append(
                self._outcome(
                    ctx,
                    sticky.route_id,
                    OutcomeState.CLOSED_TURN,
                    {
                        "reason": "next_user_turn",
                        "rung": sticky.rung.value,
                        "escalated": sticky.escalated,
                        "served_model": sticky.served_model,
                        "served_source": sticky.served_source,
                    },
                )
            )
            self._pending.pop(ctx.lineage_hmac, None)
        rung = decision.rung
        constrained = False
        if sticky is not None and sticky.escalated and sticky.rung > rung:
            rung = sticky.rung
        if rung not in permitted:
            highest = permitted.highest
            assert highest is not None
            constrained = True
            events.append(
                self._event(
                    decision.route_id,
                    POLICY_CONSTRAINT_EVENT,
                    {
                        "reason": "gate_precedes_stickiness",
                        "requested_rung": rung.value,
                        "served_rung": highest.value,
                    },
                )
            )
            rung = highest
        new = new_sticky(
            ctx.lineage_hmac,
            decision.route_id,
            rung,
            previous=sticky,
            escalated=bool(sticky and sticky.escalated and rung > decision.rung),
        )
        await self._state.set_sticky(new)
        events.append(
            self._outcome(
                ctx,
                decision.route_id,
                OutcomeState.PENDING,
                {"rung": rung.value, "decided_rung": decision.rung.value, "state_loss": False},
            )
        )
        return DispatchPlan(
            rung,
            True,
            False,
            None,
            None,
            None,
            None,
            new,
            decision.route_id,
            policy_constrained=constrained,
        )

    async def _plan_inherit(
        self,
        ctx: RequestContext,
        decision: Decision,
        gate: GateOutcome,
        sticky: StickyState | None,
        boundary: Any,
        events: list[LedgerEvent],
    ) -> DispatchPlan:
        permitted = gate.permitted
        state_loss = False
        if sticky is None:
            state_loss = ctx.request_class is RequestClass.CONTINUATION
            sticky = (
                mark_state_loss(
                    new_sticky(ctx.lineage_hmac, decision.route_id, decision.rung, previous=None)
                )
                if state_loss
                else new_sticky(ctx.lineage_hmac, decision.route_id, decision.rung, previous=None)
            )
            await self._state.set_sticky(sticky)
            events.append(
                self._outcome(
                    ctx,
                    decision.route_id,
                    OutcomeState.PENDING,
                    {
                        "rung": sticky.rung.value,
                        "decided_rung": decision.rung.value,
                        "state_loss": state_loss,
                        "request_class": ctx.request_class.value,
                    },
                )
            )
        rung = sticky.rung
        constrained = False
        if rung not in permitted:
            highest = permitted.highest
            assert highest is not None
            constrained = True
            events.append(
                self._event(
                    sticky.route_id,
                    POLICY_CONSTRAINT_EVENT,
                    {
                        "reason": "gate_precedes_stickiness",
                        "requested_rung": rung.value,
                        "served_rung": highest.value,
                    },
                )
            )
            rung = highest
            sticky = _retarget(sticky, rung)
            await self._state.set_sticky(sticky)
        if boundary.is_boundary and not gate.pinned:
            await self._ingest_verifier_signal(ctx, sticky, rung, events)
        pending = self._pending.get(ctx.lineage_hmac)
        if pending is not None and boundary.is_boundary and not gate.pinned:
            target = self._registry.next_higher(rung, permitted)
            if target is not None:
                return await self._escalate(ctx, sticky, pending, rung, target, events, state_loss)
        suppressed = (
            sticky.escalated
            and self._registry.family_for(rung) == "anthropic"
            and needs_thinking_suppression(ctx.json)
        )
        return DispatchPlan(
            rung,
            boundary.is_boundary,
            False,
            None,
            None,
            None,
            None,
            sticky,
            sticky.route_id,
            state_loss=state_loss,
            policy_constrained=constrained,
            thinking_suppressed=suppressed,
        )

    async def _ingest_verifier_signal(
        self, ctx: RequestContext, sticky: StickyState, rung: Rung, events: list[LedgerEvent]
    ) -> None:
        """Wire class (e): verifier failures recorded on the lineage arm an escalation."""
        if self._ledger is None:
            return
        try:
            signals = await self._ledger.read_lineage_events(
                ctx.lineage_hmac, VERIFIER_FAILED_EVENT
            )
        except Exception as exc:
            log.warning("verifier_signal_read_failed", error=type(exc).__name__)
            return
        consumed = self._verifier_consumed.get(ctx.lineage_hmac, 0)
        fresh = [s for s in signals if (s.seq or 0) > consumed]
        if not fresh:
            return
        self._verifier_consumed[ctx.lineage_hmac] = max((s.seq or 0) for s in fresh)
        hit = self._evaluator.verifier_failure(rung)
        if hit is None:
            return
        events.append(self._event(sticky.route_id, TRIPWIRE_EVENT, hit.as_record()))
        if ctx.lineage_hmac not in self._pending:
            self._pending[ctx.lineage_hmac] = PendingEscalation(sticky.route_id, rung, (hit,))

    async def _escalate(
        self,
        ctx: RequestContext,
        sticky: StickyState,
        pending: PendingEscalation,
        from_rung: Rung,
        to_rung: Rung,
        events: list[LedgerEvent],
        state_loss: bool,
    ) -> DispatchPlan:
        source_family = family_of_model(
            sticky.served_model, from_rung, self._registry.family_for(from_rung)
        )
        target_family = self._registry.family_for(to_rung)
        thinking = isinstance(ctx.json.get("thinking"), Mapping)
        source_has_thinking = latest_assistant_has_thinking(ctx.json)
        rule = self._bundle.provider_pairs.rule_for(
            source_family, target_family, thinking, source_has_thinking=source_has_thinking
        )
        side_effects = executed_side_effects_since_turn_start(ctx.json, trust=self._trust)
        verifier_result = None
        for hit in pending.hits:
            if hit.wire is WireClass.VERIFIER_FAILURE:
                verifier_result = VerificationResult.FAIL
        note = HandoffNote(
            cause=",".join(h.wire.value for h in pending.hits),
            from_rung=from_rung,
            to_rung=to_rung,
            executed_side_effects=side_effects,
            verifier_result=verifier_result,
        )
        result = transform(ctx.json, rule, note)
        new = escalate(sticky, to_rung)
        await self._state.set_sticky(new)
        self._pending.pop(ctx.lineage_hmac, None)
        events.append(
            self._event(
                sticky.route_id,
                ESCALATION_EVENT,
                {
                    "from_rung": from_rung.value,
                    "to_rung": to_rung.value,
                    "cause": note.cause,
                    "pair_rule": rule.model_dump(),
                    "handoff_schema": note.schema_version,
                    "side_effects_before_escalation": bool(side_effects),
                    "source_has_thinking": source_has_thinking,
                    "thinking_disabled_for_handoff": bool(thinking and result.thinking_disabled),
                    **result.as_record(),
                },
            )
        )
        log.info("escalation", from_rung=from_rung.value, to_rung=to_rung.value, cause=note.cause)
        return DispatchPlan(
            to_rung,
            True,
            True,
            from_rung,
            note,
            rule,
            None,
            new,
            sticky.route_id,
            transform=result,
            state_loss=state_loss,
            thinking_suppressed=bool(thinking and result.thinking_disabled),
        )

    async def _plan_subagent(
        self,
        ctx: RequestContext,
        decision: Decision,
        gate: GateOutcome,
        sticky: StickyState | None,
        is_boundary: bool,
        events: list[LedgerEvent],
    ) -> DispatchPlan:
        """SEM-006 interim: constrained passthrough at the requested model, pin inherited."""
        permitted = gate.permitted
        requested = self._registry.rung_for_model_name(ctx.requested_model)
        rung = (
            requested
            if requested is not None and requested in permitted
            else (
                permitted.highest
                if requested is None or requested > (permitted.highest or Rung.LOCAL)
                else permitted.lowest
            )
        )
        assert rung is not None
        if sticky is None:
            sticky = new_sticky(ctx.lineage_hmac, decision.route_id, rung, previous=None)
            await self._state.set_sticky(sticky)
        elif sticky.rung is not rung:
            sticky = _retarget(sticky, rung)
            await self._state.set_sticky(sticky)
        events.append(
            self._event(
                sticky.route_id,
                SUBAGENT_EVENT,
                {
                    "subagent": True,
                    "requested_model": ctx.requested_model,
                    "served_rung": rung.value,
                    "pinned": gate.pinned,
                    "agent_id_present": ctx.agent_id is not None,
                },
            )
        )
        await self._emit(events)
        return DispatchPlan(
            rung, is_boundary, False, None, None, None, None, sticky, sticky.route_id, subagent=True
        )

    # observe ---------------------------------------------------------------------------

    async def observe(
        self, ctx: RequestContext, plan: DispatchPlan, obs: ResponseObservation
    ) -> CascadeEvents:
        events: list[LedgerEvent] = []
        sticky = plan.sticky
        infra = False
        now = self._now()
        await self._seed_seq(sticky.route_id)
        if obs.status < 400 and obs.served is not None:
            sticky, changed = with_served(sticky, obs.served, now)
            if changed:
                infra = True
                events.append(
                    self._event(
                        sticky.route_id,
                        INFRASTRUCTURE_EVENT,
                        {
                            "reason": "within_rung_model_change",
                            "served_model": obs.served.model,
                            "previous_model": plan.sticky.served_model,
                            "cache_cold": True,
                        },
                    )
                )
            await self._state.set_sticky(sticky)
        if plan.subagent:
            await self._emit(events)
            return CascadeEvents((), tuple(events), sticky, infra, emitted=self._ledger is not None)
        if obs.status >= 400 or not obs.completed:
            return await self._observe_failure(ctx, plan, obs, sticky, events, infra)
        fired = (
            () if plan.escalated else self._evaluator.evaluate(ctx.json, plan.rung, observation=obs)
        )
        pending = False
        for hit in fired:
            events.append(self._event(sticky.route_id, TRIPWIRE_EVENT, hit.as_record()))
        if fired and not plan.pinned:
            higher = self._registry.next_higher(plan.rung, PermittedSet.all())
            if higher is not None:
                self._pending[ctx.lineage_hmac] = PendingEscalation(
                    sticky.route_id, plan.rung, fired
                )
                pending = True
        await self._emit(events)
        return CascadeEvents(
            fired, tuple(events), sticky, infra, pending, emitted=self._ledger is not None
        )

    async def _observe_failure(
        self,
        ctx: RequestContext,
        plan: DispatchPlan,
        obs: ResponseObservation,
        sticky: StickyState,
        events: list[LedgerEvent],
        infra: bool,
    ) -> CascadeEvents:
        candidates: list[FailureType] = []
        message = ""
        if obs.error and isinstance(obs.error.get("error"), Mapping):
            message = str(obs.error["error"].get("message", ""))
        if VENDOR_PROMPT_TOO_LONG_PHRASE in message.lower() or (
            "context" in message.lower() and "long" in message.lower()
        ):
            candidates.append(FailureType.CONTEXT_FEASIBILITY)
        if obs.status == 429 or obs.status >= 500 or not obs.completed:
            candidates.append(FailureType.INFRASTRUCTURE)
        if plan.policy_constrained:
            candidates.append(FailureType.POLICY_CONSTRAINT)
        if plan.sticky.served_source == "assumed_intended" and not candidates:
            candidates = [FailureType.UNVERIFIABLE]
        primary, secondary = resolve_primary(candidates)
        partial = obs.streamed_tool_content and not obs.completed
        code = ErrorCode.PARTIAL_STREAM_FAILURE if partial else ErrorCode.TERMINAL_FAILURE
        detail = f"failure_type={primary.value} rung={plan.rung.value} status={obs.status}"
        surfaced = render_error(code, detail)
        events.append(
            self._outcome(
                ctx,
                sticky.route_id,
                OutcomeState.CLOSED_TURN,
                {
                    "reason": "terminal_failure",
                    "failure_type": primary.value,
                    "secondary_type": secondary.value if secondary else None,
                    "rung": plan.rung.value,
                    "status": obs.status,
                    "partial_stream": partial,
                    "surfaced": True,
                    "gateway_attempts_observed": 1,
                    "served_source": sticky.served_source,
                },
            )
        )
        self._pending.pop(ctx.lineage_hmac, None)
        await self._emit(events)
        return CascadeEvents(
            (), tuple(events), sticky, infra, False, surfaced, primary, self._ledger is not None
        )

    # episode boundaries ----------------------------------------------------------------

    async def episode_boundary(
        self, lineage: LineageId, signal: EpisodeSignal
    ) -> StickyState | None:
        """Release only the escalation ratchet (ADRL-SEM-005); pins are never touched here."""
        sticky = await self._state.get_sticky(lineage)
        if sticky is None:
            return None
        released = release_ratchet(sticky, signal)
        await self._state.set_sticky(released)
        self._pending.pop(lineage, None)
        await self._emit(
            [
                self._event(
                    sticky.route_id,
                    BOUNDARY_CANDIDATE_EVENT,
                    {
                        "signal": signal.value,
                        "released": sticky.escalated,
                        "sticky": sticky_record(released),
                    },
                )
            ]
        )
        return released

    def pending_for(self, lineage: LineageId) -> PendingEscalation | None:
        return self._pending.get(lineage)


def _retarget(sticky: StickyState, rung: Rung) -> StickyState:
    return StickyState(
        lineage_hmac=sticky.lineage_hmac,
        route_id=sticky.route_id,
        rung=rung,
        escalated=sticky.escalated,
        served_model=None,
        served_provider=None,
        served_source="assumed_intended",
        turn_index=sticky.turn_index,
        last_served_at=None,
        state_loss=sticky.state_loss,
    )

FILE /Users/arunmenon/projects/adrl-core/src/adrl/proxy/pipeline.py
"""The per-request pipeline. Primary: ADRL-FND-003.
Also implements: ADRL-TRU-002 (register additions of 2026-09-03).

Secondary: ADRL-FND-001 (byte-exact relay), ADRL-FND-004 (fail-open by class and pin state),
ADRL-SAF-001 (gates on every class), ADRL-SAF-009 (egress write-ahead), ADRL-SEM-003
(continuations inherit), ADRL-SEM-004 (utility on pinned lineages), ADRL-SEM-006 (pin
inheritance materialised per lineage), ADRL-CAS-006 (served identity recorded),
ADRL-MEM-001/002 (forwarded outcome identity).

Order per request: parse, identity, pin lookup, classify, gate, sticky lookup, route-or-inherit,
cascade plan, egress write-ahead, ledger decision (write-through), dispatch once, relay while
observing, cascade observe, ledger events (write-behind). The per-lineage lock is held from the
gate through the decision write and again briefly when the response has been observed.
"""

from __future__ import annotations

import asyncio
import dataclasses
import hashlib
import hmac
import json
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

import structlog

from adrl.config.checks import check_live_rung_has_evidence
from adrl.config.loaders import ConfigBundle
from adrl.config.settings import Settings
from adrl.core.enums import FailureClass, GateMode, RequestClass, RoutingMode, Rung, UtilityKind
from adrl.core.errors import VENDOR_PROMPT_TOO_LONG_PHRASE, ErrorCode, LedgerAppendFailure
from adrl.core.ids import LineageId, RouteId
from adrl.core.ports import EgressEvent, LineageEvent, StateProvider, StickyState, Tokenizer
from adrl.core.types import (
    Decision,
    DeploymentInfo,
    DeploymentSet,
    Finding,
    GateVerdict,
    LedgerEvent,
    PermittedSet,
    RequestContext,
)
from adrl.gates.deployments import DeploymentPolicy, egress_fields
from adrl.ledger.egress import EgressLedger
from adrl.ledger.facade import PIN_EVENT, MemoryFacade
from adrl.proxy.claude_experiment import ClaudeExperimentClient
from adrl.proxy.errors import (
    JSON_HEADERS,
    block_message,
)
from adrl.proxy.fallback import FailureResolution, FallbackAction, FallbackRecorder, resolve_failure
from adrl.proxy.observe_only import ObserveOnlyGateOutcome
from adrl.proxy.stages import (
    CascadeStage,
    DispatchPlanLike,
    GateOutcomeLike,
    GateStage,
    RouteStage,
    TranscriptTransform,
)
from adrl.proxy.upstream import HttpxGatewayClient, UpstreamUnreachableError, read_all, relay
from adrl.telemetry.logging import bind_request
from adrl.telemetry.metrics import (
    EVENT_DROPPED_TOTAL,
    GATE_LATENCY_SECONDS,
    LEDGER_DEGRADED_TOTAL,
    REQUESTS_TOTAL,
)
from adrl.wire.adapters import ClaudeCodeAdapter, HarnessAdapter, IdentitySignals
from adrl.wire.classify import Classification, UnclassifiableError
from adrl.wire.identity import Identity, IdentityResolver, LineageLocks
from adrl.wire.observe import ResponseObservation
from adrl.wire.parse import (
    forward_headers,
    parse_request,
    response_headers,
)
from adrl.wire.profiles.base import ProtocolProfile, ProtocolResponse, RequestView
from adrl.wire.profiles.messages import MessagesProfile

log = structlog.get_logger(__name__)

PRODUCER = "proxy"
INHERITED_ESTIMATOR = "inherited"
INHERITED_ESTIMATOR_VERSION = "sticky-v1"
FALLBACK_ESTIMATOR = "fail_open"
FALLBACK_ESTIMATOR_VERSION = "fnd-004-v1"
AGENT_PARENT_EVENT = "agent_parent"
ALLOWLISTED_ERROR_PHRASES: tuple[str, ...] = (
    VENDOR_PROMPT_TOO_LONG_PHRASE,
    "prompt is too long",
    "rate limit",
    "overloaded",
    "thinking",
    "context",
    "invalid_request",
)


def _content_free_error(error: Mapping[str, Any], status: int, key: bytes) -> dict[str, Any]:
    """Record an upstream error without its wording (ADRL-SAF-009, MEM-005).

    Vendor validation errors quote prompt fragments; only the error type, the status, a keyed
    hash and length of the message, and an allow-listed phrase match are kept.
    """
    inner = error.get("error", error)
    inner_map = inner if isinstance(inner, Mapping) else {}
    message = str(inner_map.get("message", ""))
    lowered = message.lower()
    phrase = next((p for p in ALLOWLISTED_ERROR_PHRASES if p in lowered), None)
    return {
        "type": inner_map.get("type"),
        "status": status,
        "message_hmac": hmac.new(key, message.encode("utf-8"), hashlib.sha256).hexdigest()[:32],
        "message_length": len(message),
        "phrase": phrase,
    }


Finalizer = Callable[[], Awaitable[None]]


@dataclass
class ProxyResponse:
    status: int
    headers: dict[str, str]
    body: bytes | None = None
    stream: AsyncIterator[bytes] | None = None
    after: Finalizer | None = None
    route_id: str | None = None

    @property
    def is_stream(self) -> bool:
        return self.stream is not None


@dataclass(frozen=True, slots=True)
class _Turn:
    ctx: RequestContext
    gate: GateOutcomeLike
    decision: Decision
    plan: DispatchPlanLike
    target_rung: Rung
    body: bytes
    fresh_decision: bool
    state_loss: bool
    resolution: FailureResolution | None
    ledger_degraded: bool
    forward_original: bool
    deployment: DeploymentInfo | None = None


@dataclass
class _RouteSeq:
    """Per-route producer sequence continued from the ledger (ADRL-MEM-001 idempotency).

    The key (route_id, event_type, producer, producer_seq) must never be reused, so the first
    event for a route_id in this process starts after the highest sequence already stored.
    """

    counters: dict[str, int] = field(default_factory=dict)

    async def next(self, ledger: MemoryFacade, route_id: str) -> int:
        if route_id not in self.counters:
            try:
                stored = await ledger.read_events(RouteId(route_id))
            except Exception:
                stored = []
            self.counters[route_id] = max(
                (e.producer_seq for e in stored if e.producer == PRODUCER), default=0
            )
        self.counters[route_id] += 1
        return self.counters[route_id]


class Pipeline:
    def __init__(
        self,
        *,
        settings: Settings,
        bundle: ConfigBundle,
        ledger: MemoryFacade,
        egress: EgressLedger | None,
        gateway: HttpxGatewayClient,
        gate: GateStage,
        router: RouteStage,
        cascade: CascadeStage,
        state: StateProvider | None,
        identity: IdentityResolver,
        locks: LineageLocks | None = None,
        transcript_transform: TranscriptTransform | None = None,
        tokenizer: Tokenizer | None = None,
        profile: ProtocolProfile | None = None,
        adapter: HarnessAdapter | None = None,
    ) -> None:
        self._settings = settings
        self._bundle = bundle
        self._ledger = ledger
        self._egress = egress
        self._gateway = gateway
        self._claude_experiment = gateway if isinstance(gateway, ClaudeExperimentClient) else None
        if self._claude_experiment is not None:
            if (
                settings.routing_mode is not RoutingMode.LIVE
                or settings.gate_mode is not GateMode.ENFORCE
            ):
                raise ValueError(
                    "Claude experiment requires explicit LIVE routing and enforcing gates"
                )
            if not check_live_rung_has_evidence(bundle, settings).ok:
                raise ValueError("Claude experiment cannot bypass LIVE admission")
        self._gate = gate
        self._router = router
        self._cascade = cascade
        self._state = state
        self._identity = identity
        self._locks = locks or LineageLocks()
        self._transform = transcript_transform
        self._tokenizer = tokenizer
        self._profile: ProtocolProfile = profile or MessagesProfile()
        self._adapter: HarnessAdapter = adapter or ClaudeCodeAdapter()
        self._recorder = FallbackRecorder(ledger, egress, deployment_tag=settings.deployment_tag)
        self._deployments = DeploymentPolicy(bundle.endpoint_inventory)
        self._seq = _RouteSeq()
        self._background: set[asyncio.Task[Any]] = set()
        self._persisted_parents: set[tuple[str, str]] = set()

    # ------------------------------------------------------------------ public entry point

    async def handle(
        self,
        method: str,
        path: str,
        headers: Mapping[str, str],
        body: bytes,
        peer: tuple[str, int] | None,
        *,
        query: str = "",
    ) -> ProxyResponse:
        if self._claude_experiment is not None and query:
            return self._error_response(
                ErrorCode.CAPABILITY_REJECTED, "experiment query not admitted"
            )
        if not self._profile.handles(method, path, headers):
            return await self._forward_non_api(parse_request(method, path, headers, body, query))
        parsed = self._profile.parse(method, path, headers, body, query)
        signals = self._adapter.identity_signals(parsed)
        is_pre_warm = self._profile.is_pre_warm(parsed)
        root = await self._prime_parents(signals, peer, is_pre_warm=is_pre_warm)
        identity = self._identity.resolve_signals(signals, peer, is_pre_warm=is_pre_warm)
        await self._persist_parent(identity, root)

        # Pin lookup and classification run under the per-lineage lock so a request racing the
        # pinning request resolves its gate failure against the pinned state (ADRL-FND-004).
        lock = self._locks.get(identity.lineage_hmac)
        async with lock:
            pinned_before = await self._effective_pin(identity)
            try:
                classification = self._profile.classify(
                    parsed,
                    self._bundle.utility_fingerprints,
                    pinned=self._enforcing and pinned_before,
                )
            except UnclassifiableError as exc:
                return self._error_response(exc.code, exc.detail)
            ctx = self._context(parsed, identity, classification)
            bind_request(lineage=ctx.lineage_hmac, request_class=ctx.request_class.value)
            prepared = await self._prepare(ctx, classification, pinned_before)
        if isinstance(prepared, ProxyResponse):
            return prepared
        return await self._dispatch(prepared)

    async def _prime_parents(
        self, signals: IdentitySignals, peer: tuple[str, int] | None, *, is_pre_warm: bool
    ) -> LineageId | None:
        """Rebuild the agent chain from persisted parent links after a restart (ADRL-SEM-006)."""
        if not signals.agent_id:
            return None
        root = self._identity.session_root_from_signals(signals, peer, is_pre_warm=is_pre_warm)
        if self._identity.needs_priming(root):
            try:
                events = await self._ledger.read_lineage_events(root, AGENT_PARENT_EVENT)
            except Exception as exc:
                log.warning("agent_parent_read_failed", error=type(exc).__name__)
                events = []
            self._identity.prime_parents(
                root,
                [
                    (str(e.payload.get("agent_id", "")), str(e.payload.get("parent_agent_id", "")))
                    for e in events
                ],
            )
        return root

    async def _persist_parent(self, identity: Identity, root: LineageId | None) -> None:
        if root is None or identity.agent_id is None or identity.parent_agent_id is None:
            return
        pair = (identity.agent_id, identity.parent_agent_id)
        if pair in self._persisted_parents:
            return
        self._persisted_parents.add(pair)
        try:
            await self._ledger.append_lineage_event(
                LineageEvent(
                    lineage_hmac=root,
                    event_type=AGENT_PARENT_EVENT,
                    payload={"agent_id": pair[0], "parent_agent_id": pair[1]},
                )
            )
        except Exception as exc:
            log.warning("agent_parent_persist_failed", error=type(exc).__name__)

    async def drain(self) -> None:
        """Wait for write-behind ledger work; used by tests and shutdown."""
        if self._background:
            await asyncio.gather(*list(self._background), return_exceptions=True)

    # ------------------------------------------------------------------ preparation under lock

    async def _prepare(
        self, ctx: RequestContext, classification: Classification, pinned_before: bool
    ) -> _Turn | ProxyResponse:
        gate, gate_resolution = await self._run_gate(ctx, pinned_before)
        if isinstance(gate, ProxyResponse):
            return gate
        pinned = self._enforcing and gate.pinned

        if gate.block is not None and self._enforcing:
            return await self._blocked(ctx, gate, gate.block)

        if ctx.request_class is RequestClass.UTILITY and pinned:
            serve_empty = bool(getattr(gate, "serve_empty_utility", False))
            if ctx.utility_kind is UtilityKind.COSMETIC and (
                serve_empty or Rung.LOCAL not in gate.permitted
            ):
                await self._record_egress(ctx, gate, None, 0, kind="empty_utility")
                return self._protocol_response(self._profile.empty_utility(ctx))

        if pinned and gate.permitted.is_empty:
            return await self._blocked(ctx, gate, ErrorCode.PINNED_CLOUD_DENIED)

        if ctx.request_class is RequestClass.PASSTHROUGH and self._profile.is_token_count(ctx.path):
            if pinned or bool(getattr(gate, "serve_local_estimate", False)):
                return await self._count_tokens_locally(ctx, gate)

        sticky, sticky_failure = await self._sticky(ctx)
        state_loss = sticky is None and classification.inherits_route
        resolution = gate_resolution or sticky_failure

        decision: Decision | None = None
        fresh = (
            classification.is_routed
            or (classification.request_class is RequestClass.SUBAGENT)
            or sticky is None
        )
        if resolution is None:
            if fresh:
                try:
                    decision = await self._router.decide(ctx, gate, sticky)
                except Exception as exc:
                    resolution = resolve_failure(
                        FailureClass.ROUTING_PATH, pinned=pinned, mode=self._settings.fallback_mode
                    )
                    await self._recorder.record(ctx, resolution, exception=exc)
            else:
                assert sticky is not None
                decision = self._inherited_decision(ctx, gate, sticky)
        if resolution is not None and resolution.action in (
            FallbackAction.BLOCK,
            FallbackAction.SURFACE,
        ):
            return self._error_response(
                resolution.code or ErrorCode.TERMINAL_FAILURE,
                f"{resolution.failure_class.value} failure; last-known-safe is to refuse",
            )
        if decision is None:
            assert resolution is not None
            decision = self._fallback_decision(ctx, gate, resolution)

        try:
            plan = await self._cascade.plan(ctx, decision, gate, sticky)
        except Exception as exc:
            plan_resolution = resolve_failure(
                FailureClass.ROUTING_PATH, pinned=pinned, mode=self._settings.fallback_mode
            )
            await self._recorder.record(ctx, plan_resolution, exception=exc)
            if plan_resolution.action in (FallbackAction.BLOCK, FallbackAction.SURFACE):
                return self._error_response(
                    plan_resolution.code or ErrorCode.TERMINAL_FAILURE, "cascade stage failed"
                )
            resolution = plan_resolution
            decision = self._fallback_decision(ctx, gate, plan_resolution)
            plan = _FallbackPlan.for_decision(
                ctx, decision, sticky, is_boundary=self._profile.is_action_boundary(ctx.json)
            )
        if plan.block is not None and self._enforcing:
            return await self._blocked(ctx, gate, plan.block)

        target_rung, forward_original = self._target(ctx, gate, plan, resolution)
        if pinned and target_rung is not Rung.LOCAL:
            return await self._blocked(ctx, gate, ErrorCode.PINNED_CLOUD_DENIED)
        deployment, deployment_block = self._choose_deployment(
            ctx, gate, target_rung, forward_original
        )
        if deployment_block is not None:
            return await self._blocked(ctx, gate, deployment_block)
        plan = _with_deployment(plan, deployment, forward_original)

        body = self._body_for(ctx, plan, target_rung, forward_original, deployment)
        if self._claude_experiment is not None:
            # Do not force a cloud model after fallback, pinning or an escalated transform.
            permitted = getattr(gate, "permitted_deployments", None)
            if (
                resolution is not None
                or pinned
                or target_rung is not Rung.FRONTIER
                or not forward_original
                or permitted is None
            ):
                return await self._blocked(ctx, gate, ErrorCode.CAPABILITY_REJECTED)
            try:
                body, deployment = self._claude_experiment.selection.prepare(
                    ctx.body, lineage=str(ctx.lineage_hmac), permitted=permitted, pinned=pinned
                )
            except ValueError:
                return await self._blocked(ctx, gate, ErrorCode.CAPABILITY_REJECTED)
            if self._deployments.catalog.get(deployment.deployment_id) != deployment:
                return await self._blocked(ctx, gate, ErrorCode.CAPABILITY_REJECTED)
            decision = dataclasses.replace(
                decision,
                estimator="experiment_forced_claude",
                estimator_version=self._claude_experiment.config.version,
                features={
                    **decision.features,
                    "experiment_config_hash": self._claude_experiment.config.fingerprint,
                    "experiment_model": deployment.model,
                },
            )
            forward_original = False
            plan = _with_deployment(plan, deployment, False)
        ledger_degraded = await self._record_egress(
            ctx, gate, target_rung, len(body), deployment=deployment, receipt_source="intended"
        )
        if ledger_degraded is None:
            return await self._blocked(ctx, gate, ErrorCode.EGRESS_LEDGER_UNAVAILABLE)

        if fresh and resolution is None:
            await self._ledger.append_decision(
                decision, self._decision_context(ctx, gate, state_loss)
            )
        if self._state is not None:
            try:
                await self._state.set_sticky(plan.sticky)
            except Exception as exc:
                log.warning("sticky_write_failed", error=str(exc))
        self._write_behind(
            ctx,
            decision.route_id,
            "request",
            {
                "request_class": ctx.request_class.value,
                "target_rung": target_rung.value,
                "deployment_id": deployment.deployment_id if deployment else None,
                "decided_rung": decision.rung.value,
                "is_boundary": plan.is_boundary,
                "escalated": plan.escalated,
                "forward_original": forward_original,
                "unscanned": gate.unscanned,
                "pinned": gate.pinned,
                "fail_open": resolution.failure_class.value if resolution else None,
                "state_loss": state_loss,
                "routing_mode": self._settings.routing_mode.value,
                "experiment_config_hash": (
                    self._claude_experiment.config.fingerprint if self._claude_experiment else None
                ),
                "experiment_selected_model": deployment.model
                if self._claude_experiment and deployment
                else None,
            },
        )
        return _Turn(
            ctx=ctx,
            gate=gate,
            decision=decision,
            plan=plan,
            target_rung=target_rung,
            body=body,
            fresh_decision=fresh,
            state_loss=state_loss,
            resolution=resolution,
            ledger_degraded=ledger_degraded,
            forward_original=forward_original,
            deployment=deployment,
        )

    def _choose_deployment(
        self,
        ctx: RequestContext,
        gate: GateOutcomeLike,
        rung: Rung,
        forward_original: bool,
    ) -> tuple[DeploymentInfo | None, ErrorCode | None]:
        """Pick the attested deployment for the rung inside the permitted set (ADRL-SAF-008).

        A rung label never reaches the gateway on its own: the alias sent is the deployment id.
        A pinned lineage may only reach a ``local_host`` deployment, whatever the label says.
        """
        policy = self._deployments
        permitted = getattr(gate, "permitted_deployments", None)
        if permitted is None:
            permitted = policy.permitted_for(
                permitted_rungs=gate.permitted.rungs,
                pinned=self._enforcing and gate.pinned,
                residency=gate.residency,
            )
        if forward_original and rung not in permitted.rungs():
            # Routing is not live: the rung ceiling is advisory here (the harness's own model
            # is forwarded), but the pin and residency still bind at the deployment level.
            log.info("rung_ceiling_advisory_passthrough", rung=rung.value)
            permitted = policy.permitted_for(
                permitted_rungs=frozenset(Rung),
                pinned=self._enforcing and gate.pinned,
                residency=gate.residency,
            )
        if not self._enforcing and permitted.is_empty:
            log.warning("deployment_set_empty_observe_mode", rung=rung.value)
            permitted = policy.universe()
        if forward_original:
            deployment = policy.frontier_for_model(permitted, ctx.requested_model)
        else:
            spec = self._bundle.rungs.rungs.get(rung)
            members = spec.members if spec is not None else ()
            deployment = policy.choose(permitted, rung, rung_member_order=tuple(members))
        if deployment is None:
            if self._enforcing and gate.pinned:
                return None, ErrorCode.PINNED_CLOUD_DENIED
            log.warning(
                "no_permitted_deployment",
                rung=rung.value,
                residency=gate.residency,
                permitted=permitted.as_list(),
            )
            return None, ErrorCode.CAPABILITY_REJECTED
        if self._enforcing and gate.pinned and not deployment.is_local_host:
            log.error(
                "pinned_lineage_non_local_deployment",
                deployment=deployment.deployment_id,
                trust_zone=deployment.trust_zone,
            )
            return None, ErrorCode.PINNED_CLOUD_DENIED
        return deployment, None

    def _with_receipt(
        self, turn: _Turn, obs: ResponseObservation, headers: Mapping[str, str]
    ) -> ResponseObservation:
        """Attach the gateway's destination receipt to the observation (ADRL-RTG-008)."""
        if self._claude_experiment is not None:
            served = dataclasses.replace(
                obs.served,
                provider="anthropic",
                api_base_host="api.anthropic.com",
                deployment_id=None,
                trust_zone=None,
                geo=None,
            )
            if served.model != self._claude_experiment.config.target_model:
                self._claude_experiment.stopped = True
            return dataclasses.replace(obs, served=served)
        served = self._deployments.served_identity(obs.served, headers, turn.deployment)
        return dataclasses.replace(obs, served=served)

    # ------------------------------------------------------------------ dispatch and relay

    async def _dispatch(self, turn: _Turn) -> ProxyResponse:
        ctx = turn.ctx
        headers = forward_headers(ctx.headers)
        headers["content-type"] = "application/json"
        try:
            response = await self._gateway.send(
                turn.body, headers, path=ctx.path, rung=turn.target_rung
            )
        except UpstreamUnreachableError as exc:
            self._write_behind(
                ctx,
                turn.decision.route_id,
                "upstream_unreachable",
                {"rung": turn.target_rung.value, "error": type(exc).__name__},
            )
            return self._error_response(
                ErrorCode.TERMINAL_FAILURE, str(exc), turn.decision.route_id
            )

        status = response.status_code
        out_headers = response_headers(response.headers)
        observer = self._profile.stream_observer(
            status=status,
            headers={} if self._claude_experiment else response.headers,
            intended_rung=turn.target_rung,
            requested_model=ctx.requested_model,
            rungs=self._bundle.rungs,
            hash_key=self._identity.hmac_key,
        )
        content_type = str(response.headers.get("content-type", "")).lower()
        if status >= 400 or not ctx.is_stream or "text/event-stream" not in content_type:
            raw = await read_all(response)
            obs = self._profile.observe_response(
                raw,
                status=status,
                headers={} if self._claude_experiment else response.headers,
                intended_rung=turn.target_rung,
                requested_model=ctx.requested_model,
                rungs=self._bundle.rungs,
                hash_key=self._identity.hmac_key,
            )
            obs = self._with_receipt(turn, obs, response.headers)
            await self._finalize(turn, obs)
            return ProxyResponse(
                status=status, headers=out_headers, body=raw, route_id=turn.decision.route_id
            )

        response_headers_snapshot = dict(response.headers)

        async def after() -> None:
            await self._finalize(
                turn, self._with_receipt(turn, observer.finish(), response_headers_snapshot)
            )

        return ProxyResponse(
            status=status,
            headers=out_headers,
            stream=relay(response, observer),
            after=after,
            route_id=turn.decision.route_id,
        )

    async def _finalize(self, turn: _Turn, obs: ResponseObservation) -> None:
        ctx = turn.ctx
        REQUESTS_TOTAL.labels(
            request_class=ctx.request_class.value, rung=obs.served.rung.value
        ).inc()
        lock = self._locks.get(ctx.lineage_hmac)
        try:
            async with lock:
                events = await self._cascade.observe(ctx, turn.plan, obs)
                if self._state is not None and events.sticky is not None:
                    await self._state.set_sticky(events.sticky)
                payload: dict[str, Any] = {
                    "status": obs.status,
                    "served_rung": obs.served.rung.value,
                    "served_model": obs.served.model,
                    "served_provider": obs.served.provider,
                    "served_source": obs.served.source.value,
                    "served_deployment_id": obs.served.deployment_id,
                    "served_trust_zone": obs.served.trust_zone,
                    "served_geo": obs.served.geo,
                    "receipt_confirmed": obs.served.receipt_confirmed,
                    "intended_rung": turn.target_rung.value,
                    "intended_deployment_id": (
                        turn.deployment.deployment_id if turn.deployment else None
                    ),
                    "stop_reason": obs.stop_reason,
                    "streamed_tool_content": obs.streamed_tool_content,
                    "completed": obs.completed,
                    "malformed_tool_json": obs.malformed_tool_json,
                    "tool_uses": [dataclasses.asdict(t) for t in obs.tool_uses],
                    "bytes_relayed": obs.bytes_relayed,
                    "fired_wires": list(events.fired_wires),
                }
                if obs.usage is not None:
                    payload["usage"] = {
                        "input_tokens": obs.usage.input_tokens,
                        "output_tokens": obs.usage.output_tokens,
                        "cache_read_input_tokens": obs.usage.cache_read_input_tokens,
                        "cache_creation_input_tokens": obs.usage.cache_creation_input_tokens,
                    }
                if obs.error is not None:
                    payload["error"] = _content_free_error(
                        obs.error, obs.status, self._identity.hmac_key
                    )
                event_type = "upstream_error" if obs.status >= 400 else "served"
                await self._append_event(ctx, turn.decision.route_id, event_type, payload)
                await self._record_receipt(turn, obs)
                for outcome_event in events.outcome_events:
                    # Preserve the cascade's route and idempotency identity on continuations.
                    if not isinstance(outcome_event, LedgerEvent):
                        raise TypeError("cascade must return LedgerEvent instances")
                    if not await self._ledger.append_event(outcome_event):
                        EVENT_DROPPED_TOTAL.labels(producer=outcome_event.producer).inc()
                        log.warning(
                            "event_dropped",
                            route_id=outcome_event.route_id,
                            event_type=outcome_event.event_type,
                            producer=outcome_event.producer,
                            producer_seq=outcome_event.producer_seq,
                        )
        except Exception as exc:
            log.error("finalize_failed", error=str(exc), route_id=turn.decision.route_id)

    # ------------------------------------------------------------------ helpers

    @property
    def _enforcing(self) -> bool:
        return self._settings.gate_mode is GateMode.ENFORCE

    def _context(
        self, parsed: RequestView, identity: Identity, classification: Classification
    ) -> RequestContext:
        return RequestContext(
            body=parsed.body,
            json=parsed.json,
            headers=parsed.headers,
            path=parsed.path,
            request_class=classification.request_class,
            content_bearing=classification.content_bearing,
            interaction_mode=classification.interaction_mode,
            session_hmac=identity.session_hmac,
            lineage_hmac=identity.lineage_hmac,
            requested_model=parsed.requested_model,
            is_stream=parsed.is_stream,
            max_tokens=parsed.max_tokens,
            agent_id=identity.agent_id,
            parent_agent_id=identity.parent_agent_id,
            utility_kind=classification.utility_kind,
            session_key_source=identity.source,
            fingerprint_id=classification.fingerprint_id,
            protocol_profile_id=self._profile.profile_id,
            protocol_profile_version=self._profile.version,
            harness_adapter_id=self._adapter.adapter_id,
            harness_adapter_version=self._adapter.version,
        )

    async def _effective_pin(self, identity: Identity) -> bool:
        """Own pin, or an ancestor's, materialised as an inherited pin event (ADRL-SEM-006)."""
        own = await self._ledger.pin_state(identity.lineage_hmac)
        if own.effective_pinned:
            return True
        for ancestor in identity.ancestor_lineages:
            state = await self._ledger.pin_state(ancestor)
            if state.effective_pinned:
                await self._ledger.append_lineage_event(
                    LineageEvent(
                        lineage_hmac=identity.lineage_hmac,
                        event_type=PIN_EVENT,
                        payload={
                            "finding_id": f"inherited:{ancestor}",
                            "detector_id": "inherited",
                            "inherited_from": ancestor,
                        },
                    )
                )
                return True
        return False

    async def _run_gate(
        self, ctx: RequestContext, pinned_before: bool
    ) -> tuple[GateOutcomeLike | ProxyResponse, FailureResolution | None]:
        try:
            gate = await self._gate.evaluate(ctx)
        except Exception as exc:
            resolution = resolve_failure(
                FailureClass.GATE_PATH, pinned=pinned_before, mode=self._settings.fallback_mode
            )
            await self._recorder.record(ctx, resolution, exception=exc)
            if resolution.action in (FallbackAction.BLOCK, FallbackAction.SURFACE):
                return (
                    self._error_response(
                        resolution.code or ErrorCode.GATE_UNAVAILABLE,
                        "gate unavailable on a pinned lineage; failing closed",
                    ),
                    resolution,
                )
            synthetic = ObserveOnlyGateOutcome(
                permitted=resolution.permitted,
                verdicts=(
                    GateVerdict(
                        gate="fail_open",
                        permitted_after=resolution.permitted,
                        unscanned=True,
                        reason=type(exc).__name__,
                        pinned=pinned_before,
                    ),
                ),
                pinned=pinned_before,
                unscanned=True,
                findings=(),
                block=None,
                repo_class=None,
                residency=None,
                latency_s=0.0,
            )
            return synthetic, resolution
        GATE_LATENCY_SECONDS.labels(request_class=ctx.request_class.value).observe(gate.latency_s)
        if pinned_before and not gate.pinned:
            # The gate never sees an inherited pin; the pipeline owns lineage inheritance.
            gate = _PinnedOverlay(gate)
        return gate, None

    async def _sticky(
        self, ctx: RequestContext
    ) -> tuple[StickyState | None, FailureResolution | None]:
        if self._state is None:
            return None, None
        try:
            return await self._state.get_sticky(ctx.lineage_hmac), None
        except Exception as exc:
            resolution = resolve_failure(
                FailureClass.ROUTING_PATH,
                pinned=await self._pin_flag(ctx),
                mode=self._settings.fallback_mode,
            )
            await self._recorder.record(ctx, resolution, exception=exc)
            return None, resolution

    async def _pin_flag(self, ctx: RequestContext) -> bool:
        return (await self._ledger.pin_state(ctx.lineage_hmac)).effective_pinned

    def _inherited_decision(
        self, ctx: RequestContext, gate: GateOutcomeLike, sticky: StickyState
    ) -> Decision:
        rung = sticky.rung
        reason = "inherited"
        if rung not in gate.permitted:
            highest = gate.permitted.highest
            rung = highest if highest is not None else Rung.LOCAL
            reason = "inherited_tightened"
        return Decision(
            route_id=sticky.route_id,
            rung=rung,
            permitted=gate.permitted,
            estimator=INHERITED_ESTIMATOR,
            estimator_version=INHERITED_ESTIMATOR_VERSION,
            policy_version=self._bundle.policy.version,
            objective_version=self._bundle.policy.objective_version,
            cascade_feasible=False,
            cascade_reason=reason,
            features={"request_class": ctx.request_class.value},
            features_version="features-inherited-v1",
        )

    def _fallback_decision(
        self, ctx: RequestContext, gate: GateOutcomeLike, resolution: FailureResolution
    ) -> Decision:
        from adrl.core.ids import mint_route_id

        rung = Rung.LOCAL if resolution.action is FallbackAction.FORWARD_LOCAL else Rung.FRONTIER
        return Decision(
            route_id=mint_route_id(),
            rung=rung,
            permitted=resolution.permitted,
            estimator=FALLBACK_ESTIMATOR,
            estimator_version=FALLBACK_ESTIMATOR_VERSION,
            policy_version=self._bundle.policy.version,
            objective_version=self._bundle.policy.objective_version,
            cascade_feasible=False,
            cascade_reason=resolution.failure_class.value,
            features={"request_class": ctx.request_class.value},
            features_version="features-fallback-v1",
        )

    def _target(
        self,
        ctx: RequestContext,
        gate: GateOutcomeLike,
        plan: DispatchPlanLike,
        resolution: FailureResolution | None,
    ) -> tuple[Rung, bool]:
        """Effective destination and whether the original bytes are forwarded."""
        pinned = self._enforcing and gate.pinned
        if resolution is not None:
            if resolution.action is FallbackAction.FORWARD_LOCAL:
                return Rung.LOCAL, False
            return Rung.FRONTIER, True
        if self._settings.routing_mode is RoutingMode.LIVE:
            rung = plan.rung
            suppressed = bool(getattr(plan, "thinking_suppressed", False))
            original = rung is Rung.FRONTIER and not plan.escalated and not suppressed
            return rung, original
        if pinned:
            return Rung.LOCAL, False
        return Rung.FRONTIER, True

    def _body_for(
        self,
        ctx: RequestContext,
        plan: DispatchPlanLike,
        rung: Rung,
        forward_original: bool,
        deployment: DeploymentInfo | None = None,
    ) -> bytes:
        if forward_original:
            return ctx.body
        body: dict[str, Any] = dict(ctx.json)
        if plan.escalated and self._transform is not None:
            body = self._transform(body, plan.pair_rule, plan.handoff)
        alias = (
            deployment.deployment_id
            if deployment is not None
            else self._bundle.rungs.alias_for(rung)
        )
        return self._profile.serialize(
            body,
            rung=rung,
            alias=alias,
            bundle=self._bundle,
            suppress_thinking=bool(getattr(plan, "thinking_suppressed", False)),
        )

    async def _record_egress(
        self,
        ctx: RequestContext,
        gate: GateOutcomeLike,
        rung: Rung | None,
        bytes_out: int,
        *,
        kind: str = "forward",
        deployment: DeploymentInfo | None = None,
        receipt_source: str | None = None,
    ) -> bool | None:
        """Write-ahead egress record. Returns degraded flag, or None when a pinned append failed."""
        if self._egress is None:
            return False
        findings: tuple[Finding, ...] = tuple(gate.findings)
        tier = findings[0].tier.value if findings else None
        try:
            self._egress.append(
                EgressEvent(
                    lineage_hmac=ctx.lineage_hmac,
                    request_class=ctx.request_class.value,
                    content_bearing=ctx.content_bearing,
                    destination_rung=rung.value if rung is not None else None,
                    deployment_tag=self._settings.deployment_tag,
                    gate_verdicts=[v.as_record() for v in gate.verdicts],
                    detector_tier=tier,
                    span_hashes=[f.span_hash for f in findings],
                    bytes_out=bytes_out,
                    actor="adrl",
                    reason=None,
                    event_kind=kind,
                    **egress_fields(deployment, receipt_source or "intended"),
                )
            )
        except LedgerAppendFailure as exc:
            if self._enforcing and gate.pinned:
                log.error("egress_append_failed_pinned", error=str(exc))
                return None
            LEDGER_DEGRADED_TOTAL.inc()
            log.warning("egress_append_failed_unpinned", error=str(exc))
            return True
        return False

    async def _record_receipt(self, turn: _Turn, obs: ResponseObservation) -> None:
        """Append the actual destination as a content-free egress row (ADRL-SAF-009).

        This row, not the write-ahead ``forward`` row, is what the audit trusts. A missing
        receipt is recorded as ``assumed_intended`` so the audit can say "unconfirmed".
        """
        if self._egress is None:
            return
        served = obs.served
        deployment = self._deployments.catalog.get(served.deployment_id or "")
        if (
            self._claude_experiment is None
            and deployment is None
            and turn.deployment is not None
            and served.deployment_id is None
        ):
            deployment = turn.deployment
        fields = egress_fields(deployment, served.source.value)
        if served.deployment_id is None and served.api_base_host is not None:
            fields["api_base_host"] = served.api_base_host
        try:
            self._egress.append(
                EgressEvent(
                    lineage_hmac=turn.ctx.lineage_hmac,
                    request_class=turn.ctx.request_class.value,
                    content_bearing=turn.ctx.content_bearing,
                    destination_rung=served.rung.value,
                    deployment_tag=self._settings.deployment_tag,
                    gate_verdicts=[{"status": obs.status, "intended_rung": turn.target_rung.value}],
                    bytes_out=obs.bytes_relayed,
                    actor="gateway",
                    reason=None,
                    event_kind="served_receipt",
                    **fields,
                )
            )
        except LedgerAppendFailure as exc:
            LEDGER_DEGRADED_TOTAL.inc()
            log.error("egress_receipt_append_failed", error=str(exc))

    async def _blocked(
        self, ctx: RequestContext, gate: GateOutcomeLike, code: ErrorCode
    ) -> ProxyResponse:
        detector = gate.findings[0].detector_id if gate.findings else None
        if detector is None and gate.pinned:
            pins = await self._ledger.read_lineage_events(ctx.lineage_hmac, PIN_EVENT)
            if pins:
                detector = str(pins[-1].payload.get("detector_id") or "") or None
        executed_tool = self._profile.executed_tool(ctx)
        await self._record_egress(ctx, gate, None, 0, kind="block")
        await self._ledger.append_lineage_event(
            LineageEvent(
                lineage_hmac=ctx.lineage_hmac,
                event_type="block",
                payload={"code": code.value, "request_class": ctx.request_class.value},
            )
        )
        rendered = getattr(gate, "block_response", None)
        if rendered is not None and getattr(rendered, "code", None) is code:
            return ProxyResponse(
                status=int(rendered.status),
                headers={**JSON_HEADERS, **dict(getattr(rendered, "headers", {}) or {})},
                body=(
                    rendered.bytes
                    if isinstance(getattr(rendered, "bytes", None), bytes)
                    else json.dumps(rendered.body).encode("utf-8")
                ),
            )
        return self._error_response(
            code, block_message(code, detector=detector, executed_tool=executed_tool)
        )

    async def _count_tokens_locally(
        self, ctx: RequestContext, gate: GateOutcomeLike
    ) -> ProxyResponse:
        """A pinned lineage's count_tokens body never leaves the machine (ADRL-SEM-001)."""
        feasibility = getattr(self._gate, "feasibility", None)
        estimate_fn = getattr(feasibility, "estimate_count_tokens", None)
        if callable(estimate_fn):
            estimate = int(estimate_fn(ctx.json)["input_tokens"])
            await self._record_egress(ctx, gate, Rung.LOCAL, 0, kind="count_tokens_local")
            return self._protocol_response(self._profile.count_tokens_response(max(1, estimate)))
        estimate = self._profile.estimate_count_tokens(
            ctx, self._tokenizer, ratio=self._bundle.rungs.rungs[Rung.LOCAL].tokenizer_ratio
        )
        await self._record_egress(ctx, gate, Rung.LOCAL, 0, kind="count_tokens_local")
        return self._protocol_response(self._profile.count_tokens_response(estimate))

    async def _forward_non_api(self, parsed: RequestView) -> ProxyResponse:
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        try:
            response = await self._gateway.forward(
                parsed.method, path, forward_headers(parsed.headers), parsed.body
            )
        except UpstreamUnreachableError as exc:
            return self._error_response(ErrorCode.TERMINAL_FAILURE, str(exc))
        raw = await read_all(response)
        return ProxyResponse(
            status=response.status_code, headers=response_headers(response.headers), body=raw
        )

    def _decision_context(
        self, ctx: RequestContext, gate: GateOutcomeLike, state_loss: bool
    ) -> dict[str, Any]:
        return {
            "session_hmac": ctx.session_hmac,
            "lineage_hmac": ctx.lineage_hmac,
            "request_class": ctx.request_class.value,
            "content_bearing": ctx.content_bearing,
            "interaction_mode": ctx.interaction_mode.value,
            "requested_model": ctx.requested_model,
            "is_subagent": ctx.is_subagent,
            "session_key_source": ctx.session_key_source,
            "fingerprint_id": ctx.fingerprint_id,
            "pinned": gate.pinned,
            "unscanned": gate.unscanned,
            "gate_verdicts": [v.as_record() for v in gate.verdicts],
            "repo_class": gate.repo_class,
            "residency": gate.residency,
            "permitted_deployment_ids": _deployment_ids(gate),
            "state_loss": state_loss,
            "routing_mode": self._settings.routing_mode.value,
            "gate_mode": self._settings.gate_mode.value,
            "config_versions": self._bundle.versions,
            "protocol_profile_id": ctx.protocol_profile_id,
            "protocol_profile_version": ctx.protocol_profile_version,
            "harness_adapter_id": ctx.harness_adapter_id,
            "harness_adapter_version": ctx.harness_adapter_version,
            "protocol_operation_supported": ctx.path in self._profile.endpoints,
        }

    async def _append_event(
        self, ctx: RequestContext, route_id: str, event_type: str, payload: Mapping[str, Any]
    ) -> None:
        producer_seq = await self._seq.next(self._ledger, route_id)
        stored = await self._ledger.append_event(
            LedgerEvent(
                route_id=RouteId(route_id),
                event_type=event_type,
                producer=PRODUCER,
                producer_seq=producer_seq,
                payload=payload,
            )
        )
        if not stored:
            EVENT_DROPPED_TOTAL.labels(producer=PRODUCER).inc()
            log.warning(
                "event_dropped",
                route_id=route_id,
                event_type=event_type,
                producer_seq=producer_seq,
                degraded=self._ledger.degraded,
            )

    def _write_behind(
        self, ctx: RequestContext, route_id: str, event_type: str, payload: Mapping[str, Any]
    ) -> None:
        task = asyncio.create_task(self._append_event(ctx, route_id, event_type, payload))
        self._background.add(task)
        task.add_done_callback(self._background.discard)

    @staticmethod
    def _protocol_response(
        response: ProtocolResponse, route_id: str | None = None
    ) -> ProxyResponse:
        return ProxyResponse(
            status=response.status,
            headers=dict(response.headers),
            body=response.body,
            route_id=route_id,
        )

    def _error_response(
        self, code: ErrorCode, detail: str, route_id: str | None = None
    ) -> ProxyResponse:
        return self._protocol_response(self._profile.error(code, detail), route_id)


class _PinnedOverlay:
    """A gate outcome re-read as pinned because an ancestor lineage is pinned (ADRL-SEM-006)."""

    def __init__(self, inner: GateOutcomeLike) -> None:
        self._inner = inner
        self.permitted: PermittedSet = inner.permitted.tighten({Rung.LOCAL} & inner.permitted.rungs)
        self.verdicts: tuple[GateVerdict, ...] = (
            *inner.verdicts,
            GateVerdict(
                gate="inherited_pin",
                permitted_after=self.permitted,
                reason="ancestor lineage pinned",
                pinned=True,
            ),
        )
        self.pinned = True
        self.unscanned = inner.unscanned
        self.findings = inner.findings
        self.block = inner.block
        self.repo_class = inner.repo_class
        self.residency = inner.residency
        self.latency_s = inner.latency_s
        inherited = getattr(inner, "permitted_deployments", None)
        self.permitted_deployments: DeploymentSet | None = (
            inherited.local_host_only() if inherited is not None else None
        )


@dataclass(frozen=True, slots=True)
class _FallbackPlan:
    rung: Rung
    is_boundary: bool
    escalated: bool
    from_rung: Rung | None
    handoff: Any
    pair_rule: Any
    block: ErrorCode | None
    sticky: StickyState

    @classmethod
    def for_decision(
        cls,
        ctx: RequestContext,
        decision: Decision,
        sticky: StickyState | None,
        *,
        is_boundary: bool,
    ) -> _FallbackPlan:
        turn_index = (sticky.turn_index + 1) if sticky is not None else 0
        state = StickyState(
            lineage_hmac=ctx.lineage_hmac,
            route_id=decision.route_id,
            rung=decision.rung,
            escalated=False,
            served_model=None,
            served_provider=None,
            served_source="assumed_intended",
            turn_index=turn_index,
            last_served_at=None,
            state_loss=sticky is None,
        )
        return cls(
            rung=decision.rung,
            is_boundary=is_boundary,
            escalated=False,
            from_rung=None,
            handoff=None,
            pair_rule=None,
            block=None,
            sticky=state,
        )


def _deployment_ids(gate: GateOutcomeLike) -> list[str] | None:
    deployments = getattr(gate, "permitted_deployments", None)
    return deployments.as_list() if deployments is not None else None


def _with_deployment(
    plan: DispatchPlanLike, deployment: DeploymentInfo | None, forward_original: bool
) -> DispatchPlanLike:
    """Record the chosen deployment on the plan when the plan type carries the fields."""
    candidate: Any = plan
    if deployment is None or not dataclasses.is_dataclass(candidate):
        return plan
    names = {f.name for f in dataclasses.fields(candidate)}
    if "deployment_id" not in names:
        return plan
    alias = None if forward_original else deployment.deployment_id
    replace_fn: Any = dataclasses.replace
    replaced: Any = replace_fn(candidate, deployment_id=deployment.deployment_id, model_alias=alias)
    return replaced  # type: ignore[no-any-return]

FILE /Users/arunmenon/projects/adrl-core/src/adrl/ledger/outcomes.py
"""Outcome lifecycle: pending, closed_turn, closed_final. Primary: ADRL-MEM-002.

Secondary: ADRL-MEM-004 (label freeze), ADRL-CAS-005 (episode boundary trigger).

The closing window is a parameter, not a promise: close-v1 emits closed_final after N subsequent
user turns in the same session, T minutes of session inactivity, or an explicit episode boundary,
whichever comes first. The rule id and trigger are stored on the event so a longer window can be
applied retroactively by replay. Evidence arriving after closed_final is appended as late_evidence
and the label is re-derived; the freeze point is recorded, the truth keeps moving.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from statistics import median
from typing import Any

import structlog

from adrl.config.models import CloseRule
from adrl.core.enums import FailureType, OutcomeState
from adrl.core.ids import RouteId
from adrl.core.types import LedgerEvent
from adrl.ledger.events import (
    EPISODE_BOUNDARY_EVENT,
    LABEL_CORRECTION_EVENT,
    LABEL_EVENT,
    LATE_EVIDENCE_EVENT,
    OUTCOME_EVENT,
    PRODUCER_CLOSER,
    PRODUCER_CORRECTION,
    PRODUCER_LABELER,
    CauseCandidate,
    StoredEvent,
    label_event,
    late_evidence_event,
    outcome_event,
    producer_seq_for,
    read_stored_events,
    stored_event_from_row,
)
from adrl.ledger.labels import Label, derive_label, outcome_state
from adrl.ledger.store import LedgerStore, utc_now_iso

log = structlog.get_logger(__name__)


def _parse_ts(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


@dataclass(frozen=True, slots=True)
class OutcomeProjection:
    """Current state of one route, derived from its events (never a source of truth)."""

    route_id: RouteId
    state: OutcomeState | None
    pending_ts: str | None
    closed_turn_ts: str | None
    closed_final_ts: str | None
    closed_final_rule_id: str | None
    label: Label
    late_evidence_count: int
    session_hmac: str | None
    lineage_hmac: str | None

    @property
    def countable(self) -> bool:
        return self.state is OutcomeState.CLOSED_FINAL


def project_outcome(route_id: RouteId, events: Sequence[StoredEvent]) -> OutcomeProjection:
    pending_ts = closed_turn_ts = closed_final_ts = rule_id = None
    session = lineage = None
    late = 0
    for event in events:
        if event.event_type == OUTCOME_EVENT:
            state = str(event.payload.get("state"))
            if state == OutcomeState.PENDING.value and pending_ts is None:
                pending_ts = event.ts
            elif state == OutcomeState.CLOSED_TURN.value:
                closed_turn_ts = event.ts
            elif state == OutcomeState.CLOSED_FINAL.value:
                closed_final_ts = event.ts
                rule_id = event.payload.get("rule_id")
            session = event.payload.get("session_hmac") or session
            lineage = event.payload.get("lineage_hmac") or lineage
        elif event.event_type == LATE_EVIDENCE_EVENT:
            late += 1
    return OutcomeProjection(
        route_id=route_id,
        state=outcome_state(events),
        pending_ts=pending_ts,
        closed_turn_ts=closed_turn_ts,
        closed_final_ts=closed_final_ts,
        closed_final_rule_id=str(rule_id) if rule_id else None,
        label=derive_label(events),
        late_evidence_count=late,
        session_hmac=str(session) if session else None,
        lineage_hmac=str(lineage) if lineage else None,
    )


def read_projection(store: LedgerStore, route_id: RouteId) -> OutcomeProjection:
    return project_outcome(route_id, read_stored_events(store, route_id))


def _latest_outcome_rows(store: LedgerStore) -> list[StoredEvent]:
    rows = store.read(
        "SELECT e.* FROM events e JOIN (SELECT route_id, MAX(seq) AS mseq FROM events "
        "WHERE event_type=? GROUP BY route_id) m ON e.seq = m.mseq ORDER BY e.seq",
        (OUTCOME_EVENT,),
    )
    return [stored_event_from_row(r) for r in rows]


def routes_in_state(store: LedgerStore, state: OutcomeState) -> list[StoredEvent]:
    return [e for e in _latest_outcome_rows(store) if str(e.payload.get("state")) == state.value]


class Closer:
    """Emits closed_final under a named rule; idempotent per (route_id, rule_id)."""

    def __init__(self, store: LedgerStore, rule: CloseRule) -> None:
        self._store = store
        self._rule = rule

    @property
    def rule_id(self) -> str:
        return self._rule.rule_id

    def _session_of(
        self, route_id: RouteId, payload: Mapping[str, Any]
    ) -> tuple[str | None, str | None]:
        session = payload.get("session_hmac")
        lineage = payload.get("lineage_hmac")
        if session is None or lineage is None:
            row = self._store.read_decision(str(route_id))
            if row is not None:
                session = session or row["session_hmac"]
                lineage = lineage or row["lineage_hmac"]
        return (str(session) if session else None, str(lineage) if lineage else None)

    def trigger_for(self, closed_turn: StoredEvent, *, now: datetime) -> str | None:
        """Return the trigger name if the closing window has elapsed, else None."""
        session, lineage = self._session_of(closed_turn.route_id, closed_turn.payload)
        if lineage is not None:
            boundaries = self._store.read(
                "SELECT seq FROM lineage_events WHERE lineage_hmac=? AND event_type=? AND ts>? "
                "LIMIT 1",
                (lineage, EPISODE_BOUNDARY_EVENT, closed_turn.ts),
            )
            if boundaries:
                return "episode_boundary"
        if session is not None:
            turns = self._store.read(
                "SELECT COUNT(*) AS c FROM decisions WHERE session_hmac=? AND "
                "request_class='user_turn' AND ts>?",
                (session, closed_turn.ts),
            )[0]["c"]
            if int(turns) >= self._rule.subsequent_turns:
                return "subsequent_turns"
            last = self._store.read(
                "SELECT MAX(ts) AS t FROM decisions WHERE session_hmac=?", (session,)
            )[0]["t"]
            last_activity = _parse_ts(str(last)) if last else _parse_ts(closed_turn.ts)
        else:
            last_activity = _parse_ts(closed_turn.ts)
        idle = (now - max(last_activity, _parse_ts(closed_turn.ts))).total_seconds() / 60.0
        if idle >= self._rule.idle_minutes:
            return "idle"
        return None

    async def close_route(self, closed_turn: StoredEvent, trigger: str) -> bool:
        events = read_stored_events(self._store, closed_turn.route_id)
        label = derive_label(events)
        session, lineage = self._session_of(closed_turn.route_id, closed_turn.payload)
        event = outcome_event(
            closed_turn.route_id,
            OutcomeState.CLOSED_FINAL,
            PRODUCER_CLOSER,
            producer_seq_for(self._rule.rule_id),
            rule_id=self._rule.rule_id,
            trigger=trigger,
            label=label.as_dict(),
        )
        payload = dict(event.payload)
        payload["closed_turn_seq"] = closed_turn.seq
        payload["session_hmac"] = session
        payload["lineage_hmac"] = lineage
        ok = bool(
            await self._store.write_through(
                LedgerStore.insert_event(
                    event.route_id,
                    event.event_type,
                    event.producer,
                    event.producer_seq,
                    payload,
                    event.schema_version,
                )
            )
        )
        if ok:
            await self._store.write_through(
                LedgerStore.insert_event(
                    event.route_id,
                    LABEL_EVENT,
                    PRODUCER_LABELER,
                    producer_seq_for("closed_final", self._rule.rule_id),
                    {**label.as_dict(), "supersedes_seq": None},
                    event.schema_version,
                )
            )
        return ok

    async def scan(self, *, now: datetime | None = None) -> list[tuple[RouteId, str]]:
        """Close every route whose window has elapsed. Returns (route_id, trigger) pairs."""
        current = now or datetime.now(UTC)
        closed: list[tuple[RouteId, str]] = []
        for closed_turn in routes_in_state(self._store, OutcomeState.CLOSED_TURN):
            trigger = self.trigger_for(closed_turn, now=current)
            if trigger is None:
                continue
            if await self.close_route(closed_turn, trigger):
                closed.append((closed_turn.route_id, trigger))
        return closed


async def append_late_evidence(
    store: LedgerStore,
    route_id: RouteId,
    *,
    source: str,
    detail: Mapping[str, Any],
    causes: Sequence[CauseCandidate] = (),
    producer: str = PRODUCER_CORRECTION,
    evidence_id: str | None = None,
) -> Label:
    """Append late evidence and re-derive the label; returns the new label."""
    ident = evidence_id or json.dumps(dict(detail), sort_keys=True, default=str)
    event = late_evidence_event(
        route_id, source, producer, producer_seq_for(source, ident), detail, causes=causes
    )
    await store.write_through(
        LedgerStore.insert_event(
            event.route_id,
            event.event_type,
            event.producer,
            event.producer_seq,
            event.payload,
            event.schema_version,
        )
    )
    events = read_stored_events(store, route_id)
    label = derive_label(events)
    previous = [e for e in events if e.event_type in (LABEL_EVENT, LABEL_CORRECTION_EVENT)]
    supersedes = previous[-1].seq if previous else None
    if outcome_state(events) is OutcomeState.CLOSED_FINAL or previous:
        correction = label_event(
            route_id,
            producer_seq_for("late", source, ident),
            label.as_dict(),
            supersedes_seq=supersedes,
        )
        await store.write_through(
            LedgerStore.insert_event(
                correction.route_id,
                correction.event_type,
                correction.producer,
                correction.producer_seq,
                correction.payload,
                correction.schema_version,
            )
        )
    return label


def current_label(store: LedgerStore, route_id: RouteId) -> Label:
    return derive_label(read_stored_events(store, route_id))


class HumanCorrectionDetector:
    """Late evidence from ledger-visible human corrections (ADRL-MEM-002 follow-up).

    A later route in the same session whose closed_turn reports touched_paths overlapping the
    routed turn's touched_paths, or a revert_paths entry touching them, within the window is a
    correction. Paths are keyed hashes supplied by the producer, never raw paths.
    """

    def __init__(self, store: LedgerStore, window_minutes: int) -> None:
        self._store = store
        self._window = window_minutes

    def find(self, route_id: RouteId) -> list[dict[str, Any]]:
        events = read_stored_events(self._store, route_id)
        touched: set[str] = set()
        closed_turn_ts: str | None = None
        session: str | None = None
        for event in events:
            if event.event_type != OUTCOME_EVENT:
                continue
            touched.update(str(p) for p in event.payload.get("touched_paths", []) or [])
            session = event.payload.get("session_hmac") or session
            if str(event.payload.get("state")) == OutcomeState.CLOSED_TURN.value:
                closed_turn_ts = event.ts
        if not touched or closed_turn_ts is None:
            return []
        if session is None:
            row = self._store.read_decision(str(route_id))
            session = str(row["session_hmac"]) if row else None
        if session is None:
            return []
        rows = self._store.read(
            "SELECT e.* FROM events e WHERE e.event_type=? AND e.route_id!=? AND e.ts>? "
            "AND json_extract(e.payload_json,'$.session_hmac')=? ORDER BY e.seq",
            (OUTCOME_EVENT, str(route_id), closed_turn_ts, session),
        )
        limit = _parse_ts(closed_turn_ts).timestamp() + self._window * 60
        found: list[dict[str, Any]] = []
        for row in rows:
            event = stored_event_from_row(row)
            if _parse_ts(event.ts).timestamp() > limit:
                break
            later = set(str(p) for p in event.payload.get("touched_paths", []) or [])
            reverted = set(str(p) for p in event.payload.get("revert_paths", []) or [])
            overlap = sorted(touched & (later | reverted))
            if overlap:
                found.append(
                    {
                        "correcting_route_id": str(event.route_id),
                        "correcting_seq": event.seq,
                        "overlap": overlap,
                        "kind": "revert" if touched & reverted else "re_edit",
                    }
                )
        return found

    async def emit(self, route_id: RouteId) -> int:
        emitted = 0
        for hit in self.find(route_id):
            await append_late_evidence(
                self._store,
                route_id,
                source="human_correction",
                detail=hit,
                causes=(CauseCandidate(FailureType.TASK_CAPABILITY, None, "human_correction"),),
                evidence_id=str(hit["correcting_seq"]),
            )
            emitted += 1
        return emitted


@dataclass(frozen=True, slots=True)
class CloseMeasurements:
    time_to_close_seconds: tuple[float, ...]
    label_flip_fraction: float
    closed_final_count: int

    @property
    def median_seconds(self) -> float | None:
        return median(self.time_to_close_seconds) if self.time_to_close_seconds else None


def measure_closing(store: LedgerStore) -> CloseMeasurements:
    """Time-to-close distribution and the fraction of labels that changed after closed_turn."""
    rows = store.read(
        "SELECT DISTINCT route_id FROM events WHERE event_type=? AND "
        "json_extract(payload_json,'$.state')=?",
        (OUTCOME_EVENT, OutcomeState.CLOSED_FINAL.value),
    )
    durations: list[float] = []
    flips = 0
    total = 0
    for row in rows:
        route_id = RouteId(str(row["route_id"]))
        events = read_stored_events(store, route_id)
        projection = project_outcome(route_id, events)
        if projection.closed_turn_ts is None or projection.closed_final_ts is None:
            continue
        total += 1
        evidence_ts = [e.ts for e in events if e.event_type == LATE_EVIDENCE_EVENT] or [
            projection.closed_final_ts
        ]
        start = _parse_ts(projection.closed_turn_ts)
        durations.append((_parse_ts(evidence_ts[-1]) - start).total_seconds())
        frozen = next(
            (
                e.payload.get("label")
                for e in events
                if e.event_type == OUTCOME_EVENT
                and str(e.payload.get("state")) == OutcomeState.CLOSED_FINAL.value
            ),
            None,
        )
        if isinstance(frozen, dict):
            now = projection.label.as_dict()
            if (frozen.get("result"), frozen.get("failure_type")) != (
                now["result"],
                now["failure_type"],
            ):
                flips += 1
    return CloseMeasurements(tuple(durations), (flips / total) if total else 0.0, total)


def ledger_event_to_write(event: LedgerEvent) -> Any:
    """Convenience: a WriteFn for a typed event."""
    return LedgerStore.insert_event(
        event.route_id,
        event.event_type,
        event.producer,
        event.producer_seq,
        event.payload,
        event.schema_version,
    )


def now_iso() -> str:
    return utc_now_iso()

FILE /Users/arunmenon/projects/adrl-core/src/adrl/ledger/readiness.py
"""Learning readiness counts on censored, cause-clean labels. Primary: ADRL-MEM-004.

Secondary: ADRL-MEM-002 (censoring), ADRL-MEM-006 (degraded windows), ADRL-FND-005,
ADRL-EVL-004, ADRL-EVL-009.
Only task_capability evidence at closed_final counts; excluded types are reported next to the
count, never averaged into it. A non-zero memory_degraded count blocks the window.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from adrl.core.enums import FailureType, OutcomeState
from adrl.core.ids import RouteId
from adrl.ledger.events import MEMORY_DEGRADED_EVENT, OUTCOME_EVENT, read_stored_events
from adrl.ledger.labels import derive_label
from adrl.ledger.store import LedgerStore

READINESS_VERSION = "readiness-count-v1"


@dataclass(frozen=True, slots=True)
class ReadinessReport:
    version: str
    closed_final_count: int
    censored_count: int
    capability_evidence_count: int
    verified_success_count: int
    task_capability_failure_count: int
    excluded_by_type: dict[str, int]
    excluded_fraction: float
    distinct_bands: int
    distinct_repo_classes: int
    memory_degraded_count: int
    window_blocked: bool
    blockers: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "closed_final_count": self.closed_final_count,
            "censored_count": self.censored_count,
            "capability_evidence_count": self.capability_evidence_count,
            "verified_success_count": self.verified_success_count,
            "task_capability_failure_count": self.task_capability_failure_count,
            "excluded_by_type": dict(self.excluded_by_type),
            "excluded_fraction": self.excluded_fraction,
            "distinct_bands": self.distinct_bands,
            "distinct_repo_classes": self.distinct_repo_classes,
            "memory_degraded_count": self.memory_degraded_count,
            "window_blocked": self.window_blocked,
            "blockers": list(self.blockers),
        }


def learning_readiness(store: LedgerStore) -> ReadinessReport:
    routes = store.read("SELECT DISTINCT route_id FROM events WHERE event_type=?", (OUTCOME_EVENT,))
    closed_final = 0
    censored = 0
    verified_success = 0
    capability_failure = 0
    excluded: Counter[str] = Counter()
    bands: set[str] = set()
    repos: set[str] = set()
    for row in routes:
        route_id = RouteId(str(row["route_id"]))
        events = read_stored_events(store, route_id)
        state = None
        for event in events:
            if event.event_type == OUTCOME_EVENT:
                state = str(event.payload.get("state"))
        if state != OutcomeState.CLOSED_FINAL.value:
            censored += 1
            continue
        closed_final += 1
        label = derive_label(events)
        if label.is_capability_evidence:
            if label.result == "success":
                verified_success += 1
            else:
                capability_failure += 1
            decision = store.read_decision(str(route_id))
            if decision is not None:
                features = json.loads(str(decision["features_json"]))
                if features.get("band_id"):
                    bands.add(str(features["band_id"]))
                if features.get("repo_class"):
                    repos.add(str(features["repo_class"]))
        else:
            excluded[(label.failure_type or FailureType.UNVERIFIABLE).value] += 1
    degraded = int(
        store.read("SELECT COUNT(*) AS c FROM events WHERE event_type=?", (MEMORY_DEGRADED_EVENT,))[
            0
        ]["c"]
    )
    evidence = verified_success + capability_failure
    blockers: list[str] = []
    if degraded:
        blockers.append("memory_degraded_nonzero")
    if closed_final and evidence == 0:
        blockers.append("no_capability_evidence")
    return ReadinessReport(
        version=READINESS_VERSION,
        closed_final_count=closed_final,
        censored_count=censored,
        capability_evidence_count=evidence,
        verified_success_count=verified_success,
        task_capability_failure_count=capability_failure,
        excluded_by_type=dict(excluded),
        excluded_fraction=(sum(excluded.values()) / closed_final) if closed_final else 0.0,
        distinct_bands=len(bands),
        distinct_repo_classes=len(repos),
        memory_degraded_count=degraded,
        window_blocked=bool(blockers),
        blockers=tuple(blockers),
    )

FILE /Users/arunmenon/projects/adrl-core/src/adrl/routing/router.py
"""Router: composes features, bands, estimator, cost, advisor and cascade feasibility.

Primary: ADRL-RTG-002. Secondary: ADRL-RTG-003/004/006/009, ADRL-LRN-008 (explorer port).
The router always computes a full decision; routing mode (off/shadow/live) is honoured by the
proxy when it decides whether to act on it.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import httpx
import structlog

from adrl.config.loaders import ConfigBundle
from adrl.config.settings import Settings
from adrl.core.enums import Rung
from adrl.core.ids import mint_route_id
from adrl.core.ports import StickyState
from adrl.core.types import Decision, PermittedSet, RequestContext
from adrl.ledger.store import LedgerStore
from adrl.routing.advisor import (
    AdvisoryClassifier,
    ClassifierResult,
    Explorer,
    LocalHttpClassifier,
)
from adrl.routing.cascade_feasibility import evaluate_cascade
from adrl.routing.cost import CostInputs, CostModel
from adrl.routing.features import FEATURES_VERSION, compute_features
from adrl.routing.policy import BandHeuristicEstimator, BandMatch, classify_band, select_rung
from adrl.routing.registry import RungRegistry
from adrl.routing.rule_health import RuleHealthSnapshot, compute_rule_health
from adrl.routing.side_effects import UNTRUSTED, TrustPolicy, load_trust_policy

if TYPE_CHECKING:
    from adrl.gates.pipeline import GateOutcome

log = structlog.get_logger(__name__)


class Router:
    def __init__(
        self,
        bundle: ConfigBundle,
        *,
        registry: RungRegistry | None = None,
        cost_model: CostModel | None = None,
        classifier: AdvisoryClassifier | None = None,
        explorer: Explorer | None = None,
        rule_health: RuleHealthSnapshot | None = None,
        trust: TrustPolicy | None = None,
        now: Any = None,
    ) -> None:
        self._bundle = bundle
        self._trust = trust or UNTRUSTED
        self._policy = bundle.policy
        self._registry = registry or RungRegistry(bundle.rungs)
        self._cost = cost_model or CostModel(bundle.prices, bundle.policy, self._registry)
        self._estimator = BandHeuristicEstimator(bundle.policy, self._registry)
        self._classifier = classifier
        self._explorer = explorer
        self._rule_health = rule_health or RuleHealthSnapshot.empty(
            bundle.policy.rule_precision_threshold
        )
        self._now = now or (lambda: datetime.now(UTC))

    @classmethod
    def from_components(
        cls,
        *,
        bundle: ConfigBundle,
        settings: Settings,
        ledger: LedgerStore | None = None,
        explorer: Explorer | None = None,
        classifier_client: httpx.AsyncClient | None = None,
    ) -> Router:
        """Build the router with real adapters from config and settings (composition root)."""
        registry = RungRegistry(bundle.rungs)
        classifier: AdvisoryClassifier | None = None
        if settings.classifier_base_url:
            classifier = LocalHttpClassifier(
                settings.classifier_base_url,
                settings.classifier_model,
                timeout_s=bundle.policy.classifier_timeout_s,
                token_cap=bundle.policy.classifier_token_cap,
                prompt_version=bundle.policy.classifier_prompt_version,
                is_local=settings.classifier_is_local,
                client=classifier_client,
            )
        rule_health: RuleHealthSnapshot | None = None
        if ledger is not None:
            rule_health = compute_rule_health(
                ledger, threshold=bundle.policy.rule_precision_threshold
            )
        return cls(
            bundle,
            registry=registry,
            classifier=classifier,
            explorer=explorer,
            rule_health=rule_health,
            trust=load_trust_policy(settings.config_dir),
        )

    @property
    def registry(self) -> RungRegistry:
        return self._registry

    @property
    def trust(self) -> TrustPolicy:
        """MCP servers whose annotations the feature snapshot honours (ADRL-CAS-009)."""
        return self._trust

    def set_rule_health(self, snapshot: RuleHealthSnapshot) -> None:
        self._rule_health = snapshot

    async def decide(
        self, ctx: RequestContext, gate: GateOutcome, sticky: StickyState | None
    ) -> Decision:
        permitted = gate.permitted
        deployments = getattr(gate, "permitted_deployments", None)
        if deployments is not None:
            # a rung with no attested, permitted deployment is not a choice (ADRL-SAF-008)
            permitted = permitted.tighten(permitted.rungs & deployments.rungs())
        if permitted.is_empty:
            raise ValueError("router called with an empty permitted set; the gate must block")
        features = compute_features(ctx, self._policy.rule_thresholds, trust=self._trust)
        band = classify_band(features, self._policy, self._rule_health.demoted)
        probabilities = self._estimator.probabilities(features, band)
        inputs = CostInputs(
            context_tokens=int(features["context_tokens_estimate"]),
            expected_output_tokens=self._policy.expected_output_tokens_by_mode.get(
                ctx.interaction_mode.value, 2_000
            ),
            request_kind=ctx.request_class.value,
            band_id=band.band_id,
            now=self._now(),
            sticky=sticky,
        )
        costs = self._cost.estimate_all(inputs, probabilities, permitted)
        selection = select_rung(permitted, probabilities, costs, self._policy)
        rung = selection.rung
        provenance: dict[str, Any] | None = None
        classifier_result: ClassifierResult | None = None
        if band.is_ambiguous:
            rung, classifier_result = await self._advise(ctx, features, permitted, gate, rung)
            if classifier_result is not None:
                provenance = classifier_result.as_provenance()
                inputs_after = CostInputs(
                    context_tokens=inputs.context_tokens + classifier_result.tokens_used,
                    expected_output_tokens=inputs.expected_output_tokens,
                    request_kind=inputs.request_kind,
                    band_id=inputs.band_id,
                    now=inputs.now,
                    sticky=inputs.sticky,
                )
                costs = self._cost.estimate_all(inputs_after, probabilities, permitted)
        cascade = evaluate_cascade(
            features, permitted, pinned=gate.pinned, registry=self._registry, policy=self._policy
        )
        if rung is Rung.LOCAL and not gate.pinned and not cascade.feasible:
            fallback = cascade.next_rung or permitted.highest
            assert fallback is not None
            log.info("local_first_infeasible", reason=cascade.reason, fallback=fallback.value)
            rung = fallback
        propensity = 1.0
        explore_version: str | None = None
        if (
            self._explorer is not None
            and band.is_ambiguous
            and not gate.pinned
            and permitted.rungs == PermittedSet.all().rungs
            and (sticky is None or not sticky.escalated)
        ):
            choice = self._explorer.explore(ctx, features, band.band_id, permitted, rung)
            if choice is not None and choice.rung in permitted:
                rung = choice.rung
                propensity = choice.propensity
                explore_version = choice.explore_version
        decision = Decision(
            route_id=mint_route_id(),
            rung=rung,
            permitted=permitted,
            estimator=self._estimator.name,
            estimator_version=self._estimator.version,
            policy_version=self._policy.version,
            objective_version=self._policy.objective_version,
            cascade_feasible=cascade.feasible,
            cascade_reason=cascade.reason,
            features=features,
            features_version=FEATURES_VERSION,
            propensity=propensity,
            explore_version=explore_version,
            no_rung_met_threshold=selection.no_rung_met_threshold,
            classifier_provenance=provenance,
        )
        return decision

    def decision_context(
        self, decision: Decision, band: BandMatch | None = None, **extra: Any
    ) -> dict[str, Any]:
        """Context stored next to the decision row: band, rules, versions, weights."""
        features = decision.features
        if band is None:
            band = classify_band(features, self._policy, self._rule_health.demoted)
        return {
            "band_id": band.band_id,
            "band_demoted": band.demoted,
            "rules_fired": list(band.rules_fired),
            "tau_by_rung": {r.value: t for r, t in self._policy.tau_by_rung.items()},
            "objective_weights": self._policy.objective_weights.model_dump(),
            "config_versions": self._bundle.versions,
            "episode_estimator_version": self._cost.episode_estimator_version,
            "rule_health_version": self._rule_health.version,
            **extra,
        }

    async def _advise(
        self,
        ctx: RequestContext,
        features: Mapping[str, Any],
        permitted: PermittedSet,
        gate: GateOutcome,
        selected: Rung,
    ) -> tuple[Rung, ClassifierResult | None]:
        fallback = self._policy.ambiguous_fallback_rung
        if fallback not in permitted:
            highest = permitted.highest
            assert highest is not None
            fallback = highest
        if self._classifier is None:
            return fallback, None
        if gate.pinned and not self._classifier.is_local:
            log.info("classifier_skipped", reason="pinned_lineage_cloud_classifier")
            return fallback, None
        result = await self._classifier.classify(ctx, features, permitted)
        floor = self._policy.estimator_params.get("classifier_confidence_floor", 0.6)
        if result.timed_out or result.malformed or result.label is None:
            return fallback, result
        if result.confidence < floor:
            return fallback, result
        return result.label, result

FILE /Users/arunmenon/projects/adrl-core/src/adrl/routing/rule_health.py
"""Per-band rule precision on verified outcomes. Primary: ADRL-RTG-003.

A band whose measured precision falls below the versioned threshold loses its clear status and
routes through the advisor until re-qualified. Reads the ledger only; never writes.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from adrl.core.enums import FailureType, OutcomeState
from adrl.ledger.store import LedgerStore

RULE_HEALTH_VERSION = "rule-health-v1"


@dataclass(frozen=True, slots=True)
class BandPrecision:
    band_id: str
    verified: int
    completed_without_escalation: int

    @property
    def precision(self) -> float | None:
        return None if self.verified == 0 else self.completed_without_escalation / self.verified


@dataclass(frozen=True, slots=True)
class RuleHealthSnapshot:
    version: str
    threshold: float
    by_band: Mapping[str, BandPrecision]
    minimum_verified: int = 20
    demoted: frozenset[str] = field(default_factory=frozenset)

    @classmethod
    def empty(cls, threshold: float) -> RuleHealthSnapshot:
        return cls(RULE_HEALTH_VERSION, threshold, {})

    def as_report(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "threshold": self.threshold,
            "minimum_verified": self.minimum_verified,
            "demoted": sorted(self.demoted),
            "bands": {
                b: {
                    "verified": p.verified,
                    "completed_without_escalation": p.completed_without_escalation,
                    "precision": p.precision,
                }
                for b, p in self.by_band.items()
            },
        }


def compute_rule_health(
    store: LedgerStore, *, threshold: float, minimum_verified: int = 20
) -> RuleHealthSnapshot:
    """Precision = closed_final verified successes without escalation / verified closed_final."""
    decisions = store.read(
        "SELECT route_id, context_json FROM decisions WHERE request_class = 'user_turn'"
    )
    band_of: dict[str, str] = {}
    for row in decisions:
        context = json.loads(row["context_json"])
        band = context.get("band_id")
        if isinstance(band, str):
            band_of[row["route_id"]] = band
    escalated: set[str] = set()
    for row in store.read("SELECT DISTINCT route_id FROM events WHERE event_type = 'escalation'"):
        escalated.add(row["route_id"])
    counts: dict[str, list[int]] = {}
    for row in store.read(
        "SELECT route_id, payload_json FROM events WHERE event_type = ? ORDER BY seq",
        (OutcomeState.CLOSED_FINAL.value,),
    ):
        band = band_of.get(row["route_id"])
        if band is None:
            continue
        payload = json.loads(row["payload_json"])
        if not payload.get("verified"):
            continue
        failure_type = payload.get("failure_type")
        success = bool(payload.get("success"))
        if not success and failure_type != FailureType.TASK_CAPABILITY.value:
            continue
        bucket = counts.setdefault(band, [0, 0])
        bucket[0] += 1
        if success and row["route_id"] not in escalated:
            bucket[1] += 1
    by_band = {b: BandPrecision(b, v, c) for b, (v, c) in counts.items()}
    demoted = frozenset(
        b
        for b, p in by_band.items()
        if p.verified >= minimum_verified and p.precision is not None and p.precision < threshold
    )
    return RuleHealthSnapshot(RULE_HEALTH_VERSION, threshold, by_band, minimum_verified, demoted)

FILE /Users/arunmenon/projects/adrl-core/src/adrl/cascade/tripwires.py
"""Deterministic post-call trip-wires. Primary: ADRL-CAS-001. Secondary: ADRL-CAS-002.

Wire classes (a) repeated or alternating tool calls, (b) schema or dialect-invalid calls typed
harness_dialect, (c) tool-error repetition, (d) attempt-budget exhaustion with no verifiable
progress, (e) deterministic verifier failure. Model-authored text is never a wire.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from adrl.config.models import PolicyConfig, TripwiresConfig, WireThresholds
from adrl.core.enums import FailureType, OutcomeState, Rung
from adrl.ledger.store import LedgerStore
from adrl.routing.side_effects import turn_start_index

if TYPE_CHECKING:
    from adrl.wire.observe import ResponseObservation

TRIPWIRE_EVENT = "tripwire_fired"

EDIT_FAIL_MARKER = "String to replace not found in file"
SCHEMA_ERROR_MARKERS: tuple[str, ...] = (
    "input validation error",
    "does not match the required schema",
    "invalid tool name",
    "InputValidationError",
)
READ_TOOLS: frozenset[str] = frozenset(
    {"read", "read_file", "readfile", "view", "view_file", "cat", "open_file", "glob", "grep"}
)
EDIT_TOOLS: frozenset[str] = frozenset(
    {
        "edit",
        "multiedit",
        "write",
        "str_replace",
        "str_replace_editor",
        "str_replace_based_edit_tool",
        "apply_patch",
        "create_file",
        "notebookedit",
    }
)
RESOURCE_KEYS: tuple[str, ...] = ("file_path", "path", "filename", "notebook_path", "file")


class WireClass(StrEnum):
    REPEATED_TOOL_CALLS = "a_repeated_tool_calls"
    INVALID_TOOL_CALLS = "b_invalid_tool_calls"
    TOOL_ERROR_REPEATS = "c_tool_error_repeats"
    ATTEMPT_BUDGET_EXHAUSTED = "d_attempt_budget_exhausted"
    VERIFIER_FAILURE = "e_verifier_failure"

    @property
    def failure_type(self) -> FailureType:
        return (
            FailureType.HARNESS_DIALECT
            if self is WireClass.INVALID_TOOL_CALLS
            else FailureType.TASK_CAPABILITY
        )


@dataclass(frozen=True, slots=True)
class WireHit:
    wire: WireClass
    rung: Rung
    threshold: int | bool
    observed: int
    failure_type: FailureType
    detail: str
    tripwires_version: str

    def as_record(self) -> dict[str, Any]:
        return {
            "wire": self.wire.value,
            "rung": self.rung.value,
            "threshold": self.threshold,
            "observed": self.observed,
            "failure_type": self.failure_type.value,
            "detail": self.detail,
            "tripwires_version": self.tripwires_version,
        }


@dataclass(frozen=True, slots=True)
class ToolCall:
    tool_use_id: str
    name: str
    canonical: str
    input_parse_ok: bool


@dataclass(frozen=True, slots=True)
class ToolResultView:
    tool_use_id: str
    is_error: bool
    content_hash: str
    text: str


def canonical_call(name: str, tool_input: Any) -> str:
    """Canonical call form so replays agree on sameness (sorted keys, no trailing slash)."""

    def norm(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {k: norm(v) for k, v in sorted(value.items())}
        if isinstance(value, list):
            return [norm(v) for v in value]
        if isinstance(value, str):
            stripped = value.strip()
            return stripped[:-1] if len(stripped) > 1 and stripped.endswith("/") else stripped
        return value

    return name.lower() + ":" + json.dumps(norm(tool_input), sort_keys=True, separators=(",", ":"))


def _hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="replace")).hexdigest()[:16]  # noqa: S324


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            str(b.get("text", ""))
            for b in content
            if isinstance(b, Mapping) and b.get("type") == "text"
        )
    return ""


def turn_calls_and_results(
    body: Mapping[str, Any],
) -> tuple[list[ToolCall], dict[str, ToolResultView]]:
    messages_raw = body.get("messages")
    messages: list[Mapping[str, Any]] = (
        [m for m in messages_raw if isinstance(m, Mapping)]
        if isinstance(messages_raw, list)
        else []
    )
    start = turn_start_index(messages)
    calls: list[ToolCall] = []
    results: dict[str, ToolResultView] = {}
    for message in messages[start:]:
        content = message.get("content")
        if not isinstance(content, list):
            continue
        if message.get("role") == "assistant":
            for block in content:
                if isinstance(block, Mapping) and block.get("type") == "tool_use":
                    tool_input = block.get("input")
                    calls.append(
                        ToolCall(
                            tool_use_id=str(block.get("id") or ""),
                            name=str(block.get("name") or ""),
                            canonical=canonical_call(str(block.get("name") or ""), tool_input),
                            input_parse_ok=isinstance(tool_input, Mapping),
                        )
                    )
        elif message.get("role") == "user":
            for block in content:
                if isinstance(block, Mapping) and block.get("type") == "tool_result":
                    text = _text_of(block.get("content"))
                    results[str(block.get("tool_use_id") or "")] = ToolResultView(
                        tool_use_id=str(block.get("tool_use_id") or ""),
                        is_error=bool(block.get("is_error")),
                        content_hash=_hash(text),
                        text=text,
                    )
    return calls, results


def _resource(call_canonical: str) -> str | None:
    try:
        payload = json.loads(call_canonical.split(":", 1)[1])
    except (ValueError, IndexError):
        return None
    if isinstance(payload, Mapping):
        for key in RESOURCE_KEYS:
            value = payload.get(key)
            if isinstance(value, str):
                return value
    return None


class TripwireEvaluator:
    def __init__(self, tripwires: TripwiresConfig, policy: PolicyConfig) -> None:
        self._config = tripwires
        self._policy = policy

    @property
    def version(self) -> str:
        return self._config.version

    def thresholds(self, rung: Rung) -> WireThresholds:
        return self._config.by_rung[rung]

    def verifier_failure(self, rung: Rung) -> WireHit | None:
        """Wire class (e): a deterministic verifier failure fires on its own (ADRL-CAS-001)."""
        if not self.thresholds(rung).verifier_failure:
            return None
        return WireHit(
            WireClass.VERIFIER_FAILURE,
            rung,
            True,
            1,
            FailureType.TASK_CAPABILITY,
            "deterministic verifier reported failure",
            self.version,
        )

    def evaluate(
        self,
        body: Mapping[str, Any],
        rung: Rung,
        *,
        observation: ResponseObservation | None = None,
        verifier_failed: bool = False,
        wall_clock_s: float | None = None,
    ) -> tuple[WireHit, ...]:
        t = self.thresholds(rung)
        calls, results = turn_calls_and_results(body)
        hits: list[WireHit] = []
        hits.extend(self._repeated(calls, results, rung, t))
        hits.extend(self._invalid(calls, results, rung, t, observation))
        hits.extend(self._error_repeats(calls, results, rung, t))
        hits.extend(self._attempt_budget(calls, results, rung, t, wall_clock_s))
        if verifier_failed and t.verifier_failure:
            hits.append(
                WireHit(
                    WireClass.VERIFIER_FAILURE,
                    rung,
                    True,
                    1,
                    FailureType.TASK_CAPABILITY,
                    "deterministic verifier reported failure",
                    self.version,
                )
            )
        return tuple(hits)

    def _repeated(
        self,
        calls: Sequence[ToolCall],
        results: Mapping[str, ToolResultView],
        rung: Rung,
        t: WireThresholds,
    ) -> list[WireHit]:
        if not calls:
            return []
        # identical consecutive calls, allowing a long-running command whose observation changes
        run = 1
        best = 1
        for prev, cur in itertools.pairwise(calls):
            if cur.canonical == prev.canonical and not self._observation_changed(
                prev, cur, results, t
            ):
                run += 1
            else:
                run = 1
            best = max(best, run)
        detail = "identical consecutive tool calls"
        # alternating A,B,A,B
        alt = 1
        for i in range(2, len(calls)):
            if (
                calls[i].canonical == calls[i - 2].canonical
                and calls[i].canonical != calls[i - 1].canonical
            ):
                alt += 1
            else:
                alt = 1
            if alt > best:
                best = alt
                detail = "alternating tool calls"
        if best >= t.repeated_tool_calls:
            return [
                WireHit(
                    WireClass.REPEATED_TOOL_CALLS,
                    rung,
                    t.repeated_tool_calls,
                    best,
                    FailureType.TASK_CAPABILITY,
                    detail,
                    self.version,
                )
            ]
        return []

    @staticmethod
    def _observation_changed(
        prev: ToolCall, cur: ToolCall, results: Mapping[str, ToolResultView], t: WireThresholds
    ) -> bool:
        a = results.get(prev.tool_use_id)
        b = results.get(cur.tool_use_id)
        if a is None or b is None:
            return False
        return a.content_hash != b.content_hash and not a.is_error and not b.is_error

    def _invalid(
        self,
        calls: Sequence[ToolCall],
        results: Mapping[str, ToolResultView],
        rung: Rung,
        t: WireThresholds,
        observation: ResponseObservation | None,
    ) -> list[WireHit]:
        count = sum(1 for c in calls if not c.input_parse_ok)
        for call in calls:
            result = results.get(call.tool_use_id)
            if result is None or not result.is_error:
                continue
            if EDIT_FAIL_MARKER in result.text or any(
                m in result.text for m in SCHEMA_ERROR_MARKERS
            ):
                count += 1
        if observation is not None and observation.malformed_tool_json:
            count += 1
        if count >= t.invalid_tool_calls:
            return [
                WireHit(
                    WireClass.INVALID_TOOL_CALLS,
                    rung,
                    t.invalid_tool_calls,
                    count,
                    FailureType.HARNESS_DIALECT,
                    "schema or dialect-invalid tool calls",
                    self.version,
                )
            ]
        return []

    def _error_repeats(
        self,
        calls: Sequence[ToolCall],
        results: Mapping[str, ToolResultView],
        rung: Rung,
        t: WireThresholds,
    ) -> list[WireHit]:
        run = 0
        best = 0
        last_name = None
        for call in calls:
            result = results.get(call.tool_use_id)
            if result is not None and result.is_error:
                run = run + 1 if call.name == last_name or last_name is None else 1
                last_name = call.name
            else:
                run = 0
                last_name = None
            best = max(best, run)
        if best >= t.tool_error_repeats:
            return [
                WireHit(
                    WireClass.TOOL_ERROR_REPEATS,
                    rung,
                    t.tool_error_repeats,
                    best,
                    FailureType.TASK_CAPABILITY,
                    "repeated tool errors",
                    self.version,
                )
            ]
        return []

    def _attempt_budget(
        self,
        calls: Sequence[ToolCall],
        results: Mapping[str, ToolResultView],
        rung: Rung,
        t: WireThresholds,
        wall_clock_s: float | None,
    ) -> list[WireHit]:
        if not t.attempt_budget_exhausted:
            return []
        budget = self._policy.local_attempt_budget
        exhausted = False
        observed = len(calls)
        if budget.unit == "tool_calls" and len(calls) >= budget.limit:
            exhausted = True
        if wall_clock_s is not None and wall_clock_s >= budget.wall_clock_cap_s:
            exhausted = True
            observed = int(wall_clock_s)
        if not exhausted:
            return []
        if self._made_progress(calls, results):
            return []
        return [
            WireHit(
                WireClass.ATTEMPT_BUDGET_EXHAUSTED,
                rung,
                budget.limit,
                observed,
                FailureType.TASK_CAPABILITY,
                "attempt budget exhausted with no verifiable progress",
                self.version,
            )
        ]

    @staticmethod
    def _made_progress(calls: Sequence[ToolCall], results: Mapping[str, ToolResultView]) -> bool:
        """Progress: a new file read, a successful edit or a new non-error output, recently."""
        seen_reads: set[str] = set()
        seen_hashes: set[str] = set()
        progress_at: list[int] = []
        for index, call in enumerate(calls):
            result = results.get(call.tool_use_id)
            if result is None or result.is_error:
                continue
            name = call.name.lower()
            resource = _resource(call.canonical)
            if name in READ_TOOLS and resource and resource not in seen_reads:
                seen_reads.add(resource)
                progress_at.append(index)
            elif name in EDIT_TOOLS:
                progress_at.append(index)
            elif result.content_hash not in seen_hashes:
                seen_hashes.add(result.content_hash)
                progress_at.append(index)
        if not progress_at:
            return False
        return progress_at[-1] >= (2 * len(calls)) // 3


def coverage_report(store: LedgerStore) -> dict[str, Any]:
    """Trip-wire miss rate and false-fire rate per rung over closed_final verified outcomes."""
    fired: dict[str, set[str]] = {}
    for row in store.read(
        "SELECT route_id, payload_json FROM events WHERE event_type = ?", (TRIPWIRE_EVENT,)
    ):
        payload = json.loads(row["payload_json"])
        fired.setdefault(row["route_id"], set()).add(str(payload.get("wire")))
    stats: dict[str, dict[str, int]] = {}
    for row in store.read(
        "SELECT route_id, payload_json FROM events WHERE event_type = ?",
        (OutcomeState.CLOSED_FINAL.value,),
    ):
        payload = json.loads(row["payload_json"])
        if not payload.get("verified"):
            continue
        rung = str(payload.get("rung") or "unknown")
        bucket = stats.setdefault(
            rung, {"verified_failures": 0, "missed": 0, "verified_successes": 0, "false_fires": 0}
        )
        had_wire = row["route_id"] in fired
        if payload.get("success"):
            bucket["verified_successes"] += 1
            if had_wire:
                bucket["false_fires"] += 1
        else:
            bucket["verified_failures"] += 1
            if not had_wire:
                bucket["missed"] += 1
    report: dict[str, Any] = {}
    for rung, b in stats.items():
        report[rung] = {
            **b,
            "miss_rate": (b["missed"] / b["verified_failures"]) if b["verified_failures"] else None,
            "false_fire_rate": (b["false_fires"] / b["verified_successes"])
            if b["verified_successes"]
            else None,
        }
    return report

FILE /Users/arunmenon/projects/adrl-core/src/adrl/learning/tiers.py
"""Evidence tiers and pooling rules. Primary: ADRL-LRN-001.
Also implements: ADRL-EVL-005 (register additions of 2026-09-03).

Secondary: ADRL-MEM-002 (censoring), ADRL-MEM-003 (indeterminate, tree drift), ADRL-MEM-004
(only task_capability is capability evidence), ADRL-LRN-002 (T5), ADRL-LRN-008 (explore).

Only T1 enters the estimator objective and the holdout. Lower tiers are declared weak signal
with the tier recorded per example. Organic, counterfactual and exploration families never
pool: a TieredDataset carries exactly one family and refuses to merge across families.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

from adrl.config.models import LearningContract
from adrl.core.enums import EvidenceTier, FailureType, OutcomeState, Rung, VerificationResult
from adrl.core.ids import RouteId, SessionId
from adrl.ledger.store import LedgerStore

TIERS_VERSION = "evidence-tiers-v1"

ExampleSource = Literal["organic", "simulator", "benchmark", "counterfactual", "explore"]
Family = Literal["organic", "synthetic", "counterfactual", "explore"]

_FAMILY_BY_SOURCE: dict[str, Family] = {
    "organic": "organic",
    "simulator": "synthetic",
    "benchmark": "synthetic",
    "counterfactual": "counterfactual",
    "explore": "explore",
}


class PoolingError(ValueError):
    """Raised when evidence families or tiers would be pooled (ADRL-LRN-001 clause 2)."""


@dataclass(frozen=True, slots=True)
class VerifierPrecision:
    """Measured verifier precision that conditions T1 status (ADRL-LRN-001 clause 3)."""

    verifier_version: str
    repeat_run_agreement: float
    flake_rate: float
    tree_drift_rate: float
    runs: int = 0

    def meets(self, threshold: float) -> bool:
        return (
            self.repeat_run_agreement >= threshold
            and self.flake_rate <= (1.0 - threshold)
            and self.tree_drift_rate <= (1.0 - threshold)
        )


@dataclass(frozen=True, slots=True)
class Example:
    """One routed turn with everything the tier rules need. Content-free."""

    route_id: RouteId
    session_hmac: SessionId
    decision_ts: str
    rung: Rung
    features: Mapping[str, Any]
    features_version: str
    source: ExampleSource
    outcome_state: OutcomeState
    failure_type: FailureType | None
    verification: VerificationResult | None
    tree_drift: bool
    verifier_version: str | None
    harness_reported_success: bool | None
    propensity: float = 1.0
    explore_version: str | None = None
    pinned: bool = False
    privacy_suppressed: bool = False
    slice_id: str = "all"
    repo_class: str | None = None
    intent_class: str | None = None

    @property
    def family(self) -> Family:
        return _FAMILY_BY_SOURCE[self.source]

    @property
    def verified_success(self) -> bool | None:
        """Verified label: pass is success, fail is failure, anything else is unknown."""
        if self.verification is VerificationResult.PASS:
            return True
        if self.verification is VerificationResult.FAIL:
            return False
        return None

    @property
    def label(self) -> int | None:
        """Binary outcome for the estimator: verified when present, else proxy."""
        verified = self.verified_success
        if verified is not None:
            return 1 if verified else 0
        if self.harness_reported_success is None:
            return None
        return 1 if self.harness_reported_success else 0


@dataclass(frozen=True, slots=True)
class TierAssignment:
    tier: EvidenceTier | None
    reason: str


def assign_tier(
    example: Example,
    contract: LearningContract,
    verifier_precision: Mapping[str, VerifierPrecision] | None = None,
) -> TierAssignment:
    """Assign the evidence tier per ADRL-LRN-001; None means the example is excluded."""
    if example.source == "counterfactual":
        return TierAssignment(EvidenceTier.T5, "counterfactual pair")
    if example.source == "explore" or example.explore_version is not None:
        return TierAssignment(EvidenceTier.EXPLORE, "logged exploration with propensity")
    if example.source in ("simulator", "benchmark"):
        return TierAssignment(EvidenceTier.T4, f"{example.source} evidence")

    if example.failure_type is not None and not example.failure_type.is_capability_evidence:
        return TierAssignment(
            None, f"excluded failure type {example.failure_type.value} (ADRL-MEM-004)"
        )

    verified = example.verification is not None and (
        example.verification is not VerificationResult.INDETERMINATE
    )
    if verified and not example.tree_drift:
        if example.outcome_state is OutcomeState.CLOSED_FINAL:
            precision = None
            if verifier_precision is not None and example.verifier_version is not None:
                precision = verifier_precision.get(example.verifier_version)
            if precision is None:
                return TierAssignment(EvidenceTier.T2, "verifier precision not measured")
            if not precision.meets(contract.verifier_precision_threshold):
                return TierAssignment(EvidenceTier.T2, "verifier precision below threshold")
            return TierAssignment(EvidenceTier.T1, "verified, task_capability, closed_final")
        if example.outcome_state is OutcomeState.CLOSED_TURN:
            return TierAssignment(EvidenceTier.T2, "verified but closed_turn only (censored)")
        return TierAssignment(None, "verified but outcome still pending")
    if verified and example.tree_drift:
        return TierAssignment(None, "tree drift excludes the verification (ADRL-MEM-003)")
    if example.harness_reported_success is not None:
        return TierAssignment(EvidenceTier.T3, "proxy label from harness report")
    return TierAssignment(None, "no verification and no proxy signal")


@dataclass(frozen=True, slots=True)
class TieredExample:
    example: Example
    tier: EvidenceTier
    reason: str


@dataclass(slots=True)
class TieredDataset:
    """Examples of exactly one family; merges across families raise PoolingError."""

    family: Family
    examples: list[TieredExample] = field(default_factory=list)
    excluded: list[tuple[Example, str]] = field(default_factory=list)
    tiers_version: str = TIERS_VERSION

    @classmethod
    def build(
        cls,
        examples: Iterable[Example],
        contract: LearningContract,
        verifier_precision: Mapping[str, VerifierPrecision] | None = None,
        family: Family | None = None,
    ) -> TieredDataset:
        items = list(examples)
        families = {e.family for e in items}
        if family is None:
            if len(families) > 1:
                raise PoolingError(
                    "examples span families "
                    + ",".join(sorted(families))
                    + "; build one per family"
                )
            family = next(iter(families)) if families else "organic"
        assert family is not None
        dataset = cls(family=family)
        for example in items:
            if example.family != family:
                raise PoolingError(f"example {example.route_id} is {example.family}, not {family}")
            assignment = assign_tier(example, contract, verifier_precision)
            if assignment.tier is None:
                dataset.excluded.append((example, assignment.reason))
            else:
                dataset.examples.append(TieredExample(example, assignment.tier, assignment.reason))
        return dataset

    def merge(self, other: TieredDataset) -> TieredDataset:
        if other.family != self.family:
            raise PoolingError(f"cannot pool {self.family} with {other.family} (ADRL-LRN-001)")
        merged = TieredDataset(family=self.family)
        merged.examples = [*self.examples, *other.examples]
        merged.excluded = [*self.excluded, *other.excluded]
        return merged

    @property
    def tier_set(self) -> frozenset[EvidenceTier]:
        return frozenset(item.tier for item in self.examples)

    def objective_examples(self) -> list[TieredExample]:
        """Only T1 enters the objective (ADRL-LRN-001 clause 1)."""
        return [item for item in self.examples if item.tier.enters_objective]

    def weak_signal_examples(self) -> list[TieredExample]:
        return [item for item in self.examples if not item.tier.enters_objective]

    def tier_mix(self) -> dict[str, int]:
        counts = Counter(item.tier.value for item in self.examples)
        return {tier.value: counts.get(tier.value, 0) for tier in EvidenceTier}

    def exclusion_reasons(self) -> dict[str, int]:
        return dict(Counter(reason for _, reason in self.excluded))

    def excluded_fraction(self) -> float:
        total = len(self.examples) + len(self.excluded)
        return len(self.excluded) / total if total else 0.0

    def pinned_fraction(self) -> float:
        total = len(self.examples) + len(self.excluded)
        pinned = sum(1 for item in self.examples if item.example.pinned) + sum(
            1 for example, _ in self.excluded if example.pinned
        )
        return pinned / total if total else 0.0


def assert_holdout_is_t1(items: Sequence[TieredExample]) -> None:
    """The evaluation holdout is T1-only (ADRL-LRN-001 clause 2)."""
    offending = sorted({item.tier.value for item in items if not item.tier.enters_objective})
    if offending:
        raise PoolingError("holdout contains non-T1 tiers: " + ",".join(offending))


def verifier_precision_from_runs(
    verifier_version: str,
    run_results: Sequence[Sequence[VerificationResult]],
    tree_drift_flags: Sequence[bool] = (),
) -> VerifierPrecision:
    """Compute precision from repeated runs of the same verification (run x10 follow-up).

    repeat_run_agreement is the fraction of task groups whose non-indeterminate runs agree;
    flake_rate is the fraction of groups with at least one disagreement or indeterminate run.
    """
    groups = [list(group) for group in run_results if group]
    if not groups:
        return VerifierPrecision(verifier_version, 0.0, 1.0, 0.0, 0)
    agreeing = 0
    flaky = 0
    for group in groups:
        decided = [r for r in group if r is not VerificationResult.INDETERMINATE]
        if decided and len(set(decided)) == 1 and len(decided) == len(group):
            agreeing += 1
        else:
            flaky += 1
    drift_rate = (
        sum(1 for flag in tree_drift_flags if flag) / len(tree_drift_flags)
        if tree_drift_flags
        else 0.0
    )
    return VerifierPrecision(
        verifier_version=verifier_version,
        repeat_run_agreement=agreeing / len(groups),
        flake_rate=flaky / len(groups),
        tree_drift_rate=drift_rate,
        runs=sum(len(g) for g in groups),
    )


# ledger reader --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class EventNames:
    """Event type names the reader looks for; the ledger builder owns the real names."""

    outcome: str = "outcome"
    verification: str = "verification"
    label: str = "label"
    counterfactual: str = "counterfactual"


def _payload(row: sqlite3.Row) -> dict[str, Any]:
    try:
        data = json.loads(row["payload_json"])
    except (TypeError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _enum_or_none(enum_cls: Any, value: Any) -> Any:
    if value is None:
        return None
    try:
        return enum_cls(value)
    except ValueError:
        return None


class LedgerExampleReader:
    """Build examples from decisions plus their events, tolerating unknown fields."""

    def __init__(self, store: LedgerStore, names: EventNames | None = None) -> None:
        self._store = store
        self._names = names or EventNames()

    def read(self, *, limit: int | None = None) -> list[Example]:
        sql = "SELECT * FROM decisions ORDER BY ts, route_id"
        if limit is not None:
            sql += f" LIMIT {int(limit)}"
        examples: list[Example] = []
        for row in self._store.read(sql):
            examples.append(self._example_from_row(row))
        return examples

    def _example_from_row(self, row: sqlite3.Row) -> Example:
        events = self._store.read_events(row["route_id"])
        outcome_state = OutcomeState.PENDING
        failure_type: FailureType | None = None
        source: ExampleSource = "organic"
        harness_success: bool | None = None
        verification: VerificationResult | None = None
        tree_drift = False
        verifier_version: str | None = None
        for event in events:
            kind = event["event_type"]
            payload = _payload(event)
            if kind == self._names.outcome:
                state = _enum_or_none(OutcomeState, payload.get("state"))
                if state is not None:
                    outcome_state = state
                failure = _enum_or_none(FailureType, payload.get("failure_type"))
                if failure is not None:
                    failure_type = failure
                if payload.get("source") in _FAMILY_BY_SOURCE:
                    source = payload["source"]
                if "harness_reported_success" in payload:
                    harness_success = bool(payload["harness_reported_success"])
            elif kind == self._names.label:
                failure = _enum_or_none(FailureType, payload.get("failure_type"))
                if failure is not None:
                    failure_type = failure
            elif kind == self._names.verification:
                result = _enum_or_none(VerificationResult, payload.get("result"))
                if result is not None and result is not VerificationResult.INDETERMINATE:
                    verification = result
                    tree_drift = bool(payload.get("tree_drift", False))
                    verifier_version = payload.get("verifier_version")
                elif verification is None and result is not None:
                    verification = result
            elif kind == self._names.counterfactual:
                source = "counterfactual"
        try:
            features = json.loads(row["features_json"])
        except (TypeError, ValueError):
            features = {}
        try:
            context = json.loads(row["context_json"])
        except (TypeError, ValueError):
            context = {}
        explore_version = row["explore_version"]
        if explore_version is not None and source == "organic":
            source = "explore"
        return Example(
            route_id=RouteId(row["route_id"]),
            session_hmac=SessionId(row["session_hmac"]),
            decision_ts=row["ts"],
            rung=Rung(row["decided_rung"]),
            features=features if isinstance(features, dict) else {},
            features_version=row["features_version"],
            source=source,
            outcome_state=outcome_state,
            failure_type=failure_type,
            verification=verification,
            tree_drift=tree_drift,
            verifier_version=verifier_version,
            harness_reported_success=harness_success,
            propensity=float(row["propensity"]),
            explore_version=explore_version,
            pinned=bool(context.get("pinned", False)),
            privacy_suppressed=bool(context.get("privacy_suppressed", False)),
            repo_class=features.get("repo_class") if isinstance(features, dict) else None,
            intent_class=features.get("intent_class") if isinstance(features, dict) else None,
        )

FILE /Users/arunmenon/projects/adrl-core/tools/run_routing_lab.py
"""Synthetic routing workbench. Primary: ADRL-EVL-005.

Secondary: ADRL-RTG-002, ADRL-MEM-001, ADRL-SEM-007. Real composed stages,
synthetic Messages client and endpoint, disposable ledgers, no learned authority.
This developer tool deliberately has no real endpoint, credential or harness option.
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import hashlib
import json
import logging
import os
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Literal
from uuid import uuid4

import httpx
import structlog
from pydantic import BaseModel, ConfigDict, Field, model_validator
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from adrl.app import build_components
from adrl.config.loaders import load_bundle
from adrl.config.settings import Settings
from adrl.core.enums import RoutingMode
from adrl.gates.workload import HEADER_WORKLOAD_ASSERTION, RepoInventory, sign_assertion
from adrl.proxy.asgi import build_asgi
from check_all import ROOT, source_manifest

FIXTURE = ROOT / "tests/fixtures/wire/user_turn.json"


class Case(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    id: str = Field(pattern=r"^[a-z][a-z0-9_-]{0,63}$")
    family: str = Field(min_length=1, max_length=80)
    session: str = Field(pattern=r"^[a-z][a-z0-9_-]{0,63}$")
    prompt: str = Field(min_length=1, max_length=2000)
    context_chars: int = Field(default=0, ge=0, le=700_000)
    tool_repeats: int = Field(default=0, ge=0, le=4)
    tool_result: Literal["clean", "secret", "oversize"] = "clean"
    endpoint: Literal["reported", "missing_identity", "error"] = "reported"
    profile: Literal["messages_fixture", "responses_unqualified"] = "messages_fixture"
    stream: bool = True


class Suite(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    schema_version: Literal["adrl-routing-lab-suite-v1"]
    evidence_origin: Literal["curated_synthetic"]
    question: str = Field(min_length=1, max_length=1000)
    cases: tuple[Case, ...] = Field(min_length=1, max_length=24)

    @model_validator(mode="after")
    def unique_ids(self) -> Suite:
        if len({c.id for c in self.cases}) != len(self.cases):
            raise ValueError("case IDs must be unique")
        return self


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def append_event(out: Path, event: dict[str, Any]) -> None:
    """Durable append; manifest supplies the denominator after interruption."""
    with (out / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"at": datetime.now(UTC).isoformat(), **event}) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(value, indent=2) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def summary(out: Path) -> dict[str, Any]:
    manifest = json.loads((out / "manifest.json").read_text())
    rows = {
        c["id"]: {"case_id": c["id"], "state": "not_started"} for c in manifest["suite"]["cases"]
    }
    truncated = False
    journal = out / "events.jsonl"
    if journal.exists():
        lines = journal.read_text().splitlines()
        for index, line in enumerate(lines):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                if index != len(lines) - 1:
                    raise ValueError("corrupt non-tail journal record") from None
                truncated = True
                break
            if event["type"] == "started":
                rows[event["case_id"]] = {"case_id": event["case_id"], "state": "indeterminate"}
            elif event["type"] == "finished":
                rows[event["case_id"]] = event["result"]
    counts = dict(Counter(row["state"] for row in rows.values()))
    return {
        "experiment_id": manifest["experiment_id"],
        "execution_mode": "simulation",
        "source": "synthetic",
        "evidence_tier": "T4",
        "evidence_origin": "curated_synthetic",
        "eligible_for_learning": False,
        "planned": len(rows),
        "counts": counts,
        "truncated_tail": truncated,
        "rows": list(rows.values()),
        "model_calls": 0,
        "task_success": None,
        "measured_provider_cost": None,
    }


def make_body(case: Case) -> dict[str, Any]:
    body = copy.deepcopy(json.loads(FIXTURE.read_text())["body"])
    body["stream"] = case.stream
    body["messages"] = [{"role": "user", "content": [{"type": "text", "text": case.prompt}]}]
    if case.context_chars:
        body["system"].append({"type": "text", "text": "x" * case.context_chars})
    for index in range(case.tool_repeats):
        result = {
            "clean": "same synthetic file content",
            "secret": "AWS_KEY=AKIAIOSFODNN7EXAMPLE",
            "oversize": "x" * 700_000,
        }[case.tool_result]
        body["messages"].extend(
            [
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": f"lab-{index}",
                            "name": "Read",
                            "input": {"file_path": "README.md"},
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": f"lab-{index}", "content": result}
                    ],
                },
            ]
        )
    return body


class SyntheticEndpoint:
    """Controlled in-process response source; records actual received request bytes."""

    def __init__(self) -> None:
        self.mode = "reported"
        self.received: list[dict[str, Any]] = []

    async def messages(self, request: Request) -> Response:
        raw = await request.body()
        body = json.loads(raw)
        self.received.append(
            {
                "body_sha256": digest(raw),
                "model": body.get("model"),
                "stream": body.get("stream"),
                "path": request.url.path,
            }
        )
        if self.mode == "error":
            return JSONResponse(
                {
                    "type": "error",
                    "error": {"type": "api_error", "message": "Synthetic upstream failure"},
                },
                status_code=503,
            )
        model = str(body["model"]) if self.mode == "reported" else None
        headers = {"x-litellm-model-id": str(model)} if model else {}
        message = {
            "id": "msg_lab",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": "Synthetic response; no task executed."}],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 0, "output_tokens": 0},
        }
        if model:
            message["model"] = model
        if not body.get("stream"):
            return JSONResponse(message, headers=headers)
        start = {**message, "content": [], "stop_reason": None}
        events = [
            ("message_start", {"type": "message_start", "message": start}),
            (
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "text", "text": ""},
                },
            ),
            (
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": "Synthetic response."},
                },
            ),
            ("content_block_stop", {"type": "content_block_stop", "index": 0}),
            (
                "message_delta",
                {
                    "type": "message_delta",
                    "delta": {"stop_reason": "end_turn"},
                    "usage": {"output_tokens": 0},
                },
            ),
            ("message_stop", {"type": "message_stop"}),
        ]
        payload = "".join(f"event: {name}\ndata: {json.dumps(data)}\n\n" for name, data in events)
        return Response(payload, media_type="text/event-stream", headers=headers)


def lab_settings(directory: Path) -> Settings:
    # Supply every field explicitly so environment cannot enable a classifier,
    # remote anchor, live ledger, tokenizer download or alternative configuration.
    defaults = {
        name: field.get_default(call_default_factory=True)
        for name, field in Settings.model_fields.items()
    }
    return Settings(
        **(
            defaults
            | {
                "config_dir": ROOT / "config",
                "data_dir": directory,
                "ledger_path": directory / "synthetic.db",
                "egress_ledger_path": directory / "egress.db",
                "keystore_path": directory / "keys",
                "gateway_base_url": "http://lab.invalid",
                "gateway_health_enabled": False,
                "routing_mode": RoutingMode.LIVE,
                "fallback_mode": RoutingMode.LIVE,
            }
        )
    )


async def execute(suite: Suite, out: Path) -> None:
    endpoint = SyntheticEndpoint()
    app = Starlette(routes=[Route("/v1/messages", endpoint.messages, methods=["POST"])])
    with TemporaryDirectory(prefix="adrl-synthetic-lab-") as directory:
        settings = lab_settings(Path(directory))
        # Existing integration-test pattern; impossible to select a network transport here.
        bundle = load_bundle(settings.model_copy(update={"routing_mode": RoutingMode.SHADOW}))
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://lab.invalid", trust_env=False
        ) as gateway:
            components = build_components(settings, bundle=bundle, gateway_client=gateway)
            try:
                if not all(components.installed.values()):
                    raise RuntimeError("required real component missing")
                inventory = RepoInventory(
                    root=str(ROOT),
                    remote=None,
                    head="synthetic-only",
                    fingerprint="e" * 64,
                    tracked_files=1,
                )
                assertion = sign_assertion(inventory, components.keystore.hmac_key())
                write_new(
                    out / "environment.json",
                    {
                        "config_versions": bundle.versions,
                        "installed": components.installed,
                        "harness_binary_version": None,
                        "model_revision": None,
                        "repo_snapshot": None,
                        "client": "synthetic Claude Code Messages fixture; no harness executed",
                        "endpoint": "in-process synthetic ASGI",
                        "health": "static fixture health",
                        "workload_assertion": "synthetic development-repository identity",
                        "live_config_admitted": False,
                        "config_load_mode": "shadow",
                        "pipeline_mode": "live inside in-process simulation only",
                        "config_evidence_bypass": "test-only bundle; no provider transport",
                    },
                )
                async with httpx.AsyncClient(
                    transport=httpx.ASGITransport(app=build_asgi(components.pipeline)),
                    base_url="http://adrl.invalid",
                    trust_env=False,
                ) as client:
                    for case in suite.cases:
                        append_event(out, {"type": "started", "case_id": case.id})
                        result: dict[str, Any] = {"case_id": case.id, "state": "unsupported"}
                        if case.profile == "responses_unqualified":
                            result["reason"] = (
                                "Responses and a real Codex harness are unqualified here"
                            )
                            append_event(
                                out, {"type": "finished", "case_id": case.id, "result": result}
                            )
                            continue
                        before = len(endpoint.received)
                        last_seq = components.store.read(
                            "SELECT COALESCE(MAX(seq),0) AS n FROM events"
                        )[0]["n"]
                        raw = json.dumps(make_body(case)).encode()
                        endpoint.mode = case.endpoint
                        try:
                            response = await asyncio.wait_for(
                                client.post(
                                    "/v1/messages",
                                    content=raw,
                                    headers={
                                        "content-type": "application/json",
                                        "anthropic-version": "2023-06-01",
                                        "x-claude-code-session-id": f"lab-{case.session}",
                                        HEADER_WORKLOAD_ASSERTION: assertion,
                                    },
                                ),
                                timeout=30,
                            )
                            await components.pipeline.drain()
                            events = [
                                {**dict(row), "payload": json.loads(row["payload_json"])}
                                for row in components.store.read(
                                    "SELECT * FROM events WHERE seq>? ORDER BY seq", (last_seq,)
                                )
                            ]
                            for event in events:
                                event.pop("payload_json")
                            route_ids = sorted({e["route_id"] for e in events if e["route_id"]})
                            decisions = [
                                dict(row)
                                for route_id in route_ids
                                for row in components.store.read(
                                    "SELECT * FROM decisions WHERE route_id=?", (route_id,)
                                )
                            ]
                            dispatched = endpoint.received[before:]
                            result.update(
                                state=(
                                    "responded"
                                    if response.status_code < 400
                                    else "upstream_error"
                                    if dispatched
                                    else "blocked"
                                ),
                                http_status=response.status_code,
                                input_sha256=digest(raw),
                                response_sha256=digest(response.content),
                                decisions=decisions,
                                events=events,
                                dispatched=dispatched,
                                synthetic_receipt=True,
                                eligible_for_learning=False,
                            )
                        except Exception as exc:
                            result.update(
                                state="indeterminate",
                                error_type=type(exc).__name__,
                                dispatched=endpoint.received[before:],
                            )
                            append_event(
                                out, {"type": "finished", "case_id": case.id, "result": result}
                            )
                            # State may be inconsistent. Leave remaining planned cases not_started.
                            raise
                        append_event(
                            out, {"type": "finished", "case_id": case.id, "result": result}
                        )
            finally:
                await components.aclose()


def write_report(out: Path, report: dict[str, Any]) -> None:
    """Readable view keeps original selection separate from current dispatch."""
    lines = [
        "# Routing lab: actual choices, synthetic execution",
        "",
        "Real ADRL stages ran against a controlled in-process endpoint. No harness or model",
        "executed a coding task. Receipt identity is synthetic. No quality or savings measured.",
        "",
        "A continuation keeps its original route ID and initial choice. Its dispatched tier",
        "can change through cascade or privacy enforcement. Read both columns together.",
        "",
        "| Case | Initial choice | Dispatched tier | Endpoint received | Identity source | State |",
        "|---|---|---|---|---|---|",
    ]
    for row in report["rows"]:
        decisions = row.get("decisions", [])
        requests = [e["payload"] for e in row.get("events", []) if e["event_type"] == "request"]
        served = [e["payload"] for e in row.get("events", []) if e["event_type"] == "served"]
        received = row.get("dispatched", [])
        values = [
            row["case_id"],
            decisions[0]["decided_rung"] if decisions else "-",
            requests[-1]["target_rung"] if requests else "-",
            str(received[-1]["model"]) if received else "no dispatch",
            served[-1]["served_source"] if served else "-",
            row["state"],
        ]
        lines.append("| " + " | ".join(values) + " |")
    lines.extend(
        [
            "",
            f"Planned cells: {report['planned']}. Accounting: {json.dumps(report['counts'])}.",
            "",
            "Task definitions: [manifest](manifest.json). Every event: [journal](events.jsonl).",
            "Full decisions/features and receipts: [results](results.json).",
            "Fixture/config qualifications: [environment](environment.json).",
            "",
            "These exports are curated synthetic T4 diagnostics, ineligible for learning.",
            "The manifest retains planned cells; --inspect reports interrupted work.",
        ]
    )
    with (out / "report.md").open("x", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--inspect", type=Path, help="Read all planned attempts, including interrupted ones"
    )
    args = parser.parse_args()
    if args.inspect:
        if args.suite or args.out:
            parser.error("--inspect cannot be combined with --suite or --out")
        print(json.dumps(summary(args.inspect), indent=2))
        return 0
    if args.suite is None or args.out is None:
        parser.error("--suite and --out are required")
    data = args.suite.read_bytes()
    suite = Suite.model_validate_json(data)
    out = args.out.resolve()
    if out == ROOT or ROOT in out.parents:
        parser.error("output must be outside the runtime repository")
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700, exist_ok=False)
    before = source_manifest(ROOT)
    write_new(
        out / "manifest.json",
        {
            "schema_version": "adrl-routing-lab-run-v1",
            "experiment_id": str(uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
            "suite": suite.model_dump(mode="json"),
            "suite_sha256": digest(data),
            "source_manifest": before,
            "eligible_for_learning": False,
            "execution_mode": "simulation",
            "source": "synthetic",
            "evidence_tier": "T4",
            "evidence_origin": "curated_synthetic",
        },
    )
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.CRITICAL))
    failed = False
    try:
        asyncio.run(execute(suite, out))
    except (Exception, KeyboardInterrupt) as exc:
        failed = True
        append_event(out, {"type": "run_interrupted", "error_type": type(exc).__name__})
    after = source_manifest(ROOT)
    report = summary(out)
    report["source_unchanged_during_run"] = before == after
    report["run_completed"] = not failed and before == after
    write_new(out / "results.json", report)
    write_report(out, report)
    print(
        json.dumps({k: report[k] for k in ("experiment_id", "counts", "run_completed")}, indent=2)
    )
    return 1 if failed or before != after else 0


if __name__ == "__main__":
    raise SystemExit(main())

FILE /Users/arunmenon/projects/adrl-core/config/repo-classification-v1.json
{
  "version": "repo-classification-v1",
  "owner": "security",
  "default_class_id": "default",
  "classes": [
    {
      "class_id": "default",
      "allowed_rungs": [
        "local",
        "cheap_cloud"
      ],
      "residency": null,
      "release_permitted": true,
      "restricted": false
    },
    {
      "class_id": "open",
      "allowed_rungs": [
        "local",
        "cheap_cloud",
        "frontier"
      ],
      "residency": null,
      "release_permitted": true,
      "restricted": false
    },
    {
      "class_id": "residency-eu",
      "residency": "eu",
      "release_permitted": true,
      "restricted": false
    },
    {
      "class_id": "restricted",
      "allowed_rungs": [
        "local"
      ],
      "residency": null,
      "release_permitted": false,
      "restricted": true
    }
  ],
  "repos": [
    {
      "repo_id": "adrl-core",
      "match": "/Users/arunmenon/projects/adrl-core",
      "class_id": "open",
      "restricted_path_prefixes": []
    },
    {
      "repo_id": "payments-core-example",
      "match": "git@github.example.com:payments/core",
      "class_id": "restricted",
      "restricted_path_prefixes": []
    }
  ],
  "unknown_identity_policy": "local_only"
}

FILE /Users/arunmenon/projects/adrl-core/tests/integration/e2e/test_outcome_contract.py
"""ADRL-MEM-002: persisted cascade outcomes reach the canonical lifecycle consumers.

Synthetic ASGI transport only. The shared E2E fixture loads SHADOW configuration into
LIVE components; these tests do not qualify live configuration admission or real traffic.
"""

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from adrl.cascade.controller import CascadeController
from adrl.cascade.sticky import MemoryStateProvider
from adrl.config.models import CloseRule
from adrl.core.enums import FailureType, OutcomeState
from adrl.core.ids import RouteId
from adrl.core.types import LedgerEvent
from adrl.ledger.events import OUTCOME_EVENT, read_stored_events
from adrl.ledger.outcomes import Closer, read_projection, routes_in_state
from adrl.ledger.readiness import learning_readiness
from adrl.ledger.store import LedgerStore
from adrl.proxy.pipeline import _Turn
from adrl.telemetry.metrics import EVENT_DROPPED_TOTAL
from adrl.wire.observe import ResponseObservation
from tests.unit.routing.helpers import make_ctx, make_gate, make_obs, user_body

from .conftest import E2E, user_turn_body


async def test_composed_outcomes_close_once_without_inventing_success(live: E2E) -> None:
    await live.send("user_turn", body=user_turn_body("Fix the typo in README.md"))
    first = RouteId(live.decisions()[0]["route_id"])
    await live.send("user_turn", body=user_turn_body("Fix another typo in README.md"))
    second = RouteId(live.decisions()[1]["route_id"])
    assert [e.route_id for e in routes_in_state(live.store, OutcomeState.CLOSED_TURN)] == [first]
    events = read_stored_events(live.store, first, OUTCOME_EVENT)
    assert [e.payload["state"] for e in events] == ["pending", "closed_turn"]
    assert all(
        e.event.producer == "cascade" and e.event.schema_version == "events-v1" for e in events
    )
    assert [e.event.producer_seq for e in events] == [1, 2]
    assert all(e.payload.get("harness_reported_success") is None for e in events)
    assert events[-1].payload["session_hmac"] == live.decisions()[0]["session_hmac"]
    assert read_projection(live.store, second).state is OutcomeState.PENDING
    closer = Closer(live.store, CloseRule(subsequent_turns=100, idle_minutes=30))
    future = datetime.now(UTC) + timedelta(days=1)
    assert await closer.scan(now=future) == [(first, "idle")]
    assert await closer.scan(now=future) == []
    projected = read_projection(live.store, first)
    assert projected.state is OutcomeState.CLOSED_FINAL
    assert projected.label.failure_type is FailureType.UNVERIFIABLE
    assert projected.label.result == "excluded"
    assert len(live.store.read_events(first, "label")) == 1
    readiness = learning_readiness(live.store)
    assert readiness.closed_final_count == 1
    assert readiness.censored_count == 1
    assert readiness.capability_evidence_count == readiness.verified_success_count == 0
    assert readiness.window_blocked and "no_capability_evidence" in readiness.blockers


@pytest.mark.parametrize(
    "status,cause", [(503, FailureType.INFRASTRUCTURE), (400, FailureType.INFRASTRUCTURE)]
)
async def test_terminal_cause_survives_next_turn_and_close(
    live: E2E, status: int, cause: FailureType
) -> None:
    live.gateway_state.status_code = status
    response = await live.send("user_turn")
    assert response.status_code == status
    first = RouteId(live.decisions()[0]["route_id"])
    assert read_projection(live.store, first).state is OutcomeState.CLOSED_TURN
    live.gateway_state.status_code = 200
    await live.send("user_turn", body=user_turn_body("Fix the typo in README.md"))
    closed = [
        e
        for e in read_stored_events(live.store, first, OUTCOME_EVENT)
        if e.payload["state"] == "closed_turn"
    ]
    assert len(closed) == 2
    assert closed[0].payload["failure_type"] == cause.value
    assert closed[-1].payload["reason"] == "next_user_turn"
    await Closer(live.store, CloseRule(subsequent_turns=100, idle_minutes=30)).scan(
        now=datetime.now(UTC) + timedelta(days=1)
    )
    label = read_projection(live.store, first).label
    assert label.result == "excluded" and label.failure_type is cause
    assert learning_readiness(live.store).capability_evidence_count == 0


async def test_completed_400_stays_unverifiable(live: E2E) -> None:
    controller = CascadeController(
        live.components.bundle, MemoryStateProvider(), ledger=live.components.facade
    )
    ctx = make_ctx(user_body())
    decision = await live.components.router.decide(ctx, make_gate(), None)
    plan = await controller.plan(ctx, decision, make_gate(), None)
    await controller.observe(ctx, plan, make_obs(status=400, completed=True))
    projected = read_projection(live.store, decision.route_id)
    assert projected.state is OutcomeState.CLOSED_TURN
    assert projected.label.failure_type is FailureType.UNVERIFIABLE
    assert not projected.label.is_capability_evidence


@pytest.mark.parametrize("forwarded", [False, True])
async def test_continuation_terminal_event_preserves_identity(
    live: E2E, monkeypatch: pytest.MonkeyPatch, forwarded: bool
) -> None:
    await live.send("user_turn")
    route = RouteId(live.decisions()[0]["route_id"])
    finalize = live.components.pipeline._finalize
    different_route = RouteId("different-current-decision")
    assert different_route != route

    async def divergent_finalization(turn: _Turn, obs: ResponseObservation) -> None:
        assert turn.plan.route_id == route
        # Force divergence at the stage boundary: ordinary continuations inherit identity.
        altered = replace(turn, decision=replace(turn.decision, route_id=different_route))
        assert altered.decision.route_id != altered.plan.route_id
        await finalize(altered, obs)

    monkeypatch.setattr(live.components.pipeline, "_finalize", divergent_finalization)
    if forwarded:
        # Only observe-phase fallback is supported; plan-phase persistence requires a ledger.
        monkeypatch.setattr(live.components.cascade, "_ledger", None)
    live.gateway_state.status_code = 503
    await live.send("continuation")
    closed = routes_in_state(live.store, OutcomeState.CLOSED_TURN)
    assert len(closed) == 1 and closed[0].route_id == route
    assert closed[0].event.producer == "cascade"
    assert closed[0].event.producer_seq == 2
    assert closed[0].event.schema_version == "events-v1"
    assert closed[0].payload["failure_type"] == "infrastructure"


async def test_restart_sequence_includes_legacy_events(live: E2E) -> None:
    ctx = make_ctx(user_body())
    decision = await live.components.router.decide(ctx, make_gate(), None)
    legacy = LedgerEvent(decision.route_id, "pending", "cascade", 77, {"legacy": True})
    await live.components.facade.append_event(legacy)
    controller = CascadeController(
        live.components.bundle, MemoryStateProvider(), ledger=live.components.facade
    )
    await controller.plan(ctx, decision, make_gate(), None)
    events = read_stored_events(live.store, decision.route_id)
    assert events[0].event == legacy
    assert events[-1].event_type == OUTCOME_EVENT
    assert events[-1].event.producer_seq == 78
    assert events[-1].payload["state"] == "pending"


async def test_legacy_only_route_is_absent_from_readiness(live: E2E) -> None:
    route = RouteId("legacy-only")
    await live.components.facade.append_event(
        LedgerEvent(route, "closed_turn", "cascade", 1, {"reason": "historical"})
    )
    assert routes_in_state(live.store, OutcomeState.CLOSED_TURN) == []
    report = learning_readiness(live.store)
    assert report.closed_final_count == report.censored_count == 0
    assert read_projection(live.store, route).state is None


@pytest.mark.parametrize("trigger", ["subsequent_turns", "episode_boundary"])
async def test_context_identity_enables_closing_triggers(live: E2E, trigger: str) -> None:
    await live.send("user_turn")
    first = RouteId(live.decisions()[0]["route_id"])
    await live.send("user_turn", body=user_turn_body("Fix another typo"))
    if trigger == "subsequent_turns":
        await live.send("user_turn", body=user_turn_body("Fix a third typo"))
    else:
        await live.store.write_through(
            LedgerStore.insert_lineage_event(
                live.decisions()[0]["lineage_hmac"], "episode_boundary", {"signal": "clear"}
            )
        )
    rule = CloseRule(
        subsequent_turns=1 if trigger == "subsequent_turns" else 100, idle_minutes=10000
    )
    closed = await Closer(live.store, rule).scan()
    assert (first, trigger) in closed


async def test_dropped_forwarded_event_is_observable(
    live: E2E, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    await live.send("user_turn")
    monkeypatch.setattr(live.components.cascade, "_ledger", None)
    append = live.components.facade.append_event

    async def reject_outcome(event: LedgerEvent) -> bool:
        if event.event_type == OUTCOME_EVENT and event.producer == "cascade":
            return False
        return await append(event)

    monkeypatch.setattr(live.components.facade, "append_event", reject_outcome)
    metric = EVENT_DROPPED_TOTAL.labels(producer="cascade")
    before = metric._value.get()
    live.gateway_state.status_code = 503
    await live.send("continuation")
    assert metric._value.get() == before + 1
    output = capsys.readouterr().out
    assert "event_dropped" in output and "finalize_failed" not in output

FILE /Users/arunmenon/projects/.adrl-execution-state/rv-reconciliation-20260910/comparison.json
{
  "historical_check_status": "passed",
  "historical_changed_inputs": [],
  "checks_passed": true,
  "current_differences": {
    "AGENTS.md": {
      "reviewed": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490",
      "current": "5e182174b281e0be16dc23354ad2ceece44e63f8e2b02599af8a4a9430ee1e65"
    },
    "CLAUDE.md": {
      "reviewed": "b5fd37e36c52874192a3e87966822cd0d7ea0ef789a3e47e9fc9f9bc3120a490",
      "current": "13fcfc1e216a1ccd467f11030db96ee3a70c56e3f5cc971cccc7bb0d1827d0ee"
    },
    "src/adrl/proxy/pipeline.py": {
      "reviewed": "68a170c352ad7793113626002be84608f9c656740280156405682040407b152f",
      "current": "300069be159da6ec62b42cac934f4ab834b87cbb34d78cdfd0f01d287f20b3af"
    }
  }
}

FILE /Users/arunmenon/projects/.adrl-execution-state/rv-reconciliation-20260910/current-test.json
{
  "actor": "coordinator:codex",
  "argv": [
    "../adrl-core/.venv/bin/python",
    "-m",
    "pytest",
    "-q",
    "tests/integration/e2e/test_outcome_contract.py"
  ],
  "cwd": "/Users/arunmenon/projects/adrl-core",
  "exit_code": 0,
  "result": "11 passed in 0.61s",
  "capture": "Codex exec session 52358; coordinator transcript, not raw pytest log",
  "test_sha256": "b19cd9e234079e3076b966113b89dbb41f074922342ed0d0e639155baa48cc1b"
}

FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/fable-retrospective-2026-09-08/findings.json
{
 "schema": "review-ledger-v1",
 "review_id": "fable-retrospective-2026-09-08",
 "findings": [
  {
   "id": "RV-01",
   "global_id": "fable-retrospective-2026-09-08:RV-01",
   "severity": "critical",
   "kind": "observed defect",
   "blocking": true,
   "confidence": "high",
   "owning_adrs": [
    "MEM-001",
    "MEM-002",
    "MEM-004",
    "LRN-001"
   ],
   "title": "Live outcome events are invisible to every consumer that turns a decision into a label.",
   "appendix_refs": "EL D1, M1."
  },
  {
   "id": "RV-02",
   "global_id": "fable-retrospective-2026-09-08:RV-02",
   "severity": "high",
   "kind": "observed defect",
   "blocking": true,
   "confidence": "high",
   "owning_adrs": [
    "RTG-002",
    "RTG-003",
    "RTG-006"
   ],
   "title": "The estimator, thresholds and cost model never influence the initial route; cheap cloud is never chosen on merit.",
   "appendix_refs": "RT F1, U2, U3, M3."
  },
  {
   "id": "RV-03",
   "global_id": "fable-retrospective-2026-09-08:RV-03",
   "severity": "high",
   "kind": "observed defect",
   "blocking": true,
   "confidence": "high",
   "owning_adrs": [
    "TRU-001",
    "OPS-005",
    "EVL-005"
   ],
   "title": "Lab routing evidence and the 911-test result depend on the author's absolute checkout path.",
   "appendix_refs": "RT F2, W3 F7, CH."
  },
  {
   "id": "RV-04",
   "global_id": "fable-retrospective-2026-09-08:RV-04",
   "severity": "high",
   "kind": "unsupported claim",
   "blocking": true,
   "confidence": "high",
   "owning_adrs": [
    "FND-005",
    "OPS-005",
    "RTG-001"
   ],
   "title": "The lab reaches live dispatch by loading the bundle in shadow mode, and the reports do not say so.",
   "appendix_refs": "RT F3, U1."
  },
  {
   "id": "RV-05",
   "global_id": "fable-retrospective-2026-09-08:RV-05",
   "severity": "high",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "RTG-003",
    "CAS-001"
   ],
   "title": "Rule health and trip-wire coverage read a third event shape that no runtime producer writes.",
   "appendix_refs": "EL D2."
  },
  {
   "id": "RV-06",
   "global_id": "fable-retrospective-2026-09-08:RV-06",
   "severity": "high",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "MEM-002",
    "LRN-001"
   ],
   "title": "Late human corrections update the ledger label but never reach learning examples.",
   "appendix_refs": "EL D3; D4 records the verifier-immune variant."
  },
  {
   "id": "RV-07",
   "global_id": "fable-retrospective-2026-09-08:RV-07",
   "severity": "high",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "LRN-001",
    "MEM-003",
    "EVL-004"
   ],
   "title": "T1 evidence is unreachable because nothing produces a verifier-precision record.",
   "appendix_refs": "EL D6, M2."
  },
  {
   "id": "RV-08",
   "global_id": "fable-retrospective-2026-09-08:RV-08",
   "severity": "high",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "LRN-004",
    "LRN-005",
    "LRN-008"
   ],
   "title": "Every organic decision since W7.0a is untrainable and unexplorable.",
   "appendix_refs": "EL D7; RT F7 records that the v1 contract's feature list already did not match what `compute_features` emits."
  },
  {
   "id": "RV-09",
   "global_id": "fable-retrospective-2026-09-08:RV-09",
   "severity": "high",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "LRN-004",
    "MEM-007"
   ],
   "title": "The neighbour success feature reports success for verifier-failed routes.",
   "appendix_refs": "EL D5."
  },
  {
   "id": "RV-10",
   "global_id": "fable-retrospective-2026-09-08:RV-10",
   "severity": "high",
   "kind": "strategic disagreement for the stated next action",
   "blocking": true,
   "confidence": "high",
   "owning_adrs": [
    "SAF-007",
    "OPS-001",
    "FND-005"
   ],
   "title": "The isolated backend cannot host a real harness, so the roadmap's next W3 step does not lead to a real-task demonstration.",
   "appendix_refs": "W3 F1 and section 6; RC."
  },
  {
   "id": "RV-11",
   "global_id": "fable-retrospective-2026-09-08:RV-11",
   "severity": "high",
   "kind": "unsupported claim",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "SAF-007",
    "MEM-003"
   ],
   "title": "No code extracts output from a stopped container, so \"the retained layer\" is not task-output evidence.",
   "appendix_refs": "W3 F4."
  },
  {
   "id": "RV-12",
   "global_id": "fable-retrospective-2026-09-08:RV-12",
   "severity": "high",
   "kind": "unsupported claim",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "EVL-007 and each affected decision"
   ],
   "title": "Thirteen to sixteen historical D3 and D4 grades are displayed as current although EVL-007 says a new implementation inherits nothing above D2.",
   "appendix_refs": "AA F6, LC F2."
  },
  {
   "id": "RV-13",
   "global_id": "fable-retrospective-2026-09-08:RV-13",
   "severity": "high",
   "kind": "observed process defect for every \"validated\" label",
   "blocking": true,
   "confidence": "high",
   "owning_adrs": [
    "EVL-007",
    "OPS-008"
   ],
   "title": "No independent reviewer has been named in twenty-one journey entries although the W0 exit required it.",
   "appendix_refs": "LC F11, RG guardrail table."
  },
  {
   "id": "RV-14",
   "global_id": "fable-retrospective-2026-09-08:RV-14",
   "severity": "high",
   "kind": "unsupported claim",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "MEM-008",
    "MEM-005",
    "MEM-007"
   ],
   "title": "MEM-008 \"runs against real traffic, 34 of 300 evaluated decisions\" describes the old codebase; adrl-core never instantiates the retriever.",
   "appendix_refs": "EL U1, D8."
  },
  {
   "id": "RV-15",
   "global_id": "fable-retrospective-2026-09-08:RV-15",
   "severity": "high",
   "kind": "unsupported claim",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "LRN-007",
    "EVL-005"
   ],
   "title": "The improvement experiment's headline overstates a tautological result.",
   "appendix_refs": "EL U2."
  },
  {
   "id": "RV-16",
   "global_id": "fable-retrospective-2026-09-08:RV-16",
   "severity": "high",
   "kind": "unsupported claim",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "RTG-003",
    "LRN-004",
    "EVL-002"
   ],
   "title": "The routing-correction record omits that candidate 2 was fitted to the two literals that failed candidate 1, that the fresh 12 matched the author's expectations 12 of 12, and that two changes shipped under one defect story; the regression tests mirror the evaluation cases.",
   "appendix_refs": "EL U3, D10; RT S1."
  },
  {
   "id": "RV-17",
   "global_id": "fable-retrospective-2026-09-08:RV-17",
   "severity": "medium",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "LRN-004",
    "RTG-003"
   ],
   "title": "features-v2 introduced over-routing classes the record does not name, with no over-route budget.",
   "appendix_refs": "RT F4, M6, S1; S2 notes destructive-intent vocabulary routes \"fix the typo in payments.py\" to frontier."
  },
  {
   "id": "RV-18",
   "global_id": "fable-retrospective-2026-09-08:RV-18",
   "severity": "medium",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "RTG-003",
    "SEM-005"
   ],
   "title": "No outcome-driven adaptation is wired into the running service.",
   "appendix_refs": "RT F5, LC F5."
  },
  {
   "id": "RV-19",
   "global_id": "fable-retrospective-2026-09-08:RV-19",
   "severity": "medium",
   "kind": "evidence integrity",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "EVL-006",
    "OPS-004"
   ],
   "title": "Five frozen wave packets were amended after their hashes were recorded.",
   "appendix_refs": "W3 F2."
  },
  {
   "id": "RV-20",
   "global_id": "fable-retrospective-2026-09-08:RV-20",
   "severity": "medium",
   "kind": "evidence integrity",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "OPS-001",
    "SAF-007",
    "EVL-006"
   ],
   "title": "Engine evidence lives only in the private state directory and the eight engine tests have been skipped in every run since the 316-input build; the executive review's \"895 tests, no skipped tests\" is stale.",
   "appendix_refs": "W3 F3, AA F7, EL U4."
  },
  {
   "id": "RV-21",
   "global_id": "fable-retrospective-2026-09-08:RV-21",
   "severity": "medium",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "OPS-001"
   ],
   "title": "Permanent execution fences make every supervised workspace single-use.",
   "appendix_refs": "W3 F6."
  },
  {
   "id": "RV-22",
   "global_id": "fable-retrospective-2026-09-08:RV-22",
   "severity": "medium",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "MEM-010",
    "SAF-002"
   ],
   "title": "Materialised plaintext copies have no durable custody record.",
   "appendix_refs": "W3 F8."
  },
  {
   "id": "RV-23",
   "global_id": "fable-retrospective-2026-09-08:RV-23",
   "severity": "medium",
   "kind": "register defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "register rules in `R/AGENTS"
   ],
   "title": "INDEX rows are stale for 21 decisions although each 8 September changelog entry claims synchronisation; bucket overview tables are frozen at 2 September and lack SEM-007 and CAS-009; file fields and INDEX disagree for FND-001, FND-005, SEM-002, TRU-001; five planning notes lack changelog rows.",
   "appendix_refs": "AA F1, F3, F4, F5."
  },
  {
   "id": "RV-24",
   "global_id": "fable-retrospective-2026-09-08:RV-24",
   "severity": "medium",
   "kind": "register defect, concealed progress",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "Eleven Maturity fields describe defects that `C/docs/known-gaps.md` records as closed on 3 September.",
   "appendix_refs": "AA F2."
  },
  {
   "id": "RV-25",
   "global_id": "fable-retrospective-2026-09-08:RV-25",
   "severity": "medium",
   "kind": "leadership accuracy",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "Leadership artefacts are frozen at journey entry 014 while the program is at 021; the lab shows a synthetic endpoint with provider-receipt vocabulary; \"no immediate input blocks the next offline work\" omits four unmade leadership decisions; the deck's \"learning\" slide describes manual code edits.",
   "appendix_refs": "LC F1, F3, F4, F5."
  },
  {
   "id": "RV-26",
   "global_id": "fable-retrospective-2026-09-08:RV-26",
   "severity": "medium",
   "kind": "unsupported claim",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "OPS-006",
    "TRU-002"
   ],
   "title": "The served-identity debate concerns a header the runtime does not read.",
   "appendix_refs": "RG F1."
  },
  {
   "id": "RV-27",
   "global_id": "fable-retrospective-2026-09-08:RV-27",
   "severity": "medium",
   "kind": "missing coverage",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "CAS-004",
    "RTG-008"
   ],
   "title": "Thinking-block binding is per model version and per exact prefix, with 400 by default for accounts created on or after 31 August 2026; CAS-004 keys by family and nothing in the snapshot exercises the binding.",
   "appendix_refs": "RG F2."
  },
  {
   "id": "RV-28",
   "global_id": "fable-retrospective-2026-09-08:RV-28",
   "severity": "medium",
   "kind": "missing coverage",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "SEM-004",
    "RTG-009"
   ],
   "title": "Server-side compaction arrives inside the response and its tokens sit outside top-level usage; nothing sums `usage.iterations`, so cost accounting undercounts.",
   "appendix_refs": "RG F3."
  },
  {
   "id": "RV-29",
   "global_id": "fable-retrospective-2026-09-08:RV-29",
   "severity": "medium",
   "kind": "process defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "OPS-008",
    "EVL-009"
   ],
   "title": "W3.2b2d2 closed as validated despite recorded stop-rule deviations and a self-granted exception with no owner disposition.",
   "appendix_refs": "RG F6, W3 F5."
  },
  {
   "id": "RV-30",
   "global_id": "fable-retrospective-2026-09-08:RV-30",
   "severity": "medium",
   "kind": "strategic disagreement",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "FND-005",
    "OPS-001"
   ],
   "title": "Roughly half of the two-day engineering built a container execution backend that no product stage requires and that the W3 contract itself called optional.",
   "appendix_refs": "RC; CH."
  },
  {
   "id": "RV-31",
   "global_id": "fable-retrospective-2026-09-08:RV-31",
   "severity": "medium",
   "kind": "observed gap",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "Shadow retrieval, embedding writer, instruction hasher, projection index and human-correction detector are never composed outside tests, so MEM-005 suppression, MEM-007 staleness and MEM-008 measurement have never met traffic in this runtime.",
   "appendix_refs": "EL D8."
  },
  {
   "id": "RV-32",
   "global_id": "fable-retrospective-2026-09-08:RV-32",
   "severity": "medium",
   "kind": "evidence integrity",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [
    "EVL-006",
    "OPS-004"
   ],
   "title": "Validation records are overwritable and machine-bound.",
   "appendix_refs": "RG F7, EL U5."
  },
  {
   "id": "RV-33",
   "global_id": "fable-retrospective-2026-09-08:RV-33",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "RT F6, F7."
  },
  {
   "id": "RV-34",
   "global_id": "fable-retrospective-2026-09-08:RV-34",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "AA F8."
  },
  {
   "id": "RV-35",
   "global_id": "fable-retrospective-2026-09-08:RV-35",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "RG F4."
  },
  {
   "id": "RV-36",
   "global_id": "fable-retrospective-2026-09-08:RV-36",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "EL D9."
  },
  {
   "id": "RV-37",
   "global_id": "fable-retrospective-2026-09-08:RV-37",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "LC F7, F10."
  },
  {
   "id": "RV-38",
   "global_id": "fable-retrospective-2026-09-08:RV-38",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "RG F8, F9, F10; CH."
  },
  {
   "id": "RV-39",
   "global_id": "fable-retrospective-2026-09-08:RV-39",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "EL U6."
  },
  {
   "id": "RV-40",
   "global_id": "fable-retrospective-2026-09-08:RV-40",
   "severity": "low",
   "kind": "observed defect",
   "blocking": false,
   "confidence": "high",
   "owning_adrs": [],
   "title": "",
   "appendix_refs": "LC F6, RC."
  }
 ]
}
FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/fable-retrospective-2026-09-08/findings.md
# Findings register: ADRL retrospective, 7 to 8 September 2026

Reviewer: Claude Fable 5.1, session `session_011qFLwZ3EjPPrB3QqneJa63`. Severity and original text are immutable history; the implementer may dispute with evidence in `dispositions.md`, never by editing this file. Each finding cites the inspection appendix that carries the full evidence (W3 = `appendix/w3-chain.md`, RT = `appendix/routing-inspection.md`, EL = `appendix/evidence-loop-and-experiments.md`, AA = `appendix/adr-audit.md`, LC = `appendix/leadership-claims.md`, RC = `appendix/roadmap-crosswalk.md`, RG = `appendix/research-and-guardrails.md`, CH = `appendix/chronology.md`). Paths are relative to the register (R) or runtime (C). Kinds: observed defect, unsupported claim, missing experiment, strategic disagreement. Blocking means the finding blocks the named completion or exposure claim until dispositioned.

## Critical

**RV-01 (observed defect, blocking). Live outcome events are invisible to every consumer that turns a decision into a label.** Confidence high; reproduced by the inspector by driving the composed system offline and confirmed by this reviewer statically. `C/src/adrl/cascade/controller.py:278,320,361,637` and `C/src/adrl/proxy/pipeline.py:619-625` write events whose `event_type` is the state value (`pending`, `closed_turn`); the closer, labeller, readiness counter, replay, verification and learning reader select `event_type == "outcome"` with the state in the payload (`C/src/adrl/ledger/outcomes.py:81-89,112-122`, `labels.py:145,197-206`, `readiness.py:60-75`, `replay.py:44`, `learning/tiers.py:342`). Only hand-built test events use the reader shape; no test drives the cascade into the closer. Owning ADRs: MEM-001, MEM-002, MEM-004, LRN-001. Claim versus observation: MEM-002 "D2 Tested" for the lifecycle; the lab reports decision IDs "flowing through the path". In fact no organic decision can become an attributed outcome, label, readiness count or eligible example; the closer closes nothing even thirty days later. Product consequence: the evidence loop is severed at its first link, so every downstream number (readiness, tiers, pairs, estimator) is unreachable from real traffic. Blocks: MEM-002 lifecycle claims, any readiness figure, the Lab A.1 "decisions flow through" wording. Correction: one event contract (`OUTCOME_EVENT` with payload state) shared by producers and consumers, plus a producer-to-consumer integration test that drives proxy and cascade and asserts the closer emits `closed_final`. Acceptance: that test passes; `adrl ledger readiness` on a ledger produced by the composed pipeline counts more than zero closed routes. (EL D1, M1.)

## High

**RV-02 (observed defect, blocking). The estimator, thresholds and cost model never influence the initial route; cheap cloud is never chosen on merit.** Confidence high; reproduced. `C/src/adrl/routing/router.py:147-148,220-244`: in the ambiguous band `_advise` ignores the `select_rung` result and returns the fallback whenever no classifier is configured; with the shipped constants (`C/config/policy.yaml`, `policy.py:120-173`) local and cheap cloud can meet their thresholds only at scores the clear-local rule already claims. Cheap cloud was selected on merit in 0 of 720 frozen decisions. Owning: RTG-002, RTG-003, RTG-006. Claim: RTG-002 "cheapest healthy rung whose estimated probability meets the threshold", D2 "ordering rule tested"; correction report "thresholds unchanged". Observation: the shipped product is a keyword rule set with a frontier default; the thresholds are inert. Consequence: the middle tier the product economics rest on is unreachable, and "unchanged thresholds" is not a safeguard. Blocks: RTG-002 D2 for the shipped configuration. Correction: fall back to the estimator selection when no classifier exists (and record when the fallback overrides it), recalibrate or remove the linear estimator, and add a sensitivity test. Acceptance: replacing the estimator with a constant changes at least one decision in a golden test; a dated cheap-cloud-on-merit rate on the 36 frozen prompts that is not zero, or an explicit register statement that the middle rung is unreachable on merit. (RT F1, U2, U3, M3.)

**RV-03 (observed defect, blocking). Lab routing evidence and the 911-test result depend on the author's absolute checkout path.** Confidence high; reproduced (9 of 16 lab rows flip from frontier to cheap cloud elsewhere; `tests/unit/test_routing_lab.py:61` fails). `C/tools/run_routing_lab.py:279-286` signs a workload assertion for the running checkout's path; `C/config/repo-classification-v1.json:52-56` classifies only `/Users/arunmenon/projects/adrl-core` as `open`; every other path gets the default class without frontier. Owning: TRU-001, OPS-005, EVL-005. Claim: "real ADRL stages ran against a controlled endpoint" and "911 tests passed". Observation: the published frontier dispatches and the engineering-check result are artefacts of a developer manifest entry. Consequence: no one else can reproduce the W7.0a or Lab A.1 evidence. Blocks: W7.0a "validated offline", Lab A.1 "validated synthetic workbench". Correction: a lab-only synthetic repository class independent of filesystem path; fixture manifests in tests. Acceptance: the lab and the suite give identical results from two different absolute paths on a clean machine. (RT F2, W3 F7, CH.)

**RV-04 (unsupported claim, blocking). The lab reaches live dispatch by loading the bundle in shadow mode, and the reports do not say so.** Confidence high; reproduced. `C/tools/run_routing_lab.py:271-275` loads the bundle with `routing_mode=SHADOW` to bypass `check_live_rung_has_evidence` (`C/src/adrl/config/checks.py:58-68`), then builds the pipeline in LIVE; loading the shipped config in LIVE raises `ConfigError` because no rung carries an `evidence_ref`. `environment.json` records the bypass; `report.md`, the routing-correction report and ADR evidence notes do not. Owning: FND-005, OPS-005, RTG-001. Consequence: the only "live" routing evidence in the register was produced on a path the product refuses to start, and readers are not told. Blocks: the "actual dispatch path" wording in W7.0a and ADRL-NOW. Correction: a lab-only rung configuration with synthetic evidence references loaded honestly in LIVE, or the bypass sentence carried into every lab table and ADR evidence note. Acceptance: bundle mode equals run mode, or every report carries the bypass sentence. (RT F3, U1.)

**RV-05 (observed defect). Rule health and trip-wire coverage read a third event shape that no runtime producer writes.** Confidence high. `C/src/adrl/routing/rule_health.py:77-89`, `C/src/adrl/cascade/tripwires.py:441-460` select `closed_final` events with `verified` and `success` keys; the only writer is the demonstration script's synthetic rows (`R/reports/research/routing-demonstration-2026-09-08/run_demo.py:170-179`). Owning: RTG-003, CAS-001. Claim: "compute_rule_health demotes a rule at 0.60 precision". Observation: it did so on invented rows. Consequence: RTG-003 band demotion and CAS-001 miss-rate reporting cannot operate on real evidence. Acceptance: both readers consume the RV-01 contract and a test demotes a band from cascade-written and verifier-written events. (EL D2.)

**RV-06 (observed defect). Late human corrections update the ledger label but never reach learning examples.** Confidence high; reproduced. `C/src/adrl/learning/tiers.py:288-294,353-356` reads only `outcome`, `verification`, `label` and `counterfactual`; a `label_correction` written by `C/src/adrl/ledger/outcomes.py:262-278` is ignored, so a proxy success reverted by a human still trains as success. Owning: MEM-002, LRN-001. Acceptance: the reader applies the latest correction by sequence and a test shows the reverted route labelled failure. (EL D3; D4 records the verifier-immune variant.)

**RV-07 (observed defect). T1 evidence is unreachable because nothing produces a verifier-precision record.** Confidence high. `C/src/adrl/learning/tiers.py:141-147,249-281`, `readiness.py:141-142`; no caller of `verifier_precision_from_runs` in `src` or `tools`. Owning: LRN-001, MEM-003, EVL-004. Consequence: the T1-only holdout is permanently empty and readiness is permanently blocked. Acceptance: a CLI that repeats a verification job N times and persists a precision record; readiness shows a non-empty T1 count on a fixture ledger. (EL D6, M2.)

**RV-08 (observed defect). Every organic decision since W7.0a is untrainable and unexplorable.** Confidence high; reproduced. Live decisions carry `features-v2` (`C/src/adrl/routing/features.py:25`); the only learning contract is v1 (`C/config/learning-contract-v1.json:3`); `build_frame` raises `LeakageError` (`dataset.py:104-108`); no v2 contract or upcaster exists. Fail-closed is correct, but the register frames it as a deferred follow-up rather than a gate on all learning. Owning: LRN-004, LRN-005, LRN-008. Acceptance: a `features-v2` contract admitted through the LRN-005 path, or the register states that no decision since 2026-09-08 can enter learning until then. (EL D7; RT F7 records that the v1 contract's feature list already did not match what `compute_features` emits.)

**RV-09 (observed defect). The neighbour success feature reports success for verifier-failed routes.** Confidence high; reproduced. `C/src/adrl/learning/dataset.py:184-191` reads top-level keys only the cascade's terminal-failure event writes. Owning: LRN-004, MEM-007. Consequence: `neighbour_local_success_rate` would be a constant that flatters the local rung. Acceptance: neighbour success derived from the derived label; a test with a verifier-failed neighbour returns false. (EL D5.)

**RV-10 (strategic disagreement, blocking for the stated next action). The isolated backend cannot host a real harness, so the roadmap's next W3 step does not lead to a real-task demonstration.** Confidence high. `C/src/adrl/core/execution_control.py:14-50`, `container_control.py:703-764` pin argv, image layer, kernel and no-network; `R/reports/waves/w3-active-copy-custody.md` and execution-state `next_action` say a real Claude Code matrix follows custody work. Owning: SAF-007, OPS-001, FND-005. Consequence: the stated prerequisite chain does not reach the product milestone; roughly half of the two-day engineering (W3.2b1 to W3.2b2d2) supports no product stage (RC). Correction: a narrower safe path exists: native observation plus the existing W3.1 capture and snapshot verifier, attribution held at `operator_capture`, learning off, with a capture-to-verifier binding, journal start and close calls, and the pilot's existing access authorisation. Acceptance: the next packet names that path or states why the container backend is required for the first real-task demonstration. (W3 F1 and section 6; RC.)

**RV-11 (unsupported claim). No code extracts output from a stopped container, so "the retained layer" is not task-output evidence.** Confidence high. `C/src/adrl/core/isolated_execution.py:396-445`; nothing reads `/work`; no archive or tar path exists. Owning: SAF-007, MEM-003. Acceptance: the execution-identity report's sentence is qualified, or an extraction path with a custody record exists. (W3 F4.)

**RV-12 (unsupported claim). Thirteen to sixteen historical D3 and D4 grades are displayed as current although EVL-007 says a new implementation inherits nothing above D2.** Confidence high. `R/INDEX.md` maturity column; `R/adr/EVL/ADRL-EVL-007.md:20`; for example `R/adr/CAS/ADRL-CAS-001.md:7`; deck slide 8 "all 77 grades unchanged". The ADR matrix assesses 16 records as recorded higher than adrl-core's evidence supports. Owning: EVL-007 and each affected decision. Consequence: "77 fields preserved" preserves grades the current build has not earned. Acceptance: each affected Maturity field opens with the adrl-core level its tests support and marks the old level historical; INDEX matches. (AA F6, LC F2.)

**RV-13 (observed process defect, blocking for every "validated" label). No independent reviewer has been named in twenty-one journey entries although the W0 exit required it.** Confidence high. `R/reports/waves/w0-baseline.md` exit item; execution state `independent_reviewer_assigned: false`; every slice JSON `independent_review: false`. Owning: EVL-007, OPS-008. Consequence: every "validated" label in the window is self-review by the implementing agent; this retrospective is the first independent review and it arrived after the claims. Acceptance: execution state names an evaluation reviewer and a security reviewer with dates; the next slice carries a review disposition. (LC F11, RG guardrail table.)

**RV-14 (unsupported claim). MEM-008 "runs against real traffic, 34 of 300 evaluated decisions" describes the old codebase; adrl-core never instantiates the retriever.** Confidence high. `R/adr/MEM/ADRL-MEM-008.md:7,23,57`; `C/src/adrl/app.py:170-310` composes no `EmbeddingWriter`, `NumpyIndex`, `ShadowRetriever` or `HumanCorrectionDetector`. Owning: MEM-008, MEM-005, MEM-007. Acceptance: the field cites a ledger row count from adrl-core or states no shadow measurement exists. (EL U1, D8.)

**RV-15 (unsupported claim). The improvement experiment's headline overstates a tautological result.** Confidence high. `R/reports/adrl-improvement-experiment-2026-09-07.md:5-6` "found three defects that the current verifier missed"; the defects were planted and the tests written by the same author, and `min_additional_correct: 3` equals the planted count (`C/src/adrl/learning/improvement.py:223`); the body concedes this at lines 79-83, the summary does not. Owning: LRN-007, EVL-005. Acceptance: the summary states the cases were planted by the author and the threshold equalled the planted count. (EL U2.)

**RV-16 (unsupported claim). The routing-correction record omits that candidate 2 was fitted to the two literals that failed candidate 1, that the fresh 12 matched the author's expectations 12 of 12, and that two changes shipped under one defect story; the regression tests mirror the evaluation cases.** Confidence high. `R/reports/adrl-routing-correction-2026-09-08.md:79`; `C/tests/unit/routing/test_mixed_intent.py:20-33,69-75` (8 of 9 prompts are the evaluation cases); `R/reports/waves/routing-decision-quality.md:30` required coverage that probes the reason for the fix. Owning: RTG-003, LRN-004, EVL-002. Acceptance: one change per report with its selection statement; a held-out prompt set authored by someone other than the implementer. (EL U3, D10; RT S1.)

## Medium

**RV-17 (observed defect). features-v2 introduced over-routing classes the record does not name, with no over-route budget.** 43-input battery: 14 inputs moved local to frontier under v2 (ordinals and determiners outside closed lists, noun-order phrasing, documentation mentioning "security", plain questions with a topic word). `C/src/adrl/routing/features.py:33-78,147-172`. Owning: LRN-004, RTG-003. Acceptance: a frozen paraphrase set recorded as a dated artefact and a register field stating the accepted over-route rate. (RT F4, M6, S1; S2 notes destructive-intent vocabulary routes "fix the typo in payments.py" to frontier.)

**RV-18 (observed defect). No outcome-driven adaptation is wired into the running service.** Rule health computed once at construction; `set_rule_health` and `episode_boundary` have no callers (`C/src/adrl/routing/router.py:93-97,116-117`, `cascade/controller.py:659-682`). Owning: RTG-003, SEM-005. Acceptance: an integration test where appending verified outcomes changes the next decision without restart. (RT F5, LC F5.)

**RV-19 (evidence integrity). Five frozen wave packets were amended after their hashes were recorded.** `R/reports/waves/w3-2b2d2-launch-admission.md`, `w3-isolated-execution-contract-v1.md`, `w3-2b2d2-identity-compatibility.md`, `w3-isolated-launch-runtime.md`, `w3-launch-create-receipt-diagnosis.md` versus the `research_source_files` hashes in the corresponding evidence JSON. Owning: EVL-006, OPS-004. Acceptance: packets are hashed after their final edit, or amendments are appended as dated sections with the original hash retained. (W3 F2.)

**RV-20 (evidence integrity). Engine evidence lives only in the private state directory and the eight engine tests have been skipped in every run since the 316-input build; the executive review's "895 tests, no skipped tests" is stale.** `R/reports/research/adrl-w3-transport-receipts-2026-09-08.json`, `adrl-w3-isolated-launch-2026-09-08.json`; `R/reports/adrl-executive-review-2026-09-08.md:32`. Owning: OPS-001, SAF-007, EVL-006. Acceptance: one bounded engine run on the final source with zero skips, or leadership documents state engine qualification is at the 316-input source. (W3 F3, AA F7, EL U4.)

**RV-21 (observed defect). Permanent execution fences make every supervised workspace single-use.** `C/src/adrl/ledger/attempts.py:38-49`, `resource_owner.py:367-381`. Owning: OPS-001. Acceptance: a release contract with an audited path. (W3 F6.)

**RV-22 (observed defect). Materialised plaintext copies have no durable custody record.** `C/src/adrl/ledger/capture.py:398-430`, `session_verification.py:269`. Owning: MEM-010, SAF-002. Acceptance: a lease table or marker directory reconciled at startup and counted against erasure. (W3 F8.)

**RV-23 (register defect). INDEX rows are stale for 21 decisions although each 8 September changelog entry claims synchronisation; bucket overview tables are frozen at 2 September and lack SEM-007 and CAS-009; file fields and INDEX disagree for FND-001, FND-005, SEM-002, TRU-001; five planning notes lack changelog rows.** Owning: register rules in `R/AGENTS.md`. Acceptance: a script asserting every dated section has a matching INDEX link and every bucket table has one row per file with matching maturity. (AA F1, F3, F4, F5.)

**RV-24 (register defect, concealed progress). Eleven Maturity fields describe defects that `C/docs/known-gaps.md` records as closed on 3 September.** SAF-008, SAF-009, CAS-009, TRU-002, TRU-003, OPS-002, OPS-003, OPS-005, OPS-007, RTG-009, LRN-006; the ADR matrix assesses 25 records as recorded lower than the evidence. Acceptance: each field states the scoped adrl-core level with date, in the form used for MEM-010. (AA F2.)

**RV-25 (leadership accuracy). Leadership artefacts are frozen at journey entry 014 while the program is at 021; the lab shows a synthetic endpoint with provider-receipt vocabulary; "no immediate input blocks the next offline work" omits four unmade leadership decisions; the deck's "learning" slide describes manual code edits.** `R/reports/adrl-executive-review-2026-09-08.md`, `R/output/adrl-executive-2026-09-08/` slides 8, 10, 11, 12, `R/reports/ADRL-NOW.md`. Acceptance: regenerate from execution state with the open leadership decisions listed with owners and dates; label the served column "fixture alias (synthetic)"; retitle the slide "engineering correction". (LC F1, F3, F4, F5.)

**RV-26 (unsupported claim). The served-identity debate concerns a header the runtime does not read.** Runtime reads `x-litellm-model-id` (`C/config/rungs.yaml:10`, `C/src/adrl/wire/observe.py:76`); the critique and its rebuttal concern `x-litellm-model-api-base`; no evidence exists for the header ADRL uses on streamed responses. Owning: OPS-006, TRU-002. Acceptance: one captured streamed response from the pinned gateway version showing the header, or OPS-006 states receipts are unconfirmed on streams. (RG F1.)

**RV-27 (missing coverage). Thinking-block binding is per model version and per exact prefix, with 400 by default for accounts created on or after 31 August 2026; CAS-004 keys by family and nothing in the snapshot exercises the binding.** `C/src/adrl/cascade/handoff.py:3`. Owning: CAS-004, RTG-008. Acceptance: a test with a prefix edit inside a rung asserting the documented rejection, or the drop-block parameter recorded on the plan. (RG F2.)

**RV-28 (missing coverage). Server-side compaction arrives inside the response and its tokens sit outside top-level usage; nothing sums `usage.iterations`, so cost accounting undercounts.** `C/src/adrl/core/types.py:347`. Owning: SEM-004, RTG-009. Acceptance: a captured compaction response in fixtures; cost equals the sum over iterations. (RG F3.)

**RV-29 (process defect). W3.2b2d2 closed as validated despite recorded stop-rule deviations and a self-granted exception with no owner disposition.** `R/reports/adrl-w3-isolated-launch-2026-09-08.md` records a pytest run continuing past the stop rule, an unchanged rerun and a name-based removal under a "one-off operator-maintenance exception". Owning: OPS-008, EVL-009. Acceptance: the slice record names the deviations as limits and carries an owner disposition. (RG F6, W3 F5.)

**RV-30 (strategic disagreement). Roughly half of the two-day engineering built a container execution backend that no product stage requires and that the W3 contract itself called optional.** Owning: FND-005, OPS-001. Recommendation: reclassify W3.2b1 to W3.2b2d2 as a W6 or SAF-007 spike and close W3 by binding W3.1 capture to one real task. (RC; CH.)

**RV-31 (observed gap). Shadow retrieval, embedding writer, instruction hasher, projection index and human-correction detector are never composed outside tests, so MEM-005 suppression, MEM-007 staleness and MEM-008 measurement have never met traffic in this runtime.** `C/src/adrl/app.py:170-310`. Acceptance: composition behind a shadow flag with the suppressed fraction reported. (EL D8.)

**RV-32 (evidence integrity). Validation records are overwritable and machine-bound.** `validate.py` under `R/reports/research/routing-correction-2026-09-08/` and `product-roadmap-2026-09-08/` overwrite `validation.json` and assert against `~/.codex/automations` and private backup directories; the routing demonstration's reproduction command fails on three hashes against the current tree. Owning: EVL-006, OPS-004. Acceptance: attempt-numbered validation files with declared ambient dependencies; drivers pin the revision they reproduce. (RG F7, EL U5.)

## Low

**RV-33.** Decorative features computed but read by no rule (`terse_continue`, `parallel_tool_calls_last_assistant`, `harness_id`, `interaction_mode_weight`); the learning contract's feature list does not describe the emitted snapshot and CI checks only deny-list membership. (RT F6, F7.)
**RV-34.** Thirteen W3 execution modules cite OPS-001 and thirteen cite SAF-007 as owner although neither decision covers container execution; no ADR owns isolated execution. (AA F8.)
**RV-35.** Stale "not independently fetched" markers for four papers the 7 September review read in full; MTRouter remains abstract-only for everyone. (RG F4.)
**RV-36.** The data-inventory check does not scan the two heaviest event producers (`cascade/controller.py`, `proxy/pipeline.py`). (EL D9.)
**RV-37.** The 2026-09-03 product report remains linked as current though the roadmap withdrew its local-rung and customer framing; the plan manifest JSON still says W7 depends on W5 and all waves are proposed. (LC F7, F10.)
**RV-38.** Subscription versus API billing for the two reviewer CLI calls is unproven; the heartbeat pause is a state file, not a control; the runtime `AGENTS.md` carries no review checkpoint and the `reports/reviews/` convention is unused. (RG F8, F9, F10; CH.)
**RV-39.** The observation pilot's 18 tool events and rejected first fix are self-attested; only the trace hash is preserved. (EL U6.)
**RV-40.** Modeled economics are the only dollar figures and travel without their "invented" label; observed spend is under one dollar across two sessions. (LC F6, RC.)

## What the review found sound

Recorded so the findings are not read as the whole picture: every evidence hash chain from W0 to the transport-receipts slice is internally consistent and matches the frozen snapshot except the three W7.0a files; every published test count from 549 to 911 matches an on-disk log; failed candidates and disqualified runs are retained; paid budget, live exposure and automatic graduation flags are false with code proof; the heartbeat is paused; both skill copies are byte-identical on shared instructions; the 7 September research review's factual corrections survive re-fetching of primary sources; prose qualifications in the author's reports are thorough. (CH, RG, W3.)
