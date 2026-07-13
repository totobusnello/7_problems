"""Gate G3-style da FASE 6C (pré-requisito §6 do 14_FASE6C_DESIGN):
re-deriva opt_AIG das 222 classes NPN-4 com o NOSSO encoder fim-a-fim e
compara com o catálogo (Krinkin 220 + nossas 2). Dupla função:
(a) revalida a generalização do encoder antes do n=5;
(b) validação independente das 220 entradas do Krinkin que nunca re-derivamos.

Uso: python3 gate_n4_full.py <worker_id> <n_workers>   (resume por classe)
"""
import csv
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exp_gate_0001"))
import aig_exact
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, "..", "exp_gate_0001", "npn4_opt_aig.csv")


def opt_aig(tt, kmax=12):
    if aig_exact.trivial_opt(4, tt):
        return 0
    for k in range(1, kmax + 1):
        enc = aig_exact.AIGEncoder(4, k, tt).build()
        if any(len(c) == 0 for c in enc.clauses):
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
            p = f.name
            f.write(f"p cnf {enc.nvars} {len(enc.clauses)}\n")
            for cl in enc.clauses:
                f.write(" ".join(map(str, cl)) + " 0\n")
        rc = subprocess.run(["kissat", "-q", p], capture_output=True).returncode
        os.unlink(p)
        if rc == 10:
            return k
        assert rc == 20, f"rc={rc}"
    return None


def main():
    wid, nw = int(sys.argv[1]), int(sys.argv[2])
    rows = list(csv.DictReader(open(CAT)))
    out_path = os.path.join(HERE, f"gate_n4_out_{wid:02d}.csv")
    done = set()
    if os.path.exists(out_path):
        for r in csv.DictReader(open(out_path)):
            done.add(r["npn_rep_hex"])
    mode = "a" if done else "w"
    with open(out_path, mode, newline="") as f:
        w = csv.DictWriter(f, fieldnames=["npn_rep_hex", "opt_catalogo", "opt_rederivado", "match", "t_sec"])
        if not done:
            w.writeheader()
        for r in rows[wid::nw]:
            if r["npn_rep_hex"] in done:
                continue
            tt = int(r["npn_rep_dec"])
            cat = int(r["opt_aig"])
            t0 = time.time()
            got = opt_aig(tt)
            dt = time.time() - t0
            m = "OK" if got == cat else "MISMATCH"
            w.writerow({"npn_rep_hex": r["npn_rep_hex"], "opt_catalogo": cat,
                        "opt_rederivado": got, "match": m, "t_sec": f"{dt:.1f}"})
            f.flush()
            print(f"[w{wid}] {r['npn_rep_hex']}: cat={cat} got={got} {m} {dt:.0f}s", flush=True)
            if m == "MISMATCH":
                print(f"[w{wid}] !!! MISMATCH em {r['npn_rep_hex']} !!!", flush=True)
    print(f"[w{wid}] GATE_WORKER_DONE", flush=True)


if __name__ == "__main__":
    main()
