from abc import ABC, abstractmethod
from typing import List, Tuple

class ReflexionAgent(ABC):
    """
    Text-based Reflexion Agent 
    """
    def __init__(
        self,
        window_size: int = 1,
    ) -> None:
        self.steps = 0
        self.window_size = window_size
        self.__actions = []
        self.__feedbacks = []
        self.__reflections = []

    @abstractmethod
    def reflect(self, action: str, feedback: str) -> str:
        """
        Return a reflection on the previous step
        """
        ...
    
    @abstractmethod
    def act(self, reflections: List[str]) -> str:
        """
        Return an action based on a list of reflections
        """
        ...
    
    @abstractmethod
    def evaluate(self, action: str) -> Tuple[bool, str]:
        """
        Return environment feedback on an action
        """
        ...

    def step(self):
        """
        Executes a step in the agent's decision-making process.

        This method performs the following steps:
        1. Generates a reflection on the previous step (if it exists).
        2. Generates a new action based on the agent's reflections.
        3. Evaluates the action and receives feedback from the environment.
        4. Stores the action and feedback for future reflections.
        5. Increments the trial count.

        Returns:
            reward (bool): The reward received from the environment for the action.
            message (str): The message received from the environment for the action.
        """
        if self.steps > 0:
            self.__reflections.append(self.reflect(self.__actions[-1], self.__feedbacks[-1]))

        action = self.act(self.__reflections[max(0, self.steps - self.window_size) : self.steps]) 

        reward, message = self.evaluate(action)

        self.__actions.append(action)
        self.__feedbacks.append(message)
        self.steps += 1

        return reward, message
