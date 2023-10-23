"""**Vector store** stores embedded data and performs vector search.

One of the most common ways to store and search over unstructured data is to
embed it and store the resulting embedding vectors, and then query the store
and retrieve the data that are 'most similar' to the embedded query.

**Class hierarchy:**

.. code-block::

    VectorStore --> <name>  # Examples: Annoy, FAISS, Milvus

    BaseRetriever --> VectorStoreRetriever --> <name>Retriever  # Example: VespaRetriever

**Main helpers:**

.. code-block::

    Embeddings, Document
"""  # noqa: E501
from oplangchain.vectorstores.alibabacloud_opensearch import (
    AlibabaCloudOpenSearch,
    AlibabaCloudOpenSearchSettings,
)
from oplangchain.vectorstores.analyticdb import AnalyticDB
from oplangchain.vectorstores.annoy import Annoy
from oplangchain.vectorstores.atlas import AtlasDB
from oplangchain.vectorstores.awadb import AwaDB
from oplangchain.vectorstores.azuresearch import AzureSearch
from oplangchain.vectorstores.base import VectorStore
from oplangchain.vectorstores.cassandra import Cassandra
from oplangchain.vectorstores.chroma import Chroma
from oplangchain.vectorstores.clarifai import Clarifai
from oplangchain.vectorstores.clickhouse import Clickhouse, ClickhouseSettings
from oplangchain.vectorstores.deeplake import DeepLake
from oplangchain.vectorstores.docarray import DocArrayHnswSearch, DocArrayInMemorySearch
from oplangchain.vectorstores.elastic_vector_search import (
    ElasticKnnSearch,
    ElasticVectorSearch,
)
from oplangchain.vectorstores.faiss import FAISS
from oplangchain.vectorstores.hologres import Hologres
from oplangchain.vectorstores.lancedb import LanceDB
from oplangchain.vectorstores.marqo import Marqo
from oplangchain.vectorstores.matching_engine import MatchingEngine
from oplangchain.vectorstores.meilisearch import Meilisearch
from oplangchain.vectorstores.milvus import Milvus
from oplangchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from oplangchain.vectorstores.myscale import MyScale, MyScaleSettings
from oplangchain.vectorstores.opensearch_vector_search import OpenSearchVectorSearch
from oplangchain.vectorstores.pgembedding import PGEmbedding
from oplangchain.vectorstores.pgvector import PGVector
from oplangchain.vectorstores.pinecone import Pinecone
from oplangchain.vectorstores.qdrant import Qdrant
from oplangchain.vectorstores.redis import Redis
from oplangchain.vectorstores.rocksetdb import Rockset
from oplangchain.vectorstores.scann import ScaNN
from oplangchain.vectorstores.singlestoredb import SingleStoreDB
from oplangchain.vectorstores.sklearn import SKLearnVectorStore
from oplangchain.vectorstores.starrocks import StarRocks
from oplangchain.vectorstores.supabase import SupabaseVectorStore
from oplangchain.vectorstores.tair import Tair
from oplangchain.vectorstores.tigris import Tigris
from oplangchain.vectorstores.typesense import Typesense
from oplangchain.vectorstores.vectara import Vectara
from oplangchain.vectorstores.weaviate import Weaviate
from oplangchain.vectorstores.zilliz import Zilliz

__all__ = [
    "AlibabaCloudOpenSearch",
    "AlibabaCloudOpenSearchSettings",
    "AnalyticDB",
    "Annoy",
    "AtlasDB",
    "AwaDB",
    "AzureSearch",
    "Cassandra",
    "Chroma",
    "Clickhouse",
    "ClickhouseSettings",
    "DeepLake",
    "DocArrayHnswSearch",
    "DocArrayInMemorySearch",
    "ElasticVectorSearch",
    "ElasticKnnSearch",
    "FAISS",
    "PGEmbedding",
    "Hologres",
    "LanceDB",
    "MatchingEngine",
    "Marqo",
    "Meilisearch",
    "Milvus",
    "Zilliz",
    "SingleStoreDB",
    "Chroma",
    "Clarifai",
    "OpenSearchVectorSearch",
    "AtlasDB",
    "DeepLake",
    "Annoy",
    "MongoDBAtlasVectorSearch",
    "MyScale",
    "MyScaleSettings",
    "OpenSearchVectorSearch",
    "Pinecone",
    "Qdrant",
    "Redis",
    "Rockset",
    "ScaNN",
    "SKLearnVectorStore",
    "SingleStoreDB",
    "StarRocks",
    "SupabaseVectorStore",
    "Tair",
    "Tigris",
    "Typesense",
    "Vectara",
    "VectorStore",
    "Weaviate",
    "Zilliz",
    "PGVector",
]
