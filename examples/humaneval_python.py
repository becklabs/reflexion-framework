from reflexion.datasets import HumanEvalDataset
language = "python"
dataset = HumanEvalDataset(language=language)
id, signature, docstring, tests = dataset[0]

from reflexion.llms import StarChat
llm = StarChat(temperature=0.1)

from reflexion.environments import InternalTestingEnv, LocalPythonTestingEnv
local_env = LocalPythonTestingEnv(timeout=10)
internal_env = InternalTestingEnv(signature, docstring, language, local_env, llm)

from reflexion.agents.programming import PythonReflexionAgent 
agent = PythonReflexionAgent(
    signature, docstring, internal_env, llm
)

for _ in range(3):
    reward, message = agent.step()

rewards, messages = local_env.step(agent.implementation, tests)


