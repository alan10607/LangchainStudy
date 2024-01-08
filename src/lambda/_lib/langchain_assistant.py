from langchain.agents import Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.agents import AgentType
# from langchain.memory import ConversationBufferMemory
from langchain.utilities.serpapi import SerpAPIWrapper

class ChatAI:
    def __init__(self):
        search = SerpAPIWrapper(params={
            "engine": "google",
            "google_domain": "google.com",
            "gl": "tw",    # location
            "hl": "zh-TW",  # language
        })

        tools = [
            Tool(
                name="Google Search",
                func=search.run,
                description="use this when you need to answer questions about current events or something you don't know"
            )
        ]
        # memory = ConversationBufferMemory(memory_key="chat_history")
        llm = OpenAI(temperature=0, max_tokens=2048)

        self.agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

        print("Init AI done!")

    def run(self, message):
        return self.agent.run(message)


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
