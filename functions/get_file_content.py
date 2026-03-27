import os
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        absolute_working_path = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(
            os.path.join(absolute_working_path, file_path)
        )
        if (
            os.path.commonpath([absolute_file_path, absolute_working_path])
            != absolute_working_path
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(absolute_file_path, "r") as f:
            content = f.read(10000)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
    except Exception as e:
        return f"Error: {e}"

    return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens the specified file in the current working directory via file path, with a maximum read capacity of 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The target file path relative from the working directory",
            ),
        },
        required=["file_path"],
    ),
)
