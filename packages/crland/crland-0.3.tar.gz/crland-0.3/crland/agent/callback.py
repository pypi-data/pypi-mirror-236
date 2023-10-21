from typing import Dict, Any

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import (
    AgentAction,
    AgentFinish,
)
import asyncio

from crland.service.error import StatusCodeEnum
from crland.service.base import wrapper_return

class WebsocketCallbackHandler(BaseCallbackHandler):
    def __init__(self, socket, loop):
        self.socket = socket
        self.loop = loop

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        print("************* output *************\n", outputs)
        self.loop.create_task(
            self.socket.send(
            wrapper_return(outputs["text"], StatusCodeEnum.OK)
        ))

    """
    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        self.loop.create_task(
            self.socket.send(
            wrapper_return(outputs["text"], StatusCodeEnum.OK)
        ))
    """