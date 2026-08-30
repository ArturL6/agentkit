# ADR-001: Agent Execution Framework Selection

- **Status:** Proposed — pending implementation spike
- **Date:** 2026-08-30

## Context

We need an embeddable Python agent package with durable execution, HITL, custom models, memory, knowledge/retrieval, tools, middleware, and persistent conversation state.

We explicitly do not want to rebuild a graph runtime, checkpoint engine, interrupt/resume mechanism, tool loop, or session system from scratch.

We also want domain agent packages to remain independent from any one execution framework. Supporting more than one framework therefore requires a narrow translation boundary between Agentkit-owned product contracts and framework-native execution APIs.

## Decision

Do not build a new execution runtime.

Introduce **framework-specific execution adapters** as a concrete integration boundary. An execution adapter translates Agentkit-owned inputs such as agent package configuration, plugin contributions, and `ContextAssembly` into the native APIs and types of one execution framework. It does not reimplement that framework's workflow, state, checkpoint, interrupt, tool-loop, or resume semantics.

For v1, implement and evaluate the same non-trivial agent through concrete adapters for:

1. **LangGraph**
2. **Google ADK**
3. **Microsoft Agent Framework (MAF)**

Conceptually:

```text
Domain Agent Package
        ↓
Agentkit product contracts
        ↓
framework-specific execution adapter
        ↓
LangGraph / Google ADK / MAF
```

The adapter boundary is intentional. A generic multi-framework `Runtime` API is not.

Use framework-native extension contracts behind each adapter wherever possible. Do not normalize materially different workflow, state, checkpoint, middleware, interruption, or resume semantics merely to make the adapters look identical.

The implementation spike determines which adapter/runtime becomes the default for the first production path. MAF remains a first-class supported target rather than being deferred to an unspecified future abstraction.

Strands or other runtimes may be added later through their own concrete adapters when there is a product requirement.

## Spike Requirements

Test the same agent through the LangGraph, Google ADK, and MAF adapters with:

- model provider;
- memory provider;
- knowledge/RAG provider;
- tools;
- middleware/guardrail;
- observability;
- persistent conversation;
- conditional workflow;
- retry loop;
- human interruption;
- process kill/restart;
- replay/resume;
- clean Python package installation.

Document both shared behavior and framework-specific capability gaps. Do not hide a missing or different capability behind a lowest-common-denominator abstraction.

## Verification

The ADR becomes final only after the spike results for all three v1 adapters are documented and a default production execution path is selected.
