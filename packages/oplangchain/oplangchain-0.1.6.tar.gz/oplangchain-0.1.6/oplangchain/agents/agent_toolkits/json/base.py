"""Json agent."""
from typing import Any, Dict, List, Optional

from oplangchain.agents.agent import AgentExecutor
from oplangchain.agents.agent_toolkits.json.prompt import JSON_PREFIX, JSON_SUFFIX
from oplangchain.agents.agent_toolkits.json.toolkit import JsonToolkit
from oplangchain.agents.mrkl.base import ZeroShotAgent
from oplangchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
from oplangchain.callbacks.base import BaseCallbackManager
from oplangchain.chains.llm import LLMChain
from oplangchain.schema.language_model import BaseLanguageModel


def create_json_agent(
    llm: BaseLanguageModel,
    toolkit: JsonToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = JSON_PREFIX,
    suffix: str = JSON_SUFFIX,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct a json agent from an LLM and tools."""
    tools = toolkit.get_tools()
    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        format_instructions=format_instructions,
        input_variables=input_variables,
    )
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        callback_manager=callback_manager,
    )
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, **kwargs)
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        **(agent_executor_kwargs or {}),
    )
