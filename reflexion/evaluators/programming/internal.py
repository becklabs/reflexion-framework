from typing import List, Tuple

from .base import TestingEnv
from .local.base import LocalTestingEnv


class InternalTestingEnv(TestingEnv):
    def __init__(self, problem: str, language: str, local_env: LocalTestingEnv):
        self.problem = problem
        self.language = language
        self.local_env = local_env
        self.generated_tests: [List[str]] = []

    def step(
        self, program: str, tests: List[str] = [], metadata={}
    ) -> Tuple[List[bool], List[str]]:
        return self.local_env.step(program, self.generated_tests, metadata)
