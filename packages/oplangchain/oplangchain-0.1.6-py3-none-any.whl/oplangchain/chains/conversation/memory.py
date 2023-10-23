"""Memory modules for conversation prompts."""

from oplangchain.memory.buffer import (
    ConversationBufferMemory,
    ConversationStringBufferMemory,
)
from oplangchain.memory.buffer_window import ConversationBufferWindowMemory
from oplangchain.memory.combined import CombinedMemory
from oplangchain.memory.entity import ConversationEntityMemory
from oplangchain.memory.kg import ConversationKGMemory
from oplangchain.memory.summary import ConversationSummaryMemory
from oplangchain.memory.summary_buffer import ConversationSummaryBufferMemory

# This is only for backwards compatibility.

__all__ = [
    "ConversationSummaryBufferMemory",
    "ConversationSummaryMemory",
    "ConversationKGMemory",
    "ConversationBufferWindowMemory",
    "ConversationEntityMemory",
    "ConversationBufferMemory",
    "CombinedMemory",
    "ConversationStringBufferMemory",
]
