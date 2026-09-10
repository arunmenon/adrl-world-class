# Claude Code compatibility spike: pre-wave packet

Date: 2026-09-09. Stage P1, direct prerequisite to Claude Code ROI diagnostic. User authorized preparation and Fable critique of the concrete spike packet. No inference task launched, live profile changed, paid API use or expanded task matrix authorized by this preparation. This is not a whole-product review.

## Product question

Can one isolated native Claude Code session, using the existing claude.ai Max login through ADRL, receive a cheaper Claude model chosen by ADRL and continue with tool/thinking history? Produce either actual request/decision/served-model evidence or a precise failing boundary. Forced selection is integration proof only; it is not routing merit, savings, learned admission or production qualification.

## Verified preflight and exact blockers

Claude Code 2.1.265 is installed. Read-only auth status returned loggedIn true, authMethod claude.ai, apiProvider firstParty, subscriptionType max. No ANTHROPIC_API_KEY/AUTH_TOKEN/BASE_URL or alternate-provider environment overrides are present in the coordinator. This does not attest that paid overflow is disabled or that the target deployment is currently available to this account.

Read-only synthetic probes against existing functions, in static-probes.json:
- Authorization and anthropic-beta pass through forward_headers; local workload assertion is removed upstream. Actual subscription traffic is not yet exercised.
- strip_for_rung rewrites Opus to Sonnet but drops thinking, output_config, a server-tool declaration and system cache marker. Therefore current cheaper-rung code is not qualified as a model-only Claude rewrite.
- Loading the actual config with LIVE settings fails: live_rung_has_evidence, local enabled without evidence_ref. No server or ledger created by these probes. All configured Claude model names are listed as frontier; cheap_cloud currently maps an adrl-cheap-cloud gateway group, not a qualified direct Claude destination. No use of SHADOW-loaded bundle with LIVE settings is allowed.

These are concrete implementation/configuration blockers found before spend, not evidence that Anthropic rejects subscription rerouting. Preparation must not imply the live spike is launch-ready.

## Intended smallest profile, for disposition

Source model candidate: claude-opus-5. Cheaper candidate: claude-sonnet-5. Exact IDs are already present in source config and current vendor documentation; account execution availability remains a measured precondition. No alias fallback to another model. Do not begin with Haiku because its thinking/tool behavior would add a second compatibility variable.

Native Claude Code -> isolated loopback ADRL -> https://api.anthropic.com using the original native authorization and anthropic-beta. No LiteLLM deployment is required for this direct compatibility path, but endpoint inventory/identity must explicitly support and label direct Anthropic; do not fabricate a LiteLLM receipt/header or send the adrl-cheap-cloud group name directly to Anthropic. A fixed HTTPS upstream, no redirects, no alternate destination, and no credentials serialized into records are required. The existing HttpxGatewayClient provides a candidate forwarding transport; actual composed support is unqualified.

Use a new generated workspace with one tiny synthetic text file containing two integers; allow only a native Read tool scoped to that workspace. No customer repository, shell, network tool, write tool, plugin, MCP server or arbitrary hook. If a narrowly scoped Read permission cannot be enforced by the launcher, stop. Save the input tree/hash before execution. A hash of private content is not a reason to retain it; inputs here are synthetic.

Normal first response uses Opus and must contain genuine thinking and a tool call. Return its tool result, then exercise one explicit forced Opus-to-Sonnet switch with that original history. Also exercise a Sonnet continuation. Do not edit the thinking blocks, system or tool definitions to force acceptance. If initial selection is proven but switching fails, report the narrower result and assess an initial-choice-only experiment separately. If genuine thinking/tool history is absent, the switch criterion is untested, not passed. The observed model comes from unmodified response JSON/SSE; missing model or fallback attribution means incomplete. Current docs say unreadable prior-model thinking may be dropped; require compatibility and record loss, not impossible retention equivalence.

The diagnostic force must be a versioned, isolated experiment control after existing permission gates; never remap a remote Claude model as local, release a pin, or present forced choice as estimator output. At initial entry and all continuations maintain the permitted destination intersection. No automatic policy learner or automatic health refresh is enabled.

## Required bounded amendments before launch

1. SEM-007/FND-001/CAS-004: explicitly scoped Claude-to-Claude model selection/rewrite behavior, preserving non-model capabilities and native response semantics; test correct thinking handling at a legitimate boundary. Keep old decision wording in changelog. A new model-only rewrite exception cannot be smuggled under the non-Claude rewrite invariant.
2. RTG-001/FND-002/TRU-002: versioned experiment destination membership and explicit direct-upstream inventory/binding. No fake capability admission or pricing evidence; keep experimental qualification separate from enabled production rungs.
3. FND-005/EVL-005/EVL-009: determine an explicit permitted route for this finite compatibility experiment that does not bypass existing LIVE admission checks or relabel synthetic evidence as organic qualification. If this requires a scoped exception/new experiment profile, draft it for owner disposition; do not grant it ourselves. Prefer a minimal declared mechanism, not general infrastructure.
4. OPS-006/MEM-001 and CAS-006: prove model/usage/request lineage capture from the actual stream and no secret-bearing header log. Route decisions, served receipts and failed attempts retained; full learning-reader fixes are not a prerequisite.

