# ADR-007: Design Side Effects for Replay and Resume

- **Status:** Accepted
- **Date:** 2026-08-30

## Decision

Assume **at-least-once execution around failure boundaries** unless a provider explicitly guarantees otherwise.

Rules:

1. keep durable work units reasonably small;
2. make mutations idempotent where possible;
3. use idempotency keys for external writes;
4. persist side-effect intent/result when exactly-once behavior matters;
5. isolate expensive or non-idempotent operations into explicit steps/nodes/tools;
6. never equate checkpointing with arbitrary Python call-stack continuation;
7. test process failure around important side effects.

Checkpoint/resume correctness is an application design concern as well as a framework feature.
