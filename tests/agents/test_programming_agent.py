import os

from reflexion.agents.programming import ProgrammingReflexionAgent
from reflexion.prompts import PROMPTS_DIR
from reflexion.actors import LanguageFunction

from reflexion.evaluators.programming import InternalTestingEnv
from reflexion.evaluators.programming import LocalPythonTestingEnv
from reflexion.llms import OpenAIChatLLM, MockLLM
from langchain.callbacks import get_openai_callback

import logging
logging.basicConfig(level=logging.INFO)

problem = '''
def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
'''

llm = OpenAIChatLLM(model_name="gpt-4", temperature=0, max_tokens=1000)

# PROMPTS
simple_implementation_function = LanguageFunction.from_yaml(
    os.path.join(
        PROMPTS_DIR,
        "programming",
        "improved",
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
        "improved",
        "implementation",
        "python",
        "reflexion.yaml",
    ),
    llm=llm,
)

reflexion_function = LanguageFunction.from_yaml(
    os.path.join(
        PROMPTS_DIR, "programming", "improved", "reflecting", "python", "reflexion.yaml"
    ),
    llm=llm,
)

local_env = LocalPythonTestingEnv(timeout=10)

agent = ProgrammingReflexionAgent(
    problem=problem,
    testing_env=InternalTestingEnv(
        problem=problem, language="python", local_env=local_env, llm=llm
    ),
    simple_implemenation_function=simple_implementation_function,
    implementation_function=implementation_function,
    reflection_function=reflexion_function,
)

with get_openai_callback() as cb:
    reward, message = agent.step()
    print(reward)
    print(message)
print("Total cost", cb.total_cost)

with get_openai_callback() as cb:
    reward, message = agent.step()
    print(reward)
    print(message)
print("Total cost", cb.total_cost)
