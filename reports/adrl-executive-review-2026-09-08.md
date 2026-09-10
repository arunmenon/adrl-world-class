# ADRL: executive progress review

**Routing clarification, 8 September 2026:** this briefing emphasizes execution/evidence progress and does not establish routing effectiveness. The current [routing report](adrl-routing-in-action-2026-09-08.md) adds actual decision probes, their failed cases and the revised immediate priority. The earlier presentation remains a dated progress snapshot.

**8 September 2026. Current stage: a working local prototype, with Wave 3 still in progress.**

[Two-page PDF brief](../output/adrl-executive-2026-09-08/ADRL-Executive-Brief.pdf) · [Editable executive presentation](../output/adrl-executive-2026-09-08/ADRL-Executive-Progress-v2.pptx)

ADRL has progressed from an architecture and early implementation into a working product foundation. We have observed a real Claude Code task, retained evidence about its actions, built separate ways to check the work, and tested how a controlled job recovers when something goes wrong. The next milestone is connecting those pieces into one trustworthy record of exactly what a task produced.

## What ADRL is for

Think of ADRL as a shared supervisor around AI coding tools. The coding tool works on files. The model suggests the next action. ADRL's intended role is to apply rules, keep an accountable record and help determine whether the result is useful.

The product direction is one shared core across supported tools, beginning with Claude Code, then OpenCode, and later Codex. The business value we want to establish is better control and confidence in AI work. Quality gains and savings still need measurement.

## What we have achieved

| Achievement | What it means in ordinary language |
|---|---|
| A shared product foundation | Working local connection, task/session identity, event intake and activity-history services give future integrations a common base. |
| One real observation pilot | ADRL recorded all 18 executed tool actions in the checked Claude Code session trace, including a failed action. This proves a limited integration works. |
| Separate checks on the result | The first plausible repair passed the old tests but failed compatibility checks. A corrected repair passed all eight checks. The agent's success message did not decide acceptance. |
| A way to compare improved checks | A proposed checker identified three defects the earlier checker missed. It classified seven of seven prepared examples correctly, versus four of seven for the earlier checker. These were visible variants of one task, not a general accuracy study. |
| Protected evidence and task records | Encrypted captures preserve selected work even after later edits. Task records distinguish started, interrupted and incomplete work. Exactly tying a final capture to task completion remains unfinished. |
| Tested controlled execution and recovery | Fixed test jobs now pass normal stop, lost confirmation, access-revocation and owner-process-death cases on the selected local engine. Recovery keeps the original job identity and avoids a second launch. |

Sources: [product services](adrl-product-services-implementation-2026-09-07.md), [Claude pilot](adrl-live-observation-pilot-2026-09-07.md), [checker comparison](adrl-improvement-experiment-2026-09-07.md), [latest execution result](adrl-w3-transport-receipts-2026-09-08.md).

## The strongest current evidence

The latest full validation passed **895 tests and all 11 engineering checks**, with no skipped tests. The fresh controlled-job experiment accounted for **13 original creation receipts and 13 confirmed removals**. Its test image was removed too. These runs used synthetic jobs, without real task payloads or model calls.

These figures show that named behaviors and failure cases pass on the tested build. They are not a percentage of product completion, a population reliability estimate or proof of commercial value.

## How testing is changing the design

Testing has changed our implementation, not just produced green results. A helper that could keep writing after its parent stopped led to a separately controlled execution boundary. A stale-key recovery weakness led to lasting denial of future access through the current APIs. Shared preparation and supervision timeouts led to separate budgets and better receipt diagnostics.

The previous real creation failure still has an unknown underlying cause. We reproduced a plausible timeout mechanism and the corrected workflow now passes. We have preserved that distinction in the decision record.

## What maturity means now

The core has stronger implementation and test evidence. Claude Code has one limited real observation result. The controlled execution path has passed its fixed local test scenarios. **The overall product remains a prototype.** We have not established a reliable complete customer workflow, broad integration support, production readiness, lower cost or better coding quality.

We keep the architecture decision ledger aligned with implementation changes. The latest slice updated eight owning decisions and preserved all 77 formal status and maturity fields. We have not invented an overall score or promoted grades because a test count rose. Independent evaluation and security reviewers remain future qualification gates.

## What happens next

1. **Finish trustworthy task evidence.** Account for temporary decrypted copies, handle interrupted cleanup, and preserve the exact output at task completion. This is the current Wave 3 work.
2. **Check useful work across tools.** Test verification on fresh, independently reviewed tasks and reuse the shared foundation through OpenCode. This is the route toward a developer preview.
3. **Prove control and value.** Exercise real enforcement, compare permissible routing choices, add the later protocol integration and qualify setup, upgrades and recovery before a supported release.
4. **Expand adaptive improvement carefully.** Use approved outcomes to propose and test changes. Later automation may improve how proposals are generated, but it cannot approve its own wider authority.

The current adaptive loop is concrete: keep failure evidence, propose a bounded change, test it and update the decision ledger. Recursive self-improvement would also improve the method that finds future improvements. That later capability remains unproven.

No immediate user input blocks the next offline work. Before broader pilots, we will need independently reviewed task examples, reviewer assignments and concrete choices about access, data retention and spending. The next executive demonstration should show a task finishing, its exact output preserved, and separate checks judging that same output.

For detail: [running journey](adrl-implementation-journey.md), [forward roadmap](adrl-implementation-roadmap-2026-09-07.md), [current execution state](research/adrl-execution-state.json). The presentation contains source references and additional explanation in its speaker notes.
