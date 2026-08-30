# Agent Harness ADR Set

This set decomposes the larger framework-strategy ADR into focused decisions.

## Index

1. ADR-001 — Agent Execution Framework Selection
2. ADR-002 — Reuse Framework-Native Extension Contracts First
3. ADR-003 — Plugins Are Independently Installable Python Packages
4. ADR-004 — Separate History, Memory, Knowledge, and Checkpoints
5. ADR-005 — Deterministic Context Assembly (`soul.md`, `agent.md`, plugin layers)
6. ADR-006 — Hosting Runtime Is Separate
7. ADR-007 — Side Effects Must Be Replay-Safe
8. ADR-008 — Agent Is an Importable Python Package
9. ADR-009 — No Premature Multi-Runtime Abstraction

## Target Shape

```text
                 Domain Agent Package
      soul.md / agent.md / skills / defaults
                         │
                         ▼
                Thin Plugin Composition
                         │
         ┌───────────────┼────────────────┐
         ▼               ▼                ▼
       Memory         Knowledge          MCP
       plugin          plugin           plugin
         │               │                │
         └───────────────┼────────────────┘
                         ▼
                   Context Builder
             typed fragments + provenance
                         │
                         ▼
                   ContextAssembly
                         │
                         ▼
          Framework-Specific Execution Adapter
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        LangGraph    Google ADK       MAF
            └────────────┼────────────┘
                         ▼
                 Durable Execution
```

All dynamic model-visible context goes through the Context Builder rather than arbitrary prompt mutation.

Agentkit supports concrete execution adapters for LangGraph, Google ADK, and MAF while deliberately avoiding a universal lowest-common-denominator runtime abstraction. Hosting integrations remain separate from execution adapters.
