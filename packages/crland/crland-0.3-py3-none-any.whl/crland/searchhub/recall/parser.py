from typing import Callable, Union, List

EMPTY_DATA = "NO DATA"

def get_chinese(inputs):
    chineses = inputs[1].split("chinese:")[1].strip().split("|")
    return chineses[0].strip()

def get_english(inputs):
    englishs = inputs[2].split("english:")[1].strip().split("|")
    return englishs[0].strip()

def recall_chinese(inputs):
    chineses = inputs[1].split("chinese:")[1].strip().split("|")
    return chineses

def recall_english(inputs):
    englishs = inputs[2].split("english:")[1].strip().split("|")
    return englishs

def parse_arg(inputs):
    out = "" 
    input_arg = inputs[3].split("\n")
    if len(input_arg) > 2:
        for i in input_arg[1:-1]:
            out += i.split(":")[-1].strip()
    else:
        out = "None"
    return out

class FuncParser:
    '''##[must] chinese: 中文解释|常见查询1|...
    ##[must] english: english explain|CommonQuery1|...
    ##[must] args:
        arg1: def1
        arg2: def2
    ##'''
    @classmethod
    def chinese(
        cls, 
        input: Union[Callable, str]
    ) -> str:
        #return input.__doc__.split("\t")[0]
        if isinstance(input, Callable):
            input = input.__doc__
        inputs = input.split("##")
        if len(inputs) == 5:
            return get_chinese(inputs)

    @classmethod
    def chinese_recall(
        cls, 
        input: Union[Callable, str]
    ) -> List[str]:
        if isinstance(input, Callable):
            input = input.__doc__
        inputs = input.split("##")
        if len(inputs) == 5:
            return recall_chinese(inputs)

    @classmethod
    def english(cls, input: Union[Callable, str]) -> str:
        if isinstance(input, Callable):
            input = input.__doc__
        inputs = input.split("##")
        if len(inputs) == 5:
            return get_english(inputs)

    @classmethod
    def english_recall(
        cls, 
        input: Union[Callable, str]
    ) -> List[str]:
        if isinstance(input, Callable):
            input = input.__doc__
        inputs = input.split("##")
        if len(inputs) == 5:
            return recall_english(inputs)

    @classmethod
    def arg(
        cls, 
        input: Union[Callable, str]
    ) -> str:
        if isinstance(input, Callable):
            input = input.__doc__
        inputs = input.split("##")
        if len(inputs) == 5:
            return parse_arg(inputs)

    @classmethod
    def parse(
        cls, 
        input: Union[Callable, str]
    ) -> dict:
        '''
        return {'chinese': str, 'english': str, 'args': str}
        '''
        ret = {}
        if isinstance(input, Callable):
            input = input.__doc__
        inputs = input.split("##")
        if len(inputs) == 5:
            ret["chinese"] = get_chinese(inputs)
            ret["english"] = get_english(inputs)
            ret["args"] = parse_arg(inputs)