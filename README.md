# 🤖 CLAI — AI Coding Agent

> An autonomous AI coding agent powered by Google Gemini that can explore codebases, read & write files, run Python, and fix bugs — all on its own.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20API-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Overview

CLAI is a Python-based AI agent that takes a natural language prompt and autonomously completes coding tasks by calling tools in a feedback loop — just like a junior developer who can read code, make changes, run tests, and report back.

**Example:**
```bash
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20"
```

The agent will:
- 🔍 Explore the project files
- 📖 Read the relevant source code
- 🔧 Identify and fix the bug
- ✅ Run tests to verify the fix
- 💬 Report back with a final response

---

## ⚡ Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/Ratnam12/clai.git
cd clai
```

**2. Install dependencies**
```bash
uv sync
```

**3. Add your Gemini API key**
```bash
# Create a .env file in the root
GEMINI_API_KEY=your_api_key_here
```

**4. Run the agent**
```bash
uv run main.py "your prompt here"
```

---

## 🛠️ Tools

The agent has access to 4 tools, all sandboxed to the working directory:

| Tool | Description |
|------|-------------|
| `get_files_info` | Lists files and folders with name, size, and type |
| `get_file_content` | Reads file contents (up to 10,000 characters) |
| `write_file` | Writes or overwrites a file with new content |
| `run_python_file` | Executes a Python file with optional arguments |

---

## 💡 Example Prompts

```bash
# Explore the codebase
uv run main.py "what files are in the calculator directory?"

# Read a file
uv run main.py "read the contents of calculator/main.py"

# Run tests
uv run main.py "run the tests in calculator/tests.py"

# Fix a bug autonomously
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20"

# Verbose mode (see every function call)
uv run main.py "how does the calculator work?" --verbose
```

---

## 🏗️ Project Structure

```
clai/
├── main.py               # Agent loop — entry point
├── prompts.py            # System prompt for Gemini
├── call_function.py      # Dispatches function calls
├── config.py             # Configuration (MAX_CHARS, etc.)
├── functions/            # Agent tools
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
└── calculator/           # Sample project for the agent
    ├── main.py
    ├── tests.py
    └── pkg/
        ├── calculator.py
        └── render.py
```

---

## 🔄 How the Agent Loop Works

```
You give a prompt
        ↓
Gemini decides which tool to call
        ↓
Tool runs → result returned to Gemini
        ↓
Gemini decides what to do next
        ↓
Repeats up to 20 iterations
        ↓
Gemini gives a final response
```

The full conversation history (prompts, tool calls, results) is passed to Gemini on every iteration so it always has full context.

---

## 🔒 Security

- All tools are **sandboxed** to `./calculator` — the agent cannot access anything outside
- API key stored in `.env`, excluded from git via `.gitignore`
- Python execution has a **30-second timeout**
- Agent is limited to **20 iterations** per task to prevent runaway loops

---

## 🧰 Built With

- [Python 3.11+](https://www.python.org/)
- [Google Gemini API](https://ai.google.dev/)
- [uv](https://github.com/astral-sh/uv) — fast Python package manager
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 👤 Author

**Ratnam Singh**
- GitHub: [@Ratnam12](https://github.com/Ratnam12)
