from dotenv import load_dotenv
load_dotenv()

import os
import time
import json
from pathlib import Path
from openai import OpenAI
from functions import google_search

TOOL_FUNCTIONS = [google_search]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_assistant_id(name = "Dr. Penguin"):
    assistant_file_path = Path(__file__).parent / "assistant.json"
    old_assistants = []

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, "r") as file:
            old_assistants = json.load(file)
            for assistant_data in old_assistants:
                if assistant_data["name"] == name:
                    assistant_id = assistant_data["id"]
                    print("Assistant id: ", assistant_id)
                    return assistant_id
    
    assistant = create_assistant()
    old_assistants.append(
        {
            "name": assistant.name,
            "id": assistant.id
        }
    )
    with open(assistant_file_path, "w", encoding="utf-8") as file:
        json.dump(old_assistants, file, ensure_ascii = False, indent = 4)
        print(f"Create and save new assistan. Assistant name: {assistant.name}, Assistant id:{assistant.id}")
                
    return assistant.id
    
def create_assistant():
    return client.beta.assistants.create(
        name = "Dr. Penguin",
        instructions = "You are Dr. Penguin, living in Taiwan, loving winter.",
        model = "gpt-4-1106-preview",
        tools = [
            {
                "type": "retrieval"
            },
            {
                "type": "code_interpreter"
            },
            {
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Use this when you need to answer questions about current events or something you don't know. If the user asks a question in a language other than English, respond and query in that language.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The part that you don't know."
                            }
                        },
                        "required": [
                            "query"
                        ]
                    }
                }
            }
        ]
    )



def create_thread():
    thread = client.beta.threads.create()
    print("Thread id: ", thread.id)
    return thread

def run(assistant_id, thread, question):
    # 1. Prepare user question message
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = question
    )

    # 2. Create a new run
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant_id,
    )

    
    while True:
        print("Run status: " + run.status)
        if run.status not in ["queued", "in_progress", "requires_action"]:
            break

        if run.status in ["queued", "in_progress"]:
            # 3. Wait for message retrieval
            run = client.beta.threads.runs.retrieve(
                thread_id = thread.id,
                run_id = run.id
            )
            if run.status == "in_progress":
                time.sleep(1)
            

        elif run.status == "requires_action":
            # 4. Submit tool outputs
            tool_outputs = process_tools(run)

            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id = thread.id,
                run_id = run.id,
                tool_outputs = tool_outputs
            )

        elif run.status == "failed":
            raise Exception("Run Failed. Error: ", run.last_error)
        
            
    # 5. Return the result message
    result = get_message()
    return result

def get_message():
    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )
    return messages.data[0].content[0].text.value or "<no message>"

def process_tools(run):
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []

    for tool_call in tool_calls:
        function = find_matching_function(tool_call.function.name)
        output = execute_function(function, tool_call.function.arguments)

        print(f"{tool_call.function.name}: ", output)

        tool_outputs.append(
            {
                "tool_call_id": tool_call.id,
                "output": json.dumps(output)
            }
        )

    return tool_outputs

def find_matching_function(function_name):
    return next((func for func in TOOL_FUNCTIONS if func.__name__ == function_name))

def execute_function(function, arguments):
    try:
        return function(**eval(arguments))
    except Exception as e:
        return "Execute function error: " + str(e)

# Instantiate OpenAI client
client = OpenAI(api_key = OPENAI_API_KEY, timeout = 600)
assistant_id = get_assistant_id()
thread = create_thread()
if __name__ == "__main__":
    

    print("Type 'quit' to quit chat")
    while True:
        question = input("Question >>> ")
        if question.lower() == "quit":
            print("Quit chat...")
            break
        
        result = run(assistant_id, thread, question)
        print(f"Answer >>>  {result}")
        print("-----------------\n")

