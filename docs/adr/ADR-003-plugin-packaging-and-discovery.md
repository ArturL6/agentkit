# ADR-003: Plugins Are Independently Installable Python Packages

- **Status:** Accepted
- **Date:** 2026-08-30

## Decision

Capabilities may be distributed as independent Python packages:

```text
our-harness-mem0
our-harness-qdrant
our-harness-mcp
our-harness-openrouter
our-harness-otel
```

Optional automatic discovery uses standard Python package entry points.

Example:

```toml
[project.entry-points."our_harness.plugins"]
mem0 = "our_harness_mem0.plugin:plugin"
```

Discovery and activation are separate:

```text
Installed package
      ↓
Entry-point discovery
      ↓
Known plugin
      ↓
Explicit composition
      ↓
Activated capability
```

Installing a plugin must not automatically enable it.

A new provider must not require editing a central `if provider == ...` switch.
