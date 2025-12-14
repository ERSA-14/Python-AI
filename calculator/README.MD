'''# Directory Summary

This project provides a set of tools for managing files and executing Python scripts within the current working directory.

## Capabilities

*   **File and Directory Management:**
    *   List files and directories: View the contents of any directory using `get_files_info`.
    *   Read file content: Access the content of any file using `get_file_content`.
    *   Write to files: Create new files or update existing ones with specified content using `write_file`.
*   **Code Execution:**
    *   Run Python files: Execute Python scripts and capture their output using `run_file`.

## Features

*   **`get_files_info(directory: str | None = None)`**: Lists files in the specified directory relative to the working directory. If no directory is provided, it lists files in the working directory itself.
*   **`get_file_content(file_path: str | None = None)`**: Gets the content of a file as a string, relative to the working directory.
*   **`run_file(args: list[str] | None = None, file_path: str | None = None)`**: Runs a Python file with the Python interpreter. Accepts additional CLI arguments.
*   **`write_file(content: str | None = None, file_path: str | None = None)`**: Overwrites an existing file or writes to a new file if it doesn't exist. It also safely creates the parent directory if needed.
'''