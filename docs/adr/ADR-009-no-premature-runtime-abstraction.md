# ADR-009: Do Not Introduce a Generic Multi-Framework Runtime Abstraction Prematurely

- **Status:** Accepted
- **Date:** 2026-08-30

## Context

Agentkit is intended to support multiple execution frameworks, including LangGraph, Google ADK, and Microsoft Agent Framework (MAF). Supporting those frameworks requires concrete integration code.

A generic API such as:

```python
Harness(
    runtime=LangGraphRuntime(),
    plugins=[...],
)
```

looks attractive, but LangGraph, ADK, MAF, and Strands have materially different state, workflow, middleware, interruption, and checkpoint semantics.

The risk is not having adapters. The risk is prematurely pretending those different runtimes share one stable execution model.

## Decision

**Concrete framework-specific execution/runtime adapters are part of v1.**

The initial adapter targets are:

- LangGraph;
- Google ADK;
- Microsoft Agent Framework (MAF).

Each adapter translates narrow Agentkit-owned product contracts into framework-native APIs. Examples of product-owned inputs include agent package configuration, plugin contributions, and `ContextAssembly`.

Adapters must delegate execution semantics to their framework rather than reimplementing them.

Do **not** create a public universal runtime interface in v1 that attempts to normalize:

- graph or workflow models;
- state schemas;
- checkpointing;
- interruption and HITL;
- retry and resume behavior;
- middleware lifecycle;
- replay/fork semantics;
- framework-specific session behavior.

Conceptually:

```text
                         Agentkit
                            │
                  narrow product contracts
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
 LangGraph adapter      ADK adapter       MAF adapter
          │                 │                 │
          ▼                 ▼                 ▼
     LangGraph          Google ADK            MAF
```

The adapters are concrete boundary implementations, not subclasses of a guessed lowest-common-denominator runtime model.

Only extract a broader shared runtime abstraction later if production experience demonstrates that it is useful. Before doing so:

1. at least two adapters must be exercised in real product paths;
2. repeated semantics must be visible in actual implementation rather than inferred from documentation;
3. conformance tests must show that the proposed shared behavior is genuinely equivalent;
4. the abstraction must preserve access to framework-native capabilities rather than hiding them.

Shared helper code used by multiple adapters is allowed. A universal execution contract is not required merely because multiple adapters exist.

## Consequence

We can support LangGraph, Google ADK, and MAF from the start without turning Agentkit into a lowest-common-denominator agent framework.

Domain packages and Agentkit product contracts stay portable, while workflow and durability semantics remain owned by the selected execution framework.
