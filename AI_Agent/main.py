import os
import sys
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from prompts import *
from call_function import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    # Gets input info
    args = []
    verbose = "--verbose" in sys.argv
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_input = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]

    # Sends input info through gemini
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    # Output
    if verbose:
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls:
        function_responses = []
        for function in response.function_calls:
            result = call_function(function, verbose)
            if(
                not result.parts
                or not result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])
        if not function_responses:
            raise Exception("Expected function response structure not found")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
