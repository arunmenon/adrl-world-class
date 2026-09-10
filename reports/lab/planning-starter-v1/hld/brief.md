# HLD task: multi-tenant webhook delivery

This is a fictional architecture brief. Produce `hld.md`; do not implement a system.

## Fixed requirements and environment

- An existing service emits events containing `tenant_id`, `event_id`, event type
  and a payload. Event IDs are unique within a tenant.
- Customers register HTTPS webhook endpoints. Endpoint registration and credential
  storage exist already; design their use, not a replacement identity service.
- Normal aggregate traffic is 100 events/second; bursts reach 500/second for five
  minutes. Assume a 4 KB payload and a 24-hour maximum delivery/retry horizon.
- Delivery is at least once. Receivers must be given a stable idempotency identity;
  do not promise exactly-once side effects across the public network.
- One tenant's slow endpoint must not exhaust delivery capacity for other tenants.
- Each outgoing request must be authenticated with the tenant's configured signing
  secret. No tenant may select or receive another tenant's event or secret.
- Endpoints can time out, return 429/500, redirect or become unreachable. Describe
  the retry policy, destination validation and handling of unsafe destinations.
- Event payloads remain in the designated EU deployment. Delivery to a registered
  customer endpoint is permitted; external observability systems must not receive
  payload contents. Payload storage must expire within the stated horizon.
- The team can operate PostgreSQL and a managed queue. Use alternatives only with
  explicit benefits and operating costs. No budget or provider prices are supplied.

## Required deliverable

Cover components and data flow, tenant boundaries, persistence and delivery state,
capacity calculations, retries, idempotency, security, observability, retention,
failure recovery and alternatives. Include at least one text or diagrammed sequence.
State assumptions for overhead, retry volume and headroom in capacity calculations.

Evaluation identifiers: HLD-1 semantics, HLD-2 tenant boundaries, HLD-3 failures/fairness,
HLD-4 residency/retention, HLD-5 capacity and operating tradeoffs.
