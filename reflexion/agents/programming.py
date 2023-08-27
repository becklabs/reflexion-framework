from ..evaluators.programming import InternalTestingEnv
from ..actors import LanguageFunction
from .base import ReflexionAgent
from typing import List, Tuple, Optional


class ProgrammingReflexionAgent(ReflexionAgent):
    """
    Reflexion Agent for implementing functions based on feedback from a generated testing environment
    """

    def __init__(
        self,
        problem: str,
        testing_env: InternalTestingEnv,
        simple_implemenation_function: LanguageFunction,
        implementation_function: LanguageFunction,
        reflection_function: LanguageFunction,
    ):
        self.problem = problem
        self.testing_env = testing_env
        self.simple_impl_function = simple_implemenation_function
        self.impl_function = implementation_function
        self.reflection_function = reflection_function
        super().__init__(window_size=1)

    def reflect(self, action: str, feedback: str) -> str:
        return self.reflection_function(previous_impl=action, unit_test_results=feedback)

    def act(
        self,
        reflections: List[str],
        last_action: Optional[str],
        last_feedback: Optional[str],
    ) -> str:
        if not reflections:
            return self.simple_impl_function(function_signature=self.problem)
        else:
            return self.impl_function(
                previous_impl=last_action,
                unit_test_results=last_feedback,
                reflection=next(iter(reflections)),
            )

    def evaluate(self, action: str) -> Tuple[bool, str]:
        rewards, results = self.testing_env.step(action)
        feedback_str = self.testing_env.format_feedback(rewards, results)
        return all(rewards), feedback_str
