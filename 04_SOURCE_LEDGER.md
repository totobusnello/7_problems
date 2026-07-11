# 04 — SOURCE LEDGER — Bibliografia verificada

> Prioridade de fontes: Clay (formulação oficial) → artigo original → peer-reviewed → versão do autor → arXiv → livro/survey reconhecido → docs de software → secundária identificada.
> Cada entrada registra: autores, título, ano, publicação, DOI/ID, teorema/seção/página usada, hipóteses, conclusão, data de consulta.
> **Proibido inventar:** artigos, autores, links, citações, números de teorema, páginas, resultados, consenso.

## Entradas

### SRC-0001 — Clay Mathematics Institute: Millennium Problems (página oficial)
- **URL:** https://www.claymath.org/millennium-problems/
- **Uso:** estado oficial dos sete problemas.
- **Conteúdo verificado:** 6 problemas unsolved; Poincaré solved (Perelman).
- **Data de consulta:** 2026-07-10 (HTTP 200, scrape direto).
- **Estado:** SOURCE_VERIFIED.

### SRC-0002 — Busnello, Flandoli, Romito (2003/2005)
- **Título:** "A probabilistic representation for the vorticity of a three-dimensional viscous fluid and for general systems of parabolic equations"
- **Autores:** Barbara Busnello; Franco Flandoli; Marco Romito.
- **arXiv:** math/0306075 — https://arxiv.org/abs/math/0306075
- **Publicação peer-reviewed:** Proceedings of the Edinburgh Mathematical Society, 48 (2005) 295–336 — **PENDENTE DE VERIFICAÇÃO DIRETA** (metadado a confirmar quando o PDF for processado).
- **Uso:** artigo-base da frente NS-PROB; representação probabilística da vorticidade 3D.
- **Data de consulta:** referenciado no briefing 2026-07-10; **PDF ainda não baixado/parseado nesta sessão**.
- **Estado:** SOURCE_VERIFIED (existência no arXiv) / conteúdo AGUARDANDO PROCESSAMENTO.

