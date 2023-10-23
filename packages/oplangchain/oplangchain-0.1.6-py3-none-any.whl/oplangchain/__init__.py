"""Main entrypoint into package."""

from importlib import metadata
from typing import Optional

from oplangchain.agents import MRKLChain, ReActChain, SelfAskWithSearchChain
from oplangchain.cache import BaseCache
from oplangchain.chains import (
    ConversationChain,
    LLMBashChain,
    LLMChain,
    LLMCheckerChain,
    LLMMathChain,
    QAWithSourcesChain,
    VectorDBQA,
    VectorDBQAWithSourcesChain,
)
from oplangchain.docstore import InMemoryDocstore, Wikipedia
from oplangchain.llms import (
    Anthropic,
    Banana,
    CerebriumAI,
    Cohere,
    ForefrontAI,
    GooseAI,
    HuggingFaceHub,
    HuggingFaceTextGenInference,
    LlamaCpp,
    Modal,
    OpenAI,
    Petals,
    PipelineAI,
    SagemakerEndpoint,
    StochasticAI,
    Writer,
)
from oplangchain.llms.huggingface_pipeline import HuggingFacePipeline
from oplangchain.prompts import (
    FewShotPromptTemplate,
    Prompt,
    PromptTemplate,
)
from oplangchain.schema.prompt_template import BasePromptTemplate
from oplangchain.utilities.arxiv import ArxivAPIWrapper
from oplangchain.utilities.golden_query import GoldenQueryAPIWrapper
from oplangchain.utilities.google_search import GoogleSearchAPIWrapper
from oplangchain.utilities.google_serper import GoogleSerperAPIWrapper
from oplangchain.utilities.powerbi import PowerBIDataset
from oplangchain.utilities.searx_search import SearxSearchWrapper
from oplangchain.utilities.serpapi import SerpAPIWrapper
from oplangchain.utilities.sql_database import SQLDatabase
from oplangchain.utilities.wikipedia import WikipediaAPIWrapper
from oplangchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from oplangchain.vectorstores import FAISS, ElasticVectorSearch

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

verbose: bool = False
debug: bool = False
llm_cache: Optional[BaseCache] = None

# For backwards compatibility
SerpAPIChain = SerpAPIWrapper

__all__ = [
    "LLMChain",
    "LLMBashChain",
    "LLMCheckerChain",
    "LLMMathChain",
    "ArxivAPIWrapper",
    "GoldenQueryAPIWrapper",
    "SelfAskWithSearchChain",
    "SerpAPIWrapper",
    "SerpAPIChain",
    "SearxSearchWrapper",
    "GoogleSearchAPIWrapper",
    "GoogleSerperAPIWrapper",
    "WolframAlphaAPIWrapper",
    "WikipediaAPIWrapper",
    "Anthropic",
    "Banana",
    "CerebriumAI",
    "Cohere",
    "ForefrontAI",
    "GooseAI",
    "Modal",
    "OpenAI",
    "Petals",
    "PipelineAI",
    "StochasticAI",
    "Writer",
    "BasePromptTemplate",
    "Prompt",
    "FewShotPromptTemplate",
    "PromptTemplate",
    "ReActChain",
    "Wikipedia",
    "HuggingFaceHub",
    "SagemakerEndpoint",
    "HuggingFacePipeline",
    "SQLDatabase",
    "PowerBIDataset",
    "FAISS",
    "MRKLChain",
    "VectorDBQA",
    "ElasticVectorSearch",
    "InMemoryDocstore",
    "ConversationChain",
    "VectorDBQAWithSourcesChain",
    "QAWithSourcesChain",
    "LlamaCpp",
    "HuggingFaceTextGenInference",
]
