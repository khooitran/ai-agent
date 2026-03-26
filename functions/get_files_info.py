import os


def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir])
        if valid_target_dir != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_info = []
        for item in os.listdir(target_dir):
            if item == "__pycache__":
                continue
            filepath = os.path.join(target_dir, item)
            files_info.append(
                f"- {item}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}"
            )
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(files_info)
