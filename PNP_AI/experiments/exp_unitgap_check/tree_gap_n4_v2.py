"""2ª implementação INDEPENDENTE do tree(f) n=4 (para o claim 0026):
Bellman fixed-point global — relaxa custo[f] = min(custo[f], 1 + custo[a] + custo[b])
sobre TODOS os pares (a,b) com f = a AND b, varrendo até ponto fixo, SEM camadas.

Diferenças estruturais vs tree_gap_n4.py (BFS por camadas):
- ordem de descoberta diferente (relaxação global, não frontier);
- polaridades tratadas EXPLICITAMENTE: para cada par (a,b) relaxa as 4 combinações
  (a&b, a&~b, ~a&b, ~a&~b) e o complemento da saída — NADA de "camada fechada por
  complemento" (se aquela absorção estiver errada, esta versão diverge);
- custo inicial INF (int32) em vez de -1 sentinel.

Compara as 65.536 células com a saída da v1 recomputada na hora.
"""
import time

import numpy as np

N, ROWS = 4, 16
MASK = (1 << ROWS) - 1
INF = np.int32(10 ** 6)

t0 = time.time()

cost = np.full(1 << ROWS, INF, dtype=np.int32)
cost[0] = cost[MASK] = 0
for j in range(N):
    v = sum(1 << t for t in range(ROWS) if (t >> j) & 1)
    cost[v] = cost[v ^ MASK] = 0

CHUNK = 256
sweep = 0
while True:
    sweep += 1
    changed = 0
    known = np.nonzero(cost < INF)[0]
    kc = cost[known]
    # ordena por custo p/ relaxar barato-primeiro (acelera convergência, não muda o ponto fixo)
    order = np.argsort(kc, kind="stable")
    known, kc = known[order], kc[order]
    for s in range(0, len(known), CHUNK):
        A = known[s:s + CHUNK]
        cA = kc[s:s + CHUNK]
        for a, ca in zip(A.tolist(), cA.tolist()):
            newc = 1 + ca + kc  # custo do AND com cada b conhecido
            for aa in (a, a ^ MASK):
                for bvec in (known, known ^ MASK):
                    f = np.bitwise_and(aa, bvec)
                    # relaxa f e ~f (negação de saída livre)
                    for g in (f, f ^ MASK):
                        upd = newc < cost[g]
                        if upd.any():
                            np.minimum.at(cost, g[upd], newc[upd])
                            changed += int(upd.sum())
    print(f"sweep {sweep}: {changed} relaxações [{time.time() - t0:.0f}s]", flush=True)
    if changed == 0:
        break

assert (cost < INF).all(), "funções inalcançáveis — bug"
print(f"ponto fixo em {sweep} sweeps; max tree = {int(cost.max())} [{time.time() - t0:.0f}s]")

# --- recomputa a v1 (BFS por camadas) e compara célula a célula ---
c1 = np.full(1 << ROWS, -1, dtype=np.int16)
layer0 = {0, MASK}
for j in range(N):
    v = sum(1 << t for t in range(ROWS) if (t >> j) & 1)
    layer0 |= {v, v ^ MASK}
for f in layer0:
    c1[f] = 0
layers = [np.array(sorted(layer0), dtype=np.int64)]
k = 0
while (c1 < 0).any():
    k += 1
    new = set()
    for i in range((k - 1) // 2 + 1):
        j = k - 1 - i
        if j >= len(layers):
            continue
        Di, Dj = layers[i], layers[j]
        for s in range(0, len(Di), 512):
            block = np.bitwise_and.outer(Di[s:s + 512], Dj).ravel()
            cand = block[c1[block] < 0]
            if len(cand):
                new.update(np.unique(cand).tolist())
    both = set()
    for f in new:
        both |= {f, f ^ MASK}
    arr = np.array(sorted(both), dtype=np.int64)
    arr = arr[c1[arr] < 0]
    c1[arr] = k
    layers.append(arr)

diff = np.nonzero(cost.astype(np.int64) != c1.astype(np.int64))[0]
if len(diff):
    for f in diff[:10]:
        print(f"DIVERGÊNCIA {f:#06x}: v2={int(cost[f])} v1={int(c1[f])}")
    raise SystemExit(f"FALHOU: {len(diff)} células divergem")
print(f"v2 (Bellman) == v1 (camadas) em TODAS as 65.536 células ✓")
print(f"tree(0x6996) = {int(cost[0x6996])} | [{time.time() - t0:.0f}s total]")
