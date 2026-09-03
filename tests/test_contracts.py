from agentkit import AgentDefinition, ModelReply, ToolCall


def test_contracts_are_immutable_and_comparable() -> None:
    definition = AgentDefinition(name="demo", instructions="be useful")
    call = ToolCall(name="lookup", arguments={"query": "x"})

    assert definition == AgentDefinition(name="demo", instructions="be useful")
    assert ModelReply(tool_call=call).tool_call == call
