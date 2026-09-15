import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

SYSTEM_PROMPT = "You are ChatBot, a helpful, friendly assistant. Keep answers clear and useful."
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
DESKTOP_AGENT_URL = os.getenv("DESKTOP_AGENT_URL", "http://127.0.0.1:5050")


def fallback_reply(message: str) -> str:
    text = message.lower().strip()
    if text in {"hi", "hello", "hey"}:
        return "Hello! I'm ChatBot. How can I help you?"
    if "your name" in text:
        return "I'm ChatBot, your assistant."
    return "Your free local AI is not running yet. Install Ollama, download the model, and start it. See the README for the steps."


def ollama_reply(message: str) -> str | None:
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json={"model": OLLAMA_MODEL, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message}], "stream": False}, timeout=120)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "").strip() or None
    except requests.RequestException:
        return None


def desktop_request(endpoint: str, message: str) -> str | None:
    try:
        response = requests.post(f"{DESKTOP_AGENT_URL}{endpoint}", json={"message": message}, timeout=3)
        if response.ok:
            return response.json().get("message")
    except requests.RequestException:
        pass
    return None


def desktop_command(message: str) -> str | None:
    text = message.lower().strip()
    if text.startswith(("open ", "launch ", "start ")):
        return desktop_request("/api/desktop/open", message)
    return None


def file_command(message: str) -> str | None:
    text = message.lower().strip()
    triggers = ("make a new file", "create a new file", "make a file", "create a file", "make a new html", "make a new txt", "create an html", "create a txt", "make a 2d game", "create a 2d game")
    if text.startswith(triggers) or "minecraft-like 2d" in text:
        return desktop_request("/api/desktop/create", message)
    return None


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    browser_api_key = request.headers.get("X-OpenAI-API-Key", "").strip()

    if not message:
        return jsonify({"error": "Message is required."}), 400

    action_result = desktop_command(message) or file_command(message)
    if action_result:
        return jsonify({"reply": action_result, "mode": "desktop-agent"})

    api_key = browser_api_key or os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.responses.create(model=os.getenv("OPENAI_MODEL", "gpt-5-mini"), instructions=SYSTEM_PROMPT, input=message)
            return jsonify({"reply": response.output_text, "mode": "openai"})
        except Exception:
            app.logger.exception("OpenAI request failed; trying local Ollama")

    reply = ollama_reply(message)
    if reply:
        return jsonify({"reply": reply, "mode": "local"})

    return jsonify({"reply": fallback_reply(message), "mode": "demo"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
