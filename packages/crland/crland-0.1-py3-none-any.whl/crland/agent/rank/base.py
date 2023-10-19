from typing import Any, List, Optional, Sequence, Tuple, Dict, Union

from pydantic import Field

from langchain.agents.agent import Agent, AgentExecutor, AgentOutputParser

from crland.agent.rank.prompt import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from crland.agent.rank.output_parser import FunctionOutParser

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import AgentAction
from langchain.agents.tools import Tool
from langchain.tools.base import BaseTool
from langchain.agents.utils import validate_tools_single_input
from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
)
from langchain.schema import (
    AgentAction,
    AgentFinish,
)
from langchain.input import get_color_mapping

class FunctionAgent(Agent):
    """Agent for the FunctionAgent chain."""

    output_parser: AgentOutputParser = Field(default_factory=FunctionOutParser)

    @classmethod
    def _get_default_output_parser(cls, **kwargs: Any) -> AgentOutputParser:
        return FunctionOutParser()

    @property
    def _agent_type(self) -> str:
        """Return Identifier of agent type."""
        return "FunctionAgent"

    @property
    def observation_prefix(self) -> str:
        """Prefix to append the observation with."""
        return "Observation: "

    @property
    def llm_prefix(self) -> str:
        """Prefix to append the llm call with."""
        return "Thought:"

    @classmethod
    def create_prompt(
        cls,
        tools: Sequence[BaseTool],
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:
        """Create prompt in the style of the zero shot agent.

        Args:
            tools: List of tools the agent will have access to, used to format the
                prompt.
            prefix: String to put before the list of tools.
            suffix: String to put after the list of tools.
            input_variables: List of input variables the final prompt will expect.

        Returns:
            A PromptTemplate with the template assembled from the pieces here.
        """
        tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = format_instructions.format(tool_names=tool_names) + """: {query}"""
        template = "\n\n".join([prefix, tool_strings, format_instructions, suffix])
        #print(template)
        if input_variables is None:
            input_variables = ["input", "agent_scratchpad", "query"]
        return PromptTemplate(template=template, input_variables=input_variables)

    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseLanguageModel,
        tools: Sequence[BaseTool],
        callback_manager: Optional[BaseCallbackManager] = None,
        output_parser: Optional[AgentOutputParser] = None,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Agent:
        """Construct an agent from an LLM and tools."""
        cls._validate_tools(tools)
        prompt = cls.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            format_instructions=format_instructions,
            input_variables=input_variables,
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
        tool_names = [tool.name for tool in tools]
        _output_parser = output_parser or cls._get_default_output_parser()
        return cls(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            output_parser=_output_parser,
            **kwargs,
        )

    @classmethod
    def _validate_tools(cls, tools: Sequence[BaseTool]) -> None:
        validate_tools_single_input(cls.__name__, tools)
        for tool in tools:
            if tool.description is None:
                raise ValueError(
                    f"Got a tool {tool.name} without a description. For this agent, "
                    f"a description must always be provided."
                )
        super()._validate_tools(tools)

class FunctionChain(AgentExecutor):
    """Chain that implements the MRKL system.
    """
    @classmethod
    def from_chains(
        cls, llm: BaseLanguageModel, tools: List[Tool], **kwargs: Any
    ) -> AgentExecutor:
        """User friendly way to initialize the MRKL chain.

        This is intended to be an easy way to get up and running with the
        MRKL chain.

        Args:
            llm: The LLM to use as the agent LLM.
            tools: The chains the MRKL system has access to.
            **kwargs: parameters to be passed to initialization.

        Returns:
            An initialized MRKL chain.

        """
        agent = FunctionAgent.from_llm_and_tools(llm, tools)
        return cls(agent=agent, tools=tools, **kwargs)
        
    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """Run text through and get agent response."""
        # Construct a mapping of tool name to tool for easy lookup
        name_to_tool_map = {tool.name: tool for tool in self.tools}
        # We construct a mapping from each tool to a color, used for logging.
        color_mapping = get_color_mapping(
            [tool.name for tool in self.tools], excluded_colors=["green"]
        )
        intermediate_steps: List[Tuple[AgentAction, str]] = []
        # We now enter the agent loop (until it returns something).
        next_step_output = self._take_next_step(
            name_to_tool_map,
            color_mapping,
            inputs,
            intermediate_steps,
            run_manager=run_manager,
        )
        if isinstance(next_step_output, AgentFinish):
            return self._return(
                next_step_output, intermediate_steps, run_manager=run_manager
            )
        intermediate_steps.extend(next_step_output)
        if len(next_step_output) == 1:
            next_step_action = next_step_output[0]
            # See if tool should return directly
            # print("next_step_action", next_step_action)
            tool_return = self._get_tool_return(next_step_action)
            #print("tool_return", next_step_action)
            if tool_return is not None:
                return self._return(tool_return, intermediate_steps)
        return {"output": "Sorry! Not found"}

    def _take_next_step(
        self,
        name_to_tool_map: Dict[str, BaseTool],
        color_mapping: Dict[str, str],
        inputs: Dict[str, str],
        intermediate_steps: List[Tuple[AgentAction, str]],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Union[AgentFinish, List[Tuple[AgentAction, str]]]:
        """Take a single step in the thought-action-observation loop.

        Override this to take control of how the agent makes and acts on choices.
        """
        try:
            # Call the LLM to see what to do.
            output = self.agent.plan(
                intermediate_steps,
                callbacks=run_manager.get_child() if run_manager else None,
                **inputs,
            )
        except Exception as e:
            if not self.handle_parsing_errors:
                raise e
            text = str(e).split("`")[1]
            observation = "Invalid or incomplete response"
            output = AgentAction("_Exception", observation, text)
            tool_run_kwargs = self.agent.tool_run_logging_kwargs()
            observation = ExceptionTool().run(
                output.tool,
                verbose=self.verbose,
                color=None,
                callbacks=run_manager.get_child() if run_manager else None,
                **tool_run_kwargs,
            )
            return [(output, observation)]
        # If the tool chosen is the finishing tool, then we end and return.
        if isinstance(output, AgentFinish):
            return output
        actions: List[AgentAction]
        if isinstance(output, AgentAction):
            actions = [output]
        else:
            actions = output
        result = []
        for agent_action in actions:
            # if have input params, use default
            if "params" in inputs and len(inputs["params"]) != 0:
                #print(inputs['params'])
                agent_action.tool_input=inputs['params']
            #if run_manager:
            #    run_manager.on_agent_action(agent_action, color="green")
            # Otherwise we lookup the tool
            #print(agent_action.tool, name_to_tool_map)
            if agent_action.tool in name_to_tool_map:
                tool = name_to_tool_map[agent_action.tool]
                return_direct = tool.return_direct
                color = color_mapping[agent_action.tool]
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()
                if return_direct:
                    tool_run_kwargs["llm_prefix"] = ""
                # We then call the tool on the tool input to get an observation
                # if inputs are multi-variable
                if isinstance(agent_action.tool_input, list):
                    observation = ""
                    for k in agent_action.tool_input:
                        observation += k + ":\n"
                        observation += tool.run(
                            k,
                            verbose=self.verbose,
                            color=color,
                            callbacks=run_manager.get_child() if run_manager else None,
                            **tool_run_kwargs,
                        )
                        observation += "\n"
                else:
                    observation = tool.run(
                        agent_action.tool_input,
                        verbose=self.verbose,
                        color=color,
                        callbacks=run_manager.get_child() if run_manager else None,
                        **tool_run_kwargs,
                    )
            else:
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()
                observation = InvalidTool().run(
                    agent_action.tool,
                    verbose=self.verbose,
                    color=None,
                    callbacks=run_manager.get_child() if run_manager else None,
                    **tool_run_kwargs,
                )
            result.append((agent_action, observation))
        return result