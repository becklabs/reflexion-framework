import multiprocessing
import os
from abc import abstractmethod
from typing import List, Sequence

from ..base import TestingEnv
from queue import Queue


class LocalTestingEnv(TestingEnv):
    """
    Abstract class for testing environments that run locally.  
    """

    def __init__(self, directory: str = os.getcwd(), timeout: int = 10):
        self.directory = directory
        self.timeout = timeout
        super().__init__()

    def step(self, program: str, tests: List[str] = []) -> Sequence:
        """
        Check if the program compiles and passes the tests. Return a list of results.
        """
        results = [self._check_program(program, test) for test in tests]
        reward = all([result["passed"] for result in results])
        return reward, results

    @abstractmethod
    def _unsafe_execute(self, program: str, test: str, result: Queue) -> bool:
        ...
    
    def _check_program(self, program: str, test: str) -> bool:
        result = multiprocessing.Queue()
        self._unsafe_execute(program, test, result)

        # p = multiprocessing.Process(target=self._unsafe_execute, args=(program, test, result))
        # p.start()
        # p.join(timeout=self.timeout + 1)
        # if p.is_alive():
        #     p.kill()
        # if not result:
        #     result.put("Test timed out")
        
        res = result.get()
        
        return dict(
                passed = res == "passed",
                result = res
        )

