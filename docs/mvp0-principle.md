# MVP-0: das Agentkit-Prinzip

MVP-0 ist absichtlich klein. Er beantwortet nur die Frage: **Wie bleibt ein Domain-Agent installierbar, während Modell und Tools austauschbar sind?**

```text
example_agent (Domain-Paket)
  ├─ identity.md + agent.md       besitzt Identität und Anweisungen
  ├─ create_agent(...)            kleine Konstruktor-API
  └─ GreetingAgent.invoke(...)    konkretes Demo-Verhalten
             │
             ├── Model (injiziert) ──► bittet um Tool-Aufruf / liefert Antwort
             └── Tool  (injiziert) ──► führt eine benannte Fähigkeit aus

agentkit
  └─ schmale Produktdaten         AgentDefinition, ToolCall, ModelReply
```

## Ablauf der Demo

1. Der Aufrufer importiert `create_agent` aus dem installierten Domain-Paket.
2. Er injiziert das deterministische Fake-Modell und das `uppercase_name`-Tool.
3. Das Modell sieht `Mein Name ist Artur` und fordert das Tool an.
4. Das Tool liefert `ARTUR`.
5. Das Modell erzeugt daraus `Hallo, ARTUR!`.

Der wichtige Punkt ist nicht das Großschreiben. Der wichtige Punkt ist die **Richtung der Abhängigkeiten**:

- Das Agent-Paket besitzt die fachliche Identität und das Beispielverhalten.
- Das Agent-Paket erstellt weder ein echtes LLM noch einen externen Tool-Client selbst.
- Konkrete Fähigkeiten werden von außen injiziert und können ersetzt werden.
- Agentkit definiert keine universelle Runtime für Checkpoints, HITL, Retry oder Resume.
- Spätere LangGraph-, ADK- und MAF-Adapter übersetzen dieselben schmalen Produktdaten in ihre jeweils nativen APIs; ihre unterschiedlichen Laufzeitsemantiken bleiben sichtbar.

## Selbst ausprobieren

```bash
uv sync --extra dev
uv run agentkit-mvp0
```

Erwartete Ausgabe:

```text
Hallo, ARTUR!
```

Der reale Installationsbeweis baut zuerst ein Wheel und installiert es in eine neue Python-3.12-Umgebung:

```bash
bash scripts/smoke_clean_install.sh
```

## Bewusst noch nicht enthalten

MVP-0 implementiert keine echte Provider-Anbindung, keine drei Framework-Adapter, keine Persistenz, keine Langzeit-Memory, kein RAG, keine Telemetrie und kein HITL. Diese Fähigkeiten gehören in spätere Tickets und werden nicht vorgetäuscht.
