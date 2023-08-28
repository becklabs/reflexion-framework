# reflexion-framework
A simple, modular framework for implementing text-based Reflexion agents. Designed for compatability with diverse problem domains.

```python
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
```

## Setup

Follow these steps to get the Reflexion-Framework up and running:

1. Clone the repository with submodules:
```
git clone --recurse-submodules https://github.com/yourusername/reflexion-framework.git
```

2. Install the package:
```
pip3 install -e .
```

3. If using the Rust programming environment, Install [Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html)

4. If using the StarChat LLM, install the necessary libraries:
```
pip3 install transformers torch
```

5. If evaluating with the `LeetCodeHard` benchmark, build the dataset according to the instructions in the [README](https://github.com/GammaTauAI/leetcode-hard-gym).

## Roadmap/Opportunities for Contribution

- [ ] Wider language support for programming tasks
- [ ] HotpotQA and Alfworld agent and environment implementations

