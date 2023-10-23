from typing import Dict, Type, Union

from oplangchain.agents.agent import BaseSingleActionAgent
from oplangchain.agents.agent_types import AgentType
from oplangchain.agents.chat.base import ChatAgent
from oplangchain.agents.conversational.base import ConversationalAgent
from oplangchain.agents.conversational_chat.base import ConversationalChatAgent
from oplangchain.agents.mrkl.base import ZeroShotAgent
from oplangchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from oplangchain.agents.openai_functions_multi_agent.base import (
    OpenAIMultiFunctionsAgent,
)
from oplangchain.agents.react.base import ReActDocstoreAgent
from oplangchain.agents.self_ask_with_search.base import SelfAskWithSearchAgent
from oplangchain.agents.structured_chat.base import StructuredChatAgent

AGENT_TYPE = Union[Type[BaseSingleActionAgent], Type[OpenAIMultiFunctionsAgent]]

AGENT_TO_CLASS: Dict[AgentType, AGENT_TYPE] = {
    AgentType.ZERO_SHOT_REACT_DESCRIPTION: ZeroShotAgent,
    AgentType.REACT_DOCSTORE: ReActDocstoreAgent,
    AgentType.SELF_ASK_WITH_SEARCH: SelfAskWithSearchAgent,
    AgentType.CONVERSATIONAL_REACT_DESCRIPTION: ConversationalAgent,
    AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION: ChatAgent,
    AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION: ConversationalChatAgent,
    AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION: StructuredChatAgent,
    AgentType.OPENAI_FUNCTIONS: OpenAIFunctionsAgent,
    AgentType.OPENAI_MULTI_FUNCTIONS: OpenAIMultiFunctionsAgent,
}
