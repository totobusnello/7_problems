(node:51770) ExperimentalWarning: SQLite is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
Vou ler todos os documentos e scripts do experimento para fazer a revisão adversarial.SUSTENTADA

---

### Limitação de leitura
O PDF `krinkin_2026_unit_gap.pdf` não pôde ser extraído neste modo somente-leitura (o arquivo é binário e as ferramentas de extração estão bloqueadas). No entanto, as revisões anteriores e o dossiê transcrevem verbatim os enunciados críticos do paper (Teorema 2, Corolário 6, Teorema 7, Tabela 1, §2, §3), e eu re-derivei independentemente os valores e as recursões a partir do código e da teoria clássica. A análise abaixo não depende de acesso direto ao PDF.

---

## Findings numerados (severidade)

**1. [CRÍTICA — ALTA] Erro raiz na recursão do §2: troca ilegítima de `tree` por `opt` nos filhos.**  
O paper define verbalmente *formula* como AIG em que "toda porta tem fan-out 1 — uma árvore". A recursão correta para tamanho mínimo de fórmula é

\[
\mathrm{tree}(f)=\min_{f=a\land b\ \text{ou}\ \bar f=a\land b}\bigl(1+\mathrm{tree}(a)+\mathrm{tree}(b)\bigr),
\]

com base 0 em constantes e literais. O paper escreve em §2:

\[
\mathrm{tree}(f)=\min\bigl(1+\mathrm{opt}(a)+\mathrm{opt}(b)\bigr).
\]

Isso não computa tamanho de fórmula: os filhos `a` e `b` são representados por circuitos DAGs ótimos, que podem compartilhar portas internamente; colocá-los sob um novo AND não produz uma árvore. A "prova" do Teorema 2 usa a decomposição `f=1∧f` para obter `tree(f)≤1+opt(f)`; sob a definição padrão essa decomposição só dá `tree(f)≤1+tree(f)`, uma tautologia inútil.

**2. [CRÍTICA — ALTA] `⊕₃` é contraexplo explícito: `opt=6`, `tree=9`, `gap=3`.**  
Construção ótima (DAG, 6 portas):

\[
\begin{aligned}
g_1&=x_1\land\bar x_2,\\
g_2&=\bar x_1\land x_2,\\
g_3&=\overline{\bar g_1\land\bar g_2}=x_1\oplus x_2,\\
g_4&=g_3\land\bar x_3,\\
g_5&=\bar g_3\land x_3,\\
g_6&=\overline{\bar g_4\land\bar g_5}=x_1\oplus x_2\oplus x_3.
\end{aligned}
\]

`g₃` tem fan-out 2, logo não é fórmula; portanto `opt(⊕₃)≤6`. O SAT-encoder (`check_unitgap_claims.py`) devolve `UNSAT@5` com prova DRAT verificada, e o paper próprio reporta `max opt=6` para `n=3`. Logo `opt(⊕₃)=6`.

Para fórmula, as duas cópias de `x₁⊕x₂` não podem compartilhar `g₃`; replicando-se obtemos 9 portas:

\[
\text{2 cópias de }x_1\oplus x_2\;(3+3\text{ portas})+\text{combinação com }x_3\;(3\text{ portas})=9.
\]

Assim `tree(⊕₃)≤9`. Pelo DP exato (`tree_gap_n3.py`) e por Khrapchenko, `tree(⊕₃)=9`. Portanto

\[
\mathrm{gap}(\oplus_3)=9-6=3\notin\{0,1\}.
\]

**3. [ALTA] O DP de `tree` e o lower bound de Khrapchenko estão corretos.**  
O DP implementa exatamente o operador de Bellman da recursão padrão:
- base em `0, 1, xᵢ, ¬xᵢ` com custo 0;
- iteração `tree[g] = min(tree[g], 1+tree[a]+tree[b])` para `g=a∧b` e `g^MASK` para cobrir inversão de saída;
- `a,b` percorrem todas as funções, cobrindo inversões internas;
- folhas repetíveis são permitidas; fan-out 1 vale só para portas;
- ponto fixo converge porque o reticulado é finito e os custos decrescem monotonicamente.

Resultado do script para `n=3`: distribuição `{0:214, 1:40, 3:2}`; as duas funções com gap 3 são `0x96` (`⊕₃`) e `0x69` (`¬⊕₃`).

Khrapchenko para `⊕₃`: `A=f⁻¹(0)`, `B=f⁻¹(1)`, `|A|=|B|=4`, cada vértice de `A` tem 3 vizinhos em `B`, logo `|E|=12`. Então

\[
L(\oplus_3)\ge \frac{|E|^2}{|A||B|}=\frac{144}{16}=9\text{ folhas}.
\]

Como fórmula AIG com inversões livres ↔ fórmula De Morgan preserva o número de portas binárias, 9 folhas implicam ≥8 portas. O DP exclui 8 e fecha em 9. (REV-0009 deixou `tree∈{8,9}`; REV-0010 e o DP fecham exatamente em 9.)

**4. [CRÍTICA — ALTA] Corolário 6 (`s∈{0,1}`) é falso: no circuito ótimo de `⊕₃` temos `s=3`.**  
Na decomposição pela porta de saída `g₆`, os dois filhos são

