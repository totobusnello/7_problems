"""
EXP-PROBE-0001 — Rodadas de certificação pós-veredito.

Modo 'unsat9': re-executa k=9 COM proof logging DRAT + verificação drat-trim
  (certifica o lado "não existe circuito de 9 portas").
Modo 'sat10': busca circuito de k=10 portas e verifica por SIMULAÇÃO
  (certifica o lado "10 portas bastam" sem depender do catálogo).

Mesmo budget da sonda (12h/execução). Disco monitorado: prova esperada ~4-6GB.
"""

import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "exp_gate_0001"))
from aig_exact import AIGEncoder, verify_circuit  # noqa: E402

BUDGET_S = 12 * 3600
KISSAT = "kissat"
DRAT_TRIM = "/private/tmp/claude-501/-Users-lab-Claude-Projetos-7-problems/8ffb0bad-6e82-4e1b-b08b-00ff4ab65529/scratchpad/drat-trim/drat-trim"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def parse_model(stdout):
    lits = []
    for line in stdout.splitlines():
        if line.startswith("v "):
            lits.extend(int(x) for x in line[2:].split() if x != "0")
    return lits


def unsat9(hexname, tt):
    k = 9
    enc = AIGEncoder(4, k, tt).build()
    cnf = HERE / f"cert_{hexname}_k{k}.cnf"
    proof = HERE / f"cert_{hexname}_k{k}.drat"
    enc.to_dimacs(cnf)
    log(f"[unsat9 {hexname}] CNF {enc.nvars} vars / {len(enc.clauses)} cláusulas; kissat COM DRAT...")
    t0 = time.time()
    r = subprocess.run([KISSAT, "-q", str(cnf), str(proof)], capture_output=True,
                       text=True, timeout=BUDGET_S)
    dt = time.time() - t0
    assert r.returncode == 20, f"esperado UNSAT(20), veio {r.returncode}"
    log(f"[unsat9 {hexname}] UNSAT em {dt:.0f}s; DRAT = {proof.stat().st_size/1e9:.2f} GB; drat-trim...")
    t1 = time.time()
    v = subprocess.run([DRAT_TRIM, str(cnf), str(proof)], capture_output=True,
                       text=True, timeout=BUDGET_S)
    ok = "s VERIFIED" in v.stdout
    log(f"[unsat9 {hexname}] drat-trim: {'s VERIFIED' if ok else 'FALHOU: ' + v.stdout[-300:]} ({time.time()-t1:.0f}s)")
    assert ok
    log(f"[unsat9 {hexname}] CERTIFICADO: nenhum circuito AIG de 9 portas computa {hexname}")


def sat10(hexname, tt):
    k = 10
    enc = AIGEncoder(4, k, tt).build()
    cnf = HERE / f"sat_{hexname}_k{k}.cnf"
    enc.to_dimacs(cnf)
    log(f"[sat10 {hexname}] CNF {enc.nvars} vars / {len(enc.clauses)} cláusulas; kissat sem proof...")
    t0 = time.time()
    r = subprocess.run([KISSAT, "-q", str(cnf)], capture_output=True, text=True, timeout=BUDGET_S)
    dt = time.time() - t0
    assert r.returncode == 10, f"esperado SAT(10), veio {r.returncode} — se UNSAT, catálogo ub=10 está ERRADO (investigar!)"
    gates, op = enc.decode(parse_model(r.stdout))
    ok = verify_circuit(4, tt, gates, op)
    log(f"[sat10 {hexname}] SAT em {dt:.0f}s; circuito de 10 portas "
        f"{'VERIFICADO POR SIMULAÇÃO' if ok else 'FALHOU NA SIMULAÇÃO!'}")
    assert ok
    log(f"[sat10 {hexname}] circuito: {gates} out_inv={op}")


if __name__ == "__main__":
    mode, hexname, tt = sys.argv[1], sys.argv[2], int(sys.argv[3])
    {"unsat9": unsat9, "sat10": sat10}[mode](hexname, tt)
