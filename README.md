# ChatBot

A simple Flask web chatbot with optional OpenAI API integration.

## Features
- Clean browser chat interface
- `/api/chat` JSON endpoint
- OpenAI Responses API integration when `OPENAI_API_KEY` is configured
- Local demo replies when no API key is configured
- Secrets kept out of Git with `.gitignore`

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Set your API key as an environment variable:

**Windows PowerShell**
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

**macOS/Linux**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

Start the app:

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

Never commit a real API key. Use environment variables or your deployment platform's secret manager.
