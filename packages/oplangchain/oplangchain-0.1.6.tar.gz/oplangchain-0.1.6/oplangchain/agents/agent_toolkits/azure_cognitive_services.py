from __future__ import annotations

import sys
from typing import List

from oplangchain.agents.agent_toolkits.base import BaseToolkit
from oplangchain.tools.azure_cognitive_services import (
    AzureCogsFormRecognizerTool,
    AzureCogsImageAnalysisTool,
    AzureCogsSpeech2TextTool,
    AzureCogsText2SpeechTool,
)
from oplangchain.tools.base import BaseTool


class AzureCognitiveServicesToolkit(BaseToolkit):
    """Toolkit for Azure Cognitive Services."""

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""

        tools = [
            AzureCogsFormRecognizerTool(),
            AzureCogsSpeech2TextTool(),
            AzureCogsText2SpeechTool(),
        ]

        # TODO: Remove check once azure-ai-vision supports MacOS.
        if sys.platform.startswith("linux") or sys.platform.startswith("win"):
            tools.append(AzureCogsImageAnalysisTool())
        return tools
