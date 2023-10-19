from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, Union
from crland.datacenter.knowledge.factor import Factor

EMPTY_DATA = "No Data"
EMPTY_NUM = -1000000

def factor(
    func: Callable,
    factor: Factor,
    return_direct: bool = False,
    ) -> Callable:
    """Make tools out of functions, can be used with or without arguments.

    Args:
        *args: The arguments to the tool.
        return_direct: Whether to return directly from the tool rather
            than continuing the agent loop.

    Requires:
        - Function must be of type (str) -> str
        - Function must have a docstring

    Examples:
        .. code-block:: python
            @factor(factor= your Factor, return_direct=True)
            def search_api(query: str) -> str:
                # Searches the API for the query.
                return
    """
    def _make_tool(func: Callable) -> BaseTool:
        assert func.__doc__ is not None, "Function must have a docstring"
        tool = Tool(
            name=func.__name__,
            func=func,
            description=f"tool",
            return_direct=return_direct,
        )
        factor.register(tool)
        return tool
    return _make_tool(func)