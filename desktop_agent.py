import os
import subprocess
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

app = Flask(__name__)

WORKSPACE = Path.home() / "ChatBotAgentWorkspace"
SCREENSHOT_DIR = WORKSPACE / "screenshots"
WORKSPACE.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# Only explicitly allowlisted Windows apps can be opened.
ALLOWED_APPS = {
    "camera": ["explorer.exe", "shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App"],
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "files": ["explorer.exe"],
    "settings": ["explorer.exe", "ms-settings:"],
}


def safe_path(relative_path: str) -> Path:
    """Resolve a path and keep it inside the agent workspace."""
    raw = str(relative_path).strip().replace("\\", "/")
    if not raw or raw.startswith("/") or ":" in raw:
        raise ValueError("Only relative workspace paths are allowed.")
    target = (WORKSPACE / raw).resolve()
    workspace = WORKSPACE.resolve()
    if target != workspace and workspace not in target.parents:
        raise ValueError("Path must stay inside the agent workspace.")
    return target


def open_allowlisted_app(name: str) -> str:
    key = name.lower().strip()
    command = ALLOWED_APPS.get(key)
    if not command:
        raise ValueError("That app is not on the safe allowlist.")
    subprocess.Popen(command, shell=False)
    return f"Opened {name}."


def save_screenshot() -> Path:
    if ImageGrab is None:
        raise RuntimeError("Pillow is required for screenshots. Run: pip install -r requirements.txt")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"screenshot_{timestamp}.png"
    image = ImageGrab.grab()
    image.save(path)
    return path


@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "service": "System 64 Desktop Agent",
        "workspace": str(WORKSPACE),
        "screenshots": str(SCREENSHOT_DIR),
        "allowlisted_apps": sorted(ALLOWED_APPS),
    })


@app.post("/api/open")
def open_app():
    data = request.get_json(silent=True) or {}
    app_name = str(data.get("app", "")).strip()
    if not app_name:
        return jsonify({"error": "App name is required."}), 400

    # The UI/client should ask the user for confirmation before sending this action.
    try:
        message = open_allowlisted_app(app_name)
        return jsonify({"ok": True, "message": message})
    except (OSError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/screenshot")
def screenshot():
    # Screenshot capture is intentionally explicit: the client should request it only
    # after the user has asked for a screenshot and confirmed the action.
    try:
        path = save_screenshot()
        return jsonify({"ok": True, "message": f"Screenshot saved to {path}", "path": str(path)})
    except (OSError, RuntimeError) as exc:
        return jsonify({"error": str(exc)}), 500


@app.post("/api/files/preview")
def preview_files():
    data = request.get_json(silent=True) or {}
    files = data.get("files", [])
    if not isinstance(files, list) or not files:
        return jsonify({"error": "A non-empty files list is required."}), 400

    preview = []
    try:
        for item in files:
            if not isinstance(item, dict):
                raise ValueError("Each file must be an object.")
            path = safe_path(str(item.get("path", "")))
            content = str(item.get("content", ""))
            if len(content.encode("utf-8")) > 2_000_000:
                raise ValueError(f"File is too large: {path.name}")
            preview.append({"path": str(path.relative_to(WORKSPACE)), "bytes": len(content.encode("utf-8"))})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"ok": True, "files": preview, "requires_confirmation": True})


@app.post("/api/files/write")
def write_files():
    data = request.get_json(silent=True) or {}
    if data.get("confirmed") is not True:
        return jsonify({"error": "Explicit confirmation is required."}), 400

    files = data.get("files", [])
    if not isinstance(files, list) or not files:
        return jsonify({"error": "A non-empty files list is required."}), 400

    written = []
    try:
        for item in files:
            if not isinstance(item, dict):
                raise ValueError("Each file must be an object.")
            path = safe_path(str(item.get("path", "")))
            content = str(item.get("content", ""))
            if len(content.encode("utf-8")) > 2_000_000:
                raise ValueError(f"File is too large: {path.name}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written.append(str(path.relative_to(WORKSPACE)))
    except (OSError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"ok": True, "written": written})


if __name__ == "__main__":
    # Local-only server; it is not exposed to the network.
    app.run(host="127.0.0.1", port=5050, debug=False)
