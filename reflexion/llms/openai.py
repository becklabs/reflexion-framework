from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import AIMessage, BaseMessage, HumanMessage

from .base import ChatLLM


class OpenAIChatLLM(ChatLLM):
    def __init__(self, *args, **kwargs):
        self.chat_model = ChatOpenAI(*args, **kwargs)

    def __call__(self, messages: [List[BaseMessage]]) -> AIMessage:
        return self.chat_model(messages)


class OpenAICompletionLLM(ChatLLM):
    def __init__(self, *args, **kwargs):
        self.completion_model = OpenAI(*args, **kwargs)

    def __call__(self, messages: List[BaseMessage]) -> AIMessage:
        prompt = ""
        for message in messages:
            if isinstance(message, AIMessage):
                prompt += f"ASSISTANT:\n{message.content}\n"
            elif isinstance(message, HumanMessage):
                prompt += f"USER:\n{message.content}\n"
            else:
                prompt += f"SYSTEM:\n{message.content}\n"

        return AIMessage(content=self.completion_model(prompt))
