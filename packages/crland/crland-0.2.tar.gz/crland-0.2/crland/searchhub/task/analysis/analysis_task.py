from typing import Dict
from crland.config import Config
from crland.datacenter.knowledge.graph import Graph
from crland.datacenter.knowledge.executor import ExecutorManager
from crland.searchhub.recall.base import IndexManager
from crland.datacenter.knowledge.executor import ExecutorManager
from crland.searchhub.recall.channel.faiss import FAISS2
from crland.models.base import ModelManager
from crland.tools.embeddings.embedding_manager import EmbeddingManager
from crland.agent.recall.base import FuncRecallChain
from crland.agent.collect.base import CollectChain
from crland.agent.base import JustModel
#from crland.agent.analysis.base import AnalysisChain
from crland.searchhub.task.base import Task

class AnalysisTask(Task):
    name = "analysis"
    def __init__(
        self
    ):
        self.config = Config()
        self.model_manager = ModelManager(config=self.config)
        self.llm = self.model_manager.get_model("chatgpt")
        #self.analysis_chain = AnalysisChain.from_llm(self.llm)
        self.analysis_chain = None
        self.graph = Graph.build_from_file(
            "crland/datacenter/knowledge/schema.md"
        )
        self.graph.assemble(ExecutorManager())
        db = FAISS2.from_texts(
            inputs = self.graph.get_available_executors(), 
            embedding = EmbeddingManager.get_embedding(self.config)
        )
        index_manager = IndexManager()
        index_manager.register(self.config.get('index'), db)
        #db.save_local("./crland/datacenter/local_data")
        #db = FAISS2.load_local("./crland/datacenter/local_data", embedding)
        self.collect_chain = CollectChain.from_chains(
            self.llm, 
            index_manager
        )

    def execute(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        #require_data = self.analysis_chain(
        #    text
        #)["text"]
        require_data = ExecutorManager().name_to_executor
        collect_data = self.collect_chain({
            "input": require_data,
            "channel": self.config.get('index')["channel"],
            "query": text,
            "params": kwargs.get('company', "")
        })["result"]
        print(collect_data)
        JustModel(self.llm)(collect_data)['result']
        return {
            "intermediate": collect_data,
            "result": result
        }

if __name__ == '__main__':
    task = AnalysisTask()
    result = task.execute("", company = "xx")
    print(result)
    #graph = Graph.build_from_file("crland/datacenter/knowledge/schema.md")
    #graph.assemble(analysis_func)
    #print(graph.get_available_func()) 

