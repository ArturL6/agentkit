# ADR-004: Conversation History, Long-Term Memory, Knowledge, and Workflow Checkpoints Are Separate Capabilities

- **Status:** Accepted
- **Date:** 2026-08-30

## Decision

The architecture distinguishes four state domains.

### Conversation / Session History
What happened in the conversation: messages, tool calls, tool results, metadata.

### Long-Term Memory
Information intentionally retained across sessions, such as user preferences or semantic/episodic memories.

### Knowledge / Retrieval
Authoritative or searchable external information: vector databases, document indexes, APIs, SQL, enterprise search.

### Workflow Checkpoints
Execution state needed to resume work: node state, branch position, pending interrupts, checkpoint history.

## Rule

```text
Conversation History != Long-Term Memory
Long-Term Memory     != Knowledge
Knowledge            != Workflow Checkpoint
Workflow Checkpoint  != Conversation History
```

They may share physical storage, but they must remain logically distinct.

Example:

```text
history       -> Postgres
memory        -> Mem0 / AgentCore Memory
knowledge     -> Qdrant
checkpointer  -> LangGraph Postgres saver
```
