__version__ = "0.1.0"

# Expose main submodules for easy import
from . import agents, attacks, config, runner
from .agents.mcp_agent import MCPAgent
from .agents.llm_agent import LLMAgent
from .attacks.prompt_injection import PromptInjectionAttack
