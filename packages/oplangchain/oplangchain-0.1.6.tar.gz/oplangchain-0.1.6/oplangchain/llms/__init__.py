"""
**LLM** classes provide
access to the large language model (**LLM**) APIs and services.

**Class hierarchy:**

.. code-block::

    BaseLanguageModel --> BaseLLM --> LLM --> <name>  # Examples: AI21, HuggingFaceHub, OpenAI

**Main helpers:**

.. code-block::

    LLMResult, PromptValue,
    CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun,
    CallbackManager, AsyncCallbackManager,
    AIMessage, BaseMessage
"""  # noqa: E501
from typing import Dict, Type

from oplangchain.llms.ai21 import AI21
from oplangchain.llms.aleph_alpha import AlephAlpha
from oplangchain.llms.amazon_api_gateway import AmazonAPIGateway
from oplangchain.llms.anthropic import Anthropic
from oplangchain.llms.anyscale import Anyscale
from oplangchain.llms.aviary import Aviary
from oplangchain.llms.azureml_endpoint import AzureMLOnlineEndpoint
from oplangchain.llms.bananadev import Banana
from oplangchain.llms.base import BaseLLM
from oplangchain.llms.baseten import Baseten
from oplangchain.llms.beam import Beam
from oplangchain.llms.bedrock import Bedrock
from oplangchain.llms.cerebriumai import CerebriumAI
from oplangchain.llms.chatglm import ChatGLM
from oplangchain.llms.clarifai import Clarifai
from oplangchain.llms.cohere import Cohere
from oplangchain.llms.ctransformers import CTransformers
from oplangchain.llms.databricks import Databricks
from oplangchain.llms.deepinfra import DeepInfra
from oplangchain.llms.edenai import EdenAI
from oplangchain.llms.fake import FakeListLLM
from oplangchain.llms.fireworks import Fireworks, FireworksChat
from oplangchain.llms.forefrontai import ForefrontAI
from oplangchain.llms.google_palm import GooglePalm
from oplangchain.llms.gooseai import GooseAI
from oplangchain.llms.gpt4all import GPT4All
from oplangchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from oplangchain.llms.huggingface_hub import HuggingFaceHub
from oplangchain.llms.huggingface_pipeline import HuggingFacePipeline
from oplangchain.llms.huggingface_text_gen_inference import HuggingFaceTextGenInference
from oplangchain.llms.human import HumanInputLLM
from oplangchain.llms.koboldai import KoboldApiLLM
from oplangchain.llms.llamacpp import LlamaCpp
from oplangchain.llms.manifest import ManifestWrapper
from oplangchain.llms.minimax import Minimax
from oplangchain.llms.mlflow_ai_gateway import MlflowAIGateway
from oplangchain.llms.modal import Modal
from oplangchain.llms.mosaicml import MosaicML
from oplangchain.llms.nlpcloud import NLPCloud
from oplangchain.llms.octoai_endpoint import OctoAIEndpoint
from oplangchain.llms.openai import AzureOpenAI, OpenAI, OpenAIChat
from oplangchain.llms.openllm import OpenLLM
from oplangchain.llms.openlm import OpenLM
from oplangchain.llms.petals import Petals
from oplangchain.llms.pipelineai import PipelineAI
from oplangchain.llms.predibase import Predibase
from oplangchain.llms.predictionguard import PredictionGuard
from oplangchain.llms.promptlayer_openai import PromptLayerOpenAI, PromptLayerOpenAIChat
from oplangchain.llms.replicate import Replicate
from oplangchain.llms.rwkv import RWKV
from oplangchain.llms.sagemaker_endpoint import SagemakerEndpoint
from oplangchain.llms.self_hosted import SelfHostedPipeline
from oplangchain.llms.self_hosted_hugging_face import SelfHostedHuggingFaceLLM
from oplangchain.llms.stochasticai import StochasticAI
from oplangchain.llms.textgen import TextGen
from oplangchain.llms.tongyi import Tongyi
from oplangchain.llms.vertexai import VertexAI
from oplangchain.llms.vllm import VLLM
from oplangchain.llms.writer import Writer
from oplangchain.llms.xinference import Xinference

