from typing import Any, Dict, List, Optional, Callable
from crland.datacenter.knowledge.executor import Executor

class Factor:
    '''
        class for factor, used in graph
    '''    
    def __init__(
        self,
        name: str,
        description: str,
        recall: List[str] = [],
        parents: List['Factor'] = [],
        childrens: List['Factor'] = [],
        executors: List[Executor] = []
    ):
        self.name = name
        self.description = description
        self.recall = recall
        self.parents = parents
        self.childrens = childrens
        self.executors = executors

    @classmethod
    def create(
        cls,
        name: str,
        description: str
    ) -> 'Factor':
        return cls(name=name, description=description)
    
    def register_func(
        self, 
        func: Executor
    ):
        self.executors.append(func)
    
    def add_parents(
        self, 
        parent: 'Factor'
    ):
        if parent not in self.parents:
            self.parents.append(parent)

    def get_parents(
        self
    ) -> List['Factor']:
        return self.parents

    def add_childrens(
        self, 
        child: 'Factor'
    ):
        if child not in self.childrens:
            self.childrens.append(child)

    def get_childrens(
        self
    ) -> List['Factor']:
        return self.childrens    