import subprocess
import time
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

# Explicit allowlist: the agent does not execute arbitrary shell commands.
ACTIONS = {
    "camera": ["explorer.exe", "shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App"],
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "settings": ["explorer.exe", "ms-settings:"],
}

SCREENSHOT_DIR = Path.home() / "Pictures" / "ChatBotScreenshots"


def normalize(text: str) -> str:
    text = " ".join(text.lower().strip().split())
    replacements = {
        "open my camera": "open camera",
        "launch my camera": "launch camera",
        "start my camera": "start camera",
        "please open my camera": "open camera",
        "please open camera": "open camera",
    }
    return replacements.get(text, text)


def find_action(text: str):
    text = normalize(text)
    for name in sorted(ACTIONS, key=len, reverse=True):
        if text in {f"open {name}", f"launch {name}", f"start {name}", name}:
            return name, ACTIONS[name]
    return None, None


def take_screenshot() -> Path:
    from PIL import ImageGrab

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SCREENSHOT_DIR / time.strftime("screenshot_%Y%m%d_%H%M%S.png")
    ImageGrab.grab().save(path)
    return path


def confirmation_window(name: str, command: list[str], screenshot_after: bool = False):
    action_text = f"open {name}" + (" and take a screenshot" if screenshot_after else "")
    if screenshot_after:
        after_code = (
            'python -c "from desktop_agent import take_screenshot; '
            'p=take_screenshot(); print(\"Screenshot saved to: \"+str(p))"'
        )
    else:
        after_code = ""

    script = (
        f'echo Desktop Agent: You asked to {action_text}. & '
        'echo. & '
        'choice /C YN /N /M "Do you want to continue? [Y/N] " & '
        'if errorlevel 2 (echo Cancelled. & timeout /t 2 >nul & exit /b 0) & '
        'echo Opening... & '
        f'start "" {subprocess.list2cmdline(command)} & '
        'timeout /t 2 >nul & '
        f'{after_code} & '
        'echo. & echo Done. & timeout /t 3 >nul'
    )
    subprocess.Popen(["cmd.exe", "/c", script], creationflags=subprocess.CREATE_NEW_CONSOLE)


@app.post("/api/desktop/open")
def desktop_open():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    normalized = normalize(message)

    if normalized in {
        "open camera and take a screenshot",
        "open my camera and take a screenshot",
        "launch camera and take a screenshot",
        "start camera and take a screenshot",
    }:
        confirmation_window("camera", ACTIONS["camera"], screenshot_after=True)
        return jsonify({"ok": True, "message": "A confirmation window was opened for the camera + screenshot action."})

    if normalized in {"take a screenshot", "take screenshot", "screenshot", "capture my screen"}:
        script = (
            'echo Desktop Agent: You asked to take a screenshot. & '
            'echo. & '
            'choice /C YN /N /M "Do you want to take a screenshot? [Y/N] " & '
            'if errorlevel 2 (echo Cancelled. & timeout /t 2 >nul & exit /b 0) & '
            'python -c "from desktop_agent import take_screenshot; p=take_screenshot(); print(\"Saved: \"+str(p))" & '
            'timeout /t 4 >nul'
        )
        subprocess.Popen(["cmd.exe", "/c", script], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return jsonify({"ok": True, "message": "A confirmation window was opened for the screenshot."})

    name, command = find_action(message)
    if not name:
        return jsonify({
            "ok": False,
            "message": "I don't have a safe action for that yet. Add an explicit action to ACTIONS in desktop_agent.py."
        }), 400

    confirmation_window(name, command)
    return jsonify({"ok": True, "message": f"A confirmation window was opened for {name}."})


@app.get("/health")
def health():
    return jsonify({"ok": True, "agent": "desktop-agent"})


if __name__ == "__main__":
    print("Desktop Agent running on http://127.0.0.1:5050")
    print("Keep this window open while you use the desktop agent.")
    app.run(host="127.0.0.1", port=5050, debug=False)
