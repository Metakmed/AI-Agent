from config import MAX_CHARS
import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Opens and reads files up to max character limit in a specified directory relative to the working directory, and if the file was truncated",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to file location, relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_target_dir = os.path.commonpath([abs_working_directory, target_file_path]) == os.path.abspath(working_directory)
    if not valid_target_dir:
        return f'Error: Cannot read "{target_file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{target_file_path}"'

    try:
        with open(target_file_path, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return content
        return content
    except Exception as e:
        return f"Error: {e}"
