import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_working_path = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(
            os.path.join(absolute_working_path, file_path)
        )

        if (
            os.path.commonpath([absolute_file_path, absolute_working_path])
            != absolute_working_path
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        outputstr = ""
        if result.returncode != 0:
            outputstr += f"Process exited with exit code {result.returncode}"
        if not result.stdout and not result.stderr:
            outputstr += "No output produced"
        outputstr += "STDOUT: " + result.stdout + "\n" + "STDERR: " + result.stderr

    except Exception as e:
        return f"Error: executing Python file: {e}"

    return outputstr + "\n"
