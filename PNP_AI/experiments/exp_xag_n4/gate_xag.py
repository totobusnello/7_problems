"""Gates de validação do encoder XAG (pré-registrados no EXP-XAG-N4).

X1: sanity n=2 — AND2 e XOR2 têm opt=1; as 16 funções de n=2 conferem contra valores óbvios.
X2: n=3 COMPLETO — opt_XAG das 256 funções por encoder+kissat, cruzado com:
    (a) enumeração exaustiva INDEPENDENTE de circuitos XAG (BFS sobre conjuntos de nós,
        k até onde couber — esperado cobrir todas as 256, opt_XAG(n=3) deve ser pequeno);
    (b) invariantes: opt_XAG <= opt_AIG (tabela AIG n=3 do EXP-UNITGAP recomputada aqui
        pelo encoder AIG validado), opt_XAG(par3)=2, NPN-invariância em amostra.
"""
import sys
import os
import time
from itertools import combinations, permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exp_gate_0001"))
from xag_exact import opt_via_sat, trivial_opt
import aig_exact

# ---------- X1: n=2 ----------
print("== X1: n=2 ==", flush=True)
AND2 = 0b1000  # linhas t=0..3, bit t = (t0 AND t1)
XOR2 = 0b0110
assert opt_via_sat(2, AND2, kmax=3) == 1, "AND2 != 1"
assert opt_via_sat(2, XOR2, kmax=3) == 1, "XOR2 != 1 (porta XOR não está funcionando)"
o2 = {tt: opt_via_sat(2, tt, kmax=4) for tt in range(16)}
assert all(v is not None and v <= 2 for v in o2.values()), o2
n_trivial = sum(1 for tt in range(16) if trivial_opt(2, tt))
print(f"X1 OK: AND2=1, XOR2=1; n=2 completo: {sorted(set(o2.values()))} (max {max(o2.values())}), {n_trivial} triviais")

# ---------- X2a: enumeração exaustiva independente (n=3) ----------
print("== X2a: enumeração exaustiva XAG n=3 ==", flush=True)
N, ROWS = 3, 8
MASK = (1 << ROWS) - 1
t0 = time.time()
# estado da BFS: frozenset de tts disponíveis (fecho por complemento das entradas já
# absorvido: começamos com literais POSITIVOS e constante; AND tem polaridades explícitas)
lits = []
for j in range(N):
    lits.append(sum(1 << t for t in range(ROWS) if (t >> j) & 1))
base = tuple(sorted({0, *lits}))  # constante-0 e literais (complementos via polaridade)


def closure_opt_enum(kmax):
    """opt exato por BFS sobre multiconjuntos de valores computados.
    Estado = tupla ordenada de tts dos nós já construídos; custo = nº de portas.
    Poda: memo por conjunto (estados equivalentes)."""
    from collections import deque
    best = {}
    start = base
    seen = {start}
    dq = deque([(start, 0)])
    while dq:
        nodes, k = dq.popleft()
        for v in nodes:
            for w in (v, v ^ MASK):
                for f in (w,):
                    best.setdefault(f, k)
        # expandir
        if k == kmax:
            continue
        avail = nodes
        newstates = set()
        for a, b in combinations(avail, 2):
            for va in (a, a ^ MASK):
                for vb in (b, b ^ MASK):
                    newstates.add(va & vb)
            newstates.add(a ^ b)
        for g in newstates:
            ns = tuple(sorted(set(nodes) | {g}))
            if ns not in seen:
                seen.add(ns)
                dq.append((ns, k + 1))
    # fecho por complemento de saída
    out = {}
    for f in range(1 << ROWS):
        c = min(best.get(f, 99), best.get(f ^ MASK, 99))
        out[f] = c
    return out


KMAX_ENUM = 4
enum_opt = closure_opt_enum(KMAX_ENUM)
n_cov = sum(1 for f in range(256) if enum_opt[f] <= KMAX_ENUM)
print(f"X2a: enumeração até k={KMAX_ENUM} cobre {n_cov}/256 funções [{time.time()-t0:.0f}s]", flush=True)

