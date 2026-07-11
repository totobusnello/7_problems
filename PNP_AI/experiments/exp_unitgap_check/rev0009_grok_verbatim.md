**SUSTENTADA**

Li o paper (arXiv:2603.08033v2) e o dossiê. Abaixo, as 6 perguntas — tentando, de fato, salvar o Teorema 2 antes de concluir que não dá.

---

### 1. A identidade `tree(f) = min(1+opt(a)+opt(b))` salva-se sob alguma leitura?

**Só sob redefinição não-padrão, e aí o paper fica desonesto.**

Há **duas grandezas distintas** misturadas no texto:

- **(A) `tree_formula`** — tamanho mínimo de fórmula no sentido clássico (DAG em que toda *porta* tem fan-out 1; folhas/variáveis podem repetir). Recursão correta:
  \[
  \mathrm{tree}_{\mathrm{formula}}(f)=\min_{a,b:\,f=a\land b\ \mathrm{ou}\ \bar f=a\land b}\bigl(1+\mathrm{tree}_{\mathrm{formula}}(a)+\mathrm{tree}_{\mathrm{formula}}(b)\bigr),
  \]
  com base 0 em constantes e literais. É o ponto fixo do operador de Bellman \(T\) a partir de \(v_0(x_i)=v_0(1)=0\) — exactamente o que o paper *diz* em §3 e §7.

- **(B) `tree_oneshot`** — a identidade escrita em §2:
  \[
  \mathrm{tree}_{\mathrm{oneshot}}(f)=\min\bigl(1+\mathrm{opt}(a)+\mathrm{opt}(b)\bigr).
  \]
  Isso *não* é formula size: os filhos podem ser DAGs arbitrários. Colar `opt(a)` e `opt(b)` sob um AND **não produz uma fórmula**, a menos que `a` e `b` já sejam árvores e não partilhem portas.

O “upper bound” do Teorema 2 (`f=1∧f ⇒ tree ≤ 1+opt`) vale **apenas** para (B). Para (A) a mesma decomposição dá só
\[
\mathrm{tree}_{\mathrm{formula}}(f)\le 1+\mathrm{tree}_{\mathrm{formula}}(1)+\mathrm{tree}_{\mathrm{formula}}(f)=1+\mathrm{tree}_{\mathrm{formula}}(f),
\]
uma tautologia inútil. Não liga `tree` a `opt`.

Leituras de salvamento e por que falham:

| Leitura | Salva Thm 2? | Problema |
|---|---|---|
| “Fórmula” = árvore só na raiz, filhos = DAGs óptimos contados a `opt` | Sim (quase tautológico) | Contradiz a definição verbal (“fan-out one at every gate — a tree”) e a comparação com complexidade de fórmulas clássica |
| Sub-DAGs contam como “folhas” de custo `opt` | Idem | Não é o modelo de Shannon/Khrapchenko/Jukna; chamar isso de formula size é equívoco |
| O Bellman iterado a partir de 0 (texto de §3/§7) | Não | Aí o upper bound da prova é inválido; ⊕₃ é contraexemplo |

Sobre honestidade do abstract/§3: o paper invoca explicitamente
> “parity on n variables has formula complexity Θ(n²) [De Morgan] but circuit complexity O(n). The collapse to a gap of at most 1 in the AIG basis arises from … constant 1 … and free complementation.”

Sob (B), `tree_oneshot(⊕_n) ≤ opt(⊕_n)+1 = O(n)`, e a comparação com Θ(n²) é **falsa**. Constante 1 livre e inversões livres **não** colapsam formula size de paridade para `opt+1`; só tornam a desigualdade tautológica para a grandeza errada. Portanto: mesmo a leitura que salva a matemática do Thm 2 torna abstract e §3 enganosos.

Há ainda **contradição interna**: §2 define (B); §3/§7 afirmam que o ponto fixo de \(T\) desde \(v_0=0\) é `tree` (isso é (A)). São funções diferentes. Para ⊕₃, `tree_oneshot=7` e `tree_formula∈{8,9}`.

---

### 2. O DP de `tree` do dossiê está correto?

**Sim, com ressalva menor em 8 vs 9 — irrelevante para o gap > 1.**

O que o DP computa é exactamente `tree_formula` no modelo AIG com inversões livres:

- **Base:** constantes e literais (ambas polaridades) com custo 0 — correto (`opt=0` e `tree=0`).
- **Passo:** \(v(f)=\min 1+v(a)+v(b)\) sobre \(a\land b\in\{f,\bar f\}\) — cobre AND e OR (OR via \(\overline{\bar a\land\bar b}\), com \(a,b\) a variar sobre todas as 256 funções).
- **Polaridade de saída livre:** o “ou \(\bar f\)” no min, mais \(v(\bar f)=v(f)\) por indução.
- **Repetição de folhas:** livre (inputs têm custo 0; a restrição de fan-out 1 é só em portas). Correto para fórmulas.
- **Ponto fixo monótono** num reticulado finito: converge para o mínimo.
- **AIG-fórmula ↔ De Morgan-fórmula em nº de portas:** sim — cada \(\lor\) vira um AND com inversões nas arestas/saída; NOT não conta. Número de portas binárias = nº de folhas − 1 (sem constantes inúteis).

