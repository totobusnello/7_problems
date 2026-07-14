"""Busca n=5 por um SEPARADOR do unit-gap em XAG: uma funcao f de 5 variaveis com
gap_XAG(f) = tree_XAG(f) - opt_XAG(f) >= 2 (open question #1 da technote).

Em n<=4, gap_XAG in {0,1} (empirico). Em XAG NAO ha a decomposicao trivial f=1&f que
forca gap<=1 no AIG, entao gap>=2 e possivel a priori. Um separador refina a base-
dependencia; a ausencia (amostra grande) e evidencia a favor da conjectura.

Estrategia: gerar candidatos de opt BAIXO (SAT viavel) via circuitos XAG aleatorios
com sharing/reconvergencia; para cada tt de 5 variaveis essenciais:
  opt = opt_XAG(f) (SAT, timeout);
  testa formula em opt+1: SAT => tree=opt+1 (gap 1); UNSAT => tree>=opt+2 (SEPARADOR,
  certificado); TIMEOUT => inconclusivo (registra p/ revisita).

Uso: python3 search_n5.py <worker_id> <n_workers>
Saida: search_n5_w<id>.csv (todas as f) + sep_n5_w<id>.jsonl (separadores). Resume por tt.
"""
import sys, os, csv, json, time, random, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from xag_exact import opt_via_sat, solve_k, simulate, tt_bit

N = 5
ROWS = 1 << N
MASK = (1 << ROWS) - 1
TIMEOUT = 20  # s por chamada SAT


def circuit_tt(gates, out_pol):
    """tt de 32 bits do circuito XAG (n=5)."""
    tt = 0
    for t in range(ROWS):
        if simulate(N, gates, out_pol, t):
            tt |= 1 << t
    return tt


def essential_all5(tt):
    """f depende das 5 variaveis? (cofator xj=0 != cofator xj=1 em cada eixo)"""
    for j in range(N):
        diff = False
        for t in range(ROWS):
            if not ((t >> j) & 1) and ((tt >> t) & 1) != ((tt >> (t | (1 << j))) & 1):
                diff = True
                break
        if not diff:
            return False
    return True


def random_candidate(rng, kmin=4, kmax=8):
    """circuito XAG aleatorio com vies p/ reconvergencia (reuso de gates)."""
    k = rng.randint(kmin, kmax)
    gates = []
    for i in range(1, k + 1):
        node = N + i
        prev = list(range(1, node))
        # vies: com prob 0.6 escolhe ao menos um predecessor entre gates ja criados
        gate_nodes = [p for p in prev if p > N]
        if gate_nodes and rng.random() < 0.6:
            a = rng.choice(gate_nodes)
            b = rng.choice([p for p in prev if p != a])
        else:
            a, b = rng.sample(prev, 2)
        if a > b:
            a, b = b, a
        typ = rng.choice(["and", "xor", "xor"])  # vies XOR (estrutura nao-linear)
        pa, pb = (rng.randint(0, 1), rng.randint(0, 1)) if typ == "and" else (0, 0)
        gates.append((typ, a, pa, b, pb))
    return circuit_tt(gates, rng.randint(0, 1))


def main():
    wid, nw = int(sys.argv[1]), int(sys.argv[2])
    out_csv = os.path.join(HERE, f"search_n5_w{wid:02d}.csv")
    out_sep = os.path.join(HERE, f"sep_n5_w{wid:02d}.jsonl")
    seen = set()
    if os.path.exists(out_csv):
        for r in csv.DictReader(open(out_csv)):
            seen.add(int(r["tt"]))
    rng = random.Random(90210 + wid)
    t0 = time.time()
    mode = "a" if seen else "w"
    n_done = n_sep = n_gap1 = n_gap0 = n_inc = 0
    with open(out_csv, mode, newline="") as fc, open(out_sep, "a") as fs:
        w = csv.DictWriter(fc, fieldnames=["tt", "opt", "tree", "gap", "verdict", "t_sec"])
        if not seen:
            w.writeheader()
        # loop ate 1e9 candidatos (backstop); na pratica roda ate matarmos
        for _ in range(10**9):
            tt = random_candidate(rng)
            if tt in seen or tt in (0, MASK):
                continue
            if not essential_all5(tt):
                continue
            seen.add(tt)
            t1 = time.time()
            opt = opt_via_sat(N, tt, kmax=12, timeout=TIMEOUT, verify=False)
            if opt is None:
                continue  # opt alto/timeout — fora do alcance
            # tree_XAG por busca ASCENDENTE a partir de opt (solve_k em modo formula,
            # validado pelo gate G-T3). O primeiro k SAT = tree. gap = tree - opt.
            # (parity e lineares dao SAT ja em k=opt => gap 0, sem falso positivo.)
            tree = None; timed_out = False
            for kk in range(opt, opt + 6):
                try:
                    sat, _ = solve_k(N, tt, kk, timeout=TIMEOUT, formula=True)
                except subprocess.TimeoutExpired:
                    timed_out = True; break
                if sat:
                    tree = kk; break
            if tree is not None:
                gap = tree - opt
                verdict = "SEPARATOR" if gap >= 2 else ("gap1" if gap == 1 else "gap0")
            elif timed_out:
                verdict, gap = "inconclusive", -1
            else:
                verdict, gap, tree = "SEPARATOR", 6, opt + 6  # tree>opt+5 (gap>=6, forte)
            n_done += 1
            if verdict == "SEPARATOR":
                n_sep += 1
                fs.write(json.dumps({"tt": tt, "tt_hex": f"{tt:#010x}", "opt": opt,
                                     "tree": tree, "gap": gap}) + "\n")
                fs.flush()
                print(f"[w{wid}] *** SEPARATOR *** tt={tt:#010x} opt={opt} tree={tree} gap={gap}", flush=True)
            elif verdict == "gap1":
                n_gap1 += 1
            elif verdict == "gap0":
                n_gap0 += 1
            else:
                n_inc += 1
            w.writerow({"tt": tt, "opt": opt, "tree": tree if tree is not None else "",
                        "gap": gap, "verdict": verdict, "t_sec": f"{time.time()-t1:.2f}"})
            fc.flush()
            if n_done % 100 == 0:
                print(f"[w{wid}] {n_done} f (sep {n_sep}, gap1 {n_gap1}, gap0 {n_gap0}, "
                      f"inc {n_inc}) [{time.time()-t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
