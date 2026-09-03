# agentkit

Embeddable Python system for packaging domain agents independently from their execution framework and hosting environment.

## Architecture and planning

- [Consolidated ADR set](docs/adr/README.md)
- [Agentkit v1 product backlog](docs/architecture/agentkit-v1-product-backlog.md)
- [MVP implementation operating model](governance/MVP-OPERATING-MODEL.md)
- [Legacy architecture baseline](ARCHITECTURE.md)
- [Legacy ADRs](adr/README.md)

The consolidated ADRs and v1 product backlog are the current governing artifacts. `ARCHITECTURE.md`, `ROADMAP.md`, the ADRs under `adr/`, and `governance/kanban-backlog.json` are retained solely as non-binding historical provenance. ADR-001 remains proposed pending the comparative execution-framework spike; ADR-002 through ADR-009 are accepted.

## MVP-0 moving skeleton

The first executable slice demonstrates the package-first dependency direction without pretending to implement a universal agent runtime:

```bash
uv sync --extra dev
uv run agentkit-mvp0
bash scripts/smoke_clean_install.sh
```

Expected output: `Hallo, ARTUR!`

Read [the illustrated MVP-0 principle](docs/mvp0-principle.md) and the [reference-agent acceptance matrix](docs/reference-agent-acceptance-matrix.md).
