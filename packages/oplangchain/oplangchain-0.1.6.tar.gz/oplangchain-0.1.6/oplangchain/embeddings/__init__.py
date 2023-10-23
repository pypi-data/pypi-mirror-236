"""**Embedding models**  are wrappers around embedding models
from different APIs and services.

**Embedding models** can be LLMs or not.

**Class hierarchy:**

.. code-block::

    Embeddings --> <name>Embeddings  # Examples: OpenAIEmbeddings, HuggingFaceEmbeddings
"""


import logging
from typing import Any

from oplangchain.embeddings.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from oplangchain.embeddings.awa import AwaEmbeddings
from oplangchain.embeddings.bedrock import BedrockEmbeddings
from oplangchain.embeddings.clarifai import ClarifaiEmbeddings
from oplangchain.embeddings.cohere import CohereEmbeddings
from oplangchain.embeddings.dashscope import DashScopeEmbeddings
from oplangchain.embeddings.deepinfra import DeepInfraEmbeddings
from oplangchain.embeddings.edenai import EdenAiEmbeddings
from oplangchain.embeddings.elasticsearch import ElasticsearchEmbeddings
from oplangchain.embeddings.embaas import EmbaasEmbeddings
from oplangchain.embeddings.fake import DeterministicFakeEmbedding, FakeEmbeddings
from oplangchain.embeddings.google_palm import GooglePalmEmbeddings
from oplangchain.embeddings.gpt4all import GPT4AllEmbeddings
from oplangchain.embeddings.huggingface import (
    HuggingFaceEmbeddings,
    HuggingFaceInstructEmbeddings,
)
from oplangchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from oplangchain.embeddings.jina import JinaEmbeddings
from oplangchain.embeddings.llamacpp import LlamaCppEmbeddings
from oplangchain.embeddings.localai import LocalAIEmbeddings
from oplangchain.embeddings.minimax import MiniMaxEmbeddings
from oplangchain.embeddings.mlflow_gateway import MlflowAIGatewayEmbeddings
from oplangchain.embeddings.modelscope_hub import ModelScopeEmbeddings
from oplangchain.embeddings.mosaicml import MosaicMLInstructorEmbeddings
from oplangchain.embeddings.nlpcloud import NLPCloudEmbeddings
from oplangchain.embeddings.octoai_embeddings import OctoAIEmbeddings
from oplangchain.embeddings.openai import OpenAIEmbeddings
from oplangchain.embeddings.sagemaker_endpoint import SagemakerEndpointEmbeddings
from oplangchain.embeddings.self_hosted import SelfHostedEmbeddings
from oplangchain.embeddings.self_hosted_hugging_face import (
    SelfHostedHuggingFaceEmbeddings,
    SelfHostedHuggingFaceInstructEmbeddings,
)
from oplangchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from oplangchain.embeddings.spacy_embeddings import SpacyEmbeddings
from oplangchain.embeddings.tensorflow_hub import TensorflowHubEmbeddings
from oplangchain.embeddings.vertexai import VertexAIEmbeddings
from oplangchain.embeddings.xinference import XinferenceEmbeddings

logger = logging.getLogger(__name__)

__all__ = [
    "OpenAIEmbeddings",
    "HuggingFaceEmbeddings",
    "CohereEmbeddings",
    "ClarifaiEmbeddings",
    "ElasticsearchEmbeddings",
    "JinaEmbeddings",
    "LlamaCppEmbeddings",
    "HuggingFaceHubEmbeddings",
    "MlflowAIGatewayEmbeddings",
    "ModelScopeEmbeddings",
    "TensorflowHubEmbeddings",
    "SagemakerEndpointEmbeddings",
    "HuggingFaceInstructEmbeddings",
    "MosaicMLInstructorEmbeddings",
    "SelfHostedEmbeddings",
    "SelfHostedHuggingFaceEmbeddings",
    "SelfHostedHuggingFaceInstructEmbeddings",
    "FakeEmbeddings",
    "DeterministicFakeEmbedding",
    "AlephAlphaAsymmetricSemanticEmbedding",
    "AlephAlphaSymmetricSemanticEmbedding",
    "SentenceTransformerEmbeddings",
    "GooglePalmEmbeddings",
    "MiniMaxEmbeddings",
    "VertexAIEmbeddings",
    "BedrockEmbeddings",
    "DeepInfraEmbeddings",
    "EdenAiEmbeddings",
    "DashScopeEmbeddings",
    "EmbaasEmbeddings",
    "OctoAIEmbeddings",
    "SpacyEmbeddings",
    "NLPCloudEmbeddings",
    "GPT4AllEmbeddings",
    "XinferenceEmbeddings",
    "LocalAIEmbeddings",
    "AwaEmbeddings",
]


# TODO: this is in here to maintain backwards compatibility
class HypotheticalDocumentEmbedder:
    def __init__(self, *args: Any, **kwargs: Any):
        logger.warning(
            "Using a deprecated class. Please use "
            "`from oplangchain.chains import HypotheticalDocumentEmbedder` instead"
        )
        from oplangchain.chains.hyde.base import HypotheticalDocumentEmbedder as H

        return H(*args, **kwargs)  # type: ignore

    @classmethod
    def from_llm(cls, *args: Any, **kwargs: Any) -> Any:
        logger.warning(
            "Using a deprecated class. Please use "
            "`from oplangchain.chains import HypotheticalDocumentEmbedder` instead"
        )
        from oplangchain.chains.hyde.base import HypotheticalDocumentEmbedder as H

        return H.from_llm(*args, **kwargs)
