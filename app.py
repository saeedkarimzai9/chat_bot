import os
from flask import Flask, jsonify, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

SYSTEM_PROMPT = "You are ChatBot, a helpful, friendly assistant. Keep answers clear and useful."


def fallback_reply(message: str) -> str:
    text = message.lower().strip()
    if text in {"hi", "hello", "hey"}:
        return "Hello! I'm ChatBot. How can I help you?"
    if "your name" in text:
        return "I'm ChatBot, your assistant."
    return "I'm running in local demo mode. Add OPENAI_API_KEY to your .env file to enable full AI responses."


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Message is required."}), 400

    if client is None:
        return jsonify({"reply": fallback_reply(message)})

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            instructions=SYSTEM_PROMPT,
            input=message,
        )
        return jsonify({"reply": response.output_text})
    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({"error": "Chat service error. Check your API key and server logs."}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
