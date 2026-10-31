#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ $# -eq 0 ]]; then
  mkdir -p data/documents
  found=0
  while IFS= read -r -d '' input_file; do
    found=1
    filename="$(basename "$input_file")"
    output_file="data/documents/${filename%.html}.md"
    if [[ -e "$output_file" ]]; then
      echo "Ignorado, Markdown já existe: $output_file"
      continue
    fi
    uv run python extractor/convert_article_html.py "$input_file" "$output_file"
  done < <(find docs_extractor -maxdepth 1 -type f -iname '*.html' -print0 | sort -z)

  if [[ "$found" -eq 0 ]]; then
    echo "Nenhum arquivo HTML encontrado em docs_extractor/." >&2
    exit 1
  fi
  exit 0
fi

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "Uso: $0 [INPUT.html OUTPUT.md [SOURCE_URL]]" >&2
  echo "Sem argumentos: converte todos os HTMLs de docs_extractor/." >&2
  exit 1
fi

if [[ -e "$2" ]]; then
  echo "Ignorado, Markdown já existe: $2"
  exit 0
fi

exec uv run python extractor/convert_article_html.py "$@"
