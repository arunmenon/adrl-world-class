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
