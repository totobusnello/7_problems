**SUSTENTADA** (4ª família, máxima certeza — re-derivação independente confirmou todos os pontos; certificados DRAT re-hasheados e re-resolvidos por dois solvers independentes).

---

### Findings (severidade: CRÍTICA = derruba teorema; ALTA = derruba leitura; MÉDIA = ressalva lógica)

**1. [CRÍTICA] Re-derivação independente de `opt(⊕₃)=6` confirmada por dois solvers e dois circuitos distintos.**
- `tt(par3) = 0x96`, `tt(~par3) = 0x69` (bits `0 1 1 0 1 0 0 1`) — re-computados diretamente de `x1⊕x2⊕x3`. ✓
- **kissat** (própria máquina, esta sessão): `par3 k=4: UNSAT`, `k=5: UNSAT`, `k=6: SAT` com circuito `[(1,1,2,0),(1,0,2,1),(4,1,5,1),(3,1,6,1),(3,0,6,0),(7,1,8,1)]`.
- **Glucose4 via pysat** (solver e código independentes do kissat): `k=5 UNSAT`, `k=6 SAT`. ✓
- Re-simulação manual do circuito de 6 portas nas 8 linhas: bate parity em todas. ✓
- Re-execução de `kissat -q certs/par3_k5.cnf`: `s UNSATISFIABLE`, exit=20. Mesma CNF que foi certificada por `drat-trim`.
- SHA-256 re-computado do DRAT permanente: `6e2a6f081bc3f1cd…` (matching `check_claims_output.txt`). O hash `[:16]` do dossiê é o prefixo correto.

**2. [CRÍTICA] Re-derivação independente de `tree(⊕₃)=9` por DP de ponto fixo própria.**
- Reescrevi o Bellman do zero (sem importar `tree_gap_n3.py`), com base `cost∈{0}↔{0,1,x_i,¬x_i}` e relaxação `cost[a∧b], cost[¬(a∧b)] ← min(…, 1+cost[a]+cost[b])` até ponto fixo.
- Convergiu em 3 rodadas. Distribuição idêntica à reportada: `{0:8, 1:24, 2:64, 3:30, 4:80, 5:32, 7:16, 9:2}` (soma 256 ✓).
- `tree(0x96) = tree(0x69) = 9`. **`gap(⊕₃) = 9 − 6 = 3`** — exatamente como alegado.
- **Testemunha explícita de 9 portas (árvore, fan-out 1 em toda porta interna):**
  `g1=~x1∧x2, g2=x1∧~x2, g3=~(~g1∧~g2)` [XNOR12]; **cópias independentes** `g4=~x1∧x2, g5=x1∧~x2, g6=~(~g4∧~g5)`; `g7=~g3∧~x3, g8=g6∧x3, g9=~(~g7∧~g8)`, saída `~g9`.
  Verificada por simulação e por contagem de fan-out: cada uma das 9 portas internas é usada ≤ 1×; inputs `x1,x2,x3` reaparecem (legal em fórmula). **A挡la do DP, esta testemunha prova `tree ≤ 9` sem depender do script.**

**3. [CRÍTICA] Khrapchenko re-derivado: `|E|²/|A||B| = 12²/(4·4) = 9` folhas ⟹ ≥ 8 portas.**
- Computei diretamente: `A=f⁻¹(0)` tem 4 vértices, `B=f⁻¹(1)` tem 4, e **12** arestas do cubo `Q₃` cruzam o corte `(A,B)` (todas as 12 arestas, pois paridade é bipartida por peso de Hamming).
- Logo `L(⊕₃) ≥ 9` folhas em De Morgan ⟹ ≥ 8 portas binárias.
- Pela equivalência AIG-fórmula ↔ De Morgan-fórmula em nº de portas (cada `∨` vira `∧` com inversões nas arestas/saída; inversões não contam; portas binárias = folhas − 1), `tree(⊕₃) ∈ {8,9}`.
- O DP fecha o valor em **9** — refutando Thm 2 (`gap ∈ {0,1}`) sob qualquer leitura. Note que mesmo o limite inferior fraco `{2,3}` (Khrapchenko sem DP) já refuta o enunciado.

