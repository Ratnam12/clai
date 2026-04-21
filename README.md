# 🤖 CLAI — AI Coding Agent

> An autonomous AI coding agent powered by Google Gemini that can explore codebases, read & write files, run Python, and fix bugs — all on its own.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20API-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Overview

CLAI is a Python-based AI agent that takes a natural language prompt and autonomously completes coding tasks by calling tools in a feedback loop — just like a junior developer who can read code, make changes, run tests, and report back.

**Example — Build a complete REST API from scratch:**
```bash
uv run main.py "Build a REST API for a todo app with endpoints to create, read, \
update, and delete tasks. Store data in a JSON file. Write a test file covering \
all endpoints, run the tests, fix any failures automatically, and show me the results."
```

The agent will:
- 🔍 Explore the existing project structure
- 📖 Read relevant files to understand the codebase
- 🔧 Write multiple new Python files from scratch
- ✅ Run the tests — fix any failures automatically and re-run
- 💬 Report back with a final summary of everything it did

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

### 🟢 Beginner — Ask questions about your code
```bash
# Explore the codebase
uv run main.py "what files are in my project and what does each one do?"

# Understand how something works
uv run main.py "explain how the authentication system works in this project"

# Read a specific file
uv run main.py "read the contents of app.py and summarise what it does"

# Run existing tests
uv run main.py "run the tests and tell me if anything is failing"
```

### 🟡 Intermediate — Fix bugs and make changes
```bash
# Autonomously find and fix a bug
uv run main.py "Users are getting a 500 error when they submit the login form. Find and fix the bug."

# Add a new feature
uv run main.py "Add input validation to the signup form — email must be valid, password must be at least 8 characters"

# Write tests for existing code
uv run main.py "Write 10 test cases for the user authentication module covering edge cases"
```

### 🔴 Advanced — Build entire features from scratch
```bash
uv run main.py "Build a complete URL shortener from scratch. \
1) Explore the existing project structure first. \
2) Create shortener.py with functions to shorten URLs, store mappings in a JSON file, \
and resolve short URLs back to the original. \
3) Create a CLI in main.py that accepts a URL and returns the shortened version. \
4) Create test_shortener.py with at least 15 test cases covering: shortening, \
resolving, duplicate URLs, invalid URLs, and missing keys. \
5) Run the tests — fix any failures automatically and re-run until all pass. \
6) Show me the final test results and a summary of what was built."
```

> 💬 Use `--verbose` to see every function call and result in real time:
> ```bash
> uv run main.py "explain how the authentication system works" --verbose
> ```

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
└── clai_created_projects/           # Sample project for the agent
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

- All tools are **sandboxed** to `./clai_created_projects` — the agent cannot access anything outside
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
