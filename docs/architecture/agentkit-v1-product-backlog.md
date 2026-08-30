# Agentkit v1 Product Backlog

## Goal

Build Agentkit as an embeddable Python system for packaging domain agents independently from their execution framework and hosting environment. A domain agent owns its identity, instructions, skills, defaults, and domain-specific context, while Agentkit supplies deterministic context composition and thin capability/plugin composition. Durable execution, HITL, checkpoints, workflow state, retries, and resume behavior remain native to concrete LangGraph, Google ADK, and Microsoft Agent Framework (MAF) adapters.

The v1 outcome is:

- an importable domain-agent package that can run under more than one host;
- independently installable but explicitly activated plugins;
- deterministic, policy-aware context assembly with provenance;
- concrete LangGraph, Google ADK, and MAF adapters without a universal runtime API;
- a documented spike that selects the default production execution path;
- explicit separation of conversation history, long-term memory, knowledge, and workflow checkpoints; and
- replay-safe handling of external side effects and verified process restart/resume behavior.

## Source and Planning Assumptions

- The expanded revisions of ADR-001, ADR-005, ADR-006, and ADR-009 are treated as authoritative where the supplied copies differ.
- All three v1 execution adapters are real, installable integrations. The comparative spike selects one as the default production path; it does not remove the other two.
- Framework-native contracts are used whenever adequate. Agentkit-owned contracts are limited to product boundaries such as package configuration, plugin contributions, context fragments, and context assemblies.
- The reference agent used in acceptance tests must be the same across adapters and hosts.
- Story-point estimates are relative planning estimates, not elapsed time commitments.

## Architecture Guardrails

1. Do not implement a graph runtime, checkpoint engine, interrupt/resume engine, tool loop, or generic multi-framework `Runtime` API.
2. Do not normalize materially different framework semantics behind a lowest-common-denominator interface.
3. Installing a plugin never activates it automatically.
4. Adding a provider never requires editing a central provider-type switch.
5. All dynamic model-visible context passes through the Context Builder.
6. Retrieved content is data and cannot override protected instructions.
7. Conversation history, long-term memory, knowledge, and workflow checkpoints remain logically separate even when they share storage.
8. Checkpointing is not treated as continuation of an arbitrary Python call stack.
9. External mutations are designed for at-least-once execution unless a provider proves a stronger guarantee.
10. Hosting and transport concerns do not leak into domain-agent packages or execution adapters.

## Priority and Milestones

| Label | Meaning |
| --- | --- |
| P0 | Required to resolve architecture or unblock the v1 critical path |
| P1 | Required for the usable v1 release |
| P2 | Important follow-up or additional proof of portability |

| Milestone | Outcome |
| --- | --- |
| M0 — Framework decision | Three installable adapters are compared with the same durable agent; a default production path is selected. |
| M1 — Composition and context | Agent packages, plugins, and deterministic context assembly work across all adapters. |
| M2 — State and reliability | State domains are distinct, side effects are replay-safe, and restart/resume is verified. |
| M3 — Packaging and hosting | A reference agent is distributable, host-portable, observable, and release-ready. |

## Ticket Index

