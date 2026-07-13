# 11 — AUDIT TRACK — Charter da trilha de auditoria certificada da literatura

> **Status: PROPOSTA para revisão de Luiz (2026-07-13). NADA executa antes da aprovação.**
> Origem: reflexão estratégica de Luiz — "será que não é melhor entrarmos para a história tendo
> ganhos e ajudando com alguma vitória onde as teorias empacaram ou estão com resultado errado?"
> Proof of concept já entregue: o pacote Unit Gap (refutação certificada + reparo + 4 famílias +
> Lean + contato respeitoso, custo < US$ 100).

## 1. Missão (v1.1 — escopo Millennium aprovado por Luiz, 2026-07-13)

Produzir, em cadência, **refutações e reparos certificados por máquina** de claims publicados que
estejam errados, sem prova, ou empacados — **na literatura dos 7 Problemas do Milênio, atacando UM
problema por vez** (decisão de Luiz: "quero tentar fazer esta trilha com os 7 problemas do milênio,
atacando 1 por vez"). A trilha COMPLEMENTA a linha PNP-AI (que segue, com a FASE 6C como
instrumento); não a substitui.

### 1a. Auditabilidade por problema (avaliação honesta — ordena a fila)

| # | Problema | Auditabilidade mecânica | Observações |
|---|---|---|---|
| 1 | **P vs NP** | ★★★★★ EM VOO | Ground truth finita (circuitos/SAT), ferramentas validadas; caso 1 = Krinkin (2 issues) |
| 2 | **Navier–Stokes** | ★★★★ | arXiv cheio de "provas" erradas de regularidade (alvo-rico); auditoria via análise + numerics rigorosa (aritmética intervalar); conexão pessoal (Barbara) e material aguardando importação |
| 3 | **Riemann** | ★★★★ | Tradição computacional forte (verificação de zeros, Λ de de Bruijn–Newman/Polymath 15); "provas" erradas abundantes e frequentemente mecanizáveis |
| 4 | **BSD** | ★★★ | Teoria computacional de números (curvas elípticas, LMFDB); claims verificáveis existem, exige tooling novo |
| 5 | **Yang–Mills** | ★★ | Sem framework matemático consensual; lattice é computável mas a distância claim→certificado é grande |
| 6 | **Hodge** | ★ | Quase puramente abstrato — fit fraco para auditoria mecanizada |
| — | **Poincaré (resolvido)** | caso especial | O "gap" é de formalização (prova de Perelman não formalizada) — mega-projeto fora da nossa escala; fica como estudo de caso, não alvo |

Regra: só se passa ao problema seguinte quando o atual tiver ≥ 1 vitória reconhecida OU a fila de
alvos scoreados dele secar (decisão de Luiz em ambos os casos). Estrutura de diretórios já existe
(PNP_AI, NS_PROB, RH_AI, BSD_AI, HODGE_AI, YM_AI, POINCARE_CASE — Sessão 0).

## 2. Por que isto pode "entrar para a história"

- Refutação certificada é rara e definitiva: contraexemplo + DRAT + formalização não admite réplica.
- Existe o movimento de formalização (Lean/Mathlib), mas NÃO existe um programa organizado de
  **auditoria adversarial AI-assisted** da literatura viva, com certificados e reparos. Ser o
  primeiro programa disciplinado nisso é uma posição, não um resultado isolado.
- Economia: cada auditoria custa dias e dezenas de dólares; o valor esperado por dólar domina
  qualquer tentativa de resolução frontal.

## 3. Protocolo de seleção de alvos (gate obrigatório antes de gastar 1 ciclo)

Score 1–5 em cada eixo; alvo só entra com **checabilidade ≥ 4 E (peso ≥ 3 OU reparo ≥ 4)**:

