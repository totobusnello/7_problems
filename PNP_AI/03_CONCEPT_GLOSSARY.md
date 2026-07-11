# PNP-AI — 03 — GLOSSÁRIO PROGRESSIVO

> Formato: **termo** — informal (1 linha) · técnica (precisa) · fonte. Crescerá a cada fase; entradas nunca são removidas, só refinadas com registro.
> Iniciado na FASE 2 (2026-07-10). Fontes: SRC-0003 salvo indicação.

| Termo | Informal | Definição técnica | Fonte |
|---|---|---|---|
| **Linguagem** | Conjunto das entradas "SIM" de um problema de decisão | L ⊆ Σ*, Σ alfabeto finito (\|Σ\| ≥ 2) | SRC-0003 §1 |
| **Máquina de Turing (TM)** | Modelo matemático de computador | Definida no apêndice do doc oficial; modelo padrão da computabilidade (Turing 1936) | SRC-0003 App. |
| **T_M(n)** | Custo de pior caso da máquina M | Máximo de passos de M sobre entradas de comprimento n | SRC-0003 §1 |
| **Tempo polinomial** | "Eficiente" no sentido técnico | ∃k: T_M(n) ≤ n^k + k para todo n | SRC-0003 §1 |
| **P** | Problemas resolvíveis rápido | {L : L = L(M) para TM M de tempo polinomial} | SRC-0003 §1 |
| **Checking relation** | Regra que confere um par (instância, palpite) | R ⊆ Σ* × Σ₁*; R é poly-time sse L_R = {w#y : R(w,y)} ∈ P | SRC-0003 §1 |
| **NP** | Problemas com solução conferível rápido | L ∈ NP ⟺ ∃k, R poly-time: w ∈ L ⟺ ∃y(\|y\| ≤ \|w\|^k ∧ R(w,y)) | SRC-0003 §1 |
| **Certificado / witness** | O "gabarito" que convence o verificador | O y da definição de NP; comprimento polinomial | SRC-0003 §1 |
| **Verificador** | Quem confere o gabarito | Algoritmo polinomial que decide L_R | SRC-0003 §1 |
| **≤m (many-one)** | Tradução computável entre problemas | L₁ ≤m L₂ ⟺ ∃f computável total: x ∈ L₁ ⟺ f(x) ∈ L₂ (Def. 1) | SRC-0003 §2 |
| **≤p (p-redução)** | Tradução EFICIENTE entre problemas | Como ≤m, com f computável em tempo polinomial (Def. 3) | SRC-0003 §2 |
| **NP-completo** | Problema universal de NP | L ∈ NP e L' ≤p L ∀L' ∈ NP (Def. 4) | SRC-0003 §2 |
| **SAT / Satisfiability** | "Esta fórmula booleana tem como ser verdadeira?" | Dada fórmula proposicional F, decidir se ∃ atribuição que satisfaz F; NP-completo (Cook 1971) | SRC-0003, SRC-0005 |
| **3-SAT** | SAT com cláusulas de ≤3 literais | NP-completo (Cook 1971; item 11 da lista de Karp como "SATISFIABILITY WITH AT MOST 3 LITERALS PER CLAUSE") | SRC-0005, SRC-0006 |
| **Teorema de Cook–Levin** | SAT é o problema universal | SAT é NP-completo; provado por Cook (1971) e independentemente por Levin (1971/73) | SRC-0005, SRC-0007 |
| **Perebor** | Termo soviético p/ busca exaustiva | "Brute-force search"; linha de pesquisa soviética desde os anos 1950; "universal perebor problems" ≈ NP-completos | SRC-0008 |
| **Circuito booleano** | "Hardware" que computa f: {0,1}ⁿ → {0,1} | DAG de portas AND/OR/NOT; tamanho = nº de portas | SRC-0003 §3 |
| **Família de circuitos** | Um circuito por tamanho de entrada | {Cₙ}; modelo NÃO uniforme de computação | SRC-0003 §3 |
| **Uniformidade** | Um único algoritmo p/ todos os tamanhos | Exigência da definição de P; famílias de circuitos arbitrárias a violam | SRC-0003 |
| **Circuit lower bound** | Prova de que hardware pequeno não basta | Cota inferior no tamanho de circuito p/ uma função; superpolinomial p/ problema NP-completo ⟹ P ≠ NP; recorde geral registrado no doc: ~4n | SRC-0003 §3 |
| **Relativization** | Teste do oráculo | Técnica relativiza se sobrevive a oráculos; ∃A: P^A = NP^A ⟹ diagonalização+redução não separa P/NP | SRC-0003 §3 |
| **Natural proofs** | O muro das provas "naturais" | Razborov–Rudich: métodos naturais de lower bound quebrariam PRGs fortes (e melhorariam fatoração) | SRC-0003 §3 |
| **Pior caso vs caso médio** | "Sempre" vs "quase sempre" | P/NP são classes de pior caso; desempenho médio ou empírico não transfere | SRC-0003 + charter |
| **Instância adversarial** | Entrada construída p/ quebrar um algoritmo | Ferramenta central do papel REVISOR COMPUTACIONAL | charter |
| **Qualifying Outlet** | Onde uma solução precisa sair | Requisito das regras Clay 2018 (+2 anos + aceitação geral) | SRC-0004 |

## Entradas da FASE 3 (2026-07-10)

| Termo | Informal | Definição técnica | Fonte |
|---|---|---|---|
| **NTM** | Máquina que "adivinha" — ∃ disfarçado de hardware | TM com relação de transição (múltiplos sucessores); aceita w sse ∃ ramo aceitante | SRC-0005 + `05_COMPLEXITY_FOUNDATIONS.md` §1 |
| **co-NP** | Problemas com gabarito curto para o NÃO | {L : complemento de L ∈ NP}; canônico: TAUTOLOGY | `05` §3 |
| **NP ∩ co-NP** | Certificado dos dois lados — zona "suspeita de P" | Ex.: PRIMES (pré-AKS), FACTORING (decisão) | `05` §3 |
| **DTIME(f) / NTIME(f)** | Orçamento de tempo determinístico / não determinístico | Classes de linguagens decidíveis/aceitáveis em O(f(n)) passos | SRC-0010 cap. 3 |
| **Time-constructible** | f "computável dentro do próprio orçamento" | ∃ TM que computa f(n) em O(f(n)) — hipótese técnica das hierarquias | SRC-0010 |
| **Hierarquia de tempo** | Mais tempo = mais poder (provado!) | f log f = o(g) ⟹ DTIME(f) ⊊ DTIME(g); corolário: P ⊊ EXP | SRC-0009/0010 (Thm 3.1) |
| **Padding** | Inflar a entrada pra diluir a dificuldade | Técnica de Ladner: SAT_H = SAT + 1^(n^H(n)) | SRC-0010 (Thm 3.4) |
| **NP-intermediate** | Nem fácil, nem universal | L ∈ NP∖P não NP-completo; existe se P≠NP (Ladner); candidatos: graph isomorphism, factoring | SRC-0010/0011 |
| **P/poly** | Algoritmo + "cola" por tamanho de entrada | Linguagens decididas por famílias de circuitos de tamanho polinomial ≡ TM com advice polinomial | SRC-0010 cap. 6 |
| **Advice** | A cola: string que só depende de \|x\| | αₙ fornecida de graça à máquina para entradas de tamanho n | SRC-0013 (título!) |
| **Σᵖᵢ / Πᵖᵢ / PH** | Andares de quantificadores sobre P | i quantificadores alternados (∃… / ∀…) sobre verificador polinomial; PH = ∪Σᵖᵢ; Σᵖ₁=NP, Πᵖ₁=coNP | SRC-0010 (Defs 5.1/5.4) |
| **Colapso da PH** | Os andares desabam | Σᵖᵢ = Σᵖᵢ₊₁ ⟹ PH = Σᵖᵢ; P=NP ⟹ PH=P; "PH não colapsa" = conjectura-moeda da área | SRC-0010 §5.2 |
| **Karp–Lipton** | Circuitos pequenos p/ NP custam caro | NP ⊆ P/poly ⟹ PH = Σᵖ₂ | SRC-0010 (Thm 6.13) |

## Entradas da FASE 4 (2026-07-10)

| Termo | Informal | Definição técnica | Fonte |
|---|---|---|---|
| **Relativizar** | Sobreviver a oráculos | Prova válida quando todas as máquinas recebem o mesmo oráculo arbitrário; BGS: ∃A, B com P^A = NP^A e P^B ≠ NP^B | SRC-0017 (primária SRC-0014) |
| **Propriedade natural** | Teste amplo e eficiente de "esta função é difícil" | Constructivity (decidível em P na truth table) + Largeness (≥ 2^(−O(n)) das funções) | SRC-0015 (verbatim) |
| **Useful (contra P/poly)** | A propriedade de fato mata circuitos pequenos | Toda sequência fₙ ∈ Cₙ tem circuit size superpolinomial | SRC-0015 (verbatim) |
| **PRG (pseudorandom generator)** | Esticador de aleatoriedade que engana circuitos | G: {0,1}^k → {0,1}^2k em P/poly cuja saída circuitos pequenos não distinguem de aleatória; dureza H(G_k) | SRC-0015 |
| **Aritmetização** | Fórmulas booleanas viram polinômios | Extensão de predicados booleanos a corpos finitos; motor de IP = PSPACE; NÃO relativiza, mas ALGEBRIZA | SRC-0016/0017 |
| **Algebrizar** | Sobreviver a oráculos algébricos | Separação C ⊄ D algebriza se C^Ã ⊄ D^A ∀A e toda extensão de baixo grau Ã (assimetria essencial) | SRC-0016 (verbatim) |

## Pendentes de entrada (à medida que as fases avançarem)

proof complexity · MCSP/meta-complexidade · GCT · hardness magnification · PSPACE/Savitch · ETH/SETH · IP = PSPACE (detalhe).
