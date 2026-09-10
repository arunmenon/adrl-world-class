**Verdict: no-go for the forced Opus-to-Sonnet live launch as the source stands. Conditional go for a cheaper two-step scouting sequence that needs no policy exception.**

**Cheapest valid experiment**

The packet bundles two unknowns: whether Anthropic accepts Opus thinking-plus-tool history on Sonnet under this OAuth account, and whether ADRL can perform the switch. The first is the larger unknown and needs zero ADRL code.

1. **Step 0, no proxy.** Native Claude Code in the synthetic workspace, Opus turn with Read, then a mid-session `/model` switch to Sonnet and one continuation. The session transcript records the response model and usage per assistant message. Caveat: the harness may reshape history on its own switch, so this bounds compatibility from above rather than proving a proxy rewrite.
2. **Step 1, passthrough only.** Same script through ADRL in SHADOW routing with the upstream pointed at Anthropic. This exercises subscription forwarding, beta passthrough, and lineage capture from the real stream with no rewrite and no LIVE admission. Only the inventory fix below is required first.
3. **Step 2, forced rewrite.** Only if steps 0 and 1 pass, and only after amendments 1 to 4.

**Exact blockers in the frozen source**

- **No model-only rewrite exists.** The only code that sets a model is `strip_for_rung` in src/adrl/wire/rewrite.py, which refuses frontier bodies and strips thinking, output_config and cache markers. The probe's tool removal is an artifact of a server-tool-only fixture. Read has an input_schema and would survive. The thinking and output_config loss alone disqualifies it. Amendment 1 is essential.
- **Frame the force as intra-rung, not cheap_cloud.** Both candidate IDs already sit in the frontier name list in config/rungs.yaml. A within-rung served-model change is already contemplated by CAS-006 clause 2, and the same-family pair needs no CAS-004 transform. This keeps the permitted deployment set identical before and after the switch, avoids any cheap_cloud evidence question, and makes RTG-001 amendment unnecessary. It does not avoid amendment 1, since FND-001 clause 1 still forbids rewriting a frontier body.
- **Receipts would be mislabeled.** With no LiteLLM headers, `DeploymentPolicy.receipt` in src/adrl/gates/deployments.py returns the intended deployment as assumed. That deployment is the LiteLLM frontier entry, so the egress ledger would name the wrong host. A signed direct-Anthropic deployment entry is required even for step 1. Amendment 2 reduces to this one entry plus a receipt source that trusts the observed model when the upstream is the provider itself.
- **LIVE mode is unusable and unnecessary.** Every rung lacks an evidence reference, so LIVE fails at load. Adding a placeholder reference is fake admission. The experiment control should run under SHADOW as a versioned post-gate stage, which is the minimal declared mechanism amendment 3 asks for. That still requires owner disposition because FND-001 gains a clause.
- **Header leak to verify.** The connect command emits three custom headers, but the forwarding filter in src/adrl/wire/parse.py strips only two names. If the gates module's session header differs from the x-adrl-session-id name, a local identifier reaches Anthropic. One offline fixture settles this before any credential-bearing run.
- **No limit enforcement exists.** Attempt counts, body bytes, max_tokens, count_tokens caps and single-active-request are all unimplemented. The retry budget in config/policy.yaml allows two attempts per turn, which should be set to one so a failed switch is not silently retried. Timeout and health refresh are existing settings and can be set to the proposed values.
- **Workspace registration.** The connect command requires the checkout to match exactly one entry in the signed classification manifest with a class permitting the frontier rung. The synthetic workspace must be registered and the manifest re-signed.

**What already holds**

Authorization and beta pass through verbatim. The transport uses zero retries, does not follow redirects, and verifies TLS by default. The stream observer reads model and usage from message_start and message_delta and marks the source as proxy-observed. Redaction covers authorization, API keys and cookies.

**Shortcuts that break contracts**

Pointing the cheap_cloud group at Anthropic remaps a rung by label and fakes admission. Setting evidence references to pass LIVE is fake qualification. Running the cascade handoff on the switch would append a note and strip older thinking, which mutates the request and confounds the compatibility criterion. Skip the transform for the same-family pair.

**Also plan for**

Claude Code background calls may use Haiku and will count against the eight attempts. Sonnet may reject an effort value in output_config that Opus accepts. Record that as a boundary finding, not as a failure to preserve.

**Ownership split**

Implementation prerequisites: model-only rewrite stage, direct-upstream inventory entry and receipt source, limit enforcement with offline fixtures, header-name fixture, workspace registration. Human dispositions: the FND-001 clause for scoped Claude-to-Claude rewrite, the SHADOW experiment profile, and the included-usage overflow policy for the account.