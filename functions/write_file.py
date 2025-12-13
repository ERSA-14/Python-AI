from google.genai import types

def write_file(working_directory , file_path , content):
    import os
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f"Error: The file {file_path} is outside the working directory {working_directory}."
    
    parent_dir = os.path.dirname(abs_file_path)
    
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Error occurred while creating {parent_dir}: {e}"

    try:
        with open(abs_file_path, 'w') as file:
            file.write(content)
        return f"File written successfully to {abs_file_path} with {len(content)} characters."
    except Exception as e:
        return f"Error occurred while writing to {abs_file_path}: {e}"



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file if it doesn't exists (and creates the parent directory safely), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, from the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file as a string.",
            ),
        },
    ),
)
    