import os
from typing import List, Optional, Tuple

from ..actors import LanguageFunction
from ..environments.programming import InternalTestingEnv
from ..llms import ChatLLM
from ..prompts import PROMPTS_DIR
from .base import ReflexionAgent


class ProgrammingReflexionAgent(ReflexionAgent):
    """
    Reflexion Agent for implementing functions based on feedback from a generated testing environment
    """

    def __init__(
        self,
        function_signature: str,
        docstring: str,
        testing_env: InternalTestingEnv,
        simple_implemenation_function: LanguageFunction,
        implementation_function: LanguageFunction,
        reflection_function: LanguageFunction,
    ):
        self.function_signature = function_signature
        self.docstring = docstring
        self.testing_env = testing_env
        self.simple_impl_function = simple_implemenation_function
        self.impl_function = implementation_function
        self.reflection_function = reflection_function
        super().__init__(window_size=1)

    def reflect(self, action: str, feedback: str) -> str:
        return self.reflection_function(
            docstring=self.docstring, previous_impl=action, unit_test_results=feedback
        )

    def act(
        self,
        reflections: List[str],
        last_action: Optional[str],
        last_feedback: Optional[str],
    ) -> str:
        if not reflections:
            self.implementation = self.simple_impl_function(
                docstring=self.docstring, function_signature=self.function_signature
            )
        else:
            self.implementation = self.impl_function(
                docstring=self.docstring,
                previous_impl=last_action,
                unit_test_results=last_feedback,
                reflection=next(iter(reflections)),
            )
        return self.implementation

    def evaluate(self, action: str) -> Tuple[bool, str]:
        rewards, results = self.testing_env.step(action)
        feedback_str = self.testing_env.format_feedback(rewards, results)
        return all(rewards), feedback_str


class PythonReflexionAgent(ProgrammingReflexionAgent):
    def __init__(
        self,
        function_signature: str,
        docstring: str,
        testing_env: InternalTestingEnv,
        llm: ChatLLM,
    ):
        super().__init__(
            function_signature=function_signature,
            docstring=docstring,
            testing_env=testing_env,
            simple_implemenation_function=LanguageFunction.from_yaml(
                os.path.join(
                    PROMPTS_DIR,
                    "programming",
                    "v1",
                    "implementation",
                    "python",
                    "simple.yaml",
                ),
                llm=llm,
            ),
            implementation_function=LanguageFunction.from_yaml(
                os.path.join(
                    PROMPTS_DIR,
                    "programming",
                    "v1",
                    "implementation",
                    "python",
                    "reflexion.yaml",
                ),
                llm=llm,
            ),
            reflection_function=LanguageFunction.from_yaml(
                os.path.join(
                    PROMPTS_DIR,
                    "programming",
                    "v1",
                    "reflecting",
                    "python",
                    "reflexion.yaml",
                ),
                llm=llm,
            ),
        )

class RustReflexionAgent(ProgrammingReflexionAgent):
    def __init__(
        self,
        function_signature: str,
        docstring: str,
        testing_env: InternalTestingEnv,
        llm: ChatLLM,
    ):
        super().__init__(
            function_signature=function_signature,
            docstring=docstring,
            testing_env=testing_env,
            simple_implemenation_function=LanguageFunction.from_yaml(
                os.path.join(
                    PROMPTS_DIR,
                    "programming",
                    "v1",
                    "implementation",
                    "rust",
                    "simple.yaml",
                ),
                llm=llm,
            ),
            implementation_function=LanguageFunction.from_yaml(
                os.path.join(
                    PROMPTS_DIR,
                    "programming",
                    "v1",
                    "implementation",
                    "rust",
                    "reflexion.yaml",
                ),
                llm=llm,
            ),
            reflection_function=LanguageFunction.from_yaml(
                os.path.join(
                    PROMPTS_DIR,
                    "programming",
                    "v1",
                    "reflecting",
                    "rust",
                    "reflexion.yaml",
                ),
                llm=llm,
            ),
        )
