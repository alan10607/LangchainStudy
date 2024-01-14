import os
from openai import OpenAI
from langchain.utilities.serpapi import SerpAPIWrapper
# from langchain.utilities.dalle_image_generator import DallEAPIWrapper

class DallE3Wrapper:
    def __init__(self, client):
        self.__client = client

    def run(self, query):
        response = self.__client.images.generate(
            model="dall-e-3",
            prompt=query,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url

class Functions:
    def __init__(self, client):
        self.__serpApi = SerpAPIWrapper(params = {
            "engine": "google",
            "google_domain": "google.com",
            "gl": "tw",    # location
            "hl": "zh-TW", # language
        })


        self.__dalle3Api = DallE3Wrapper(client=client)
    def google_search(self, query):
        return self.__serpApi.run(query=query)
    
    def dalle3_image_generator(self, query):
        return self.__dalle3Api.run(query=query)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=600)
    func = Functions(client)

    print("Type 'quit' to quit chat")
    while True:
        query = input("Query >>> ")
        if query.lower() == "quit":
            break
        print(func.dalle3_image_generator(query))