**4. [CRÍTICA] `s = 3` re-derivado de duas formas independentes — Cor 6 (`s ∈ {0,1}`) falsa.**
- **Estrutural:** no circuito ótimo `g₆ = ~(g₄ ∧ g₅)`, `Cone(g₄) = {g₁,g₂,g₃,g₄}` e `Cone(g₅) = {g₁,g₂,g₃,g₅}`. **Interseção = {g₁,g₂,g₃} → s=3.**
- **Aritmético (independente):** computei `opt(g₄-fn)=(x₁⊕x₂)∧¬x₃` [tt=0x06] e `opt(g₅-fn)=¬(x₁⊕x₂)∧x₃` [tt=0x90] por kissat e Glucose4: ambos **UNSAT@3, SAT@4** → `opt=4` (e por simetria NPN, `opt(h₀)=opt(h₁)`). Identidade de inclusão-exclusão:
  `s = 1 + opt(h₀) + opt(h₁) − opt(⊕₃) = 1 + 4 + 4 − 6 = 3`. ✓
- Os dois caminhos dão `s=3`, contradizendo `s ∈ {0,1}`. SHA do DRAT `h_child_k3.drat` re-computado: `d69d7fe22034ad8c…` (matching).

**5. [ALTA] A recursão "tree(f) = min(1+opt(a)+opt(b))" é a falha raiz; nenhuma leitura honesta salva o paper.**
- Pela definição verbal ("fan-out one at every gate — a tree"), os filhos da raiz têm de ser fórmulas também, dando a recursão **correta** `tree(f)=min(1+tree(a)+tree(b))`. Substituir `tree` por `opt` nos filhos é **ilegal**: cola um DAG sob um AND e chama de árvore.
- Sob a definição verbal (standard), `tree(⊕₃)=9`, `gap=3`, **Thm 2 refutado**.
- Sob a "salva" de redefinir `tree:=min(1+opt(a)+opt(b))` ("tree_oneshot"): Thm 2 vira quase-tautologia (`tree≤1+opt` via `f=1∧f`; `tree≥opt` empírico), mas:
  - a grandeza deixou de ser formula size;
  - a comparação no abstract/§3 com `Θ(n²)` (complexidade de fórmula de paridade em De Morgan) torna-se enganosa, pois `tree_oneshot(⊕ₙ)≤opt(⊕ₙ)+1=O(n)`;
  - o ponto fixo do operador tropical `T` descrito em §3/§7 converge para `tree_formula`, NÃO para `tree_oneshot` — então o argumento de §7 ("tropical overshoot ∈ {0,1}") é falso para o `T` efetivamente definido.
- Mesmo nesta leitura "salvadora", **Cor 6 ainda cai** (por s=3 estrutural).

**6. [MÉDIA — contesta uma frase da REV-0009 Grok e da REV-0010 Codex] Teorema 7 não é "independentemente refutado" sob a definição padrão.**
- O enunciado condicional do Thm 7 começa com "gap(f)=1". Para `⊕₃`, `gap=3` sob a definição padrão — então `⊕₃` **não** é contra-exemplo direto da implicação condicional.
- O que cai é: (i) a **prova** do Thm 7 (depende do Cor 6 falso); (ii) a alegação universal posterior de "classificar todo sharing em qualquer AIG ótima".
- Sob `tree_oneshot` (Tabela 1 do autor), a paridade aparece como "gap 1"; nesse sistema interno, `⊕₃` com `s=3` contradiz Thm 7 diretamente.
- Recomendação de linguagem: dizer "Thm 7 fica **sem prova** e sua pretensão classificatória universal é falsa; sob a grandeza interna do autor, é diretamente contraditório" — não "Thm 7 é falso sob a definição padrão".

