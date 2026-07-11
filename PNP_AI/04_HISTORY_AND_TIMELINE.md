# PNP-AI — 04 — HISTÓRIA E LINHA DO TEMPO

> Marcação: ✅ = verificado em fonte primária deste projeto (source ledger) · ⚠️ = RESULTADO CONHECIDO da literatura, fonte primária ainda não processada (datas/detalhes a confirmar nas FASES 3–4).
> Iniciado na FASE 2 (2026-07-10).

## Linha do tempo

| Ano | Evento | Status |
|---|---|---|
| 1936 | Turing define a máquina de Turing e prova a indecidibilidade do Halting Problem — nasce a teoria da computabilidade, com ≤m e problemas completos (c.e.-completude) como moldes do que viria | ✅ SRC-0003 (§2 e App.) |
| 1953 | von Neumann discute antecedentes de complexidade computacional | ✅ citado em SRC-0003 ("earlier von Neumann [38], in 1953") |
| anos 1950 | Escola soviética inicia o estudo do *perebor* (busca exaustiva) — Yablonskii e outros | ✅ SRC-0008 |
| 1965 | **Hartmanis–Stearns, "On the computational complexity of algorithms"** (Trans. AMS): batiza o campo; hierarquia de classes de complexidade por diagonalização (Corollary 1.2), TM multifita | ✅ SRC-0009 (verificado no PDF oficial da AMS) |
| anos 1960 | Cobham e Edmonds propõem tempo polinomial como critério de viabilidade (*feasibility*); Edmonds destaca verificação rápida via teoremas min-max (prenúncio de NP, segundo o próprio Karp) | ✅ SRC-0003 (§1) + SRC-0006 (introdução de Karp, reprint 2010) |
| 1971 | **Cook, "The complexity of theorem-proving procedures" (STOC):** tautologias/SAT como problema universal via P-reducibility (análogo polinomial de redução de Turing); nasce a NP-completude | ✅ SRC-0005 (PDF obtido, Theorem 1 conferido no texto) |
| 1971 | **Levin obtém resultados análogos na URSS** (publicação só em 1973) | ✅ SRC-0008 ("in 1971, Levin obtained similar results") |
| 1972 | **Karp, "Reducibility among combinatorial problems":** 21 problemas NP-completos; introduz a notação P e NP e a NP-completude via ≤p (many-one polinomial), que vira padrão | ✅ SRC-0003 §2 + SRC-0006 (OCR: Main Theorem + 20/21 itens capturados; item 9 ilegível no scan — pela literatura é DIRECTED HAMILTON CIRCUIT ⚠️) |
| 1973 | **Levin, "Universal'nye perebornye zadachi"** (Probl. Pered. Inform. 9(3):265–266): 6 problemas universais de busca; tradução inglesa no survey de Trakhtenbrot | ✅ SRC-0007/SRC-0008 (tradução integral no PDF obtido: Problems 1–6, Lemma 1) |
| 1973 | Conferência de Tsakhkadzor (70 anos de Kolmogorov): audiência soviética ainda desconhecia Cook e Karp — as duas tradições corriam em paralelo | ✅ SRC-0008 |
| 1975 | **Ladner:** se P ≠ NP, existem problemas NP-intermediários (nem em P, nem NP-completos) — prova por padding | ✅ enunciado verificado (SRC-0010, Thm 3.4); primária JACM = SRC-0011 A OBTER |
| 1975 | Baker–Gill–Solovay: **relativization** — ∃ oráculo A com P^A = NP^A; diagonalização pura não resolve | ✅ fato citado em SRC-0003 (ref. [3]); ⚠️ ano e paper a processar na FASE 4 |
| 1976 | **Stockmeyer** formaliza a **hierarquia polinomial** (conceito de Meyer–Stockmeyer 1972) | ✅ definição verificada (SRC-0010, Defs 5.1/5.4); primária TCS = SRC-0012 A OBTER (paywall) |
| 1980/82 | **Karp–Lipton:** NP ⊆ P/poly ⟹ PH colapsa a Σᵖ₂ — circuitos pequenos para NP custariam caro demais | ✅ enunciado verificado (SRC-0010, Thm 6.13); primária = SRC-0013 A OBTER |
| anos 1980 | Lower bounds para circuitos restritos (AC⁰: Furst–Saxe–Sipser, Ajtai; monótonos: Razborov) — otimismo com a via de circuitos | ⚠️ literatura padrão; fontes primárias na FASE 4 |
| 1994–97 | Razborov–Rudich: **natural proofs** — os métodos conhecidos de circuit lower bounds não podem separar P de NP se PRGs fortes existem | ✅ fato citado em SRC-0003 (ref. [27]); ⚠️ ano/paper a processar na FASE 4 |
| 2000 | Clay Mathematics Institute inclui P vs NP entre os sete Millennium Prize Problems (descrição oficial por Cook) | ✅ SRC-0001, SRC-0003 |
| 2002 | AKS: PRIMES ∈ P — exemplo de problema que passou de "só verificável" a "resolvível" | ✅ fato citado em SRC-0003 (composites em P, ref. [1]); ⚠️ paper na FASE 3 |
| 2008 | Aaronson–Wigderson: **algebrization** — terceira barreira | ⚠️ fora do doc de Cook; fonte primária na FASE 4 |
| 2000s–hoje | SAT solvers industriais (CDCL) resolvem instâncias enormes na prática — sem impacto no pior caso; meta-complexidade (MCSP), hardness magnification e GCT como fronteiras ativas | ⚠️ mapear na FASE 4 (`08_RESEARCH_FRONTIERS.md`) |

## Leituras da história para o programa

1. **Duas tradições independentes chegaram ao mesmo conceito** (EUA: Cook/Karp; URSS: Levin/perebor) — sinal de que NP-completude é uma estrutura natural, não um artefato de formalismo.
2. **O padrão histórico é de barreiras provadas**, não de estagnação: cada geração de técnicas (diagonalização → circuitos → provas naturais → algebrização) foi *demonstrada* insuficiente. Qualquer proposta nova deve declarar de saída como escapa das três barreiras.
3. **Problemas migram de NP para P** (PRIMES/AKS) — a fronteira não é estática; problemas intermediários (graph isomorphism, citado no doc oficial como não sabido em P nem NP-completo) são laboratórios naturais.
4. Para o 7_PROBLEMS: a história valida a estratégia de **resultados intermediários** — Karp virou marco sem resolver P vs NP; mapas de redução e barreiras são contribuições reais.
