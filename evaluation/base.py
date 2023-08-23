from abc import ABC, abstractmethod
from typing import Any, List, Sequence

class TestingEnv(ABC):
    @abstractmethod
    def step(self, program: str, tests: List[str] = []) -> Sequence:
        """
        Test the program against the tests. Return a list of results.
        """
        ...
