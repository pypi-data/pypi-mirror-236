"""**Document Loaders**  are classes to load Documents.

**Document Loaders** are usually used to load a lot of Documents in a single run.

**Class hierarchy:**

.. code-block::

    BaseLoader --> <name>Loader  # Examples: TextLoader, UnstructuredFileLoader

**Main helpers:**

.. code-block::

    Document, <name>TextSplitter
"""

from oplangchain.document_loaders.acreom import AcreomLoader
from oplangchain.document_loaders.airbyte_json import AirbyteJSONLoader
from oplangchain.document_loaders.airtable import AirtableLoader
from oplangchain.document_loaders.apify_dataset import ApifyDatasetLoader
from oplangchain.document_loaders.arxiv import ArxivLoader
from oplangchain.document_loaders.async_html import AsyncHtmlLoader
from oplangchain.document_loaders.azlyrics import AZLyricsLoader
from oplangchain.document_loaders.azure_blob_storage_container import (
    AzureBlobStorageContainerLoader,
)
from oplangchain.document_loaders.azure_blob_storage_file import (
    AzureBlobStorageFileLoader,
)
from oplangchain.document_loaders.bibtex import BibtexLoader
from oplangchain.document_loaders.bigquery import BigQueryLoader
from oplangchain.document_loaders.bilibili import BiliBiliLoader
from oplangchain.document_loaders.blackboard import BlackboardLoader
from oplangchain.document_loaders.blob_loaders import (
    Blob,
    BlobLoader,
    FileSystemBlobLoader,
    YoutubeAudioLoader,
)
from oplangchain.document_loaders.blockchain import BlockchainDocumentLoader
from oplangchain.document_loaders.brave_search import BraveSearchLoader
from oplangchain.document_loaders.browserless import BrowserlessLoader
from oplangchain.document_loaders.chatgpt import ChatGPTLoader
from oplangchain.document_loaders.college_confidential import CollegeConfidentialLoader
from oplangchain.document_loaders.concurrent import ConcurrentLoader
from oplangchain.document_loaders.confluence import ConfluenceLoader
from oplangchain.document_loaders.conllu import CoNLLULoader
from oplangchain.document_loaders.csv_loader import CSVLoader, UnstructuredCSVLoader
from oplangchain.document_loaders.cube_semantic import CubeSemanticLoader
from oplangchain.document_loaders.datadog_logs import DatadogLogsLoader
from oplangchain.document_loaders.dataframe import DataFrameLoader
from oplangchain.document_loaders.diffbot import DiffbotLoader
from oplangchain.document_loaders.directory import DirectoryLoader
from oplangchain.document_loaders.discord import DiscordChatLoader
from oplangchain.document_loaders.docugami import DocugamiLoader
from oplangchain.document_loaders.dropbox import DropboxLoader
from oplangchain.document_loaders.duckdb_loader import DuckDBLoader
from oplangchain.document_loaders.email import (
    OutlookMessageLoader,
    UnstructuredEmailLoader,
)
from oplangchain.document_loaders.embaas import EmbaasBlobLoader, EmbaasLoader
from oplangchain.document_loaders.epub import UnstructuredEPubLoader
from oplangchain.document_loaders.etherscan import EtherscanLoader
from oplangchain.document_loaders.evernote import EverNoteLoader
from oplangchain.document_loaders.excel import UnstructuredExcelLoader
from oplangchain.document_loaders.facebook_chat import FacebookChatLoader
from oplangchain.document_loaders.fauna import FaunaLoader
from oplangchain.document_loaders.figma import FigmaFileLoader
from oplangchain.document_loaders.gcs_directory import GCSDirectoryLoader
from oplangchain.document_loaders.gcs_file import GCSFileLoader
from oplangchain.document_loaders.geodataframe import GeoDataFrameLoader
from oplangchain.document_loaders.git import GitLoader
from oplangchain.document_loaders.gitbook import GitbookLoader
from oplangchain.document_loaders.github import GitHubIssuesLoader
from oplangchain.document_loaders.googledrive import GoogleDriveLoader
from oplangchain.document_loaders.gutenberg import GutenbergLoader
from oplangchain.document_loaders.hn import HNLoader
from oplangchain.document_loaders.html import UnstructuredHTMLLoader
from oplangchain.document_loaders.html_bs import BSHTMLLoader
from oplangchain.document_loaders.hugging_face_dataset import HuggingFaceDatasetLoader
from oplangchain.document_loaders.ifixit import IFixitLoader
from oplangchain.document_loaders.image import UnstructuredImageLoader
from oplangchain.document_loaders.image_captions import ImageCaptionLoader
from oplangchain.document_loaders.imsdb import IMSDbLoader
from oplangchain.document_loaders.iugu import IuguLoader
from oplangchain.document_loaders.joplin import JoplinLoader
from oplangchain.document_loaders.json_loader import JSONLoader
from oplangchain.document_loaders.larksuite import LarkSuiteDocLoader
from oplangchain.document_loaders.markdown import UnstructuredMarkdownLoader
from oplangchain.document_loaders.mastodon import MastodonTootsLoader
from oplangchain.document_loaders.max_compute import MaxComputeLoader
from oplangchain.document_loaders.mediawikidump import MWDumpLoader
from oplangchain.document_loaders.merge import MergedDataLoader
from oplangchain.document_loaders.mhtml import MHTMLLoader
from oplangchain.document_loaders.modern_treasury import ModernTreasuryLoader
from oplangchain.document_loaders.news import NewsURLLoader
from oplangchain.document_loaders.notebook import NotebookLoader
from oplangchain.document_loaders.notion import NotionDirectoryLoader
from oplangchain.document_loaders.notiondb import NotionDBLoader
from oplangchain.document_loaders.obs_directory import OBSDirectoryLoader
from oplangchain.document_loaders.obs_file import OBSFileLoader
from oplangchain.document_loaders.obsidian import ObsidianLoader
from oplangchain.document_loaders.odt import UnstructuredODTLoader
from oplangchain.document_loaders.onedrive import OneDriveLoader
from oplangchain.document_loaders.onedrive_file import OneDriveFileLoader
from oplangchain.document_loaders.open_city_data import OpenCityDataLoader
from oplangchain.document_loaders.org_mode import UnstructuredOrgModeLoader
from oplangchain.document_loaders.pdf import (
    AmazonTextractPDFLoader,
    MathpixPDFLoader,
    OnlinePDFLoader,
    PDFMinerLoader,
    PDFMinerPDFasHTMLLoader,
    PDFPlumberLoader,
    PyMuPDFLoader,
    PyPDFDirectoryLoader,
    PyPDFium2Loader,
    PyPDFLoader,
    UnstructuredPDFLoader,
)
from oplangchain.document_loaders.powerpoint import UnstructuredPowerPointLoader
from oplangchain.document_loaders.psychic import PsychicLoader
from oplangchain.document_loaders.pyspark_dataframe import PySparkDataFrameLoader
from oplangchain.document_loaders.python import PythonLoader
from oplangchain.document_loaders.readthedocs import ReadTheDocsLoader
from oplangchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from oplangchain.document_loaders.reddit import RedditPostsLoader
from oplangchain.document_loaders.roam import RoamLoader
from oplangchain.document_loaders.rocksetdb import RocksetLoader
from oplangchain.document_loaders.rss import RSSFeedLoader
from oplangchain.document_loaders.rst import UnstructuredRSTLoader
from oplangchain.document_loaders.rtf import UnstructuredRTFLoader
from oplangchain.document_loaders.s3_directory import S3DirectoryLoader
from oplangchain.document_loaders.s3_file import S3FileLoader
from oplangchain.document_loaders.sitemap import SitemapLoader
from oplangchain.document_loaders.slack_directory import SlackDirectoryLoader
from oplangchain.document_loaders.snowflake_loader import SnowflakeLoader
from oplangchain.document_loaders.spreedly import SpreedlyLoader
from oplangchain.document_loaders.srt import SRTLoader
from oplangchain.document_loaders.stripe import StripeLoader
from oplangchain.document_loaders.telegram import (
    TelegramChatApiLoader,
    TelegramChatFileLoader,
)
from oplangchain.document_loaders.tencent_cos_directory import TencentCOSDirectoryLoader
from oplangchain.document_loaders.tencent_cos_file import TencentCOSFileLoader
from oplangchain.document_loaders.text import TextLoader
from oplangchain.document_loaders.tomarkdown import ToMarkdownLoader
from oplangchain.document_loaders.toml import TomlLoader
from oplangchain.document_loaders.trello import TrelloLoader
from oplangchain.document_loaders.tsv import UnstructuredTSVLoader
from oplangchain.document_loaders.twitter import TwitterTweetLoader
from oplangchain.document_loaders.unstructured import (
    UnstructuredAPIFileIOLoader,
    UnstructuredAPIFileLoader,
    UnstructuredFileIOLoader,
    UnstructuredFileLoader,
)
from oplangchain.document_loaders.url import UnstructuredURLLoader
from oplangchain.document_loaders.url_playwright import PlaywrightURLLoader
from oplangchain.document_loaders.url_selenium import SeleniumURLLoader
from oplangchain.document_loaders.weather import WeatherDataLoader
from oplangchain.document_loaders.web_base import WebBaseLoader
from oplangchain.document_loaders.whatsapp_chat import WhatsAppChatLoader
from oplangchain.document_loaders.wikipedia import WikipediaLoader
from oplangchain.document_loaders.word_document import (
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
)
from oplangchain.document_loaders.xml import UnstructuredXMLLoader
from oplangchain.document_loaders.xorbits import XorbitsLoader
from oplangchain.document_loaders.youtube import (
    GoogleApiClient,
    GoogleApiYoutubeLoader,
    YoutubeLoader,
)

