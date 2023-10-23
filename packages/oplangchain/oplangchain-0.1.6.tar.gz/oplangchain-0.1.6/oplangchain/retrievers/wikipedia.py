from typing import List

from oplangchain.callbacks.manager import CallbackManagerForRetrieverRun
from oplangchain.schema import BaseRetriever, Document
from oplangchain.utilities.wikipedia import WikipediaAPIWrapper


class WikipediaRetriever(BaseRetriever, WikipediaAPIWrapper):
    """Retriever for Wikipedia API.

    It wraps load() to get_relevant_documents().
    It uses all WikipediaAPIWrapper arguments without any change.
    """

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return self.load(query=query)