| ID | Title | Priority | Milestone | Points | Depends on |
| --- | --- | --- | --- | ---: | --- |
| AK-001 | Define the v1 reference agent and acceptance matrix | P0 | M0 | 3 | — |
| AK-002 | Scaffold the Agentkit package workspace and quality gates | P0 | M0 | 3 | — |
| AK-003 | Define narrow Agentkit-owned product contracts | P0 | M0 | 5 | AK-001, AK-002 |
| AK-004 | Build the reusable execution-adapter spike runner | P0 | M0 | 5 | AK-001, AK-003 |
| AK-005 | Implement and evaluate the LangGraph adapter | P0 | M0 | 8 | AK-004 |
| AK-006 | Implement and evaluate the Google ADK adapter | P0 | M0 | 8 | AK-004 |
| AK-007 | Implement and evaluate the MAF adapter | P0 | M0 | 8 | AK-004 |
| AK-008 | Run cross-adapter HITL, failure, replay, and resume tests | P0 | M0 | 8 | AK-005, AK-006, AK-007 |
| AK-009 | Select the default execution path and finalize ADR-001 | P0 | M0 | 3 | AK-008 |
| AK-010 | Harden the selected adapter as the first production path | P0 | M0 | 8 | AK-009 |
| AK-011 | Define the plugin descriptor and contribution model | P0 | M1 | 5 | AK-003 |
| AK-012 | Discover installed plugins through Python entry points | P0 | M1 | 3 | AK-011 |
| AK-013 | Implement explicit plugin activation and composition | P0 | M1 | 5 | AK-011, AK-012 |
| AK-014 | Add plugin compatibility and composition diagnostics | P1 | M1 | 3 | AK-013 |
| AK-015 | Build reference model, tool, guardrail, and telemetry plugins | P1 | M1 | 8 | AK-005, AK-006, AK-007, AK-013 |
| AK-016 | Define the domain-agent package contract and loader | P0 | M1 | 5 | AK-003, AK-013 |
| AK-017 | Implement typed context fragments and assemblies | P0 | M1 | 5 | AK-003 |
| AK-018 | Load `soul.md`, `agent.md`, and built-in context providers | P1 | M1 | 5 | AK-016, AK-017 |
| AK-019 | Implement the deterministic Context Builder pipeline | P0 | M1 | 8 | AK-017, AK-018 |
| AK-020 | Enforce context trust, scope, sensitivity, and TTL policy | P0 | M1 | 5 | AK-019 |
| AK-021 | Implement context token budgets and omission policy | P1 | M1 | 5 | AK-019, AK-020 |
| AK-022 | Record context provenance and expose diagnostics | P1 | M1 | 5 | AK-019, AK-020, AK-021 |
| AK-023 | Verify context translation in all three adapters | P0 | M1 | 8 | AK-005, AK-006, AK-007, AK-022 |
| AK-024 | Encode and document the four state-domain boundaries | P0 | M2 | 3 | AK-003, AK-013 |
| AK-025 | Integrate native conversation and checkpoint persistence | P0 | M2 | 8 | AK-010, AK-024 |
| AK-026 | Build a reference long-term-memory plugin | P1 | M2 | 5 | AK-013, AK-017, AK-024 |
| AK-027 | Build a reference knowledge/retrieval plugin | P1 | M2 | 5 | AK-013, AK-017, AK-024 |
| AK-028 | Introduce replay-safe side-effect primitives | P0 | M2 | 5 | AK-003, AK-010 |
| AK-029 | Persist side-effect intent/result and support reconciliation | P1 | M2 | 8 | AK-025, AK-028 |
| AK-030 | Add process-kill and side-effect fault-injection tests | P0 | M2 | 8 | AK-025, AK-029 |
| AK-031 | Package the reference domain agent for installation | P1 | M3 | 5 | AK-015, AK-016, AK-023, AK-026, AK-027, AK-030 |
| AK-032 | Define the host integration boundary and build a service host | P1 | M3 | 8 | AK-010, AK-016, AK-025 |
| AK-033 | Prove portability with a second hosting integration | P2 | M3 | 5 | AK-031, AK-032 |
| AK-034 | Deliver end-to-end observability and provenance correlation | P1 | M3 | 5 | AK-015, AK-022, AK-025, AK-029, AK-032 |
| AK-035 | Publish the v1 release, examples, and operator documentation | P1 | M3 | 8 | AK-031, AK-032, AK-034 |

## Global Definition of Done

Unless a ticket explicitly narrows the requirement, done means:

- code is typed and covered by unit or integration tests appropriate to the change;
- public behavior and configuration are documented;
- secrets and sensitive context are not emitted to logs or diagnostics;
- framework-native seams are used and any new Agentkit-owned abstraction is justified in the ticket or ADR;
- failure messages identify the package/plugin/adapter and the corrective action;
- examples run from a clean environment using only declared dependencies; and
- relevant architecture and end-to-end checks pass in CI.

---

## M0 — Framework Decision

### AK-001 — Define the v1 reference agent and acceptance matrix

- **Priority:** P0
- **Estimate:** 3 points
- **ADRs:** ADR-001, ADR-004, ADR-007

**Outcome:** Establish one non-trivial, framework-neutral acceptance scenario that every adapter and host must run without changing domain behavior.

**Scope:** Specify the agent's model, memory, knowledge retrieval, tools, guardrail, telemetry, persistent conversation, conditional branch, retry loop, HITL interrupt, and an externally visible side effect. Define test inputs, expected outputs, restart points, and evidence to collect. Keep framework-specific implementation details out of the domain fixture.

**Acceptance criteria:**

- [ ] The scenario includes every capability listed in ADR-001's spike requirements.
- [ ] Expected shared behavior and allowed framework-specific differences are explicit.
- [ ] Stable test fixtures exist for normal, retry, rejection, interruption, restart, and replay paths.
- [ ] The same agent package and scenario inputs are required for all three adapters.
- [ ] Pass/fail evidence can be captured without relying on manual observation alone.

### AK-002 — Scaffold the Agentkit package workspace and quality gates

