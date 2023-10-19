"""Implement an LLM driven browser."""
from __future__ import annotations

import warnings
import copy
from typing import Any, Dict, List, Optional

from pydantic import Extra
from pydantic import BaseModel, root_validator

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain

from crland.agent.recall.base import FuncRecallChain
from crland.config import Config
from crland.models.base import ModelManager

class CollectChain(Chain):

    func_chain: FuncRecallChain
    input_key: str = "input"
    output_key: str = "result"
    query_key: str = "query"
    """Objective that NatBot is tasked with completing."""
    """[Deprecated] LLM wrapper to use."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @classmethod
    def from_chains(
        cls, llm: BaseLanguageModel, manager: ModelManager, **kwargs: Any
    ) -> CollectChain:
        """Load from LLM."""
        func_chain = FuncRecallChain.from_llm_index(llm=llm, index_manager=manager)
        return cls(func_chain=func_chain, **kwargs)

    @property
    def input_keys(self) -> List[str]:
        """Expect url and browser content.

        :meta private:
        """
        return [self.input_key, self.query_key]

    @property
    def output_keys(self) -> List[str]:
        """Return command.

        :meta private:
        """
        return [self.output_key]

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        require_data = inputs[self.input_key]
        query = inputs[self.query_key]
        query_data = f"""Question: {query}\n```\n"""
        for k, v in require_data.items():
            func_inputs = copy.deepcopy(inputs)
            func_inputs.update({"input": k})
            k_ret = self.func_chain(func_inputs)
            print(k, k_ret)
            func_ret = k_ret['func']
            if isinstance(func_ret, dict):
                func_ret = func_ret['result'] # for function return with chart
            query_data += k + "\n" + func_ret + "\n\n"

        query_data += """```\nTry you best to answer reasonable and helpfully in Chinese, think step by step."""
        return {self.output_key: query_data}

    @property
    def _chain_type(self) -> str:
        return "collect_chain"