from typing import Dict
from crland.config import Config
from crland.models.base import ModelManager
from crland.searchhub.recall.base import IndexManager
from crland.datacenter.database.data_read.macro import *
from crland.agent.recall.base import FuncRecallChain
from crland.searchhub.task.base import Task

class SearchTask(Task):
    name = "search"
    def __init__(
        self
    ):
        self.config = Config()
        self.model_manager = ModelManager(config=self.config)
        self.llm = self.model_manager.get_model("guanaco")
        index_manager = IndexManager()
        self.chain = FuncRecallChain.from_llm_index(
            self.llm, 
            index_manager
        )

    def execute(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        result =  self.chain({
            "input": text, 
            "channel": self.config.get('index')["channel"], 
            "query": text,
            "params": kwargs.get('company', "深圳万象城")
            })['func']
        if isinstance(result, dict):
            return result
        else:
            return {
                "result": result
            }

if __name__ == '__main__':
    task = SearchTask()
    result = task.execute("查询深圳万象城的运营情况")
    print(result)