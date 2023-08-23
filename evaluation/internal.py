from typing import List, Sequence

from .base import TestingEnv
from .local.base import LocalTestingEnv


class InternalTestingEnv(TestingEnv):
    def __init__(self, problem: str, language: str, local_env: LocalTestingEnv):
        self.problem = problem
        self.language = language
        self.local_env = local_env

    def step(self, program: str, tests: List[str] = []) -> Sequence:
        return self.local_env.step(program, tests)
