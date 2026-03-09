"""Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

# custom utils
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface.chat_models import ChatHuggingFace
from transformers import AutoModelForCausalLM, AutoTokenizer,pipeline
import torch


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    return init_chat_model(
        model,
        model_provider=provider,
        max_tokens=2048,

    )

def load_local_chat_model(model_name: str) -> BaseChatModel:
    """Load a local chat model from a model name.

    Args:
        model_name (str): The name of the local model.
    """
    model_name = 'mistralai/Mistral-7B-Instruct-v0.3'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name,
                                                 device_map="auto",
                                                 dtype=torch.float16,
                                                 trust_remote_code=True
                                                )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=1024,
        do_sample=False,
    )   
    llm = HuggingFacePipeline(pipeline=pipe)
    return ChatHuggingFace(llm=llm)
