# ChatBot Desktop Agent / System 64

A lightweight local desktop assistant built around Ollama for Windows 11.

## What you need to download/install — NOW

You only need these things:

1. **Python 3.11+** — required to run the app.
2. **Ollama** — required for the local AI model. You already have Ollama installed.
3. **One Ollama model** — use the coding model you already downloaded, such as `qwen2.5-coder`. Do not download another model unless your installed model is missing.
4. **Python packages** — run `setup_system64.bat`; it installs the packages listed in `requirements.txt`.
5. **One small Vosk English speech model** — required only for the offline wake phrase `System 64, wake up`. Put it in `models/vosk-model-small-en-us`.

There is no paid API and no cloud speech-recognition service in this project.

## Important: the one thing that cannot be bundled here

The Vosk speech model is model data rather than Python code, so it is intentionally not stored in this GitHub repository. Download the small English Vosk model once and keep the extracted folder at:

`models/vosk-model-small-en-us`

After that, you should not need another speech-model download.

## Easy setup

1. Download/clone this repository to your PC.
2. Put the Vosk model folder at `models/vosk-model-small-en-us`.
3. Double-click `setup_system64.bat` once. It installs the Python packages and checks Python/Ollama.
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

Check that the extracted model folder exists exactly here:

`models/vosk-model-small-en-us`

Do not put the ZIP file there; extract the model folder first.

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
