__version__ = "0.1.0"

# Expose main submodules for easy import
from . import agents, attacks, config, runner
#
from .attacks.prompt_injection import PromptInjectionAttack
