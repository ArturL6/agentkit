# Legacy ADR set

The ADR-0001 through ADR-0004 documents in this directory formed Agentkit's original minimal-first baseline. They are retained unchanged except for their status line so repository history remains auditable. They are **superseded and non-binding**.

The consolidated ADRs under [`docs/adr/`](../docs/adr/README.md) and the [Agentkit v1 product backlog](../docs/architecture/agentkit-v1-product-backlog.md) govern current architecture and delivery. ADR-001 is proposed pending the comparative spike; ADR-002 through ADR-009 are accepted.

## Decision-by-decision supersession map

| Legacy decision | Status | Current replacement | Surviving principle |
| --- | --- | --- | --- |
| [ADR-0001 — Minimal-first staged plugin architecture](0001-minimal-first-staged-plugin-architecture.md) | Superseded | [ADR-003](../docs/adr/ADR-003-plugin-packaging-and-discovery.md), [ADR-009](../docs/adr/ADR-009-no-premature-runtime-abstraction.md), and AK-011–AK-016 | Explicit activation and no premature generic runtime remain; the one-distribution and deferred-entry-point decisions do not. |
| [ADR-0002 — Typed configuration and package-first API](0002-configuration-and-package-api.md) | Superseded | [ADR-003](../docs/adr/ADR-003-plugin-packaging-and-discovery.md), [ADR-008](../docs/adr/ADR-008-agent-package-boundary.md), [ADR-009](../docs/adr/ADR-009-no-premature-runtime-abstraction.md), and AK-002/AK-003/AK-011–AK-016/AK-031 | Programmatic typed package configuration remains first-class; a single universal `RuntimeSpec`, one composition root, and one-distribution topology are no longer binding. |
| [ADR-0003 — LangGraph boundary](0003-langgraph-boundary.md) | Superseded | Proposed [ADR-001](../docs/adr/ADR-001-framework-selection.md), accepted [ADR-002](../docs/adr/ADR-002-native-contracts-first.md), accepted [ADR-009](../docs/adr/ADR-009-no-premature-runtime-abstraction.md), and AK-004–AK-010/AK-023 | Framework containment remains; LangGraph is not preselected as the production default before comparative evidence, and no universal loop API is introduced. |
| [ADR-0004 — Kernel-owned tool invocation enforcement](0004-tool-invocation-enforcement.md) | Superseded | [ADR-002](../docs/adr/ADR-002-native-contracts-first.md), [ADR-007](../docs/adr/ADR-007-side-effects-and-resume.md), [ADR-009](../docs/adr/ADR-009-no-premature-runtime-abstraction.md), and AK-003/AK-015/AK-028–AK-030 | Tool safety, authorization, audit, and replay safety remain required, but a universal kernel-owned `ToolInvoker` is not a binding v1 abstraction; concrete adapters use the closest adequate native seams. |

Where a legacy sentence is not explicitly preserved in the final column, it has no governing force.
