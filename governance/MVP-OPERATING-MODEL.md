# Agentkit MVP operating model

**Status:** Owner-authorized implementation mode

## Goal

Deliver the smallest installable Agentkit package that runs one useful agent end to end, while establishing only the modular seams needed to extend models, tools, context, state, and execution adapters safely.

## Roles

- **Terra — implementation:** claim ready implementation tickets, work in an isolated task branch/worktree, implement the smallest acceptance-complete change, run tests/build/install proof, push, and open a PR.
- **Sol — architecture and design:** own design tickets, answer Terra's blocking product/contract/architecture questions, document decisions on the ticket or PR, and independently review the exact final PR head.
- **Hermes — orchestration:** keep Kanban dependencies and assignments accurate, route questions and reviews, verify remote state, and merge only an exact head with Sol `on_track`.

## Initial vertical slice

1. **AK-001 / Sol:** define one small but non-trivial reference agent and executable acceptance matrix.
2. **AK-002 / Terra:** scaffold the Python 3.12+ workspace, package boundaries, tests, lint/type/build gates, and clean-install smoke path.
3. **AK-003 onward:** introduce only product contracts required by the reference path, then build the reusable spike runner and concrete adapters incrementally.

The first demonstrable outcome is a minimal agent that can be installed, invoked, exercise at least one tool or capability boundary, and be tested from a clean environment. Multi-adapter durability, broad plugin catalogs, and production hardening follow through the existing dependency graph; they are not prerequisites for the first local demonstration unless an earlier ticket explicitly requires them.

## Execution rules

1. A ready, assigned Kanban ticket is already owner-authorized; no per-ticket approval round trip is required.
2. One worker owns one claimed ticket at a time. Dependencies remain authoritative.
3. Terra asks Sol when a decision would create or materially change a public contract, plugin/adapter boundary, state boundary, or durability guarantee.
4. Prefer a working vertical slice over speculative abstractions. Framework-specific semantics remain visible rather than forced into a universal runtime.
5. Every implementation change uses a task branch and GitHub PR with focused verification evidence.
6. Sol reviews the exact final PR head. `blocked` returns the ticket for changes; `on_track` permits Hermes to merge.
7. After merge, Hermes verifies the remote SHA, completes the ticket, and allows newly unblocked work to proceed.
