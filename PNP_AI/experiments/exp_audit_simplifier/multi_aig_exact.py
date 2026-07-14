"""Exact synthesis AIG MULTI-OUTPUT via SAT — extensão do aig_exact.py validado.

Modelo: k portas AND-2 com polaridades livres nas arestas (como sempre); m saídas,
cada uma seleciona UM nó (constante-0, entrada ou porta) + polaridade de saída.
Custo = k (nº de ANDs, compartilhados entre as saídas — é onde mora o ganho).

Normalizações (sound para busca ascendente, mesmo argumento do single-output):
- dedup de portas (circuito multi-output MÍNIMO não tem portas duplicadas:
  remover a duplicata e religar consumidores/saídas dá circuito menor);
- toda porta é usada por outra porta OU selecionada por alguma saída.

Gates pré-registrados (rodar gate_multi.py ANTES de qualquer auditoria):
  G-M1: reduções single-output — 256/256 tts reproduzem a tabela opt3 certificada;
  G-M2: identidades ((f,~f) custa opt(f); pares amostrados vs enumeração exaustiva).
"""
import subprocess
import tempfile
import os
from itertools import combinations


def tt_bit(tt, t):
    return (tt >> t) & 1


class MultiAIGEncoder:
    def __init__(self, n, k, tts):
        self.n, self.k = n, k
        self.tts = list(tts)
        self.m = len(self.tts)
        self.rows = 1 << n
        self.nvars = 0
        self.clauses = []
        self.v = {(i, t): self._new() for i in range(1, k + 1) for t in range(self.rows)}
        self.options = {}
        for i in range(1, k + 1):
            opts = []
            nodes = list(range(1, self.n + i))
            for a, b in combinations(nodes, 2):
                for pa in (0, 1):
                    for pb in (0, 1):
                        opts.append((a, pa, b, pb, self._new()))
            self.options[i] = opts
        # seleção de saída: nó 0 = constante-0; 1..n entradas; n+1..n+k portas
        self.osel = {}   # (o, node) -> var
        self.opol = {}   # o -> var
        for o in range(self.m):
            for node in range(0, self.n + k + 1):
                self.osel[(o, node)] = self._new()
            self.opol[o] = self._new()

    def _new(self):
        self.nvars += 1
        return self.nvars

    def _lit(self, node, pol, t):
        if node <= self.n:
            bit = 0 if node == 0 else (t >> (node - 1)) & 1
            return "const", bit ^ pol
        var = self.v[(node - self.n, t)]
        return "lit", (-var if pol else var)

    def build(self):
        c = self.clauses
        # portas (idêntico ao single-output validado)
        for i in range(1, self.k + 1):
            svars = [o[4] for o in self.options[i]]
            c.append(svars)
            c.extend([-x, -y] for x, y in combinations(svars, 2))
            for a, pa, b, pb, s in self.options[i]:
                for t in range(self.rows):
                    x = self.v[(i, t)]
                    ka, la = self._lit(a, pa, t)
                    kb, lb = self._lit(b, pb, t)
                    if (ka == "const" and la == 0) or (kb == "const" and lb == 0):
                        c.append([-s, -x])
                    elif ka == "const" and kb == "const":
                        c.append([-s, x])
                    elif ka == "const":
                        c.append([-s, -x, lb]); c.append([-s, x, -lb])
                    elif kb == "const":
                        c.append([-s, -x, la]); c.append([-s, x, -la])
                    else:
                        c.append([-s, -x, la]); c.append([-s, -x, lb])
                        c.append([-s, x, -la, -lb])
        # dedup entre portas
        by_tuple = {}
        for i in range(1, self.k + 1):
            for a, pa, b, pb, s in self.options[i]:
                by_tuple.setdefault((a, pa, b, pb), []).append(s)
        for svars in by_tuple.values():
            if len(svars) > 1:
                c.extend([-x, -y] for x, y in combinations(svars, 2))
        # seleção de saída: one-hot por saída
        for o in range(self.m):
            sv = [self.osel[(o, node)] for node in range(0, self.n + self.k + 1)]
            c.append(sv)
            c.extend([-x, -y] for x, y in combinations(sv, 2))
        # semântica da saída o na linha t: sel(node) -> (valor(node) ^ opol) == tt_o(t)
        for o in range(self.m):
            po = self.opol[o]
            for node in range(0, self.n + self.k + 1):
                s = self.osel[(o, node)]
                for t in range(self.rows):
                    want = tt_bit(self.tts[o], t)
                    kd, val = self._lit(node, 0, t)
                    if kd == "const":
                        # (val ^ pol) == want  <=>  pol == (val ^ want)
                        need_pol = val ^ want
                        c.append([-s, po] if need_pol else [-s, -po])
                    else:
                        x = val  # var da porta
                        if want:  # x ^ pol = 1
                            c.append([-s, -po, -x]); c.append([-s, po, x])
                        else:
                            c.append([-s, -po, x]); c.append([-s, po, -x])
        # toda porta usada: por outra porta ou por seleção de saída
        for i in range(1, self.k + 1):
            node = self.n + i
            users = [op[4] for j in range(i + 1, self.k + 1)
                     for op in self.options[j] if op[0] == node or op[2] == node]
            users += [self.osel[(o, node)] for o in range(self.m)]
            c.append(users if users else [])
        return self

    def decode(self, model):
        pos = {abs(l) for l in model if l > 0}
        gates = []
        for i in range(1, self.k + 1):
            sel = [o for o in self.options[i] if o[4] in pos]
            assert len(sel) == 1
            gates.append(sel[0][:4])
        outs = []
        for o in range(self.m):
            nodes = [node for node in range(0, self.n + self.k + 1) if self.osel[(o, node)] in pos]
            assert len(nodes) == 1
            outs.append((nodes[0], self.opol[o] in pos))
        return gates, outs


