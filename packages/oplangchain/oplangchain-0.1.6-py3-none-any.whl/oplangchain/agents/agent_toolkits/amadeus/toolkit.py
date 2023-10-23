from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import Field

from oplangchain.agents.agent_toolkits.base import BaseToolkit
from oplangchain.tools import BaseTool
from oplangchain.tools.amadeus.closest_airport import AmadeusClosestAirport
from oplangchain.tools.amadeus.flight_search import AmadeusFlightSearch
from oplangchain.tools.amadeus.utils import authenticate

if TYPE_CHECKING:
    from amadeus import Client


class AmadeusToolkit(BaseToolkit):
    """Toolkit for interacting with Office365."""

    client: Client = Field(default_factory=authenticate)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            AmadeusClosestAirport(),
            AmadeusFlightSearch(),
        ]
