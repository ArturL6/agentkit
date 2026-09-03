"""Deterministic capabilities make the full path testable without API keys."""

from collections.abc import Mapping

from agentkit import AgentDefinition, ModelReply, ToolCall


class UppercaseTool:
    @property
    def name(self) -> str:
        return "uppercase_name"

    def invoke(self, arguments: Mapping[str, str]) -> str:
        try:
            value = arguments["name"]
        except KeyError as exc:
            raise ValueError("uppercase_name requires a name") from exc
        return value.upper()


class DeterministicGreetingModel:
    def respond(
        self,
        *,
        definition: AgentDefinition,
        user_input: str,
        tool_result: str | None,
    ) -> ModelReply:
        del definition
        if tool_result is None:
            name = user_input.removeprefix("Mein Name ist ").strip().rstrip(".")
            return ModelReply(tool_call=ToolCall("uppercase_name", {"name": name}))
        return ModelReply(text=f"Hallo, {tool_result}!")
