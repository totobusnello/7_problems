"""Filtro heurístico de upper bound para n=5 SEM código externo:
UB_Shannon(f) = min sobre a variável de split e polaridade da saída de
  opt4(f|x=0) + opt4(f|x=1) + custo_mux,
onde opt4 vem do NOSSO catálogo exato certificado de n=4 (npn4_opt_aig.csv,
lookup por canonicalização NPN-4) e custo_mux(AIG) = 3 (ite = 3 ANDs), com os
casos degenerados tratados (cofatores iguais/complementares/constantes/literais).

Também UB por decomposição em 2 níveis (split em 2 variáveis, 4 cofatores de
n=3 + árvore de mux) como refinamento barato.

Calibração: roda nas 470 classes do piloto e compara com o resultado exato
(decididas) e com a censura (censored_k ⟹ opt > k... na verdade opt não
resolvido em k dentro de 2h — usamos apenas consistência UB >= opt conhecido).
"""
import csv
import json
import glob
import time
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent

# ---------- catálogo n=4 (exato, certificado) ----------
OPT4 = {}
for r in csv.DictReader(open(EXP / "exp_gate_0001" / "npn4_opt_aig.csv")):
    assert r["status"] == "exact"
    OPT4[int(r["npn_rep_dec"])] = int(r["opt_aig"])

# canonicalização NPN-4 (mesmo esquema do sample_n5, N=4)
N4, R4 = 4, 16
M4 = (1 << R4) - 1
ROWMAPS4 = []
for perm in permutations(range(N4)):
    for neg in range(1 << N4):
        rm = []
        for t in range(R4):
            u = 0
            for j in range(N4):
                bit = (t >> j) & 1
                if (neg >> j) & 1:
                    bit ^= 1
                u |= bit << perm[j]
            rm.append(u)
        ROWMAPS4.append(tuple(rm))

_canon4_cache = {}


def canon4(tt):
    if tt in _canon4_cache:
        return _canon4_cache[tt]
    best = M4 + 1
    for rm in ROWMAPS4:
        g = 0
        for t in range(R4):
            if (tt >> rm[t]) & 1:
                g |= 1 << t
        if g < best:
            best = g
        gc = g ^ M4
        if gc < best:
            best = gc
    _canon4_cache[tt] = best
    return best


def opt4(tt):
    """opt exato de uma função de 4 variáveis qualquer (lookup via NPN)."""
    return OPT4[canon4(tt)]


# ---------- cofatores de n=5 ----------
N5, R5 = 5, 32
M5 = (1 << R5) - 1


def cofactors(tt, j):
    """f|x_j=0 e f|x_j=1 como tts de 4 variáveis (nas variáveis restantes, em ordem)."""
    lo = hi = 0
    pos = 0
    for t in range(R5):
        if (t >> j) & 1:
            continue
        # linha t com x_j=0; a linha correspondente com x_j=1 é t | (1<<j)
        if (tt >> t) & 1:
            lo |= 1 << pos
        if (tt >> (t | (1 << j))) & 1:
            hi |= 1 << pos
        pos += 1
    assert pos == 16
    return lo, hi


def ub_shannon1(tt):
    """UB por split em 1 variável. Casos: f = ite(x, hi, lo).
    - hi == lo: f nao depende de x -> opt4(lo)
    - lo == 0: f = x AND hi -> opt4(hi) + 1 ; hi == 0: opt4(lo) + 1
    - lo == M4 (tudo 1): f = ~x OR hi = ~(x AND ~hi) -> opt4(hi) + 1 (negação livre)
      idem hi == M4 -> opt4(lo) + 1
    - hi == lo ^ M4: f = x XOR lo -> XOR = 3 ANDs -> opt4(lo) + 3
    - geral: mux(x, hi, lo) = 3 ANDs -> opt4(lo) + opt4(hi) + 3
    (custo de compartilhamento entre cofatores NAO é explorado — é UB.)"""
    best = 10 ** 9
    for j in range(N5):
        lo, hi = cofactors(tt, j)
        if lo == hi:
            c = opt4(lo)
        elif lo == 0 or lo == M4:
            c = opt4(hi) + 1
        elif hi == 0 or hi == M4:
            c = opt4(lo) + 1
        elif hi == (lo ^ M4):
            c = opt4(lo) + 3
        else:
            c = opt4(lo) + opt4(hi) + 3
        best = min(best, c)
    return best


def trivial5(tt):
    cands = {0, M5}
    for j in range(N5):
        v = sum(1 << t for t in range(R5) if (t >> j) & 1)
        cands |= {v, v ^ M5}
    return tt in cands


def ub_davio(tt):
    """Davio positivo/negativo: f = f0 ^ (x AND d) ou f = f1 ^ (~x AND d), d = f0^f1.
    Custo AIG: opt4(base) + opt4(d) + 1 (AND) + 3 (XOR), com degenerados:
    d == 0 -> f nao depende de x (coberto no shannon1); d constante-1 -> f = f0 ^ x (custo opt4(f0)+3)."""
    best = 10 ** 9
    for j in range(N5):
        lo, hi = cofactors(tt, j)
        d = lo ^ hi
        if d == 0:
            continue
        if d == M4:
            c = min(opt4(lo), opt4(hi)) + 3  # f = f0 ^ x (XOR com literal = 3)
        else:
            c = min(opt4(lo), opt4(hi)) + opt4(d) + 4
        best = min(best, c)
    return best


def ub(tt):
    if trivial5(tt):
        return 0
    return min(ub_shannon1(tt), ub_davio(tt))


# ---------- calibração nas classes do piloto ----------
if __name__ == "__main__":
    t0 = time.time()
    recs = []
    for d in ("out_pod", "out_pod2", "out_mac"):
        for f in glob.glob(str(EXP / "exp_pilot_n5" / d / "out_*.jsonl")):
            for line in open(f):
                if line.strip():
                    recs.append(json.loads(line))
    print(f"{len(recs)} classes do piloto carregadas")
    viol = []
    rows = []
    for r in recs:
        tt = int(r["canon_hex"], 16)
        u = ub(tt)
        opt = r.get("opt")
        ck = r.get("censored_k")
        if opt is not None and u < opt:
            viol.append((r["canon_hex"], opt, u))
        rows.append({"canon_hex": r["canon_hex"], "ub_shannon": u,
                     "opt": opt if opt is not None else "",
                     "censored_k": ck if ck is not None else ""})
    assert not viol, f"UB < opt exato (impossível se tudo certo): {viol[:5]}"
    with open(HERE / "ub_calibration.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["canon_hex", "ub_shannon", "opt", "censored_k"])
        w.writeheader()
        w.writerows(rows)

    dec = [(int(r["canon_hex"], 16), r["opt"]) for r in recs if r.get("opt") is not None]
    if dec:
        slack = [ub(tt) - o for tt, o in dec]
        from collections import Counter
        print(f"decididas ({len(dec)}): folga UB−opt = {sorted(Counter(slack).items())}")
    ubs = [row["ub_shannon"] for row in rows]
    from collections import Counter
    print(f"distribuição do UB nas 470: {sorted(Counter(ubs).items())}")
    print(f"[{time.time()-t0:.0f}s]")