# Legacy: only for backwards compatibility. Use PyPDFLoader instead
PagedPDFSplitter = PyPDFLoader

# For backwards compatibility
TelegramChatLoader = TelegramChatFileLoader

__all__ = [
    "AcreomLoader",
    "AsyncHtmlLoader",
    "AZLyricsLoader",
    "AirbyteJSONLoader",
    "AirtableLoader",
    "ApifyDatasetLoader",
    "ArxivLoader",
    "AzureBlobStorageContainerLoader",
    "AzureBlobStorageFileLoader",
    "BSHTMLLoader",
    "BibtexLoader",
    "BigQueryLoader",
    "BiliBiliLoader",
    "BlackboardLoader",
    "Blob",
    "BlobLoader",
    "BlockchainDocumentLoader",
    "BraveSearchLoader",
    "BrowserlessLoader",
    "CSVLoader",
    "ChatGPTLoader",
    "CoNLLULoader",
    "CollegeConfidentialLoader",
    "ConfluenceLoader",
    "CubeSemanticLoader",
    "DatadogLogsLoader",
    "DataFrameLoader",
    "DiffbotLoader",
    "DirectoryLoader",
    "DiscordChatLoader",
    "DocugamiLoader",
    "Docx2txtLoader",
    "DropboxLoader",
    "DuckDBLoader",
    "EmbaasBlobLoader",
    "EmbaasLoader",
    "EtherscanLoader",
    "EverNoteLoader",
    "FacebookChatLoader",
    "FaunaLoader",
    "FigmaFileLoader",
    "FileSystemBlobLoader",
    "GCSDirectoryLoader",
    "GCSFileLoader",
    "GeoDataFrameLoader",
    "GitHubIssuesLoader",
    "GitLoader",
    "GitbookLoader",
    "GoogleApiClient",
    "GoogleApiYoutubeLoader",
    "GoogleDriveLoader",
    "GutenbergLoader",
    "HNLoader",
    "HuggingFaceDatasetLoader",
    "HuggingFaceDatasetLoader",
    "IFixitLoader",
    "IMSDbLoader",
    "ImageCaptionLoader",
    "IuguLoader",
    "JSONLoader",
    "JoplinLoader",
    "LarkSuiteDocLoader",
    "MWDumpLoader",
    "MastodonTootsLoader",
    "MathpixPDFLoader",
    "MaxComputeLoader",
    "MergedDataLoader",
    "MHTMLLoader",
    "ModernTreasuryLoader",
    "NewsURLLoader",
    "NotebookLoader",
    "NotionDBLoader",
    "NotionDirectoryLoader",
    "OBSDirectoryLoader",
    "OBSFileLoader",
    "ObsidianLoader",
    "OneDriveFileLoader",
    "OneDriveLoader",
    "OnlinePDFLoader",
    "OutlookMessageLoader",
    "OpenCityDataLoader",
    "PDFMinerLoader",
    "PDFMinerPDFasHTMLLoader",
    "PDFPlumberLoader",
    "PagedPDFSplitter",
    "PlaywrightURLLoader",
    "PsychicLoader",
    "PyMuPDFLoader",
    "PyPDFDirectoryLoader",
    "PyPDFLoader",
    "PyPDFium2Loader",
    "PySparkDataFrameLoader",
    "PythonLoader",
    "ReadTheDocsLoader",
    "RecursiveUrlLoader",
    "RedditPostsLoader",
    "RoamLoader",
    "RocksetLoader",
    "RSSFeedLoader",
    "S3DirectoryLoader",
    "S3FileLoader",
    "SRTLoader",
    "SeleniumURLLoader",
    "SitemapLoader",
    "SlackDirectoryLoader",
    "SnowflakeLoader",
    "SpreedlyLoader",
    "StripeLoader",
    "TencentCOSDirectoryLoader",
    "TencentCOSFileLoader",
    "TelegramChatApiLoader",
    "TelegramChatFileLoader",
    "TelegramChatLoader",
    "TextLoader",
    "ToMarkdownLoader",
    "TomlLoader",
    "TrelloLoader",
    "TwitterTweetLoader",
    "UnstructuredAPIFileIOLoader",
    "UnstructuredAPIFileLoader",
    "UnstructuredCSVLoader",
    "UnstructuredEPubLoader",
    "UnstructuredEmailLoader",
    "UnstructuredExcelLoader",
    "UnstructuredFileIOLoader",
    "UnstructuredFileLoader",
    "UnstructuredHTMLLoader",
    "UnstructuredImageLoader",
    "UnstructuredMarkdownLoader",
    "UnstructuredODTLoader",
    "UnstructuredOrgModeLoader",
    "UnstructuredPDFLoader",
    "UnstructuredPowerPointLoader",
    "UnstructuredRSTLoader",
    "UnstructuredRTFLoader",
    "UnstructuredTSVLoader",
    "UnstructuredURLLoader",
    "UnstructuredWordDocumentLoader",
    "UnstructuredXMLLoader",
    "WeatherDataLoader",
    "WebBaseLoader",
    "WhatsAppChatLoader",
    "WikipediaLoader",
    "XorbitsLoader",
    "YoutubeAudioLoader",
    "YoutubeLoader",
    "ConcurrentLoader",
    "AmazonTextractPDFLoader",
]
