# AgentKit repository instructions

These instructions apply to every human or automated contributor working in this repository.

## Authority and current mode

Read, in order:

1. owner directives recorded in the repository and accepted consolidated ADRs under `docs/adr/`;
2. `docs/architecture/agentkit-v1-product-backlog.md` for planned scope and sequencing, subject to ADR status;
3. `ARCHITECTURE.md` only for legacy context that does not conflict with items 1–2;
4. the owner-approved roadmap/work packet, if one exists;
5. the assigned issue/task and its discussion;
6. relevant code and tests;
7. legacy ADRs under `adr/` for provenance only.

Higher items govern lower items. `docs/adr/ADR-001-framework-selection.md` is **Proposed**, not accepted: the three adapters are authorized v1 comparison targets, while selection of the default production path remains conditional on the AK-001 through AK-009 spike evidence. ADR-002 through ADR-009 under `docs/adr/` are accepted. The ADR-0001 through ADR-0004 documents under `adr/` are superseded and non-binding; `adr/README.md` records the exact replacement map. If code or a task contradicts an accepted architectural decision, stop and request an ADR or owner clarification. Do not silently redesign.

**Current mode is architecture/governance only. Implementation dispatch is not authorized.** Do not create autonomous jobs, Kanban implementation work, implementation branches, implementation PRs, or code changes unless the owner separately authorizes implementation scope.

## Non-negotiable architecture rules

1. Python support starts at 3.12.
2. Domain-agent packages own identity, instructions, skills, defaults, and domain context without importing hosting or execution-framework concerns.
3. Reuse framework-native messages, tools, models, stores, retrievers, middleware, checkpoints, HITL, and durability contracts where adequate. Agentkit-owned contracts are limited to stable product boundaries and require written justification.
4. LangGraph, Google ADK, and Microsoft Agent Framework are concrete v1 adapter targets. Do not introduce a generic multi-framework `Runtime`, graph, checkpoint, interrupt, session, or resume API, and do not flatten materially different semantics.
5. Plugins are independently installable Python packages discovered through entry points. Discovery never activates a plugin; only explicitly named/configured plugins activate, with deterministic composition and diagnostics.
6. Adding a provider must not require editing a central provider-name/type switch.
7. Every dynamic model-visible context contribution passes through the deterministic Context Builder with structured fragments, provenance, authorization, trust, sensitivity, TTL, and budget handling. Retrieved content remains data and cannot override protected instructions.
8. Conversation history, long-term memory, knowledge, and workflow checkpoints remain logically separate capabilities, even when physical storage is shared.
9. Durable execution, HITL, checkpointing, retries, resume, and workflow state remain native to each concrete adapter. Checkpointing is not arbitrary Python call-stack continuation.
10. External mutations are designed for at-least-once execution unless a provider proves stronger guarantees. Stable operation identity, durable intent/result where required, and explicit reconciliation govern replay safety.
11. Hosting and transport concerns remain outside domain-agent packages and execution adapters.
12. Public behavior, package resources, and adapter/plugin integrations must be proven from built artifacts in clean environments using only declared dependencies.

## Scope discipline

- Work on exactly one owner-authorized task at a time.
- Inspect open work before starting to avoid duplication.
- Keep a change small enough for one focused review.
- Do not broaden a task to build deferred target-state machinery.
- If a requirement is speculative, propose a time-boxed spike with a `VALIDATED`, `PARTIAL`, or `INVALIDATED` exit rather than committing public contracts.
- Never use chat history as the sole source of architectural or task state; durable repository artifacts and the authorized task govern.

## Change process

Before editing:

1. read the applicable architecture sections and ADRs;
2. inspect repository status and relevant neighboring modules/tests;
3. identify dependency, lifecycle, cancellation, persistence, configuration, packaging, and security impact;
4. confirm the task has implementation authorization.

During implementation:

- add or update tests with the behavior;
- keep public exports deliberately small;
- register cleanup immediately after resource acquisition;
- own spawned tasks and make cancellation behavior explicit;
- keep secrets out of source, logs, fixtures, snapshots, and PR text;
- use package-resource APIs rather than repository-relative paths;
- do not mask command failures.

Before handoff:

1. run focused checks, then the repository's complete required gates;
2. build the distribution;
3. run the clean-wheel external-consumer proof when packaging/public behavior changes;
4. inspect the full diff and run whitespace checks;
5. report exact commands and outcomes, including any unrun check or limitation;
6. update docs and ADRs when semantics changed.

## ADR triggers

Create or update an ADR before changing:

- ownership, lifecycle, versioning, or serialization of an Agentkit-owned product contract;
- plugin identity, packaging, discovery, explicit activation, compatibility, or composition semantics;
- Context Builder ordering, trust boundaries, scope, sensitivity, TTL, budgeting, omission, or provenance semantics;
- separation or lifecycle rules for conversation history, long-term memory, knowledge, and workflow checkpoints;
- adapter mappings for framework-native execution, HITL, durability, checkpoints, retries, or resume;
- replay-safety, idempotency, durable side-effect intent/result, or reconciliation guarantees;
- domain-agent package or host/transport ownership boundaries;
- the selected default production execution path or a claim that framework semantics are equivalent;
- any new generic cross-framework abstraction.

An implementation agent may propose an ADR but may not silently accept its own structural change.

## Review contract

Every implementation PR requires independent review. The implementer must not approve or merge its own PR.

Reviewers check, in this order:

1. authorized scope and acceptance criteria;
2. correctness and meaningful tests;
3. public API growth and dependency direction;
4. ToolInvoker bypass risk;
5. framework/provider leakage;
6. lifecycle ownership, failure unwind, and bounded shutdown;
7. stream bounds, abandonment, cancellation, and terminal-outcome rules;
8. persistence and checkpoint truth claims;
9. secret handling and security behavior;
10. wheel/package behavior and evidence accuracy.

Use severities:

- **BLOCKER:** architecture, security, correctness, data-loss, or lifecycle violation; must be fixed.
- **MAJOR:** material behavior, compatibility, test, or maintainability issue; normally fixed before merge.
- **MINOR:** non-critical improvement.
- **NIT:** style-only; never blocks alone.

Green tests do not override an architectural blocker. Claims in code, docs, and PRs must not exceed the evidence.

## Definition of done

A change is ready for review only when implementation, tests, focused verification, required documentation/ADR updates, and a complete PR description exist.

A change is done only when independent review is resolved, required checks pass on the final revision, the PR is merged or explicitly accepted under repository policy, and durable task evidence is updated. No implementation workflow is currently active; these rules apply once the owner authorizes one.
