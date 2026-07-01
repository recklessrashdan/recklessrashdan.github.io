#!/usr/bin/env bash
# Daily health check for recklessrashdan.github.io
set -euo pipefail

BASE_URL="${SITE_URL:-https://recklessrashdan.github.io}"
REPORT_FILE="${REPORT_FILE:-daily-site-report.txt}"

PATHS=(
  "/"
  "/projects/clock-app/index.html"
  "/style.css"
  "/script.js"
)

pass=0
fail=0
now_utc="$(date -u '+%Y-%m-%d %H:%M:%S UTC')"

{
  echo "Daily Website Health Report"
  echo "============================"
  echo "Site: ${BASE_URL}"
  echo "Checked: ${now_utc}"
  echo ""
  echo "Page checks"
  echo "-----------"
} >"${REPORT_FILE}"

for path in "${PATHS[@]}"; do
  url="${BASE_URL%/}${path}"
  # -L follow redirects; -o discard body; -w write stats
  if response="$(curl -sSL -o /dev/null -w '%{http_code} %{time_total}' --max-time 30 "${url}" 2>&1)"; then
    code="${response%% *}"
    time_sec="${response#* }"
    if [[ "${code}" =~ ^2 ]]; then
      status="OK"
      ((pass++)) || true
    else
      status="FAIL"
      ((fail++)) || true
    fi
    printf '%-6s  %6ss  %s\n' "${status}" "${time_sec}" "${url}" >>"${REPORT_FILE}"
  else
    ((fail++)) || true
    printf 'FAIL    —      %s (error: %s)\n' "${url}" "${response}" >>"${REPORT_FILE}"
  fi
done

echo "" >>"${REPORT_FILE}"
echo "Summary" >>"${REPORT_FILE}"
echo "-------" >>"${REPORT_FILE}"
echo "Passed: ${pass}" >>"${REPORT_FILE}"
echo "Failed: ${fail}" >>"${REPORT_FILE}"

if [[ "${fail}" -gt 0 ]]; then
  echo "" >>"${REPORT_FILE}"
  echo "Action: open the repo Actions tab or re-run the workflow after fixing broken URLs." >>"${REPORT_FILE}"
  echo "::warning::${fail} site check(s) failed"
  exit 1
fi

echo "All checks passed."
