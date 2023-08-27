from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from collections import deque


class ReflexionAgent(ABC):
    """
    Text-based Reflexion Agent
    """

    def __init__(
        self,
        window_size: int = 1,
    ) -> None:
        """
        Initialize a Reflexion Agent with a given window size for reflections
        """
        self.steps = 0
        self.window_size = window_size
        self.__actions = []
        self.__feedbacks = []
        self.__reflections = deque(maxlen=window_size)

    @abstractmethod
    def reflect(self, action: str, feedback: str) -> str:
        """
        Return a reflection on the previous step
        """
        ...

    @abstractmethod
    def act(
        self,
        reflections: List[str],
        last_action: Optional[str] = None,
        last_feedback: Optional[str] = None,
    ) -> str:
        """
        Return an action based on a list of reflections, and optionally the previous action and feedback
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
            self.__reflections.append(
                self.reflect(
                    action=self.__actions[-1], feedback=self.__feedbacks[-1]
                )
            )

        action = self.act(
            reflections=list(self.__reflections),
            last_action=self.__actions[-1] if self.steps > 0 else None,
            last_feedback=self.__feedbacks[-1] if self.steps > 0 else None,
        )

        reward, message = self.evaluate(action)

        self.__actions.append(action)
        self.__feedbacks.append(message)
        self.steps += 1

        return reward, message
