import os


def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir])
        if valid_target_dir != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        result = ""
        for item in os.path.listdir(target_dir):
            result += f"- {item}: file_size={os.path.getsize(os.path.join(target_dir, item))}, is_dir={os.path.isdir(os.path.join(target_dir, item))}\n"
    except Exception as e:
        return f"Error: {e}"
