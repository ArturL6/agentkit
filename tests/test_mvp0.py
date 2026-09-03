from collections.abc import Mapping

import pytest

from agentkit import AgentDefinition, ModelReply, ToolCall
from example_agent import DeterministicGreetingModel, UppercaseTool, create_agent


def test_complete_model_tool_model_path() -> None:
    agent = create_agent(model=DeterministicGreetingModel(), tools=[UppercaseTool()])

    assert agent.invoke("Mein Name ist Artur") == "Hallo, ARTUR!"
    assert agent.definition.name == "friendly-greeter"
    assert "transparent" in agent.definition.instructions


def test_model_reply_has_exactly_one_outcome() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        ModelReply()
    with pytest.raises(ValueError, match="exactly one"):
        ModelReply(text="done", tool_call=ToolCall("x", {}))


class DirectModel:
    def respond(
        self,
        *,
        definition: AgentDefinition,
        user_input: str,
        tool_result: str | None,
    ) -> ModelReply:
        del definition, user_input, tool_result
        return ModelReply(text="direkt")


class NeverCalledTool:
    @property
    def name(self) -> str:
        return "unused"

    def invoke(self, arguments: Mapping[str, str]) -> str:
        raise AssertionError(f"must not be called: {arguments}")


def test_direct_reply_needs_no_tool_execution() -> None:
    agent = create_agent(model=DirectModel(), tools=[NeverCalledTool()])
    assert agent.invoke("egal") == "direkt"
