"""
This tool allows agents to interact with the atlassian-python-api library
and operate on a Jira instance. For more information on the
atlassian-python-api library, see https://atlassian-python-api.readthedocs.io/jira.html

To use this tool, you must first set as environment variables:
    JIRA_API_TOKEN
    JIRA_USERNAME
    JIRA_INSTANCE_URL

Below is a sample script that uses the Jira tool:

```python
from oplangchain.agents import AgentType
from oplangchain.agents import initialize_agent
from oplangchain.agents.agent_toolkits.jira.toolkit import JiraToolkit
from oplangchain.llms import OpenAI
from oplangchain.utilities.jira import JiraAPIWrapper

llm = OpenAI(temperature=0)
jira = JiraAPIWrapper()
toolkit = JiraToolkit.from_jira_api_wrapper(jira)
agent = initialize_agent(
    toolkit.get_tools(),
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```
"""
from typing import Optional

from pydantic import Field

from oplangchain.callbacks.manager import CallbackManagerForToolRun
from oplangchain.tools.base import BaseTool
from oplangchain.utilities.jira import JiraAPIWrapper


class JiraAction(BaseTool):
    """Tool that queries the Atlassian Jira API."""

    api_wrapper: JiraAPIWrapper = Field(default_factory=JiraAPIWrapper)
    mode: str
    name = ""
    description = ""

    def _run(
        self,
        instructions: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Atlassian Jira API to run an operation."""
        return self.api_wrapper.run(self.mode, instructions)
