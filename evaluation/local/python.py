import os
from typing import Any, List
from .base import LocalTestingEnv
from typing import Callable, Any
import ast
from queue import Queue
from .util import time_limit, TimeoutException

IMPORTS = [
        "import math",
        "import re",
        "import sys",
        "import copy",
        "import datetime",
        "import itertools",
        "import collections",
        "import heapq",
        "import statistics",
        "import functools",
        "import hashlib",
        "import numpy",
        "import numpy as np",
        "import string",
        "from typing import *",
        "from collections import *",
]


class LocalPythonTestingEnv(LocalTestingEnv):
    """
    Local Testing environment for Python programs.
    """
    def __init__(self, directory: str = os.getcwd(), timeout: int = 10):
        super().__init__(directory, timeout)

    def _unsafe_execute(self, program: str, test: str, result: Queue) -> bool:
        program = "\n".join(IMPORTS) + "\n" + program + "\n" + test
        try:
            exec_globals = {}
            with time_limit(self.timeout):
                exec(program, exec_globals)
            result.put("passed")
        except TimeoutException:
            result.put("Timed out")
        except AssertionError as e:
            # Get the actual value of the function call.
            func_call = get_func_call(test)
            try:
                actual_value = eval(func_call, exec_globals)
            except Exception as e:
                actual_value = f"Error when rerunning function call: {e}"
            result.put(f"AssertionError, actual value was: {actual_value}")

        except Exception as e:
            print(type(e))
            result.put(f"Failed: {e}")


def get_func_call(assert_statement: str) -> str:
    """
    Get the "left" statement from the assert_statement.
    """
    tree = ast.parse(assert_statement)
    
    if not isinstance(tree.body[0], ast.Assert):
        raise ValueError("Input string is not an assert statement.")
    
    test_expr = tree.body[0].test
    
    if isinstance(test_expr, ast.Call):
        call = test_expr
    elif isinstance(test_expr, ast.UnaryOp) and isinstance(test_expr.op, ast.Not):
        call = test_expr.operand
    elif isinstance(test_expr, ast.Compare) and len(test_expr.ops) == 1 and isinstance(test_expr.ops[0], ast.Eq):
        call = test_expr.left
    else:
        raise ValueError("Unsupported assert statement format.")
    
    return ast.unparse(call)    
    