- **Priority:** P0
- **Estimate:** 3 points
- **ADRs:** ADR-002, ADR-003, ADR-008

**Outcome:** Create a clean Python workspace that supports the core package, concrete adapter packages, plugin packages, host integrations, examples, and tests without coupling their dependencies.

**Acceptance criteria:**

- [ ] Core, adapters, plugins, hosts, and example-agent packages have explicit dependency boundaries.
- [ ] Each package can be built and installed from a clean environment.
- [ ] CI runs formatting, linting, type checks, unit tests, package builds, and installation smoke tests.
- [ ] Optional adapter/plugin dependencies do not become mandatory core dependencies.
- [ ] Package naming and supported Python versions are documented.

### AK-003 — Define narrow Agentkit-owned product contracts

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-001, AK-002
- **ADRs:** ADR-001, ADR-002, ADR-005, ADR-009

**Outcome:** Define only the stable product-owned inputs that agent packages, plugins, the Context Builder, and concrete adapters need to exchange.

**Scope:** Cover agent-package configuration, plugin contributions, invocation identity/configuration, `ContextFragment`, and `ContextAssembly`. Use framework-native messages, tools, models, stores, retrievers, middleware, and checkpoint types behind each adapter where adequate.

**Acceptance criteria:**

- [ ] Contract ownership, lifecycle, versioning, and validation rules are documented.
- [ ] No public generic runtime, graph, checkpoint, interrupt, session, or resume interface is introduced.
- [ ] Framework-specific capabilities can remain accessible without unsafe casts or hidden side channels.
- [ ] Contract tests prove deterministic serialization or comparison where fixtures require it.
- [ ] Every custom port includes a written justification against ADR-002's four criteria.

### AK-004 — Build the reusable execution-adapter spike runner

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-001, AK-003
- **ADRs:** ADR-001, ADR-009

**Outcome:** Provide one automated harness that runs the reference scenario against a selected concrete adapter and emits comparable evidence.

**Acceptance criteria:**

- [ ] The runner accepts the same domain-agent package, inputs, and scenario steps for each adapter.
- [ ] Adapter selection is concrete configuration, not a generic public runtime abstraction.
- [ ] Results capture capability support, semantic differences, timings, checkpoints, interrupts, resume behavior, and failures.
- [ ] The evidence format separates shared assertions from adapter-specific observations.
- [ ] A fake adapter fixture verifies the runner without creating a reusable fake runtime contract.

### AK-005 — Implement and evaluate the LangGraph adapter

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-004
- **ADRs:** ADR-001, ADR-002, ADR-005, ADR-009

**Outcome:** Deliver an installable LangGraph adapter that translates Agentkit product contracts into LangGraph/LangChain-native execution and runs the full reference scenario.

**Acceptance criteria:**

- [ ] Model, tools, retriever/store, middleware, graph routing, checkpointing, interrupts, retries, and resume use supported native seams.
- [ ] `ContextAssembly` is translated without losing required content, provenance references, or tool exposure.
- [ ] The adapter does not reimplement LangGraph workflow or durability semantics.
- [ ] Clean installation and the complete AK-001 scenario pass.
- [ ] Unsupported or different semantics are documented rather than silently normalized.

### AK-006 — Implement and evaluate the Google ADK adapter

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-004
- **ADRs:** ADR-001, ADR-002, ADR-005, ADR-009

**Outcome:** Deliver an installable Google ADK adapter that translates the same Agentkit contracts through ADK-native APIs and runs the full reference scenario.

**Acceptance criteria:**

- [ ] Native ADK extension, session, workflow, tool, callback/plugin, and persistence seams are used where adequate.
- [ ] `ContextAssembly` translation preserves required content, provenance references, and tool exposure.
- [ ] The adapter does not simulate missing semantics inside a hidden generic runtime layer.
- [ ] Clean installation and the complete AK-001 scenario pass or produce an explicit capability-gap result.
- [ ] Differences from LangGraph are recorded in comparable evidence.

### AK-007 — Implement and evaluate the MAF adapter

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-004
- **ADRs:** ADR-001, ADR-002, ADR-005, ADR-009

**Outcome:** Deliver an installable Microsoft Agent Framework adapter that translates the same Agentkit contracts through MAF-native APIs and runs the full reference scenario.

**Acceptance criteria:**

- [ ] Native MAF model, tool, middleware, workflow, state, HITL, and persistence seams are used where adequate.
- [ ] `ContextAssembly` translation preserves required content, provenance references, and tool exposure.
- [ ] The adapter delegates workflow and durability behavior to MAF.
- [ ] Clean installation and the complete AK-001 scenario pass or produce an explicit capability-gap result.
- [ ] Differences from LangGraph and ADK are recorded in comparable evidence.

