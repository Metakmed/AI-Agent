import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file in a specified directory relative to the working directory, while also providing other details like the returncode, standard output and standard error",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to file location, relative to the working directory",
                },
                "args":{
                    "type": "array",
                    "description": "An optional list of items of which are strings",
                }
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_target_dir = os.path.commonpath([abs_working_directory, target_file_path]) == os.path.abspath(working_directory)
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file_path.endswith("py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file_path]
    if args:
        command.extend(args)

    try:
        process = subprocess.run(args=command, cwd=abs_working_directory,capture_output=True,text=True,timeout=30)
        result: str = ""
        if process.returncode != 0:
            result += f"Process exited with code {process.returncode}"
        if not process.stderr and not process.stdout:
            result += "No output produced"
            return result
        result += f"STDOUT: {process.stdout}STDERR:{process.stderr}"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
