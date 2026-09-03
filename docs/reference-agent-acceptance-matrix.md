# Reference-agent acceptance matrix

AK-001 separates two scopes: a small executable MVP-0 fixture and the complete comparative v1 scenario. The broad scenario is specification input for the three adapter spikes, not permission to implement all capabilities in MVP-0.

## MVP-0 executable fixture

| Path | Input | Shared assertion | Automated evidence |
|---|---|---|---|
| normal tool path | `Mein Name ist Artur` | model requests `uppercase_name`; tool result is fed back; final output is `Hallo, ARTUR!` | `tests/test_mvp0.py` and clean-wheel smoke |
| direct response | arbitrary input with `DirectModel` | no tool is executed; model text is returned | `tests/test_mvp0.py` |
| invalid model outcome | neither or both result variants | contract rejects ambiguous output | `tests/test_mvp0.py` |

## Full v1 comparative scenario

All adapters must eventually use the same installable reference-agent package, fixture IDs, inputs, and expected domain outcomes. Adapter-native evidence may differ and must be reported rather than normalized away.

| Capability | Stable fixture / action | Shared assertion | Allowed adapter-specific observation |
|---|---|---|---|
| model | `normal-001` | a deterministic response is produced | native message/event types |
| memory | `memory-001`, recall saved preference | recalled value is scoped to the same identity | store APIs and serialization |
| knowledge | `knowledge-001`, retrieve a cited fact | answer contains the expected source ID | retriever/vector-store API |
| tool | `tool-001`, normalize a name | exactly one named invocation with captured input/output | native tool-call representation |
| guardrail | `reject-001`, forbidden request | model/tool side effect is not emitted | middleware/hook lifecycle |
| telemetry | every scenario | invocation, model, tool, and terminal outcome correlate | trace/span schema |
| persistent conversation | `conversation-001`, second turn | prior accepted turn is available after process restart | session/thread identifiers |
| conditional branch | `branch-001` | fixture takes the declared branch | graph/workflow representation |
| retry | `retry-001`, transient failure then success | bounded retry count and final result match | retry ownership and event shape |
| HITL rejection | `hitl-reject-001` | proposed mutation is never executed | interrupt/approval primitive |
| HITL resume | `hitl-resume-001` | approved operation resumes once | resume command/state format |
| restart | kill at `restart-before-tool` | workflow reaches a truthful resumable state | checkpoint format/location |
| replay | replay completed side effect | no duplicate externally visible mutation | idempotency/reconciliation evidence |
| clean install | built wheel in empty Python 3.12 env | no repository-relative/editable import | build/install logs |

## Evidence schema

Each run records:

- fixture ID, adapter name/version, package version and source commit;
- shared assertion results;
- adapter-native observations for messages, state, checkpoints, interrupts, resume and failures;
- timestamps and terminal outcome;
- side-effect operation ID and durable intent/result references where applicable.

## Required negative cases

- unknown tool;
- permanent model failure after the retry budget;
- guardrail rejection before any side effect;
- human rejection and human approval;
- kill before side effect, during uncertain completion, and after durable result;
- replay when the result already exists.

No MVP-0 result counts as evidence for these deferred capabilities. AK-005 through AK-009 must implement and compare them before ADR-001 can become final.
