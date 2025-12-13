import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions import get_files_info
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_file import schema_run_file
from functions.write_file import schema_write_file


def main():
    load_dotenv()
    
    api = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of file
- Run a python file with optional arguments
- Write to file (create or update)

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    
    is_developer = False

    if len(sys.argv) < 2:
        print("need a prompt, for context")
        sys.exit(1)


    if len(sys.argv) > 2 and sys.argv[2] == "--developer":
        is_developer = True
    
    user_prompt = sys.argv[1]
    message = [types.Content(role="user",parts=[types.Part(text=user_prompt)]),]
    
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info,schema_get_file_content,schema_run_file,schema_write_file],
)    
    configi=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config = configi
        )


        if response is None or response.usage_metadata is None:
            print("response doesnt exists or is malformed")
            return

        if is_developer:
            print(f"User prompt : {user_prompt}")
            print(f"Prompt token count : {response.usage_metadata.prompt_token_count}")
            print(f"Response token count : {response.usage_metadata.candidates_token_count}")
         
        if response.function_calls:
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})\n")    
        print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

main()
