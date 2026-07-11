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

## Pendentes de entrada (à medida que as fases avançarem)

NTM (máquina não determinística) · co-NP · P/poly · advice · hierarquia polinomial · algebrization · proof complexity · PRG/hardness-vs-randomness · MCSP/meta-complexidade · GCT.
