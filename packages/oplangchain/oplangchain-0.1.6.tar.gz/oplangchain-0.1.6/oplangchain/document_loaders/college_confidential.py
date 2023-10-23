"""Loads College Confidential."""
from typing import List

from oplangchain.docstore.document import Document
from oplangchain.document_loaders.web_base import WebBaseLoader


class CollegeConfidentialLoader(WebBaseLoader):
    """Loads College Confidential webpages."""

    def load(self) -> List[Document]:
        """Load webpages as Documents."""
        soup = self.scrape()
        text = soup.select_one("main[class='skin-handler']").text
        metadata = {"source": self.web_path}
        return [Document(page_content=text, metadata=metadata)]
