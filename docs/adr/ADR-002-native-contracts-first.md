# ADR-002: Reuse Framework-Native Extension Contracts First

- **Status:** Accepted
- **Date:** 2026-08-30

## Context

We want plugin ergonomics without rebuilding every abstraction ourselves.

With LangGraph/LangChain, mature seams already exist for models, tools, retrievers, vector stores, stores, checkpoint savers, middleware, nodes, and routing.

## Decision

The plugin SDK must prefer **framework-native contracts**.

For a LangGraph/LangChain implementation:

```text
Gateway plugin     -> chat-model interface
Checkpoint plugin  -> BaseCheckpointSaver
Memory plugin      -> BaseStore / supported store interface
Knowledge plugin   -> Retriever / VectorStore
MCP plugin         -> contributes Tools
Guardrail plugin   -> Middleware / hooks
Graph plugin       -> contributes nodes / edges when necessary
```

Create our own public port only when:

1. no adequate native seam exists;
2. it represents a real domain-level replacement boundary;
3. it is not merely a wrapper around one framework type;
4. more than one implementation or consumer justifies it.

## Rule

> Our plugin layer composes capabilities; it does not re-specify every capability.

## Consequences

This minimizes glue, preserves ecosystem compatibility, and prevents us from accidentally building another agent framework.
