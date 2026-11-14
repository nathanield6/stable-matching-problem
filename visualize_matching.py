"""Serve the matching replay and run both algorithms on demand."""

import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from brute_force_visualization import find_matches
from gale_shapley_visualization import gale_shapley
from groups import create_group


REPLAY_PAGE = Path(__file__).resolve().parent / "output" / "stable-matching-replay.html"
GROUP_SIZE = 4
MAX_GROUP_SIZE = 7


def create_run(size=GROUP_SIZE):
    group1 = create_group(size)
    group2 = create_group(size)
    gale_steps = []
    brute_steps = []
    gale_shapley(group1, group2, on_proposal=gale_steps.append)
    find_matches(group1, group2, on_candidate=brute_steps.append)
    return {
        "preferences": [
            [person.get_all_rankings() for person in group.get_members()]
            for group in (group1, group2)
        ],
        "gale": gale_steps,
        "brute": brute_steps,
    }


class ReplayHandler(BaseHTTPRequestHandler):
    def send_content(self, content, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path == "/":
            self.send_content(REPLAY_PAGE.read_bytes(), "text/html; charset=utf-8")
        else:
            self.send_error(404)

    def do_POST(self):
        request = urlsplit(self.path)
        if request.path != "/run":
            self.send_error(404)
            return

        sizes = parse_qs(request.query, keep_blank_values=True).get("size", [str(GROUP_SIZE)])
        allowed_sizes = {str(size) for size in range(1, MAX_GROUP_SIZE + 1)}
        if len(sizes) != 1 or sizes[0] not in allowed_sizes:
            self.send_error(400, f"Choose between 1 and {MAX_GROUP_SIZE} people per group.")
            return

        data = json.dumps(create_run(int(sizes[0]))).encode("utf-8")
        self.send_content(data, "application/json")


if __name__ == "__main__":
    with ThreadingHTTPServer(("127.0.0.1", 0), ReplayHandler) as server:
        url = f"http://127.0.0.1:{server.server_port}/"
        print(f"Open {url} in your browser. Keep this terminal running.", flush=True)
        try:
            webbrowser.open(url)
            server.serve_forever()
        except KeyboardInterrupt:
            pass
