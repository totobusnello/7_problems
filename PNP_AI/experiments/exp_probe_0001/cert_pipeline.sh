#!/bin/zsh
# EXP-PROBE-0001 — pipeline SEQUENCIAL de certificação (lição: paralelismo com
# provas de 4GB + drat-trim estoura a RAM da máquina; um passo por vez).
# Desacoplado da sessão (nohup) para sobreviver a kills do harness.
set -u
cd "$(dirname "$0")"
DT=/private/tmp/claude-501/-Users-lab-Claude-Projetos-7-problems/8ffb0bad-6e82-4e1b-b08b-00ff4ab65529/scratchpad/drat-trim/drat-trim
LOG=cert_pipeline.log
say() { echo "[$(date +%H:%M:%S)] $1" >> $LOG; }

say "=== PIPELINE INICIADO ==="

# Passo 1: verificar a prova COMPLETA do 0x166b (3,87GB, kissat já terminou)
say "P1: drat-trim 0x166b (prova existente de 3.87GB)..."
if $DT cert_0x166b_k9.cnf cert_0x166b_k9.drat > dt_0x166b.out 2>&1; then :; fi
if grep -q "s VERIFIED" dt_0x166b.out; then
  say "P1: 0x166b DRAT **s VERIFIED**"
else
  say "P1: 0x166b FALHOU — $(tail -1 dt_0x166b.out)"
fi

# Passo 2: re-rodar kissat COM DRAT para 0x1669 (prova anterior morreu incompleta)
say "P2: kissat+DRAT 0x1669 (re-run, sozinho na máquina)..."
rm -f cert_0x1669_k9.drat
kissat -q cert_0x1669_k9.cnf cert_0x1669_k9.drat > kissat_0x1669.out 2>&1
RC=$?
if [ $RC -eq 20 ]; then
  say "P2: 0x1669 UNSAT (re-confirmado); prova $(du -h cert_0x1669_k9.drat | cut -f1)"
else
  say "P2: 0x1669 retorno inesperado: $RC"
fi

# Passo 3: verificar a prova do 0x1669
say "P3: drat-trim 0x1669..."
if $DT cert_0x1669_k9.cnf cert_0x1669_k9.drat > dt_0x1669.out 2>&1; then :; fi
if grep -q "s VERIFIED" dt_0x1669.out; then
  say "P3: 0x1669 DRAT **s VERIFIED**"
else
  say "P3: 0x1669 FALHOU — $(tail -1 dt_0x1669.out)"
fi

say "=== PIPELINE CONCLUÍDO ==="
touch PIPELINE_DONE