### AK-008 — Run cross-adapter HITL, failure, replay, and resume tests

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-005, AK-006, AK-007
- **ADRs:** ADR-001, ADR-007, ADR-009

**Outcome:** Produce repeatable evidence for durability and recovery behavior at equivalent scenario boundaries across all adapters.

**Acceptance criteria:**

- [ ] Tests interrupt before and after model calls, tool calls, HITL requests, checkpoint writes, and external side effects.
- [ ] Each run kills the process, creates a new process, and resumes from persisted state.
- [ ] Duplicate, lost, and reordered external effects are detected explicitly.
- [ ] Replay/fork support and semantic differences are reported per framework.
- [ ] No test claims arbitrary Python call-stack continuation.

### AK-009 — Select the default execution path and finalize ADR-001

- **Priority:** P0
- **Estimate:** 3 points
- **Depends on:** AK-008
- **ADRs:** ADR-001, ADR-009

**Outcome:** Turn the proposed framework decision into an evidence-backed selection while preserving all three concrete adapters as v1 targets.

**Acceptance criteria:**

- [ ] The comparison covers correctness, HITL, restart/resume, replay/fork, native plugin seams, ecosystem fit, operational complexity, and custom glue.
- [ ] Capability gaps and non-equivalent semantics are visible.
- [ ] One adapter is named as the default first production path with rationale.
- [ ] ADR-001 status and decision are updated without weakening ADR-009.
- [ ] Follow-up risks have owners or backlog links.

### AK-010 — Harden the selected adapter as the first production path

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-009
- **ADRs:** ADR-001, ADR-002, ADR-007

**Outcome:** Promote the selected adapter from comparative implementation to the supported default path.

**Acceptance criteria:**

- [ ] Dependency versions, configuration defaults, persistence setup, migrations, and supported capability matrix are documented.
- [ ] Error handling covers invalid configuration, provider failures, checkpoint failures, and incompatible persisted state.
- [ ] Baseline latency, recovery time, and checkpoint-size measurements are recorded for the reference scenario.
- [ ] Upgrade and rollback expectations are stated.
- [ ] Release-blocking reliability checks run in CI.

---

## M1 — Composition and Context

### AK-011 — Define the plugin descriptor and contribution model

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-003
- **ADRs:** ADR-002, ADR-003

**Outcome:** Define how an independently installed package describes identity, compatibility, configuration, and contributions without redefining native framework contracts.

**Acceptance criteria:**

- [ ] Descriptors include stable ID, version, compatibility range, configuration schema, and contribution factories.
- [ ] Contributions can include native models, tools, stores, retrievers, middleware/hooks, checkpoints, context providers, and adapter-specific extensions.
- [ ] Plugin import has no activation side effects.
- [ ] The model supports more than one plugin for a capability where composition is valid.
- [ ] Adding a provider requires no central provider-name switch.

### AK-012 — Discover installed plugins through Python entry points

- **Priority:** P0
- **Estimate:** 3 points
- **Depends on:** AK-011
- **ADRs:** ADR-003

**Outcome:** Discover available plugin packages using a documented Python entry-point group while keeping discovery separate from activation.

**Acceptance criteria:**

- [ ] Discovery returns metadata without constructing providers or performing external I/O.
- [ ] Duplicate IDs, load errors, malformed descriptors, and incompatible versions produce actionable diagnostics.
- [ ] Discovery order does not change activation order or final composition.
- [ ] Unit tests use built distributions/entry points, not only monkey-patched registries.
- [ ] The command/API can list known versus explicitly active plugins.

### AK-013 — Implement explicit plugin activation and composition

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-011, AK-012
- **ADRs:** ADR-002, ADR-003

**Outcome:** Resolve an explicit agent configuration into a validated, deterministic set of active contributions.

**Acceptance criteria:**

- [ ] Only named/configured plugins activate; newly installed packages remain inert.
- [ ] Configuration is validated before provider construction or network access.
- [ ] Composition order and conflict rules are deterministic and documented.
- [ ] Missing, duplicate, incompatible, or mutually exclusive contributions fail with corrective guidance.
- [ ] Sensitive configuration is represented by references and is redacted from errors.

### AK-014 — Add plugin compatibility and composition diagnostics

- **Priority:** P1
- **Estimate:** 3 points
- **Depends on:** AK-013
- **ADRs:** ADR-002, ADR-003

**Outcome:** Let developers explain exactly which plugins and native seams will be used before an invocation starts.

**Acceptance criteria:**

