# ChatBot Desktop Agent / System 64

A lightweight local desktop assistant built around Ollama for Windows 11.

## What you need to download/install — NOW

You only need these things:

1. **Python 3.11+** — required to run the app.
2. **Ollama** — required for the local AI model. You already have Ollama installed.
3. **One Ollama model** — use the coding model you already downloaded, such as `qwen2.5-coder`. Do not download another model unless your installed model is missing.
4. **Python packages** — run `setup_system64.bat`; it installs the packages listed in `requirements.txt`.
5. **Vosk English speech model** — the current repository already includes the small model at `models/vosk-model-small-en-us`.

There is no paid API and no cloud speech-recognition service in this project.

## Vosk wake-word model

The current repository already contains the small English Vosk model used for the offline wake phrase. After downloading the ZIP from GitHub, keep the folder structure intact so this path exists:

`models/vosk-model-small-en-us`

You do not need to download the Vosk model separately when using the current repository ZIP.

## Easy setup

1. Download/clone this repository to your PC.
2. Keep the included Vosk model at `models/vosk-model-small-en-us`.
3. Double-click `setup_system64.bat` once. It installs the Python packages and checks Python/Ollama/model files.
4. Make sure your Ollama model is installed. You can check with `ollama list`.
5. Double-click `system64_launcher.bat`.
6. The local web interface opens at `http://127.0.0.1:5000`.
7. Say **System 64, wake up** to trigger the local wake listener.

## Current capabilities

- Local chat through Ollama.
- Offline local wake-word detection with Vosk.
- Windows SAPI voice output.
- Open allowlisted Windows apps such as Camera, Notepad, Calculator, File Explorer, and Settings.
- Create/modify files inside the protected `ChatBotAgentWorkspace`.
- Explicit screenshots.
- Visible confirmation before desktop actions and file changes.

## What is NOT enabled yet

System 64 does **not** have unrestricted PC access. It does not secretly record audio, secretly capture screenshots, run arbitrary shell commands, or silently change the whole PC.

A future permission system can add more capabilities only when you explicitly choose them. That is separate from the lightweight setup above.

## Troubleshooting

### `qwen2.5-coder` is not found

Run `ollama list` and use the exact model name shown there. If needed, set `OLLAMA_MODEL` to that name before starting `app.py`.

### Wake phrase says the Vosk model is missing

Check that the extracted repository contains this folder:

`models/vosk-model-small-en-us`

If you downloaded the repository as a ZIP, make sure you extracted the whole ZIP rather than running files from inside the ZIP.

### Python package installation fails

Run `python -m pip install -r requirements.txt` from the repository folder and read the error shown in the window.

## Workspace

Generated files are kept under:

`%USERPROFILE%\ChatBotAgentWorkspace`

## Example requests

- Open my camera.
- Open File Explorer.
- Make a new HTML page.
- Make a 2D game where I can move up, down, left, and right.
- Make a text file containing my command categories.
- Add trees to my game.
- Change the player speed.
- Explain this code.

## Windows Smart App Control

If Windows 11 shows a Smart App Control or Windows security warning when you launch a `.bat` file downloaded from GitHub, that is Windows checking a downloaded script before allowing it to run. Do not disable Smart App Control just for this project. If you trust the repository, extract the ZIP to a normal folder and review the script before running it. You can also run the Python commands manually from Command Prompt instead of using the batch launcher.

