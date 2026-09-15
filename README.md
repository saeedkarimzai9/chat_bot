# ChatBot Desktop Agent

A fresh local chatbot and desktop-agent project built around Ollama.

## What it will do

- Chat with you using a local Ollama model.
- Understand normal-language requests.
- Create files inside a safe workspace.
- Generate HTML, JavaScript, Python, text, and other project files.
- Modify files when you ask for changes.
- Open explicitly requested Windows apps such as Camera, Notepad, Calculator, and File Explorer.
- Take screenshots only when explicitly requested.
- Ask for confirmation before changing files or performing desktop actions.

## Safety

The agent uses an allowlist and a confirmation step. It does not execute arbitrary shell commands or secretly record input.

## Workspace

Generated projects are kept under:

`%USERPROFILE%\\ChatBotAgentWorkspace`

## Start

1. Install Python 3.11+.
2. Install Ollama and download a coding model such as `qwen2.5-coder`.
3. Install dependencies with `pip install -r requirements.txt`.
4. Start the desktop agent with `python desktop_agent.py`.
5. Start the chatbot with `python app.py`.
6. Open `http://127.0.0.1:5000`.

## Example requests

- Open my camera.
- Make a new HTML page.
- Make a 2D game where I can move up, down, left, and right.
- Make a text file containing my command categories.
- Add trees to my game.
- Change the player speed.
- Explain this code.
