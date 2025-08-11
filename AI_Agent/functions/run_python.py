import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_abs = os.path.abspath(working_directory)

    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_path_abs):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python", file_path_abs]
        if args:
            commands.extend(args)
        result = subprocess.run(commands, capture_output=True, timeout=30, text=True, cwd=working_dir_abs)
        output = []
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append(result.stderr)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if output:
            return "\n".join(output)
        return "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file= types.FunctionDeclaration(
    name="run_python_file",
    description="runs the python file in the specified file path.  Has an option to add a list of arguemnts to pass to the specified python file.  Constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="An optional list of arguments that is passed to the file being ran from the file path",
            )
        },
        required=["file_path"],
    )
)