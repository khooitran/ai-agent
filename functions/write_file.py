import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        absolute_working_path = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(
            os.path.join(absolute_working_path, file_path)
        )

        if (
            os.path.commonpath([absolute_file_path, absolute_working_path])
            != absolute_working_path
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(absolute_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)

        with open(absolute_file_path, "w") as f:
            f.write(content)

    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to the file at the target file path in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The target file path relative from the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the target file",
            ),
        },
        required=["file_path", "content"],
    ),
)
