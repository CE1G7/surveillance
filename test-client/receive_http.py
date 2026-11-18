"""Simple HTTP receiver for testing the edge device.

Accepts any POST/PUT and stores what it gets in --out (default: ./received):
  * multipart/form-data   -> every file part is saved (e.g. an .mp4), other fields are logged
  * video/*, image/*, application/octet-stream -> raw body saved as a file
  * application/json / text -> logged and saved as .json / .txt

Examples:
  python receive_http.py --port 8080
  curl -F "event=motion" -F "video=@clip.mp4" http://localhost:8080/upload
  curl -H "Content-Type: video/mp4" --data-binary @clip.mp4 http://localhost:8080/upload
  curl -H "Content-Type: application/json" -d '{"event":"motion"}' http://localhost:8080/event
"""
import argparse
import json
import mimetypes
import re
import sys
from datetime import datetime
from email.parser import BytesParser
from email.policy import HTTP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

OUT_DIR = Path("received")


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", Path(name).name) or "file"


def save(data: bytes, name: str) -> Path:
    path = OUT_DIR / f"{timestamp()}_{safe_name(name)}"
    path.write_bytes(data)
    return path


def ext_for(content_type: str) -> str:
    return mimetypes.guess_extension(content_type) or ".bin"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._reply(200, {"status": "ok", "stored_in": str(OUT_DIR.resolve())})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        ctype = self.headers.get("Content-Type", "application/octet-stream")
        mime = ctype.split(";")[0].strip().lower()
        print(f"\n[{datetime.now():%H:%M:%S}] {self.command} {self.path}  {mime}  {length} bytes")

        saved = []
        if mime == "multipart/form-data":
            saved = self._handle_multipart(body, ctype)
        elif mime == "application/json":
            try:
                print("  json:", json.dumps(json.loads(body), indent=2))
            except json.JSONDecodeError:
                print("  invalid json:", body[:200])
            saved.append(save(body, "payload.json"))
        elif mime.startswith("text/"):
            print("  text:", body.decode(errors="replace")[:500])
            saved.append(save(body, "payload.txt"))
        else:
            # Raw binary (video/mp4, image/jpeg, octet-stream, ...).
            name = self.headers.get("X-Filename") or f"upload{ext_for(mime)}"
            saved.append(save(body, name))

        for p in saved:
            print(f"  saved -> {p}")
        self._reply(200, {"status": "ok", "saved": [str(p) for p in saved]})

    do_PUT = do_POST

    def _handle_multipart(self, body: bytes, ctype: str) -> list[Path]:
        msg = BytesParser(policy=HTTP).parsebytes(
            f"Content-Type: {ctype}\r\n\r\n".encode() + body
        )
        saved = []
        for part in msg.iter_parts():
            field = part.get_param("name", header="content-disposition")
            filename = part.get_filename()
            data = part.get_payload(decode=True) or b""
            if filename:
                print(f"  file field '{field}': {filename} ({len(data)} bytes, {part.get_content_type()})")
                saved.append(save(data, filename))
            else:
                print(f"  field '{field}': {data.decode(errors='replace')[:500]}")
        return saved

    def _reply(self, code: int, payload: dict):
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        pass  # we print our own log lines


def main():
    global OUT_DIR
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--out", default="received", help="folder to store received files in")
    args = parser.parse_args()

    sys.stdout.reconfigure(line_buffering=True)  # show logs immediately even when piped
    OUT_DIR = Path(args.out)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Listening on http://{args.host}:{args.port}, storing files in {OUT_DIR.resolve()}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping")


if __name__ == "__main__":
    main()
