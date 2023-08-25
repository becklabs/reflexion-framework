from typing import List

from langchain.schema import (AIMessage, BaseMessage, HumanMessage,
                              SystemMessage)

from .base import ChatLLM

MESSAGE_TO_TOKEN = {
    HumanMessage: "<|user|>",
    AIMessage: "<|assistant|>",
    SystemMessage: "<|system|>",
}


class StarChat(ChatLLM):
    def __init__(self, max_tokens: int = 1024, temperature: float = 0.2):
        import torch
        from transformers import pipeline

        self.name = "star-chat"
        self.pipe = pipeline(
            "text-generation",
            model="HuggingFaceH4/starchat-beta",
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.max_tokens = max_tokens
        self.temperature = temperature

    def __call__(self, messages: List[BaseMessage]) -> AIMessage:
        # NOTE: HF does not like temp of 0.0.
        if temperature < 1e-4:
            temperature = 1e-4

        prompt = ""
        for i, message in enumerate(messages):
            prompt += f"{MESSAGE_TO_TOKEN[type(message)]}\n{message.content}\n<|end|>\n"
        prompt += "<|assistant|>\n"

        outputs = self.pipe(
            prompt,
            max_new_tokens=self.max_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=0.95,
            eos_token_id=49155,
            num_return_sequences=1,
        )

        outs = [output["generated_text"] for output in outputs]  # type: ignore
        assert isinstance(outs, list)
        for i, out in enumerate(outs):
            assert isinstance(out, str)
            out = out.split("<|assistant|>")[1]
            if out.endswith("<|end|>"):
                out = out[: -len("<|end|>")]

            outs[i] = out

        return AIMessage(content=outs[0])
