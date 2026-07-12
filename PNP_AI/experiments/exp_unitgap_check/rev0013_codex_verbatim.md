Reading additional input from stdin...
OpenAI Codex v0.144.1
--------
workdir: /Users/lab/Claude/Projetos/7_problems
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: 019f53d8-e428-77f2-8aca-a9b2a9fddc7b
--------
user
ADVERSARIAL REVIEW (REV-0013) — try to REFUTE claim 7P-PNP-CLM-0026 before confirming it.

CLAIM: In the AIG cost model (2-input AND gates; negations free on edges AND on the output; cost 0 = constants and literals), define tree(f) = minimum gate count of a FORMULA (fan-out 1, i.e. children of every gate are themselves formulas) computing f or its complement, and opt(f) = minimum gate count of a circuit (DAG, sharing allowed). Claim: over the 222 NPN classes of n=4 boolean functions, the distribution of gap = tree - opt is {0: 93, 1: 57, 2: 40, 3: 13, 4: 14, 5: 2, 6: 3}; max gap = 6 attained exactly by classes 0x1668, 0x16e9, 0x6996 (parity-4 and relatives), with opt=9, tree=15; max tree over n=4 = 15.

YOUR TASKS, IN ORDER:
1. INDEPENDENT re-derivation FIRST (do not read our script before doing this): write and run YOUR OWN implementation of the tree DP for n=4 (65536 truth tables; closure under complement absorbs edge polarities — justify this yourself or choose your own equivalent formulation). Compute tree(f) for all 65536 functions and report: (a) max tree, (b) tree(0x6996), (c) the number of new functions per cost level. You may run python3 inline (read-only sandbox: compute in memory, print results, do not write files).
2. Only THEN read our implementation at PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py and outputs (tree_gap_n4_out.txt, npn4_gap.csv) and attack: soundness of the layered DP (does closure-under-complement correctly absorb all 4 polarity combinations of f = (+-a) AND (+-b)? is cost-0 seeding right? any way the DP can UNDERcount or OVERcount tree size?), the NPN-invariance argument for both tree and opt, and the join with the opt catalog at PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv.
3. Check the Khrapchenko application: for parity-4, does Khrapchenko's bound |E|^2/(|A||B|) really give >= 16 leaves, hence >= 15 gates for a binary-AND formula with free negations? State the A,B sets and the count explicitly.
4. VERDICT: SUSTAINED or REFUTED, with your independently computed distribution vs ours, and any discrepancy explained.

Rules: cite exact numbers from your own run; if your distribution differs from ours, that is a FINDING, not an error to reconcile silently.
2026-07-12T01:02:32.028289Z ERROR codex_memories_write::phase2: Phase 2 no changes
hook: SessionStart
hook: SessionStart Completed
codex
I’ll first derive and execute an in-memory formula DP without opening any project files. I’ll record its layer counts and key values, then inspect the supplied implementation and catalogs only after that independent result is fixed.
codex
The shell tried to materialize the heredoc as a temporary file, which the read-only environment blocks. I’m rerunning the same independent DP via `python3 -c`, still entirely in memory and without inspecting the repository.
exec
/bin/zsh -lc "python3 -c '
MASK=(1<<16)-1
def canon(f):
 g=f"'^MASK
 return f if f<g else g
variables=[]
for bit in range(4):
 tt=0
 for assignment in range(16):
  if (assignment>>bit)&1: tt |= 1<<assignment
 variables.append(tt)
seen={canon(0)}
seen.update(canon(x) for x in variables)
layers=[set(seen)]
cost={f:0 for f in seen}
k=1
while len(seen)<32768:
 new=set()
 for i in range(k):
  j=k-1-i
  if j<0 or j>=len(layers) or i>j: continue
  lefts,rights=layers[i],layers[j]
  for a in lefts:
   for b in rights:
    if i==j and b<a: continue
    for pa in (a,a''^MASK):
     for pb in (b,b''^MASK):
      out=canon(pa&pb)
      if out not in seen: new.add(out)
 for f in new: cost[f]=k
 layers.append(new)
 seen.update(new)
 print("cost %d: new complement-classes=%d, new functions=%d, cumulative functions=%d"%(k,len(new),2*len(new),2*len(seen)))
 if not new: raise RuntimeError("closure stalled")
 k+=1
