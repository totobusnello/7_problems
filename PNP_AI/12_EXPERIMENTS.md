# PNP-AI — 12 — EXPERIMENTS

> Todo experimento registra: código, versão, parâmetros, hardware (quando relevante), entradas, saídas, seeds, tempo, memória, limite do experimento, conclusão permitida e conclusão NÃO permitida.

---

## EXP-PED-0001 — Redução 3-COLORING → SAT (pedagógico)

- **Data:** 2026-07-10 · **Fase:** 2 (pedagógica) · **Código:** `experiments/exp_ped_0001_3col_to_sat.py`
- **Ambiente:** Python 3.14.3, python-sat (Glucose4), macOS darwin 25.6.0. Determinístico (sem seeds).
- **Codificação:** x[v,c] = "vértice v tem cor c"; cláusulas: ≥1 cor por vértice, ≤1 cor por vértice, vizinhos com cores distintas. Tamanho exato: 4n+3|E| cláusulas e 9n+6|E| literais (grupo 1: n×3; grupo 2: 3n×2; grupo 3: 3|E|×2) [contagem de literais explicitada após REV-0002]; construção O(n+|E|) em word-RAM com lista de arestas, O((n+|E|)·log n) em bits — em qualquer caso polinomial (complexidade corrigida pela REV-0001; ver claim 7P-PNP-CLM-0010).
- **Hardening pós-REV-0002 (Kimi):** verificação independente agora exige EXATAMENTE UMA cor por vértice (rejeita 0 ou ≥2, sem confiar no solver) + validação de arestas na entrada (range e laços). Re-executado: mesmos resultados (C5/Petersen SAT, K4 UNSAT); testes negativos da validação passam.
- **Hardening pós-REV-0006 (GLM, 2026-07-11):** rejeição de multiarestas — incl. (u,v)/(v,u) — enforçando a hipótese de grafo simples; caso n=0 (conjunção vazia ⟹ SAT, certificado {}) incluído na bateria. Re-executado: mesmos resultados; testes negativos das multiarestas passam.
- **Entradas e saídas (execução real):**

| Instância | \|V\| | \|E\| | Cláusulas | Resultado |
|---|---|---|---|---|
| C5 (ciclo de 5) | 5 | 5 | 35 | SAT — certificado {0:2, 1:1, 2:0, 3:1, 4:0}, conferido independentemente |
| Petersen | 10 | 15 | 85 | SAT — certificado conferido independentemente |
| K4 (completo) | 4 | 6 | 34 | UNSAT (K4 não é 3-colorável) |

- **Limite do experimento:** 3 instâncias minúsculas; propósito exclusivamente didático.
- **Conclusão permitida:** a redução implementada preserva SIM/NÃO nas instâncias testadas; ilustra concretamente redução polinomial, certificado e a assimetria encontrar/conferir.
- **Conclusão NÃO permitida:** qualquer afirmação sobre P vs NP, sobre desempenho assintótico de solvers, ou sobre correção da redução para todos os grafos (a prova geral da correção da codificação é exercício da FASE 3 — candidata a primeiro lema formalizável).

---

## EXP-GATE-0001 — Gate de qualificação da FASE 5 (pré-registrado na proposta v5) — **PASSOU**

- **Data:** 2026-07-11 · **Código:** `experiments/exp_gate_0001/` (`aig_exact.py` encoder, `enumerate_aig.py` enumerador independente, `run_gate.py` orquestração) · **Dados:** `npn4_opt_aig.csv` (SRC-0027, catálogo Krinkin).
- **Ambiente:** Python 3.14.3 + pysat/Glucose4 (G1/G3), kissat 4.x via brew (G2), drat-trim compilado do fonte (checker independente). Determinístico. Budget pré-registrado: 4h/instância.
- **Resultados (execução real):**

| Critério | Resultado | Tempo |
|---|---|---|
| **G3** validação semântica | n=2: 16/16 funções encoder==enumeração (max opt 3) · n=3: 126 funções opt≤3 conferidas + 130 inalcançáveis confirmadas UNSAT k=1..3 (duas direções) | 0,2s |
| **G1** SAT em k=opt | Classe 0x0016 (opt catálogo 7): circuito de 7 portas encontrado e **verificado por simulação** contra a truth table completa | 0,1s |
| **G2** UNSAT em k=opt−1 | k=6: kissat UNSAT; prova DRAT de 3,6MB **verificada por drat-trim ("s VERIFIED")** | 0,9s + 0,7s check |