### SRC-0003 — Cook, "The P versus NP Problem" (descrição oficial do Clay)
- **Autor:** Stephen Cook. **Título:** The P versus NP Problem. **Publicação:** Clay Mathematics Institute, official problem description (12 pp.).
- **URL:** https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf (página do problema: https://www.claymath.org/millennium/p-vs-np/)
- **Uso:** formulação oficial, definições de P/NP/≤p/NP-completude (Defs. 1–4, Prop. 1), barreiras (relativization, natural proofs). Base de `PNP_AI/01_OFFICIAL_PROBLEM_SPEC.md` e claims 7P-PNP-CLM-0001..0007.
- **Método de verificação:** PDF baixado (176 KB, HTTP 200) e parseado localmente com pypdf; trechos-chave conferidos verbatim (não confiado a extração por LLM — uma extração automática errou um heading e omitiu o qualificador poly-time da Def. 3; corrigido contra o texto).
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED.

### SRC-0004 — Clay: Rules for the Millennium Prize Problems
- **URL:** https://www.claymath.org/millennium-problems/rules/ (regras adotadas pelo Board do CMI em 2018-09-26).
- **Uso:** critérios institucionais de solução: publicação em Qualifying Outlet + ≥2 anos + aceitação geral da comunidade; CMI não aceita submissões diretas.
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED.

### SRC-0005 — Cook (1971), "The Complexity of Theorem-Proving Procedures"
- **Autor:** Stephen A. Cook (University of Toronto). **Publicação:** Proc. 3rd ACM STOC, 1971. DOI ACM: 10.1145/800157.805047.
- **Cópias obtidas (2026-07-10):** scan da homepage do autor (cs.toronto.edu/~sacook) + redigitação pesquisável (unibz.it) — hashes em `_sources/README.md`.
- **Conferido no texto (cópia redigitada):** Summary ("any recognition problem solved by a polynomial time-bounded nondeterministic Turing machine..."), Theorem 1 (tautologyhood como alvo de redução; noção de "reduced" via oráculo = P-reducibility, análogo polinomial de Turing reducibility).
- **Ressalva:** redigitação ≠ original; para citação página-a-página usar o scan do autor. Reconstrução da prova: FASE 3.
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED.

### SRC-0006 — Karp (1972), "Reducibility Among Combinatorial Problems"
- **Autor:** Richard M. Karp. **Publicação:** Complexity of Computer Computations (Miller & Thatcher, eds.), Plenum Press, 1972, pp. 85–103.
- **Cópias obtidas (2026-07-10):** scan do original (uoa.gr) + reprint Springer 2010 com introdução retrospectiva de Karp (umd.edu) — hashes em `_sources/README.md`.
- **Conferido:** introdução de 2010 (texto pesquisável — influência de Edmonds, min-max como prenúncio de NP); corpo original extraído por **OCR/LLM (Firecrawl)**: definição L ∝ M via f ∈ Π, "Main Theorem: All the problems on the following list are complete", e 20 dos 21 problemas capturados (item 9 ilegível na extração; pela literatura padrão é DIRECTED HAMILTON CIRCUIT — **não conferido no scan**, marcado ⚠️).
- **Ressalva metodológica:** conteúdo do corpo veio de OCR sem conferência mecânica possível (scan) — tratar citações textuais de Karp como PENDENTES até OCR local ou cópia com texto.
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED (obtido; verbatim do corpo parcial).

### SRC-0007 — Levin (1973), "Universal'nye perebornye zadachi" (Universal Search Problems)
- **Autor:** Leonid A. Levin. **Publicação:** Problemy Peredachi Informatsii 9(3):265–266, 1973 (em russo).
- **Tradução inglesa:** contida integralmente em SRC-0008 (Trakhtenbrot 1984), seção "Brief Communications / Universal Search Problems" — conferida no PDF: Problems 1–6, Lemma 1 ("Problems 1–6 are universal search problems"), noção de problema "universal".
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED (via tradução em SRC-0008; original russo não obtido).

### SRC-0008 — Trakhtenbrot (1984), "A Survey of Russian Approaches to Perebor (Brute-Force Search) Algorithms"
- **Publicação:** Annals of the History of Computing 6(4):384–400, 1984. IEEE DOI: 4640789.
- **Cópia obtida (2026-07-10):** PDF com texto (drdoane.com) — hash em `_sources/README.md`.
- **Conferido no texto:** história do perebor desde os anos 1950; "in 1971, Levin obtained similar results" (anterioridade de Levin à publicação de 1973); conferência de Tsakhkadzor (março/1973) com audiência ignorando Cook/Karp; terminologia "universal perebor problems"; apêndice com a tradução do artigo de Levin.
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED.

### SRC-0009 — Hartmanis & Stearns (1965), "On the Computational Complexity of Algorithms"
- **Publicação:** Transactions of the AMS, vol. 117 (1965), pp. 285–306. PDF oficial livre da AMS.
- **URL:** https://www.ams.org/journals/tran/1965-117-00/S0002-9947-1965-0170805-7/S0002-9947-1965-0170805-7.pdf
- **Conferido (parse server-side, 2026-07-10):** título/autores; Corollary 1.2 (cadeias infinitas de classes de complexidade distintas); modelo = TM multifita. Download local falhou 2× (PDFs truncados) — cópia local pendente; conteúdo verificado remotamente.
- **Uso:** origem da hierarquia de tempo (§6 de `PNP_AI/05_COMPLEXITY_FOUNDATIONS.md`).
- **Estado:** SOURCE_VERIFIED (verificação remota; arquivo local A OBTER).

### SRC-0010 — Arora & Barak (2007, draft), "Computational Complexity: A Modern Approach"
- **Natureza:** draft oficial do livro (Princeton), 489 pp., distribuído publicamente pelos autores. Nível 6 da hierarquia de fontes (livro reconhecido) — usado para enunciados modernos quando a primária está inacessível.
- **URL:** https://theory.cs.princeton.edu/complexity/book.pdf · PDF local em `_sources/` com SHA-256.
- **Conferido verbatim (pypdf, 2026-07-10):** Theorem 3.1 (time hierarchy), Theorem 3.3 (NTIME hierarchy), Theorem 3.4 (Ladner, com prova por padding), Definition 5.1 (Σᵖ₂), Definition 5.4 (PH), Theorem 6.13 (Karp–Lipton c/ Sipser), Theorem 6.14 (Meyer, EXP).
- **Erratum detectado:** Remark 5.5 do draft afirma "Πᵖ₂ = coNP" (typo; o correto pela própria Def. 5.4 é Πᵖ₁ = coNP). Registrado; não propagado.
- **Estado:** SOURCE_VERIFIED (com ressalva: draft, não a edição final publicada).

### SRC-0011 — Ladner (1975), "On the Structure of Polynomial Time Reducibility"
- **Publicação:** Journal of the ACM 22(1):155–171. DOI: 10.1145/321864.321877.
- **Tentativa 2026-07-10:** download da ACM DL bloqueado (bot detection); nenhum mirror .edu com o paper completo localizado na primeira busca.
- **Uso:** primária do Teorema de Ladner (enunciado já verificado via SRC-0010, Thm 3.4).
- **Estado:** A OBTER (citação confirmada por múltiplas fontes independentes; paper pendente).

### SRC-0012 — Stockmeyer (1976), "The Polynomial-Time Hierarchy"
- **Publicação:** Theoretical Computer Science 3(1):1–22. Elsevier (paywall).
- **Uso:** primária da definição da PH (definição já verificada via SRC-0010, Defs 5.1/5.4).
- **Estado:** A OBTER (paywall; avaliar acesso institucional com Luiz se necessário).

### SRC-0013 — Karp & Lipton (1982), "Turing Machines That Take Advice"
- **Publicação:** L'Enseignement Mathématique 28(2):191–209 (versão de periódico do resultado de STOC 1980).
- **Secundária claramente identificada:** notas de aula CS860 (R. Oliveira, U. Waterloo, 2022) — PDF local `karplipton-waterloo-lecture6-secondary.pdf` em `_sources/`.
- **Uso:** primária do teorema de Karp–Lipton (enunciado já verificado via SRC-0010, Thm 6.13).
- **Estado:** A OBTER (primária); secundárias verificadas.

### SRC-0014 — Baker, Gill & Solovay (1975), "Relativizations of the P =? NP Question"
- **Publicação:** SIAM Journal on Computing 4(4):431–442, 1975. Paywall SIAM.
- **Uso:** primária da Barreira 1 (relativization). Conteúdo central verificado via SRC-0017 (survey de Fortnow): os DOIS oráculos (P^A = NP^A e P^B ≠ NP^B) e a observação de que as técnicas da época relativizam.
- **Estado:** A OBTER (primária); conteúdo verificado via survey.

### SRC-0015 — Razborov & Rudich (1997), "Natural Proofs"
- **Publicação:** Journal of Computer and System Sciences 55(1):24–35, 1997 (versão de journal; cabeçalho JCSS conferido no PDF). PDF local em `_sources/` com SHA-256 (mirror do curso MIT 6.875).
- **Conferido verbatim (pypdf, 2026-07-10):** definições de Constructivity (decidir fₙ ∈ Cₙ em P na truth table), Largeness (|Cₙ| ≥ 2^(−O(n))·|Fₙ|), Usefulness (circuit size superpolinomial); Theorem 4.1 (inexistência de prova P/poly-natural contra P/poly sob PRGs fortes); exemplo do logaritmo discreto.
- **Estado:** SOURCE_VERIFIED.

### SRC-0016 — Aaronson & Wigderson, "Algebrization: A New Barrier in Complexity Theory"
- **Publicação:** STOC 2008; versão de journal ACM TOCT 1(1), 2009. Cópia do autor (scottaaronson.com), 50 pp. PDF local em `_sources/` com SHA-256.
- **Conferido verbatim (pypdf, 2026-07-10):** abstract (terceira barreira; extensão de baixo grau Ã sobre corpo/anel finito; lower bounds que superam as duas primeiras barreiras simultaneamente); definição assimétrica de "algebrizes" para separações (C^Ã ⊄ D^A ∀A,Ã); conclusão de que P vs NP exige técnicas não-relativizantes e não-algebrizantes.
- **Estado:** SOURCE_VERIFIED.

### SRC-0017 — Fortnow, "The Role of Relativization in Complexity Theory"
- **Natureza:** survey (Bulletin of the EATCS / página do autor), 15 pp. PDF local em `_sources/` com SHA-256. Fonte nível 6 (survey reconhecido de autoridade da área).
- **Conferido no texto (2026-07-10):** BGS deram mundo relativizado com P = NP E outro com P ≠ NP; "essentially all the known complexity techniques at that time relativize"; resultados de provas interativas como exceção não-relativizante.
- **Uso:** ponte verificada para SRC-0014 enquanto a primária não é obtida.
- **Estado:** SOURCE_VERIFIED.

### SRC-0018 — Kulikov, Pechenev & Slezkin, "SAT-based Circuit Local Improvement" (arXiv:2102.12579, 2021/22)
- **Conferido (abstract via busca semântica + inspect, 2026-07-10):** fronteira prática de exact synthesis — tamanho 7 é instantâneo, tamanho 13 leva 1+ semana; espaço de busca s^Θ(s); local improvement provou novos upper bounds p/ funções simétricas.
- **Uso:** calibração do que é viável em C1. **Estado:** SOURCE_VERIFIED (abstract; corpo A PROCESSAR se C1 for selecionado).

### SRC-0019 — Krinkin, "A Simple Constructive Bound on Circuit Size Change Under Truth Table Perturbation" (arXiv:2603.09379, mar/2026)
- **Conferido (corpo lido via full-text search, 2026-07-10):** |opt(f)−opt(f′)| ≤ c_B·n·d_H (prova construtiva por detector+correção); verificação exaustiva em n=4/AIG; **220/222 classes NPN-4 com valores exatos SAT-verified (136 por enumeração, 84 por exact synthesis com cube-and-conquer); 2 CLASSES RESTANTES só com upper bound (timeout em k=9, SAT em k=10)**; dados e scripts em github.com/krinkin/bounds (tag v1.0); questões abertas explícitas (gap constante p/ d_H=1? famílias Ω(n)?).
- **Ressalva:** preprint (não peer-reviewed); dados do repo A VERIFICAR antes de uso.
- **Uso:** alvo candidato da 1ª unidade de trabalho de C1. **Estado:** SOURCE_VERIFIED (preprint).

### SRC-0020 — Kojevnikov, Kulikov & Yaroslavtsev, "Finding efficient circuits using SAT-solvers" (SAT 2009, LNCS 5584)
- **Uso:** método fundacional de SAT-based exact synthesis (citado por SRC-0019 como a técnica dos 84 valores). **Estado:** REFERENCIADO via SRC-0019; A OBTER se C1 selecionado.

### SRC-0021 — Heule, Kullmann, Wieringa & Biere, "Cube and conquer" (HVC 2011, LNCS 7261)
- **Uso:** estratégia de paralelização SAT usada nos valores exatos de SRC-0019; candidata para atacar as 2 classes pendentes. **Estado:** REFERENCIADO via SRC-0019; A OBTER se C1 selecionado.

### SRC-0022 — "Towards the shortest DRAT proof of the Pigeonhole Principle" (arXiv:2207.11284)
- **Uso:** estado da arte do nicho experimental de C2 (proof complexity com certificados DRAT); mostra que o nicho é ativo e competitivo. **Estado:** REFERENCIADO (abstract); A OBTER se C2 selecionado.

### SRC-0023 — Testa et al., "Determining the Multiplicative Complexity of Boolean Functions using SAT" (arXiv:2005.01778)
- **Uso:** variante de C1 (complexidade multiplicativa, motivação criptográfica); linha ativa até 2026 (cf. arXiv:2601.08368, implementações AND/XOR dim ≤9). **Estado:** REFERENCIADO (abstract).

### SRC-0024 — Gäher & Kunze, "Mechanising Complexity Theory: The Cook-Levin Theorem in Coq"
- **Conferido (metadados Semantic Scholar, 2026-07-10):** Cook–Levin mecanizado em **Coq** — anunciado como o primeiro resultado de complexidade computacional mecanizado (com custo de computação incluído). **Impacto em C4:** formalizar Cook–Levin NÃO é novidade; um port a Lean tem valor apenas parcial. **Estado:** REFERENCIADO; A OBTER se C4 avançar.

### SRC-0025 — Mathlib4 issue #35366: "Step counting and complexity classes P/NP for TM1"
- **Conferido (busca, 2026-07-10):** contribuidor declara ter formalização funcional de P e NP sobre a infra de Turing do Mathlib, em processo de upstream. **Impacto em C4:** o espaço "definir P/NP em Lean/Mathlib" está sendo ocupado AGORA por terceiros — duplicação alta; a rota de valor seria CONTRIBUIR ao esforço existente (interação externa ⟹ exige autorização de Luiz). **Estado:** REFERENCIADO; monitorar.

### SRC-0026 — MCSP: estado da arte (via arXiv:2511.16903, nov/2025 + varredura)
- **Conferido (abstracts, 2026-07-10):** MCSP* (funções parciais) é ETH-hard (Ilango 2020); estender a redução para MCSP TOTAL permanece ABERTO com obstáculos identificados (read-once formulas); SoS lower bounds p/ MCSP (2023); MCSP↔Graph Isomorphism (Allender et al.); linha quântica. **Impacto em C3:** teoria profunda e ativa, dependência alta de especialistas; a face EXPERIMENTAL de C3 (dados exatos em pequena escala) é exatamente C1. **Estado:** REFERENCIADO.

### SRC-0027 — Repo krinkin/bounds (dados do SRC-0019)
- **Conferido (scrape do GitHub, 2026-07-10):** README confirma "**220 exact, 2 upper bounds**"; último commit 2026-03-10 (revisão de README); nenhum sinal de fechamento das 2 classes. Dados em `data/npn4_opt_aig.csv` + `scripts/verify_all.py` (Python stdlib). **GAP CONFIRMADO VIVO** (na data da consulta). **Estado:** SOURCE_VERIFIED (estado do repo); classes específicas a identificar no CSV quando o trabalho iniciar.

### SRC-0028 — Heule, "Schur Number Five" (AAAI 2018, arXiv:1711.08076)
- **Uso:** marco da linha "combinatória extremal / problemas centenários via SAT com certificados massivos" (prova ~2PB, verificada por checker formalmente verificado) — fonte-âncora do candidato C6 (fora da shortlist), documentado no fechamento da FASE 5. **Consulta:** 2026-07-11 (abstract arXiv + página do autor confirmados por busca). **Estado:** REFERENCIADO (abstract).

### SRC-0029 — MathCheck (Waterloo) — SAT+CAS para conjecturas matemáticas (uwaterloo.ca/mathcheck; paper IJCAI 2025)
- **Uso:** segunda fonte-âncora do candidato C6: pipeline SAT+Computer Algebra com DRAT logging para conjecturas em combinatória/teoria dos números. Mostra que o nicho fora da shortlist é ativo e DOMINADO por grupos estabelecidos (CMU/Waterloo). **Consulta:** 2026-07-11 (PDF IJCAI 2025 localizado por busca). **Estado:** REFERENCIADO (abstract/página).

## Template de entrada

```
### SRC-NNNN — [autores curtos, ano]
- Título / Autores / Ano / Publicação / DOI ou ID
- Teorema, seção ou página usada
- Hipóteses / Conclusão
- Data de consulta / Estado
```
