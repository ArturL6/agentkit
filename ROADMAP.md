# AgentKit Roadmap

## Binding direction

AgentKit will ship a **minimal, package-first vertical slice before plugin-host machinery**. The long-term target remains a full DeepSeek-Harness-inspired plugin system, introduced in evidence-gated stages rather than as the old 47-ticket starting plan.

This is a planning artifact, not a dispatch. Suggested lanes are routing hints only. If a card is separately dispatched, work is limited to that card on a dedicated task branch. No card authorizes work from another card, backlog expansion, merges, direct commits or changes to `main`, or autonomous follow-on implementation.

## Minimal architecture baseline

The first slice is one `agentkit` wheel with:

- a framework-neutral `Agent` facade and immutable typed `RuntimeSpec`;
- direct constructor/composition-root wiring and runtime-owned async cleanup;
- a small native model → tool → model loop;
- a kernel-owned, non-bypassable `ToolInvoker` for validation, policy, audit, timeout, and execution;
- a closed, bounded public stream with exactly one terminal outcome;
- product-shaped completed-message and tool/run audit persistence, not event sourcing;
- a clean-wheel external consumer proof using fake components.

Explicitly absent: entry-point scans, plugin manifests/registry/DAG, named bindings, capability version negotiation, DI scope hierarchy, generic hooks/event buses, Hydra/profile overlays, hot unload/reload, framework-independent replay, independent provider wheels, and public LangGraph types.

## Bounded board

Exactly seven cards are defined in `governance/kanban-backlog.json`.

| ID | Priority | Suggested lane | Outcome | Depends on |
|---|---|---|---|---|
| AK-001 | P0 | implementer | Public facade + explicit typed composition | — |
| AK-002 | P0 | implementer | Safe bounded model/tool invocation | AK-001 |
| AK-003 | P0 | implementer | Minimal product-shaped session persistence | AK-002 |
| AK-004 | P0 | implementer | Clean-wheel external consumer proof | AK-001, AK-002, AK-003 |
| AK-005 | P1 | architect | 1-day entry-point/import/duplicate spike | — |
| AK-006 | P1 | architect | 2-day LangGraph HITL/resume translation spike | — |
| AK-007 | P1 | architect | Architecture review and staged convergence | AK-004, AK-005, AK-006 |

## Dependency DAG

```text
AK-001 ──▶ AK-002 ──▶ AK-003 ──▶ AK-004 ──┐
   └───────────────────────────────▲       │
   └───────────────────────────────┘       │
                                           ├──▶ AK-007
AK-005 ────────────────────────────────────┤
AK-006 ────────────────────────────────────┘
```

AK-005 and AK-006 can run independently of the implementation chain. AK-007 is blocked until the clean-wheel slice and both time-boxed spikes provide evidence.

## Stages

### Stage 1 — Minimal vertical slice

Complete AK-001 through AK-004. Exit only when a freshly built wheel installs in an isolated consumer and proves public import, fake model → tool → model execution, product-shaped persistence, cancellation, one terminal outcome, and resource cleanup.

### Stage 2 — Falsification spikes

Run AK-005 and AK-006 as disposable, time-boxed experiments. Each exits `VALIDATED`, `PARTIAL`, or `INVALIDATED`; neither commits a public contract or production implementation.

### Stage 3 — Architecture convergence

AK-007 reconciles slice evidence, spike results, the red-team review, framework assessments, and owner direction. It records which original ideas are retained, deferred, simplified, or killed for v1 and defines measurable gates for later stages. It may recommend future card boundaries but may not create, dispatch, or implement them.

### Stage 4 — Evidence-gated plugin target (not ticketed or authorized)

The staged target may eventually include explicit entry-point discovery, selected/allowlisted plugin activation, deterministic duplicate identity rules, a small capability registry and dependency DAG, lifecycle-owned registrations/resources, typed configuration, LangGraph HITL as a private adapter, and—only with ecosystem demand—independent wheels.

Entry gates:

- **Entry points:** an external plugin consumer exists and AK-005 supports a trusted-import and duplicate policy.
- **Registry/DAG:** at least three activated extensions have dependencies explicit assembly cannot express cleanly.
- **New scope:** a measured lifetime cannot be represented by runtime ownership plus explicit invocation data.
- **Hooks/events:** a concrete 1:N/interception requirement has specified ordering, error, mutation, and cancellation semantics.
- **LangGraph adapter:** AK-006 validates one real HITL/resume translation without public leakage or duplicate side effects.
- **Common loop port:** a second production loop reveals a stable shared contract.
- **Independent wheels:** an external consumer, separate owner/release cadence, or dependency isolation justifies the release/security matrix.
- **Canonical replay/events:** two consumers need replay/projections and retention, privacy, migration, concurrency, and side-effect reconciliation are specified.

Never-stage targets: in-process hot unload/reload, optional or bypassable tool enforcement, runtime auto-installation, claims that import-time effects are reversible, or treating framework checkpoints as canonical session truth.

## Source synthesis

This plan applies the architecture red-team as the v1 constraint, uses the three framework assessments as decision evidence (runtime/composition, plugin/lifecycle, and agent-loop/session), and retains the original source brief as long-term intent where it does not conflict with the owner’s minimal-first decision. AK-007 is the explicit convergence point for remaining conflicts.
