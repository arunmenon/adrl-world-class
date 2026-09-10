# LLD task: inventory reservations

This is a fictional detailed-design brief. Produce `lld.md`; code is optional
illustrative pseudocode only. Do not implement or deploy a service.

## Approved high-level boundary

- One service uses PostgreSQL as the authority for inventory and reservations.
  Transactions on that database are available. No distributed transaction is assumed.
- Inventory is keyed by `(tenant_id, sku)`. All API requests carry authenticated
  tenant identity. Cross-tenant access is forbidden even when IDs are guessed.
- A reservation requests a positive integer quantity. It either reserves the full
  quantity or fails; available stock must never become negative.
- `POST /reservations` takes SKU, quantity and a client idempotency key. Repeating
  the same request under the same tenant/key returns the original result. Reusing
  that key with a changed payload returns a conflict.
- A successful reservation expires after 15 minutes unless confirmed. Confirmation
  consumes the reserved stock. Cancellation or expiry releases stock once only.
- Confirmation, cancellation, expiry and retries can race. Specify permitted state
  transitions, atomic operations and their behavior on an already-terminal state.
- A worker scans for expiry. It may crash and repeat work. HTTP responses can be lost
  after the transaction commits. The design must handle both situations.
- Reservation-ID generation and authentication libraries are existing dependencies.
  No performance target beyond correctness has been supplied.

## Required deliverable

Provide API request/response/error examples, tables and keys, constraints, transaction
boundaries, state transitions, concurrency strategy and pseudocode for critical
operations. Include test scenarios with expected invariants for retries and races.
Show how you trace each detailed choice to the approved boundary or label it as an
additional assumption. A valid-looking schema alone is not sufficient.

Evaluation identifiers: LLD-1 tenant isolation, LLD-2 stock invariant, LLD-3 idempotency,
LLD-4 lifecycle/races, LLD-5 implementability and testability.
