# Agentkit MVP operating model

**Status:** Owner-authorized implementation mode

## Goal

Deliver the smallest installable Agentkit package that runs one useful agent end to end, while establishing only the modular seams needed to extend models, tools, context, state, and execution adapters safely.

## Roles

- **Terra — implementation:** claim ready implementation tickets, work in an isolated task branch/worktree, implement the smallest acceptance-complete change, run tests/build/install proof, push, and open a PR.
- **Sol — architecture and design:** own design tickets, answer Terra's blocking product/contract/architecture questions, document decisions on the ticket or PR, and independently review the exact final PR head.
- **Hermes — orchestration:** keep Kanban dependencies and assignments accurate, route questions and reviews, verify remote state, and merge only an exact head with Sol `on_track`.

## MVP-0 moving-skeleton checkpoint

Before implementing the three framework adapters, Agentkit must produce one acceptance-bounded local demonstration with all of the following on the same revision:

1. Build a normal wheel containing the minimal core and one example domain-agent package/resource set required by the demonstration.
2. Install the wheel into a clean Python 3.12+ environment without editable or repository-relative imports.
3. Construct an agent through a small typed Python API using an injected deterministic fake model and one injected tool/capability.
4. Invoke the agent with one input, observe the tool/capability boundary, and receive the expected final output.
5. Run the same path through deterministic automated tests and a documented smoke command.
6. Keep model and tool implementations replaceable through narrow product-owned inputs without introducing a generic multi-framework runtime.

MVP-0 explicitly does **not** require long-term memory, knowledge retrieval, guardrails, telemetry backends, persistent conversation, branching, retries, HITL, checkpoints, external side effects, entry-point plugin discovery, three adapters, or a service host. Those remain in the full reference scenario and later tickets.

## Initial ticket interpretation

1. **AK-001 / Sol:** define both the complete comparative reference scenario required by the ticket and a separately labeled MVP-0 fixture limited to the six criteria above. The broad capability matrix is design/test input, not permission to implement every capability immediately.
2. **AK-002 / Terra:** create only the workspace, core/example package boundaries, and quality/build gates needed by MVP-0. Do not create empty adapter/plugin/host packages merely to resemble the eventual repository topology; add a package when the first consuming ticket needs it.
3. **AK-003 / Terra with Sol answers:** introduce only the narrow Agentkit-owned contracts exercised by MVP-0. Every extra public abstraction needs a concrete MVP-0 consumer or must wait.
4. **AK-004 / Terra:** make the reusable spike runner execute MVP-0 from a clean installation; this is the first working-agent checkpoint.
5. **AK-005 onward:** add concrete adapter and broader scenario capabilities incrementally while preserving the working MVP-0 smoke path.

AK-031 remains packaging of the full reference domain agent for v1 release. It does not prevent the earlier AK-004 moving-skeleton wheel and example from being installable test evidence.

The first demonstrable outcome is therefore complete at AK-004: a minimal agent that can be built, clean-installed, invoked, exercise one tool/capability boundary, and return a tested result. Multi-adapter durability, broad plugin catalogs, and production hardening are not prerequisites for that checkpoint.

## Execution rules

1. A ready, assigned Kanban ticket is already owner-authorized; no per-ticket approval round trip is required.
2. One worker owns one claimed ticket at a time. Dependencies remain authoritative.
3. Terra asks Sol when a decision would create or materially change a public contract, plugin/adapter boundary, state boundary, or durability guarantee.
4. Prefer a working vertical slice over speculative abstractions. Framework-specific semantics remain visible rather than forced into a universal runtime.
5. Every implementation change uses a task branch and GitHub PR with focused verification evidence.
6. Sol reviews the exact final PR head. `blocked` returns the ticket for changes; `on_track` permits Hermes to merge.
7. After merge, Hermes verifies the remote SHA, completes the ticket, and allows newly unblocked work to proceed.
