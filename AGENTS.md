# AgentKit repository instructions

These instructions apply to every human or automated contributor working in this repository.

## Authority and current mode

Read, in order:

1. accepted ADRs under `adr/`;
2. `ARCHITECTURE.md`;
3. the owner-approved roadmap/work packet, if one exists;
4. the assigned issue/task and its discussion;
5. relevant code and tests.

Higher items govern lower items. If code or a task contradicts an accepted architectural decision, stop and request an ADR or owner clarification. Do not silently redesign.

**Current mode is architecture/governance only. Implementation dispatch is not authorized.** Do not create autonomous jobs, Kanban implementation work, branches, PRs, or code changes unless the owner separately authorizes implementation scope.

## Non-negotiable architecture rules

1. Python support starts at 3.12.
2. Keep the public `Agent` facade, `RuntimeSpec`, messages, tools, stream events, and session values framework-neutral.
3. Adapters depend on inward-facing contracts. Contracts and application/kernel code do not import concrete providers or agent frameworks.
4. LangGraph is an adapter. Its graph, message, command, config, checkpoint, and stream types stay inside its boundary.
5. Use typed explicit composition in v1. Do not add entry-point discovery, a registry/DAG, named bindings, a DI container, profiles/bundles, Hydra, richer scopes, canonical events, independent plugin wheels, or a plugin SDK without satisfying the gate in `ARCHITECTURE.md` and accepting an ADR.
6. Every AgentKit-managed tool execution must cross the kernel-owned `ToolInvoker`. Never expose a raw tool-callable route to a loop or framework adapter.
7. Public streaming is closed, bounded, and framework-neutral. Cancellation must propagate to owned work and each run must have exactly one terminal outcome.
8. Runtime resources must have recorded cleanup and bounded shutdown. Do not claim deterministic cleanup or reversible external effects.
9. v1 session persistence is product-shaped and minimal. Framework checkpoints are private; do not describe the repository as event sourcing or promise cross-framework replay.
10. One distribution is the v1 default. Passing in an editable checkout is not package proof; build and clean-install the wheel.
11. Do not implement hot in-process unload/reload.
12. Installed Python is trusted code; never claim AgentKit sandboxes in-process packages.

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

- public contract semantics;
- dependency direction or framework containment;
- `RuntimeSpec` or configuration precedence;
- ToolInvoker enforcement order or bypass rules;
- streaming/cancellation guarantees;
- lifecycle ownership or shutdown policy;
- session source-of-truth claims;
- plugin discovery, activation, identity, or dependency resolution;
- packaging topology or compatibility policy;
- any target-stage evidence gate.

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
