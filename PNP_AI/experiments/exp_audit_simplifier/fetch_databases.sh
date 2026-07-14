#!/usr/bin/env bash
# Baixa as databases do Simplifier (dados externos, NÃO versionados) e verifica sha256.
# Fonte: github.com/SPbSAT/simplifier @ 5b088f2f. Uso: ./fetch_databases.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REF=5b088f2fc3ef1de196d91b9d16febc3052e324d5
BASE="https://raw.githubusercontent.com/SPbSAT/simplifier/$REF/databases"

verify() {  # <arquivo> <sha256-esperado>
  local f="$1" want="$2"
  echo "baixando $f..."
  curl -sSL -o "$HERE/$f" "$BASE/$f"
  local got; got=$(sha256sum "$HERE/$f" | cut -d' ' -f1)
  if [ "$got" = "$want" ]; then echo "  $f OK ($got)"; else
    echo "  SHA MISMATCH em $f: got=$got want=$want" >&2; exit 1; fi
}

verify database_aig.txt   ac253e596bed0cdb05ee138cf6191e79b6e15ff0bf1d6d6708615f2249dca1aa
verify database_bench.txt 2b47eeb969a9f56f0881157d25a96723fd1c2207ecd20f1527809b0448bd3434
echo "databases prontas em $HERE"
