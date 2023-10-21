from typing import  Callable, Any, Dict, List, Union, Tuple
from pydantic import BaseModel
from crland.searchhub.recall.parser import FuncParser

class IndexManager():
    def __init__(
        self, 
        config=None
    ):
        self.index_name_to_index = {}

    def register(
        self, 
        channel: dict, 
        index : Any
    ) -> None:
        try:
            index_name = channel['channel']
            if index_name not in self.index_name_to_index.keys():
                self.index_name_to_index.update({index_name: index})
        except:
            raise "No Channel config Found"

    def get(
        self, 
        index_name: str
    ):
        if index_name in self.index_name_to_index.keys():
            return self.index_name_to_index[index_name]
    
    def search(
        self, 
        index_name: str, 
        query: str
    ):
         if index_name in self.index_name_to_index.keys():
            return self.index_name_to_index[index_name].similarity_search(query)

    def build_func_recall(
        self,
        name_to_func: List[Any],
        lang: str = "en"
    ):
        '''
            Based on func description build query to func recall pair
        '''
        if lang != "en":
            parse_func = FuncParser.chinese_recall
        else:
            parse_func = FuncParser.english_recall
        desc_to_func = {}
        def inner_func(src):
            rets = {}
            for (k, v) in src.items():
                defs = parse_func(v)
                for d in defs:
                    rets[d] = v
            return rets
        for item in name_to_func:
            desc_to_func.update(inner_func(item))
        return desc_to_func
