"""**Chains** are easily reusable components linked together.

Chains encode a sequence of calls to components like models, document retrievers,
other Chains, etc., and provide a simple interface to this sequence.

The Chain interface makes it easy to create apps that are:

    - **Stateful:** add Memory to any Chain to give it state,
    - **Observable:** pass Callbacks to a Chain to execute additional functionality,
      like logging, outside the main sequence of component calls,
    - **Composable:** combine Chains with other components, including other Chains.

**Class hierarchy:**

.. code-block::

    Chain --> <name>Chain  # Examples: LLMChain, MapReduceChain, RouterChain
"""

from oplangchain.chains.api.base import APIChain
from oplangchain.chains.api.openapi.chain import OpenAPIEndpointChain
from oplangchain.chains.combine_documents.base import AnalyzeDocumentChain
from oplangchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from oplangchain.chains.combine_documents.map_rerank import MapRerankDocumentsChain
from oplangchain.chains.combine_documents.reduce import ReduceDocumentsChain
from oplangchain.chains.combine_documents.refine import RefineDocumentsChain
from oplangchain.chains.combine_documents.stuff import StuffDocumentsChain
from oplangchain.chains.constitutional_ai.base import ConstitutionalChain
from oplangchain.chains.conversation.base import ConversationChain
from oplangchain.chains.conversational_retrieval.base import (
    ChatVectorDBChain,
    ConversationalRetrievalChain,
)
from oplangchain.chains.example_generator import generate_example
from oplangchain.chains.flare.base import FlareChain
from oplangchain.chains.graph_qa.arangodb import ArangoGraphQAChain
from oplangchain.chains.graph_qa.base import GraphQAChain
from oplangchain.chains.graph_qa.cypher import GraphCypherQAChain
from oplangchain.chains.graph_qa.hugegraph import HugeGraphQAChain
from oplangchain.chains.graph_qa.kuzu import KuzuQAChain
from oplangchain.chains.graph_qa.nebulagraph import NebulaGraphQAChain
from oplangchain.chains.graph_qa.neptune_cypher import NeptuneOpenCypherQAChain
from oplangchain.chains.graph_qa.sparql import GraphSparqlQAChain
from oplangchain.chains.hyde.base import HypotheticalDocumentEmbedder
from oplangchain.chains.llm import LLMChain
from oplangchain.chains.llm_bash.base import LLMBashChain
from oplangchain.chains.llm_checker.base import LLMCheckerChain
from oplangchain.chains.llm_math.base import LLMMathChain
from oplangchain.chains.llm_requests import LLMRequestsChain
from oplangchain.chains.llm_summarization_checker.base import (
    LLMSummarizationCheckerChain,
)
from oplangchain.chains.loading import load_chain
from oplangchain.chains.mapreduce import MapReduceChain
from oplangchain.chains.moderation import OpenAIModerationChain
from oplangchain.chains.natbot.base import NatBotChain
from oplangchain.chains.openai_functions import (
    create_citation_fuzzy_match_chain,
    create_extraction_chain,
    create_extraction_chain_pydantic,
    create_qa_with_sources_chain,
    create_qa_with_structure_chain,
    create_tagging_chain,
    create_tagging_chain_pydantic,
)
from oplangchain.chains.qa_generation.base import QAGenerationChain
from oplangchain.chains.qa_with_sources.base import QAWithSourcesChain
from oplangchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from oplangchain.chains.qa_with_sources.vector_db import VectorDBQAWithSourcesChain
from oplangchain.chains.retrieval_qa.base import RetrievalQA, VectorDBQA
from oplangchain.chains.router import (
    LLMRouterChain,
    MultiPromptChain,
    MultiRetrievalQAChain,
    MultiRouteChain,
    RouterChain,
)
from oplangchain.chains.sequential import SequentialChain, SimpleSequentialChain
from oplangchain.chains.sql_database.query import create_sql_query_chain
from oplangchain.chains.transform import TransformChain

__all__ = [
    "APIChain",
    "AnalyzeDocumentChain",
    "ArangoGraphQAChain",
    "ChatVectorDBChain",
    "ConstitutionalChain",
    "ConversationChain",
    "ConversationalRetrievalChain",
    "FlareChain",
    "GraphCypherQAChain",
    "GraphQAChain",
    "GraphSparqlQAChain",
    "HugeGraphQAChain",
    "HypotheticalDocumentEmbedder",
    "KuzuQAChain",
    "LLMBashChain",
    "LLMChain",
    "LLMCheckerChain",
    "LLMMathChain",
    "LLMRequestsChain",
    "LLMRouterChain",
    "LLMSummarizationCheckerChain",
    "MapReduceChain",
    "MapReduceDocumentsChain",
    "MapRerankDocumentsChain",
    "MultiPromptChain",
    "MultiRetrievalQAChain",
    "MultiRouteChain",
    "NatBotChain",
    "NebulaGraphQAChain",
    "NeptuneOpenCypherQAChain",
    "OpenAIModerationChain",
    "OpenAPIEndpointChain",
    "QAGenerationChain",
    "QAWithSourcesChain",
    "ReduceDocumentsChain",
    "RefineDocumentsChain",
    "RetrievalQA",
    "RetrievalQAWithSourcesChain",
    "RouterChain",
    "SequentialChain",
    "SimpleSequentialChain",
    "StuffDocumentsChain",
    "TransformChain",
    "VectorDBQA",
    "VectorDBQAWithSourcesChain",
    "create_citation_fuzzy_match_chain",
    "create_extraction_chain",
    "create_extraction_chain_pydantic",
    "create_qa_with_sources_chain",
    "create_qa_with_structure_chain",
    "create_tagging_chain",
    "create_tagging_chain_pydantic",
    "generate_example",
    "load_chain",
    "create_sql_query_chain",
]
