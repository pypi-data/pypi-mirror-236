"""**Tools** are classes that an Agent uses to interact with the world.

Each tool has a **description**. Agent uses the description to choose the right
tool for the job.

**Class hierarchy:**

.. code-block::

    ToolMetaclass --> BaseTool --> <name>Tool  # Examples: AIPluginTool, BaseGraphQLTool
                                   <name>      # Examples: BraveSearch, HumanInputRun

**Main helpers:**

.. code-block::

    CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
"""

from oplangchain.tools.arxiv.tool import ArxivQueryRun
from oplangchain.tools.azure_cognitive_services import (
    AzureCogsFormRecognizerTool,
    AzureCogsImageAnalysisTool,
    AzureCogsSpeech2TextTool,
    AzureCogsText2SpeechTool,
)
from oplangchain.tools.base import BaseTool, StructuredTool, Tool, tool
from oplangchain.tools.bing_search.tool import BingSearchResults, BingSearchRun
from oplangchain.tools.brave_search.tool import BraveSearch
from oplangchain.tools.convert_to_openai import format_tool_to_openai_function
from oplangchain.tools.ddg_search.tool import (
    DuckDuckGoSearchResults,
    DuckDuckGoSearchRun,
)
from oplangchain.tools.file_management import (
    CopyFileTool,
    DeleteFileTool,
    FileSearchTool,
    ListDirectoryTool,
    MoveFileTool,
    ReadFileTool,
    WriteFileTool,
)
from oplangchain.tools.gmail import (
    GmailCreateDraft,
    GmailGetMessage,
    GmailGetThread,
    GmailSearch,
    GmailSendMessage,
)
from oplangchain.tools.google_places.tool import GooglePlacesTool
from oplangchain.tools.google_search.tool import GoogleSearchResults, GoogleSearchRun
from oplangchain.tools.google_serper.tool import GoogleSerperResults, GoogleSerperRun
from oplangchain.tools.graphql.tool import BaseGraphQLTool
from oplangchain.tools.human.tool import HumanInputRun
from oplangchain.tools.ifttt import IFTTTWebhook
from oplangchain.tools.interaction.tool import StdInInquireTool
from oplangchain.tools.jira.tool import JiraAction
from oplangchain.tools.json.tool import JsonGetValueTool, JsonListKeysTool
from oplangchain.tools.metaphor_search import MetaphorSearchResults
from oplangchain.tools.office365.create_draft_message import O365CreateDraftMessage
from oplangchain.tools.office365.events_search import O365SearchEvents
from oplangchain.tools.office365.messages_search import O365SearchEmails
from oplangchain.tools.office365.send_event import O365SendEvent
from oplangchain.tools.office365.send_message import O365SendMessage
from oplangchain.tools.office365.utils import authenticate
from oplangchain.tools.openapi.utils.api_models import APIOperation
from oplangchain.tools.openapi.utils.openapi_utils import OpenAPISpec
from oplangchain.tools.openweathermap.tool import OpenWeatherMapQueryRun
from oplangchain.tools.playwright import (
    ClickTool,
    CurrentWebPageTool,
    ExtractHyperlinksTool,
    ExtractTextTool,
    GetElementsTool,
    NavigateBackTool,
    NavigateTool,
)
from oplangchain.tools.plugin import AIPluginTool
from oplangchain.tools.powerbi.tool import (
    InfoPowerBITool,
    ListPowerBITool,
    QueryPowerBITool,
)
from oplangchain.tools.pubmed.tool import PubmedQueryRun
from oplangchain.tools.python.tool import PythonAstREPLTool, PythonREPLTool
from oplangchain.tools.requests.tool import (
    BaseRequestsTool,
    RequestsDeleteTool,
    RequestsGetTool,
    RequestsPatchTool,
    RequestsPostTool,
    RequestsPutTool,
)
from oplangchain.tools.scenexplain.tool import SceneXplainTool
from oplangchain.tools.searx_search.tool import SearxSearchResults, SearxSearchRun
from oplangchain.tools.shell.tool import ShellTool
from oplangchain.tools.sleep.tool import SleepTool
from oplangchain.tools.spark_sql.tool import (
    BaseSparkSQLTool,
    InfoSparkSQLTool,
    ListSparkSQLTool,
    QueryCheckerTool,
    QuerySparkSQLTool,
)
from oplangchain.tools.sql_database.tool import (
    BaseSQLDatabaseTool,
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from oplangchain.tools.steamship_image_generation import SteamshipImageGenerationTool
from oplangchain.tools.vectorstore.tool import (
    VectorStoreQATool,
    VectorStoreQAWithSourcesTool,
)
from oplangchain.tools.wikipedia.tool import WikipediaQueryRun
from oplangchain.tools.wolfram_alpha.tool import WolframAlphaQueryRun
from oplangchain.tools.youtube.search import YouTubeSearchTool
from oplangchain.tools.zapier.tool import ZapierNLAListActions, ZapierNLARunAction

__all__ = [
    "AIPluginTool",
    "APIOperation",
    "ArxivQueryRun",
    "AzureCogsFormRecognizerTool",
    "AzureCogsImageAnalysisTool",
    "AzureCogsSpeech2TextTool",
    "AzureCogsText2SpeechTool",
    "BaseGraphQLTool",
    "BaseRequestsTool",
    "BaseSQLDatabaseTool",
    "BaseSparkSQLTool",
    "BaseTool",
    "BingSearchResults",
    "BingSearchRun",
    "BraveSearch",
    "ClickTool",
    "CopyFileTool",
    "CurrentWebPageTool",
    "DeleteFileTool",
    "DuckDuckGoSearchResults",
    "DuckDuckGoSearchRun",
    "ExtractHyperlinksTool",
    "ExtractTextTool",
    "FileSearchTool",
    "GetElementsTool",
    "GmailCreateDraft",
    "GmailGetMessage",
    "GmailGetThread",
    "GmailSearch",
    "GmailSendMessage",
    "GooglePlacesTool",
    "GoogleSearchResults",
    "GoogleSearchRun",
    "GoogleSerperResults",
    "GoogleSerperRun",
    "HumanInputRun",
    "IFTTTWebhook",
    "InfoPowerBITool",
    "InfoSQLDatabaseTool",
    "InfoSparkSQLTool",
    "JiraAction",
    "JsonGetValueTool",
    "JsonListKeysTool",
    "ListDirectoryTool",
    "ListPowerBITool",
    "ListSQLDatabaseTool",
    "ListSparkSQLTool",
    "MetaphorSearchResults",
    "MoveFileTool",
    "NavigateBackTool",
    "NavigateTool",
    "O365SearchEmails",
    "O365SearchEvents",
    "O365CreateDraftMessage",
    "O365SendMessage",
    "O365SendEvent",
    "authenticate",
    "OpenAPISpec",
    "OpenWeatherMapQueryRun",
    "PubmedQueryRun",
    "PythonAstREPLTool",
    "PythonREPLTool",
    "QueryCheckerTool",
    "QueryPowerBITool",
    "QuerySQLCheckerTool",
    "QuerySQLDataBaseTool",
    "QuerySparkSQLTool",
    "ReadFileTool",
    "RequestsDeleteTool",
    "RequestsGetTool",
    "RequestsPatchTool",
    "RequestsPostTool",
    "RequestsPutTool",
    "SceneXplainTool",
    "SearxSearchResults",
    "SearxSearchRun",
    "ShellTool",
    "SleepTool",
    "StdInInquireTool",
    "SteamshipImageGenerationTool",
    "StructuredTool",
    "Tool",
    "VectorStoreQATool",
    "VectorStoreQAWithSourcesTool",
    "WikipediaQueryRun",
    "WolframAlphaQueryRun",
    "WriteFileTool",
    "YouTubeSearchTool",
    "ZapierNLAListActions",
    "ZapierNLARunAction",
    "format_tool_to_openai_function",
    "tool",
]
