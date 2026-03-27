import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function


def main():
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("could not fetch API key")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    for _ in range(20):
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("failed API request")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_responses = []

            for function_call in response.function_calls:
                result = call_function(function_call)
                if not result.parts:
                    raise Exception("Error: Empty parts list")
                elif not result.parts[0].function_response:
                    raise Exception("Error: Function response not found in parts list")
                elif not result.parts[0].function_response.response:
                    raise Exception("Error: No response found in the function response")

                function_responses.append(result.parts[0])

            messages.append(types.Content(role="user", parts=function_responses))

            if args.verbose:
                # print(f"User prompt: {args.user_prompt}")
                # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print(f"-> {result.parts[0].function_response.response}")

        else:
            print(response.text)
            break

    if response.function_calls:
        print(
            "Error: Model reached maximum feedback loop without finalising a response"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
