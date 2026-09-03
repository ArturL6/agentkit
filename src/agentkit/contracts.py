"""Narrow data and capability boundaries for the MVP-0 demonstration.

These contracts describe product inputs. They do not define checkpoints,
interrupts, sessions, graphs, retries, or a universal execution runtime.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AgentDefinition:
    """Framework-neutral identity and instructions owned by an agent package."""

    name: str
    instructions: str


@dataclass(frozen=True)
class ToolCall:
    """A model's request to invoke one named capability."""

    name: str
    arguments: Mapping[str, str]


@dataclass(frozen=True)
class ModelReply:
    """Exactly one model outcome: a final answer or a tool request."""

    text: str | None = None
    tool_call: ToolCall | None = None

    def __post_init__(self) -> None:
        if (self.text is None) == (self.tool_call is None):
            raise ValueError("ModelReply requires exactly one of text or tool_call")


class Model(Protocol):
    """Model capability consumed by the concrete example agent."""

    def respond(
        self,
        *,
        definition: AgentDefinition,
        user_input: str,
        tool_result: str | None,
    ) -> ModelReply: ...


class Tool(Protocol):
    """Named capability consumed by the concrete example agent."""

    @property
    def name(self) -> str: ...

    def invoke(self, arguments: Mapping[str, str]) -> str: ...
