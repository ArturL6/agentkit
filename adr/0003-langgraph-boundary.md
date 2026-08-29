# ADR-0003: LangGraph is an advanced adapter, not a public contract owner

## Status

Accepted

## Context

LangGraph is the intended first advanced agent framework because it supports graph-shaped orchestration, streaming, checkpoints, pause/resume, and human-in-the-loop flows. Those strengths are expressed through framework-specific graph state, reducers, commands, stream modes, checkpoint schemas, and thread identity. Allowing those types to define AgentKit would make the framework the platform.

Conversely, designing a rich stable `AgentLoopPort` before a second meaningful implementation risks either a lowest-common-denominator contract or a LangGraph-shaped abstraction. A trivial second ReAct loop would not prove replacement of durable or human-in-the-loop behavior.

## Decision

AgentKit owns a small framework-neutral public `Agent` facade and the product-level values used by invoke/stream operations. LangGraph is contained in an adapter/internal loop module.

LangGraph must not own public messages, tools, `RuntimeSpec`, tool invocation, session records, cancellation policy, provider ports, or public stream event types. All tool calls from a LangGraph graph route through kernel-owned `ToolInvoker`. LangGraph streams are translated into the bounded closed AgentKit stream vocabulary. Framework checkpoints remain adapter-private recovery artifacts and are not canonical session truth.

A simple model/tool flow may use a small native loop. LangGraph is introduced when an owner-approved product flow needs advanced graph behavior. AgentKit does not promise a stable public `AgentLoopPort` or full loop replaceability until at least two meaningful implementations reveal and pass a representative common contract. Framework-specific capabilities may remain adapter-specific rather than contaminating the public facade.

## Alternatives considered

### Make LangGraph the public application model

Rejected. This would leak framework messages, graph state, configuration, persistence, and streaming semantics into consumers and domain agents.

### Define the complete AgentLoopPort before implementation

Rejected for now. The common abstraction is not yet supported by evidence from two meaningful implementations.

### Reject LangGraph entirely

Rejected. It is the intended advanced engine when a real flow benefits from its graph and recovery features.

### Always use a native loop

Rejected as a general rule. A native loop is appropriate for simple flows but should not recreate advanced workflow machinery without need.

## Consequences

Positive:

- domain and consumer code remains framework-neutral;
- LangGraph can provide advanced behavior without owning platform policy;
- checkpoint compatibility does not define session compatibility;
- replacement claims remain evidence-based.

Negative:

- the adapter must translate messages, tools, streams, IDs, errors, and cancellation;
- some LangGraph-specific behavior may not be available through the common facade;
- a stable loop extension contract is postponed.

## Compatibility

No LangGraph, LangChain, `StateGraph`, framework message, `RunnableConfig`, `Command`, checkpoint, or stream-part type may appear in public annotations or serialized records. Adapter checkpoint versions may change independently and must be namespaced/versioned if persistence is added.

## Verification

- Forbidden-import tests permit framework imports only in the adapter boundary.
- Public API and serialized values contain no framework types.
- LangGraph-facing tools call `ToolInvoker`; raw tool implementations are not passed to the graph.
- Stream translation is bounded and emits exactly one terminal outcome.
- Cancellation during model streaming and tool execution leaves no owned orphan task.
- Private checkpoint changes cannot mutate the minimal session repository contract.
- A clean wheel does not require LangSmith, Agent Server, or hosted LangGraph infrastructure.

## Supersedes / superseded by

Supersedes LangChain-as-initial-loop wording and any unproven claim of full loop replaceability.