- [ ] A diagnostic report lists installed, discovered, active, rejected, and shadowed plugins.
- [ ] Each active contribution is mapped to its consuming adapter/native seam.
- [ ] Version and capability mismatches are reported without exposing secrets.
- [ ] Report ordering is stable and snapshot-testable.
- [ ] Diagnostics do not import or activate unrelated plugins.

### AK-015 — Build reference model, tool, guardrail, and telemetry plugins

- **Priority:** P1
- **Estimate:** 8 points
- **Depends on:** AK-005, AK-006, AK-007, AK-013
- **ADRs:** ADR-001, ADR-002, ADR-003

**Outcome:** Prove non-state plugin composition using real native contracts needed by the reference agent.

**Scope:** Provide one configurable model gateway, one tool/MCP contribution, one guardrail or middleware contribution, and one OpenTelemetry-style observability contribution. Split distributions where dependencies or release cadence justify it.

**Acceptance criteria:**

- [ ] Each plugin is independently buildable and installable.
- [ ] Installation alone does not activate any plugin.
- [ ] Each adapter consumes the closest supported native contract.
- [ ] Configuration and secrets remain host supplied, not embedded in the agent package.
- [ ] Reference-agent tests demonstrate all four contributions.

### AK-016 — Define the domain-agent package contract and loader

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-003, AK-013
- **ADRs:** ADR-006, ADR-008, ADR-009

**Outcome:** Make a domain agent a normal Python package with a small construction API and no hosting or generic runtime implementation.

**Acceptance criteria:**

- [ ] A package can expose `create_agent` plus prompts, `soul.md`, `agent.md`, skills, defaults, and domain context providers.
- [ ] Package resources load correctly from both source and built wheel installations.
- [ ] Defaults can be overridden explicitly by the embedding application.
- [ ] The package does not own model gateways, checkpoint engines, graph execution, MCP transport, vector clients, or cloud hosting.
- [ ] Loader errors identify missing resources and invalid package configuration.

### AK-017 — Implement typed context fragments and assemblies

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-003
- **ADRs:** ADR-004, ADR-005

**Outcome:** Implement the typed, immutable inputs and structured output required for deterministic model-context composition.

**Acceptance criteria:**

- [ ] `ContextFragment` includes stable ID, source, layer, content, priority, scope, optional budget, optional TTL, merge strategy, sensitivity, and metadata.
- [ ] `ContextAssembly` keeps system sections, history, retrieved documents, runtime context, tools, and metadata structurally distinct.
- [ ] Layer, scope, merge, and sensitivity values are closed and documented.
- [ ] Invalid combinations fail before rendering.
- [ ] Equality/serialization behavior supports deterministic tests and provenance recording.

### AK-018 — Load `soul.md`, `agent.md`, and built-in context providers

- **Priority:** P1
- **Estimate:** 5 points
- **Depends on:** AK-016, AK-017
- **ADRs:** ADR-005, ADR-008

**Outcome:** Provide built-in providers for stable identity, operational instructions, tenant policy, plugin instructions, workflow state, and current input.

**Acceptance criteria:**

- [ ] `soul.md` and `agent.md` are loaded as distinct, attributable protected fragments.
- [ ] Package versions or content hashes are recorded for stable resources.
- [ ] Providers implement one narrow `ContextProvider` contract and return fragments without mutating global prompts.
- [ ] Missing optional providers are handled explicitly; missing required identity/instruction files fail clearly.
- [ ] Tests prove task workflow instructions do not leak into `soul.md` handling.

### AK-019 — Implement the deterministic Context Builder pipeline

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-017, AK-018
- **ADRs:** ADR-005

**Outcome:** Compose all model-visible dynamic context through one deterministic pipeline.

**Acceptance criteria:**

- [ ] The implementation performs collect, authorize/filter, normalize, deduplicate, order, budget, render, and provenance phases in that order.
- [ ] Stable IDs and documented tie-breakers make output independent of provider completion order.
- [ ] Merge strategies are explicit and validated.
- [ ] Final output remains a structured `ContextAssembly` until an adapter translates it.
- [ ] Unit tests cover ordering, duplicate fragments, provider failures, and deterministic repeated builds.

### AK-020 — Enforce context trust, scope, sensitivity, and TTL policy

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-019
- **ADRs:** ADR-005

**Outcome:** Prevent lower-trust or stale context from overriding protected policy and prevent unauthorized context from reaching a model or diagnostic surface.

**Acceptance criteria:**

