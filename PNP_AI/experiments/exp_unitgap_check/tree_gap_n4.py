"""Gap n=4: tree(f) para todas as 65536 funções via DP por camadas (numpy),
opt(f) do catálogo npn4_opt_aig.csv (completo, claims 0022/0023).

Modelo idêntico ao n=3 (tree_gap_n3.py): AIG, negações livres nas arestas e na
saída => cost(f) == cost(~f); custo 0 = constantes e literais; tree = fórmula
(fan-out 1): f = (+-a) AND (+-b) com a,b árvores => camadas fechadas por
complemento absorvem as polaridades.

tree e opt são NPN-invariantes (perm/neg de entrada e neg de saída são livres
no modelo AIG), então basta ler tree(rep) nas 222 representantes do catálogo.

Saída: npn4_gap.csv (classe, opt, tree, gap) + distribuição no stdout.
"""
import csv
import time
from collections import Counter
from pathlib import Path

import numpy as np

N, ROWS = 4, 16
MASK = (1 << ROWS) - 1
HERE = Path(__file__).resolve().parent
CAT = HERE.parent / "exp_gate_0001" / "npn4_opt_aig.csv"

t0 = time.time()

# --- custo 0: constantes e literais (+ complementos) ---
cost = np.full(1 << ROWS, -1, dtype=np.int16)
layer0 = {0, MASK}
for j in range(N):
    v = 0
    for t in range(ROWS):
        if (t >> j) & 1:
            v |= 1 << t
    layer0.add(v)
    layer0.add(v ^ MASK)
for f in layer0:
    cost[f] = 0
layers = [np.array(sorted(layer0), dtype=np.int64)]

# --- camadas k=1..: f = a AND b, a em D[i], b em D[j], i+j = k-1 ---
CHUNK = 512
k = 0
while (cost < 0).any():
    k += 1
    new = set()
    for i in range((k - 1) // 2 + 1):
        j = k - 1 - i
        if j >= len(layers):
            continue
        Di, Dj = layers[i], layers[j]
        for s in range(0, len(Di), CHUNK):
            block = np.bitwise_and.outer(Di[s:s + CHUNK], Dj).ravel()
            cand = block[cost[block] < 0]
            if len(cand):
                new.update(np.unique(cand).tolist())
    if not new:
        # nenhuma função nova nesta camada; segue (pode haver em k+1)
        layers.append(np.array([], dtype=np.int64))
        if k > 40:
            raise RuntimeError("sem progresso ate k=40 — bug")
        continue
    both = set()
    for f in new:
        both.add(f)
        both.add(f ^ MASK)
    arr = np.array(sorted(both), dtype=np.int64)
    arr = arr[cost[arr] < 0]  # complemento pode já ter custo menor? não — cost(f)==cost(~f); guarda mesmo assim
    cost[arr] = k
    layers.append(arr)
    done = int((cost >= 0).sum())
    print(f"k={k}: +{len(arr)} novas (total {done}/{1 << ROWS}) [{time.time() - t0:.1f}s]", flush=True)

print(f"tree completo: max tree = {k} [{time.time() - t0:.1f}s]", flush=True)

# sanity: tree(f) == tree(~f)
alltt = np.arange(1 << ROWS, dtype=np.int64)
assert (cost[alltt] == cost[alltt ^ MASK]).all(), "tree nao fechou por complemento"

# --- juncao com o catalogo opt ---
rows = list(csv.DictReader(open(CAT)))
# REV-0013 (Codex): o join deve exigir catalogo 100% exato, nao consumir
# improved_ub silenciosamente (0x1669/0x166b tinham metadado obsoleto no CSV,
# corrigido — os DRATs k=9 dos claims 0022/0023 estabelecem opt=10 exato)
nonexact = [r["npn_rep_hex"] for r in rows if r["status"] != "exact"]
assert not nonexact, f"catalogo com linhas nao-exatas: {nonexact}"
out_rows = []
dist = Counter()
viol = []
for r in rows:
    rep = int(r["npn_rep_dec"])
    opt = int(r["opt_aig"])
    tree = int(cost[rep])
    gap = tree - opt
    if gap < 0:
        viol.append((r["npn_rep_hex"], opt, tree))
    out_rows.append({"npn_rep_hex": r["npn_rep_hex"], "npn_rep_dec": rep,
                     "opt_aig": opt, "tree_aig": tree, "gap": gap})
    dist[gap] += 1

assert not viol, f"tree < opt em {viol[:5]} — bug em um dos dois"

with open(HERE / "npn4_gap.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["npn_rep_hex", "npn_rep_dec", "opt_aig", "tree_aig", "gap"])
    w.writeheader()
    w.writerows(out_rows)

print(f"\nDistribuicao de gap nas {len(out_rows)} classes NPN-4:")
for g in sorted(dist):
    print(f"  gap={g}: {dist[g]} classes")
print("\nClasses com gap maximo:")
gmax = max(dist)
for r in out_rows:
    if r["gap"] == gmax:
        print(f"  {r['npn_rep_hex']}: opt={r['opt_aig']} tree={r['tree_aig']} gap={r['gap']}")
print(f"\ntree(0x6996 = paridade-4) = {int(cost[0x6996])}")
print(f"[{time.time() - t0:.1f}s total]")
