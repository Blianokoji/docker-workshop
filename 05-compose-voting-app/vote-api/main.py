import os
import json
import socket
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import redis

PORT = 3000
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Attempt Redis connection with retry
r = None
for _ in range(5):
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_connect_timeout=2)
        r.ping()
        print(f"[SUCCESS] Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        break
    except Exception as e:
        print(f"[WAIT] Waiting for Redis at {REDIS_HOST}:{REDIS_PORT}... ({e})")
        time.sleep(1)

HTML_VOTE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Workshop | Voting App</title>
    <style>
        :root {
            --bg: #0b0f19;
            --card: #151d30;
            --border: #222f4c;
            --text: #f8fafc;
            --muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1.5rem;
        }
        .container { width: 100%; max-width: 600px; text-align: center; }
        .badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.15);
            color: #818cf8;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        h1 { font-size: 2.2rem; margin-bottom: 0.5rem; }
        p.desc { color: var(--muted); margin-bottom: 2rem; }
        .vote-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
        .vote-card {
            background: var(--card);
            border: 2px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem 1rem;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            user-select: none;
        }
        .vote-card:hover {
            transform: translateY(-4px);
            border-color: #818cf8;
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.25);
        }
        .vote-card:active { transform: scale(0.96); }
        .icon { font-size: 3rem; margin-bottom: 0.5rem; display: block; }
        .name { font-weight: 700; font-size: 1.1rem; }
        .toast {
            margin-top: 1.5rem;
            min-height: 24px;
            font-size: 0.95rem;
            color: #34d399;
            font-weight: 600;
        }
        .footer-link {
            margin-top: 2rem;
            font-size: 0.9rem;
            color: var(--muted);
        }
        .footer-link a { color: #818cf8; text-decoration: none; font-weight: 600; }
        .instance-tag {
            font-size: 0.8rem;
            color: var(--muted);
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">🐳 Module 5: Docker Compose</div>
        <h1>Cast Your Vote</h1>
        <p class="desc">Which animal is the undisputed mascot of DevOps?</p>

        <div class="vote-grid">
            <div class="vote-card" onclick="castVote('cats')">
                <span class="icon">🐱</span>
                <span class="name">Cats</span>
            </div>
            <div class="vote-card" onclick="castVote('dogs')">
                <span class="icon">🐶</span>
                <span class="name">Dogs</span>
            </div>
            <div class="vote-card" onclick="castVote('capybaras')">
                <span class="icon">🦫</span>
                <span class="name">Capybaras</span>
            </div>
        </div>

        <div id="toast" class="toast"></div>

        <div class="footer-link">
            Want to see live results? Open the <a href="http://localhost:3001" target="_blank">Live Dashboard ↗</a>
        </div>
        <div class="instance-tag">Served by API Container: <strong>{{HOSTNAME}}</strong></div>
    </div>

    <script>
        async function castVote(candidate) {
            const toast = document.getElementById('toast');
            toast.textContent = 'Recording vote in Redis...';
            try {
                const res = await fetch('/vote', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ candidate: candidate })
                });
                const data = await res.json();
                toast.textContent = '🎉 Voted for ' + candidate.toUpperCase() + '! (Processed by ' + data.served_by + ')';
                setTimeout(() => { toast.textContent = ''; }, 3000);
            } catch (err) {
                toast.textContent = '❌ Failed to record vote: ' + err.message;
            }
        }
    </script>
</body>
</html>"""

class VoteHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]} {args[1]}")

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html = HTML_VOTE.replace("{{HOSTNAME}}", socket.gethostname())
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/results":
            cats = int(r.get("vote:cats") or 0) if r else 0
            dogs = int(r.get("vote:dogs") or 0) if r else 0
            capys = int(r.get("vote:capybaras") or 0) if r else 0

            payload = {
                "cats": cats,
                "dogs": dogs,
                "capybaras": capys,
                "total": cats + dogs + capys,
                "served_by": socket.gethostname()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/vote":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode("utf-8"))
                candidate = data.get("candidate", "").lower().strip()
            except Exception:
                candidate = ""

            if candidate in ["cats", "dogs", "capybaras"]:
                if r:
                    r.incr(f"vote:{candidate}")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "candidate": candidate, "served_by": socket.gethostname()}).encode("utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error":"Invalid candidate"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), VoteHandler)
    print(f"[API] Voting API server listening on 0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()