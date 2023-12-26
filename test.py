from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ''
llm = OpenAI(model_name="text-davinci-003",max_tokens=1024)
print(llm("What is elasticsearch?"))
print("end")

