import base64
import re
import subprocess
import time
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

# Explicit allowlist. The agent does not execute arbitrary shell commands.
ACTIONS = {
    "camera": ["explorer.exe", "shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App"],
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "settings": ["explorer.exe", "ms-settings:"],
}

WORKSPACE = Path.home() / "ChatBotAgentWorkspace"
SCREENSHOT_DIR = Path.home() / "Pictures" / "ChatBotScreenshots"

TWO_D_GAME_HTML = r'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Mini Minecraft-Like 2D Game</title>
<style>body{margin:0;background:#222;color:white;font-family:system-ui,sans-serif;text-align:center}canvas{margin-top:20px;border:3px solid #111;image-rendering:pixelated;max-width:95vw}p{margin:8px}</style></head>
<body><h1>Mini Minecraft-Like 2D Game</h1><p>Move with WASD or the arrow keys.</p><canvas id="game" width="800" height="500"></canvas>
<script>
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
const TILE=40,cols=canvas.width/TILE,rows=canvas.height/TILE;
const player={x:10,y:6,size:26,speed:.12},keys=new Set();
addEventListener('keydown',e=>{keys.add(e.key.toLowerCase());if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(e.key.toLowerCase()))e.preventDefault()});
addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));
function update(){if(keys.has('w')||keys.has('arrowup'))player.y-=player.speed;if(keys.has('s')||keys.has('arrowdown'))player.y+=player.speed;if(keys.has('a')||keys.has('arrowleft'))player.x-=player.speed;if(keys.has('d')||keys.has('arrowright'))player.x+=player.speed;player.x=Math.max(0,Math.min(cols-1,player.x));player.y=Math.max(0,Math.min(rows-1,player.y))}
function drawGround(){for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){ctx.fillStyle=(x+y)%2===0?'#55a83b':'#4a9635';ctx.fillRect(x*TILE,y*TILE,TILE,TILE);ctx.strokeStyle='rgba(0,0,0,.10)';ctx.strokeRect(x*TILE,y*TILE,TILE,TILE)}}
function drawPlayer(){const px=player.x*TILE+(TILE-player.size)/2,py=player.y*TILE+(TILE-player.size)/2;ctx.fillStyle='#3b82f6';ctx.fillRect(px,py,player.size,player.size);ctx.fillStyle='#111827';ctx.fillRect(px+6,py+7,5,5);ctx.fillRect(px+15,py+7,5,5)}
function loop(){update();drawGround();drawPlayer();requestAnimationFrame(loop)}loop();
</script></body></html>
'''

HTML_TEMPLATE = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ChatBot HTML Page</title></head><body><h1>Hello from ChatBot!</h1><p>Edit this file and ask the agent to change it.</p></body></html>'''

COMMANDS_TXT = r'''CHATBOT DESKTOP AGENT COMMAND CATEGORIES

FILES
- make a new txt file called notes.txt
- create an html page called test.html
- make a 2D game in a new html file

GAMES
- make a 2D game where I move up down left right
- make a Minecraft-like 2D ground game

APPS
- open my camera
- open notepad
- open calculator
- open file explorer

SCREENSHOTS
- take a screenshot
- open my camera and take a screenshot

CODING / EXPLANATION
- explain this code
- change the player speed to 0.2
- add trees to the game

The agent asks for confirmation before creating files or opening apps.
Created files are kept in the ChatBotAgentWorkspace folder.
'''


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def safe_filename(name: str, default: str) -> str:
    name = Path(name.strip().strip('"\'')).name
    name = re.sub(r"[^a-zA-Z0-9._ -]", "_", name)
    return name or default


def requested_filename(text: str, default: str) -> str:
    match = re.search(r"(?:called|named)\s+[\"']?([\w .-]+\.(?:html?|txt))[\"']?", text, re.I)
    return safe_filename(match.group(1), default) if match else default


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


def create_file_from_request(message: str):
    text = normalize(message)
    is_game = "2d game" in text or ("minecraft" in text and "game" in text)
    is_html = "html" in text or "web page" in text or "website" in text
    is_txt = ".txt" in text or "text file" in text
    if not (is_game or is_html or is_txt):
        return None
    if is_game:
        filename, content = requested_filename(message, "2d_game.html"), TWO_D_GAME_HTML
    elif is_html:
        filename, content = requested_filename(message, "new_page.html"), HTML_TEMPLATE
    else:
        filename = requested_filename(message, "notes.txt")
        content = COMMANDS_TXT if "categor" in text or "commands" in text else "Created by ChatBot Desktop Agent.\n"
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    return WORKSPACE / filename, content