| Eixo | Pergunta |
|---|---|
| **Checabilidade** | Um contraexemplo/validação pode ser CERTIFICADO por máquina (SAT/DRAT, enumeração com gate, Lean)? |
| **Peso (load-bearing)** | O claim é citado/usado por outros resultados ou por um programa ativo? Refutá-lo/repará-lo muda algo para alguém? |
| **Tratabilidade** | Cabe nas nossas ferramentas e budget (dias, não meses)? |
| **Reparabilidade** | Conseguimos oferecer conserto junto (prova corrigida, versão enfraquecida verdadeira, catálogo fechado)? |
| **Risco reputacional** | Postura do autor/comunidade; claim recente vs consagrado; chance de estarmos nós errados. |

**Fontes de alvos:** arXiv cs.CC / math.CO recentes com provas "sketch"; tabelas/catálogos
publicados sem certificados; claims folclóricos usados sem prova; solicitações da comunidade.
**Anti-padrões (recusar):** erro trivial de autor obscuro (gotcha sem peso); claims não
mecanizáveis (só prosa assintótica); áreas sem ground truth computacional.

## 4. Pipeline (o template validado no Unit Gap — inalterado)

1. **Fonte verbatim** (parse mecânico, SRC no ledger) → extração de claims com IDs.
2. **Checagem mecanizada** com gates pré-registrados (encoder/enumeração validados ANTES do alvo).
3. **Dupla implementação** de qualquer computação decisiva + fail-safe analítico quando existir.
4. **Revisão adversarial multi-família:** ≥ 2 famílias para claim interno; **4 famílias para
   qualquer contato externo** (padrão REV-0009..0012).
5. **Formalização Lean** quando o resultado justificar (refutação de teorema publicado: sim).
6. **Contato:** pergunta-antes-de-afirmar, reparo anexado, tom do krinkin/unit-gap#1. SEMPRE com
   autorização explícita de Luiz (herda o charter do programa).
7. **Nota técnica** por auditoria (formato da casa, níveis de verificação explícitos).
   Publicação: 10_PUBLICATION_RULES, decisão de Luiz.

## 5. Cadência e portfólio

- **1 alvo por vez**, ciclo de auditoria alvo: ≤ 2 semanas (se estourar, checkpoint com Luiz).
- Portfólio de publicação: notas individuais → bundle "case studies em refutação certificada"
  → paper de metodologia (o motor em si) quando houver ≥ 3 casos.
- A linha PNP-AI continua em paralelo (FASE 6C aguarda go; issues do Krinkin monitoradas).

## 6. Métricas de vitória (honestas)

- Refutação/reparo RECONHECIDO (autor corrige/responde, ou errata, ou citação do nosso material).
- Validação independente de tabela load-bearing adotada como referência.
- Formalização aceita em ecossistema público (quando aplicável).
- NÃO conta: volume de refutações sem peso; "gotchas" sem reparo.

## 7. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Virar "caçador de erro" | Reparo junto, sempre; anti-padrões do §3; tom do template |
| Nós estarmos errados em público | 4 famílias + certificados ANTES de qualquer contato; formato pergunta |
| Alvo sem peso = esforço perdido | Gate de seleção com score; Luiz aprova cada alvo |
| Dispersão (abandonar P=NP) | Escopo inicial = literatura P=NP-adjacente; FASE 6C segue |

## 8. Fila de execução (Problema 1 = P vs NP, EM VOO)

1. **Follow-ups Krinkin** (já em voo — respostas às 2 issues podem gerar a 1ª "vitória reconhecida").
2. **Varredura pré-registrada de cs.CC/math.CO recente** por claims mecanizáveis em circuit
   complexity/meta-complexidade — produz shortlist scoreada para Luiz escolher o alvo 2.
3. **Tabelas/catálogos sem certificado** citados por ferramentas — validação estilo MIG-match.

Problema 2 (Navier–Stokes) entra quando: regra do §1a disparar + material da Barbara importado +
Sessão 0 do NS autorizada (mapa da literatura + fit de auditoria específico).

## 9. O que este charter NÃO autoriza

Nenhum alvo, nenhuma varredura, nenhum contato, nenhuma publicação. Cada um exige aprovação
explícita de Luiz, como sempre.
