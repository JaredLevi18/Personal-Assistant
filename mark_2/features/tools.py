from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.utilities import WikipediaAPIWrapper, PythonREPL
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import Any, List, Union
from langchain.schema import AgentAction, AgentFinish, BaseMessage, HumanMessage
import re
from getpass import getpass

# let's set up the tools the agent may use
SERPAPI_API_KEY = getpass()

# Define the tools the agent can use to answer the questions we ask.
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
wikipedia = WikipediaAPIWrapper()
python = PythonREPL()
tools = [
    Tool.from_function(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),

    Tool.from_function(
        name="Wikipedia",
        func=wikipedia.run,
        description="useful for when you need to know something about a person or a country"
    ),

    Tool.from_function(
        name="Python",
        func=python.run,
        description="useful for when you need to use python code."
    )
]

# Set up the base template
template = """Complete the objective as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

These were previous tasks you completed:



Begin!

Question: {input}
{agent_scratchpad}"""

# set up a promt template
class CustomPromtTemplate(BaseChatPromptTemplate):
    # the template to use
    template: str
    # the list of tools to use
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        # Get the intermidiate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermidiate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # create a  tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]
    
prompt = CustomPromtTemplate(
    template=template,
    tools=tools,
    input_variables=["input", "intermediate_steps"]
)

class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # check is agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single 'output' key
                # It is not recommended to try anything else at the moment
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()}
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r""
        return
