"""Censo opt_XAG nas 222 classes NPN de n=4 (EXP-XAG-N4, gate X1+X2 PASSOU).
Busca ascendente k=0,1,... por classe; modelo SAT verificado por simulação.
Saída: npn4_xag.csv + progresso no stdout.
"""
import csv
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xag_exact import opt_via_sat

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, "..", "exp_gate_0001", "npn4_opt_aig.csv")

rows = list(csv.DictReader(open(CAT)))
assert len(rows) == 222 and all(r["status"] == "exact" for r in rows)

out_path = os.path.join(HERE, "npn4_xag.csv")
done = {}
if os.path.exists(out_path):
    for r in csv.DictReader(open(out_path)):
        done[r["npn_rep_hex"]] = r

t0 = time.time()
mode = "a" if done else "w"
with open(out_path, mode, newline="") as f:
    w = csv.DictWriter(f, fieldnames=["npn_rep_hex", "npn_rep_dec", "opt_aig", "opt_xag", "t_sec"])
    if not done:
        w.writeheader()
    for i, r in enumerate(rows):
        if r["npn_rep_hex"] in done:
            continue
        tt = int(r["npn_rep_dec"])
        t1 = time.time()
        # opt_XAG <= opt_AIG sempre — usar como kmax (poda correta, não heurística)
        kmax = int(r["opt_aig"])
        opt = opt_via_sat(4, tt, kmax=kmax, verify=True)
        assert opt is not None, f"{r['npn_rep_hex']}: sem opt ate kmax={kmax} — violaria opt_XAG<=opt_AIG"
        dt = time.time() - t1
        w.writerow({"npn_rep_hex": r["npn_rep_hex"], "npn_rep_dec": tt,
                    "opt_aig": r["opt_aig"], "opt_xag": opt, "t_sec": f"{dt:.1f}"})
        f.flush()
        print(f"[{i+1}/222] {r['npn_rep_hex']}: opt_xag={opt} (aig={r['opt_aig']}) {dt:.1f}s "
              f"[total {time.time()-t0:.0f}s]", flush=True)
print("CENSO_XAG_DONE", flush=True)
