import os
import time
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found. Make sure it's set in your .env file.")

client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

if args.verbose:
    print(f"User prompt: {args.user_prompt}")

for _ in range(20):
    response = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    temperature=0
                ),
            )
            break
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                raise e

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        print(f"Final response:\n{response.text}")
        break

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)

        if not function_call_result.parts:
            raise Exception("No parts in function call result")

        if function_call_result.parts[0].function_response is None:
            raise Exception("No function response in parts")

        if function_call_result.parts[0].function_response.response is None:
            raise Exception("No response in function response")

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))
else:
    print("Error: Maximum iterations reached without a final response.")
    exit(1)
