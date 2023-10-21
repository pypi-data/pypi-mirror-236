import json
from typing import Any, Dict, List, Optional, Callable, Union
from crland.datacenter.knowledge.factor import Factor
from crland.datacenter.knowledge.executor import Executor, ExecutorManager

class Graph:
    name = "Temporal Financial Graph"
    factors: Dict[str, Factor] = {}
    headers: List[str] = []

    def __init__(
        self, 
        factors, 
        headers
    ):
        self.factors = factors
        self.headers = headers

    @classmethod
    def build_from_file(
        cls, 
        filename="crland/datacenter/knowledge/schema.md"
        #infofile="crland/datacenter/knowledge/schema.json",
    ) -> 'Graph':
        '''
            Use Stack to build graph
        '''
        stack = []
        factors = {}
        headers = []
        level = -1
        #name_to_info = json.load(open(infofile, "r"))
        with open(filename, "r") as infile:
            for l in infile:
                data = l.rstrip("").strip("\n").split("-")
                if len(data) == 1:
                    continue
                new_level = int(len(data[0])/3)
                name = data[1].strip()
                if name not in factors:
                    factors.update(
                        {
                            name: Factor(
                                name, 
                                "",
                                [],
                                [],
                                [],
                                [])
                        }  # a deep hole here for python object memory allocation
                    )
                if 0 == new_level:
                    headers.append(name)      
                if new_level > level:
                    stack.append(name)
                elif new_level == level:
                    stack[-1] = name
                else:
                    stack = stack[:new_level]
                    stack.append(name)
                level = new_level
                if level > 0:
                    factors[name].add_parents(
                        factors[stack[-2]]
                    )
                    factors[stack[-2]].add_childrens(
                        factors[name]
                    )
        return cls(factors, headers)

    def show(
        self
    ):
        for n, f in self.factors.items():
            print("*"*10, f.name, "*"*10)
            for p in f.get_parents():
                print("parents:", p.name)
            for c in f.get_childrens():
                print("children:", c.name)
    
    def get_factor(
        self, 
        name
    ) -> Factor:
        if name in self.factors:
            return self.factors[name]
        raise f"No Element called {name}"

    #  downgrade, will drop in future
    def assemble_func(
        self, 
        name, 
        func
    ):
        self.factors[name].register_func(
            Executor.create_from_func(func, self.factors[name].description)
        )

    #  downgrade, will drop in future
    def assemble(
        self, 
        funcs: Union[List[Dict[str, Callable]], Dict[str, Callable]]
    ):
        if isinstance(funcs, List):
            for term in funcs:
                for name, func in term.items():
                    self.assemble_func(name, func)
        else:
            for name, func in funcs.items():
                self.assemble_func(name, func)

    def assemble(
        self, 
        manager: ExecutorManager
    ):
        for name_signature, exe in ExecutorManager().name_to_executor.items():
            d = name_signature.split("|")
            name = d[0]
            signature = d[1]
            if not exe.graph_node:
                continue
            if signature == "default":
                self.factors[name].description = exe.description
            if name in self.factors:
                self.factors[name].register_func(
                    exe
                )

    def get_available_executors(
        self,
        factor_to_models: Dict[str, str] = {}
    ):
        '''
            Based on user's requirements, return funcs
            :factor_to_models, user require
        '''
        desc_to_func = {}
        for name, factor in self.factors.items():
            if len(factor.executors):
                flag = False
                model = factor_to_models.get(name, "")
                if model:  # if user require hit
                    for exe in factor.executors:
                        if model == exe.name:
                            desc_to_func.update({factor.name : exe})  # recall by name
                            desc_to_func.update({factor.description : exe})  # recall by description                                                     
                            flag = True
                            break
                if not flag:
                    desc_to_func.update({factor.name : factor.executors[0]})
                    desc_to_func.update({factor.description : factor.executors[0]})
        return desc_to_func

    def get_all_exec(
        self
    ):
        '''
            Based on user's requirements, return execs
        '''
        desc_to_func = []
        for name, factor in self.factors.items():
            for exe in factor.executors:
                desc_to_func.append((name, exe))
        return desc_to_func

    def get_factor_exec(
        self,
        factor: str
    ):
        '''
            return factor and children func
        '''
        desc_to_func = []
        factor = self.factors[factor]
        def inner_func(factor, desc_to_func):
            if len(factor.executors):
                for exe in factor.executors:
                    desc_to_func.append((factor.name, exe))
            for chd in factor.get_childrens():
                desc_to_func = inner_func(chd, desc_to_func)
            return desc_to_func
        return inner_func(factor, desc_to_func)


if __name__ == "__main__":
    graph = Graph.build_from_file("crland/datacenter/knowledge/schema.md")
    graph.show()