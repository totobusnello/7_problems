"""
EXP-PILOT-N5 — runner do piloto (roda no pod, Python 3.8+, stdlib apenas).

Por classe: busca ascendente k=0,1,2,... até SAT (verificado por SIMULAÇÃO —
regra do programa) ou até estourar o budget de 7200s/classe (classe vira
CENSORED — dado, não falha). SEM proof logging (fase de medição; lição do
EXP-PROBE-0001). Registra tempos por k e tamanhos de CNF.

Uso: python3 pilot_run.py <shard.jsonl> <out.jsonl>
"""
import json
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aig_exact import AIGEncoder, trivial_opt, verify_circuit

N = 5
CLASS_BUDGET = 7200.0   # s, pré-registrado no 13_FASE6_PLAN
KMAX = 20               # tampa de sanidade (não deve ser atingida)
KISSAT = "kissat"


def parse_model(out):
    lits = []
    for line in out.splitlines():
        if line.startswith("v "):
            lits.extend(int(x) for x in line[2:].split())
    return [l for l in lits if l != 0]


def run_class(rec):
    tt = rec["canon_dec"]
    t_class = time.time()
    result = {**rec, "opt": None, "censored_k": None, "times": {}, "cnf": {}, "witness": None}

    if trivial_opt(N, tt):
        result["opt"] = 0
        return result

    for k in range(1, KMAX + 1):
        remaining = CLASS_BUDGET - (time.time() - t_class)
        if remaining <= 5:
            result["censored_k"] = k
            return result
        enc = AIGEncoder(N, k, tt).build()
        result["cnf"][str(k)] = [enc.nvars, len(enc.clauses)]
        if any(len(c) == 0 for c in enc.clauses):
            result["times"][str(k)] = 0.0
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
            path = f.name
            f.write(f"p cnf {enc.nvars} {len(enc.clauses)}\n")
            for cl in enc.clauses:
                f.write(" ".join(map(str, cl)) + " 0\n")
        t0 = time.time()
        try:
            p = subprocess.run([KISSAT, "-q", path], capture_output=True,
                               text=True, timeout=remaining)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            rc = None
        dt = time.time() - t0
        os.unlink(path)
        result["times"][str(k)] = round(dt, 2)
        if rc == 10:
            gates, op = enc.decode(parse_model(p.stdout))
            assert verify_circuit(N, tt, gates, op), f"SIMULACAO FALHOU {rec['canon_hex']} k={k}"
            result["opt"] = k
            result["witness"] = {"gates": gates, "out_pol": op}
            return result
        if rc == 20:
            continue
        result["censored_k"] = k   # timeout ou retorno inesperado
        if rc not in (None, 20):
            result["rc_unexpected"] = rc
        return result
    result["censored_k"] = KMAX + 1
    return result


def main():
    shard, out = sys.argv[1], sys.argv[2]
    done = set()
    if os.path.exists(out):  # retomada
        with open(out) as f:
            for line in f:
                try:
                    done.add(json.loads(line)["canon_hex"])
                except Exception:
                    pass
    with open(shard) as f:
        recs = [json.loads(l) for l in f]
    with open(out, "a") as fo:
        for rec in recs:
            if rec["canon_hex"] in done:
                continue
            r = run_class(rec)
            fo.write(json.dumps(r) + "\n")
            fo.flush()
    print("SHARD_DONE", shard)


if __name__ == "__main__":
    main()