These are pre-wave decisions and testable entry gates, not changes applied by this packet. Reviewer should identify whether an existing supported route avoids any amendment. Do not require building learning, fleet management or container orchestration for this spike.

## Proposed finite execution limits

After preparation, at most 60 minutes total execution/diagnosis, one isolated session, at most eight outbound Messages attempts including failures/retries/background calls, max 262144 body bytes per admitted request, max_tokens no greater than 4096, at most four count_tokens requests, max 90 seconds per forwarded request and one active request. These are proposed limits, not existing implemented controls. The launcher/proxy must demonstrate enforcement with offline fixtures before credential-bearing execution. An over-limit request is rejected before forwarding; no post-hoc hope that CLI turn counts cap model calls. Do not rewrite max_tokens silently; use a supported harness setting or stop on mismatch. The ceiling permits at most 32768 requested output tokens, not a total-token/cash guarantee; cumulative request-body bytes are separately bounded. No run until native included-usage/overflow policy has a concrete disposition. No purchased usage credit, paid API or model fallback is allowed by default. Fable review usage is separate and retained in reviewer metadata.

Two total bounded correction rounds for this spike at most; no automatic extension past a failed request/exposure boundary. Shutdown closes the dedicated proxy/session and removes the ephemeral connection settings; other Claude sessions and global config remain unchanged. Do not treat direct cloud bypass as recovery for a blocked/pinned request.

Retain sanitized structural request/response facts and synthetic input/output evidence for seven days in a private experiment directory; keep nonsecret hashes, verdict and review summary thereafter. No authorization headers/cookies/tokens, raw signatures or raw thinking text in retained diagnostics. Record thinking-block presence, provenance and unchanged-handling checks without logging content. No automation cleanup job is created here; cleanup is an explicit closure action with limitations reported.

## Acceptance table

- Subscription forwarding: actual request succeeds through ADRL with native credentials, beta preserved and no provider override; API-equivalent prices are not invoice savings.
- Control: incoming Opus, emitted target Sonnet, upstream response reports Sonnet, decision/attempt linked. Model metadata is provider-reported evidence, not independent server attestation.
- Compatibility: original history contains thinking + tool use, switched response and next continuation complete without unexplained request mutation or signature/tool errors. Preserve and report any native dropped-thinking indication.
- Limits/safety: offline denial tests establish no external dispatch for over-budget or forbidden destination; actual run respects them. Otherwise no live launch.
- Evidence: every attempt accounted for with failures, response model source, usage when present, output hashes and code/config/profile/harness versions. Missing usage means usage claim incomplete; no invented zeros.
- Disposition: controlled/compatible, initial-choice-only, explicit blocker, or inconclusive. None is generalized ROI, P1 graduation or production admission.

## Review request and ownership

Independently challenge this packet and the frozen actual source. Prioritize the cheapest valid experiment and exact blockers. Confirm whether the proposed routing path can operate under existing contracts, which changes are essential, and whether any apparent shortcut breaks admission, thinking, identity or accounting. Give go/no-go for the packet and distinguish implementation prerequisites from human access/experimental-policy dispositions. Do not execute, edit, delegate, call model tools, or promote grades. Maximum 700-word review preferred.

Owning decisions to be synchronized if implementation proceeds: SEM-007 anchor; FND-001/002/005, RTG-001, CAS-004/006/007, TRU-001/002, OPS-006, MEM-001, EVL-005/009 as applicable to the actual diff. This planning-only packet preserves existing ADR fields; no implementation closure receipt claimed for an unchanged source tree. Taxonomy pre-edit baseline is /Users/arunmenon/projects/.adrl-execution-state/claude-code-spike-baseline-20260909.json.

## Current primary references checked 2026-09-09

- https://code.claude.com/docs/en/llm-gateway#subscriptions-and-gateways : base-URL-only gateway retains native subscription; credential overrides change billing; OAuth beta must pass through.
- https://code.claude.com/docs/en/model-config : explicit model IDs and model/effort configuration; base URL does not itself choose the model.
- https://platform.claude.com/docs/en/build-with-claude/thinking : preserve thinking blocks; model-readability and prefix validity differ. Current page states direction-dependent dropped blocks; do not assume every model switch inherently errors. Account-dependent prefix enforcement means one successful run does not qualify every account.
