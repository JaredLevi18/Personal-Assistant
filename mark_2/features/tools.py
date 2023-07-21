from langchain import OpenAI
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.tools import BaseTool
from langchain.tools import DuckDuckGoSearchRun

os.environ["OPENAI_API_KEY"] = ""
# setup the turbo LLM
turbo_llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name = "search",
        func = search.run,
        description="useful for when you need something from the internet",
    )
]

# creating an agent
memory = ConversationBufferWindowMemory(
    memory_key='chat-history',
    k=3,
    return_messages=True
)

conversational_agent = initialize_agent(tools=tools, llm=turbo_llm, agent=memory)

conversational_agent("What time is it in London?")