def confirmation_window(name: str, command: list[str], screenshot_after: bool = False):
    action_text = f"open {name}" + (" and take a screenshot" if screenshot_after else "")
    after_code = ('python -c "from desktop_agent import take_screenshot; p=take_screenshot(); print(\"Screenshot saved to: \"+str(p))"' if screenshot_after else "")
    script=(f'echo Desktop Agent: You asked to {action_text}. & echo. & choice /C YN /N /M "Do you want to continue? [Y/N] " & if errorlevel 2 (echo Cancelled. & timeout /t 2 >nul & exit /b 0) & echo Opening... & start "" {subprocess.list2cmdline(command)} & timeout /t 2 >nul & {after_code} & echo. & echo Done. & timeout /t 3 >nul')
    subprocess.Popen(["cmd.exe","/c",script],creationflags=subprocess.CREATE_NEW_CONSOLE)


def file_confirmation(path: Path, content: str):
    encoded=base64.b64encode(content.encode('utf-8')).decode('ascii')
    escaped=str(path).replace("'","''")
    script=(f'echo Desktop Agent: You asked to create {path.name}. & echo. & choice /C YN /N /M "Create this file? [Y/N] " & if errorlevel 2 (echo Cancelled. & timeout /t 2 >nul & exit /b 0) & powershell -NoProfile -Command "$b=[Convert]::FromBase64String(\'{encoded}\'); [IO.File]::WriteAllBytes(\'{escaped}\',$b)" & echo Created: {path} & timeout /t 4 >nul')
    subprocess.Popen(["cmd.exe","/c",script],creationflags=subprocess.CREATE_NEW_CONSOLE)


@app.post("/api/desktop/create")
def desktop_create():
    message=str((request.get_json(silent=True) or {}).get("message","")).strip()
    result=create_file_from_request(message)
    if not result:
        return jsonify({"ok":False,"message":"I can currently create HTML, TXT, and the built-in 2D game template."}),400
    path,content=result
    file_confirmation(path,content)
    return jsonify({"ok":True,"message":f"A confirmation window was opened to create {path.name} in {WORKSPACE}."})


@app.post("/api/desktop/open")
def desktop_open():
    message=str((request.get_json(silent=True) or {}).get("message","")).strip(); normalized=normalize(message)
    if normalized in {"open camera and take a screenshot","open my camera and take a screenshot","launch camera and take a screenshot","start camera and take a screenshot"}:
        confirmation_window("camera",ACTIONS["camera"],True); return jsonify({"ok":True,"message":"A confirmation window was opened for the camera + screenshot action."})
    if normalized in {"take a screenshot","take screenshot","screenshot","capture my screen"}:
        script=('echo Desktop Agent: You asked to take a screenshot. & echo. & choice /C YN /N /M "Do you want to take a screenshot? [Y/N] " & if errorlevel 2 (echo Cancelled. & timeout /t 2 >nul & exit /b 0) & python -c "from desktop_agent import take_screenshot; p=take_screenshot(); print(\"Saved: \"+str(p))" & timeout /t 4 >nul')
        subprocess.Popen(["cmd.exe","/c",script],creationflags=subprocess.CREATE_NEW_CONSOLE); return jsonify({"ok":True,"message":"A confirmation window was opened for the screenshot."})
    name,command=find_action(message)
    if not name:
        return jsonify({"ok":False,"message":"I don't have a safe action for that yet. Add an explicit action to ACTIONS in desktop_agent.py."}),400
    confirmation_window(name,command); return jsonify({"ok":True,"message":f"A confirmation window was opened for {name}."})


@app.get("/health")
def health():
    return jsonify({"ok":True,"agent":"desktop-agent","workspace":str(WORKSPACE)})


if __name__ == "__main__":
    print("Desktop Agent running on http://127.0.0.1:5050")
    print("Keep this window open while you use the desktop agent.")
    app.run(host="127.0.0.1",port=5050,debug=False)
