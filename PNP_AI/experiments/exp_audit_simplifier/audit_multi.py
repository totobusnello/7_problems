"""Auditoria das entradas multi-output da database AIG do Simplifier.

Por entrada: parse -> simulação valida os tts declarados (convenção x0=MSB,
refs forward) -> k_deles = #ANDs -> certificação (cap de TIMEOUT_S por SAT):
  - trivial (k=0 alcançável): compara direto;
  - senão, SAT em k_deles-1? UNSAT => entrada ÓTIMA (circuito deles é mínimo);
    SAT => SUBÓTIMA: desce até UNSAT (opt fechado) e registra o circuito melhorado.

Veredictos: OPTIMAL | SUBOPTIMAL (opt fechado) | SUBOPT_UB (melhoria certificada
por simulação, mas o mínimo exato não foi fechado antes do timeout) | INCONCLUSIVE
(timeout já no 1º teste — entrada não auditada). O timeout NÃO afeta o rigor das
melhorias emitidas (toda uma é verificada por simulação); afeta só a certificação
de otimalidade da cauda cara.

Uso: python3 audit_multi.py <n_out:2|3> <worker_id> <n_workers>
Saída: audit_<nout>out_w<id>.csv + melhorias em improved_<nout>out_w<id>.jsonl
Resume por índice de linha. TIMEOUT_S ajustável no topo.
"""
import csv
import json
import sys
import os
import time
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multi_aig_exact import solve_k, trivial_multi

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "database_aig.txt")
TIMEOUT_S = 30  # cap por chamada SAT; estouro => nao-decidido (rigor intacto)


def solve_k_to(tts, k):
    """solve_k com cap de tempo. Retorna 'UNSAT' | ('SAT', cert) | 'TIMEOUT'.
    O cap so afeta a CERTIFICACAO de otimalidade: toda melhoria emitida segue
    verificada por simulacao dentro de solve_k. Estouro no 1o teste => a entrada
    fica 'nao-decidida'; estouro na descida => temos UB certificado (nao o minimo)."""
    try:
        sat, cert = solve_k(3, tts, k, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    return ("SAT", cert) if sat else "UNSAT"


def parse_line(line):
    parts = line.split()
    n_in, n_out = int(parts[0]), int(parts[1])
    tts = [int(x) for x in parts[2:2 + n_out]]
    outs = [int(x) for x in parts[2 + n_out:2 + 2 * n_out]]
    toks = parts[2 + 2 * n_out:]
    gatedef = {}
    node = n_in
    i = 0
    while i < len(toks):
        if toks[i] == "NOT":
            gatedef[node] = ("NOT", int(toks[i + 1])); i += 2
        else:
            gatedef[node] = ("AND", int(toks[i + 1]), int(toks[i + 2])); i += 3
        node += 1
    return n_in, n_out, tts, outs, gatedef


def eval_node(gatedef, node, iv, memo):
    if node in memo:
        return memo[node]
    g = gatedef[node]
    v = (eval_node(gatedef, g[1], iv, memo) ^ 1) if g[0] == "NOT" else \
        (eval_node(gatedef, g[1], iv, memo) & eval_node(gatedef, g[2], iv, memo))
    memo[node] = v
    return v


def declared_tts_ok(n_in, tts, outs, gatedef):
    got = [0] * len(outs)
    for t in range(1 << n_in):
        iv = {j: (t >> (n_in - 1 - j)) & 1 for j in range(n_in)}  # x0 = MSB
        memo = dict(iv)
        for o, nd in enumerate(outs):
            if eval_node(gatedef, nd, iv, memo):
                got[o] |= 1 << t
    return got == tts


def main():
    n_out, wid, nw = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    out_csv = os.path.join(HERE, f"audit_{n_out}out_w{wid:02d}.csv")
    out_imp = os.path.join(HERE, f"improved_{n_out}out_w{wid:02d}.jsonl")
    done = set()
    if os.path.exists(out_csv):
        for r in csv.DictReader(open(out_csv)):
            done.add(int(r["line_idx"]))
    entries = []
    with open(DB) as f:
        for idx, line in enumerate(f):
            if line.startswith(f"3 {n_out} "):
                entries.append((idx, line.rstrip("\n")))
    mine = entries[wid::nw]
    t0 = time.time()
    mode = "a" if done else "w"
    with open(out_csv, mode, newline="") as fc, open(out_imp, "a") as fi:
        w = csv.DictWriter(fc, fieldnames=["line_idx", "tts", "k_theirs", "k_opt", "verdict", "t_sec"])
        if not done:
            w.writeheader()
        n_done = n_opt = n_sub = 0
        for idx, line in mine:
            if idx in done:
                continue
            n_in, no, tts, outs, gatedef = parse_line(line)
            assert declared_tts_ok(n_in, tts, outs, gatedef), f"linha {idx}: tts nao conferem"
            k_theirs = sum(1 for g in gatedef.values() if g[0] == "AND")
            t1 = time.time()
            certified = True  # opt fechado por UNSAT (True) ou apenas UB (False)
            if trivial_multi(3, tts):
                k_opt = 0
                verdict = "OPTIMAL" if k_theirs == 0 else "SUBOPTIMAL"
                if k_theirs > 0:
                    fi.write(json.dumps({"line_idx": idx, "tts": tts,
                                         "k_theirs": k_theirs, "k_opt": 0,
                                         "gates": [], "outs": None,
                                         "certified_opt": True}) + "\n")
                    fi.flush()
            else:
                first = solve_k_to(tts, k_theirs - 1) if k_theirs >= 1 else "UNSAT"
                if first == "TIMEOUT":
                    k_opt = -1
                    verdict = "INCONCLUSIVE"
                elif first == "UNSAT":
                    k_opt = k_theirs
                    verdict = "OPTIMAL"
                else:  # ('SAT', cert): subotima. desce ate UNSAT ou timeout
                    k_opt = k_theirs - 1
                    best_cert = first[1]
                    while k_opt >= 1:
                        r = solve_k_to(tts, k_opt - 1)
                        if r == "TIMEOUT":
                            certified = False  # opt <= k_opt; minimo nao fechado
                            break
                        if r == "UNSAT":
                            break
                        k_opt -= 1
                        best_cert = r[1]
                    gates, o = best_cert
                    verdict = "SUBOPTIMAL" if certified else "SUBOPT_UB"
                    fi.write(json.dumps({"line_idx": idx, "tts": tts,
                                         "k_theirs": k_theirs, "k_opt": k_opt,
                                         "gates": gates, "outs": o,
                                         "certified_opt": certified}) + "\n")
                    fi.flush()
            n_done += 1
            n_opt += verdict == "OPTIMAL"
            n_sub += verdict in ("SUBOPTIMAL", "SUBOPT_UB")
            w.writerow({"line_idx": idx, "tts": json.dumps(tts), "k_theirs": k_theirs,
                        "k_opt": k_opt, "verdict": verdict, "t_sec": f"{time.time()-t1:.2f}"})
            fc.flush()
            if n_done % 200 == 0:
                print(f"[w{wid}] {n_done}/{len(mine)} (opt {n_opt}, sub {n_sub}) "
                      f"[{time.time()-t0:.0f}s]", flush=True)
    print(f"[w{wid}] AUDIT_WORKER_DONE: {n_done} entradas, {n_opt} ótimas, {n_sub} subótimas", flush=True)


if __name__ == "__main__":
    main()
