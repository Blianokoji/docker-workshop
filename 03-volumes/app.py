import os
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 5000
DATA_DIR = os.getenv("DATA_DIR", "/app/data")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Workshop | Persistent Notes</title>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --accent: #38bdf8;
            --text: #f8fafc;
            --muted: #94a3b8;
            --border: #334155;
            --danger: #ef4444;
            --success: #22c55e;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            padding: 2rem 1rem;
            min-height: 100vh;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 680px;
        }
        .badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent);
            padding: 0.35rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        h1 { font-size: 2rem; margin-bottom: 0.5rem; }
        .meta {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
            color: var(--muted);
        }
        .meta strong { color: var(--text); }
        .form-box {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
        }
        .input-row { display: flex; gap: 0.5rem; }
        input[type="text"] {
            flex: 1;
            padding: 0.75rem 1rem;
            background: #0b1120;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text);
            font-size: 1rem;
        }
        input[type="text"]:focus { outline: 2px solid var(--accent); }
        button {
            padding: 0.75rem 1.5rem;
            background: var(--accent);
            color: #042f2e;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        button:hover { opacity: 0.9; }
        .notes-list { display: flex; flex-direction: column; gap: 0.75rem; }
        .note-card {
            background: var(--card);
            border: 1px solid var(--border);
            padding: 1rem 1.25rem;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .note-text { font-size: 1.05rem; }
        .empty-state {
            text-align: center;
            color: var(--muted);
            padding: 3rem 1rem;
            border: 2px dashed var(--border);
            border-radius: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">🐳 Module 3: Docker Volumes</div>
        <h1>Persistent Notebook</h1>
        <div class="meta">
            <div>Container ID: <strong>{{HOSTNAME}}</strong></div>
            <div>Storage Path: <strong>{{FILEPATH}}</strong></div>
            <div>Persistence Status: <strong style="color:var(--accent);">Active</strong></div>
        </div>

        <div class="form-box">
            <form id="noteForm" onsubmit="addNote(event)" class="input-row">
                <input type="text" id="noteInput" placeholder="Write a note to test persistence..." required autocomplete="off">
                <button type="submit">Save Note</button>
            </form>
        </div>

        <div id="notesContainer" class="notes-list">
            <!-- Notes loaded dynamically -->
        </div>
    </div>

    <script>
        async function loadNotes() {
            const res = await fetch('/api/notes');
            const notes = await res.json();
            const container = document.getElementById('notesContainer');
            if (notes.length === 0) {
                container.innerHTML = '<div class="empty-state">No notes stored yet.<br>Add a note above to see if it survives container restarts!</div>';
                return;
            }
            container.innerHTML = notes.map((n, i) => `
                <div class="note-card">
                    <span class="note-text">${escapeHtml(n)}</span>
                    <span style="font-size:0.8rem;color:var(--muted)">#${i + 1}</span>
                </div>
            `).join('');
        }

        async function addNote(e) {
            e.preventDefault();
            const input = document.getElementById('noteInput');
            const text = input.value.trim();
            if (!text) return;

            await fetch('/api/notes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ note: text })
            });

            input.value = '';
            loadNotes();
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        loadNotes();
    </script>
</body>
</html>"""

class NotesHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Concise logging
        print(f"[{self.log_date_time_string()}] {args[0]} {args[1]}")

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            content = HTML_PAGE.replace("{{HOSTNAME}}", socket.gethostname()).replace("{{FILEPATH}}", NOTES_FILE)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        elif self.path == "/api/notes":
            try:
                with open(NOTES_FILE, "r", encoding="utf-8") as f:
                    notes = json.load(f)
            except Exception:
                notes = []
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/notes":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode("utf-8"))
                new_note = data.get("note", "").strip()
            except Exception:
                new_note = ""

            if new_note:
                try:
                    with open(NOTES_FILE, "r", encoding="utf-8") as f:
                        notes = json.load(f)
                except Exception:
                    notes = []
                notes.append(new_note)
                with open(NOTES_FILE, "w", encoding="utf-8") as f:
                    json.dump(notes, f, indent=2)

                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "count": len(notes)}).encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"Missing note text"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), NotesHandler)
    print(f"[INFO] Notes App running on http://0.0.0.0:{PORT}")
    print(f"[INFO] Storing data at: {NOTES_FILE}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()