- [ ] Protected L0–L3 content cannot be replaced by plugin, memory, retrieval, workflow, or user fragments.
- [ ] Retrieved documents are rendered as data, not promoted to system instructions.
- [ ] Root, agent, session, and invocation scope filters are enforced.
- [ ] Expired TTL fragments are omitted with a reason.
- [ ] Sensitivity and tenant/application authorization policy apply before budgeting and rendering.
- [ ] Adversarial prompt-injection fixtures prove protected-layer precedence.

### AK-021 — Implement context token budgets and omission policy

- **Priority:** P1
- **Estimate:** 5 points
- **Depends on:** AK-019, AK-020
- **ADRs:** ADR-005

**Outcome:** Apply centrally configured budgets without allowing individual providers to decide global context priority.

**Acceptance criteria:**

- [ ] Budgets can be configured globally and per semantic layer/provider.
- [ ] Protected identity/policy and the current task are preserved before lower-priority material.
- [ ] Ranked retrieval is reduced from lowest value first using deterministic tie-breakers.
- [ ] Compaction is distinguishable from omission and retains source provenance.
- [ ] Every omitted or compacted fragment has a machine-readable reason.
- [ ] Boundary tests cover exact budget, one-token overflow, and extreme overflow cases.

### AK-022 — Record context provenance and expose diagnostics

- **Priority:** P1
- **Estimate:** 5 points
- **Depends on:** AK-019, AK-020, AK-021
- **ADRs:** ADR-005

**Outcome:** Answer “why did the model see this?” for every included, compacted, rejected, and omitted fragment.

**Acceptance criteria:**

- [ ] Records include fragment ID, provider/source, scope, timestamp/version, layer, final position, token use, and retrieval/citation metadata where applicable.
- [ ] Exclusion, deduplication, compaction, and policy decisions are recorded.
- [ ] Diagnostic views redact sensitive content while retaining useful provenance.
- [ ] Assembly and invocation correlation IDs connect context decisions to model/tool traces.
- [ ] Provenance output is stable enough for snapshot and incident tests.

### AK-023 — Verify context translation in all three adapters

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-005, AK-006, AK-007, AK-022
- **ADRs:** ADR-005, ADR-009

**Outcome:** Prove that each adapter maps the same `ContextAssembly` into native requests without changing protected meaning or hiding framework differences.

**Acceptance criteria:**

- [ ] Golden fixtures cover system sections, conversation history, retrieved documents, workflow state, current input, and tools.
- [ ] Required ordering and protected boundaries survive each native translation.
- [ ] Provenance links remain correlated even where the framework request format differs.
- [ ] Tool names/schemas exposed to the model match the active plugin set.
- [ ] Unsupported native representations fail or document an explicit mapping; they are not silently flattened.

---

## M2 — State and Reliability

### AK-024 — Encode and document the four state-domain boundaries

- **Priority:** P0
- **Estimate:** 3 points
- **Depends on:** AK-003, AK-013
- **ADRs:** ADR-004

**Outcome:** Make conversation history, long-term memory, knowledge, and workflow checkpoints separately configurable and observable capabilities.

**Acceptance criteria:**

- [ ] Configuration uses distinct sections, identities, and lifecycle rules for all four domains.
- [ ] Shared physical storage, when used, has distinct namespaces/schemas and access paths.
- [ ] A capability cannot be substituted silently for another.
- [ ] Data retention, deletion, migration, and backup ownership are stated per domain.
- [ ] Architecture tests prevent package imports or configuration aliases that collapse the domains.

### AK-025 — Integrate native conversation and checkpoint persistence

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-010, AK-024
- **ADRs:** ADR-002, ADR-004, ADR-007

**Outcome:** Provide production-ready persistent conversation and workflow checkpoints on the default adapter using its native supported storage contracts.

**Acceptance criteria:**

- [ ] Conversation messages/tool records and workflow checkpoint state use logically distinct schemas or namespaces.
- [ ] Session/thread identity and checkpoint identity are explicit and never inferred from user-visible text.
- [ ] Restart from a new process resumes pending work and HITL state correctly.
- [ ] Concurrent update and stale-checkpoint behavior is defined and tested.
- [ ] Migration, cleanup, retention, and backup guidance exists for both domains.

### AK-026 — Build a reference long-term-memory plugin

- **Priority:** P1
- **Estimate:** 5 points
- **Depends on:** AK-013, AK-017, AK-024
- **ADRs:** ADR-002, ADR-004, ADR-005

**Outcome:** Prove cross-session memory as an independently installable capability that contributes attributable context without owning conversation history or knowledge retrieval.

**Acceptance criteria:**

- [ ] Memory read/write uses a native store contract where adequate.
- [ ] Retrieval returns L6 context fragments with stable memory IDs, scope, timestamps, sensitivity, and scores where available.
- [ ] Writes require explicit policy/intent and are not inferred from every conversation message.
- [ ] Tenant/user isolation, deletion, expiry, and duplicate handling are tested.
- [ ] Disabling the plugin removes memory behavior without affecting history or checkpoints.

