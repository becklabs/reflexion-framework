
from __future__ import annotations

from typing import Dict, List, Sequence
import yaml

from langchain.schema import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage,
    FunctionMessage,
    ChatMessage
)

from termcolor import colored

def load_yaml_file(filepath: str) -> List[Dict]:
    """
    Load a YAML file and return its contents as a dictionary.

    Args:
        filepath (str): The path to the YAML file.

    Returns:
        Dict: The contents of the YAML file as a dictionary.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj

def parse_conversation(raw_messages: List[Dict]) -> List[BaseMessage]:
    """
    Parse a chat thread JSON object into a list of Messages.
    """
    message_roles  = {
        "user": HumanMessage,
        "assistant": AIMessage,
        "system": SystemMessage,
    }

    messages = []
    for message in raw_messages:
        message_type = message_roles[message["role"]]
        messages.append(message_type(content=message["content"]))

    return messages

def get_buffer_string(
    messages: Sequence[BaseMessage], human_prefix: str = "Input", ai_prefix: str = "Output"
) -> str:
    """Convert sequence of Messages to strings and concatenate them into one string.

    Args:
        messages: Messages to be converted to strings.
        human_prefix: The prefix to prepend to contents of HumanMessages.
        ai_prefix: THe prefix to prepend to contents of AIMessages.

    Returns:
        A single string concatenation of all input messages.

    Example:
        .. code-block:: python

            from langchain.schema import AIMessage, HumanMessage

            messages = [
                HumanMessage(content="Hi, how are you?"),
                AIMessage(content="Good, how are you?"),
            ]
            get_buffer_string(messages)
            # -> "Human: Hi, how are you?\nAI: Good, how are you?"
    """
    role_to_color = {
        "System": "red",
        human_prefix: "green",
        ai_prefix: "blue",
        "Function": "magenta",
    }
    formatted_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            role = human_prefix
        elif isinstance(m, AIMessage):
            role = ai_prefix
        elif isinstance(m, SystemMessage):
            role = "System"
        elif isinstance(m, FunctionMessage):
            role = "Function"
        elif isinstance(m, ChatMessage):
            role = m.role
        else:
            raise ValueError(f"Got unsupported message type: {m}")
        prefix_len = len(f'{role}: ')
        message_content = m.content
        message_lines = message_content.split("\n")
        if len(message_lines) > 1: # To align indent
            message_content = "\n".join(
                [message_lines[0]]
                + [" " * prefix_len + line for line in message_lines[1:]]
            )
        message = f"{role}: {message_content}"
        if isinstance(m, AIMessage) and "function_call" in m.additional_kwargs:
            message += f"{m.additional_kwargs['function_call']}"

        formatted_messages.append(colored(message, role_to_color[role]))
    return "\n".join(formatted_messages)

