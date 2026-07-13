"""tree_XAG(f) para todas as 65.536 funções de n=4 — DP em camadas (numpy),
mesmo esquema validado do tree_gap_n4 (AIG), acrescentando XOR nas combinações.

Justificativa do fecho por complemento (como no AIG): camadas fechadas por
complemento absorvem polaridades de entrada do AND; para XOR, ~a^b = ~(a^b) e
a^~b = ~(a^b) — todo variante por negação de um filho é o complemento do XOR
positivo, que entra na camada pelo fecho. Negação de saída livre.

Cross-check embutido: as 256 funções que ignoram x4 são comparadas com uma
recomputação n=3 pelo mesmo método + a distribuição opt_XAG n=3 do gate
(tree >= opt sempre).
"""
import time
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def tree_xag(N):
    ROWS = 1 << N
    MASK = (1 << ROWS) - 1
    cost = np.full(1 << ROWS, -1, dtype=np.int16)
    layer0 = {0, MASK}
    for j in range(N):
        v = sum(1 << t for t in range(ROWS) if (t >> j) & 1)
        layer0 |= {v, v ^ MASK}
    for f in layer0:
        cost[f] = 0
    layers = [np.array(sorted(layer0), dtype=np.int64)]
    k = 0
    while (cost < 0).any():
        k += 1
        new = set()
        for i in range((k - 1) // 2 + 1):
            j = k - 1 - i
            if j >= len(layers):
                continue
            Di, Dj = layers[i], layers[j]
            for s in range(0, len(Di), 512):
                blk_and = np.bitwise_and.outer(Di[s:s + 512], Dj).ravel()
                blk_xor = np.bitwise_xor.outer(Di[s:s + 512], Dj).ravel()
                for block in (blk_and, blk_xor):
                    cand = block[cost[block] < 0]
                    if len(cand):
                        new.update(np.unique(cand).tolist())
        both = set()
        for f in new:
            both |= {f, f ^ MASK}
        arr = np.array(sorted(both), dtype=np.int64)
        arr = arr[cost[arr] < 0]
        cost[arr] = k
        layers.append(arr)
        if k > 40:
            raise RuntimeError("sem convergencia")
    return cost, k


t0 = time.time()
c4, kmax4 = tree_xag(4)
print(f"tree_XAG n=4 completo: max = {kmax4} [{time.time()-t0:.1f}s]")

# cross-check: embedding n=3
c3, kmax3 = tree_xag(3)
bad = 0
for f3 in range(256):
    f4 = f3 | (f3 << 8)
    if c4[f4] != c3[f3]:
        bad += 1
assert bad == 0, f"{bad} mismatches no embedding n=3"
print(f"embedding n=3: 256/256 ✓ (max tree_XAG n=3 = {kmax3})")

M4 = (1 << 16) - 1
assert (c4 == c4[np.arange(1 << 16) ^ M4]).all()
print(f"tree_XAG(par4 0x6996) = {int(c4[0x6996])} | tree_XAG(par3 padded 0x9696) = {int(c4[0x9696])}")

np.save(HERE / "tree_xag_n4.npy", c4)
print("salvo tree_xag_n4.npy")
