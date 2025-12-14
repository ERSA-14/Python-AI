# Python AI Agent

A lightweight, autonomous AI agent powered by **Google Gemini 2.5 Flash**. This tool allows you to interact with your local file system, execute code, and perform complex tasks using natural language prompts.

## 🚀 Features

*   **Autonomous Task Execution**: Break down user prompts into actionable steps (Plan, execute, observe, correct).
*   **File System Operations**:
    *   `get_files_info`: List files and directories to understand project structure.
    *   `get_file_content`: Read the contents of any text-based file.
    *   `write_file`: Create new files or overwrite existing ones.
*   **Code Execution**:
    *   `run_file`: Execute Python scripts directly in the environment and capture output.
*   **Smart Context**: Uses a system prompt to enforce developer-like behavior ("Fix bugs", "Analyze code", "Create features").

## 📂 Project Structure

```text
.
├── main.py                  # Entry point: Handles the chat loop, Gemini API connection, and response parsing.
├── call_function.py         # Tool Dispatcher: Maps API tool calls to local Python functions.
├── functions/               # Tool Definitions:
│   ├── get_files_info.py    # Lists directory contents.
│   ├── get_file_content.py  # Reads file content.
│   ├── write_file.py        # Writes to files.
│   └── run_file.py          # Runs Python scripts.
├── calculator/              # Default working directory for the agent's operations.
└── .env                     # Configuration file for API keys.
```

## 🛠️ Usage

This project uses `uv` for dependency management (or standard python).

### 1. Setup
Ensure you have a `.env` file with your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

### 2. Run the Agent
Execute the agent by passing your prompt as an argument:

```bash
# Using uv (recommended)
uv run main.py "Create a python script that calculates Fibonacci numbers"

# Or using standard python
python main.py "Check the current directory and list all .py files"
```

### 3. Developer Mode
The agent has a flag (in code) or specific behavior to act as a developer. By default, it follows the system prompt in `main.py` to act as a helpful coding assistant.

## ⚙️ Configuration

*   **Working Directory**: Currently, the agent is configured to operate within the `calculator/` directory by default. You can change this in `call_function.py`:
    ```python
    # call_function.py
    working_directory = "calculator" # Change this to "." for root or any other path
    ```

## 🧠 Model

The agent acts as a loop:
1.  **User Prompt** -> **Gemini API**
2.  **Gemini** decides if it needs to call a tool (e.g., `read_file`).
3.  **Local Runtime** executes the tool and returns the result.
4.  **Gemini** uses the result to formulate the final answer or take the next step.
