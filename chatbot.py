import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

HTML = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chat Bot</title>
<style>
body{font-family:Arial,sans-serif;max-width:760px;margin:40px auto;padding:0 16px;background:#f5f5f5}
#chat{height:55vh;overflow:auto;background:white;padding:18px;border-radius:12px;box-shadow:0 2px 10px #0001}
.msg{margin:10px 0;padding:10px 14px;border-radius:10px;max-width:80%}.user{margin-left:auto;background:#dbeafe}.bot{background:#eee}
form{display:flex;gap:8px;margin-top:12px}input{flex:1;padding:12px;border:1px solid #ccc;border-radius:8px}button{padding:12px 18px;border:0;border-radius:8px;cursor:pointer}
</style></head>
<body><h1>🤖 Chat Bot</h1><div id="chat"></div><form id="form"><input id="message" autocomplete="off" placeholder="Type a message..."><button>Send</button></form>
<script>
const chat=document.getElementById('chat'), input=document.getElementById('message');
function add(text,cls){const d=document.createElement('div');d.className='msg '+cls;d.textContent=text;chat.appendChild(d);chat.scrollTop=chat.scrollHeight}
add('Hello! I am your chatbot. Ask me something!','bot');
document.getElementById('form').addEventListener('submit',async e=>{e.preventDefault();const message=input.value.trim();if(!message)return;add(message,'user');input.value='';const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});const data=await r.json();add(data.reply,'bot')});
</script></body></html>'''

def reply(message):
    text = message.lower().strip()
    if text in {'hi','hello','hey'}:
        return 'Hello! 👋 How can I help you?'
    if 'name' in text:
        return 'I am Chat Bot, running from the chat_bot GitHub repository.'
    if 'help' in text:
        return 'Try saying hello, asking my name, or asking what I can do.'
    if text in {'bye','goodbye'}:
        return 'Goodbye! 👋'
    return 'I received your message: ' + message

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path == '/':
            body = HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != '/chat':
            self.send_error(404)
            return
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length) or b'{}')
        result = json.dumps({'reply': reply(str(data.get('message','')))}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(result)))
        self.end_headers()
        self.wfile.write(result)

    def log_message(self, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), Handler)
    print('Chat Bot running at http://127.0.0.1:8000')
    print('Press Ctrl+C to stop.')
    server.serve_forever()
