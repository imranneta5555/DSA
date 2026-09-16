#!/usr/bin/env bash
# Renders a .docx to PDF with headless LibreOffice.
# Used to measure the page each heading lands on and for visual checks.
# Usage: ./preview.sh input.docx output.pdf
set -euo pipefail
DOCX="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
PDF="$(mkdir -p "$(dirname "$2")" && cd "$(dirname "$2")" && pwd)/$(basename "$2")"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# A throwaway profile keeps the run independent of any open LibreOffice window.
soffice -env:UserInstallation="file://$WORK/profile" --headless \
  --convert-to pdf --outdir "$WORK" "$DOCX" >/dev/null 2>&1

OUT="$WORK/$(basename "${DOCX%.*}").pdf"
[ -s "$OUT" ] || { echo "preview failed: no PDF produced" >&2; exit 1; }
mv "$OUT" "$PDF"
echo "preview: $PDF"
