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

from call_function import call_function

def main():
    load_dotenv()
    
    api = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api)
    system_prompt = """You are a helpful AI coding assistant. Understand user intent and execute their requests systematically.
INTENT INTERPRETATION:
Rule 1: Negative statements indicate bugs that need fixing
Example: "code doesn't work" → fix the code
Example: "getting error" → debug and resolve the error
Rule 2: Analyze what the user wants to accomplish and plan accordingly
AVAILABLE OPERATIONS:
1. List Files and Directories
Display contents of a directory to understand structure
2. Read File Content
Read any text file (Python, JSON, TXT, CSV, etc.)
3. Write to File
Create new files or update existing files (replaces entire content)
4. Run Python File
Execute Python scripts and capture output

RESPONSE FORMAT:
Always structure responses in numbered points:
1. UNDERSTANDING:
What user wants
Task type (fix bug, run code, create file, etc.)
Expected outcome
2. PLAN:
Step 1: [Action needed]
Step 2: [Next action]
Step 3: [Continue]
3. EXECUTION:
[Perform operations]
4. RESULTS:
Under title RESULTS:
What was done
Output or errors
Status
5. NEXT STEPS:
Under title FUTURE STEPS:
Future steps
Recommendations or follow-up actions
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
        max_iteration = 20
        for i in range(0,max_iteration):

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
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
            
            if response.candidates:
                for candidate in response.candidates:
                    if candidate is None or candidate.content is None:
                        continue
                    message.append(candidate.content)

            if response.function_calls:
                for function_call in response.function_calls:
                    results = call_function(function_call,developer=is_developer)
                    message.append(results)
            else:
                print(response.text)
                return
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

main()
