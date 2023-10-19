# flake8: noqa
PREFIX = """Answer the following questions. You have access to the following functions:"""
FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should think which function you should use and only choose one
Function: the function to choose, should be one of [{tool_names}]
Function Input: the input parameters to the function is an entity extracted from """

SUFFIX = """
You should only find one. Begin!

Question: {input}
Thought:{agent_scratchpad}"""