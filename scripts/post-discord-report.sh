#!/usr/bin/env bash
# Post weekly-site-report.txt to a Discord channel webhook.
set -euo pipefail

REPORT_FILE="${REPORT_FILE:-weekly-site-report.txt}"
WEBHOOK_URL="${DISCORD_WEBHOOK_URL:?DISCORD_WEBHOOK_URL is not set}"
CHECK_OUTCOME="${CHECK_OUTCOME:-unknown}"

if [[ ! -f "${REPORT_FILE}" ]]; then
  echo "Report file not found: ${REPORT_FILE}" >&2
  exit 1
fi

python3 - "${REPORT_FILE}" "${CHECK_OUTCOME}" <<'PY' | curl -fsSL -X POST "${WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d @-
import json
import sys
from pathlib import Path

report_path, outcome = sys.argv[1], sys.argv[2]
report = Path(report_path).read_text(encoding="utf-8").strip()

if outcome == "success":
    color = 0x57F287
    title = "Weekly site check — all OK"
elif outcome == "failure":
    color = 0xED4245
    title = "Weekly site check — issues found"
else:
    color = 0xFEE75C
    title = "Weekly site check"

# Discord embed description limit is 4096; keep report readable in a code block.
body = report if len(report) <= 3900 else report[:3900] + "\n…(truncated)"

payload = {
    "embeds": [
        {
            "title": title,
            "url": "https://recklessrashdan.github.io/",
            "description": f"```\n{body}\n```",
            "color": color,
        }
    ]
}

print(json.dumps(payload))
PY

echo "Discord notification sent."
