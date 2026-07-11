# 02 — COMPARATIVE AI-FIT — Tabela consolidada de estado e compatibilidade AI-first

> Última revisão: 2026-07-10 (Sessão 0 — auditoria inicial)
> "Estado oficial" = fato externo (ver `01_OFFICIAL_STATUS.md`). "Compatibilidade AI-first" = hipótese estratégica interna.
> **Compatibilidade com IA ≠ menor dificuldade matemática.** Este scorecard NÃO é um ranking de dificuldade.

## Definição de compatibilidade AI-first

Grau em que as ferramentas atuais (LLMs, SAT/SMT solvers, CAS, proof assistants, busca automatizada, execução exata) conseguem interagir diretamente com os objetos, experimentos e métodos de verificação do problema.

## Critérios utilizados

Natureza discreta/contínua dos objetos · representação finita · verificabilidade exata · maturidade das ferramentas · bibliotecas formais disponíveis · geração automática de contraexemplos · execução de algoritmos candidatos · dados estruturados · decomposição em subproblemas falsificáveis · distância evidência→prova · dependência de conhecimento especializado · revisão automatizada independente.

## Tabela consolidada (auditada na Sessão 0)

| # | Problema | Área | Estado (Clay, 2026-07-10) | AI-fit | Justificativa resumida | Papel no 7_PROBLEMS | Auditoria S0 |
|---|---|---|---|---|---|---|---|
| 1 | P versus NP | Complexidade computacional | Unsolved | **Muito alta** | Objetos discretos finitamente representáveis (algoritmos, circuitos, grafos, fórmulas, provas); SAT/SMT, execução exata, instâncias adversariais, formalização progressiva. Dificuldade continua extrema (P≠NP exige limitação universal; P=NP exige algoritmo correto para todas as entradas). | Primeiro laboratório AI-first | **CONFIRMADA** |
| 2 | Navier–Stokes | EDPs, análise, fluidos | Unsolved | **Média-baixa** | IA ajuda em reconstrução de provas, literatura, manipulação simbólica, estimativas, simulação. Mas objetos contínuos e infinito-dimensionais; simulação finita não demonstra regularidade global. | Segunda frente estratégica (origem pessoal; artigo Busnello–Flandoli–Romito) | **CONFIRMADA** |
| 3 | Birch e Swinnerton-Dyer | Teoria dos números, geometria aritmética | Unsolved | **Alta** | Grande volume de dados computáveis (curvas elípticas, funções L, ranks — LMFDB); experimentação exata, CAS, geração de conjecturas. Passagem evidência→prova geral profundamente difícil. | Candidata a 3ª frente após validação da metodologia | **CONFIRMADA** |
| 4 | Hipótese de Riemann | Teoria analítica dos números | Unsolved | **Média-alta** | Objeto central preciso, literatura ampla, muitos dados numéricos, cálculo simbólico. Verificar finitos zeros não prova para todos. | Frente futura de experimentação limitada | **CONFIRMADA** |
| 5 | Conjectura de Hodge | Geometria algébrica, topologia | Unsolved | **Média** | Objetos formalmente definíveis, alguma computação algébrica; mas abstração elevada, formalização extensa, rede profunda de dependências. | Frente posterior, condicionada a especialistas e bibliotecas formais | **CONFIRMADA** |
| 6 | Yang–Mills e mass gap | Física matemática, QFT | Unsolved | **Baixa** | Simulações exploram modelos, mas parte do desafio é construir rigorosamente a própria teoria em 4D antes de provar o gap. Distância simulação→prova especialmente grande. | Longo prazo; não iniciar sem especialistas humanos | **CONFIRMADA** |
| — | Conjectura de Poincaré | Topologia, geometria diferencial | **Solved** (Perelman) | N/A p/ nova solução; alta p/ estudo retrospectivo | Caso de controle: como uma solução foi construída, verificada e aceita; teste de reconstrução formal de prova conhecida. | Caso de controle histórico/metodológico | **CONFIRMADA** |

## Auditoria da Sessão 0 (2026-07-10)

- **Estados oficiais:** todos verificados diretamente em claymath.org — coincidem com o briefing. Confiança: alta.
- **Classificações AI-fit:** nenhuma alteração proposta nesta sessão. A auditoria de Sessão 0 é preliminar (baseada no briefing + conhecimento geral); a auditoria profunda com literatura é entregável da **FASE 1**, que confirmará, revisará ou rejeitará cada linha.
- **Ressalva registrada:** a classificação "Muito alta" de P vs NP depende de solvers/proof assistants ainda **não instalados** neste ambiente (ver `03_TOOL_INVENTORY.md`). A compatibilidade é da classe de ferramentas, não do setup atual — gap de infraestrutura, não de classificação.
- Nível de confiança geral: médio-alto (pendente FASE 1).

## Reavaliação obrigatória

Ao final da FASE 1 · a cada nova integração relevante · a cada novo sistema de formalização/busca · ao obter acesso a especialistas · quando resultado científico alterar uma linha · no mínimo 1× por ciclo estratégico.

Toda mudança registra: classificação anterior, nova, motivo, evidências, fontes, confiança, data.

## Histórico de alterações

| Data | Mudança | Motivo | Confiança |
|---|---|---|---|
| 2026-07-10 | Tabela criada a partir do briefing; estados verificados no Clay; nenhuma classificação alterada | Sessão 0 | Médio-alto |
