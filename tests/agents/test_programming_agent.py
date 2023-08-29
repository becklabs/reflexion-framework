import os

from reflexion.agents.programming import ProgrammingReflexionAgent
from reflexion.prompts import PROMPTS_DIR
from reflexion.actors import LanguageFunction

from reflexion.environments.programming import InternalTestingEnv
from reflexion.environments.programming import PythonTestingEnv
from reflexion.llms import MockLLM

import logging
logging.basicConfig(level=logging.INFO)


function_signature = "def reverse_words(s: str) -> str"
docstring = "Reverse each word in a string"

buggy_solution = """
def reverse_words(s: str) -> str:
    return s[::-1]
"""

solution = """
def reverse_words(s: str) -> str:
    return ' '.join(word[::-1] for word in s.split())
"""

reflection = "Need to reverse each word independently instead of the whole string."

tests = """
Tests:
assert reverse_words("Hello World") == "olleH dlroW"  # This test will fail.
assert reverse_words("This is a test") == "sihT si a tset"
assert reverse_words("abc") == "cba"
"""

llm = MockLLM(responses =[buggy_solution, tests, reflection, solution])

# PROMPTS
simple_implementation_function = LanguageFunction.from_yaml(
    os.path.join(
        PROMPTS_DIR,
        "programming",
        "v1",
        "implementation",
        "python",
        "simple.yaml",
    ),
    llm=llm,
)

implementation_function = LanguageFunction.from_yaml(
    os.path.join(
        PROMPTS_DIR,
        "programming",
        "v1",
        "implementation",
        "python",
        "reflexion.yaml",
    ),
    llm=llm,
)

reflexion_function = LanguageFunction.from_yaml(
    os.path.join(
        PROMPTS_DIR, "programming", "v1", "reflecting", "python", "reflexion.yaml"
    ),
    llm=llm,
)

local_env = PythonTestingEnv(timeout=10)

agent = ProgrammingReflexionAgent(
    function_signature=function_signature,
    docstring=docstring,
    testing_env=InternalTestingEnv(function_signature, docstring, "python", local_env, llm),
    simple_implemenation_function=simple_implementation_function,
    implementation_function=implementation_function,
    reflection_function=reflexion_function,
)
def test_step():
    reward, message = agent.step()
    assert reward == False

    reward, message = agent.step()
    assert reward == True


