from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

class TestingEnv(ABC):
    @abstractmethod
    def step(self, program: str, tests: List[str] = [], metadata: Dict = {}) -> Tuple[List[bool], List[str]]:
        """
        Test the program against the tests. Return a tuple of (rewards, messages). 
        """
        ...
