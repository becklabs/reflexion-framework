from ..evaluators.internal import InternalTestingEnv
from ..actors.function import LanguageFunction
from .base import ReflexionAgent
from typing import List, Tuple

# agent = ReflexionAgent(problem, InternalTestingEnv(problem, language, local_env))

class ProgrammingReflexionAgent(ReflexionAgent):
    """
    Reflexion Agent for implementing functions based on feedback from a generated testing environment 
    """
    def __init__(
        self,
        problem: str,
        testing_env: InternalTestingEnv,
        implementation_function: LanguageFunction,
        reflection_function: LanguageFunction,
    ):
        self.problem = problem
        self.testing_env = testing_env
        super().__init__()

    
    def reflect(self, action: str, feedback: str) -> str:
        ...
    
    def act(self, reflections: List[str]) -> str:
        ...
    
    def evaluate(self, action: str) -> Tuple[bool, str]:
        ...

