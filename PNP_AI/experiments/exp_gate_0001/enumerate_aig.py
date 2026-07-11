"""
EXP-GATE-0001 / G3 — Enumeração exaustiva INDEPENDENTE de circuitos AIG.

Propósito (regra REV-0004): validar a SEMÂNTICA do encoder SAT por um caminho
que não compartilha nada com ele — busca bruta direta sobre circuitos.
opt(f) = menor número de portas AND tal que alguma sequência de portas
g_1..g_d (cada uma = AND de dois nós anteriores com polaridades livres)
produz f (a menos de inversão de saída) na ÚLTIMA porta adicionada.

Justificativa de "última porta": se f aparece na porta j de um circuito com
d > j portas, o prefixo até j é um circuito de j portas para f — logo basta
registrar cada função na primeira profundidade em que aparece como porta
recém-criada ao longo da recursão.
"""

import sys
from functools import lru_cache


def enumerate_opts(n, max_gates):
    """Retorna dict f_tt -> opt (0..max_gates) para todas as funções alcançáveis."""
    rows = 1 << n
    mask = (1 << rows) - 1
    inputs = tuple(sum(((t >> j) & 1) << t for t in range(rows)) for j in range(n))

    opt = {}

    def note(tt, d):
        for g in (tt, tt ^ mask):  # inversão de saída é livre
            if g not in opt or opt[g] > d:
                opt[g] = d

    # opt = 0: constantes e literais
    note(0, 0)
    for x in inputs:
        note(x, 0)

    seen_states = set()

    def rec(nodes, depth):
        state = (depth, tuple(sorted(nodes)))
        if state in seen_states:
            return
        seen_states.add(state)
        if depth == max_gates:
            return
        m = len(nodes)
        for i in range(m):
            for j in range(i + 1, m):
                for a in (nodes[i], nodes[i] ^ mask):
                    for b in (nodes[j], nodes[j] ^ mask):
                        g = a & b
                        note(g, depth + 1)
                        rec(nodes + (g,), depth + 1)

    rec(inputs, 0)
    return opt


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    opts = enumerate_opts(n, k)
    rows = 1 << n
    total = 1 << rows
    from collections import Counter
    dist = Counter(opts.values())
    print(f"n={n}, até {k} portas: {len(opts)}/{total} funções alcançadas")
    print("distribuição de opt:", dict(sorted(dist.items())))
