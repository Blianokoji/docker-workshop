import json
import random
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

FACTS = [
    "Docker was first released to the world in March 2013 as open source.",
    "Containers share the host operating system's kernel, making them start in milliseconds.",
    "Solomon Hykes originally founded Docker under the name dotCloud.",
    "Docker uses Linux kernel namespaces and cgroups to achieve process isolation.",
    "A custom Docker bridge network includes an embedded DNS server for automatic service discovery.",
    "Unlike VMs, containers have near-zero virtualization overhead for CPU and Memory."
]

class FactHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]} {args[1]}")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        payload = {
            "fact": random.choice(FACTS),
            "served_by": socket.gethostname(),
            "service": "fact-api",
            "port": PORT
        }
        self.wfile.write(json.dumps(payload).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), FactHandler)
    print(f"[API] Fact API listening internally on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()