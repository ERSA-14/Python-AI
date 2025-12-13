from google.genai import types

def get_file_content(working_directory , file_path):
    import os
    # Limiting the data , cause i am broke and cant afford gemini bill, want to reach good conclusion using free tier
    # TODO: Remove this limit for enterprise use
    MAX_CHARS = 7500

    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f"Error: The file {file_path} is outside the working directory {working_directory}."
    if not os.path.exists(abs_file_path):
        return f"Error: The file {file_path} does not exist."
    if not os.path.isfile(abs_file_path):
        return f"Error: The file {file_path} is not a file."
    
    file_content = ""
    try:
        with open(abs_file_path, 'r') as file:
            file_content = file.read(MAX_CHARS)
            if len(file_content) >= MAX_CHARS:
                file_content += f"[...File {abs_file_path} is too large to be read in full. Only {MAX_CHARS} characters are shown.]"
        return file_content
    except Exception as e:
        return f"Error occurred while reading file: {str(e)}"



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
        },
    ),
)