from abc import ABC, abstractmethod
from typing import List

from langchain.schema import AIMessage, BaseMessage


class ChatLLM(ABC):
    @abstractmethod
    def __call__(self, messages: List[BaseMessage]) -> AIMessage:
        ...