### AK-027 — Build a reference knowledge/retrieval plugin

- **Priority:** P1
- **Estimate:** 5 points
- **Depends on:** AK-013, AK-017, AK-024
- **ADRs:** ADR-002, ADR-004, ADR-005

**Outcome:** Prove authoritative/searchable knowledge as a separate retriever/vector-store capability that contributes attributable data.

**Acceptance criteria:**

- [ ] Retrieval uses a native retriever or vector-store seam where adequate.
- [ ] Results become L7 data fragments with document/chunk identity, score, source, and citation metadata.
- [ ] Retrieved text cannot become protected instructions.
- [ ] Index lifecycle and query behavior do not mutate long-term memory or conversation history.
- [ ] Tenant/document authorization and duplicate-result handling are tested.

### AK-028 — Introduce replay-safe side-effect primitives

- **Priority:** P0
- **Estimate:** 5 points
- **Depends on:** AK-003, AK-010
- **ADRs:** ADR-007

**Outcome:** Give explicit nodes/tools a consistent way to identify and safely retry external mutations under at-least-once execution.

**Acceptance criteria:**

- [ ] Idempotency keys derive from stable operation identity, not process-local randomness.
- [ ] Operation inputs and result references are serializable without storing secrets unnecessarily.
- [ ] Provider adapters can pass native idempotency keys where supported.
- [ ] Non-idempotent or expensive operations must declare retry/reconciliation behavior.
- [ ] Duplicate invocation tests prove a supported provider mutation is applied once or safely reconciled.

### AK-029 — Persist side-effect intent/result and support reconciliation

- **Priority:** P1
- **Estimate:** 8 points
- **Depends on:** AK-025, AK-028
- **ADRs:** ADR-007

**Outcome:** Preserve enough durable information to resolve ambiguous outcomes when a process fails around an important external write.

**Acceptance criteria:**

- [ ] Intent is durably recorded before the external call when the operation requires it.
- [ ] Success, known failure, and unknown outcome are distinct states.
- [ ] Resume checks durable records and provider state before retrying an unknown operation.
- [ ] Reconciliation is explicit, observable, and safe to rerun.
- [ ] Sensitive payloads are minimized/redacted and retention rules are documented.

### AK-030 — Add process-kill and side-effect fault-injection tests

- **Priority:** P0
- **Estimate:** 8 points
- **Depends on:** AK-025, AK-029
- **ADRs:** ADR-001, ADR-007

**Outcome:** Continuously verify failure behavior at durable boundaries on the default production adapter.

**Acceptance criteria:**

- [ ] Tests kill the process before/after intent persistence, external mutation, result persistence, checkpoint persistence, and HITL response.
- [ ] A fresh process resumes using only durable state.
- [ ] Assertions detect lost, duplicate, or incorrectly reordered effects.
- [ ] At least one idempotent and one non-idempotent/reconciled tool path are covered.
- [ ] Failures preserve enough correlation data for diagnosis.
- [ ] The suite runs reliably in CI or a documented release-gate environment.

---

## M3 — Packaging and Hosting

### AK-031 — Package the reference domain agent for installation

- **Priority:** P1
- **Estimate:** 5 points
- **Depends on:** AK-015, AK-016, AK-023, AK-026, AK-027, AK-030
- **ADRs:** ADR-003, ADR-008

**Outcome:** Publish the AK-001 domain agent as a normal wheel that demonstrates the intended ownership boundary.

**Acceptance criteria:**

- [ ] `pip install` followed by `from <package> import create_agent` works in a clean environment.
- [ ] The wheel contains `soul.md`, `agent.md`, prompts, skills, defaults, and domain context providers.
- [ ] Optional plugins are declared separately and remain explicitly activated.
- [ ] No execution framework, hosting transport, cloud runtime, checkpoint engine, MCP transport, or vector client is implemented inside the domain package.
- [ ] The same wheel passes the supported scenario through all three adapters.

### AK-032 — Define the host integration boundary and build a service host

- **Priority:** P1
- **Estimate:** 8 points
- **Depends on:** AK-010, AK-016, AK-025
- **ADRs:** ADR-006, ADR-008

**Outcome:** Run an imported agent package through a service/worker host without moving transport or process-lifecycle concerns into the agent or adapter.

**Scope:** Define the host-owned ingress/session mapping, configuration/secrets, cancellation, health, shutdown, and deployment hooks. Implement one practical FastAPI or worker-style reference host.

