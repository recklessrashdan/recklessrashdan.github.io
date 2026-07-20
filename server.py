from __future__ import annotations

import json
import os
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

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()


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

      content_length = int(self.headers.get("Content-Length", "0"))
      raw_body = self.rfile.read(content_length)
      payload = json.loads(raw_body.decode("utf-8"))

      ok, message = send_to_discord(payload)
      if not ok:
        self.send_json(502, {"error": message})
        return

      self.send_json(200, {"ok": True})
    except json.JSONDecodeError:
      self.send_json(400, {"error": "Invalid JSON body"})
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


def sanitize(value: object, max_length: int) -> str:
  return str(value or "").strip()[:max_length]


def send_to_discord(payload: dict) -> tuple[bool, str]:
  if not DISCORD_WEBHOOK_URL:
    return False, "Discord webhook is not configured. Set DISCORD_WEBHOOK_URL."

  name = sanitize(payload.get("name"), 120)
  email = sanitize(payload.get("email"), 254)
  message = sanitize(payload.get("message"), 4000)

  if not name or not email or not message:
    return False, "Name, email, and message are required."

  discord_payload = {
    "embeds": [
      {
        "title": "New portfolio contact message",
        "color": 0x5865F2,
        "fields": [
          {"name": "Name", "value": name, "inline": True},
          {"name": "Email", "value": email, "inline": True},
          {"name": "Message", "value": message},
        ],
        "timestamp": datetime_now_iso(),
      }
    ]
  }

  request = Request(
    DISCORD_WEBHOOK_URL,
    data=json.dumps(discord_payload).encode("utf-8"),
    method="POST",
    headers={"Content-Type": "application/json"},
  )

  try:
    with urlopen(request, timeout=10):
      return True, ""
  except HTTPError as error:
    try:
      details = error.read().decode("utf-8")
    except Exception:
      details = ""
    message_text = f"Discord HTTP {error.code}"
    if details:
      message_text = f"{message_text}: {details}"
    return False, message_text
  except URLError as error:
    return False, f"Could not connect to Discord: {error.reason}"
  except Exception as error:
    return False, f"Could not send message: {error}"


def datetime_now_iso() -> str:
  from datetime import datetime, timezone

  return datetime.now(timezone.utc).isoformat()


def main() -> None:
  server = ThreadingHTTPServer((HOST, PORT), PortfolioHandler)
  print(f"Server running at http://{HOST}:{PORT}")
  if not DISCORD_WEBHOOK_URL:
    print("Warning: DISCORD_WEBHOOK_URL missing; /api/contact will fail until configured.")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print("\nStopping server...")
  finally:
    server.server_close()


if __name__ == "__main__":
  main()
