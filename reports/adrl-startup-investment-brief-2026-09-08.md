# ADRL: what we should build, and why fund the next step

8 September 2026 · Leadership brief · Proposed roadmap, not a release commitment

**Recommendation: fund a bounded product validation phase.** ADRL has enough implementation to test a meaningful business. It does not yet have evidence that adaptive routing improves real coding-task economics, or that customers will pay for it.

The proposed product helps an engineering team choose appropriate permitted models as coding work unfolds, establish whether those choices improve completed tasks, and improve the policy from trustworthy outcomes. Developers keep their existing coding tools.

The first customer hypothesis is a platform team with model API spending and repositories with meaningful tests. The buyer is likely a VP Engineering or CTO; the platform lead is the champion. This is an assumption for discovery, not a validated customer segment.

## The problem we would solve

A cheap model call can lead to an expensive task if the developer must retry, repair and review it repeatedly. An expensive model can also be wasteful on simple work. ADRL must show when each choice is worthwhile and change course when reliable task signals justify it.

The value proposition is **better completed work for the total money and effort spent, within the customer's rules**. A lower token bill alone is insufficient.

The decision must use the request **and its context**: scope, relevant code, available tools, earlier progress, verification and remaining budget. A task classifier describes the work; LRN is designed to learn whether another model would improve the result in that context. The roadmap tests the value of these signals explicitly, rather than treating task labels as enough.

MEM already specifies memory of decisions, verified outcomes, corrections and retrieval to support adaptation. The implementation includes a retrieval index and shadow advice. We should qualify and use that foundation, then test whether a context graph improves its ability to connect circumstances, outcomes and reviewed changes. The [proposal](../design/adrl-context-graph-memory-proposal-2026-09-08.md) starts with all ten existing MEM decisions; a graph is not itself evidence of learning.

The proposed operating model places ADRL and local experience memory on the developer laptop. A separate offline process learns from authorized, qualified evidence and sends back approved, versioned routing-policy packages. This lets local context benefit from shared lessons without making a central training service part of every routing request.

Current competitors make the bar demanding. Not Diamond Code documents session-aware coding routing; LiteLLM and native harnesses also offer routing. Our proposed advantage combines customer control, verified task outcomes and reusable integration. That advantage must be demonstrated against alternatives. [Not Diamond](https://code.notdiamond.ai/docs/), [LiteLLM](https://docs.litellm.ai/docs/proxy/auto_routing), [Copilot Auto](https://docs.github.com/en/copilot/concepts/models/auto-model-selection).

## What exists today

- A substantial implementation baseline: 895 passing tests and eleven checks.
- A real Claude Code observation pilot, which captured tool activity but made no ADRL model-routing choices.
- A reproducible routing diagnostic: 240 synthetic decisions exposed two mixed-intent failures.
- A detailed decision taxonomy and evidence controls.

There are **no measured live routing savings, no demonstrated policy-learning benefit and no demonstrated RSI result**. The evidence is linked in the [full product roadmap](adrl-product-roadmap-2026-09-08.md#2-where-we-actually-stand).

## The investment sequence

| Next proof | What leaders should see | What it earns |
|---|---|---|
| A buyer has a costly, reachable problem | Actual workflow/spend evidence and named trial owners | A small product experiment |
| ADRL visibly makes dependable decisions | Selected model, actual dispatch, reason, restrictions and recovery | Real task comparisons |
| Routing improves a declared workload | Quality, full cost, repair effort and uncertainty against alternatives | A restricted, approved pilot |
| Adaptation helps during real work | Evidence that continuing or switching changes the outcome | More integration investment |
| The product works across qualified harnesses | Repeatable setup and a genuinely reusable interface | Supported product release |
| Better policies can be learned reliably | Fresh evidence and independently approved improvements | Proposal automation |
| The improvement process can itself improve | More durable routing benefit for the same total improvement budget | Further RSI investment |

Start with Claude Code and an appropriate Claude-model profile. Qualify OpenCode next, including local/provider options. Keep the API in preview until the existing requirement for two real harnesses and two protocols is met. Wider integration does not inherit the first harness's qualification.

## The proposed first 90 days

**Days 1–30:** validate the customer problem, resolve blocking architectural questions, correct the demonstrated routing weaknesses and show real controlled test dispatch. Qualify the minimum trustworthy measurement path.

**Days 31–60:** compare completed tasks using approved billing/access, independent verification and fresh confirmation cases. Report insufficient evidence when results are uncertain.

**Days 61–90:** run a restricted customer pilot only after applicable qualification. Test whether adaptation adds value and whether a customer will pay to continue. A second-harness contract exercise can proceed if it does not delay the value test.

These are planning windows from an authorized restart, assuming a staffed team and partner access. Safety, evidence or access blockers move the dates.

## Where RSI belongs

First, ADRL can change its model choice during a task. Next, it can learn a better routing policy across tasks. Later, RSI can improve how it finds and tests those policy changes.

For example, a better failure-analysis method might select experiments that yield more useful routing improvements. We compare that method with its predecessor under the same budget, with independent judging. More patches or more proposals are not success.

The improver cannot expand its own data access, weaken the protected evaluation standard, increase its budget or approve its release. A result may challenge an ADR; the decision ledger records the reviewed amendment.

## Economics and stop conditions

Price should be supported by demonstrated customer value. Test a paid evaluation and a subsequent platform subscription, with provider charges kept separate. No pricing or customer willingness to pay has been validated.

The full roadmap includes a sensitivity model: under one illustrative set of inputs, a 20% reduction on half of a $40,000 monthly model budget produces $4,000 gross savings but only $1,500 net after assumed incremental costs and product fee. Coverage and operating cost can make an impressive percentage commercially weak. These are invented planning inputs, not ADRL results.

An illustrative 90-day funding envelope is $270,000 for four technical roles, evaluation, independent review, operating allowances and contingency; product-founder salary is excluded. It must be repriced for the actual team and geography. No spending is authorized by this document.

Stop or narrow the investment if alternatives already solve the problem, completed-task economics do not improve, developers reject the workflow, or customer-specific engineering prevents repeatability. Keep a simpler selector when it wins. RSI can fail without invalidating a useful routing product.

**Decision proposed now:** approve the product direction and a bounded discovery/decision-quality phase. Fund later phases against evidence. Implementation and its scheduled continuation remain paused; the roadmap changes no ADR decisions or maturity grades.

The [full roadmap](adrl-product-roadmap-2026-09-08.md) contains milestone contracts, guardrails, owners, measurement rules, the ADR disposition queue, resources, commercial hypotheses and the 12–18-month horizon.