**Acceptance criteria:**

- [ ] The host imports the domain package and selected adapter through documented construction APIs.
- [ ] Transport/session IDs map explicitly to conversation and checkpoint identities.
- [ ] Graceful shutdown, cancellation, health/readiness, and process restart are tested.
- [ ] Host configuration and secrets remain outside the agent wheel.
- [ ] The execution adapter contains no HTTP, media, container, or deployment lifecycle code.

### AK-033 — Prove portability with a second hosting integration

- **Priority:** P2
- **Estimate:** 5 points
- **Depends on:** AK-031, AK-032
- **ADRs:** ADR-006

**Outcome:** Demonstrate that the exact reference-agent wheel and execution adapter can run under a materially different host, such as LiveKit for realtime sessions or a managed worker runtime.

**Acceptance criteria:**

- [ ] No domain-agent source changes are required.
- [ ] No execution-adapter source changes are required beyond host-independent bug fixes.
- [ ] Host-specific transport, lifecycle, and deployment configuration live in the hosting integration.
- [ ] Conversation/checkpoint identity, HITL, cancellation, and resume behavior pass the portability suite.
- [ ] Any host capability gaps are documented without leaking workarounds into the agent package.

### AK-034 — Deliver end-to-end observability and provenance correlation

- **Priority:** P1
- **Estimate:** 5 points
- **Depends on:** AK-015, AK-022, AK-025, AK-029, AK-032
- **ADRs:** ADR-001, ADR-005, ADR-007

**Outcome:** Correlate one user invocation across host ingress, context assembly, native framework execution, model/tool activity, checkpoints, HITL, and side effects.

**Acceptance criteria:**

- [ ] Trace/log attributes include invocation, conversation, checkpoint, adapter, agent-package, and active-plugin identities.
- [ ] Context provenance links to the model request without logging protected or sensitive content.
- [ ] Resume and replay create intelligible parent/link relationships rather than misleading duplicate root traces.
- [ ] Side-effect intent/result and reconciliation events share operation correlation IDs.
- [ ] A troubleshooting runbook answers common failure and “why did the model see this?” questions.

### AK-035 — Publish the v1 release, examples, and operator documentation

- **Priority:** P1
- **Estimate:** 8 points
- **Depends on:** AK-031, AK-032, AK-034
- **ADRs:** ADR-001 through ADR-009

**Outcome:** Release a coherent v1 that a new team can install, configure, operate, and extend without violating the ADR boundaries.

**Acceptance criteria:**

- [ ] Versioned packages are built for core, all three adapters, reference plugins, host integration, and example agent.
- [ ] A clean-start guide reaches a successful durable invocation and resume.
- [ ] Guides cover building an agent package, building a plugin, selecting an adapter, configuring state domains, hosting, HITL, replay safety, and provenance.
- [ ] The framework capability matrix identifies the default path and non-equivalent behaviors.
- [ ] An architecture test/checklist explicitly guards against prompt mutation, auto-activation, state-domain collapse, hosting leakage, and a universal runtime abstraction.
- [ ] The full AK-001 acceptance scenario passes from published artifacts rather than workspace source.

## ADR Traceability

| ADR | Primary tickets |
| --- | --- |
| ADR-001 — Framework selection | AK-001, AK-004–AK-010, AK-015, AK-035 |
| ADR-002 — Native contracts first | AK-003, AK-005–AK-007, AK-011, AK-015, AK-025–AK-027 |
| ADR-003 — Plugin packaging/discovery | AK-002, AK-011–AK-015, AK-031 |
| ADR-004 — State and memory separation | AK-001, AK-017, AK-024–AK-027 |
| ADR-005 — Context assembly | AK-003, AK-017–AK-023, AK-026, AK-027, AK-034 |
| ADR-006 — Hosting separation | AK-016, AK-032, AK-033 |
| ADR-007 — Side effects and resume | AK-008, AK-010, AK-025, AK-028–AK-030, AK-034 |
| ADR-008 — Agent package boundary | AK-002, AK-016, AK-018, AK-031, AK-032 |
| ADR-009 — No premature runtime abstraction | AK-003–AK-009, AK-016, AK-023 |

## Suggested Delivery Order

1. Complete AK-001 through AK-009 to settle the default framework using executable evidence.
2. Start adapter hardening (AK-010), plugin composition (AK-011), agent packaging (AK-016), and context contracts (AK-017) as parallel streams.
3. Finish plugin composition and Context Builder work through AK-023 before claiming cross-adapter agent portability.
4. Complete the state and reliability path through AK-030.
5. Package the reference agent, integrate hosts, correlate observability, and release through AK-035.
