import logging
import os
from typing import List, Tuple

from ...actors import LanguageFunction
from ...llms import ChatLLM
from ...prompts import PROMPTS_DIR
from .base import TestingEnv
from .local.base import LocalTestingEnv


class InternalTestingEnv(TestingEnv):
    def __init__(
        self,
        problem: str,
        language: str,
        local_env: LocalTestingEnv,
        llm: ChatLLM
    ):
        self.problem = problem
        self.language = language
        self.local_env = local_env
        self.test_generation_function: LanguageFunction = (
            LanguageFunction.from_yaml(
                os.path.join(
                    PROMPTS_DIR, "programming", "initial", "testing", language, "assumptions.yaml"
                ),
                llm=llm
            )
        )
        self.generated_tests: [List[str]] = []

    def step(
        self, program: str, tests: List[str] = [], metadata={}
    ) -> Tuple[List[bool], List[str]]:
        if not self.generated_tests:
            self.generated_tests = self._generate_tests()
        return self.local_env.step(program=program, tests=self.generated_tests, metadata=metadata)
    
    def format_feedback(self, rewards: List[bool], results: List[str]) -> str:
        """
        Format the feedback from the local environment into a human-readable string.
        """
        passed_str = ""
        failed_str = ""
        for reward, result, test in zip(rewards, results, self.generated_tests):
            if reward:
                passed_str += test + '\n'
            else:
                failed_str += test + '\nMessage: ' + result + '\n\n'
        return f"Tests Passed:\n{passed_str}\nTests Failed:\n{failed_str}"

    def _generate_tests(self):
        function_response = self.test_generation_function(function_signature = self.problem)
        if 'Tests:' not in function_response:
            raise ValueError(f"Test generation function {self.test_generation_function} did not produce `Test:` header")
        tests = 'Tests:'.join(function_response.split('Tests:')[1:]).strip('\n').split("\n")
        return [test.strip() for test in tests if test.strip()]



