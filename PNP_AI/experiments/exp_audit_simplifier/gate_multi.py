"""Gates do encoder multi-output (pré-registrados no EXP-AUDIT-SIMPLIFIER).

G-M1: redução single-output — as 256 tts de n=3 com m=1 reproduzem a tabela opt3
      certificada (encoder single validado por G1-G3 + gate 222/222).
G-M2: identidades e enumeração — (f,~f) custa opt(f) p/ amostra; pares (f,g)
      amostrados vs enumeração exaustiva multi-alvo até k=4.
"""
import sys
import os
import time
import random
from itertools import combinations
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exp_gate_0001"))
from multi_aig_exact import opt_multi
import aig_exact
import subprocess
import tempfile

N, ROWS = 3, 8
MASK = 255

# tabela opt3 certificada (recomputada pelo encoder single validado)
t0 = time.time()
opt3 = {}
for f in range(256):
    if aig_exact.trivial_opt(3, f):
        opt3[f] = 0
        continue
    for k in range(1, 9):
        enc = aig_exact.AIGEncoder(3, k, f).build()
        if any(len(c) == 0 for c in enc.clauses):
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as fh:
            p = fh.name
            fh.write(f"p cnf {enc.nvars} {len(enc.clauses)}\n")
            for cl in enc.clauses:
                fh.write(" ".join(map(str, cl)) + " 0\n")
        rc = subprocess.run(["kissat", "-q", p], capture_output=True).returncode
        os.unlink(p)
        if rc == 10:
            opt3[f] = k
            break
        assert rc == 20
print(f"opt3 ref pronto [{time.time()-t0:.0f}s]", flush=True)

# ---------- G-M1 ----------
print("== G-M1: redução single-output (256 tts) ==", flush=True)
t1 = time.time()
bad = []
for f in range(256):
    got = opt_multi(3, [f])
    if got != opt3[f]:
        bad.append((f, got, opt3[f]))
assert not bad, f"G-M1 FALHOU: {[(hex(f), g, o) for f, g, o in bad[:5]]}"
print(f"G-M1 OK: 256/256 batem com a tabela certificada [{time.time()-t1:.0f}s]", flush=True)

# ---------- G-M2a: (f, ~f) custa opt(f) ----------
print("== G-M2a: (f, ~f) ==", flush=True)
random.seed(20260713)
for f in random.sample(range(256), 20):
    got = opt_multi(3, [f, f ^ MASK])
    assert got == opt3[f], f"(f,~f) f={f:#04x}: got={got} esperado={opt3[f]}"
print("G-M2a OK: 20 amostras — negação de saída é grátis também no multi-output")

# ---------- G-M2b: pares vs enumeração exaustiva multi-alvo ----------
print("== G-M2b: pares (f,g) vs enumeração exaustiva ==", flush=True)
t2 = time.time()
lits = [sum(1 << t for t in range(ROWS) if (t >> j) & 1) for j in range(N)]
base = tuple(sorted({0, *lits}))


def enum_multi_opt(targets, kmax):
    """menor k tal que existe conjunto de nós construído com k ANDs contendo
    todos os alvos (a menos de complemento)."""
    tset = [{t, t ^ MASK} for t in targets]

    def covered(nodes):
        ns = set(nodes)
        return all(ns & alt for alt in tset)

    seen = {base}
    dq = deque([(base, 0)])
    while dq:
        nodes, k = dq.popleft()
        if covered(nodes):
            return k
        if k == kmax:
            continue
        news = set()
        for a, b in combinations(nodes, 2):
            for va in (a, a ^ MASK):
                for vb in (b, b ^ MASK):
                    news.add(va & vb)
        for g in news:
            ns = tuple(sorted(set(nodes) | {g}))
            if ns not in seen:
                seen.add(ns)
                dq.append((ns, k + 1))
    return None


checked = 0
cheap = [f for f in range(256) if opt3[f] <= 2]  # pares com soma <= 4: enum alcança
for _ in range(25):
    f, g = random.sample(cheap, 2)
    ref = enum_multi_opt([f, g], kmax=4)
    if ref is None:
        continue  # par caro demais p/ enum — pula (amostra cobre os baratos)
    got = opt_multi(3, [f, g])
    assert got == ref, f"par ({f:#04x},{g:#04x}): sat={got} enum={ref}"
    checked += 1
assert checked >= 5, f"amostra insuficiente ({checked})"
print(f"G-M2b OK: {checked} pares batem com a enumeração exaustiva [{time.time()-t2:.0f}s]")

# ---------- G-M2c: compartilhamento real ----------
print("== G-M2c: sanity de compartilhamento ==", flush=True)
AND3 = 0b10000000  # x0&x1&x2
AND2 = 0b10001000  # x0&x1
got = opt_multi(3, [AND2, AND3])
assert got == 2, f"(x0&x1, x0&x1&x2) deveria custar 2, deu {got}"
print("G-M2c OK: (x0&x1, x0&x1&x2) = 2 (compartilha)")

print("\nGATE MULTI-OUTPUT: PASSOU")
