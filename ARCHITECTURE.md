# AgentKit architecture

**Status:** Owner-approved architecture baseline

**Language:** Python 3.12+

**Delivery strategy:** Minimal vertical slice first; plugin platform in evidence-gated stages

**Current phase:** Architecture and governance only; implementation dispatch is not authorized

## 1. Purpose and decision hierarchy

AgentKit is an installable Python package for building and running agents without making an agent framework, model SDK, or configuration framework part of the consumer contract.

This document separates two things that must not be confused:

- **Committed v0/v1 scope:** the smallest useful, testable package and its mandatory invariants.
- **Target-state stages:** a DeepSeek-Harness-inspired plugin architecture that may be introduced only when evidence justifies each additional mechanism.

The target state is direction, not a promise that all of it belongs in v1. Passing a simple demonstration does not prove deterministic reversibility, general event replay, hot replacement, or full agent-loop interchangeability.

The decision hierarchy is:

1. accepted ADRs;
2. this document;
3. an owner-approved roadmap or work packet;
4. the assigned issue/task;
5. implementation choices.

When these disagree, stop and resolve the higher-level contradiction. Structural changes require an ADR. No implementation work is authorized merely because it appears in this document.

## 2. Architectural thesis

AgentKit follows hexagonal architecture:

> Application code depends on framework-neutral ports and values. Concrete providers and agent frameworks adapt to those ports. Composition happens explicitly at the outer boundary.

The minimal design is deliberately not “everything is a plugin.” A seam becomes a public extension point only after real variation or external extension demand exists. The long-term plugin host remains a staged goal.

```text
consumer
   |
   v
public Agent facade + RuntimeSpec
   |
   v
application/kernel
   |-- Model port ---------------- concrete model adapter
   |-- Tool contracts -- ToolInvoker -- concrete tools
   |-- SessionRepository --------- memory/SQLite adapter
   `-- internal loop boundary ----- native or LangGraph adapter
```

Dependency direction is inward:

```text
public contracts <- application/kernel <- composition root
        ^                    ^                |
        |                    |                v
        +------------- adapters/providers/frameworks
```

Rules:

- Public contracts import no agent framework, provider SDK, persistence driver, Hydra, or plugin framework.
- The application/kernel imports no concrete provider.
- Adapters implement inward-facing contracts and may import their external SDKs.
- The composition root knows concrete implementations and wires them explicitly.
- Domain agents depend on the public Agent facade and domain values, not LangGraph types.

Import-boundary tests must enforce these directions even while all modules ship in one distribution.

## 3. Goals

AgentKit must:

1. install as a normal configurable Python 3.12+ package;
2. expose a small framework-neutral `Agent` facade;
3. accept a typed programmatic `RuntimeSpec` as the primary configuration API;
4. compose resources explicitly without ambient global configuration;
5. route every AgentKit-managed tool execution through a kernel-owned `ToolInvoker`;
6. provide bounded streaming and cooperative cancellation with one terminal outcome;
7. retain only the product-required session messages and tool/run audit data in v1;
8. contain LangGraph and provider SDK types inside adapters;
9. prove the public path from a built wheel in a clean external environment;
10. preserve a credible path toward a richer plugin architecture without implementing it prematurely.

## 4. Non-goals for v0/v1

The committed first slice does not include:

- entry-point plugin discovery;
- automatic activation of installed extensions;
- a capability registry or dependency DAG;
- independent plugin/provider wheels;
- stable public plugin IDs or capability-level version negotiation;
- named binding maps or a general service locator;
- root/agent/session/invocation resource-scope hierarchy;
- profiles, bundles, overlays, inheritance, interpolation, or Hydra;
- a generic hook bus, contribution bus, or runtime event bus;
- a canonical event-sourced session model or framework-independent replay;
- public plugin SDK/testkit distributions;
- hot unload, hot reload, or in-process plugin replacement;
- arbitrary import targets in configuration;
- untrusted-code sandboxing for installed Python packages;
- a claim that any advanced loop can be exchanged without behavior loss.

Hydra is not a core dependency. It may later be offered as an optional outer configuration adapter only if measured composition needs justify it.

## 5. Versioned scope

### 5.1 v0: architecture and governance

v0 is documentation and control-plane work only:

- this architecture baseline;
- accepted initial ADRs;
- repository instructions and PR template;
- explicit evidence gates for later stages.

There is no implementation dispatch in v0. Do not create autonomous implementation jobs, tickets, branches, or PRs unless the owner separately authorizes that work.

### 5.2 v1: one useful vertical slice

v1 will be one distribution, initially named `agentkit`, with internal module boundaries. Its exact internal filenames may evolve, but the conceptual ownership is:

```text
src/agentkit/
  __init__.py             # deliberately small public exports
  api.py                  # Agent facade and create_agent
  spec.py                 # immutable typed RuntimeSpec
  contracts/              # framework-neutral messages/model/tool/session values
  runtime.py              # explicit construction and resource ownership
  tool_invoker.py         # mandatory tool enforcement path
  loops/                  # internal loop boundary and implementation(s)
  adapters/               # framework/provider/persistence adapters
  sessions/               # minimal repositories