def simulate_multi(n, gates, outs, t):
    vals = {0: 0}
    for j in range(1, n + 1):
        vals[j] = (t >> (j - 1)) & 1
    node = n
    for a, pa, b, pb in gates:
        node += 1
        vals[node] = (vals[a] ^ pa) & (vals[b] ^ pb)
    return [vals[nd] ^ (1 if pol else 0) for nd, pol in outs]


def verify_multi(n, tts, gates, outs):
    for t in range(1 << n):
        got = simulate_multi(n, gates, outs, t)
        for o, tt in enumerate(tts):
            if got[o] != tt_bit(tt, t):
                return False
    return True


def trivial_multi(n, tts):
    """k=0 possível? Toda saída é constante ou ±literal."""
    rows = 1 << n
    mask = (1 << rows) - 1
    cands = {0, mask}
    for j in range(n):
        v = sum(1 << t for t in range(rows) if (t >> j) & 1)
        cands |= {v, v ^ mask}
    return all(tt in cands for tt in tts)


def solve_k(n, tts, k, timeout=None):
    enc = MultiAIGEncoder(n, k, tts).build()
    if any(len(cl) == 0 for cl in enc.clauses):
        return False, None
    with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
        path = f.name
        f.write(f"p cnf {enc.nvars} {len(enc.clauses)}\n")
        for cl in enc.clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    try:
        r = subprocess.run(["kissat", "-q", path], capture_output=True,
                           text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if r.returncode == 10:
        model = []
        for line in r.stdout.splitlines():
            if line.startswith("v "):
                model.extend(int(x) for x in line[2:].split() if x != "0")
        gates, outs = enc.decode(model)
        assert verify_multi(n, tts, gates, outs), "modelo SAT nao simula! bug"
        return True, (gates, outs)
    assert r.returncode == 20, f"kissat rc={r.returncode}"
    return False, None


def opt_multi(n, tts, kmax=15, timeout=None):
    if trivial_multi(n, tts):
        return 0
    for k in range(1, kmax + 1):
        sat, _ = solve_k(n, tts, k, timeout=timeout)
        if sat:
            return k
    return None
