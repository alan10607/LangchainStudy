from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import Tool, AgentExecutor
from langchain.utilities.serpapi import SerpAPIWrapper

class ChatAI:
    def __init__(self):
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
        # Get the prompt to use - you can modify this!
        prompt = hub.pull("hwchase17/openai-functions-agent")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        # search = TavilySearchResults()
        # tools = [search]
        agent = create_openai_functions_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        



    def run(self, message):
        result = self.agent_executor.invoke({"input": message})
        print(result)
        return result["output"]
    

if __name__ == "__main__":
    ai = ChatAI()

    print("Type 'quit' to quit chat")
    while True:
        question = input("Question >>> ")
        if question.lower() == "quit":
            print("Quit chat...")
            break
        
        result = ai.run(question)
        print(f"Answer >>>  {result}")
        print("-----------------\n")