```

The v1 runnable path is:

```text
RuntimeSpec
  -> explicit composition
  -> model + tools + session repository + loop
  -> async Agent context
  -> model -> optional tool -> model
  -> bounded events and final result
  -> bounded shutdown
```

Minimum proof:

1. Construct a `RuntimeSpec` in Python.
2. Enter `async with create_agent(spec) as agent`.
3. Execute a fake-model `model -> tool -> model` run.
4. Observe bounded product-level stream events.
5. Verify every tool call crosses `ToolInvoker`.
6. Persist completed messages and the required tool/run audit records.
7. Cancel during model streaming and during a tool call without an orphan task or a second terminal event.
8. Build the wheel, install it into a fresh external virtual environment, and run the consumer without editable installs or repository-relative assets.

### 5.3 v1 success criteria

v1 is complete only when all of the following are demonstrated on the same revision:

- Python 3.12+ package metadata and wheel build succeed.
- The clean consumer imports only documented public names.
- Public serialized and streaming values contain no LangGraph/LangChain/provider types.
- `RuntimeSpec` can be built without a CLI, file, environment read, Hydra, or global state.
- Unknown or inconsistent configuration fails before opening external resources.
- The model and session implementations are injected through narrow contracts.
- Tools cannot be registered with or called by the loop except through `ToolInvoker`.
- Stream buffering and event payload sizes are bounded by documented limits.
- Cancellation reaches owned model/tool tasks and produces exactly one terminal result.
- Runtime-acquired resources are registered for cleanup and shutdown is bounded.
- Minimal session records support the demonstrated product flow.
- Architecture/import tests, focused tests, package build, and clean-wheel smoke test pass.

## 6. Public package API

The public API is programmatic first. The illustrative shape is:

```python
from agentkit import RuntimeSpec, create_agent

spec = RuntimeSpec(
    model=model_spec,
    tools=(tool_spec,),
    session=session_spec,
    limits=limits,
)

async with create_agent(spec) as agent:
    result = await agent.invoke("Find the answer")
```

Streaming is also framework-neutral:

```python
async with create_agent(spec) as agent:
    async for event in agent.stream("Find the answer"):
        ...
