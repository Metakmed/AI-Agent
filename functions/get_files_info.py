import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (The default value is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))
    valid_target_dir = os.path.commonpath([abs_working_directory, target_dir]) == abs_working_directory

    file_list = []

    if directory != ".":
        file_list.append(f"Result for '{directory}' directory:")
    else:
        file_list.append("Result for current directory:")

    if not valid_target_dir:
        file_list.append(f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return "\n".join(file_list)

    if not os.path.isdir(target_dir):
        file_list.append(f'   Error: "{directory}" is not a directory')
        return "\n".join(file_list)

    try:
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            file_list.append(f"  - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
    except Exception as e:
        file_list.append(f"   Error: {e}")
        return "\n".join(file_list)

    return "\n".join(file_list)
