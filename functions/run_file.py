from google.genai import types


def run_file(working_directory: str, file_path: str, args = []):
    import os
    import subprocess
    import sys
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f"Error: The file {file_path} is outside the working directory {working_directory}."
    if not os.path.exists(abs_file_path):
        return f"Error: The file {file_path} does not exist."
    if not os.path.isfile(abs_file_path):
        return f"Error: The file {file_path} is not a file."
    if not file_path.endswith(".py"):
        return f"Error: The file {file_path} is not a python file."
    try:
        final_args = [sys.executable, abs_file_path] + args
        output = subprocess.run(
            final_args,
            timeout=25,
            cwd=working_directory,
            capture_output=True,
            text=True
        )
        if output.stdout == "" and output.stderr == "":
            return "File executed successfully, but no output was produced."    
        
        if output.returncode != 0:
            return f"Stdout: {output.stdout}\nStderr: {output.stderr}\nFile execution failed with return code {output.returncode}."
        else:
            return f"Stdout: {output.stdout}\nStderr: {output.stderr}\nFile executed successfully."
    
    except Exception as e:
        return f"Error occurred while executing python file: {e}"



schema_run_file = types.FunctionDeclaration(
    name="run_file",
    description="Runs a python file with python interpreter. Aceepts addditional CLI args as an optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run ,relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as the CLI args for the python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)