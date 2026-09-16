#!/usr/bin/env bash
# Builds the Word report, renders it, and rebuilds until the contents page
# numbers match the rendered pages. The final render is kept as the PDF copy.
set -euo pipefail
cd "$(dirname "$0")"
PY="$HOME/.ctf-tools/venv/bin/python3"
PREVIEW=../out/preview/DSA_Linked_List_Report.pdf
for pass in 1 2 3 4; do
  "$PY" build_report.py
  ./preview.sh ../out/DSA_Linked_List_Report.docx "$PREVIEW" >/dev/null
  result=$("$PY" measure_pages.py "$PREVIEW")
  echo "  pass $pass: $(echo "$result" | head -1)"
  if echo "$result" | grep -q STABLE; then
    echo "contents page numbers are stable"
    cp "$PREVIEW" ../out/DSA_Linked_List_Report.pdf
    echo "pdf: out/DSA_Linked_List_Report.pdf"
    exit 0
  fi
done
echo "contents page numbers did not converge" >&2
exit 1