\[
h_0=g_4=(x_1\oplus x_2)\land\bar x_3,\qquad
h_1=g_5=\overline{(x_1\oplus x_2)}\land x_3.
\]

Ambos contêm o sub-DAG completo de `x₁⊕x₂` (`g₁,g₂,g₃`), logo

\[
s=|D_{h_0}\cap D_{h_1}|=3.
\]

Tem-se `opt(h_0)=opt(h_1)=4` (`UNSAT@3` certificado; a restrição `x₃=0` de `h₀` reduz a `⊕₂`, que exige 3 portas, e mais uma porta para o AND com `¬x₃`). A identidade de decomposição

\[
\mathrm{opt}(f)=1+\mathrm{opt}(h_0)+\mathrm{opt}(h_1)-s
=1+4+4-3=6
\]

confirma `s=3`. Logo `s∉{0,1}`.

**5. [ALTA] Teorema 7 fica sem prova; sua alegação universal é falsa, mas o enunciado condicional a `gap=1` não é refutado só por `⊕₃`.**  
A prova do Teorema 7 depende do Corolário 6 (`s≤1`), que é falso. Portanto a prova cai. A alegação de que o teorema "classifica todo compartilhamento em qualquer AIG ótimo" é falsa, pois `⊕₃` é um AIG ótimo com `s=3`.  
Entretanto, o enunciado formal começa com "se `gap(f)=1`…". Como `gap(⊕₃)=3`, `⊕₃` não é contraexemplo a esse condicional. Precisão da REV-0010: o Teorema 7 fica **não provado**, não **refutado** por `⊕₃` sob a definição padrão. Sob a grandeza espúria efetivamente usada na Tabela 1 (que classifica `⊕₃` como "gap 1"), o mesmo circuito com `s=3` contradiz o Teorema 7 diretamente.

**6. [MÉDIA] Teoremas 3 e 4 sobrevivem.**  
Teorema 4 é análise exaustiva de topologias com ≤3 portas e não usa a recursão falsa. Teorema 3 também sobrevive, mas a prova publicada tem uma contagem defeituosa (como apontado na REV-0010: a afirmação `|S|≥k−1` falha quando `g` é porta de entrada). A correção por contagem de fan-out é válida: num circuito ótimo com `m` portas e `n` entradas essenciais, se há compartilhamento então

\[
2m\ge n+(m-1)+1=n+m\;\Longrightarrow\;m\ge n.
\]

Isso vale sempre que `gap>0`, não apenas `gap=1`.

**7. [ALTA] Nenhuma leitura honesta salva o Teorema 2.**  
A única forma de fazer a aritmética `gap∈{0,1` fechar é redefinir

\[
d(f)=\min\bigl(1+\mathrm{opt}(a)+\mathrm{opt}(b)\bigr),
\]

a grandeza efetivamente computada no §2. Mas `d(f)` não é tamanho de fórmula: seus filhos são DAGs e a comparação do abstract/§3 com a complexidade clássica `Θ(n²)` da paridade em base De Morgan torna-se falsa (sob `d`, a paridade teria "fórmula" `O(n)`). Além disso, o operador tropical descrito nas §§3/7 é o Bellman padrão — cujo ponto fixo é `tree` verdadeiro, não `d`. O paper contradiz a própria definição verbal: salvar a matemática destrói o significado.

---

## Re-derivação resumida

| Grandeza | Valor | Justificativa |
|---|---|---|
| `opt(⊕₃)` | 6 | Construção 2 XORs×3 portas; `UNSAT@5` DRAT-verificado; paper reporta `max opt=6` para `n=3`. |
| `tree(⊕₃)` | 9 | Construção explícita com 9 portas (cópias disjuntas de `⊕₂`); Khrapchenko dá ≥8; DP exato exclui 8. |
| `gap(⊕₃)` | 3 | `9−6`. |
| Khrapchenko | `144/16=9` folhas | `\|A\|=\|B\|=4`, `\|E\|=12`. |
| `s` na raiz do circuito ótimo | 3 | Os dois filhos compartilham as 3 portas de `x₁⊕x₂`; `1+4+4−3=6`. |

---

## Avaliação das revisões anteriores

- **REV-0009 (Grok):** SUSTENTADA. Nenhum erro material a contestar. A ressalva `tree∈{8,9}` é conservadora e suficiente para refutar o Teorema 2.
- **REV-0010 (Codex):** SUSTENTADA. A enumeração independente por camadas (`24,64,30,80,32,0,16,0,2`, soma 248 + 8 bases = 256) confirma `tree=9` exato. A correção da prova do Teorema 3 por contagem de fan-out é válida. A precisão sobre o Teorema 7 (condicional não refutado por `⊕₃`) está correta e é importante.

---

## VEREDICTO FINAL

A refutação **aguenta**. O Teorema 2 é falso sob a definição padrão de fórmula. A causa é a substituição de `tree(a)+tree(b)` por `opt(a)+opt(b)` na recursão de §2, que faz o paper medir uma grandeza espúria `d(f)` em vez do tamanho de fórmula. O contraexemplo `⊕₃` (`opt=6`, `tree=9`, `gap=3`) é sólido e verificado computacionalmente. Corolário 6 cai com `s=3`. Teorema 7 fica sem prova e com alegação universal falsa. Teoremas 3 e 4 sobrevivem. Não há leitura honesta que salve o paper sem redefinir seus termos centrais.