- **BUG REAL PEGO PELA VALIDAÇÃO SEMÂNTICA (1ª execução):** o encoder colidia constantes 0/1 com literais DIMACS ±1 (variável 1) — o circuito decodificado não batia com a truth table e o assert de simulação REPROVOU. Corrigido com tipos separados ('const'/'lit') e re-executado. **Confirmação empírica do finding central da REV-0004:** DRAT não teria pego isso; a verificação semântica pegou.
- **Conclusão permitida:** o pipeline exact-synthesis (encoder→solver→certificado→checker independente→validação semântica) funciona de ponta a ponta no hardware local; opt_AIG(0x0016)=7 foi reproduzido independentemente com certificados nas duas direções; FER real de C1 = 5 confirmado NESTA escala (k≤7).
- **Conclusão NÃO permitida:** nada sobre as 2 classes pendentes (k=9 é outra escala de dificuldade — o catálogo registra timeout do autor); nada assintótico; nada sobre n=5.
- **Artefatos grandes (CNF/DRAT) não versionados** — regeneráveis por `run_gate.py` (determinístico).

---

## EXP-PROBE-0001 — Sonda k=9 nas classes pendentes 0x1669 / 0x166b — **CONCLUÍDO** (status atualizado 2026-07-11, pós-REV-0005)

- **Data:** 2026-07-11 · **Código:** `experiments/exp_probe_0001/` · **Budget aprovado:** 12h/classe.
- **Encoder:** o do EXP-GATE-0001 + quebra de simetria v2 (portas duplicadas proibidas — sound para opt ∈ {9,10}: circuito mínimo não tem duplicatas; gate re-validado integralmente após a mudança). CNF k=9: 1.273 vars, 133.909 cláusulas.
- **Tentativa v1 (ABORTADA — lição de engenharia):** rodada COM proof logging; DRATs ultrapassaram 4,2GB+3,8GB em ~25min (projeção >100GB/12h); processos mortos por pressão de sistema. Lição: **veredito primeiro (sem prova), certificado em execução separada e dimensionada**.
- **v2, resultados:**

| Classe | Veredito k=9 | Tempo | Estado |
|---|---|---|---|
| **0x166b** (tt=5739) | **UNSAT — não existe circuito AIG de 9 portas** ⟹ com ub=10: **opt_AIG = 10** | **1.269s (21min)** — vs timeout do autor do catálogo | COMPUTATIONALLY_TESTED; certificação DRAT + busca do circuito de 10 portas EM EXECUÇÃO |
| **0x1669** (tt=5737) | **UNSAT — não existe circuito AIG de 9 portas** ⟹ com ub=10: **opt_AIG = 10** | **1.543s (26min)** | COMPUTATIONALLY_TESTED; certificação DRAT + busca do circuito de 10 portas EM EXECUÇÃO |

**Com isso, as 222 classes NPN de n=4 têm valor exato decidido na base AIG** (220 do catálogo + 2 deste experimento).

### Certificação final (2026-07-11) — AMBAS VERIFICADAS, EM DUPLICATA

| Classe | Prova DRAT | Verificação Mac | Verificação Pod (EPYC 16c/124GB) | Circuito 10 portas (simulação) |
|---|---|---|---|---|
| 0x166b | 3,87GB | **s VERIFIED** (08:33) | **s VERIFIED** (1.345s de check) | ✅ (275s de busca) |
| 0x1669 | 4,5GB | **s VERIFIED** (09:21) | **s VERIFIED** (1.558s de check) | ✅ (11s de busca) |

- Provas geradas independentemente em cada máquina (kissat da fonte em ambas); verificadas por drat-trim compilado independentemente em cada uma. Kissat no pod: 1.115s/1.350s (≈15% mais rápido que o Mac).
- **Lições de engenharia consolidadas:** (1) veredito sem proof logging → prova → verificação, sequencial quando a RAM é curta (dois OOM no Mac antes do acerto); (2) provas de ~4GB exigem ~3-4× em RAM no drat-trim; (3) awk sem fflush engoliu eventos de monitoramento (bug de observabilidade, não de ciência).
- Estados finais: claims 0022 e 0023 = **FINITE_SCOPE_VERIFIED**. Provas regeneráveis deterministicamente (`cert_remote.sh`/`cert_pipeline.sh`); artefatos grandes fora do git.

