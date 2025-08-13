import os
import sys
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from prompts import *
from call_function import *
from functions.config import MAX_ITERS




def main():
    # Gets input info
    load_dotenv()
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

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_input = " ".join(args)

    if verbose:
        print(f"User prompt: {user_input}")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]
    try:
        for i in range (MAX_ITERS):
            has_txt = generate_content(client, messages, verbose)
            if has_txt:
                print("Final response:")
                return has_txt
            if i == 19:
                return f"Maximum iterations reached: {MAX_ITERS}"
    except Exception as e:
        return f"Error generating content: {e}"

def generate_content(client, messages, verbose):
    # Sends input info through gemini
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    # Output
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        return response.text
    
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

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
    
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
