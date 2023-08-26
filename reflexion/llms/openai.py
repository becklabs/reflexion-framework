from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage

from .base import ChatLLM

import logging

class OpenAIChatLLM(ChatLLM):
    def __init__(self, *model_args, **model_kwargs):
        self.chat_model = ChatOpenAI(*model_args, **model_kwargs)

    def __call__(self, messages: List[BaseMessage]) -> AIMessage:
        return self.chat_model(messages)

class OpenAICompletionLLM(ChatLLM):
    START_TOKEN = "<|im_start|>"
    END_TOKEN = "<|im_end|>"
    MESSAGE_TO_TOKEN = {
        HumanMessage: "user",
        AIMessage: "assistant",
        SystemMessage: "system",
    }
    def __init__(self, *args, **kwargs):
        self.completion_model = OpenAI(*args, **kwargs)

    def __call__(self, messages: List[BaseMessage]) -> AIMessage:
        prompt = ""
        for message in messages:
            prompt += self.START_TOKEN + self.MESSAGE_TO_TOKEN[type(message)] + "\n" + message.content + self.END_TOKEN + "\n"
        prompt += self.START_TOKEN + self.MESSAGE_TO_TOKEN[AIMessage] + "\n"
        logging.info(prompt)

        return AIMessage(content=self.completion_model(prompt, stop=self.END_TOKEN))
