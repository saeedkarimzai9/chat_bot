# ChatBot

A simple Flask web chatbot with optional OpenAI API integration and a free local AI mode powered by Ollama.

## Features
- Clean browser chat interface
- `/api/chat` JSON endpoint
- OpenAI Responses API integration when an API key is supplied
- Free local AI fallback through Ollama
- Demo replies if neither AI service is available
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

### Free local AI (no OpenAI money required)

Install Ollama on your computer, then download a model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running. The chatbot will automatically use it when an OpenAI key is unavailable or an OpenAI request fails.

If your computer has limited RAM, a smaller Ollama model can be used by setting `OLLAMA_MODEL` in `.env`.

### Optional OpenAI mode

You can still use an OpenAI API key if you have active API billing. Never commit a real API key.

Start the app:

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

The free local AI keeps the model on your computer and does not require OpenAI API credits.
