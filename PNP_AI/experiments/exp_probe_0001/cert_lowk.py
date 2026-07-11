"""
EXP-PROBE-0001 — certificação DRAT da varredura k=1..8 (fecho do finding 3 da
REV-0008/Kimi: a varredura era não-certificada; certificar é barato porque os
CNFs são pequenos). Sequencial: gerar prova -> drat-trim -> registrar hash ->
apagar prova. Saída: cert_lowk.log + cert_lowk_results.jsonl
"""
import hashlib
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exp_gate_0001"))
from aig_exact import AIGEncoder

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DT = "/private/tmp/claude-501/-Users-lab-Claude-Projetos-7-problems/8ffb0bad-6e82-4e1b-b08b-00ff4ab65529/scratchpad/drat-trim/drat-trim"
if not os.path.exists(DT):
    DT = "drat-trim"  # fallback: PATH

out = open("cert_lowk_results.jsonl", "a")
for tt, name in [(5739, "0x166b"), (5737, "0x1669")]:
    for k in range(1, 9):
        cnf, drat = f"lowk_{name}_k{k}.cnf", f"lowk_{name}_k{k}.drat"
        enc = AIGEncoder(4, k, tt).build()
        enc.to_dimacs(cnf)
        t0 = time.time()
        p = subprocess.run(["kissat", "-q", cnf, drat], capture_output=True, text=True)
        t_solve = time.time() - t0
        assert p.returncode == 20, f"{name} k={k}: esperado UNSAT(20), veio {p.returncode}"
        proof_bytes = os.path.getsize(drat)
        h = hashlib.sha256(open(drat, "rb").read()).hexdigest()
        t1 = time.time()
        q = subprocess.run([DT, cnf, drat], capture_output=True, text=True)
        t_check = time.time() - t1
        verified = "s VERIFIED" in q.stdout
        rec = {"class": name, "k": k, "unsat": True, "proof_bytes": proof_bytes,
               "proof_sha256": h, "drat_trim": "s VERIFIED" if verified else "FALHOU",
               "t_solve": round(t_solve, 2), "t_check": round(t_check, 2)}
        out.write(json.dumps(rec) + "\n"); out.flush()
        print(f"{name} k={k}: UNSAT, prova {proof_bytes/1e6:.1f}MB, "
              f"{'s VERIFIED' if verified else 'FALHOU!!'} ({t_solve:.1f}s+{t_check:.1f}s)", flush=True)
        os.unlink(cnf); os.unlink(drat)
print("CERT_LOWK_DONE", flush=True)
