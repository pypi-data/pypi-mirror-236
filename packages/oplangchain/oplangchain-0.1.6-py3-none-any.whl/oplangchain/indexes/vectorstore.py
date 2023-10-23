from typing import Any, List, Optional, Type

from pydantic import BaseModel, Extra, Field

from oplangchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from oplangchain.chains.retrieval_qa.base import RetrievalQA
from oplangchain.document_loaders.base import BaseLoader
from oplangchain.embeddings.base import Embeddings
from oplangchain.embeddings.openai import OpenAIEmbeddings
from oplangchain.llms.openai import OpenAI
from oplangchain.schema import Document
from oplangchain.schema.language_model import BaseLanguageModel
from oplangchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from oplangchain.vectorstores.base import VectorStore
from oplangchain.vectorstores.chroma import Chroma


def _get_default_text_splitter() -> TextSplitter:
    return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)


class VectorStoreIndexWrapper(BaseModel):
    """Wrapper around a vectorstore for easy access."""

    vectorstore: VectorStore

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def query(
        self, question: str, llm: Optional[BaseLanguageModel] = None, **kwargs: Any
    ) -> str:
        """Query the vectorstore."""
        llm = llm or OpenAI(temperature=0)
        chain = RetrievalQA.from_chain_type(
            llm, retriever=self.vectorstore.as_retriever(), **kwargs
        )
        return chain.run(question)

    def query_with_sources(
        self, question: str, llm: Optional[BaseLanguageModel] = None, **kwargs: Any
    ) -> dict:
        """Query the vectorstore and get back sources."""
        llm = llm or OpenAI(temperature=0)
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm, retriever=self.vectorstore.as_retriever(), **kwargs
        )
        return chain({chain.question_key: question})


class VectorstoreIndexCreator(BaseModel):
    """Logic for creating indexes."""

    vectorstore_cls: Type[VectorStore] = Chroma
    embedding: Embeddings = Field(default_factory=OpenAIEmbeddings)
    text_splitter: TextSplitter = Field(default_factory=_get_default_text_splitter)
    vectorstore_kwargs: dict = Field(default_factory=dict)

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def from_loaders(self, loaders: List[BaseLoader]) -> VectorStoreIndexWrapper:
        """Create a vectorstore index from loaders."""
        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        return self.from_documents(docs)

    def from_documents(self, documents: List[Document]) -> VectorStoreIndexWrapper:
        """Create a vectorstore index from documents."""
        sub_docs = self.text_splitter.split_documents(documents)
        vectorstore = self.vectorstore_cls.from_documents(
            sub_docs, self.embedding, **self.vectorstore_kwargs
        )
        return VectorStoreIndexWrapper(vectorstore=vectorstore)
