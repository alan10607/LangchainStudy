from langchain.utilities.serpapi import SerpAPIWrapper
from dotenv import load_dotenv
load_dotenv()

search = SerpAPIWrapper(params = {
    "engine": "google",
    "google_domain": "google.com",
    "gl": "tw",    # location
    "hl": "zh-TW", # language
})

def google_search(query):
    print("Google search query:", query)
    result = search.run(query=query)
    print("Get result:", result)
    return result

if __name__ == "__main__":
    while True:
        query = input("google_search >>> ")
        if query.lower() == "quit":
            break
        print(google_search(query))
