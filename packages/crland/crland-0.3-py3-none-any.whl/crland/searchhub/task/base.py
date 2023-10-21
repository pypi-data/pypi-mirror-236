from typing import Dict
from abc import ABC, abstractmethod

class Task(ABC):
    name = "task"

    @abstractmethod
    def execute(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        pass