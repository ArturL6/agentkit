# ADR-008: The Agent Is an Importable Python Package

- **Status:** Accepted
- **Date:** 2026-08-30

## Decision

A domain agent is distributed as a normal Python package.

```bash
pip install research-agent
```

```python
from research_agent import create_agent
```

The domain agent package owns:

- prompts;
- `soul.md`;
- `agent.md`;
- domain skills;
- default plugin composition;
- domain-specific context providers;
- convenience construction API.

It should not own generic checkpoint engines, graph execution, MCP transport, vector-store clients, model gateways, or cloud hosting.

Those belong to the selected framework ecosystem or reusable plugin packages.
