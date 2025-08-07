import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

user_input = sys.argv[1:][0]
verbose = None
if len(sys.argv) >= 3:
    verbose = sys.argv[2:][0]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_input)])
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model = 'gemini-2.0-flash-001',
    contents = messages
)
if verbose:
    print(f"User prompt: {user_input}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)
