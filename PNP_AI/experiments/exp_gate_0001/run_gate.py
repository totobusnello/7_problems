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
