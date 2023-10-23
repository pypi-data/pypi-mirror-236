"""MultiOn agent."""
from __future__ import annotations

from typing import List

from oplangchain.agents.agent_toolkits.base import BaseToolkit
from oplangchain.tools import BaseTool
from oplangchain.tools.multion.create_session import MultionCreateSession
from oplangchain.tools.multion.update_session import MultionUpdateSession


class MultionToolkit(BaseToolkit):
    """Toolkit for interacting with the Browser Agent"""

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [MultionCreateSession(), MultionUpdateSession()]