- ~~Conclusão intermediária (histórica, mantida por governança):~~ "sob o encoder validado no gate, não existe AIG de 9 portas para 0x166b; opt=10 pendente de certificado DRAT e de auto-verificação do ub" — **SUPERADA em 2026-07-11** pela tabela de certificação acima (ambas as classes com DRAT verificada 2× e circuito de 10 portas simulado).
- **Conclusão permitida (final, 2026-07-11):** opt_AIG(0x1669) = opt_AIG(0x166b) = 10 na base AIG do catálogo (portas AND-2, inversões livres), com cadeia: encoder validado (G3) · UNSAT k=9 certificado DRAT em duplicata · UNSAT empírico k=1..8 (addendum abaixo) · circuito de 10 portas verificado por simulação.
- **Conclusão NÃO permitida:** nada além destas classes/base/modelo; nada assintótico; nada sobre n=5.

### Addendum 2026-07-11 — varredura k=1..8 (fecho do finding v da REV-0005/GLM)

- **Motivação:** o encoder pergunta "existe circuito com **exatamente** k portas". UNSAT em k=9 refuta opt=9; para opt≤8 o argumento era só o lema de minimalidade (se opt=m, um circuito mínimo de m portas é livre de duplicatas, tem todas as portas usadas e saída na última — logo satisfaz o CNF de k=m; UNSAT em k=m refuta opt=m). A REV-0005 (GLM) apontou que esse lema estava implícito e não testado. Fecho empírico: rodar k=1..8 nas duas classes (`lowk_check.py`).
- **k=0 fora do SAT:** 5737 e 5739 não são constantes nem literais (conferido no script).
- **Resultado (execução real, Mac, kissat, `lowk_sweep.log`):** **UNSAT em TODOS os k=1..8, para AMBAS as classes.** Tempos: k≤6 sub-segundo; k=7 ≈ 4–5s; k=8 = 47,9s (0x166b) e 39,2s (0x1669). Tamanhos: k=8 → 993 vars / 89.495 cláusulas. Vereditos sem proof logging (sanidade); o resultado de claim continua ancorado no k=9 com DRAT + este fecho empírico + o lema de minimalidade agora EXPLÍCITO (acima).
- **Atualização 2026-07-11 (fecho do finding 3 da REV-0008/Kimi): a varredura k=1..8 foi CERTIFICADA.** `cert_lowk.py` no pod EPYC (kissat 4.0.4 source, drat-trim 2e3b2dc source): **16/16 execuções (2 classes × k=1..8) UNSAT com prova DRAT "s VERIFIED"**; hashes SHA-256 e tamanhos em `experiments/exp_probe_0001/cert_lowk_results.jsonl` (versionado; maiores provas: k=8 = 203,6MB/0x166b e 170,4MB/0x1669, verificadas em 144s/152s). **Com isso a cadeia inteira k=1..9 é DRAT-certificada** — nenhum elo "confie no solver" resta no lower bound.
- **Consequência:** opt ≥ 9 fica estabelecido pelo lema de minimalidade/normalização (agora explícito) + UNSAT certificado em k=9; a varredura k=1..8 rechecagem cada m≤8 empiricamente. **Correção datada 2026-07-11 (REV-0007/Codex, finding 3):** a formulação anterior "duas vias independentes" era imprecisa — a varredura TAMBÉM depende do lema (UNSAT em k=m só refuta opt=m via o lema) e é NÃO CERTIFICADA (sem DRAT). Status correto: cadeia certificada = lema + DRAT k=9; varredura = sanity check adicional.
- **Correção de unidades (datada 2026-07-11, REV-0007 finding 7):** tamanhos exatos das provas: 0x1669 = 4.785.094.117 bytes (≈4,79 GB decimais; os "4,5GB" registrados acima eram GiB de display do filesystem rotulados como GB); 0x166b = 3.871.475.211 bytes (≈3,87 GB). CNFs: 1.781.704 bytes cada.

---
## EXP-PILOT-N5 — Piloto de medição do n=5 (FASE 6) — **CONCLUÍDO 2026-07-12**

- **Data:** 2026-07-11 · **Código:** `experiments/exp_pilot_n5/` (`sample_n5.py` amostrador,
  `pilot_run.py` runner) · **Pré-registro:** `13_FASE6_PLAN.md` §3 + Emenda 1.
- **Amostra:** 320 classes NPN de n=5 (300 uniformes sobre funções, seed=20260711, com órbita p/
  reponderação HT + 20 simétricas distintas). **Pré-gate:** n=3 completo 256/256 bidirecional ✓.
- **Protocolo:** busca ascendente k=0,1,... até SAT (verificado por simulação) ou censura em
  7.200s/classe; sem proof logging; tempos e tamanhos de CNF registrados por k.
- **Infra:** pod EPYC 16c/124GB re-provisionado (Ubuntu 20.04; kissat 4.0.4 source; drat-trim
  2e3b2dc source). 16 workers, lançados 16:35 UTC.