# ---------- X2b: encoder+kissat nas 256 ----------
print("== X2b: encoder+kissat n=3 completo ==", flush=True)
t1 = time.time()
sat_opt = {}
for f in range(256):
    sat_opt[f] = opt_via_sat(3, f, kmax=8)
    assert sat_opt[f] is not None, f"{f:#04x} sem opt até k=8"
print(f"X2b: 256/256 em [{time.time()-t1:.0f}s]; max opt_XAG(n=3) = {max(sat_opt.values())}", flush=True)

# ---------- X2c: cruzamentos ----------
print("== X2c: cruzamentos ==", flush=True)
# (i) enum vs sat onde a enumeração cobre
mism = [f for f in range(256) if enum_opt[f] <= KMAX_ENUM and enum_opt[f] != sat_opt[f]]
assert not mism, f"enum != sat em {[(hex(f), enum_opt[f], sat_opt[f]) for f in mism[:5]]}"
# e onde a enumeração NÃO cobre, o sat tem que ser > KMAX_ENUM
mism2 = [f for f in range(256) if enum_opt[f] > KMAX_ENUM and sat_opt[f] <= KMAX_ENUM]
assert not mism2, f"sat acha k<=%d onde enum exaustiva nao achou: {mism2[:5]}" % KMAX_ENUM
# (ii) opt_XAG <= opt_AIG nas 256 (AIG pelo encoder validado do EXP-GATE-0001)
t2 = time.time()
aig_opt = {}
for f in range(256):
    if aig_exact.trivial_opt(3, f):
        aig_opt[f] = 0
        continue
    for k in range(1, 9):
        enc = aig_exact.AIGEncoder(3, k, f).build()
        if any(len(c) == 0 for c in enc.clauses):
            continue
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as fh:
            p = fh.name
            fh.write(f"p cnf {enc.nvars} {len(enc.clauses)}\n")
            for cl in enc.clauses:
                fh.write(" ".join(map(str, cl)) + " 0\n")
        rc = subprocess.run(["kissat", "-q", p], capture_output=True).returncode
        os.unlink(p)
        if rc == 10:
            aig_opt[f] = k
            break
        assert rc == 20
viol = [f for f in range(256) if sat_opt[f] > aig_opt[f]]
assert not viol, f"opt_XAG > opt_AIG em {[hex(v) for v in viol[:5]]}"
n_better = sum(1 for f in range(256) if sat_opt[f] < aig_opt[f])
print(f"X2c(ii): opt_XAG <= opt_AIG nas 256 ✓; XAG estritamente melhor em {n_better} funções [{time.time()-t2:.0f}s]")
# (iii) paridade-3
assert sat_opt[0x96] == 2, f"opt_XAG(par3) = {sat_opt[0x96]} != 2"
print(f"X2c(iii): opt_XAG(par3) = 2 ✓ (AIG era {aig_opt[0x96]})")
# (iv) NPN-invariância amostrada: permutar/negar entradas de 10 funções e comparar
import random
random.seed(20260713)
def apply_perm_neg(tt, perm, neg):
    g = 0
    for t in range(ROWS):
        u = 0
        for j in range(N):
            bit = (t >> j) & 1
            if (neg >> j) & 1:
                bit ^= 1
            u |= bit << perm[j]
        if (tt >> u) & 1:
            g |= 1 << t
    return g
for _ in range(10):
    f = random.randrange(256)
    perm = list(random.choice(list(permutations(range(N)))))
    neg = random.randrange(8)
    g = apply_perm_neg(f, perm, neg)
    assert sat_opt[f] == sat_opt[g], f"NPN quebrada: {f:#04x}->{g:#04x}"
print("X2c(iv): NPN-invariância amostrada (10 transformações) ✓")

from collections import Counter
print(f"\nDistribuição opt_XAG n=3 (256 funções): {sorted(Counter(sat_opt.values()).items())}")
print(f"Distribuição opt_AIG n=3 (256 funções): {sorted(Counter(aig_opt.values()).items())}")
print("\nGATE X1+X2: PASSOU")