**Construção explícita (upper bound):**
\[
\begin{align*}
g_1&=x\land\lnot y,\quad g_2=\lnot x\land y,\quad g_3=\lnot(\lnot g_1\land\lnot g_2) &&\text{// cópia 1 de }x\oplus y\\
g_4&=x\land\lnot y,\quad g_5=\lnot x\land y,\quad g_6=\lnot(\lnot g_4\land\lnot g_5) &&\text{// cópia 2}\\
g_7&=g_3\land\lnot z,\quad g_8=\lnot g_6\land z,\quad g_9=\lnot(\lnot g_7\land\lnot g_8).
\end{align*}
\]
Árvore de **9** ANDs (cada porta fan-out ≤ 1; inputs com fan-out livre). Logo \(\mathrm{tree}_{\mathrm{formula}}(\oplus_3)\le 9\).

**Lower bound:** Khrapchenko ⇒ \(L(\oplus_3)\ge 9\) folhas em De Morgan ⇒ ≥ 8 portas binárias. Com a equivalência acima, \(\mathrm{tree}_{\mathrm{formula}}(\oplus_3)\ge 8\).

Portanto \(\mathrm{tree}\in\{8,9\}\). O DP reportar 9 é compatível com a construção composicional (que dá 10 folhas / 9 portas); se existir fórmula com 9 folhas / 8 portas, o DP teria um buraco, **mas gap seria 2, ainda > 1**. Não consegui executar o script aqui (sandbox), porém o intervalo {8,9} basta e não depende do DP.

Buracos que *não* existem: base, polaridades, folhas repetíveis, convergência, equivalência AIG/De Morgan.

---

### 3. `opt(⊕₃)=6` está certo?

**Sim.**

- Construção DAG: dois XORs encadeados, cada XOR = 3 ANDs, reutilizando a saída do primeiro (fan-out 2) → 6 portas.
- O próprio paper (Tabela 1) tem máximo `opt=6` em n=3, com exactamente 16 funções — e as 2 com “gap=1” em opt=6 são, como o dossiê nota, precisamente ⊕₃ e seu complemento (tt `0x96` e `0x69`).
- Encoder SAT do projeto (validado G3: n=2 exaustivo, n=3 bidirecional, cross-check) + kissat: consistente.
- Não há AIG de 5 portas para ⊕₃: enumeração completa n=3 é factível e o catálogo do autor confirma max=6.

Acordo total entre dossiê, paper e teoria.

---

### 4. `gap(⊕₃)=3` (ou ≥2) contradiz o enunciado? Alguma leitura salva o Thm 2?

**Contradiz o enunciado sob a definição que o paper *escreve em palavras*.**

Enunciado (Thm 2): *For every Boolean function f in the AIG basis with free inversions, gap(f)∈{0,1}*, com `gap=tree−opt` e *“a formula … fan-out one at every gate — a tree”*.

Sob essa definição (= `tree_formula`):
\[
\mathrm{gap}(\oplus_3)=\mathrm{tree}_{\mathrm{formula}}(\oplus_3)-\mathrm{opt}(\oplus_3)\in\{2,3\}\not\subset\{0,1\}.
\]
Contraexemplo explícito, n=3, verificável à mão na parte ≤9 e por Khrapchenko na parte ≥8.

Leituras sob as quais o enunciado “sobrevive”:

1. **Redefinir `tree`:=`tree_oneshot`.** Aí `gap(⊕₃)=1` e Thm 2 vira quase tautologia (`tree_oneshot≤1+opt` por `f=1∧f`; `tree_oneshot≥opt` nem sempre é óbvio mas empiricamente vale na Tabela 1). **Porém** deixa de ser o gap formula-vs-circuito anunciado, e a prova em §3 de que o ponto fixo de \(T\) “overshoots by 0 or 1” torna-se falsa (o ponto fixo é `tree_formula`, não `tree_oneshot`).

2. **“Gap” medido só na decomposição de topo de um circuito óptimo** (`s` de Cor. 6). Também não salva: ver pergunta 5 — em ⊕₃ tem-se `s=3`.

Nenhuma leitura **razoável e honesta com o abstract** salva o Thm 2. A que salva a aritmética destrói o significado.

---

### 5. Consequências para Thms 3/4/7 e Tabela 1

| Resultado | Sob def. padrão (`tree_formula`) | Sob def. do autor em §2 (`tree_oneshot`) |
|---|---|---|
| **Thm 2 (Unit Gap)** | **Falso** (⊕₃) | Verdadeiro mas tautológico / má rotulagem |
| **Tabela 1 (coluna gap)** | **Errada** — reporta `tree_oneshot−opt`; as 2 funções “gap=1, opt=6” têm gap real 2 ou 3 | Coerente com (B), mas não é formula gap |
| **Cor. 6 (`s∈{0,1}`)** | **Falso** | **Falso** também |
| **Thm 7 (Two-Mechanism)** | **Cai** (usa `s≤1` e Unit Gap) | **Cai** (usa `s≤1`) |
| **Thm 4 (Tree: opt≤3 ⇒ gap=0)** | **Sobrevive** | Sobrevive |
| **Thm 3 (Threshold)** | **Sobrevive** (de facto prova algo mais forte) | Sobrevive como afirmado |

**Detalhe fatal em Cor. 6 / Thm 7 (independente da disputa tree vs oneshot):**

Circuito óptimo de ⊕₃ (6 portas): seja \(a=x\oplus y\) (3 portas), saída
\[
g_4=a\land\lnot z,\quad g_5=\lnot a\land z,\quad g_6=\lnot(\lnot g_4\land\lnot g_5).
\]
Na decomposição pela porta de saída: os dois sub-DAGs filhos partilham **as 3 portas de \(a\)**, logo \(s=|D_a\cap D_b|=3\). Pela identidade de inclusão-exclusão
\[
\mathrm{opt}(f)=1+\mathrm{opt}(a_{\mathrm{child}})+\mathrm{opt}(b_{\mathrm{child}})-s
\]
com \(\mathrm{opt}(a_{\mathrm{child}})=\mathrm{opt}(b_{\mathrm{child}})=4\): \(1+4+4-3=6\). Logo \(s=3\notin\{0,1\}\).

A “prova” de \(s\le 1\) em Cor. 6 é
\[
s=1+\mathrm{opt}(a)+\mathrm{opt}(b)-\mathrm{opt}(f)\le\mathrm{tree}(f)-\mathrm{opt}(f)\le 1,
\]
e o último “≤1” é exactamente o Thm 2 falso. Com o gap real ≥2, a cadeia só dá \(s\le\mathrm{gap}\in\{2,3\}\), o que é verdadeiro e saturado em \(s=3\).

**Thm 7** classifica “os únicos mecanismos que produzem unit gap” via \(s=1\) e polaridades — desmorona quando \(s>1\) é possível em circuitos óptimos.

**Thm 4** é análise exaustiva de topologias com ≤3 portas (“todo circuito óptimo com ≤3 portas é árvore”). Não depende da identidade falsa. Mantém-se; implica \(\mathrm{tree}_{\mathrm{formula}}=\mathrm{opt}\) sempre que \(\mathrm{opt}\le 3\).

**Thm 3:** a prova mostra, na verdade:
> se um circuito *óptimo* não é árvore (i.e. se \(\mathrm{gap}_{\mathrm{formula}}\ge 1\)), então \(\mathrm{opt}\ge n\).

Isso é correto (Lemma 1 + partição S/g/R) e **não** usa Thm 2. Sobrevive, e é até mais limpo sem o Unit Gap.

**Tabela 1:** a coluna `%gap=1` mede a fracção com `tree_oneshot=opt+1`, não o gap de fórmulas. Os números (10.5% em n=3, etc.) são artefactos da grandeza (B). A afirmação “no gap exceeds 1” é falsa para (A).

**§7 (interpretação tropical):** “the tropical operator overshoots by exactly 0 or 1, never more” — falso para o operador \(T\) que eles definem (ponto fixo = `tree_formula`). Em ⊕₃ overshoot ∈ {2,3}.

---

### 6. VEREDICTO

**Objeção SUSTENTADA.** O Teorema 2 é falso sob a definição padrão de formula size — que é a definição que o paper enuncia em português claro (“fan-out one at every gate — a tree”) e usa ao citar paridade Θ(n²).

O erro raiz é uma **substituição ilícita de `tree` por `opt` nos filhos** na identidade de §2, seguida de uma “prova” de upper bound que só fecha para essa grandeza espúria. Com isso:

- Thm 2, Cor. 6, Thm 7 e a coluna de gap da Tabela 1 caem;
- Thms 3 e 4 sobrevivem como factos estruturais sobre circuitos óptimos (quando podem deixar de ser árvores, e que opt≤3 ⇒ já é árvore);
- o contraexemplo ⊕₃ / ¬⊕₃ é sólido: `opt=6`, `tree_formula∈{8,9}`, `gap∈{2,3}>1`, com construção explícita de 9 portas e lower bound de Khrapchenko ≥8;
- a coincidência “2 funções gap=1 em opt=6 na Tabela 1 = exactamente as paridades” confirma que o autor computou `tree_oneshot`, não formula size.

A única saída para o autor é retratar a identidade de §2, redefinir explicitamente a grandeza estudada como “custo de decomposição de um nível com filhos óptimos” (não formula size), retirar a comparação com Θ(n²), e reprovar Cor. 6 / Thm 7 sem passar por `gap≤1` — porque \(s=3\) em ⊕₃ já os mata independentemente.
