from typing import List

from oplangchain.callbacks.manager import CallbackManagerForRetrieverRun
from oplangchain.schema import BaseRetriever, Document
from oplangchain.utilities.pupmed import PubMedAPIWrapper


class PubMedRetriever(BaseRetriever, PubMedAPIWrapper):
    """Retriever for PubMed API.

    It wraps load() to get_relevant_documents().
    It uses all PubMedAPIWrapper arguments without any change.
    """

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return self.load_docs(query=query)
