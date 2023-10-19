from typing import Any, Dict, List, Optional, Callable
from crland.tools.singleton import singleton

class Executor:
    '''
        class for factor functions, support user defined
    '''
    def __init__(
        self,
        name: str,
        signature: str,
        description: str,        
        func: Callable,
        graph_node: bool = True,
        stats: Dict = {}
    ):
        self.name = name
        self.signature = signature
        self.func = func
        self.description = description
        self.graph_node = graph_node
        self.stats = stats

    @classmethod
    def create(
        cls,
        name,
        signature,
        description,
        func,
        graph_node,
    ) -> 'Executor':
        return cls(
            name=name, 
            signature=signature, 
            description=description, 
            func=func,
            graph_node=graph_node
            )
    
    @classmethod
    def create_from_func(
        cls,
        func,
        description,
    ) -> 'Executor':
        return cls(
            name=func.__name__, 
            signature="default", 
            description = description, 
            func=func
            )

@singleton
class ExecutorManager:
    name_to_executor = {}
    
    def register(
        self, 
        name,
        signature,
        exe
    ):
        self.name_to_executor[name + "|" + signature] = exe

    def register(
        self, 
        name,
        func,
        description,
        signature,
        graph_node        
    ):
        key = name + "|" + signature
        if key in self.name_to_executor:
            raise f"Key already occurs: {key}"

        self.name_to_executor[name + "|" + signature] = Executor.create(
            name,
            signature,
            description,
            func,
            graph_node
        )
    
    def get(
        self, 
        name, 
        signature="default"
    ):
        return self.name_to_executor.get(name + "|" + signature, None)

    def build_recall(
        self
    ):
        recall_to_exe = {}
        for name, exe in self.name_to_executor.items():
            if exe.name:
                recall_to_exe[exe.name] = exe
            if exe.description:
                recall_to_exe[exe.description] = exe
        return recall_to_exe