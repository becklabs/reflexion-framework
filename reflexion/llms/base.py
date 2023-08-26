from abc import ABC, abstractmethod
from typing import List

from langchain.schema import AIMessage, BaseMessage


class ChatLLM(ABC):
    """
    Abstract base class for a message-thread-based LLM 
    """
    @abstractmethod
    def __call__(self, messages: List[BaseMessage]) -> AIMessage:
        ...
