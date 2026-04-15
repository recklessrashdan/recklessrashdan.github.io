from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT_DIR = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000


def load_env_file() -> None:
  env_path = ROOT_DIR / ".env"
  if not env_path.exists():
    return

  for line in env_path.read_text(encoding="utf-8").splitlines():
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" not in stripped:
      continue
    key, value = stripped.split("=", 1)
    os.environ.setdefault(key.strip(), value.strip())


load_env_file()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "contact_messages")


class PortfolioHandler(SimpleHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

  # Avoid stderr logging issues in restricted terminals.
  def log_message(self, format: str, *args) -> None:
    return

  def do_POST(self) -> None:
    try:
      if self.path != "/api/contact":
        self.send_json(404, {"error": "Not found"})
        return
      self.send_json(200, {"ok": True, "message": "Contact endpoint reached"})
    except Exception as error:
      self.send_json(500, {"error": f"Server error: {error}"})

  def do_GET(self) -> None:
    parsed = urlparse(self.path)
    if parsed.path == "/api/contact":
      self.send_json(405, {"error": "Method not allowed"})
      return

    super().do_GET()

  def send_json(self, status_code: int, payload: dict) -> None:
    response = json.dumps(payload).encode("utf-8")
    self.send_response(status_code)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.send_header("Content-Length", str(len(response)))
    self.end_headers()
    self.wfile.write(response)


def main() -> None:
  server = ThreadingHTTPServer((HOST, PORT), PortfolioHandler)
  print(f"Server running at http://{HOST}:{PORT}")
  if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    print("Warning: SUPABASE_URL / SUPABASE_ANON_KEY missing; /api/contact will fail until configured.")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print("\nStopping server...")
  finally:
    server.server_close()


def save_to_supabase(entry: dict) -> tuple[bool, str]:
  if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    return False, "Supabase is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY."

  endpoint = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
  payload = json.dumps(entry).encode("utf-8")
  headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Prefer": "return=minimal"
  }
  request = Request(endpoint, data=payload, method="POST", headers=headers)

  try:
    with urlopen(request, timeout=10):
      return True, ""
  except HTTPError as error:
    try:
      details = error.read().decode("utf-8")
    except Exception:
      details = ""
    message = f"Supabase HTTP {error.code}"
    if details:
      message = f"{message}: {details}"
    return False, message
  except URLError as error:
    return False, f"Could not connect to Supabase: {error.reason}"
  except Exception as error:
    return False, f"Could not save message: {error}"


if __name__ == "__main__":
  main()
