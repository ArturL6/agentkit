"""Installed-wheel smoke entry point."""

from .agent import create_agent
from .fake_capabilities import DeterministicGreetingModel, UppercaseTool


def run_demo() -> str:
    agent = create_agent(model=DeterministicGreetingModel(), tools=[UppercaseTool()])
    return agent.invoke("Mein Name ist Artur")


def main() -> None:
    print(run_demo())


if __name__ == "__main__":
    main()