- **Conclusão permitida (quando terminar):** distribuição empírica de opt e custo em n=5 NA AMOSTRA;
  extrapolações via pesos HT com incerteza declarada. **NÃO permitida:** valores individuais como
  claims (sem certificação DRAT nesta fase); nada sobre a cauda censurada além de "≥ k censurado".

### Resultado final (2026-07-12, 470/470 classes, 0 erros)

- **Execução:** 3 frentes (pod1 16w + pod2 16w — 2º pod adicionado por Luiz p/ acelerar — + Mac 6w,
  rebalanceamento 187/186/70+já-feitos); sobreviveu a 2 preempções + 1 blip de rede (monitor com
  sync de 15min). Outputs: `out_pod/`, `out_pod2/`, `out_mac/`; relatório `pilot_final_report.txt`.
- **RANDOM (450 classes, uniforme sobre funções, pesos HT):** 21 decididas / **429 censuradas (95,3%)**.
  Decididas (HT por classe): opt=8: 6,9% · opt=9: 17,2% · opt=10: 75,9%. Censuras: k=9: 8, k=10: 421
  ⟹ a classe aleatória típica de n=5 está em opt ≥ 11 (não-resolvida em k=10 dentro de 2h).
  Custo/classe decidida: mediana 3.317s, p90 6.553s.
- **SYMMETRIC (20 classes):** 3 decididas em segundos (opt 0/4/9), 17 censuradas — simetria NÃO
  garante facilidade além das triviais.
- **Extrapolação (616.126 classes, censura contada como PISO de 7.200s):** custo médio HT
  6.996s/classe ⟹ **recorte A (censo completo) ≥ 1,197 MILHÃO de horas-core** (~780 dias em 64
  cores; ~US$ 48k em pricing RunPod) — E o piso subestima a cauda. **Recorte A inviável.**
- **Leituras p/ os recortes:** B (opt ≤ K) exige filtro heurístico de upper bound ANTES do exato
  (sem isso, achar os ≤ K custa o censo inteiro); C (amostra estratificada) é viável em burst de
  64+ cores mas com budget/classe maior ou aceitando censura como rótulo; D (outras bases em n=4)
  já demonstrado barato — o censo de fórmulas do EXP-GAP-N4 (2,4s) é o primeiro exemplar.


## EXP-GAP-N4 — Censo completo de gap (tree − opt) nas 222 classes NPN de n=4 — **CONCLUÍDO**

- **Data:** 2026-07-11 · **Código:** `experiments/exp_unitgap_check/tree_gap_n4.py` · **Saída:**
  `npn4_gap.csv` + `tree_gap_n4_out.txt` · **Runtime:** 2,4s (numpy, Mac, nice 19).
- **Método:** tree(f) para TODAS as 65.536 funções por DP em camadas (mesmo modelo AIG do
  `tree_gap_n3.py`: negações livres nas arestas e na saída ⟹ camadas fechadas por complemento
  absorvem polaridades; custo 0 = constantes e literais). opt(f) lido do catálogo completo
  `npn4_opt_aig.csv` (EXP-GATE/PROBE, claims 0022/0023). tree e opt são NPN-invariantes no
  modelo (perm/neg de entrada e neg de saída livres) ⟹ basta avaliar nas 222 representantes.
- **Resultado:** distribuição de gap sobre as 222 classes: `{0: 93, 1: 57, 2: 40, 3: 13, 4: 14,
  5: 2, 6: 3}`. **72/222 classes (32,4%) têm gap ≥ 2** — a tese do Unit Gap (gap ∈ {0,1},
  Thm 2 de arXiv:2603.08033) falha em ~1/3 das classes de n=4, não apenas em ⊕₃. Gap máximo
  = 6, atingido exatamente por 0x1668, 0x16e9 e 0x6996 (paridade-4 e vizinhas), com opt=9
  (catálogo) e tree=15. Max tree global = 15.
- **Verificações:** (i) sanity interno: tree(f) = tree(¬f) para todas as 65.536 e tree ≥ opt em
  todas as 222 classes (asserts no script); (ii) **cross-check de embedding: as 256 funções que
  ignoram x4 batem 256/256 com a tabela n=3** (que tinha verificação dupla no EXP anterior);
  (iii) **fail-safe analítico para o pior caso:** Khrapchenko dá L(⊕₄) ≥ 16²/(8·8) = 16 folhas
  ⟹ tree(⊕₄) ≥ 15 — a enumeração atingiu EXATAMENTE o lower bound (tree=15), e opt(⊕₄)=9 tem
  circuito explícito no catálogo ⟹ gap(⊕₄) = 6 independe da enumeração para a direção ≥.
