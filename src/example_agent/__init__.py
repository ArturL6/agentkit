"""An installable domain-agent package used by the MVP-0 proof."""

from .agent import GreetingAgent, create_agent
from .fake_capabilities import DeterministicGreetingModel, UppercaseTool

__all__ = [
    "DeterministicGreetingModel",
    "GreetingAgent",
    "UppercaseTool",
    "create_agent",
]