```

The final names and fields are implementation decisions within these constraints:

- `Agent` exposes product operations, not framework graph construction.
- Public values are immutable where practical and serializable where promised.
- No `StateGraph`, framework message, `RunnableConfig`, checkpoint, `Command`, or provider response type crosses the boundary.
- Extension dictionaries are not an excuse to tunnel unbounded framework state into public contracts.
- The initial public surface stays small; new exports require a compatibility review.

The v1 facade may be backed directly by one internal loop implementation. A stable public `AgentLoopPort` is not promised until a second meaningful implementation reveals a common contract.

## 7. RuntimeSpec and configuration

`RuntimeSpec` is the single validated input to composition. It is typed, explicit, and independent of any loader.

Required v1 characteristics:

- programmatic Python construction is primary;
- fields represent actual roles, such as `model` and an optional `review_model`, rather than arbitrary named-binding strings;
- tools, session repository, policies, and limits are explicit;
- values are immutable after validation;
- unknown fields are rejected at loader boundaries;
- secrets are supplied as references or already-resolved injected values, not printed in diagnostics;
- all enabled components are validated before side-effectful resource acquisition;
- no component independently reads ambient environment settings as hidden composition behavior.

An optional flat file loader may be added within v1 only when separately approved. If added, it performs one conversion:

```text
one complete document -> validation -> RuntimeSpec
```

It must not introduce inheritance, overlays, interpolation, `_target_` imports, profiles, or bundles. Constructor/API values, file values, environment values, and defaults must not silently compete; any supported precedence is documented and tested.

Hydra/OmegaConf remains outside core. A later adapter must terminate at `RuntimeSpec`; Hydra objects and global initialization must not cross into runtime or public contracts.

## 8. Explicit composition and lifecycle

v1 uses ordinary constructors/factories at one composition root. Direct typed construction is preferred over a registry or DI container.

Runtime ownership uses async context managers and an `AsyncExitStack` or equivalent standard-library mechanism. The runtime records cleanup immediately after acquiring each owned resource and closes in reverse acquisition order.

The guarantee is intentionally narrow:

- AgentKit provides **best-effort, bounded resource cleanup** for resources and tasks acquired through its runtime.
- It does not claim arbitrary side effects are reversible.
- It does not claim cleanup cannot fail or hang without bounds.
- It cannot reverse import-time effects, module globals, external writes, or tasks created outside its ownership rules.

v1 therefore requires:

1. validate before acquisition where possible;
2. record cleanup immediately after each acquisition;
3. stop accepting new work before shutdown;
4. cancel or drain owned invocation work according to documented policy;
5. bound shutdown and report aggregated cleanup errors without skipping later cleanup;
6. prohibit hot unload/reload;
7. prohibit unowned background tasks in runtime and adapters.

There are only two lifetime concepts in v1:

- **runtime resources**, owned by the Agent async context;
- **invocation context**, explicit data containing run/session IDs, principal, deadline, cancellation, and tracing context as needed.

Session is data, not a DI scope. Agent configuration is immutable data, not a resource scope.

## 9. Kernel-owned ToolInvoker

`ToolInvoker` is a mandatory kernel enforcement point, not an optional plugin.

```text
loop/framework adapter
       |
       v
ToolInvoker
  1. resolve registered ToolSpec
  2. validate input/schema and limits
  3. propagate invocation identity/principal
  4. obtain the required policy/approval decision
  5. write required audit state
  6. apply timeout and cancellation
  7. execute the tool implementation
  8. normalize/redact result or error
  9. write terminal audit state
       |
       v
