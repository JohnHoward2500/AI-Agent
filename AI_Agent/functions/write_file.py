import os
from google.genai import types # type: ignore

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    
    if not os.path.exists(file_path_abs):
        try:
            os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        except Exception as e:
            return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(file_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="If the file in the file_path exists it writes what is passed in the content argument to that file.  If the file path does not exist it creates a new file in that path.  Constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="what is going to be written inside the file in file_path",
            )
        },
        required=["file_path", "content"]
    )
)