print("max_tree",max(cost.values()))
print("tree_0x6996",cost[canon(0x6996)])
print("cost0 complement-classes",len(layers[0]),"cost0 functions",2*len(layers[0]))
print("new_functions_per_cost",{i:2*len(s) for i,s in enumerate(layers)})
'"'" in /Users/lab/Claude/Projetos/7_problems
exec
/bin/zsh -lc "python3 -u -c '
MASK=65535
C=lambda f:min(f,f"'^MASK)
vs=[]
for bit in range(4):
 t=0
 for a in range(16):
  if (a>>bit)&1:t|=1<<a
 vs.append(t)
seen={C(0),*[C(x) for x in vs]}; layers=[set(seen)]; cost={x:0 for x in seen}
k=1
while len(seen)<32768:
 new=set()
 for i in range((k+1)//2):
  j=k-1-i
  if j>=len(layers):continue
  for a in layers[i]:
   for b in layers[j]:
    if i==j and b<a:continue
    new.update((C(a&b),C((a''^MASK)&b),C(a&(b''^MASK)),C((a''^MASK)&(b''^MASK))))
 new-=seen
 for x in new:cost[x]=k
 layers.append(new);seen|=new
 print(k,len(new),2*len(new),2*len(seen),flush=True)
 k+=1
print("RESULT",max(cost.values()),cost[C(0x6996)],{i:2*len(s) for i,s in enumerate(layers)},flush=True)
'"'" in /Users/lab/Claude/Projetos/7_problems
codex
The independent run has reached cost 13 and covered 65,326 of 65,536 functions. The remaining high-cost layer is the expensive cross-product; I’m letting it finish before looking at any supplied result.
 succeeded in 215975ms:
6 4336 8672 17222
7 5884 11768 28990
8 5296 10592 39582
9 5768 11536 51118
10 2736 5472 56590
11 3152 6304 62894
12 480 960 63854
13 736 1472 65326
14 48 96 65422
15 57 114 65536
RESULT 15 15 {0: 10, 1: 48, 2: 256, 3: 940, 4: 2048, 5: 5248, 6: 8672, 7: 11768, 8: 10592, 9: 11536, 10: 5472, 11: 6304, 12: 960, 13: 1472, 14: 96, 15: 114}

codex
Independent result is now fixed: max tree 15; `tree(0x6996)=15`; new functions by costs 0–15 are `10, 48, 256, 940, 2048, 5248, 8672, 11768, 10592, 11536, 5472, 6304, 960, 1472, 96, 114`. I’ll now inspect the supplied code and data, audit the proof obligations, and independently recompute the NPN join/distribution from the catalog.
exec
/bin/zsh -lc "sed -n '1,260p' PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py
sed -n '1,240p' PNP_AI/experiments/exp_unitgap_check/tree_gap_n4_out.txt
sed -n '1,30p' PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv
sed -n '1,20p' PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv
wc -l PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv" in /Users/lab/Claude/Projetos/7_problems
 succeeded in 0ms:
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
k=1: +48 novas (total 58/65536) [0.0s]
k=2: +256 novas (total 314/65536) [0.0s]
k=3: +940 novas (total 1254/65536) [0.0s]
k=4: +2048 novas (total 3302/65536) [0.0s]
k=5: +5248 novas (total 8550/65536) [0.0s]
k=6: +8672 novas (total 17222/65536) [0.0s]
k=7: +11768 novas (total 28990/65536) [0.1s]
k=8: +10592 novas (total 39582/65536) [0.1s]
k=9: +11536 novas (total 51118/65536) [0.2s]
k=10: +5472 novas (total 56590/65536) [0.3s]
k=11: +6304 novas (total 62894/65536) [0.5s]
k=12: +960 novas (total 63854/65536) [0.8s]
k=13: +1472 novas (total 65326/65536) [1.2s]
k=14: +96 novas (total 65422/65536) [1.7s]
k=15: +114 novas (total 65536/65536) [2.4s]
tree completo: max tree = 15 [2.4s]

Distribuicao de gap nas 222 classes NPN-4:
  gap=0: 93 classes
  gap=1: 57 classes
  gap=2: 40 classes
  gap=3: 13 classes
  gap=4: 14 classes
  gap=5: 2 classes
  gap=6: 3 classes

Classes com gap maximo:
  0x1668: opt=9 tree=15 gap=6
  0x16e9: opt=9 tree=15 gap=6
  0x6996: opt=9 tree=15 gap=6

tree(0x6996 = paridade-4) = 15
[2.4s total]
npn_rep_hex,npn_rep_dec,opt_aig,tree_aig,gap
0x0000,0,0,0,0
0x0001,1,3,3,0
0x0003,3,2,2,0
0x0006,6,5,5,0
0x0007,7,3,3,0
0x000f,15,1,1,0
0x0016,22,7,8,1
0x0017,23,5,5,0
0x0018,24,6,6,0
0x0019,25,5,5,0
0x001b,27,4,4,0
0x001e,30,5,6,1
0x001f,31,3,3,0
0x003c,60,4,4,0
0x003d,61,5,5,0
0x003f,63,2,2,0
0x0069,105,7,10,3
0x006b,107,7,8,1
0x006f,111,5,5,0
0x007e,126,6,6,0
0x007f,127,3,3,0
0x00ff,255,0,0,0
0x0116,278,9,11,2
0x0117,279,7,7,0
0x0118,280,8,9,1
0x0119,281,7,7,0
0x011a,282,7,8,1
0x011b,283,6,6,0
0x011e,286,7,9,2
npn_rep_hex,npn_rep_dec,opt_aig,status
0x0000,0,0,exact
0x0001,1,3,exact
0x0003,3,2,exact
0x0006,6,5,exact
0x0007,7,3,exact
0x000f,15,1,exact
0x0016,22,7,exact
0x0017,23,5,exact
0x0018,24,6,exact
0x0019,25,5,exact
0x001b,27,4,exact
0x001e,30,5,exact
0x001f,31,3,exact
0x003c,60,4,exact
0x003d,61,5,exact
0x003f,63,2,exact
0x0069,105,7,exact
0x006b,107,7,exact
0x006f,111,5,exact
     223 PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv
     223 PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv
     446 total

exec
/bin/zsh -lc "rg -n \"npn4_opt_aig|opt_aig|status|NPN\" PNP_AI/experiments/exp_gate_0001 -g '*.py' -g '*.md' -g '*.txt' | head -200
sed -n '200,260p' PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv
tail -20 PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv" in /Users/lab/Claude/Projetos/7_problems
 succeeded in 0ms:
PNP_AI/experiments/exp_gate_0001/run_gate.py:6:G1: classe NPN-4 já resolvida — SAT em k=opt, circuito decodificado e
PNP_AI/experiments/exp_gate_0001/run_gate.py:59:    rows = list(csv.DictReader(open(HERE / "npn4_opt_aig.csv")))
PNP_AI/experiments/exp_gate_0001/run_gate.py:61:        if r["status"] == "exact" and int(r["opt_aig"]) == target_opt:
PNP_AI/experiments/exp_gate_0001/run_gate.py:62:            return r["npn_rep_hex"], int(r["npn_rep_dec"]), int(r["opt_aig"])
0x169a,5786,8,exact
0x169b,5787,9,exact
0x169e,5790,8,exact
0x16a9,5801,9,exact
0x16ac,5804,9,exact
0x16ad,5805,9,exact
0x16bc,5820,8,exact
0x16e9,5865,9,exact
0x177e,6014,9,exact
0x178e,6030,8,exact
0x1796,6038,9,exact
0x1798,6040,8,exact
0x179a,6042,8,exact
0x17ac,6060,8,exact
0x17e8,6120,7,exact
0x18e7,6375,8,exact
0x19e1,6625,9,exact
0x19e3,6627,9,exact
0x19e6,6630,7,exact
0x1bd8,7128,9,exact
0x1be4,7140,6,exact
0x1ee1,7905,7,exact
0x3cc3,15555,6,exact
0x6996,27030,9,exact
0x16ac,5804,9,11,2
0x16ad,5805,9,13,4
0x16bc,5820,8,10,2
0x16e9,5865,9,15,6
0x177e,6014,9,11,2
0x178e,6030,8,9,1
0x1796,6038,9,11,2
0x1798,6040,8,9,1
0x179a,6042,8,9,1
0x17ac,6060,8,9,1
0x17e8,6120,7,11,4
0x18e7,6375,8,13,5
0x19e1,6625,9,11,2
0x19e3,6627,9,11,2
0x19e6,6630,7,11,4
0x1bd8,7128,9,9,0
0x1be4,7140,6,9,3
0x1ee1,7905,7,11,4
0x3cc3,15555,6,9,3
0x6996,27030,9,15,6

exec
/bin/zsh -lc "rg --files PNP_AI/experiments/exp_gate_0001
sed -n '1,220p' PNP_AI/experiments/exp_gate_0001/run_gate.py
rg -n \"0022|0023|npn4_opt\" PNP_AI | head -100" in /Users/lab/Claude/Projetos/7_problems
 succeeded in 0ms:
PNP_AI/experiments/exp_gate_0001/aig_exact.py
PNP_AI/experiments/exp_gate_0001/run_gate.py
PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv
PNP_AI/experiments/exp_gate_0001/enumerate_aig.py
"""
EXP-GATE-0001 — Execução do gate de qualificação pré-registrado (proposta v5).

G3: validação semântica do encoder — cross-check com enumeração independente
    (n=2 completo; n=3 completo até k=3, nas duas direções).
G1: classe NPN-4 já resolvida — SAT em k=opt, circuito decodificado e
    verificado por SIMULAÇÃO contra a truth table.
G2: mesma classe — UNSAT em k=opt−1 com kissat + prova DRAT verificada
    por drat-trim (checker independente).

Budget pré-registrado: 4h wall-clock por instância; estouro = FALHA do gate.
"""

import csv
import subprocess
import sys
import time
from pathlib import Path

from aig_exact import opt_via_sat, solve_k, trivial_opt, AIGEncoder, verify_circuit
from enumerate_aig import enumerate_opts

HERE = Path(__file__).parent
BUDGET_S = 4 * 3600
KISSAT = "kissat"
DRAT_TRIM = "/private/tmp/claude-501/-Users-lab-Claude-Projetos-7-problems/8ffb0bad-6e82-4e1b-b08b-00ff4ab65529/scratchpad/drat-trim/drat-trim"


def g3():
    print("=== G3 — validação semântica do encoder vs enumeração independente ===")
    t0 = time.time()
    # n=2 completo (todas as 16 funções, opt exato por enumeração até 3 portas)
    enum2 = enumerate_opts(2, 4)
    assert len(enum2) == 16, f"enumeração n=2 incompleta: {len(enum2)}"
    for tt, opt_enum in sorted(enum2.items()):
        opt_enc = opt_via_sat(2, tt, kmax=5)
        assert opt_enc == opt_enum, f"n=2 tt={tt:#06x}: encoder={opt_enc} enum={opt_enum}"
    print(f"  n=2: 16/16 funções — encoder == enumeração (max opt = {max(enum2.values())})")

    # n=3 até k=3, nas DUAS direções
    enum3 = enumerate_opts(3, 3)
    checked_le3 = 0
    for tt, opt_enum in sorted(enum3.items()):
        opt_enc = opt_via_sat(3, tt, kmax=3)
        assert opt_enc == opt_enum, f"n=3 tt={tt:#06x}: encoder={opt_enc} enum={opt_enum}"
        checked_le3 += 1
    # direção inversa: funções NÃO alcançáveis com <=3 portas => encoder UNSAT p/ k<=3
    unreachable = [tt for tt in range(256) if tt not in enum3]
    for tt in unreachable:
        assert not trivial_opt(3, tt)
        for k in (1, 2, 3):
            sat, _ = solve_k(3, tt, k)
            assert not sat, f"n=3 tt={tt:#06x}: encoder SAT em k={k}, enumeração diz inalcançável"
    print(f"  n=3: {checked_le3} funções com opt<=3 conferidas + {len(unreachable)} inalcançáveis confirmadas UNSAT (k=1..3)")
    print(f"  G3: PASSOU ({time.time()-t0:.1f}s)")


def pick_class(target_opt=7):
    rows = list(csv.DictReader(open(HERE / "npn4_opt_aig.csv")))
    for r in rows:
        if r["status"] == "exact" and int(r["opt_aig"]) == target_opt:
            return r["npn_rep_hex"], int(r["npn_rep_dec"]), int(r["opt_aig"])
    raise SystemExit("nenhuma classe exact com esse opt")


def g1(tt, opt, hexname):
    print(f"=== G1 — SAT em k={opt} para classe {hexname} (catálogo: opt={opt}) ===")
    t0 = time.time()
    sat, circ = solve_k(4, tt, opt, return_circuit=True)
    dt = time.time() - t0
    assert dt < BUDGET_S, f"estouro de budget: {dt:.0f}s"
    assert sat, f"FALHA G1: UNSAT em k={opt} — contradiz o catálogo OU encoder errado"
    gates, op = circ
    assert verify_circuit(4, tt, gates, op), "FALHA G1: circuito não verifica por simulação"
    print(f"  SAT em k={opt}; circuito de {len(gates)} portas VERIFICADO POR SIMULAÇÃO ({dt:.1f}s)")
    print(f"  circuito: {gates} out_inv={op}")
    return dt


def g2(tt, opt, hexname):
    k = opt - 1
    print(f"=== G2 — UNSAT em k={k} com kissat + DRAT + drat-trim ===")
    enc = AIGEncoder(4, k, tt).build()
    cnf = HERE / f"g2_{hexname}_k{k}.cnf"
    proof = HERE / f"g2_{hexname}_k{k}.drat"
    enc.to_dimacs(cnf)
    print(f"  CNF: {enc.nvars} vars, {len(enc.clauses)} cláusulas")
    t0 = time.time()
    r = subprocess.run([KISSAT, str(cnf), str(proof)], capture_output=True, text=True,
                       timeout=BUDGET_S)
    dt = time.time() - t0
    # kissat: exit 10 = SAT, 20 = UNSAT
    assert r.returncode == 20, f"FALHA G2: kissat retornou {r.returncode} (esperado UNSAT=20)"
    print(f"  kissat: UNSAT em {dt:.1f}s; prova DRAT: {proof.stat().st_size} bytes")
    t1 = time.time()
    v = subprocess.run([DRAT_TRIM, str(cnf), str(proof)], capture_output=True, text=True,
                       timeout=BUDGET_S)
    ok = "s VERIFIED" in v.stdout
    assert ok, f"FALHA G2: drat-trim não verificou:\n{v.stdout[-500:]}"
    print(f"  drat-trim: s VERIFIED ({time.time()-t1:.1f}s) — checker independente")
    return dt


if __name__ == "__main__":
    g3()
    hexname, dec, opt = pick_class(target_opt=7)
    # truth table da representante: o inteiro decimal do CSV É a truth table de 16 bits
    tt = dec
    print(f"\nClasse escolhida p/ G1/G2: {hexname} (tt={tt:#06x}, opt catálogo={opt})")
    t_g1 = g1(tt, opt, hexname)
    t_g2 = g2(tt, opt, hexname)
    print(f"\n*** GATE: G1 PASSOU ({t_g1:.1f}s) · G2 PASSOU ({t_g2:.1f}s) · G3 PASSOU ***")
PNP_AI/09_CANDIDATE_SUBPROBLEMS.md:43:## Auditoria bibliográfica (executada 2026-07-10 — Ciclo 7; fontes SRC-0018..0023)
PNP_AI/09_CANDIDATE_SUBPROBLEMS.md:52:- Nicho ativo e competitivo: shortest DRAT proofs de PHP (SRC-0022), hardness de parity reordenada (2024), separação CDCL/DPLL (2026). Random k-SAT: teoria madura (threshold provado p/ k grande) e experimentação de transição de fase muito trilhada — pouco espaço para nós agora. Scores mantidos.
PNP_AI/09_CANDIDATE_SUBPROBLEMS.md:189:menores casos reportados pela literatura de shortest DRAT proofs (SRC-0022): produzir com pipeline
PNP_AI/09_CANDIDATE_SUBPROBLEMS.md:196:- Auditoria no mesmo nível: nicho auditado no Ciclo 7 (SRC-0022 — ativo e COMPETITIVO; grupos
PNP_AI/09_CANDIDATE_SUBPROBLEMS.md:261:| INT | **ENTREGUE** — claims 0022/0023 FINITE_SCOPE_VERIFIED; catálogo público completado; novidade SUSTENTADA (REV-0005) | Estimado; nicho sabidamente competitivo |
PNP_AI/09_CANDIDATE_SUBPROBLEMS.md:271:1. Unidade 1 (gate) e Unidade 2 (sonda k=9) EXECUTADAS e CERTIFICADAS (claims 0021, 0022, 0023).
PNP_AI/10_PNP_CLAIM_LEDGER.md:37:| 7P-PNP-CLM-0022 | **opt_AIG(classe NPN 0x166b, n=4) = 10** — lado UNSAT: k=9 impossível, prova DRAT de 3,87GB **VERIFICADA por drat-trim ("s VERIFIED", 2026-07-11 08:33)**; lado SAT: circuito de 10 portas explícito conferido por simulação. Cadeia completa e independente do catálogo | **FINITE_SCOPE_VERIFIED** · escopo: esta classe, base AIG, modelo do encoder (validado no G3). Primeiro resultado do programa com cadeia de certificação completa | Projeto (EXP-PROBE-0001) | 2026-07-11 |
PNP_AI/10_PNP_CLAIM_LEDGER.md:39:| 7P-PNP-CLM-0023 | **opt_AIG(classe NPN 0x1669, n=4) = 10** — lado UNSAT: k=9 impossível, prova DRAT de 4,5GB **VERIFICADA 2× independentemente** (Mac: drat-trim "s VERIFIED" 09:21; pod EPYC: "s VERIFIED" em 1.558s); lado SAT: circuito de 10 portas explícito conferido por simulação (11s). Cadeia completa e independente do catálogo | **FINITE_SCOPE_VERIFIED** · escopo: esta classe, base AIG, modelo do encoder (validado no G3). Verificação dupla (2 máquinas, 2 gerações de prova) | Projeto (EXP-PROBE-0001) | 2026-07-11 |
PNP_AI/10_PNP_CLAIM_LEDGER.md:65:- **Adição datada 2026-07-11 (pós-REV-0005/GLM) aos claims 0022 e 0023:** (i) a inferência opt=10 usava implicitamente o lema de minimalidade (o encoder pergunta "exatamente k"; se opt=m≤8, um circuito mínimo de m portas — sem duplicatas, todas usadas, saída na última — satisfaria o CNF de k=m); o lema foi explicitado em `12_EXPERIMENTS` e FECHADO EMPIRICAMENTE por varredura UNSAT k=1..8 nas duas classes (`lowk_check.py`, kissat, ≤48s/instância). **Atualização 2026-07-11 (pós-REV-0008/Kimi F3): a varredura k=1..8 foi CERTIFICADA — 16/16 provas DRAT "s VERIFIED" (`cert_lowk_results.jsonl`); a cadeia k=1..9 do lower bound é integralmente certificada.** (ii) Re-check de novidade: arXiv 2603.09379 segue v1; repo krinkin/bounds sem commits desde 2026-03-10, zero issues/PRs; CSV público byte-idêntico ao local (SHA-256 conferido); Semantic Scholar sem citações. Auditoria adversarial GLM-5.2 (REV-0005): conclusão de novidade **SUSTENTADA**, com ressalva declarada — literatura clássica de exact synthesis (ABC/mockturtle, Haaswijk/Soeken et al.) não varrida sistematicamente.
PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py:2:opt(f) do catálogo npn4_opt_aig.csv (completo, claims 0022/0023).
PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py:24:CAT = HERE.parent / "exp_gate_0001" / "npn4_opt_aig.csv"
PNP_AI/12_EXPERIMENTS.md:30:- **Data:** 2026-07-11 · **Código:** `experiments/exp_gate_0001/` (`aig_exact.py` encoder, `enumerate_aig.py` enumerador independente, `run_gate.py` orquestração) · **Dados:** `npn4_opt_aig.csv` (SRC-0027, catálogo Krinkin).
PNP_AI/12_EXPERIMENTS.md:70:- Estados finais: claims 0022 e 0023 = **FINITE_SCOPE_VERIFIED**. Provas regeneráveis deterministicamente (`cert_remote.sh`/`cert_pipeline.sh`); artefatos grandes fora do git.
PNP_AI/12_EXPERIMENTS.md:107:  `npn4_opt_aig.csv` (EXP-GATE/PROBE, claims 0022/0023). tree e opt são NPN-invariantes no
PNP_AI/experiments/exp_gate_0001/run_gate.py:59:    rows = list(csv.DictReader(open(HERE / "npn4_opt_aig.csv")))
PNP_AI/drafts/DRAFT_krinkin_contact.md:99:If the gap is still open, we'll send a PR updating `data/npn4_opt_aig.csv` (2 lines), the README
PNP_AI/drafts/DRAFT_krinkin_contact.md:114:1. `data/npn4_opt_aig.csv` — 2 linhas:
PNP_AI/notes/technote_npn4_gap_closure.md:199:   EXP-PROBE-0001), `PNP_AI/experiments/exp_verify_rerun/`, claims 7P-PNP-CLM-0021/0022/0023.
PNP_AI/experiments/exp_verify_rerun/verify_all.py.snapshot:6:Loads npn4_opt_aig.csv and mutation_graph.json, computes |diff_opt|
PNP_AI/experiments/exp_verify_rerun/verify_all.py.snapshot:30:    csv_path = os.path.join(data_dir, 'npn4_opt_aig.csv')

exec
/bin/zsh -lc "sed -n '88,130p' PNP_AI/12_EXPERIMENTS.md
sed -n '130,235p' PNP_AI/notes/technote_npn4_gap_closure.md
rg -n \"Khrap|parity|16 leaves|E\\|\" PNP_AI/notes/technote_npn4_gap_closure.md PNP_AI -g '*.md' | head -100" in /Users/lab/Claude/Projetos/7_problems
 succeeded in 0ms:
- **Data:** 2026-07-11 · **Código:** `experiments/exp_pilot_n5/` (`sample_n5.py` amostrador,
  `pilot_run.py` runner) · **Pré-registro:** `13_FASE6_PLAN.md` §3 + Emenda 1.
- **Amostra:** 320 classes NPN de n=5 (300 uniformes sobre funções, seed=20260711, com órbita p/
  reponderação HT + 20 simétricas distintas). **Pré-gate:** n=3 completo 256/256 bidirecional ✓.
- **Protocolo:** busca ascendente k=0,1,... até SAT (verificado por simulação) ou censura em
  7.200s/classe; sem proof logging; tempos e tamanhos de CNF registrados por k.
- **Infra:** pod EPYC 16c/124GB re-provisionado (Ubuntu 20.04; kissat 4.0.4 source; drat-trim
  2e3b2dc source). 16 workers, lançados 16:35 UTC.
- **Conclusão permitida (quando terminar):** distribuição empírica de opt e custo em n=5 NA AMOSTRA;
  extrapolações via pesos HT com incerteza declarada. **NÃO permitida:** valores individuais como
  claims (sem certificação DRAT nesta fase); nada sobre a cauda censurada além de "≥ k censurado".

## EXP-GAP-N4 — Censo completo de gap (tree − opt) nas 222 classes NPN de n=4 — **CONCLUÍDO**

- **Data:** 2026-07-11 · **Código:** `experiments/exp_unitgap_check/tree_gap_n4.py` · **Saída:**
  `npn4_gap.csv` + `tree_gap_n4_out.txt` · **Runtime:** 2,4s (numpy, Mac, nice 19).
- **Método:** tree(f) para TODAS as 65.536 funções por DP em camadas (mesmo modelo AIG do
  `tree_gap_n3.py`: negações livres nas arestas e na saída ⟹ camadas fechadas por complemento
  absorvem polaridades; custo 0 = constantes e literais). opt(f) lido do catálogo completo
  `npn4_opt_aig.csv` (EXP-GATE/PROBE, claims 0022/0023). tree e opt são NPN-invariantes no
  modelo (perm/neg de entrada e neg de saída livres) ⟹ basta avaliar nas 222 representantes.
- **Resultado:** distribuição de gap sobre as 222 classes: `{0: 93, 1: 57, 2: 40, 3: 13, 4: 14,
  5: 2, 6: 3}`. **72/222 classes (32,4%) têm gap ≥ 2** — a tese do Unit Gap (gap ∈ {0,1},
  Thm 2 de arXiv:2603.08033) falha em ~1/3 das classes de n=4, não apenas em ⊕₃. Gap máximo
  = 6, atingido exatamente por 0x1668, 0x16e9 e 0x6996 (paridade-4 e vizinhas), com opt=9
  (catálogo) e tree=15. Max tree global = 15.
- **Verificações:** (i) sanity interno: tree(f) = tree(¬f) para todas as 65.536 e tree ≥ opt em
  todas as 222 classes (asserts no script); (ii) **cross-check de embedding: as 256 funções que
  ignoram x4 batem 256/256 com a tabela n=3** (que tinha verificação dupla no EXP anterior);
  (iii) **fail-safe analítico para o pior caso:** Khrapchenko dá L(⊕₄) ≥ 16²/(8·8) = 16 folhas
  ⟹ tree(⊕₄) ≥ 15 — a enumeração atingiu EXATAMENTE o lower bound (tree=15), e opt(⊕₄)=9 tem
  circuito explícito no catálogo ⟹ gap(⊕₄) = 6 independe da enumeração para a direção ≥.
- **Limite declarado:** tree por enumeração única (sem DRAT — proof logging não se aplica a DP);
  o lado opt herda a certificação do catálogo. Implementação única ⟹ claim 0026 fica em
  COMPUTATIONALLY_TESTED (o embedding n=3 e Khrapchenko mitigam, não substituem, 2ª implementação).
`3e66960696edf4cbdf2b5e83d6bff388a8ca297b160bb803570b912b478ca64f` (0x166b).

**Certified sweep k = 1..8.** The same encoder returns UNSAT at every gate count from 1 to 8 for
both classes, each run with proof logging and checked by drat-trim (`s VERIFIED`, 16 of 16). Proof
sizes grow from KBs to 203.6 MB (0x166b, k = 8) and 170.4 MB (0x1669, k = 8); per-proof SHA-256
hashes are archived. At k = 8 the formula has 993 variables and 89,495 clauses. Via the
normalization lemma these certified results rule out opt = m for every m ≤ 8.

### 3.2 Upper bounds: explicit 10-gate witnesses

Truth-table convention: bit t of the 16-bit integer is f on the input row where xj = bit j−1 of t
(x1 is the least-significant bit of the row index). Gate i is written (a, pa, b, pb) and computes
(val(a) ⊕ pa) ∧ (val(b) ⊕ pb) — pa = 1 means the fan-in from node a is inverted; nodes 1–4 are
x1..x4, node 4+i is gate i; the output is the last gate, non-inverted in both witnesses:

```
0x1669 (tt=5737): [(3,0,4,0),(3,1,4,1),(1,1,2,1),(2,0,5,1),(1,0,8,0),
                   (7,1,9,1),(5,1,6,1),(10,0,11,1),(10,1,11,0),(12,1,13,1)]
0x166b (tt=5739): [(2,0,3,0),(2,1,3,1),(1,0,6,1),(5,1,6,1),(4,1,8,0),
                   (4,0,8,1),(9,1,10,1),(1,1,11,1),(7,0,9,1),(12,1,13,1)]
```

Both circuits were found by kissat on the k = 10 formula (11 s and 275 s) and verified by
exhaustive simulation over all 16 rows twice: by the pipeline's built-in decoder/simulator
(`aig_exact.py`), and by a second simulator written independently of the pipeline for the review
pass (a 15-line direct evaluation of the tuple list; both agree on tt = 5737 and 5739).

### 3.3 Effect on the catalog and on the perturbation-bound verification

Marking the two classes `exact` completes the NPN-4 AIG catalog (222/222). Re-running the
catalog's own verification script (`scripts/verify_all.py`, unmodified, on the 2-line-patched CSV
and the author's published mutation graph — run archived internally with hashes and full output)
extends the script's exact-exact mutation-edge set from 987 to **995 edges, with the bound
|Δopt| ≤ n holding on all of them**. The |Δopt| distribution becomes |0| = 301, |1| = 421,
|2| = 221, |3| = 45, |4| = 7; the seven tight edges (|Δopt| = 4 = n) are unchanged. Edge
construction, canonicalization and counting are the author's script's, which we did not modify;
"gap-free" here means: every edge of the author's published mutation graph now joins two classes
with exact values, and his bound check passes on all of them.

## 4. Limitations

Finite-scope result: two specific NPN classes, in the AIG basis, under the catalog's cost model
(2-input AND gates, free inversions, size = AND-gate count). Nothing asymptotic follows. The values
are as strong as the verification chain: the normalization lemma (paper-and-pencil, stated in
§2.1), semantic validation of the encoder at small scales, and solver-independent DRAT checking at
every k = 1..9; the encoder itself is not formally verified. Timings are single-run wall-clock
times, not benchmarks.

## 5. Provenance and reproducibility

This work was produced within an AI-assisted research program led by L. A. Busnello: the encoding,
scripts, runs, and cross-checks were produced by an AI system (Claude, Anthropic) under human
direction. Proofs were generated by kissat and checked by drat-trim — the checker is the trust
anchor — on two machines. All scripts are deterministic Python; UNSAT verdicts and proof
*existence* are reproducible from the archived CNFs (proof generation ≈20–25 minutes per class on
one modern core, checking a further ≈23–26 minutes), but byte-identical proofs are **not**
guaranteed across builds/platforms — indeed the two machines' proofs differ, and only the macOS
proofs' hashes were retained. Archived internally: CNFs with hashes, proof hashes (macOS runs),
drat-trim outputs from both machines, all run scripts, and the `verify_all.py` rerun (patched CSV
diff, script snapshot, full output, hashes). Available on request.

## References

1. K. Krinkin. *A Simple Constructive Bound on Circuit Size Change Under Truth Table Perturbation.*
   arXiv:2603.09379, March 2026. Data: github.com/krinkin/bounds.
2. A. Biere, M. Fleury, N. Froleyks, M. Heule. kissat SAT solver (version 4.0.4).
3. N. Wetzler, M. Heule, W. Hunt. *DRAT-trim: Efficient Checking and Trimming Using Expressive
   Clausal Proofs.* SAT 2014. Implementation: github.com/marijnheule/drat-trim.
4. Programa 7_PROBLEMS, registros internos: `PNP_AI/12_EXPERIMENTS.md` (EXP-GATE-0001,
   EXP-PROBE-0001), `PNP_AI/experiments/exp_verify_rerun/`, claims 7P-PNP-CLM-0021/0022/0023.
PNP_AI/02_PEDAGOGICAL_GUIDE.md:85:**Exemplo executado de verdade neste projeto:** `exp_ped_0001` traduz 3-COLORING para SAT com O(|V|+|E|) cláusulas — três famílias de regras ("todo vértice tem cor", "só uma cor por vértice", "vizinhos diferem"). O solver de SAT então responde sobre coloração de grafos sem saber o que é um grafo. Isso é uma redução.
PNP_AI/12_EXPERIMENTS.md:11:- **Codificação:** x[v,c] = "vértice v tem cor c"; cláusulas: ≥1 cor por vértice, ≤1 cor por vértice, vizinhos com cores distintas. Tamanho exato: 4n+3|E| cláusulas e 9n+6|E| literais (grupo 1: n×3; grupo 2: 3n×2; grupo 3: 3|E|×2) [contagem de literais explicitada após REV-0002]; construção O(n+|E|) em word-RAM com lista de arestas, O((n+|E|)·log n) em bits — em qualquer caso polinomial (complexidade corrigida pela REV-0001; ver claim 7P-PNP-CLM-0010).
PNP_AI/12_EXPERIMENTS.md:117:  (iii) **fail-safe analítico para o pior caso:** Khrapchenko dá L(⊕₄) ≥ 16²/(8·8) = 16 folhas
PNP_AI/12_EXPERIMENTS.md:122:  COMPUTATIONALLY_TESTED (o embedding n=3 e Khrapchenko mitigam, não substituem, 2ª implementação).
PNP_AI/drafts/DRAFT_krinkin_issue2_unitgap.md:3:> **Status (2026-07-11): ISSUE ABERTA — https://github.com/krinkin/unit-gap/issues/1** (autorização de Luiz: "então vamos", após checagem de certeza — 4 famílias + fail-safe Khrapchenko). Ajuste no envio: anexos substituídos por LINKS para os artefatos versionados no repo público totobusnello/Claude (verificabilidade máxima, com histórico como carimbo). Texto enviado = corpo abaixo.
PNP_AI/drafts/DRAFT_krinkin_issue2_unitgap.md:13:**Título:** `Question about the tree(f) recursion in §2 — parity of 3 variables appears to give gap = 3 under the paper's definition of formula`
PNP_AI/drafts/DRAFT_krinkin_issue2_unitgap.md:36:**Why it matters — a concrete case.** For parity of three variables (f = x1⊕x2⊕x3, tt `0x96`):
PNP_AI/drafts/DRAFT_krinkin_issue2_unitgap.md:45:  Analytically, Khrapchenko's bound already gives ≥ 9 leaves ⟹ ≥ 8 gates, so gap ≥ 2 regardless
PNP_AI/drafts/DRAFT_krinkin_issue2_unitgap.md:50:exactly parity and its complement, which is what the displayed recursion (with `opt` in the
PNP_AI/drafts/DRAFT_krinkin_issue2_unitgap.md:87:decomposition cost rather than formula size, and the comparison with the classical Θ(n²) parity
PNP_AI/10_PNP_CLAIM_LEDGER.md:41:| 7P-PNP-CLM-0024 | **gap_fórmula(⊕₃) ≥ 2 na base AIG (valor computado pelo DP exato: 3 — tree=9, opt=6)** — REFUTA o Teorema 2 ("Unit Gap") de SRC-0032 sob a definição padrão de fórmula (a que o próprio paper enuncia: "fan-out one at every gate — a tree"). Cadeia: opt(⊕₃)=6 com UNSAT@5 DRAT "s VERIFIED" + testemunha@6 simulada; tree≤9 por construção explícita (verificável à mão); tree≥8 por Khrapchenko (resultado clássico) ⟹ gap∈{2,3} INDEPENDENTE do DP. Causa-raiz identificada: a identidade do §2 do paper usa opt (circuitos) nos filhos onde fórmula exige tree (árvores) — mede outra grandeza (≤opt+1 por construção). As "2 funções gap-1 em opt=6" da Tabela 1 dele são exatamente as paridades | **COMPUTATIONALLY_TESTED** · **QUATRO famílias SUSTENTARAM** (REV-0009 Grok/xAI + REV-0010 Codex/OpenAI + REV-0011 Kimi/Moonshot + REV-0012 GLM/Zhipu, todas com re-derivação independente; GLM re-resolveu com 2 solvers e re-hasheou os DRATs — Codex re-enumerou por camadas e confirmou tree=9 EXATO; contagens por custo 24,64,30,80,32,0,16,0,2). Liberado p/ dependência e comunicação técnica (esta última ainda exige autorização de Luiz). Certificados permanentes em `certs/` (CNF+DRAT, regeneração byte-idêntica conferida). **FORMALIZADO EM LEAN 4 (2026-07-11, `PNP_AI/formal/UnitGap.lean`, Lean 4.31.0, zero dependências externas):** `unit_gap_refuted` = (circuito de 6 portas computa ⊕₃) ∧ (toda fórmula que computa ⊕₃ tem ≥ 9 portas) ⟹ gap ≥ 3. Lema de completude do DP provado por indução (axiomas: só propext/Classical.choice/Quot.sound — kernel puro); testemunhas de 9 portas e 6 portas verificadas pelo KERNEL (`decide`, axioma: só propext); único elo `native_decide` (confiança no compilador): a varredura finita das 256 funções (par3 ∉ D₈). Auditoria de axiomas no próprio arquivo (#print axioms) | Projeto (`experiments/exp_unitgap_check/`) | 2026-07-11 |
PNP_AI/10_PNP_CLAIM_LEDGER.md:44:| 7P-PNP-CLM-0026 | **Censo de gap em n=4 (base AIG):** distribuição de gap = tree−opt sobre as 222 classes NPN é {0: 93, 1: 57, 2: 40, 3: 13, 4: 14, 5: 2, 6: 3}; em particular **72/222 classes (32,4%) têm gap ≥ 2**, estendendo a refutação do Thm 2 do Unit Gap (claims 0024/0025) de um contraexemplo para ~1/3 das classes de n=4. Gap máximo = 6 em exatamente {0x1668, 0x16e9, 0x6996} (paridade-4 e vizinhas): opt=9 (catálogo certificado) e tree=15, onde tree(⊕₄)=15 ATINGE o lower bound de Khrapchenko (≥16 folhas ⟹ ≥15 portas) — logo gap(⊕₄)=6 tem sustentação analítica independente na direção ≥. Verificações: tree=complemento-invariante nas 65.536; tree≥opt nas 222; embedding n=3 bate 256/256 com a tabela de dupla verificação | **COMPUTATIONALLY_TESTED** (implementação única do lado tree; opt herda certificação DRAT do catálogo; Khrapchenko cobre só o pior caso) | Projeto (`experiments/exp_unitgap_check/tree_gap_n4.py`, `npn4_gap.csv`, EXP-GAP-N4) | 2026-07-11 |
PNP_AI/10_PNP_CLAIM_LEDGER.md:48:- **Enunciado exato:** Seja G=(V,E) grafo simples não direcionado, |V|=n. Com variáveis x[v,c] (v∈V, c∈{0,1,2}) e φ(G) = grupo (1) [∨_c x[v,c] por vértice] ∧ grupo (2) [¬x[v,c]∨¬x[v,c'] por vértice e par c<c'] ∧ grupo (3) [¬x[u,c]∨¬x[v,c] por aresta e cor]: (a) φ(G) satisfatível ⟺ G 3-colorável; (b) φ(G) tem 4n+3|E| cláusulas e 9n+6|E| literais; construção em O(n+|E|) operações em word-RAM com entrada por lista de arestas, O((n+|E|)·log n) em codificação explícita de bits; logo G ↦ φ(G) é redução many-one polinomial de 3-COLORING a SAT.
PNP_AI/10_PNP_CLAIM_LEDGER.md:55:- **Críticas/Revisões externas:** REV-0001 (Codex/GPT-5): GAP_FOUND na complexidade → correção aceita; REV-0002 (Kimi): endureceu verificação do certificado e contagem de literais; **REV-0006 (GLM-5.2/Zhipu, 2026-07-11): VALIDADO — 0 críticos/importantes, 5 MENOR** (verificação empírica independente da aritmética 4n+3|E| e 9n+6|E| em C5/Petersen/K4; ambas as direções da prova conferidas; redundância do grupo (2) confirmada correta).
PNP_AI/experiments/exp_unitgap_check/dossie_rev0009.md:32:- Consistência com teoria clássica: Khrapchenko dá L(⊕3) ≥ 9 folhas ⟹ ≥ 8 portas binárias; a
PNP_AI/experiments/exp_unitgap_check/dossie_rev0009.md:42:   comparação com formula complexity clássica (§3 cita parity Θ(n²) De Morgan) continuam honestos?
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:43:   Assim, o intervalo teórico dado por Khrapchenko é \(\operatorname{tree}\in\{8,9\}\), mas o DP exato fecha o valor em \(9\). Logo:
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:72:   |A|=|B|=4,\qquad |E|=12.
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:75:   Khrapchenko fornece
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:78:   L(f)\ge \frac{|E|^2}{|A||B|}
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:213:   Assim, o intervalo teórico dado por Khrapchenko é \(\operatorname{tree}\in\{8,9\}\), mas o DP exato fecha o valor em \(9\). Logo:
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:242:   |A|=|B|=4,\qquad |E|=12.
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:245:   Khrapchenko fornece
PNP_AI/experiments/exp_unitgap_check/rev0010_codex_verbatim.md:248:   L(f)\ge \frac{|E|^2}{|A||B|}
PNP_AI/experiments/exp_unitgap_check/rev0012_glm_verbatim.md:11:- Re-simulação manual do circuito de 6 portas nas 8 linhas: bate parity em todas. ✓
PNP_AI/experiments/exp_unitgap_check/rev0012_glm_verbatim.md:23:**3. [CRÍTICA] Khrapchenko re-derivado: `|E|²/|A||B| = 12²/(4·4) = 9` folhas ⟹ ≥ 8 portas.**
PNP_AI/experiments/exp_unitgap_check/rev0012_glm_verbatim.md:27:- O DP fecha o valor em **9** — refutando Thm 2 (`gap ∈ {0,1}`) sob qualquer leitura. Note que mesmo o limite inferior fraco `{2,3}` (Khrapchenko sem DP) já refuta o enunciado.
PNP_AI/experiments/exp_unitgap_check/rev0012_glm_verbatim.md:62:- **Toda a refutation independe do DP.** Mesmo que `tree(⊕₃)=8` (em vez de 9) por algum bug do DP que ninguém enxergou, `gap ∈ {2,3}`, ainda `>1`, e o argumento Khrapchenko + testemunha de 9 portas + `s=3` estrutural/aritmético permanecem.
PNP_AI/09_CANDIDATE_SUBPROBLEMS.md:52:- Nicho ativo e competitivo: shortest DRAT proofs de PHP (SRC-0022), hardness de parity reordenada (2024), separação CDCL/DPLL (2026). Random k-SAT: teoria madura (threshold provado p/ k grande) e experimentação de transição de fase muito trilhada — pouco espaço para nós agora. Scores mantidos.
PNP_AI/experiments/exp_unitgap_check/rev0011_kimi_verbatim.md:51:Assim `tree(⊕₃)≤9`. Pelo DP exato (`tree_gap_n3.py`) e por Khrapchenko, `tree(⊕₃)=9`. Portanto
PNP_AI/experiments/exp_unitgap_check/rev0011_kimi_verbatim.md:57:**3. [ALTA] O DP de `tree` e o lower bound de Khrapchenko estão corretos.**  
PNP_AI/experiments/exp_unitgap_check/rev0011_kimi_verbatim.md:67:Khrapchenko para `⊕₃`: `A=f⁻¹(0)`, `B=f⁻¹(1)`, `|A|=|B|=4`, cada vértice de `A` tem 3 vizinhos em `B`, logo `|E|=12`. Então
PNP_AI/experiments/exp_unitgap_check/rev0011_kimi_verbatim.md:70:L(\oplus_3)\ge \frac{|E|^2}{|A||B|}=\frac{144}{16}=9\text{ folhas}.
PNP_AI/experiments/exp_unitgap_check/rev0011_kimi_verbatim.md:127:| `tree(⊕₃)` | 9 | Construção explícita com 9 portas (cópias disjuntas de `⊕₂`); Khrapchenko dá ≥8; DP exato exclui 8. |
PNP_AI/experiments/exp_unitgap_check/rev0011_kimi_verbatim.md:129:| Khrapchenko | `144/16=9` folhas | `\|A\|=\|B\|=4`, `\|E\|=12`. |
PNP_AI/experiments/exp_unitgap_check/rev0009_grok_verbatim.md:36:| Sub-DAGs contam como “folhas” de custo `opt` | Idem | Não é o modelo de Shannon/Khrapchenko/Jukna; chamar isso de formula size é equívoco |
PNP_AI/experiments/exp_unitgap_check/rev0009_grok_verbatim.md:40:> “parity on n variables has formula complexity Θ(n²) [De Morgan] but circuit complexity O(n). The collapse to a gap of at most 1 in the AIG basis arises from … constant 1 … and free complementation.”
PNP_AI/experiments/exp_unitgap_check/rev0009_grok_verbatim.md:71:**Lower bound:** Khrapchenko ⇒ \(L(\oplus_3)\ge 9\) folhas em De Morgan ⇒ ≥ 8 portas binárias. Com a equivalência acima, \(\mathrm{tree}_{\mathrm{formula}}(\oplus_3)\ge 8\).
PNP_AI/experiments/exp_unitgap_check/rev0009_grok_verbatim.md:102:Contraexemplo explícito, n=3, verificável à mão na parte ≤9 e por Khrapchenko na parte ≥8.
PNP_AI/experiments/exp_unitgap_check/rev0009_grok_verbatim.md:166:- o contraexemplo ⊕₃ / ¬⊕₃ é sólido: `opt=6`, `tree_formula∈{8,9}`, `gap∈{2,3}>1`, com construção explícita de 9 portas e lower bound de Khrapchenko ≥8;

 succeeded in 302203ms:
cost 1: new complement-classes=24, new functions=48, cumulative functions=58
cost 2: new complement-classes=128, new functions=256, cumulative functions=314
cost 3: new complement-classes=470, new functions=940, cumulative functions=1254
cost 4: new complement-classes=1024, new functions=2048, cumulative functions=3302
cost 5: new complement-classes=2624, new functions=5248, cumulative functions=8550
cost 6: new complement-classes=4336, new functions=8672, cumulative functions=17222
cost 7: new complement-classes=5884, new functions=11768, cumulative functions=28990
cost 8: new complement-classes=5296, new functions=10592, cumulative functions=39582
cost 9: new complement-classes=5768, new functions=11536, cumulative functions=51118
cost 10: new complement-classes=2736, new functions=5472, cumulative functions=56590
cost 11: new complement-classes=3152, new functions=6304, cumulative functions=62894
cost 12: new complement-classes=480, new functions=960, cumulative functions=63854
cost 13: new complement-classes=736, new functions=1472, cumulative functions=65326
cost 14: new complement-classes=48, new functions=96, cumulative functions=65422
cost 15: new complement-classes=57, new functions=114, cumulative functions=65536
max_tree 15
tree_0x6996 15
cost0 complement-classes 5 cost0 functions 10
new_functions_per_cost {0: 10, 1: 48, 2: 256, 3: 940, 4: 2048, 5: 5248, 6: 8672, 7: 11768, 8: 10592, 9: 11536, 10: 5472, 11: 6304, 12: 960, 13: 1472, 14: 96, 15: 114}

exec
/bin/zsh -lc "python3 -u -c '
import csv,itertools,numpy as np
MASK=65535
cost=np.full(65536,-1,dtype=np.int16)
base={0,MASK}
for bit in range(4):
 t=sum(1<<a for a in range(16) if (a>>bit)&1)
 base|={t,t"'^MASK}
cost[list(base)]=0
layers=[np.array(sorted(base),dtype=np.int64)]
k=0
while np.any(cost<0):
 k+=1; fresh=set()
 for i in range((k+1)//2):
  j=k-1-i
  if j>=len(layers):continue
  A,B=layers[i],layers[j]
  for start in range(0,len(A),512):
   z=np.bitwise_and.outer(A[start:start+512],B).ravel()
   z=z[cost[z]<0]
   fresh.update(np.unique(z).tolist())
 expanded=fresh|{x''^MASK for x in fresh}
 arr=np.array(sorted(x for x in expanded if cost[x]<0),dtype=np.int64)
 cost[arr]=k;layers.append(arr)
cat=list(csv.DictReader(open("PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv")))
gap=list(csv.DictReader(open("PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv")))
def npn_canon(f):
 best=MASK
 for p in itertools.permutations(range(4)):
  for neg in range(16):
   g=0
   for x in range(16):
    old=0
    for dst in range(4):
     old|=((((x>>dst)&1)''^((neg>>dst)&1))<<p[dst])
    g|=((f>>old)&1)<<x
   best=min(best,g,g''^MASK)
 return best
reps=[int(r["npn_rep_dec"]) for r in cat]
from collections import Counter
D=Counter(int(cost[r])-int(row["opt_aig"]) for r,row in zip(reps,cat))
bad_join=[]
for c,o in zip(cat,gap):
 expected=(c["npn_rep_hex"],c["npn_rep_dec"],c["opt_aig"],str(int(cost[int(c["npn_rep_dec"])])),str(int(cost[int(c["npn_rep_dec"])])-int(c["opt_aig"])))
 got=(o["npn_rep_hex"],o["npn_rep_dec"],o["opt_aig"],o["tree_aig"],o["gap"])
 if expected!=got:bad_join.append((expected,got))
noncanon=[(hex(r),hex(npn_canon(r))) for r in reps if npn_canon(r)!=r]
print("catalog_rows",len(cat),"unique_reps",len(set(reps)),"statuses",Counter(r["status"] for r in cat))
print("all_hex_dec_consistent",all(int(r["npn_rep_hex"],16)==int(r["npn_rep_dec"]) for r in cat))
print("noncanonical_reps",noncanon[:10],"count",len(noncanon))
print("independent_join_dist",dict(sorted(D.items())))
mx=max(D)
print("max_gap",mx,[(r["npn_rep_hex"],int(cost[int(r["npn_rep_dec"])]),int(r["opt_aig"])) for r in cat if int(cost[int(r["npn_rep_dec"])])-int(r["opt_aig"])==mx])
print("csv_join_mismatches",len(bad_join),bad_join[:3])
print("tree_lt_opt",[(r["npn_rep_hex"],int(cost[int(r["npn_rep_dec"])]),int(r["opt_aig"])) for r in cat if int(cost[int(r["npn_rep_dec"])])<int(r["opt_aig"])])
'"'" in /Users/lab/Claude/Projetos/7_problems
 succeeded in 2631ms:
catalog_rows 222 unique_reps 222 statuses Counter({'exact': 220, 'improved_ub': 2})
all_hex_dec_consistent True
noncanonical_reps [] count 0
independent_join_dist {0: 93, 1: 57, 2: 40, 3: 13, 4: 14, 5: 2, 6: 3}
max_gap 6 [('0x1668', 15, 9), ('0x16e9', 15, 9), ('0x6996', 15, 9)]
csv_join_mismatches 0 []
tree_lt_opt []

codex
The join arithmetic and NPN representatives check out, but the catalog audit exposed a material provenance issue: the file has 220 rows marked `exact` and 2 marked only `improved_ub`. I’m identifying those rows and checking whether separate project certificates upgrade them to exact values despite the stale status field.
exec
/bin/zsh -lc "rg -n \"improved_ub\" PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv
rg -n \"0x1669|0x166b\" PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv PNP_AI/10_PNP_CLAIM_LEDGER.md PNP_AI/12_EXPERIMENTS.md | head -80
rg --files PNP_AI/experiments | rg 'cert|probe|1669|166b|lowk' | head -100" in /Users/lab/Claude/Projetos/7_problems
 succeeded in 0ms:
184:0x1669,5737,10,improved_ub
186:0x166b,5739,10,improved_ub
PNP_AI/12_EXPERIMENTS.md:47:## EXP-PROBE-0001 — Sonda k=9 nas classes pendentes 0x1669 / 0x166b — **CONCLUÍDO** (status atualizado 2026-07-11, pós-REV-0005)
PNP_AI/12_EXPERIMENTS.md:56:| **0x166b** (tt=5739) | **UNSAT — não existe circuito AIG de 9 portas** ⟹ com ub=10: **opt_AIG = 10** | **1.269s (21min)** — vs timeout do autor do catálogo | COMPUTATIONALLY_TESTED; certificação DRAT + busca do circuito de 10 portas EM EXECUÇÃO |
PNP_AI/12_EXPERIMENTS.md:57:| **0x1669** (tt=5737) | **UNSAT — não existe circuito AIG de 9 portas** ⟹ com ub=10: **opt_AIG = 10** | **1.543s (26min)** | COMPUTATIONALLY_TESTED; certificação DRAT + busca do circuito de 10 portas EM EXECUÇÃO |
PNP_AI/12_EXPERIMENTS.md:65:| 0x166b | 3,87GB | **s VERIFIED** (08:33) | **s VERIFIED** (1.345s de check) | ✅ (275s de busca) |
PNP_AI/12_EXPERIMENTS.md:66:| 0x1669 | 4,5GB | **s VERIFIED** (09:21) | **s VERIFIED** (1.558s de check) | ✅ (11s de busca) |
PNP_AI/12_EXPERIMENTS.md:72:- ~~Conclusão intermediária (histórica, mantida por governança):~~ "sob o encoder validado no gate, não existe AIG de 9 portas para 0x166b; opt=10 pendente de certificado DRAT e de auto-verificação do ub" — **SUPERADA em 2026-07-11** pela tabela de certificação acima (ambas as classes com DRAT verificada 2× e circuito de 10 portas simulado).
PNP_AI/12_EXPERIMENTS.md:73:- **Conclusão permitida (final, 2026-07-11):** opt_AIG(0x1669) = opt_AIG(0x166b) = 10 na base AIG do catálogo (portas AND-2, inversões livres), com cadeia: encoder validado (G3) · UNSAT k=9 certificado DRAT em duplicata · UNSAT empírico k=1..8 (addendum abaixo) · circuito de 10 portas verificado por simulação.
PNP_AI/12_EXPERIMENTS.md:80:- **Resultado (execução real, Mac, kissat, `lowk_sweep.log`):** **UNSAT em TODOS os k=1..8, para AMBAS as classes.** Tempos: k≤6 sub-segundo; k=7 ≈ 4–5s; k=8 = 47,9s (0x166b) e 39,2s (0x1669). Tamanhos: k=8 → 993 vars / 89.495 cláusulas. Vereditos sem proof logging (sanidade); o resultado de claim continua ancorado no k=9 com DRAT + este fecho empírico + o lema de minimalidade agora EXPLÍCITO (acima).
PNP_AI/12_EXPERIMENTS.md:81:- **Atualização 2026-07-11 (fecho do finding 3 da REV-0008/Kimi): a varredura k=1..8 foi CERTIFICADA.** `cert_lowk.py` no pod EPYC (kissat 4.0.4 source, drat-trim 2e3b2dc source): **16/16 execuções (2 classes × k=1..8) UNSAT com prova DRAT "s VERIFIED"**; hashes SHA-256 e tamanhos em `experiments/exp_probe_0001/cert_lowk_results.jsonl` (versionado; maiores provas: k=8 = 203,6MB/0x166b e 170,4MB/0x1669, verificadas em 144s/152s). **Com isso a cadeia inteira k=1..9 é DRAT-certificada** — nenhum elo "confie no solver" resta no lower bound.
PNP_AI/12_EXPERIMENTS.md:83:- **Correção de unidades (datada 2026-07-11, REV-0007 finding 7):** tamanhos exatos das provas: 0x1669 = 4.785.094.117 bytes (≈4,79 GB decimais; os "4,5GB" registrados acima eram GiB de display do filesystem rotulados como GB); 0x166b = 3.871.475.211 bytes (≈3,87 GB). CNFs: 1.781.704 bytes cada.
PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv:184:0x1669,5737,10,15,5
PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv:186:0x166b,5739,10,14,4
PNP_AI/10_PNP_CLAIM_LEDGER.md:37:| 7P-PNP-CLM-0022 | **opt_AIG(classe NPN 0x166b, n=4) = 10** — lado UNSAT: k=9 impossível, prova DRAT de 3,87GB **VERIFICADA por drat-trim ("s VERIFIED", 2026-07-11 08:33)**; lado SAT: circuito de 10 portas explícito conferido por simulação. Cadeia completa e independente do catálogo | **FINITE_SCOPE_VERIFIED** · escopo: esta classe, base AIG, modelo do encoder (validado no G3). Primeiro resultado do programa com cadeia de certificação completa | Projeto (EXP-PROBE-0001) | 2026-07-11 |
PNP_AI/10_PNP_CLAIM_LEDGER.md:39:| 7P-PNP-CLM-0023 | **opt_AIG(classe NPN 0x1669, n=4) = 10** — lado UNSAT: k=9 impossível, prova DRAT de 4,5GB **VERIFICADA 2× independentemente** (Mac: drat-trim "s VERIFIED" 09:21; pod EPYC: "s VERIFIED" em 1.558s); lado SAT: circuito de 10 portas explícito conferido por simulação (11s). Cadeia completa e independente do catálogo | **FINITE_SCOPE_VERIFIED** · escopo: esta classe, base AIG, modelo do encoder (validado no G3). Verificação dupla (2 máquinas, 2 gerações de prova) | Projeto (EXP-PROBE-0001) | 2026-07-11 |
PNP_AI/experiments/exp_probe_0001/kissat_0x1669.out
PNP_AI/experiments/exp_probe_0001/cert_pipeline.sh
PNP_AI/experiments/exp_probe_0001/cert_run.py
PNP_AI/experiments/exp_probe_0001/lowk_check.py
PNP_AI/experiments/exp_probe_0001/cert_lowk_results.jsonl
PNP_AI/experiments/exp_probe_0001/dt_0x1669.out
PNP_AI/experiments/exp_probe_0001/PIPELINE_DONE
PNP_AI/experiments/exp_probe_0001/drat_hashes.txt
PNP_AI/experiments/exp_probe_0001/dt_0x166b.out
PNP_AI/experiments/exp_probe_0001/run_probe.py
PNP_AI/experiments/exp_probe_0001/cert_lowk.py

exec
/bin/zsh -lc "python3 -c 'A=[x for x in range(16) if x.bit_count()%2==0]; B=[x for x in range(16) if x.bit_count()%2==1]; E=[(a,b) for a in A for b in B if (a"'^b).bit_count()==1]; print("A",A); print("B",B); print("|A|",len(A),"|B|",len(B),"|E|",len(E),"degrees_A",[sum(1 for x,y in E if x==a) for a in A],"bound",len(E)**2/(len(A)*len(B)))'"'" in /Users/lab/Claude/Projetos/7_problems
 succeeded in 0ms:
A [0, 3, 5, 6, 9, 10, 12, 15]
B [1, 2, 4, 7, 8, 11, 13, 14]
|A| 8 |B| 8 |E| 32 degrees_A [4, 4, 4, 4, 4, 4, 4, 4] bound 16.0

codex
VERDICT: SUSTAINED, with one catalog-metadata weakness noted.

## 1. Independent tree DP

Before reading the supplied implementation, I ran an independently written DP using complement classes:

\[
[f]=\{f,\neg f\},\qquad
D_k=\left\{\operatorname{canon}\big((a\oplus p)\land(b\oplus q)\big):
a\in D_i,b\in D_j,\ i+j+1=k,\ p,q\in\{0,1^{16}\}\right\}.
\]

Complement canonicalization is valid because:

- output negation is free, so \(f\) and \(\neg f\) have equal cost;
- each child edge may be independently negated, giving all four combinations \(a\land b,\neg a\land b,a\land\neg b,\neg a\land\neg b\);
- duplicating a child when \(a=b\) is allowed but costs twice its formula size, as required by fan-out 1.

My independent results were:

- max tree over all 65,536 functions: **15**
- `tree(0x6996)`: **15**
- new functions at each exact cost:

| Cost | New functions |
|---:|---:|
| 0 | 10 |
| 1 | 48 |
| 2 | 256 |
| 3 | 940 |
| 4 | 2,048 |
| 5 | 5,248 |
| 6 | 8,672 |
| 7 | 11,768 |
| 8 | 10,592 |
| 9 | 11,536 |
| 10 | 5,472 |
| 11 | 6,304 |
| 12 | 960 |
| 13 | 1,472 |
| 14 | 96 |
| 15 | 114 |

These sum to exactly 65,536. They agree at every level with [tree_gap_n4_out.txt](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4_out.txt).

## 2. Audit of the supplied implementation

The layered DP in [tree_gap_n4.py](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py:27) is sound and complete.

- Cost-0 seeding is correct: two constants plus four variables and their complements, giving 10 distinct functions.
- Every layer is closed under complement. Consequently `bitwise_and.outer(Di, Dj)` includes all four independent input-edge polarity choices.
- Restricting to \(i\le j\) is valid because AND is commutative.
- Every generated candidate has a formula of size \(i+j+1\), so the DP cannot undercount.
- Conversely, in a minimum formula, each root child can be replaced by its minimum formula up to free output complementation. Thus its child costs occur in exact earlier layers and the root decomposition is enumerated. Therefore the DP cannot overcount.
- Equal truth tables on both inputs do not introduce illicit DAG sharing: the recurrence charges both child sizes separately.

NPN invariance is also valid:

- input permutations are free rewiring;
- negating an input is implemented by toggling every edge leaving that primary input;
- output negation is free.

These operations preserve both formula size and DAG circuit size, in both directions, so `tree` and `opt` are constant on NPN classes.

I independently checked the catalog/join:

- 222 rows and 222 unique representatives;
- every hexadecimal and decimal representative agrees;
- every representative is canonical under my independently implemented NPN transformation;
- zero row mismatches between my computed tree values and [npn4_gap.csv](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv);
- no occurrence of `tree < opt`.

My independently recomputed distribution was exactly:

\[
\{0:93,\ 1:57,\ 2:40,\ 3:13,\ 4:14,\ 5:2,\ 6:3\}.
\]

The maximum-gap rows were exactly:

- `0x1668`: tree 15, opt 9, gap 6
- `0x16e9`: tree 15, opt 9, gap 6
- `0x6996`: tree 15, opt 9, gap 6

One finding: [npn4_opt_aig.csv](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv:184) still labels `0x1669` and `0x166b` as `improved_ub`, not `exact`, and the join script ignores the `status` column. Read in isolation, the CSV therefore does not certify the entire distribution. However, the repository separately records verified lower bounds and simulated 10-gate witnesses for both rows, establishing opt \(=10\). This is stale metadata and a robustness defect in the join, not a numerical discrepancy. The three maximum-gap rows themselves are marked exact.

## 3. Khrapchenko check for parity-4

For \(f(x)=x_1\oplus x_2\oplus x_3\oplus x_4\), take:

\[
A=f^{-1}(0)=\{0,3,5,6,9,10,12,15\},
\]

\[
B=f^{-1}(1)=\{1,2,4,7,8,11,13,14\}.
\]

Thus \(|A|=|B|=8\). Every even-parity assignment has four Hamming-distance-one neighbors, all of odd parity, so:

\[
|E|=8\cdot4=32.
\]

Khrapchenko gives:

\[
L(f)\ge\frac{|E|^2}{|A||B|}
=\frac{32^2}{8\cdot8}=16
\]

variable leaves.

An AIG formula with complemented edges can be pushed, by De Morgan transformations, into an equivalent binary De Morgan formula without changing its number of leaves or gates. A binary formula with \(L\) leaves has \(L-1\) internal gates. Constants cannot weaken the result because the lower bound already requires 16 variable leaves. Hence:

\[
\operatorname{tree}(\oplus_4)\ge15.
\]

The DP supplies the matching upper bound 15, so `tree(0x6996)=15` exactly.

Overall, I found no refutation of the numerical claim. The only actionable issue is that the join should assert that every catalog row is exact—or explicitly recognize the two separately certified upgrades—instead of silently consuming `improved_ub` rows.
tokens used
65.613
VERDICT: SUSTAINED, with one catalog-metadata weakness noted.

## 1. Independent tree DP

Before reading the supplied implementation, I ran an independently written DP using complement classes:

\[
[f]=\{f,\neg f\},\qquad
D_k=\left\{\operatorname{canon}\big((a\oplus p)\land(b\oplus q)\big):
a\in D_i,b\in D_j,\ i+j+1=k,\ p,q\in\{0,1^{16}\}\right\}.
\]

Complement canonicalization is valid because:

- output negation is free, so \(f\) and \(\neg f\) have equal cost;
- each child edge may be independently negated, giving all four combinations \(a\land b,\neg a\land b,a\land\neg b,\neg a\land\neg b\);
- duplicating a child when \(a=b\) is allowed but costs twice its formula size, as required by fan-out 1.

My independent results were:

- max tree over all 65,536 functions: **15**
- `tree(0x6996)`: **15**
- new functions at each exact cost:

| Cost | New functions |
|---:|---:|
| 0 | 10 |
| 1 | 48 |
| 2 | 256 |
| 3 | 940 |
| 4 | 2,048 |
| 5 | 5,248 |
| 6 | 8,672 |
| 7 | 11,768 |
| 8 | 10,592 |
| 9 | 11,536 |
| 10 | 5,472 |
| 11 | 6,304 |
| 12 | 960 |
| 13 | 1,472 |
| 14 | 96 |
| 15 | 114 |

These sum to exactly 65,536. They agree at every level with [tree_gap_n4_out.txt](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4_out.txt).

## 2. Audit of the supplied implementation

The layered DP in [tree_gap_n4.py](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py:27) is sound and complete.

- Cost-0 seeding is correct: two constants plus four variables and their complements, giving 10 distinct functions.
- Every layer is closed under complement. Consequently `bitwise_and.outer(Di, Dj)` includes all four independent input-edge polarity choices.
- Restricting to \(i\le j\) is valid because AND is commutative.
- Every generated candidate has a formula of size \(i+j+1\), so the DP cannot undercount.
- Conversely, in a minimum formula, each root child can be replaced by its minimum formula up to free output complementation. Thus its child costs occur in exact earlier layers and the root decomposition is enumerated. Therefore the DP cannot overcount.
- Equal truth tables on both inputs do not introduce illicit DAG sharing: the recurrence charges both child sizes separately.

NPN invariance is also valid:

- input permutations are free rewiring;
- negating an input is implemented by toggling every edge leaving that primary input;
- output negation is free.

These operations preserve both formula size and DAG circuit size, in both directions, so `tree` and `opt` are constant on NPN classes.

I independently checked the catalog/join:

- 222 rows and 222 unique representatives;
- every hexadecimal and decimal representative agrees;
- every representative is canonical under my independently implemented NPN transformation;
- zero row mismatches between my computed tree values and [npn4_gap.csv](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/npn4_gap.csv);
- no occurrence of `tree < opt`.

My independently recomputed distribution was exactly:

\[
\{0:93,\ 1:57,\ 2:40,\ 3:13,\ 4:14,\ 5:2,\ 6:3\}.
\]

The maximum-gap rows were exactly:

- `0x1668`: tree 15, opt 9, gap 6
- `0x16e9`: tree 15, opt 9, gap 6
- `0x6996`: tree 15, opt 9, gap 6

One finding: [npn4_opt_aig.csv](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv:184) still labels `0x1669` and `0x166b` as `improved_ub`, not `exact`, and the join script ignores the `status` column. Read in isolation, the CSV therefore does not certify the entire distribution. However, the repository separately records verified lower bounds and simulated 10-gate witnesses for both rows, establishing opt \(=10\). This is stale metadata and a robustness defect in the join, not a numerical discrepancy. The three maximum-gap rows themselves are marked exact.

## 3. Khrapchenko check for parity-4

For \(f(x)=x_1\oplus x_2\oplus x_3\oplus x_4\), take:

\[
A=f^{-1}(0)=\{0,3,5,6,9,10,12,15\},
\]

\[
B=f^{-1}(1)=\{1,2,4,7,8,11,13,14\}.
\]

Thus \(|A|=|B|=8\). Every even-parity assignment has four Hamming-distance-one neighbors, all of odd parity, so:

\[
|E|=8\cdot4=32.
\]

Khrapchenko gives:

\[
L(f)\ge\frac{|E|^2}{|A||B|}
=\frac{32^2}{8\cdot8}=16
\]

variable leaves.

An AIG formula with complemented edges can be pushed, by De Morgan transformations, into an equivalent binary De Morgan formula without changing its number of leaves or gates. A binary formula with \(L\) leaves has \(L-1\) internal gates. Constants cannot weaken the result because the lower bound already requires 16 variable leaves. Hence:

\[
\operatorname{tree}(\oplus_4)\ge15.
\]

The DP supplies the matching upper bound 15, so `tree(0x6996)=15` exactly.

Overall, I found no refutation of the numerical claim. The only actionable issue is that the join should assert that every catalog row is exact—or explicitly recognize the two separately certified upgrades—instead of silently consuming `improved_ub` rows.
