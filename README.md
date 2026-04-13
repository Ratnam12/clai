# CLAI - AI Coding Agent

## Overview
CLAI is a Python-based autonomous AI coding agent powered by the Gemini API. Given a natural language task, the agent explores your codebase, reads and writes files, runs Python code, and iterates until the job is done — all on its own.

## Key Features
The agent includes a feedback loop that continuously calls Gemini, executes tools, and passes results back until it has a final answer. It supports four tools: listing directory contents, reading files, writing files, and executing Python scripts. All tools are sandboxed to a working directory so the agent cannot access anything outside the permitted folder.

## Example Usage
```bash
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20"
uv run main.py "how does the calculator render results to the console?"
uv run main.py "run the tests in tests.py"
uv run main.py "what files are in the pkg directory?" --verbose
```

## Installation
The project requires Python 3.11+ and a Gemini API key. Install dependencies with `uv sync`. Create a `.env` file in the root with `GEMINI_API_KEY=your_key_here`. Run the agent with `uv run main.py "your prompt"`. Use `--verbose` to see each function call and its result.

## Technical Structure
The codebase is organized into focused modules: `main.py` for the agent loop, `prompts.py` for the system prompt, `call_function.py` for dispatching function calls, `config.py` for configuration, and `functions/` for the four tool implementations. The `calculator/` directory serves as a sample project for the agent to work on.

## Security
The agent is sandboxed to the `./calculator` working directory. The Gemini API key is stored in `.env` which is excluded from git via `.gitignore`. Python execution has a 30-second timeout to prevent infinite loops and the agent is limited to 20 iterations per task.

## Architecture
The agent runs a loop up to 20 iterations. Each iteration calls Gemini with the full conversation history, appends the response to the message list, executes any requested tool calls, and appends the results back to the conversation. The loop breaks when Gemini produces a final text response with no further function calls.