framework-neutral ToolResult
```

Invariants:

- The loop receives only tool descriptions and an invocation callback owned by `ToolInvoker`; it never receives raw executable tool callables.
- LangGraph wrappers, if present, translate framework calls into `ToolInvoker.invoke(...)`.
- A tool implementation cannot register a parallel public execution path in AgentKit.
- Policy implementations may be replaceable inputs, but the decision point and invocation order are kernel-owned.
- Tool IDs, call IDs, deadlines, principal, and cancellation propagate end to end.
- Audit failure behavior is explicit; security-required pre-execution audit or authorization cannot silently degrade open.
- Repeated requests are not claimed idempotent unless a concrete idempotency contract exists for that tool.

This makes bypass structurally unavailable to conforming AgentKit loops and tools. It does not sandbox arbitrary trusted in-process Python code; a malicious installed package can ignore library conventions and call external systems directly.

## 10. Streaming and cancellation

The public stream is a small closed product vocabulary. v1 should include only events needed by the vertical slice, such as:

- text delta;
- tool requested;
- tool started;
- tool completed or failed;
- final result;
- run failed;
- run cancelled.

Rules:

- Exactly one terminal event/result occurs per run.
- No event appears after the terminal outcome.
- Buffers have fixed configurable bounds; a slow or abandoned consumer cannot create unbounded memory growth.
- Producer behavior when a buffer is full—backpressure, cancellation, or a documented coalescing rule—is explicit and tested.
- Text/event payload limits are explicit.
- Abandoning a stream triggers the documented cancel-or-detach policy; v1 should prefer cancellation for owned invocation work.
- Cancellation is cooperative and propagated into model requests, tool tasks, waits, and adapter streams.
- Cleanup has bounded time and a documented shielding policy.
- Framework debug/checkpoint/task streams are not forwarded wholesale.

Conformance tests cancel during model streaming, during a long tool call, and while the consumer is slow or abandons the stream.

## 11. Minimal session repository

v1 defines a product-shaped `SessionRepository`, not a public event-sourcing framework.

It stores only what the vertical slice needs, for example:

- normalized completed user and assistant messages;
- run status and terminal outcome;
- tool-call request/status/result metadata needed for audit and display;
- stable session/run/tool-call identifiers;
- references to large or sensitive artifacts rather than unbounded payload copies.

The initial repository may be in memory. SQLite is justified only if restart continuity is a v1 requirement. The contract must not promise:

- replay of arbitrary agent execution;
- reconstruction across unrelated loop frameworks;
- immutable retention forever;
- ordering with external side effects that no transaction can cover;
- event schema upcasting or projections;
- token-delta persistence by default.

If LangGraph is introduced, its checkpoints are private adapter artifacts. A checkpoint is not canonical session truth and its thread ID is not automatically the public session ID.

A canonical typed event spine is a later stage requiring explicit retention, privacy, sequencing, idempotency, transaction/reconciliation, schema migration, and two-consumer replay evidence.

## 12. LangGraph boundary

LangGraph is the intended first advanced agent framework. It is selected for flows that need demonstrated graph-shaped behavior such as branching, pause/resume, human approval, parallel graph work, or durable recovery.

It must not own:

- the public `Agent` facade;
- public messages or tool values;
- `RuntimeSpec`;
- tool execution or authorization;
- canonical session records;
- cancellation policy;
- public streaming types;
- provider ports.

Allowed adapter responsibilities include graph construction, reducers, nodes, framework stream consumption, and private checkpoint management. Translation occurs once at the adapter boundary.

For a simple model/tool loop, a small native loop is preferable because it exercises platform contracts directly. The project does not claim full loop replaceability until at least two implementations run a representative—not merely trivial—flow through a contract derived from observed common behavior. LangGraph-specific durable/HITL semantics may remain adapter capabilities rather than being forced into a lowest-common-denominator public port.

A LangGraph adoption must pass:

- forbidden-import checks outside the adapter;
- tool routing through `ToolInvoker`;
- canonical public stream translation with bounded buffering;
- model/tool cancellation tests;
- private checkpoint namespace/version tests;
- clean installation without requiring LangSmith, Agent Server, or a LangGraph deployment product.

## 13. Packaging and clean-wheel proof

v1 ships one distribution. Internal architectural boundaries are enforced by imports and tests, not multiplied release units.

A release candidate must:

1. build wheel and source distribution artifacts;
2. create a new external project/virtual environment;
3. install the built wheel, not the source tree or editable workspace;
4. import documented public API names;
5. construct a typed spec without repository files;
6. execute the fake model/tool vertical slice;
7. exercise cancellation and context cleanup;
8. load any packaged resources through `importlib.resources` from the installed wheel;
9. verify no undeclared runtime dependency or source-tree path is required.

Heavy adapters/providers may be optional extras inside the same distribution initially. Independent wheels are deferred until ownership, release cadence, external consumption, or dependency isolation pays their operational cost.

## 14. Target-state stages and evidence gates

Stages are cumulative. Crossing a gate requires an accepted ADR or update, a time-boxed proof where appropriate, tests, and an owner-authorized implementation packet. No stage is activated by aspiration alone.

### Stage 0 — Governance baseline (committed now)

Deliver the architecture, ADRs, repository instructions, and PR review contract. No implementation dispatch.

**Exit evidence:** owner acceptance of these artifacts.

### Stage 1 — Minimal package vertical slice (committed v1)

Deliver the one-wheel path described above: public facade, typed spec, explicit composition, ToolInvoker, bounded stream/cancellation, minimal repository, and clean-wheel proof.

**Exit evidence:** all v1 success criteria on one revision.

### Stage 2 — Prove advanced loop and selected seams

Potential work:

- LangGraph adapter for one real advanced flow;
- one additional meaningful loop implementation or a deliberate decision not to standardize a loop port;
- persistent private checkpoints where the flow needs recovery;
- narrow policy/interceptor seam if ToolInvoker has more than one real policy implementation.

**Entry gate:** a concrete product flow requires advanced graph behavior.

**Exit evidence:** representative behavior, translation, cancellation, checkpoint compatibility, and boundary tests. A simple ReAct parity demo is insufficient evidence for full loop replaceability.

### Stage 3 — Local plugin kernel inside the distribution

Potential work:

- explicit extension manifests/factories;
- selected activation;
- a small capability registry;
- dependency DAG and diagnostics;
- lifecycle ownership for extension registrations;
- no hot unload.

**Entry gate:** at least three activated extensions have real interdependencies or explicit assembly has become demonstrably error-prone.

**Required proof:** duplicate, missing, ambiguous, and cyclic dependencies fail before activation; startup failure unwinds owned registrations/resources; shutdown is bounded; typing claims are limited to what static checks and conformance suites establish.

**Constraint:** PEP 440/package dependencies own install compatibility; do not invent runtime semver solving without separate evidence.

### Stage 4 — External plugin ecosystem

Potential work:

- `importlib.metadata` entry-point discovery;
- independently distributed provider/plugin wheels;
- plugin SDK and conformance testkit;
- allowlists and distribution provenance;
- release compatibility policy.

**Entry points gate:** one third-party extension maintained outside the repository needs package-native discovery, and a spike documents duplicate names plus import-time side-effect limits.

**Independent wheels gate:** separate owner/release cadence, real external consumer, or material dependency isolation exists.

**Plugin SDK gate:** at least two external authors repeat enough safe boilerplate to define an observed SDK.

**Security proof:** pinned/controlled artifacts, origin/version diagnostics, duplicate rejection, explicit selection, no runtime auto-install, environment isolation guidance, and documented trust boundary.

Discovery and activation remain separate. Entry-point enumeration does not provide safe pre-import AgentKit manifests; selected factory imports are trusted and may have non-reversible effects. Documentation must state this honestly.

### Stage 5 — Rich composition, scopes, and session spine

Potential work is independently gated:

- **profiles/bundles:** only after at least three complete configurations show measured duplication and deterministic precedence requirements;
- **Hydra adapter:** only after profile/experiment composition pain exceeds a small loader/factory approach; Hydra remains optional and produces `RuntimeSpec`;
- **named bindings:** only when arbitrary caller-defined model roles are required beyond explicit fields;
- **new resource scope:** only when a measured lifetime cannot be represented by runtime ownership plus invocation data; inheritance/override/concurrency semantics must be specified first;
- **canonical events:** only when two independent consumers need stable replay/projections and retention, privacy, sequencing, idempotency, reconciliation, and migration policies are designed;
- **generic hook/event buses:** only for concrete fan-out/interception needs with ordering, failure, cancellation, and mutation semantics specified.

### Explicitly rejected target claims

- Hot in-process module/plugin replacement is not a target. Development reload means process restart; future zero-downtime replacement would require process isolation.
- “All side effects are reversible” is not a target. Resource ownership and cleanup are narrower than external effect reversal.
- “All loops are fully replaceable” is not a target until representative multi-implementation evidence exists.

## 15. DeepSeek-Harness inspiration

The target architecture retains useful DeepSeek-Harness/Cordis ideas:

- external frameworks and providers stay at boundaries;
- installed capabilities may eventually be selected and composed explicitly;
- runtime registrations and resources have owners;
- discovery is distinct from activation;
- richer profiles and plugin packages can become useful at scale.

AgentKit does not copy Cordis APIs or assume its TypeScript mechanics transfer directly to Python. Python imports are executable, annotations are not runtime enforcement, and package/plugin ecosystems carry release and security costs. AgentKit adopts the direction in measured stages rather than starting with the host machinery.

## 16. Security and trust

- Installed Python packages are trusted in-process executable code; AgentKit does not sandbox them.
- AgentKit never auto-installs code at runtime.
- Public configuration must not accept arbitrary import paths.
- Secrets must not appear in committed config, logs, errors, stream events, or PR evidence.
- Tool authorization, identity propagation, timeout/cancellation, and required auditing run through `ToolInvoker`.
- Redaction and artifact references are applied before data crosses persistence or public-stream boundaries.
- Dependency auditing, lock/hashes, artifact provenance, and SBOM generation become mandatory before an external plugin-wheel ecosystem.

## 17. Testing and merge gates

The repository should add exact commands as tooling lands. At minimum, implementation PRs must eventually run:

- formatting and lint checks;
- strict type checks for supported public code;
- unit and integration tests;
- architecture/forbidden-import tests;
- ToolInvoker enforcement tests;
- stream bound, abandonment, and cancellation tests;
- resource cleanup/failure-injection tests;
- package build and wheel metadata checks;
- clean-wheel external consumer test.

Claims must match evidence. Editable-install success is not wheel proof. A cleanup callback running is not deterministic reversibility. A trivial second loop is not proof of replacement for durable/HITL workflows.

Live-provider tests are optional, credentialed lanes. Keyless fake/replay tests remain the default merge path.

## 18. Governance and change control

Before implementation, read `AGENTS.md`, this document, relevant accepted ADRs, and the owner-authorized task. The task is the scope boundary.

An ADR is required before changing:

- dependency direction or framework boundaries;
- public Agent, streaming, tool, model, session, or `RuntimeSpec` semantics;
- the mandatory ToolInvoker path;
- configuration precedence or loader strategy;
- lifecycle ownership/cancellation guarantees;
- session source-of-truth claims;
- entry-point discovery/activation rules;
- capability identity/resolution;
- packaging topology;
- evidence gates or stage promotion.

A PR is not complete because tests are green. Reviewers must verify scope, architecture, lifecycle, cancellation, security, packaging, and the truthfulness of claims. No agent may merge its own PR. No autonomous dispatch is enabled until the owner explicitly authorizes it.

## 19. Stage-promotion checklist

A proposal to enter a later stage must include:

1. the observed problem and evidence that v1 mechanisms are insufficient;
2. the precise gate from section 14;
3. a time-boxed spike result (`VALIDATED`, `PARTIAL`, or `INVALIDATED`) when uncertainty is material;
4. the smallest new public semantics, if any;
5. lifecycle, cancellation, security, packaging, and migration consequences;
6. tests that would falsify the proposal;
7. an accepted ADR;
8. explicit owner authorization for implementation dispatch.

Absent this evidence, keep explicit composition and the smaller contract.

## 20. Durable invariants

1. Public AgentKit contracts are framework-neutral.
2. Adapters depend inward; contracts do not depend outward.
3. `RuntimeSpec` is typed, programmatic-first, and loader-neutral.
4. Composition is explicit until evidence earns a registry.
5. Every AgentKit-managed tool call crosses kernel-owned `ToolInvoker`.
6. Public streams are closed, bounded, and framework-neutral.
7. Cancellation is cooperative, propagated, and tested; each run has one terminal outcome.
8. Runtime-owned resources have recorded cleanup and bounded shutdown, without a reversibility claim.
9. v1 sessions are product-shaped records, not general event sourcing.
10. LangGraph owns only adapter-internal orchestration and checkpoints.
11. One wheel is the default until ecosystem evidence earns more.
12. Clean-wheel execution is required evidence.
13. Plugin machinery and richer composition enter only through explicit gates.
14. Structural change requires an ADR.
15. Implementation dispatch requires separate owner authorization.
