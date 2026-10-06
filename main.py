import os
import sys
import argparse

from config import ITERATIONS
from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


parser = argparse.ArgumentParser(description="Bot-Wilco")
parser.add_argument("user_prompt", type=str, help="inputed user_prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "user", "content": args.user_prompt},
         {"role": "system", "content": system_prompt},
    ]

    def get_response():
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )
        return response

    for _ in range(ITERATIONS):
        response = get_response()
        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(f"Final Response:\n {message.content}")
# Main has no reason to return any value so simply stating return translates to "Im done"
            return
    else:
        print(f"ERROR: Maximum number of {ITERATIONS} reached")
        sys.exit(1)

if __name__ == "__main__":
    main()
