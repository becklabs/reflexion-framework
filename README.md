# reflexion-framework
A simple, modular, non-brittle framework for implementing text-based Reflexion agents. Designed for compatability with diverse problem domains and interopability with existing workflows.

Below is an example of a Reflexion agent that implements functions based on feedback from a code execution environment, which generates its own tests. 

```python
from reflexion.agents.programming import PythonReflexionAgent
from reflexion.datasets.programming import HumanEvalDataset
from reflexion.environments.programming import (InternalTestingEnv,
                                                PythonTestingEnv)
from reflexion.llms import OpenAIChatLLM

# Load a task from a dataset 
LANG = "python"
dataset = HumanEvalDataset(language=LANG)
task_id, signature, docstring, tests = dataset[0]

# Instantiate an LLM
llm = OpenAIChatLLM(model_name="gpt-4", temperature=0)

# Instantiate a code execution environment
local_env = PythonTestingEnv(timeout=10)

# Instantiate a Reflexion agent with an internal testing environment 
agent = PythonReflexionAgent(
        function_signature=signature,
        docstring=docstring,
        testing_env=InternalTestingEnv(function_signature=signature,
                        docstring=docstring,
                        language=LANG,
                        local_env=local_env,
                        llm=llm),
        llm=llm
)

# Run the agent for a few steps
for _ in range(3):
    reward, message = agent.step()

# Evaluate the agent's implementation against the ground truth tests
rewards, messages = local_env.step(program=agent.implementation, tests=tests)
```

## Setup

Follow these steps to get reflexion-framework up and running:

1. Clone the repository with submodules:
```bash
git clone --recurse-submodules https://github.com/becklabs/reflexion-framework.git && cd reflexion-framework
```

2. Install the package:
```bash
pip3 install -e .
```


## Optional Setup
1. If using the Rust programming environment, Install [Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html)

2. If using OpenAI LLMs, set the `OPENAI_API_KEY` environment variable to your API key:
```bash
export OPENAI_API_KEY=yourkey
```

3. If using `transformers` LLMs, install the necessary libraries:
```bash
pip3 install transformers torch
```

4. If evaluating with the `LeetCodeHard` benchmark, build the dataset according to the instructions in the [README](https://github.com/GammaTauAI/leetcode-hard-gym).


## Opportunities for Contribution

- [ ] Wider language support for programming tasks
- [ ] HotpotQA and Alfworld agent and environment implementations

