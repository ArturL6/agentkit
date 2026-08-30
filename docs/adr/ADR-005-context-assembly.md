# ADR-005: Deterministic Context Assembly with `soul.md`, `agent.md`, and Plugin-Contributed Layers

- **Status:** Accepted
- **Date:** 2026-08-30

## Context

Model-visible context can come from:

- stable identity;
- operational instructions;
- tenant/application policy;
- plugin instructions;
- conversation history;
- long-term memory;
- knowledge retrieval;
- workflow state;
- current user input;
- tools;
- approval/safety constraints.

If plugins mutate prompts independently, the result becomes an untestable prompt soup.

## Decision

Introduce a **Context Builder** as a small, deterministic model-context composition seam.

The Context Builder is not the memory system and not the workflow engine.

Its phases are:

```text
collect
  ↓
authorize / filter
  ↓
normalize
  ↓
deduplicate
  ↓
order
  ↓
apply token budgets
  ↓
render
  ↓
record provenance
```

## `soul.md`

`soul.md` defines stable identity and behavioral constitution.

Typical contents:

- values;
- tone;
- stable behavioral boundaries;
- interaction philosophy;
- identity.

It changes rarely and must not contain task-specific workflow logic.

## `agent.md`

`agent.md` defines the operational role.

Typical contents:

- responsibilities;
- operating procedure;
- tool-use guidance;
- domain assumptions;
- completion criteria;
- escalation behavior.

It may vary by agent package.

## Recommended Context Layers

```text
L0  Runtime invariants / hard platform policy
L1  soul.md
L2  agent.md
L3  application / tenant policy
L4  plugin system instructions
L5  session-derived summaries / context
L6  long-term memory retrieval
L7  knowledge / RAG retrieval
L8  workflow / runtime state
L9  current task / user input
```

Lower-trust layers may not overwrite protected higher-trust layers.

Retrieved documents are data, not automatically trusted system instructions.

## Typed Context Fragment

Conceptual API:

```python
@dataclass(frozen=True)
class ContextFragment:
    id: str
    source: str
    layer: ContextLayer
    content: str | Document | StructuredContext
    priority: int = 0
    scope: Scope = Scope.INVOCATION
    token_budget: int | None = None
    ttl_seconds: int | None = None
    merge_strategy: MergeStrategy = MergeStrategy.APPEND
    sensitivity: Sensitivity = Sensitivity.INTERNAL
    metadata: Mapping[str, Any] = field(default_factory=dict)
```

Important properties:

- stable ID for deduplication;
- source/plugin provenance;
- semantic layer;
- priority inside a layer;
- root/agent/session/invocation scope;
- optional token budget;
- TTL for ephemeral context;
- merge policy;
- sensitivity;
- metadata such as retrieval score and citations.

## Context Provider

Plugins may contribute context through a narrow contract:

```python
class ContextProvider(Protocol):
    async def provide(
        self,
        request: ContextRequest,
    ) -> Sequence[ContextFragment]:
        ...
```

Examples:

```text
SoulProvider
AgentInstructionProvider
TenantPolicyProvider
Mem0ContextProvider
KnowledgeContextProvider
WorkflowStateProvider
PluginInstructionProvider
```

## Final Assembly

Do not flatten everything unnecessarily.

Prefer:

```python
@dataclass
class ContextAssembly:
    system_sections: list[ContextFragment]
    history_messages: list[Message]
    retrieved_documents: list[ContextFragment]
    runtime_context: list[ContextFragment]
    tools: list[Tool]
    metadata: dict[str, Any]
```

`ContextAssembly` is an Agentkit-owned product contract. Each **framework-specific execution adapter** converts it into the native model/request representation required by LangGraph, Google ADK, MAF, or another supported execution framework.

This is a translation seam, not a universal workflow-runtime abstraction. Execution adapters may differ internally because their frameworks have different message, tool, state, middleware, checkpoint, and interruption semantics.

## Token Budgets

Budgets are policy, not provider implementation details.

Example:

```text
soul.md          800
agent.md        1500
tenant policy    800
memory          1500
knowledge       5000
workflow state  1000
```

When over budget:

1. preserve protected policy and identity;
2. preserve the current task;
3. prefer higher-ranked retrieval;
4. compact lower-priority material;
5. record what was omitted.

## Provenance

Observability must be able to answer:

> Why did the model see this context?

Every fragment should remain attributable to its provider/source, scope, timestamp/version, and retrieval metadata where available.

## Framework Integration

The Context Builder owns deterministic model-context composition. The selected execution framework owns execution.

For every supported framework:

```text
Context Builder
      ↓
ContextAssembly
      ↓
framework-specific execution adapter
      ↓
framework-native model / message / tool integration
      ↓
framework-native execution semantics
```

The LangGraph adapter should integrate through supported LangGraph/LangChain extension points rather than replacing graph execution.

The Google ADK and MAF adapters should likewise translate `ContextAssembly` through their supported native contracts rather than recreating their runtime behavior inside Agentkit.

## Verification

Tests must cover deterministic ordering, deduplication, token budgets, scope filtering, TTL, provenance, protected-layer precedence, and separation of memory from knowledge.

Adapter integration tests must additionally verify that the same `ContextAssembly` preserves required content, provenance, and tool exposure when translated to each v1 execution framework.
