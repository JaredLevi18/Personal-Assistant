# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.tools import DuckDuckGoSearchRun
from pydantic import BaseModel, Field
from langchain.utilities import WikipediaAPIWrapper, PythonREPL
import os

os.environ["OPENAI_API_KEY"] = "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"

# initializing the llm
llm = ChatOpenAI(temperature=0.7)
search = DuckDuckGoSearchRun()
wikipedia = WikipediaAPIWrapper()
python_repl = PythonREPL()

tools = [
    Tool.from_function(
        func=search.run,
        name='Search',
        description="Useful for when you need to answer questions about current events",
    ),

    Tool.from_function(
        func=wikipedia.run,
        name='Wikipedia',
        description='Useful for when you need to look up a topic, country or person on wikipedia'
    ),

    Tool.from_function(
        func=python_repl.run,
        name='PythonREPL',
        description='Useful for when you need to use python to answer a question, You shoud input python code.'
    )
]

# make the agent
agent = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)    k=3,
    return_messages=True
)
