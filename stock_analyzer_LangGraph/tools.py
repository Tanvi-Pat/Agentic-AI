from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool

def llm():
    llm = ChatOpenAI(model= "gpt-4o-mini")
    return llm

def serper_tool():
    serper = GoogleSerperAPIWrapper(k=10, g1="us",type="search")
    return  Tool(name="search", func=serper.run, description="Useful for when you need more information from an online search")