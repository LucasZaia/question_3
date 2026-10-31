#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

LIMIT="${LIMIT:-5}"
if [[ "${1:-}" == "--limit" ]]; then
  if [[ $# -lt 2 ]]; then
    echo "Usage: $0 [--limit N] [query-file]" >&2
    exit 1
  fi
  LIMIT="$2"
  shift 2
fi

if [[ $# -gt 1 ]]; then
  echo "Usage: $0 [--limit N] [query-file]" >&2
  exit 1
fi

QUERY_FILE="${1:-data/evaluation/queries.json}"
if [[ ! -f "$QUERY_FILE" ]]; then
  echo "Query file not found: $QUERY_FILE" >&2
  exit 1
fi

uv run python -c '
import json
import sys

with open(sys.argv[1], encoding="utf-8") as file:
    for item in json.load(file):
        print(item["query"])
' "$QUERY_FILE" | while IFS= read -r query; do
  echo "========================================"
  echo "Query: $query"
  ./scripts/search_documents.sh "$query" --limit "$LIMIT"
done
