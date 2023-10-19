# flake8: noqa
from typing import Any, Dict, List, Optional, Callable
from crland.searchhub.recall.base import IndexManager
from crland.searchhub.recall.parser import FuncParser
from crland.agent.rank.base import FunctionChain
from crland.datacenter.knowledge.executor import ExecutorManager

from langchain.schema import HumanMessage
from langchain.chains.base import Chain
from langchain.agents.tools import Tool
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
)

class FuncRecallChain(Chain):
    llm: BaseLanguageModel
    index_manager: IndexManager
    input_key: str = "input"
    channel_key: str = "channel"
    output_key: str = "func"

    @property
    def input_keys(self) -> List[str]:
        """Will be whatever keys the prompt expects.

        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Will always return text key.

        :meta private:
        """
        return [self.output_key]

    @classmethod
    def from_llm_index(
        cls,
        llm : BaseLanguageModel,
        index_manager : IndexManager, 
        **kwargs: Any,  
    ):
        # pass
        return cls(llm=llm, index_manager=index_manager, **kwargs)

    def _call(self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        
        #docs = self.index_manager.search(
        #    inputs[self.channel_key],
        #    inputs[self.input_key]
        #    )
        docs = list(ExecutorManager().name_to_executor.values())

        tools = []
        tool_names = []
        for exe in docs:
            #exe = id.metadata['ref']
            print("The functions is :", exe.func)
            if exe.func in tool_names:
                continue
            tool_names.append(exe.func)
            tools.append(Tool(
                name = exe.func.__name__,
                func = exe.func,
                return_direct = True,
                description = exe.description
            ))
            # to add args to each function
        AnswerAgent = FunctionChain.from_chains(self.llm, tools)
        #print("AnswerAgent: ", inputs)        
        result = AnswerAgent(inputs)['output']
        print(result)
        prompt = "you are a business analyst, Infer helpfully\n"
        post = "\n Answer:\n"
        if isinstance(result, dict):
            #result['result'] = self.llm(
            #    [HumanMessage(content= prompt + result['result'])]
            #).content
            print(prompt + result['result'] + post)
            result['result'] = self.llm(prompt + result['result'])
        else:
            #result = self.llm(
            #    [HumanMessage(content= prompt + result)]
            #).content
            print(prompt + result + post)
            result = self.llm(prompt + result)
        #print("result", result)
        return {self.output_key: result}