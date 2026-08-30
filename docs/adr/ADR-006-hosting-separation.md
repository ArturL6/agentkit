# ADR-006: Hosting Runtime Is Separate from Agent Execution Runtime

- **Status:** Accepted
- **Date:** 2026-08-30

## Decision

Keep hosting outside the core agent architecture.

```text
LiveKit / FastAPI / Worker / AgentCore Runtime
                  ↓
          host integration / entrypoint
                  ↓
          importable agent package
                  ↓
     framework-specific execution adapter
          ┌───────┼────────┐
          ▼       ▼        ▼
     LangGraph   ADK      MAF
```

LiveKit owns realtime media/session transport.

AgentCore Runtime, ECS, EKS, Kubernetes, and containers own process hosting.

The selected execution framework owns reasoning, workflow state, interrupts, checkpoints, tools, and resumability. The framework-specific execution adapter only translates Agentkit-owned product contracts into that framework's native APIs and wires the agent package into the framework.

Hosting integrations and execution adapters are separate concerns:

- a **hosting integration** adapts process lifecycle, transport, request/session ingress, and deployment environment;
- an **execution adapter** adapts Agentkit product contracts to LangGraph, Google ADK, MAF, or another supported execution framework.

The same domain agent package should run under multiple hosts without changing core agent code, and should be usable with multiple supported execution adapters without moving hosting concerns into the package.
