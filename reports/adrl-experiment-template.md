# ADRL experiment record template

Copy this template for one question. Unfilled fields are planning fields, not evidence that an experiment ran. Keep prompt-class material in its approved store and link by protected identifiers.

## Question

- Experiment ID and date:
- Owner:
- ADR IDs and exact current clause:
- Assumption being tested:
- What result would make us change this decision:
- Scope: harness, repository/workload slice, data permissions and exclusions:

## Before running

- Source snapshot/hash and configuration versions:
- Harness, gateway, model/deployment and serving configuration:
- Adapter version, protocol profile/version and API schema version:
- Effective coverage and unsupported paths for this integration:
- Initial state and task IDs:
- Current policy and alternative:
- Independent verifier and its measured limitations:
- Primary outcome, denominator and acceptable uncertainty:
- Run/repeat count and rationale:
- Paid-run cap and enforcing mechanism:
- Stop conditions and rollback:
- Experimental exposure/admission record, if needed:
- Tuning or confirmation set:

## Observed result

- Attempted, completed, accepted, failed and indeterminate counts:
- Paid cost, cache effects, latency and repair effort:
- Blocks, false pins, missing identities/receipts and missing records:
- Repeatability and differences by slice:
- Differences by harness/protocol, including integration setup time and manual interventions when relevant:
- Data origin and verification quality, recorded separately:
- Evidence locations and run identifiers:
- Limits: what this experiment cannot establish:

## Disposition

- Classification: implementation defect / parameter problem / design assumption / ownership conflict / insufficient evidence.
- Outcome: keep / tune / amend / replace / defer.
- Before and proposed after wording:
- Code/configuration changes and regression test:
- Security/privacy consequences and relevant owner decision:
- Maturity before and justified after, scoped to this implementation:
- Confirmation result on fresh tasks or the retained reproducer:
- Decision owner and disposition date:
- Linked register changelog, bucket overview and index updates:

## Next experiment

- Remaining uncertainty:
- Next smallest test that could resolve it:
