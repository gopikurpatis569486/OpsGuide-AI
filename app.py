from engine import Retriever
from evaluate import evaluate
DEFAULT_PORT = 8001

def get_api(path):
    if path=='/api/runbooks':
        return json.loads((BASE/'data/runbooks.json').read_text())
    if path=='/api/evaluation':
        return evaluate()
    return None

def post_api(path,payload):
    if path!='/api/ask':
        raise ValueError('Unknown endpoint')
    question = str(payload.get('question','')).strip()
    if not question or len(question)>1000:
        raise ValueError('Enter a question of 1-1000 characters')
    return Retriever(get_api('/api/runbooks')).answer(question)

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import threading
from datetime import datetime, timezone

BASE = Path(__file__).parent
LOCK = threading.RLock()
START = datetime.now(timezone.utc)
AUDIT = []

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, value, status=200):
        content = json.dumps(value).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(content)))
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path=='/':
            content = (BASE/'static/index.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        with LOCK:
            result = get_api(path)
        self.respond(result if result is not None else {'error':'Not found'},200 if result is not None else 404)

    def do_POST(self):
        # Browser mutations must originate from this same local app.
        origin = self.headers.get('Origin')
        if origin and origin != 'http://' + self.headers.get('Host',''):
            return self.respond({'error':'Cross-origin request rejected'},403)
        try:
            size = int(self.headers.get('Content-Length','0'))
            if size<=0 or size>65536:
                raise ValueError('Body must be 1-65536 bytes')
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload,dict):
                raise ValueError('Expected JSON object')
            with LOCK:
                result = post_api(self.path,payload)
            self.respond(result)
        except (ValueError,KeyError,TypeError) as e:
            self.respond({'error':str(e)},400)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=DEFAULT_PORT)
    args = parser.parse_args()
    print(f'Open http://127.0.0.1:{args.port} - Ctrl+C to stop',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
