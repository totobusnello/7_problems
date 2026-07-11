"""
EXP-PROBE-0001 addendum (2026-07-11, pós-REV-0005/GLM): varredura k=1..8.

Motivação (finding v da REV-0005): o encoder pergunta "exatamente k portas";
UNSAT em k=9 sozinho não decide k<=8 sem argumento adicional. O argumento
existe (lema: se opt = m, um circuito MÍNIMO de m portas é livre de duplicatas,
com todas as portas usadas e saída na última — logo satisfaz o CNF de k=m;
UNSAT em k=m refuta opt=m). Esta varredura fecha opt >= 9 EMPIRICAMENTE,
sem depender só do lema aplicado ao k=9.

k=0 fora do SAT: 5737/5739 não são constantes nem literais (conferido abaixo).
Vereditos sem proof logging (decisão); provas DRAT só se algum k der resultado
inesperado (SAT).
"""
import subprocess, sys, time, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exp_gate_0001"))
from aig_exact import AIGEncoder, tt_bit

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def is_trivial(n, tt):
    rows = 1 << n
    if tt in (0, (1 << rows) - 1):
        return "const"
    for j in range(n):
        lit = sum(((t >> j) & 1) << t for t in range(rows))
        if tt in (lit, lit ^ ((1 << rows) - 1)):
            return f"literal x{j+1}"
    return None

for tt, name in [(5739, "0x166b"), (5737, "0x1669")]:
    triv = is_trivial(4, tt)
    print(f"{name} (tt={tt}): trivial? {triv or 'NAO (k=0 descartado)'}", flush=True)
    for k in range(1, 9):
        enc = AIGEncoder(4, k, tt).build()
        path = f"lowk_{name}_k{k}.cnf"
        enc.to_dimacs(path)
        t0 = time.time()
        r = subprocess.run(["kissat", "-q", path], capture_output=True, text=True)
        dt = time.time() - t0
        verdict = {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"RC={r.returncode}")
        print(f"{name} k={k}: {verdict} ({dt:.1f}s, {enc.nvars} vars, {len(enc.clauses)} cls)", flush=True)
        os.remove(path)
        if verdict == "SAT":
            print(f"ALERTA: {name} SAT em k={k} < 9 — contradiz UNSAT k=9; INVESTIGAR ENCODER", flush=True)

print("LOWK_SWEEP_DONE", flush=True)
