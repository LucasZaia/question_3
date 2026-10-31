#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ $# -eq 0 ]]; then
  read -r -p "Digite o que deseja buscar: " query
  if [[ -z "${query//[[:space:]]/}" ]]; then
    echo "A consulta não pode estar vazia." >&2
    exit 1
  fi
  set -- "$query"
fi

exec uv run python -m semantic_search.main search "$@"
