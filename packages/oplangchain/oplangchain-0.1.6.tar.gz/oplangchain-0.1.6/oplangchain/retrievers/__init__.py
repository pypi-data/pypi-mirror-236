"""**Retriever** class returns Documents given a text **query**.

It is more general than a vector store. A retriever does not need to be able to
store documents, only to return (or retrieve) it. Vector stores can be used as
the backbone of a retriever, but there are other types of retrievers as well.

**Class hierarchy:**

.. code-block::

    BaseRetriever --> <name>Retriever  # Examples: ArxivRetriever, MergerRetriever

**Main helpers:**

.. code-block::

    Document, Serializable, Callbacks,
    CallbackManagerForRetrieverRun, AsyncCallbackManagerForRetrieverRun
"""

from oplangchain.retrievers.arxiv import ArxivRetriever
from oplangchain.retrievers.azure_cognitive_search import AzureCognitiveSearchRetriever
from oplangchain.retrievers.bm25 import BM25Retriever
from oplangchain.retrievers.chaindesk import ChaindeskRetriever
from oplangchain.retrievers.chatgpt_plugin_retriever import ChatGPTPluginRetriever
from oplangchain.retrievers.contextual_compression import ContextualCompressionRetriever
from oplangchain.retrievers.docarray import DocArrayRetriever
from oplangchain.retrievers.elastic_search_bm25 import ElasticSearchBM25Retriever
from oplangchain.retrievers.ensemble import EnsembleRetriever
from oplangchain.retrievers.google_cloud_enterprise_search import (
    GoogleCloudEnterpriseSearchRetriever,
)
from oplangchain.retrievers.kendra import AmazonKendraRetriever
from oplangchain.retrievers.knn import KNNRetriever
from oplangchain.retrievers.llama_index import (
    LlamaIndexGraphRetriever,
    LlamaIndexRetriever,
)
from oplangchain.retrievers.merger_retriever import MergerRetriever
from oplangchain.retrievers.metal import MetalRetriever
from oplangchain.retrievers.milvus import MilvusRetriever
from oplangchain.retrievers.multi_query import MultiQueryRetriever
from oplangchain.retrievers.pinecone_hybrid_search import PineconeHybridSearchRetriever
from oplangchain.retrievers.pubmed import PubMedRetriever
from oplangchain.retrievers.re_phraser import RePhraseQueryRetriever
from oplangchain.retrievers.remote_retriever import RemoteLangChainRetriever
from oplangchain.retrievers.self_query.base import SelfQueryRetriever
from oplangchain.retrievers.svm import SVMRetriever
from oplangchain.retrievers.tfidf import TFIDFRetriever
from oplangchain.retrievers.time_weighted_retriever import (
    TimeWeightedVectorStoreRetriever,
)
from oplangchain.retrievers.vespa_retriever import VespaRetriever
from oplangchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from oplangchain.retrievers.web_research import WebResearchRetriever
from oplangchain.retrievers.wikipedia import WikipediaRetriever
from oplangchain.retrievers.zep import ZepRetriever
from oplangchain.retrievers.zilliz import ZillizRetriever

__all__ = [
    "AmazonKendraRetriever",
    "ArxivRetriever",
    "AzureCognitiveSearchRetriever",
    "ChatGPTPluginRetriever",
    "ContextualCompressionRetriever",
    "ChaindeskRetriever",
    "ElasticSearchBM25Retriever",
    "GoogleCloudEnterpriseSearchRetriever",
    "KNNRetriever",
    "LlamaIndexGraphRetriever",
    "LlamaIndexRetriever",
    "MergerRetriever",
    "MetalRetriever",
    "MilvusRetriever",
    "MultiQueryRetriever",
    "PineconeHybridSearchRetriever",
    "PubMedRetriever",
    "RemoteLangChainRetriever",
    "SVMRetriever",
    "SelfQueryRetriever",
    "TFIDFRetriever",
    "BM25Retriever",
    "TimeWeightedVectorStoreRetriever",
    "VespaRetriever",
    "WeaviateHybridSearchRetriever",
    "WikipediaRetriever",
    "ZepRetriever",
    "ZillizRetriever",
    "DocArrayRetriever",
    "RePhraseQueryRetriever",
    "WebResearchRetriever",
    "EnsembleRetriever",
]
