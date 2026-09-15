import os
from typing import Any

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder")
DESKTOP_AGENT_URL = os.getenv("DESKTOP_AGENT_URL", "http://127.0.0.1:5050")

SYSTEM_PROMPT = """You are the local ChatBot Desktop Agent assistant.

Help the user with coding, files, games, explanations, and safe desktop tasks.
You may describe actions, but never claim an action was performed unless the local
agent confirms it. Never ask for or expose secrets. Do not provide covert keylogging,
secret recording, stealth screenshots, persistence, or unrestricted shell execution.
For desktop changes, the application will require explicit confirmation before acting.
Keep answers clear and practical for a Windows 11 user.
"""


def ollama_chat(message: str) -> str:
    payload: dict[str, Any] = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return data.get("message", {}).get("content", "No response was returned by Ollama.")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    ollama_ok = False
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
        ollama_ok = response.ok
    except requests.RequestException:
        pass
    return jsonify({"ok": True, "ollama": ollama_ok, "model": OLLAMA_MODEL})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        answer = ollama_chat(message)
        return jsonify({"answer": answer, "model": OLLAMA_MODEL})
    except requests.RequestException as exc:
        return jsonify({
            "error": "Ollama is not reachable. Start Ollama and make sure the model is installed.",
            "details": str(exc),
        }), 503


@app.post("/api/desktop/open")
def desktop_open():
    data = request.get_json(silent=True) or {}
    app_name = str(data.get("app", "")).strip()
    if not app_name:
        return jsonify({"error": "App name is required."}), 400
    try:
        response = requests.post(
            f"{DESKTOP_AGENT_URL}/api/open",
            json={"app": app_name},
            timeout=15,
        )
        return (response.text, response.status_code, {"Content-Type": "application/json"})
    except requests.RequestException as exc:
        return jsonify({"error": "Desktop agent is not running.", "details": str(exc)}), 503


@app.post("/api/desktop/screenshot")
def desktop_screenshot():
    try:
        response = requests.post(f"{DESKTOP_AGENT_URL}/api/screenshot", timeout=30)
        return (response.text, response.status_code, {"Content-Type": "application/json"})
    except requests.RequestException as exc:
        return jsonify({"error": "Desktop agent is not running.", "details": str(exc)}), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