**7. [ALTA] Teoremas 3 e 4 sobrevivem (concordo com Codex; Grok menos explícito).**
- **Thm 3** ("se AIG ótima não é árvore, então `opt ≥ n`"): a prova publicada tem bug de contagem (diz "k−1 portas estritamente abaixo de g" — falso quando `g=x₁∧x₂`), mas o resultado tem prova simples via incidências: `2m ≥ n + (m−1) + 1` (entradas essenciais + portas não-finais + 1 incidência extra de sharing) `⟹ m ≥ n`. Válido sempre que `gap>0`, não só `gap=1`.
- **Thm 4** ("`opt≤3 ⟹ gap=0`"): a única topologia reconvergente útil de 3 portas é `g₁→g₂→g₃, g₁→g₃`, cuja saída reduz a `0`, `u`, `c∧u` ou `¬c∧u` — todos computáveis com ≤ 2 portas. Mantém-se como fato estrutural.

**8. [ALTA] Coincidência "2 funções com gap=1 em `opt=6` na Tabela 1 = exatamente `0x96` e `0x69`" confirmada.**
- A DP dá **16** funções com `tree_formula=7` (custo 7) e **2** com `tree_formula=9` (paridade e complemento).
- Sob `tree_oneshot`, as 18 funções com `opt=6` (Tabela 1) todas recebem `tree_oneshot=7`, ou seja "gap=1". Dessas, 16 têm `gap_formula=1` (custo real 7) e **2** têm `gap_formula=3` (custo real 9): exatamente paridade e complemento.
- Isto é a "assinatura" de que o autor computou `tree_oneshot` e rotulou como "formula gap". Coincidência não é prova, mas é consistente com o erro de raiz identificado em (5).

**9. [MÉDIA] Reservas que NÃO derrubam a objeção, mas devem ir no contato com o autor.**
- **Não temos o PDF do paper nesta sessão** — trabalhamos sobre as transcrições verbatim do dossiê e das duas revisões. Antes de qualquer comunicação externa, conferir lado-a-lado o PDF (especialmente: enumeração exata de "s" em Cor 6, e se "formula" é definida em alguma seção anterior de modo a compatibilizar com `tree_oneshot`).
- **`drat-trim` não está instalado nesta máquina** — apenas o hash e o output "s VERIFIED" foram preservados. Recomendação: anexar os dois DRATs (11546 + 147189 bytes, hashes `d69d7fe22034ad8c…` e `6e2a6f081bc3f1cd…`) ao contato externo para auditoria independente.
- **Toda a refutation independe do DP.** Mesmo que `tree(⊕₃)=8` (em vez de 9) por algum bug do DP que ninguém enxergou, `gap ∈ {2,3}`, ainda `>1`, e o argumento Khrapchenko + testemunha de 9 portas + `s=3` estrutural/aritmético permanecem.

---

### Veredito final
A refutação **sobrevive a uma quarta passagem adversarial**, com re-derivação independente de todos os pontos críticos por solver e código distintos:

| Alegação | Status | Confiança |
|---|---|---|
| (a) Thm 2 falso sob definição padrão | **SUSTENTADA** — `gap(⊕₃)=3`, Thm 2 também internally inconsistente (def. verbal vs. recursão algébrica) | Total |
| (b) Cor 6 falso | **SUSTENTADA** — `s=3` por via estrutural E aritmética, independente da disputa tree/oneshot | Total |
| (c) Thm 7 sem prova; alegação universal falsa; enunciado condicional não diretamente refutado por `⊕₃` | **SUSTENTADA** (com ajuste de linguagem vs. REV-0009) | Total |
| (d) Thms 3–4 sobrevivem | **SUSTENTADA** — Thm 3 com prova corrigida, Thm 4 intacto | Alta |

A única leitura que "salva" a aritmética do Thm 2 — redefinir `tree` como decomposição de um nível com filhos-`opt` — destrói o significado de "formula size", invalida a comparação com `Θ(n²)` no abstract, torna o argumento tropical de §7 falso, e ainda assim não salva Cor 6/Thm 7. O paper precisa de retratação da identidade de §2 e de nova prova (impossível para o enunciado atual) — ou redefinição honesta da grandeza estudada.

**Pronto para comunicação externa** (após conferir verbatim o PDF lado-a-lado e, idealmente, anexar os dois DRATs de 11 KB / 147 KB ao invés de apenas os hashes).
