from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import Tool, AgentExecutor
from langchain.utilities.serpapi import SerpAPIWrapper
from dotenv import load_dotenv
load_dotenv()

search = SerpAPIWrapper(params = {
    "engine": "google",
    "google_domain": "google.com",
    "gl": "tw",    # location
    "hl": "zh-TW", # language
})

tools = [
    Tool(
        name="Google_Search",
        func=search.run,
        description= (
            "Use this when you need to answer questions about current events or something you don't know."
        )
    )
]
# prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_openai_functions_agent(llm, tools)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
result1 = agent_executor.invoke({"input": "hi"})
result = result1["output"]
print(result)