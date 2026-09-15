import os
import subprocess
import sys
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

# Safe, explicit actions. Add more entries here as you want the agent to support them.
ACTIONS = {
    "camera": ["explorer.exe", "shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App"],
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "settings": ["explorer.exe", "ms-settings:"],
}


def find_action(text: str):
    text = text.lower().strip()
    for name in sorted(ACTIONS, key=len, reverse=True):
        if text in {f"open {name}", f"launch {name}", f"start {name}", name}:
            return name, ACTIONS[name]
    return None, None


def confirmation_window(name: str, command: list[str]):
    # Open a separate Windows Command Prompt so the confirmation is obvious.
    script = (
        f'echo Desktop Agent: You asked to open {name}. & '
        'echo. & '
        'choice /C YN /N /M "Do you want to open it? [Y/N] " & '
        'if errorlevel 2 (echo Cancelled. & timeout /t 2 >nul & exit /b 0) & '
        'echo Opening... & '
        f'start "" {subprocess.list2cmdline(command)} & '
        'timeout /t 2 >nul'
    )
    subprocess.Popen(["cmd.exe", "/c", script], creationflags=subprocess.CREATE_NEW_CONSOLE)


@app.post("/api/desktop/open")
def desktop_open():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    name, command = find_action(message)

    if not name:
        return jsonify({
            "ok": False,
            "message": "I don't have a safe action for that yet. Add it to ACTIONS in desktop_agent.py."
        }), 400

    confirmation_window(name, command)
    return jsonify({
        "ok": True,
        "message": f"A confirmation window was opened for {name}."
    })


@app.get("/health")
def health():
    return jsonify({"ok": True, "agent": "desktop-agent"})


if __name__ == "__main__":
    print("Desktop Agent running on http://127.0.0.1:5050")
    print("Keep this window open while you use the desktop agent.")
    app.run(host="127.0.0.1", port=5050, debug=False)
