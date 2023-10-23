"""OpenAPI spec agent."""
from typing import Any, Dict, List, Optional

from oplangchain.agents.agent import AgentExecutor
from oplangchain.agents.agent_toolkits.openapi.prompt import (
    OPENAPI_PREFIX,
    OPENAPI_SUFFIX,
)
from oplangchain.agents.agent_toolkits.openapi.toolkit import OpenAPIToolkit
from oplangchain.agents.mrkl.base import ZeroShotAgent
from oplangchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
from oplangchain.callbacks.base import BaseCallbackManager
from oplangchain.chains.llm import LLMChain
from oplangchain.schema.language_model import BaseLanguageModel


def create_openapi_agent(
    llm: BaseLanguageModel,
    toolkit: OpenAPIToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = OPENAPI_PREFIX,
    suffix: str = OPENAPI_SUFFIX,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    verbose: bool = False,
    return_intermediate_steps: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct an OpenAPI agent from an LLM and tools."""
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
        return_intermediate_steps=return_intermediate_steps,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        **(agent_executor_kwargs or {}),
    )
