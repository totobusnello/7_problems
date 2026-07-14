"""Gate do encoder de FORMULA XAG (flag formula=True em xag_exact).
Valida tree_via_sat por DOIS caminhos independentes antes de qualquer busca:
  G-T1: DAG intacto — opt_via_sat(rep) == opt_xag do census (flag nao quebrou o DAG).
  G-T2: n=3 completo — tree_via_sat == opt para todas 256 (gap_XAG n=3 = 0, technote).
  G-T3: n=4 cross-check — tree_via_sat(rep) == tree_xag_n4.npy[rep] (DP independente)
        para TODAS as 222 classes-rep, cobrindo as 4 com gap=1 (nao so gap=0).
"""
import sys, os, csv, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from xag_exact import opt_via_sat, tree_via_sat

tree_dp = np.load(os.path.join(HERE, "tree_xag_n4.npy"))
rows = list(csv.DictReader(open(os.path.join(HERE, "npn4_xag.csv"))))

# ---- G-T2: n=3 completo, tree == opt ----
t0 = time.time()
bad3 = []
for f in range(256):
    o = opt_via_sat(3, f)
    t = tree_via_sat(3, f, start=o)
    if t != o:
        bad3.append((f, o, t))
assert not bad3, f"G-T2 FALHOU (n=3 gap!=0): {[(hex(f), o, t) for f, o, t in bad3[:5]]}"
print(f"G-T2 OK: n=3 256/256 tree==opt (gap 0) [{time.time()-t0:.0f}s]", flush=True)

# ---- G-T1 + G-T3: n=4, todas as 222 classes ----
t1 = time.time()
gap_dist = {}
bad_opt = bad_tree = []
for r in rows:
    rep = int(r["npn_rep_dec"])
    opt_cat = int(r["opt_xag"])
    o = opt_via_sat(4, rep)
    if o != opt_cat:
        bad_opt.append((r["npn_rep_hex"], opt_cat, o))
    t_sat = tree_via_sat(4, rep, start=o)
    t_dp = int(tree_dp[rep])
    if t_sat != t_dp:
        bad_tree.append((r["npn_rep_hex"], t_sat, t_dp))
    gap_dist[t_dp - o] = gap_dist.get(t_dp - o, 0) + 1
assert not bad_opt, f"G-T1 FALHOU (opt DAG diverge do census): {bad_opt[:5]}"
assert not bad_tree, f"G-T3 FALHOU (SAT-formula != DP): {bad_tree[:5]}"
print(f"G-T1 OK: opt_via_sat bate com census XAG em 222/222 (DAG intacto)", flush=True)
print(f"G-T3 OK: tree_via_sat bate com a DP em 222/222 classes [{time.time()-t1:.0f}s]", flush=True)
print(f"gap_XAG n=4 (reconferido): {dict(sorted(gap_dist.items()))}")
n_gap1 = gap_dist.get(1, 0)
assert n_gap1 >= 1, "amostra sem gap=1 — o gate nao exercitou deteccao de gap!"
print(f"  (cobriu {n_gap1} classes com gap=1 — encoder DETECTA formula > opt)")
print("\nGATE FORMULA XAG: PASSOU")
