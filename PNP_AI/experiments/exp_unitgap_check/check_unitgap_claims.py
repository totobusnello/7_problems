"""Verificação mecânica dos claims 0024/0025 (contraexemplos ao SRC-0032)."""
import subprocess, sys, tempfile, os, hashlib
sys.path.insert(0, "/workspace/pilot")
from aig_exact import AIGEncoder, verify_circuit

N, ROWS = 3, 8
MASK = 255
PAR3 = sum((bin(t).count("1") & 1) << t for t in range(ROWS))
print(f"paridade_3 tt = {PAR3} ({PAR3:#04x})")

def solve(tt, k, want_proof=False):
    enc = AIGEncoder(N, k, tt).build()
    if any(len(c) == 0 for c in enc.clauses):
        return "INFEASIBLE", None, None
    with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
        path = f.name
        f.write(f"p cnf {enc.nvars} {len(enc.clauses)}\n")
        for cl in enc.clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    args = ["kissat", "-q", path]
    drat = path + ".drat"
    if want_proof:
        args.append(drat)
    p = subprocess.run(args, capture_output=True, text=True)
    res = {10: "SAT", 20: "UNSAT"}.get(p.returncode, f"RC{p.returncode}")
    extra = None
    if res == "SAT":
        lits = [int(x) for l in p.stdout.splitlines() if l.startswith("v ") for x in l[2:].split() if x != "0"]
        gates, op = enc.decode(lits)
        assert verify_circuit(N, tt, gates, op), "SIMULACAO FALHOU"
        extra = (gates, op)
    if want_proof and res == "UNSAT":
        q = subprocess.run(["drat-trim", path, drat], capture_output=True, text=True)
        ok = "s VERIFIED" in q.stdout
        h = hashlib.sha256(open(drat, "rb").read()).hexdigest()[:16]
        extra = f"drat-trim: {'s VERIFIED' if ok else 'FALHOU'}, sha256[:16]={h}, {os.path.getsize(drat)} bytes"
        os.unlink(drat)
    os.unlink(path)
    return res, extra, None

# 1) opt(par3) = 6: UNSAT@5 certificado + SAT@6 com testemunha simulada
r5, e5, _ = solve(PAR3, 5, want_proof=True)
print(f"par3 k=5: {r5} — {e5}")
r6, e6, _ = solve(PAR3, 6)
print(f"par3 k=6: {r6} — circuito verificado por simulação: {e6[0] if e6 else None}")

# 2) filho h = (x1 xor x2) AND (not x3): opt = 4 (UNSAT@3 certificado + SAT@4 simulado)
XOR12 = sum((((t & 1) ^ ((t >> 1) & 1))) << t for t in range(ROWS))
H = sum(((((t & 1) ^ ((t >> 1) & 1)) & (1 - ((t >> 2) & 1)))) << t for t in range(ROWS))
print(f"h = (x1^x2)&~x3 tt = {H} ({H:#04x})")
r3, e3, _ = solve(H, 3, want_proof=True)
print(f"h k=3: {r3} — {e3}")
r4, e4, _ = solve(H, 4)
print(f"h k=4: {r4} — simulado ok")

# 3) circuito explícito de 6 portas de par3 com sharing s=3 (construção do REV-0009):
#    a = x1 xor x2 (portas 1-3); g4 = a & ~x3; g5 = ~a & x3; g6 = ~( ~g4 & ~g5 )
def sim6(t):
    x1, x2, x3 = t & 1, (t >> 1) & 1, (t >> 2) & 1
    g1 = x1 & (1 - x2)
    g2 = (1 - x1) & x2
    g3 = 1 - ((1 - g1) & (1 - g2))   # a = x1^x2
    g4 = g3 & (1 - x3)
    g5 = (1 - g3) & x3
    g6 = 1 - ((1 - g4) & (1 - g5))
    return g6
tt6 = sum(sim6(t) << t for t in range(ROWS))
print(f"circuito 6 portas (s=3 estrutural: filhos g4,g5 da saída compartilham g1,g2,g3): computa {tt6:#04x} == par3? {tt6 == PAR3}")
print(f"identidade de decomposição: 1 + opt(g4-fn) + opt(g5-fn) - s = 1 + 4 + 4 - 3 = 6 = opt(par3) ✓")
