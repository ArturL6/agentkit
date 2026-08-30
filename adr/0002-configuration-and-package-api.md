# ADR-0002: Typed configuration and package-first API

## Status

Superseded by the consolidated v1 ADR set and product backlog. See `README.md` in this directory for the decision-by-decision replacement map.

## Context

AgentKit must embed cleanly in unrelated Python applications. A CLI-first or Hydra-owned API would introduce global initialization, working-directory/config-tree assumptions, and framework objects that do not belong in a library contract. Named binding maps, layered bundles, interpolation, and arbitrary import targets would commit a configuration language before repeated profiles exist.

Editable monorepo execution also fails to prove that package metadata, resources, dependencies, and public imports work for consumers.

## Decision

Python 3.12+ and programmatic package use are the primary contract.

- A typed, validated, immutable `RuntimeSpec` is the single input to runtime composition.
- `async with create_agent(spec) as agent` is the intended resource-owning package pattern.
- v1 fields represent known roles explicitly rather than a general named-binding map.
- Composition is explicit at one outer composition root.
- Core configuration has no dependency on Hydra/OmegaConf and no ambient global settings object.
- An optional flat file loader may only convert one complete document into `RuntimeSpec`, reject unknown keys, and use documented precedence.
- Public configuration does not accept `_target_` or arbitrary Python import paths.
- Secrets are references or injected values and are redacted from diagnostics.
- Hydra may later exist only as an optional adapter that produces `RuntimeSpec`; no Hydra object crosses the boundary.
- v1 ships as one `agentkit` distribution. Heavy integrations may be extras; independent wheels are evidence-gated.

A clean-wheel test is a release requirement: build the artifact, install it in a fresh external environment without editable/source-tree access, invoke the public path, and load packaged resources using package APIs.

## Alternatives considered

### Hydra/OmegaConf as core composition

Rejected for core. Its strongest features concern layered application/experiment configuration, while an embeddable library needs ordinary programmatic construction and no global composition state.

### Pydantic Settings as the public contract

Not selected as an architectural requirement. A validation library may be used internally at a boundary, but public semantics remain AgentKit-owned and components do not instantiate independent settings from the environment.

### Dataclasses plus custom layered YAML

Rejected for v1. Layering, interpolation, merge rules, and secrets precedence would recreate a configuration framework.

### Multiple distributions from the start

Rejected. One wheel avoids a release train while import tests preserve architecture.

## Consequences

Positive:

- consumers can configure AgentKit with ordinary Python;
- loaders and validation libraries remain replaceable;
- errors occur before resource acquisition;
- clean-wheel proof detects packaging failures hidden by editable installs.

Negative:

- v1 offers less declarative composition convenience;
- hosts that rely on Hydra must write or wait for an adapter;
- explicit fields may need evolution when real arbitrary roles appear.

## Compatibility

`RuntimeSpec` and documented public imports are compatibility-sensitive. Any semantic change requires tests, migration notes, and an ADR when structural. File loaders, if added, terminate at the same spec and do not define a second runtime API.

## Verification

- Construct `RuntimeSpec` with no CLI, file, environment read, or global setup.
- Reject unknown or inconsistent values before opening resources.
- Verify secret redaction in errors and representations.
- Build and install the wheel into a new external environment.
- Execute the fake model/tool flow and packaged-resource lookup without repository-relative paths.
- Assert core has no Hydra/OmegaConf import.

## Supersedes / superseded by

Supersedes Hydra-first composition and multi-wheel-first packaging for v1.
