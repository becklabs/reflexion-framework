from reflexion.environments.programming import PythonTestingEnv

env = PythonTestingEnv(timeout=10)


program = ''' 
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """
    Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    for idx, elem in enumerate(numbers):
        for idx2, elem2 in enumerate(numbers):
            if idx != idx2:
                distance = elem - elem2
                if distance < threshold:
                    return True

    return False
'''

tests = ["assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True",
    "assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False",
    "assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True",
    "assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False",
    "assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True",
    "assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True",
    "assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False"]

reward, result = env.step(program, tests)

def test_step():
    assert reward == (True, False, True, False, True, True, False)
    assert result == ("passed", "AssertionError, actual left-hand value was: True", "passed", "AssertionError, actual left-hand value was: True", "passed", "passed", "AssertionError, actual left-hand value was: True")