"""Completa a cadeia DRAT do child h=(x1⊕x2)∧¬x3 (opt=4): gera UNSAT DRAT em k=1,2
(o k=3 já existe como h_child_k3). Fecha o achado REV-0017-r2/Codex I2: no encoder de
tamanho-exato, opt(h)≥4 exige UNSAT em k=1,2,3, não só k=3.
"""
import sys, subprocess, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "exp_gate_0001"))
from aig_exact import AIGEncoder

N, ROWS = 3, 8
# h = (x1 xor x2) and (not x3)
H = sum(((((t & 1) ^ ((t >> 1) & 1)) & (1 - ((t >> 2) & 1)))) << t for t in range(ROWS))
CERTS = os.path.join(HERE, "certs")
print(f"h child tt = {H:#04x}")

for k in [1, 2]:
    enc = AIGEncoder(N, k, H).build()
    empty = any(len(c) == 0 for c in enc.clauses)
    cnf_path = os.path.join(CERTS, f"h_child_k{k}.cnf")
    with open(cnf_path, "w") as f:
        f.write(f"p cnf {enc.nvars} {len(enc.clauses)}\n")
        for cl in enc.clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    if empty:
        ch = hashlib.sha256(open(cnf_path, "rb").read()).hexdigest()[:16]
        print(f"k={k}: UNSAT SINTATICO (clausula vazia). cnf sha[:16]={ch}")
        continue
    drat_path = os.path.join(CERTS, f"h_child_k{k}.drat")
    p = subprocess.run(["kissat", "-q", cnf_path, drat_path], capture_output=True, text=True)
    res = {10: "SAT", 20: "UNSAT"}.get(p.returncode, f"RC{p.returncode}")
    dh = hashlib.sha256(open(drat_path, "rb").read()).hexdigest()[:16]
    print(f"k={k}: {res}, drat {os.path.getsize(drat_path)} bytes, drat_sha[:16]={dh}")
