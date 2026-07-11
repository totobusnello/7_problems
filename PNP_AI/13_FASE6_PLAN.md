# PNP-AI — 13 — FASE 6: plano n=5 + spec de infraestrutura (PROPOSTA — decisão de Luiz)

> Criado 2026-07-11 (Ciclo 14). Status: PROPOSTA. A REV-0004 é vinculante: **n=5 é hipótese sujeita a
> benchmark, não promessa** — por isso este plano é dirigido por um PILOTO DE MEDIÇÃO antes de
> qualquer compromisso de infra ou escopo.

## 1. O problema de escala (números honestos)

- n=5 tem 2^32 funções booleanas em **616.126 classes NPN** (vs 222 em n=4) — fator ~2.775×.
- Nosso benchmark real (n=4): classes FÁCEIS (opt ≤ 7) decidem em segundos; as DUAS classes duras
  (decisão em k=9) custaram 21–26 min/veredito em 1 core + ~40 min de certificação (prova+check) +
  ~4–5 GB de disco por prova.
- Em n=5, ambos os lados pioram: mais linhas de truth table (32 vs 16 ⟹ CNFs ~2× mais largas por
  porta) e opt máximo maior (valor exato desconhecido por nós — o próprio catálogo completo não
  existe na literatura, o que é a oportunidade). **A distribuição de dificuldade em n=5 é
  DESCONHECIDA — e é exatamente o que o piloto mede.**
- Conta ingênua de teto (todas as classes custando como as duras de n=4): 616.126 × 25 min ≈ 29
  anos-core — **inviável por força bruta**; conta ingênua de piso (todas fáceis, ~10 s): ~71
  dias-core — viável. A verdade está no meio e depende da cauda dura ⟹ sem piloto, qualquer spec de
  VPS é chute.

## 2. Recortes científicos candidatos (decisão de escopo — Luiz escolhe APÓS o piloto)

| Recorte | Entrega | Valor | Risco |
|---|---|---|---|
| **A. Catálogo n=5 completo** | 616.126 valores exatos + certificados | Primeiro catálogo público completo (nada análogo publicado que conheçamos — verificação de novidade prévia obrigatória) | Cauda dura pode ser proibitiva; compromisso de meses |
| **B. Catálogo parcial curado** | Todas as classes com opt ≤ K (K definido pelo piloto) + fronteira documentada | Entrega garantida, com "mapa do que falta" público | Menos impactante; K arbitrário sem justificativa científica |
| **C. Dataset ponte C1→C3 (meta-complexidade)** | Amostra estratificada (~10–50k classes) com opt + metadados ricos (nº de circuitos ótimos, estrutura, tempo de solve, tamanho de prova) | Alimenta experimentos MCSP-adjacentes (o caminho de REL crescente da seleção definitiva); amostragem publicável como metodologia | Desenho de amostragem exige cuidado estatístico |
| **D. n=4 em outras bases primeiro** (XAG/MIG/fórmula) | Catálogos completos pequenos, reutilizando pipeline | Entregas rápidas e completas; mais gaps fecháveis | Valor incremental; adia o n=5 |

**Recomendação do coordenador:** C como espinha dorsal (é o que serve à seleção definitiva de C1 —
a ponte para meta-complexidade), com B como subproduto natural (o piloto + a amostra JÁ produzem o
catálogo parcial dos opt baixos). A e D ficam como extensões condicionais.

## 3. PILOTO DE MEDIÇÃO (pré-requisito de tudo; aprovação de Luiz)

- **Amostra:** 300 classes NPN de n=5 sorteadas uniformemente (seed registrada) + as 16 funções
  simétricas de n=5 (interesse estrutural).
- **Protocolo por classe:** busca ascendente k=0,1,2,… até SAT (cada SAT verificado por simulação —
  regra do programa); registrar opt, tempo por k, tamanho do CNF. SEM proof logging na fase de
  medição (lição do EXP-PROBE-0001); certificação DRAT apenas de uma subamostra (ex.: 10 classes)
  para medir custo de certificação em n=5.
- **Saídas:** distribuição empírica de opt em n=5; curva tempo×k; extrapolação de custo para os
  recortes A–C; spec de infra baseada em dados.
