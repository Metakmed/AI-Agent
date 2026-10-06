import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Opens and writes to a file in a specified directory relative to the working directory, while confirming the location completed and the length of the content added in characters written",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to file location, relative to the working directory",
                },
                "content":{
                    "type": "string",
                    "description": "The string value of what is being written to the desired file"
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_file_path = os.path.commonpath([abs_working_directory, target_file_path]) == os.path.abspath(working_directory)
    if not valid_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    parent_directory = os.path.dirname(target_file_path)
    os.makedirs(parent_directory,exist_ok=True)

    try:
        with open(target_file_path, "w") as f :
            f.write(content)
        return f'Successfully wrote to "{target_file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
