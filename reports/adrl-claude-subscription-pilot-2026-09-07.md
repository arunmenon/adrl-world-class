# Starting ADRL with your Claude Code subscription

**Later implementation, 2026-09-07:** [independent session verification](adrl-session-verification-2026-09-07.md)
is now applied in API preview 4, with 532 passing tests. Two verifier jobs each passed eight
checks on the existing repaired task and added receipts to a copied timeline. Earlier figures
and outstanding-work lists below describe the original report date/stage; the linked update
contains the current scope and next steps.

**Current result, 2026-09-07:** [the first live observation pilot](adrl-live-observation-pilot-2026-09-07.md)
is complete. Native Max authentication was confirmed with normal macOS access; no new login was
needed. Observation mode is applied in API preview 3, with 511 passing tests and 18 reconciled
real tool events. The repair passed eight independent checks. The preparation/planning text
below preserves its earlier scope and must not be read as current launch or authentication status.

7 September 2026 | Prepared pilot, not a completed model run

Your subscription gives us a practical starting point: run Claude Code normally, establish a checked coding result, then add ADRL observations. Testing ADRL's routing requires a later run with ADRL on the model request path. These are separate milestones.

Claude Code **2.1.260** is installed. Its authentication check in this execution environment returned `loggedIn: false`, `authMethod: none`. This does not establish your subscription tier or whether another terminal can access a saved login. No credentials were extracted and no model request was made.

## Which repository?

| Repository | Role |
|---|---|
| [adrl-world-class](/Users/arunmenon/projects/adrl-world-class) | The taxonomy, decision ledger, research and experiment records |
| [adrl-core](/Users/arunmenon/projects/adrl-core) | The ADRL service being tested; hold its tested build fixed during the pilot |
| [dataset-validator](/Users/arunmenon/projects/dataset-validator) | A separate codebase Claude works on, so we can measure useful task completion |

I recommend a small subset of dataset-validator. Its template and configuration tests run without a model service, database or FAISS. This does not certify the whole repository. SDK MCP server's inspected test script depends on its SDK corpus and prints success without equivalent assertions, making it a weaker first fixture.

Nine selected source, configuration and test files are copied into an isolated [pilot working copy](/private/tmp/adrl-claude-pilot-9x3n90aj/run-01-sonnet). No datasets or credential files were copied. The original repository is unchanged. This is a selected-file snapshot, not a Git worktree or full clone. The [manifest](research/adrl-claude-subscription-pilot-2026-09-07.json) records source hashes. The temporary folder can be cleaned by the operating system; this report and manifest preserve the preparation record.

## A real first task

Four existing tests were run in both the original checkout and isolated copy. **Two configuration tests pass; both template tests raise `KeyError`.** Literal JSON braces in the templates are interpreted as substitution fields by Python's formatter.

P01: restore rendering for both templates while preserving literal JSON examples, variable substitution and missing-variable errors. Preserve the existing tests and keep the configuration tests passing. The [task brief](/private/tmp/adrl-claude-pilot-9x3n90aj/run-01-sonnet/TASK.md) and runner are ready. The failure is intentionally unfixed so Claude's result can be measured.

Acceptance requires four passing tests, a reviewed diff, and confirmation that JSON examples and inserted values survive. The reviewer must also check missing-variable errors. Claude's claim of success is not the verifier. This is a small integration task, not a general coding-quality benchmark.

## What the subscription supports

Normal Claude Code use can draw on a Pro or Max subscription. An API key can select separately billed API usage instead. Anthropic's current support notice says its proposed Agent SDK billing change was paused on June 15: `claude -p` and SDK usage still draw from subscription limits. The older monthly-credit text below that notice is historical. [Subscription access](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan), [current SDK notice](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan).

The current ADRL → LiteLLM → Anthropic API path needs provider/gateway credentials and an API budget. A Claude subscription does not supply API or Console access. Keep Claude's native authentication in Claude Code; ADRL's workload assertion is a separate local-service credential. [API billing distinction](https://support.claude.com/en/articles/9876003-i-have-a-paid-claude-subscription-pro-max-team-or-enterprise-plans-why-do-i-have-to-pay-separately-to-use-the-claude-api-and-console), [gateway connection](https://code.claude.com/docs/en/llm-gateway-connect).

| Stage | Model request path | What it establishes |
|---|---|---|
| A. Native baseline | Claude Code → Anthropic, subscription | A real task and independently checked outcome |
| B. Observation pilot, setup pending | Same native path; selected hooks report separately to ADRL | Event delivery, correlation and evidence reads for those events |
| C. Gateway pilot, access and budget pending | Claude Code → ADRL → gateway → provider | Exercised interception and control behavior, once prerequisites pass |

Stage B cannot establish enforced secret gating, local-only pins, complete model egress accounting or savings. The current `adrl connect claude-code` helper configures a gateway base URL. A separate observation-only launch mode remains to be implemented and tested. Do not source the existing connection's `env.sh` for this native subscription baseline. Hook records must not be represented as intercepted model requests or trusted verification.

## Models checked today

These are current catalog prices in API dollars per million input/output tokens, not charges against included subscription usage. Account availability remains to be checked. [Anthropic model catalog](https://platform.claude.com/docs/en/models/overview).

| Model | Exact API identifier | Input / output | Recommended experiment role |
|---|---|---|---|
| Sonnet 5 | `claude-sonnet-5` | $2 / $10 | First small task and everyday coding candidate |
| Opus 5 | `claude-opus-5` | $5 / $25 | Stronger comparison baseline on fresh task copies |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | $1 / $5 | Later simple-task candidate |
| Fable 5.1 | `claude-fable-5-1` | $10 / $50 | Later difficult, extended tasks |

These roles are recommendations, not measured ADRL findings. Anthropic recommends Opus 5 for most workloads and Fable 5.1 when harder evaluations warrant it. Starting P01 on Sonnet is a small integration check, not evidence of an optimal default.

Use full IDs and record any fallback or unavailable model. The installed CLI clears the documented minimum versions for Opus 5 and Sonnet 5. Aliases change and provider mappings differ. Model selection alone is not a served-model receipt. [Model configuration](https://code.claude.com/docs/en/model-config).

## Concrete next steps

1. Confirm native login in the terminal that will run the pilot. Use `claude auth login` if necessary, choose your subscription account, and inspect `/status` and `/model`. Account sign-in requires you; do not paste credentials into ADRL.
2. Confirm included usage is selected and separately purchased usage credits will not be consumed. No extra credits, API spend or top-up is authorized for this pilot. [Usage-credit billing](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans).
3. Run P01 on Sonnet 5 if available, with the native connection and no ADRL gateway override. Independently verify the result; record elapsed time, repairs, model changes and the diff.
4. Add and test the observation-only launcher, then compare native and instrumented runs from identical starting states. This measures integration behavior.
5. Compare Sonnet and Opus on a small task set using fresh copies and matched effort settings. These first observations establish feasibility. Representative repeated tasks are needed for quality or economics claims. API-equivalent token cost is not a subscription invoice.
6. Resolve the known gateway readiness gaps, provider access and budget before stage C. Continue OpenCode and Responses work under the existing release gate.

The first working directory is ready:

```bash
cd /private/tmp/adrl-claude-pilot-9x3n90aj/run-01-sonnet
claude --model claude-sonnet-5
```

After confirming account and model, ask: “Complete P01 in TASK.md and run the documented tests.” No Claude session has been started by this preparation.

This application is recorded in [FND-005](../adr/FND/ADRL-FND-005.md) and [SEM-007](../adr/SEM/ADRL-SEM-007.md). No runtime code, model inventory, policy threshold or maturity level changed.