- **Critérios de aborto pré-registrados:** timeout por classe de 2h (classe vira "dura, censurada à
  direita" — dado, não falha); budget total do piloto: 72h de wall-clock na infra existente.
- **Infra do piloto:** pod RunPod atual (16 cores paralelos, ligado só durante o piloto ≈ US$ 46
  por 72h) — SEM contratar nada novo.
- **Encoder:** o atual (`aig_exact.py` generaliza para n=5 trocando n; validação G3-style adicional
  em n=3 COMPLETO — todas as 256 funções, k até 4 — antes do piloto, para revalidar a generalização).

## 4. Spec de infraestrutura (PROVISÓRIA — contratar só após o piloto)

**Requisitos derivados do benchmark n=4:**
- CPU: kissat é single-thread ⟹ o que importa é nº de cores × clock. Paralelismo é por classe
  (embaraçosamente paralelo, job queue simples).
- RAM: drat-trim precisa ~3–4× o tamanho da prova (provas de 4–5 GB ⟹ ~16–20 GB por job de
  verificação; em n=5 provas duras podem ser maiores — piloto mede).
- Disco: provas são transientes (gerar → verificar → registrar hash → apagar); 1–2 TB NVMe dão
  folga para ~10–20 verificações simultâneas em fila.

**Opções de custo (ancoradas no preço real do pod):**

| Opção | Custo | Quando faz sentido |
|---|---|---|
| Pod RunPod atual sob demanda (EPYC 16c/124GB, US$ 0,64/h) | ~US$ 155/mês a 8h/dia; US$ 470/mês 24/7 | Piloto e campanhas intermitentes — **já disponível, zero setup** |
| Servidor dedicado 16c/128GB/NVMe (classe Hetzner AX/OVH; a cotar) | ~€100–130/mês 24/7 (ordem de grandeza; cotar na contratação) | Campanha contínua > 1 mês — quebra o ponto de equilíbrio vs pod 24/7 |
| Pod/servidor maior (32–64 cores) | escala ~linear com cores | Se o piloto mostrar cauda dura grande e Luiz quiser prazo curto |

**Regra de decisão proposta:** piloto no pod atual → se a campanha escolhida custar > ~700 h-core,
contratar dedicado mensal (mais barato que pod 24/7 e sem risco de preempção); senão, seguir no pod
sob demanda. Contratação é decisão de Luiz com os números do piloto na mesa.

## 5. Engenharia antes da campanha (independente do recorte)

1. **Job queue por classe** (fila + retomada + registro por classe) — generalização trivial dos
   scripts atuais.
2. **Pipeline prova→verifica→hash→apaga** para caber no disco (lição dos 8+ GB de provas de n=4).
3. **Cube-and-conquer** (SRC-0021) para a cauda dura — avaliar só SE o piloto mostrar classes
   censuradas demais; não é pré-requisito.
4. **Coleta C1→C3 desde o dia 1:** por classe, além do opt: circuito-testemunha, tempo por k,
   tamanho do CNF/prova. Contagem de circuitos ótimos (AllSAT) só em subamostra — custo alto.
5. **Verificação de novidade específica de n=5** antes de qualquer campanha grande (mesmo protocolo
   do re-check Krinkin: literatura de exact synthesis + repos públicos) — o catálogo pode existir
   parcialmente em artefatos de EDA.

## 6. O que este plano NÃO decide (fica com Luiz)

1. Aprovação do PILOTO (budget: ~72h de pod ≈ US$ 46 + supervisão minha).
2. Escolha do recorte (A–D) — só depois dos dados do piloto.
3. Contratação de VPS/dedicado — só depois do piloto; até lá, pod sob demanda.
4. Qualquer publicação do que sair do n=5 (10_PUBLICATION_RULES, como sempre).

---

## EMENDA 1 (2026-07-11, ANTES da execução do piloto) — desenho de amostragem corrigido

1. **Amostragem:** o pré-registro dizia "300 classes sorteadas uniformemente". Uniforme SOBRE CLASSES
   exigiria enumerar as 616.126 classes (computação pesada que o piloto não pressupõe). Corrigido
   para: **uniforme sobre FUNÇÕES** (truth tables de 32 bits, seed=20260711), canonicalizadas para
   NPN (7.680 transformações), com **tamanho de órbita registrado por classe** ⟹ estimativas
   sobre classes usam pesos de Horvitz-Thompson w=1/órbita. Viés declarado e corrigível.
2. **Simétricas:** o plano dizia "16 funções simétricas" — o correto para n=5 é **64** (2^6 mapas de
   popcount); canonicalizadas resultaram em **20 classes NPN distintas** adicionais (0 sobreposição
   com o estrato aleatório). Amostra final: **320 classes**.
3. **Pré-gate executado e PASSOU (2026-07-11):** validação bidirecional COMPLETA de n=3 — 256/256
   funções, encoder ≡ enumeração independente até k=4 (230 alcançáveis batem; 26 inalcançáveis
   confirmadas UNSAT k=1..4), com verificação por simulação de todo SAT.
4. **Infra:** pod foi RE-PROVISIONADO por Luiz (novo endpoint; mesmo hardware EPYC 4564P 16c/124GB;
   Ubuntu 20.04 neste container); stack reinstalado do fonte (kissat 4.0.4; drat-trim commit 2e3b2dc
   — agora REGISTRADO também para o pod, fechando o gap de proveniência da REV-0007 finding 9 para
   execuções futuras). Autorização do piloto: Luiz forneceu o SSH em resposta ao checkpoint.
5. **Lançado:** 2026-07-11 16:35 UTC — 16 workers paralelos, 320 classes em 16 shards round-robin,
   budget 7.200s/classe (pré-registrado), sem proof logging. Scripts em `experiments/exp_pilot_n5/`.