- **Limite declarado:** tree por enumeração única (sem DRAT — proof logging não se aplica a DP);
  o lado opt herda a certificação do catálogo. Implementação única ⟹ claim 0026 fica em
  COMPUTATIONALLY_TESTED (o embedding n=3 e Khrapchenko mitigam, não substituem, 2ª implementação).

## EXP-XAG-N4 — Catálogo completo opt_XAG e tree_XAG nas 222 classes NPN de n=4 (Trilha D da FASE 6) — **CONCLUÍDO 2026-07-13**
### Resultado (2026-07-13, gates X1+X2 PASSARAM antes do censo)

- **Gate X1 (n=2):** AND2=XOR2=1; 16/16 funções com opt ≤ 1. **Gate X2 (n=3 completo):**
  enumeração exaustiva independente até k=4 cobre 256/256 e BATE com encoder+kissat nas duas
  direções; opt_XAG ≤ opt_AIG nas 256 (estritamente melhor em 128); opt_XAG(⊕₃)=2 (AIG: 6);
  NPN-invariância amostrada ✓. Distribuição n=3: {0:8, 1:30, 2:114, 3:80, 4:24} (max 4 vs 6 AIG).
- **Censo n=4 (222 classes, 9min total, classe mais cara 45s):** opt_XAG ∈ 0..7 —
  {0:2, 1:2, 2:5, 3:20, 4:34, 5:75, 6:72, 7:12}. XAG estritamente melhor que AIG em **190/222**.
  ⊕₄: opt_XAG=3 (AIG: 9). tree_XAG (DP em camadas AND+XOR, 0,1s): max 7 (AIG: 15); embedding
  n=3 256/256 ✓.
- **ACHADO CENTRAL — gap por base:** gap_XAG = tree_XAG − opt_XAG é **{0: 256}** em n=3 (funções)
  e **{0: 218, 1: 4}** em n=4 (classes). Ou seja: a propriedade "Unit Gap" (gap ∈ {0,1}), FALSA
  na base AIG (72/222 violações, gap até 6 — EXP-GAP-N4/claim 0026), VALE empiricamente na base
  XAG até n=4. O gap grande do AIG é estrutura de paridade que o XOR nativo absorve.
- **Níveis de certificação (declarados):** modelos SAT verificados por simulação (assert no
  runner); lado UNSAT por kissat SEM DRAT nesta fase (adicionável nas classes de fronteira);
  poda kmax=opt_AIG é sound (opt_XAG ≤ opt_AIG provado por inclusão de base e verificado no X2c);
  tree por DP com método já duplamente validado na base AIG + embedding. Claims 0027/0028.
- **Custo:** ~10min de Mac. Artefatos: `exp_xag_n4/` (encoder, gates, censo, npn4_xag.csv,
  tree_xag_n4.npy, logs).


- **Contexto:** primeiro item da Trilha D (outras bases em n=4), iniciado sob o direcionamento de
  Luiz ("estamos focados no P=NP"; a decisão estratégica do recorte n=5 permanece aberta e é dele).
- **Base XAG:** portas AND-2 (polaridades livres nas arestas) + XOR-2 (entradas positivas —
  normalização padrão: negação comuta com XOR e é absorvida pelo consumidor/saída); negação de
  saída livre; custo = número TOTAL de portas (AND+XOR). NOTA de novidade: multiplicative
  complexity (só ANDs contam, XOR grátis) é medida CLÁSSICA já computada na literatura para
  n pequenos (Turan–Peralta e sucessores) — nosso alvo é o custo total de portas, que é o análogo
  direto do catálogo AIG; verificação de novidade obrigatória ANTES de qualquer claim de "primeiro".
- **Protocolo:** (X1) sanity n=2 (XOR2 e AND2 ⟹ opt=1); (X2) n=3 COMPLETO — encoder+kissat vs
  enumeração exaustiva independente de circuitos XAG até a profundidade viável + invariantes
  (opt_XAG ≤ opt_AIG nas 256; opt_XAG(⊕₃)=2; NPN-invariância amostrada); só então (X3) censo
  n=4: 222 classes, busca ascendente k=0,1,..., kissat, registro de tempos; DRAT nas UNSAT
  decisivas das classes de fronteira (a definir pelo perfil de custo). Paralelo: tree_XAG por DP
  em camadas (AND+XOR) p/ gap na base XAG.
- **Conclusões permitidas:** valores opt_XAG/tree_XAG por classe (com o grau de certificação usado
  em cada um declarado); tabela cruzada AIG×XAG×fórmula; gaps entre bases. NÃO permitida: claim de
  novidade sem a verificação bibliográfica.
