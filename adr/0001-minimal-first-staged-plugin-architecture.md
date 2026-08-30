# ADR-0001: Minimal-first staged plugin architecture

## Status

Superseded by the consolidated v1 ADR set and product backlog. See `README.md` in this directory for the decision-by-decision replacement map.

## Context

The original target architecture proposed a full plugin host before a useful AgentKit agent existed: entry-point discovery, stable plugin and capability identities, dependency resolution, lifecycle scopes, reversible effects, profiles/bundles, independent distributions, hooks, and canonical events. The design is a useful target but commits public semantics and operational cost before real extension pressure exists.

Python entry points do not contain AgentKit manifests and importing a selected factory executes trusted Python code. A registry/DAG plus named bindings and scopes would amount to a framework of its own. Independent wheels multiply release and compatibility work. `AsyncExitStack` supports cleanup ordering but cannot make arbitrary effects reversible.

The owner approved a minimal vertical slice first while preserving the DeepSeek-Harness-inspired architecture as a staged direction.

## Decision

AgentKit will begin as one installable Python 3.12+ distribution with internal hexagonal boundaries and explicit composition.

The committed v1 slice consists of a framework-neutral Agent facade, typed `RuntimeSpec`, narrow model/tool/session contracts, kernel-owned `ToolInvoker`, bounded streaming and cancellation, minimal session repository, runtime resource ownership, and a clean-wheel consumer proof.

The following are deferred behind the evidence gates in `ARCHITECTURE.md`: entry points; registry/dependency DAG; independent wheels; profiles/bundles; named bindings; richer resource scopes; canonical events; generic hook/event buses; and a public plugin SDK/testkit.

A feature becomes a plugin seam only after real variation or external extension demand exists. Stage promotion requires an accepted ADR and explicit owner authorization. Hot in-process reload is not a target.

## Alternatives considered

### Implement the full plugin platform first

Rejected for v1. It front-loads identities, lifecycle, resolution, configuration, packaging, and compatibility before one useful flow exists.

### Abandon the plugin target entirely

Rejected. Provider/framework isolation and future external extension remain valuable. The staged plan preserves that direction without pretending the machinery is free.

### Adopt a general DI/plugin framework now

Rejected. Explicit constructors are more typed and legible at the current scale. Framework adoption can be reconsidered when measured graph/scoping needs exist and must remain behind AgentKit contracts.

## Consequences

Positive:

- the first release can validate a real consumer path quickly;
- public contracts are informed by usage rather than speculation;
- package/release and security complexity is postponed;
- internal boundaries keep later extraction possible.

Negative:

- adding a provider in v1 may require editing the explicit composition root;
- external plugins are not discovered automatically;
- some later extraction or API migration may be necessary;
- the target plugin architecture is not available on day one.

## Compatibility

v1 exposes no public plugin manifest, capability registry, entry-point group, profile/bundle schema, or plugin SDK compatibility promise. Package versions own compatibility until a later ADR establishes another system.

## Verification

- A built single wheel runs the complete fake-model/tool flow in a clean external environment.
- Forbidden-import tests preserve hexagonal module boundaries.
- The v1 dependency graph contains no plugin framework, Hydra, or general DI container in core.
- Stage proposals cite and satisfy their evidence gate before implementation.

## Supersedes / superseded by

Supersedes the assumption that the full plugin target is the v1 implementation plan. It does not supersede the long-term staged direction in `ARCHITECTURE.md`.
