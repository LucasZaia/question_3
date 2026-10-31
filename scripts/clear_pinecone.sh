#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ "${1:-}" == "--yes" ]]; then
  shift
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--yes]" >&2
  exit 1
else
  echo "ATENÇÃO: todos os vetores do namespace configurado serão removidos."
  read -r -p "Digite DELETE para confirmar: " confirmation
  if [[ "$confirmation" != "DELETE" ]]; then
    echo "Operação cancelada."
    exit 0
  fi
fi

if [[ $# -gt 0 ]]; then
  echo "Uso inválido: nenhum argumento adicional é permitido." >&2
  exit 1
fi

exec uv run python -m semantic_search.clear
