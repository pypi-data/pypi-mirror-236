from typing import Union
from langchain.schema import HumanMessage
from langchain.chat_models.base import BaseChatModel
from langchain.llms.base import BaseLLM
# a quick func to test

class JustModel:
    def __init__(self, llm):
        self.llm = llm
    def __call__(self, text):
        if isinstance(self.llm, BaseChatModel):
            return {"result": self.llm([HumanMessage(content=text)]).content}
        elif isinstance(llm, BaseLLM):
            return {"result": self.llm(text)}