"""Concrete domain behavior for the example greeting agent.

The loop is deliberately local to this example. It is not an Agentkit runtime
and makes no claims about framework checkpoint, retry, or resume semantics.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from importlib.resources import files
from types import MappingProxyType

from agentkit import AgentDefinition, Model, Tool


@dataclass(frozen=True)
class GreetingAgent:
    definition: AgentDefinition
    model: Model
    tools: MappingProxyType[str, Tool]

    def invoke(self, user_input: str) -> str:
        """Run the example's bounded model -> tool -> model path."""
        first = self.model.respond(
            definition=self.definition,
            user_input=user_input,
            tool_result=None,
        )
        if first.text is not None:
            return first.text

        call = first.tool_call
        if call is None:  # defensive: ModelReply already enforces this invariant
            raise RuntimeError("model returned no outcome")
        tool = self.tools.get(call.name)
        if tool is None:
            raise LookupError(f"unknown tool: {call.name}")
        tool_result = tool.invoke(call.arguments)

        second = self.model.respond(
            definition=self.definition,
            user_input=user_input,
            tool_result=tool_result,
        )
        if second.text is None:
            raise RuntimeError("example agent permits only one tool call")
        return second.text


def _resource_text(name: str) -> str:
    return files("example_agent.resources").joinpath(name).read_text(encoding="utf-8").strip()


def create_agent(*, model: Model, tools: Iterable[Tool]) -> GreetingAgent:
    """Construct the domain agent with replaceable model and tool capabilities."""
    by_name = {tool.name: tool for tool in tools}
    if len(by_name) == 0:
        raise ValueError("at least one tool is required")
    instructions = f"{_resource_text('identity.md')}\n\n{_resource_text('agent.md')}"
    return GreetingAgent(
        definition=AgentDefinition(name="friendly-greeter", instructions=instructions),
        model=model,
        tools=MappingProxyType(by_name),
    )
