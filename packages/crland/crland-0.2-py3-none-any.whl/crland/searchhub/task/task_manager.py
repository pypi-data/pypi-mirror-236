from pydantic import BaseModel
from typing import  Callable, Any, Dict, List, Union, Tuple
from crland.searchhub.task import candidate_tasks
from crland.searchhub.task.base import Task

class TaskManager():
    tasks: Dict[str, Task] = {}
    def __init__(
        self,
        config
    ):
        self.config = config
        tasks = self.config.get('task')
        for task in candidate_tasks:
            if task.name in tasks:
                self.tasks[task.name] = task()
    
    def get_tasks(
        self
    ) -> List[str]:
        '''
            default is for non task chat
        '''
        return list(self.tasks.keys()) + ["default"]

    def get_task_by_name(
        self,
        name: str
    ) -> Task:
        return self.tasks.get(name, None)

    def extract_task(
        self,
        query: str
    ) -> Dict[str, str]:
        """
        Extract task name and fix query for input
        """
        for t in self.tasks.keys():
            if query.startswith("@" + t):
                return {
                    "task": t,
                    "query": query[len(t)+1:]
                }
        return {"query": query}