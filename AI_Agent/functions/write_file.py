import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    
    if not os.path.exists(file_path_abs):
        try:
            os.makedirs(os.path.abspath(os.path.dirname(file_path)))
        except Exception as e:
            return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(file_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file: {e}'