# DOSSIÊ — contraexemplo candidato ao Teorema 2 de arXiv:2603.08033 (Krinkin, "The Unit Gap")

## O que o paper afirma (verbatim, v2 de 19 Mar 2026)

- Teorema 2 (Unit Gap): "For every Boolean function f in the AIG basis with free inversions, gap(f) ∈ {0,1}",
  onde gap(f) = tree(f) − opt(f), tree(f) = "minimum formula size" e formula = "a circuit in which every
  gate has fan-out one — a tree".
- A prova do upper bound: "The trivial decomposition f = 1∧f gives tree(f) ≤ 1 + opt(f), since opt(1)=0."
- No §2 o paper exibe: "The minimum formula size satisfies: tree(f) = min_{a,b: f=a∧b ou f̄=a∧b} (1 + opt(a) + opt(b))."
- Tabela 1 (n=3 completo): nenhuma função com gap > 1; em opt=6 há exatamente 2 funções com "gap=1".

## Nossa objeção (a auditar adversarialmente)

A identidade do §2 é FALSA para "minimum formula size" padrão: numa fórmula (árvore de portas), os
subcircuitos que computam a e b têm de ser TAMBÉM fórmulas — a recursão correta é
tree(f) = min (1 + tree(a) + tree(b)), não 1 + opt(a) + opt(b). Com opt nos filhos, a "tree" definida
é ≤ opt(f)+1 POR CONSTRUÇÃO (via f = 1∧f), e o Teorema 2 vira tautologia sobre uma grandeza que não
é formula size. Nota: inputs podem repetir numa fórmula (fan-out livre nas FOLHAS); a restrição é só
nas portas.

## Contraexemplo computado (pod EPYC, 2026-07-11, script /workspace/pilot/tree_gap_n3_v2.py;
cópia local: Projetos/7_problems/PNP_AI/experiments/exp_pilot_n5/… a versionar)

- opt(f) para as 256 funções de n=3: via encoder SAT validado (G3: n=2 exaustivo, n=3 bidirecional
  k≤4, cross-check com enumerador independente) + kissat. Max opt = 6.
- tree(f): programação dinâmica exata de ponto fixo sobre as 256 funções:
  v(f) = min sobre pares (a,b) com a∧b ∈ {f, ¬f} de 1 + v(a) + v(b); base v=0 em constantes e
  literais (ambas polaridades). Isso computa o tamanho mínimo de fórmula AIG com inversões livres
  em arestas e saída e folhas repetíveis.
- Resultado: distribuição de gap = {0: 214, 1: 40, 3: 2}. As 2 funções com gap 3:
  tt=0x96 (paridade x1⊕x2⊕x3) e tt=0x69 (complemento): opt=6, tree=9.
- Consistência com teoria clássica: Khrapchenko dá L(⊕3) ≥ 9 folhas ⟹ ≥ 8 portas binárias; a
  construção balanceada dá 10 folhas/9 portas; nosso DP achou exatamente 9 portas (fórmula AIG e
  fórmula De Morgan têm o mesmo nº de portas — inversões empurram para as folhas).
- Coincidência reveladora: as "2 funções com gap=1 em opt=6" da Tabela 1 do paper são exatamente
  estas — a recursão com opt nos filhos reporta 1 onde o valor verdadeiro é 3.

## Perguntas ao revisor adversarial (tente DERRUBAR a objeção)

1. A identidade tree(f) = min(1+opt(a)+opt(b)) pode ser salva sob alguma leitura razoável de
   "formula" (ex.: definição não-padrão em que sub-DAGs contam como folhas)? Se sim, o abstract e a
   comparação com formula complexity clássica (§3 cita parity Θ(n²) De Morgan) continuam honestos?
2. Nosso DP de tree está correto? Procure buracos: base cases, polaridades, repetição de folhas,
   convergência do ponto fixo, e a equivalência AIG-formula ↔ De Morgan-formula em nº de portas.
3. opt(⊕3)=6 está certo? (kissat + encoder validado; conferir com o que se sabe de paridade em AIG:
   3 portas por XOR, 2 XORs.)
4. gap(⊕3)=3 contradiz mesmo o enunciado? Alguma leitura do enunciado sob a qual sobrevive?
5. Consequências: Teoremas 3/4/7 e a Tabela 1 caem juntos ou algum sobrevive com a definição do autor?
6. VEREDITO: objeção SUSTENTADA (Teorema 2 falso sob definição padrão) ou DERRUBADA. Português.
