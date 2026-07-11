"""
EXP-PED-0001 — Redução pedagógica: 3-COLORING -> SAT (pysat/Glucose4)

Propósito (trilha pedagógica, FASE 2): demonstrar concretamente o que é uma
redução polinomial — o conceito central de NP-completude (Cook 1971, Karp 1972).
CHROMATIC NUMBER está na lista de Karp; aqui usamos o caso 3 cores.

Codificação: variável booleana x[v,c] = "vértice v recebe cor c".
  (1) todo vértice tem >= 1 cor:        (x[v,0] v x[v,1] v x[v,2])
  (2) nenhum vértice tem 2 cores:       (~x[v,c] v ~x[v,c']) p/ c < c'
  (3) vizinhos não compartilham cor:    (~x[u,c] v ~x[v,c]) p/ cada aresta {u,v}

Tamanho da redução: O(|V| + |E|) cláusulas — polinomial (de fato, linear).

CONCLUSÃO PERMITIDA: a redução preserva sim/não nas instâncias testadas e
ilustra o mecanismo de reduções; o solver encontra certificados (colorações)
ou prova UNSAT nos casos finitos dados.
CONCLUSÃO NÃO PERMITIDA: nada sobre P vs NP — resolver instâncias pequenas
não diz nada sobre o pior caso assintótico.
"""

from itertools import combinations
from pysat.solvers import Glucose4

K = 3  # cores


def encode_3col(n_vertices, edges):
    """Retorna lista de cláusulas CNF (DIMACS: ints != 0)."""
    # validação de entrada (REV-0002/Kimi, finding 7): arestas fora do range
    # criariam variáveis espúrias e invalidariam a contagem 4n+3|E| em silêncio
    for u, v in edges:
        if not (0 <= u < n_vertices and 0 <= v < n_vertices) or u == v:
            raise ValueError(f"aresta inválida ({u},{v}) para n={n_vertices}")

    def var(v, c):  # variáveis 1..n*K
        return v * K + c + 1

    clauses = []
    for v in range(n_vertices):
        clauses.append([var(v, c) for c in range(K)])              # (1)
        clauses.extend([-var(v, a), -var(v, b)] for a, b in combinations(range(K), 2))  # (2)
    for u, v in edges:
        clauses.extend([-var(u, c), -var(v, c)] for c in range(K))  # (3)
    return clauses


def solve(name, n, edges):
    clauses = encode_3col(n, edges)
    with Glucose4(bootstrap_with=clauses) as s:
        ok = s.solve()
        model = s.get_model() if ok else None
    print(f"{name}: |V|={n} |E|={len(edges)} clausulas={len(clauses)} -> "
          f"{'SAT (3-coloravel)' if ok else 'UNSAT (nao 3-coloravel)'}")
    if ok:
        # verificação independente do certificado (o ponto pedagógico de NP!)
        # REV-0002/Kimi, finding 1: conferir EXATAMENTE UMA cor por vértice,
        # sem confiar no solver — rejeita atribuições com 0 ou >=2 cores.
        true_colors = {v: [c for c in range(K) if model[v * K + c] > 0]
                       for v in range(n)}
        assert all(len(cs) == 1 for cs in true_colors.values()), \
            f"certificado inválido: vértices sem cor única: " \
            f"{ {v: cs for v, cs in true_colors.items() if len(cs) != 1} }"
        coloring = {v: cs[0] for v, cs in true_colors.items()}
        assert all(coloring[u] != coloring[v] for u, v in edges), "certificado inválido"
        print(f"  certificado (verificado em tempo linear): {coloring}")


if __name__ == "__main__":
    # C5: ciclo ímpar, 3-colorável
    solve("C5 (ciclo de 5)", 5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    # Petersen: 3-cromático
    petersen = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
                (0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
    solve("Petersen", 10, petersen)
    # K4: exige 4 cores -> UNSAT com 3
    solve("K4 (completo de 4)", 4, list(combinations(range(4), 2)))
