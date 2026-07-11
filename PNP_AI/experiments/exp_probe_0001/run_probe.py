"""
EXP-PROBE-0001 (v2) — Sonda k=9 nas 2 classes NPN-4 pendentes (SRC-0019/0027).

Classes: 0x1669 (tt=5737) e 0x166b (tt=5739) — catálogo: ub=10, k=9 indecidido.

v2 (lições da 1ª tentativa, abortada por pressão de disco):
- FASE DECISÃO sem proof logging (DRAT em busca longa ultrapassou 4GB/25min;
  projeção >100GB em 12h). Veredito primeiro; certificado em execução
  separada e planejada, SÓ depois de saber que é UNSAT.
- Quebra de simetria no encoder: portas duplicadas proibidas (sound para
  opt ∈ {9,10} — circuito mínimo não tem duplicatas).
- Logs unbuffered (flush).

Budget pré-aprovado (Luiz): 12h wall-clock por classe; estouro = aborto
documentado. Sem prova nesta fase, um eventual UNSAT fica
COMPUTATIONALLY_TESTED (não FINITE_SCOPE_VERIFIED) até a rodada certificada.
"""

import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "exp_gate_0001"))
from aig_exact import AIGEncoder, verify_circuit  # noqa: E402

BUDGET_S = 12 * 3600
K = 9
KISSAT = "kissat"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def parse_kissat_model(stdout):
    lits = []
    for line in stdout.splitlines():
        if line.startswith("v "):
            lits.extend(int(x) for x in line[2:].split() if x != "0")
    return lits


def probe(hexname, tt):
    log(f"classe {hexname} tt={tt} k={K}: montando CNF (v2, com dedup de portas)...")
    enc = AIGEncoder(4, K, tt).build()
    cnf = HERE / f"probe_{hexname}_k{K}_v2.cnf"
    enc.to_dimacs(cnf)
    log(f"CNF: {enc.nvars} vars, {len(enc.clauses)} cláusulas. kissat SEM proof (budget {BUDGET_S}s)...")
    t0 = time.time()
    try:
        r = subprocess.run([KISSAT, "-q", str(cnf)], capture_output=True,
                           text=True, timeout=BUDGET_S)
    except subprocess.TimeoutExpired:
        log(f"RESULTADO {hexname}: ABORTO POR BUDGET ({BUDGET_S}s) — k={K} indecidido localmente")
        return
    dt = time.time() - t0
    if r.returncode == 10:  # SAT
        model = parse_kissat_model(r.stdout)
        gates, op = enc.decode(model)
        ok = verify_circuit(4, tt, gates, op)
        log(f"RESULTADO {hexname}: **SAT em {dt:.1f}s** — CIRCUITO DE {K} PORTAS EXISTE "
            f"(verificação por simulação: {'OK' if ok else 'FALHOU!'})")
        log(f"  circuito: {gates} out_inv={op}")
        assert ok, "circuito decodificado não verifica — INVESTIGAR"
        log(f"  => opt_AIG({hexname}) <= 9: CATÁLOGO MELHORADO (era ub=10). "
            f"Próximo: decidir k=8 p/ fixar o valor exato.")
    elif r.returncode == 20:  # UNSAT
        log(f"RESULTADO {hexname}: **UNSAT em {dt:.1f}s** — não existe circuito de {K} portas "
            f"(sem certificado nesta fase; rodada DRAT certificada a planejar)")
        log(f"  => com ub=10 do catálogo: opt_AIG({hexname}) = 10 [COMPUTATIONALLY_TESTED]")
    else:
        log(f"RESULTADO {hexname}: retorno inesperado do kissat: {r.returncode}\n{r.stdout[-300:]}")


if __name__ == "__main__":
    probe(sys.argv[1], int(sys.argv[2]))