__all__ = [
    "AI21",
    "AlephAlpha",
    "AmazonAPIGateway",
    "Anthropic",
    "Anyscale",
    "Aviary",
    "AzureMLOnlineEndpoint",
    "AzureOpenAI",
    "Banana",
    "Baseten",
    "Beam",
    "Bedrock",
    "CTransformers",
    "CerebriumAI",
    "ChatGLM",
    "Clarifai",
    "Cohere",
    "Databricks",
    "DeepInfra",
    "EdenAI",
    "FakeListLLM",
    "Fireworks",
    "FireworksChat",
    "ForefrontAI",
    "GPT4All",
    "GooglePalm",
    "GooseAI",
    "HuggingFaceEndpoint",
    "HuggingFaceHub",
    "HuggingFacePipeline",
    "HuggingFaceTextGenInference",
    "HumanInputLLM",
    "KoboldApiLLM",
    "LlamaCpp",
    "TextGen",
    "ManifestWrapper",
    "Minimax",
    "MlflowAIGateway",
    "Modal",
    "MosaicML",
    "NLPCloud",
    "OpenAI",
    "OpenAIChat",
    "OpenLLM",
    "OpenLM",
    "Petals",
    "PipelineAI",
    "Predibase",
    "PredictionGuard",
    "PromptLayerOpenAI",
    "PromptLayerOpenAIChat",
    "RWKV",
    "Replicate",
    "SagemakerEndpoint",
    "SelfHostedHuggingFaceLLM",
    "SelfHostedPipeline",
    "StochasticAI",
    "Tongyi",
    "VertexAI",
    "VLLM",
    "Writer",
    "OctoAIEndpoint",
    "Xinference",
]

type_to_cls_dict: Dict[str, Type[BaseLLM]] = {
    "ai21": AI21,
    "aleph_alpha": AlephAlpha,
    "amazon_api_gateway": AmazonAPIGateway,
    "amazon_bedrock": Bedrock,
    "anthropic": Anthropic,
    "anyscale": Anyscale,
    "aviary": Aviary,
    "azure": AzureOpenAI,
    "azureml_endpoint": AzureMLOnlineEndpoint,
    "bananadev": Banana,
    "baseten": Baseten,
    "beam": Beam,
    "cerebriumai": CerebriumAI,
    "chat_glm": ChatGLM,
    "clarifai": Clarifai,
    "cohere": Cohere,
    "ctransformers": CTransformers,
    "databricks": Databricks,
    "deepinfra": DeepInfra,
    "edenai": EdenAI,
    "fake-list": FakeListLLM,
    "forefrontai": ForefrontAI,
    "google_palm": GooglePalm,
    "gooseai": GooseAI,
    "gpt4all": GPT4All,
    "huggingface_endpoint": HuggingFaceEndpoint,
    "huggingface_hub": HuggingFaceHub,
    "huggingface_pipeline": HuggingFacePipeline,
    "huggingface_textgen_inference": HuggingFaceTextGenInference,
    "human-input": HumanInputLLM,
    "koboldai": KoboldApiLLM,
    "llamacpp": LlamaCpp,
    "textgen": TextGen,
    "minimax": Minimax,
    "mlflow-ai-gateway": MlflowAIGateway,
    "modal": Modal,
    "mosaic": MosaicML,
    "nlpcloud": NLPCloud,
    "openai": OpenAI,
    "openlm": OpenLM,
    "petals": Petals,
    "pipelineai": PipelineAI,
    "predibase": Predibase,
    "replicate": Replicate,
    "rwkv": RWKV,
    "sagemaker_endpoint": SagemakerEndpoint,
    "self_hosted": SelfHostedPipeline,
    "self_hosted_hugging_face": SelfHostedHuggingFaceLLM,
    "stochasticai": StochasticAI,
    "tongyi": Tongyi,
    "vertexai": VertexAI,
    "openllm": OpenLLM,
    "openllm_client": OpenLLM,
    "vllm": VLLM,
    "writer": Writer,
    "xinference": Xinference,
}
