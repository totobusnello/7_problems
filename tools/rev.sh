#!/usr/bin/env bash
# rev.sh — lançador ÚNICO de revisores adversariais do 7_PROBLEMS.
#
# Motivação (2026-07-11, decisão de Luiz): falhas recorrentes de lançamento
# (CLAUDE_PLUGIN_DATA faltando 2×, model id gpt-5.6 vs gpt-5.6-sol, timeout de
# Bash de subagente matando chamadas longas). A verdade executável mora AQUI,
# não em notas de rodapé.
#
# REGRAS DE USO (também no CLAUDE.md do projeto):
#   1. Todo revisor externo é lançado por este script — nunca comando manual.
#   2. Chamadas longas (kimi/codex) rodam da SESSÃO PRINCIPAL com
#      run_in_background=true — NUNCA via Bash de subagente (teto ~10min).
#   3. `rev.sh doctor` valida os 4 canais sem gastar tokens.
#
# Uso:
#   tools/rev.sh doctor
#   tools/rev.sh kimi  [review|challenge|ask] [--base <ref>] "focus/prompt..."
#   tools/rev.sh codex "prompt..."            # gpt-5.6-sol, read-only, exec
#   tools/rev.sh glm   "prompt..."            # wrapper read-only existente
#   tools/rev.sh grok  "prompt..."            # wrapper read-only existente
set -uo pipefail

REPO_ROOT="/Users/lab/Claude"
# Root do plugin: o CACHE versionado (é nele que o hook de segurança do
# ~/.kimi-code/config.toml está pinado). Usar o root do marketplace dispara
# falso-positivo de "hook path drift" E roda SEM hook (lição 2026-07-11).
KIMI_CACHE="/Users/lab/.claude/plugins/cache/kimi-marketplace/kimi"
KIMI_ROOT="$(ls -d "$KIMI_CACHE"/*/ 2>/dev/null | sort -V | tail -1 | sed 's:/$::')"
[ -n "$KIMI_ROOT" ] || KIMI_ROOT="/Users/lab/.claude/plugins/marketplaces/kimi-marketplace"
KIMI_DATA="/Users/lab/.claude/plugins/data/kimi/kimi-plugin-cc"
GLM_BIN="/Users/lab/Claude/scripts/glm"
GROK_BIN="/Users/lab/Claude/scripts/grok"
CODEX_MODEL="gpt-5.6-sol"   # call log #7: 'gpt-5.6'/'gpt-5.6-codex' dão 400 no plano ChatGPT

die() { echo "rev.sh ERRO: $*" >&2; exit 1; }

doctor() {
  local ok=0
  echo "== rev.sh doctor =="
  [ -x "$KIMI_ROOT/scripts/companion.sh" ] && echo "[OK] kimi companion.sh" || { echo "[FAIL] kimi companion.sh ausente"; ok=1; }
  [ -f "$KIMI_ROOT/dist/companion.js" ] && echo "[OK] kimi dist/companion.js" || { echo "[FAIL] kimi dist"; ok=1; }
  [ -d "$KIMI_DATA" ] && echo "[OK] CLAUDE_PLUGIN_DATA ($KIMI_DATA)" || { echo "[FAIL] kimi data dir"; ok=1; }
  node --version 2>/dev/null | grep -qE "v(2[2-9]|[3-9][0-9])" && echo "[OK] node >=22" || { echo "[FAIL] node >=22.5 (kimi exige node:sqlite)"; ok=1; }
  command -v codex >/dev/null && echo "[OK] codex CLI ($(codex --version 2>/dev/null | head -1))" || { echo "[FAIL] codex CLI"; ok=1; }
  grep -q "$CODEX_MODEL" ~/.codex/config.toml 2>/dev/null && echo "[OK] codex default = $CODEX_MODEL" || echo "[WARN] $CODEX_MODEL não é o default do ~/.codex/config.toml — omitir -m usa o default do config"
  [ -x "$GLM_BIN" ] && echo "[OK] glm wrapper" || { echo "[FAIL] glm wrapper"; ok=1; }
  [ -r ~/.config/glm/token ] && echo "[OK] glm token" || { echo "[FAIL] glm token"; ok=1; }
  [ -x "$GROK_BIN" ] && echo "[OK] grok wrapper" || { echo "[FAIL] grok wrapper"; ok=1; }
  [ -r ~/.config/grok/token ] && echo "[OK] grok token" || { echo "[FAIL] grok token"; ok=1; }
  echo "[..] kimi safety hook probe (setup --check):"
  if (cd "$REPO_ROOT" && CLAUDE_PLUGIN_ROOT="$KIMI_ROOT" CLAUDE_PLUGIN_DATA="$KIMI_DATA" \
      KIMI_PLUGIN_CC_WORKSPACE_CWD="$REPO_ROOT" \
      "$KIMI_ROOT/scripts/companion.sh" setup --check 2>&1 | grep -q "probe passed"); then
    echo "[OK] kimi hook instalado e probe passou (root: $KIMI_ROOT)"
  else
    echo "[FAIL] kimi hook probe — rodar /kimi:setup (sem hook, kimi -p auto-aprova Write/Bash)"; ok=1
  fi
  echo "== lembretes de processo =="
  echo "- kimi/codex: lançar com run_in_background=true DA SESSÃO PRINCIPAL (nunca Bash de subagente)"
  echo "- registrar TODA chamada em 07_MODEL_CALL_LOG.md (máx. 5/ciclo)"
  return $ok
}

case "${1:-}" in
  doctor) doctor ;;
  kimi)
    shift
    mode="review"
    case "${1:-}" in review|challenge|ask) mode="$1"; shift ;; esac
    [ $# -ge 1 ] || die "kimi: faltou focus/prompt"
    cd "$REPO_ROOT" || die "cd $REPO_ROOT"
    CLAUDE_PLUGIN_ROOT="$KIMI_ROOT" CLAUDE_PLUGIN_DATA="$KIMI_DATA" \
      KIMI_PLUGIN_CC_WORKSPACE_CWD="$REPO_ROOT" \
      exec "$KIMI_ROOT/scripts/companion.sh" "$mode" "$@"
    ;;
  codex)
    shift
    [ $# -ge 1 ] || die "codex: faltou prompt"
    exec codex exec --sandbox read-only -m "$CODEX_MODEL" "$@"
    ;;
  glm)
    shift; [ $# -ge 1 ] || die "glm: faltou prompt"
    exec "$GLM_BIN" "$@"
    ;;
  grok)
    shift; [ $# -ge 1 ] || die "grok: faltou prompt"
    exec "$GROK_BIN" "$@"
    ;;
  *)
    die "canal desconhecido '${1:-}' — use: doctor | kimi | codex | glm | grok"
    ;;
esac
