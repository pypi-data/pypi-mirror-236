import re
from typing import Union

from langchain.agents.agent import AgentOutputParser
from crland.agent.rank.prompt import FORMAT_INSTRUCTIONS
from langchain.schema import AgentAction, AgentFinish, OutputParserException

class FunctionOutParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        print(text)
        # \s matches against tab/newline/whitespace
        regex = (
            r"Function\s*\d*\s*:[\s]*(.*?)[\s]*Function\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        )
        match = re.search(regex, text, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{text}`")
        action = match.group(1).strip().replace("\\", "")
        action_input = re.sub(r'\([^)]*\)', '', match.group(2)).replace('"', "").strip(" ") # delete parathese and its contents
        #print(action, "\n", action_input)
        return AgentAction(action, action_input, text)