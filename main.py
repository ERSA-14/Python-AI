import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    
    api = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api)

    is_developer = False

    if len(sys.argv) < 2:
        print("need a prompt, for context")
        sys.exit(1)

    if len(sys.argv) > 2 and sys.argv[2] == "--developer":
        is_developer = True
    
    user_prompt = sys.argv[1]
    message = [types.Content(role="user",parts=[types.Part(text=user_prompt)]),]    

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message,
    )
    print(response.text)

    if response is None or response.usage_metadata is None:
        print("doesnt exists")
        return
    else:
        pass

    if is_developer:
        print(f"User prompt : {user_prompt}")
        print(f"Prompt token count : {response.usage_metadata.prompt_token_count}")
        print(f"Response token count : {response.usage_metadata.candidates_token_count}")
    else:
        pass

main()