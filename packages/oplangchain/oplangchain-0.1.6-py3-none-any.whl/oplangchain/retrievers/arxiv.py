from typing import List

from oplangchain.callbacks.manager import CallbackManagerForRetrieverRun
from oplangchain.schema import BaseRetriever, Document
from oplangchain.utilities.arxiv import ArxivAPIWrapper


class ArxivRetriever(BaseRetriever, ArxivAPIWrapper):
    """
    Retriever for Arxiv.

    It wraps load() to get_relevant_documents().
    It uses all ArxivAPIWrapper arguments without any change.
    """

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return self.load(query=query)
