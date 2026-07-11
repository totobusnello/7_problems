# REV-0010 — Codex/gpt-5.6-sol — verbatim (2026-07-11)

> Chamada via tools/rev.sh codex, sandbox read-only, background da sessão principal. Session id 019f524d-25d3-7370-95fa-a05b942dbcbf.

SUSTENTADA

1. **[CRÍTICA] O Teorema 2 confunde fórmula com DAG decomposto apenas na raiz.**

   Pela definição textual do paper, uma fórmula é uma AIG em que toda porta tem fan-out 1, isto é, uma árvore. Portanto, se a porta raiz decompõe \(f\) em \(a\land b\), seus filhos também precisam ser fórmulas:

   \[
   \operatorname{tree}(f)=
   \min_{f=a\land b\ \text{ou}\ \bar f=a\land b}
   \bigl(1+\operatorname{tree}(a)+\operatorname{tree}(b)\bigr).
   \]

   A equação do paper substitui ilegalmente esses termos por \(\operatorname{opt}(a)\) e \(\operatorname{opt}(b)\). Os DAGs ótimos dos filhos podem conter compartilhamento interno; colocá-los sob uma nova porta não os transforma em árvores.

   Consequentemente, \(f=1\land f\) produz apenas

   \[
   \operatorname{tree}(f)\le 1+\operatorname{tree}(f),
   \]

   não \(\operatorname{tree}(f)\le1+\operatorname{opt}(f)\).

2. **[CRÍTICA] A paridade de três variáveis é um contraexemplo exato: \(\operatorname{opt}=6\), \(\operatorname{tree}=9\), gap \(=3\).**

   Fiz uma enumeração independente por camadas de custo, sem reutilizar o laço de relaxação do dossiê. Partindo de constantes e literais e fechando sob

   \[
   (a,b)\mapsto a\land b,\quad \overline{a\land b},
   \]

   as quantidades de novas funções por custo foram:

   \[
   24,64,30,80,32,0,16,0,2
   \]

   para custos \(1,\ldots,9\). As duas últimas funções são exatamente \(0x96\) e \(0x69\), paridade e complemento. Nenhuma delas ocorre com custo \(\le8\).

   Assim, o intervalo teórico dado por Khrapchenko é \(\operatorname{tree}\in\{8,9\}\), mas o DP exato fecha o valor em \(9\). Logo:

   \[
   \operatorname{gap}(\oplus_3)=9-6=3.
   \]

   A formulação “gap \(\in\{2,3\}\)” é válida antes do DP; após o DP, o valor exato é 3.

3. **[ALTA] A recursão e a implementação do DP estão corretas.**

   Auditei [tree_gap_n3.py](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n3.py):

   - Base custo zero em \(0,1,x_i,\bar x_i\): correta.
   - Inversão gratuita na saída: coberta por atualizar \(g=a\land b\) e \(\bar g\).
   - Inversões internas: cobertas porque \(a,b\) percorrem todas as funções.
   - Folhas repetíveis: corretamente permitidas; apenas portas estão sujeitas a fan-out 1.
   - Restrição \(b\ge a\): válida pela comutatividade do AND.
   - Atualizações in-place: explicam as três rodadas, mas não comprometem a exatidão. Cada valor finito possui uma fórmula-testemunha; no ponto fixo, indução sobre uma fórmula mínima mostra que nenhum custo menor foi omitido.
   - O conjunto é finito e os custos são inteiros não negativos, garantindo terminação.

4. **[ALTA] A equivalência AIG-fórmula ↔ fórmula De Morgan preserva o número de portas binárias.**

   Uma fórmula AIG pode ter todas as inversões empurradas até as folhas por De Morgan. Cada AND continua sendo exatamente uma porta AND ou OR, sem criação de nova porta binária. Reciprocamente, cada OR vira um AND com inversões nas arestas e na saída.

   Portanto, o número de ANDs na fórmula AIG é igual ao número de portas binárias na fórmula De Morgan. Para uma árvore binária, portas \(=\) folhas \(-1\).

   Para \(\oplus_3\), tomando \(A=f^{-1}(0)\), \(B=f^{-1}(1)\) e as arestas do cubo entre eles:

   \[
   |A|=|B|=4,\qquad |E|=12.
   \]

   Khrapchenko fornece

   \[
   L(f)\ge \frac{|E|^2}{|A||B|}
   =\frac{144}{16}=9
   \]

   folhas, logo pelo menos 8 portas. A construção explícita tem 10 folhas/9 portas; o DP exclui 8 e prova 9.

5. **[ALTA] \(\operatorname{opt}(\oplus_3)=6\) está solidamente sustentado.**

   Há uma construção de seis portas por dois XORs AIG de três portas encadeados. Reexecutei a instância SAT para cinco portas e obtive `UNSAT`.

   O encoder também parece completo para circuitos mínimos não constantes:

   - exigir operandos distintos não elimina solução mínima: \(u\land u=u\) e \(u\land\bar u=0\);
   - omitir a constante como entrada de portas não elimina circuito mínimo não constante;
   - exigir que toda porta anterior seja usada é válido em um circuito mínimo;
   - proibir portas duplicadas é válido, pois uma duplicata pode ser substituída pela outra;
   - a saída pode ser colocada na última porta por ordenação topológica.

   A construção SAT de seis portas foi simulada em todas as oito entradas. A única ressalva de reprodutibilidade é que o arquivo DRAT original foi apagado; o output preserva apenas o resultado, hash e verificação registrada. Isso não põe o número em dúvida, mas arquivar CNF e DRAT fortaleceria o certificado permanente.

6. **[CRÍTICA] O Corolário 6 é diretamente falso: pode haver \(s=3\).**

   No circuito ótimo:

   \[
   a=x_1\oplus x_2,
   \quad h_0=a\land\bar x_3,
   \quad h_1=\bar a\land x_3,
   \quad f=h_0\lor h_1,
   \]

   o sub-DAG de \(a\) possui três portas e está contido integralmente nos dois sub-DAGs filhos da saída. Portanto:

   \[
   s=|D_{h_0}\cap D_{h_1}|=3.
   \]

   Os dois filhos têm complexidade ótima 4; reexecutei também `UNSAT` em três portas para \(h_0\). Assim:

   \[
   1+\operatorname{opt}(h_0)+\operatorname{opt}(h_1)-s
   =1+4+4-3=6.
   \]

   Isso contradiz diretamente \(s\in\{0,1\}\). Além disso, o “optimal substructure” usado pelo paper não é válido em geral quando o sub-DAG possui portas compartilhadas com outras regiões: substituir apenas um filho não permite necessariamente remover todas as portas antigas.

7. **[ALTA] Há uma ressalva lógica importante sobre o Teorema 7.**

   Sob a definição padrão, \(\oplus_3\) tem gap 3. Logo seu \(s=3\) **não é, sozinho, contraexemplo ao enunciado formal condicional** do Teorema 7, que começa com “gap\((f)=1\)”.

   O que se pode concluir rigorosamente é:

   - a prova do Teorema 7 cai, pois depende do Corolário 6 falso;
   - a afirmação posterior de que o teorema classifica todo compartilhamento em qualquer AIG ótima é falsa;
   - sob a grandeza não padrão efetivamente usada na Tabela 1, a paridade é classificada como “gap 1”; nessa leitura, o mesmo circuito com \(s=3\) contradiz diretamente o Teorema 7.

   Portanto, a alegação de que o Teorema 7 foi **independentemente refutado sob a definição padrão** é forte demais. Ele fica sem prova; já sob o “gap” computado pelo autor, fica diretamente contradito.

8. **[MÉDIA] Os Teoremas 3 e 4 sobrevivem, embora a prova publicada do Teorema 3 tenha uma contagem defeituosa.**

   No Teorema 3, o paper afirma que as portas estritamente abaixo de \(g\), excluindo \(g\), exigem \(k-1\) portas. Isso é falso: se \(g=x_1\land x_2\), há zero portas estritamente abaixo, não uma. Também pode haver interfaces laterais entre o cone de \(g\) e o restante do circuito.

   Contudo, o resultado tem uma prova simples. Seja \(m\) o número de portas de uma AIG ótima útil e \(n\) o número de entradas essenciais. Há \(2m\) incidências de entrada em portas. Cada uma das \(n\) entradas essenciais possui fan-out pelo menos 1; cada uma das \(m-1\) portas não finais possui fan-out pelo menos 1. Se alguma porta é compartilhada, há pelo menos uma incidência adicional:

   \[
   2m\ge n+(m-1)+1=n+m,
   \]

   logo \(m\ge n\). Na verdade isso vale sempre que gap \(>0\), não apenas gap \(=1\).

   O Teorema 4 também sobrevive. Uma AIG reconvergente útil de três portas tem necessariamente

   \[
   g_1\to g_2\to g_3,\qquad g_1\to g_3.
   \]

   Escrevendo \(u\) para uma polaridade de \(g_1\), a saída reduz, conforme as polaridades, a \(0\), \(u\), \(c\land u\) ou \(\bar c\land u\), todos computáveis com no máximo duas portas. Portanto nenhuma função com \(\operatorname{opt}=3\) precisa de compartilhamento.

9. **[CRÍTICA] Nenhuma leitura honesta salva simultaneamente o paper.**

   Pode-se definir uma nova grandeza

   \[
   d(f)=\min\bigl(1+\operatorname{opt}(a)+\operatorname{opt}(b)\bigr).
   \]

   Então \(\operatorname{opt}(f)\le d(f)\le\operatorname{opt}(f)+1\), e o “Unit Gap” vira essencialmente tautológico. Mas \(d\) não é tamanho de fórmula, seus filhos podem ser DAGs, seu ponto fixo não é o Bellman descrito nas seções 3 e 7, e a comparação com a complexidade clássica \(\Theta(n^2)\) da paridade deixa de ser pertinente.

   Resultado final:

   - Teorema 2: **falso** sob a definição publicada de fórmula.
   - Valor exato: \(\operatorname{opt}(\oplus_3)=6\), \(\operatorname{tree}(\oplus_3)=9\), gap \(=3\).
   - Corolário 6: **falso**, com \(s=3\).
   - Teorema 7: prova inválida; diretamente contradito sob o “gap” computado pelo paper, mas não refutado apenas pela paridade sob o gap padrão.
   - Teoremas 3 e 4: **verdadeiros**, embora o Teorema 3 necessite de uma prova corrigida.
tokens used
57.584
SUSTENTADA

1. **[CRÍTICA] O Teorema 2 confunde fórmula com DAG decomposto apenas na raiz.**

   Pela definição textual do paper, uma fórmula é uma AIG em que toda porta tem fan-out 1, isto é, uma árvore. Portanto, se a porta raiz decompõe \(f\) em \(a\land b\), seus filhos também precisam ser fórmulas:

   \[
   \operatorname{tree}(f)=
   \min_{f=a\land b\ \text{ou}\ \bar f=a\land b}
   \bigl(1+\operatorname{tree}(a)+\operatorname{tree}(b)\bigr).
   \]

   A equação do paper substitui ilegalmente esses termos por \(\operatorname{opt}(a)\) e \(\operatorname{opt}(b)\). Os DAGs ótimos dos filhos podem conter compartilhamento interno; colocá-los sob uma nova porta não os transforma em árvores.

   Consequentemente, \(f=1\land f\) produz apenas

   \[
   \operatorname{tree}(f)\le 1+\operatorname{tree}(f),
   \]

   não \(\operatorname{tree}(f)\le1+\operatorname{opt}(f)\).

2. **[CRÍTICA] A paridade de três variáveis é um contraexemplo exato: \(\operatorname{opt}=6\), \(\operatorname{tree}=9\), gap \(=3\).**

   Fiz uma enumeração independente por camadas de custo, sem reutilizar o laço de relaxação do dossiê. Partindo de constantes e literais e fechando sob

   \[
   (a,b)\mapsto a\land b,\quad \overline{a\land b},
   \]

   as quantidades de novas funções por custo foram:

   \[
   24,64,30,80,32,0,16,0,2
   \]

   para custos \(1,\ldots,9\). As duas últimas funções são exatamente \(0x96\) e \(0x69\), paridade e complemento. Nenhuma delas ocorre com custo \(\le8\).

   Assim, o intervalo teórico dado por Khrapchenko é \(\operatorname{tree}\in\{8,9\}\), mas o DP exato fecha o valor em \(9\). Logo:

   \[
   \operatorname{gap}(\oplus_3)=9-6=3.
   \]

   A formulação “gap \(\in\{2,3\}\)” é válida antes do DP; após o DP, o valor exato é 3.

3. **[ALTA] A recursão e a implementação do DP estão corretas.**

   Auditei [tree_gap_n3.py](/Users/lab/Claude/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n3.py):

   - Base custo zero em \(0,1,x_i,\bar x_i\): correta.
   - Inversão gratuita na saída: coberta por atualizar \(g=a\land b\) e \(\bar g\).
   - Inversões internas: cobertas porque \(a,b\) percorrem todas as funções.
   - Folhas repetíveis: corretamente permitidas; apenas portas estão sujeitas a fan-out 1.
   - Restrição \(b\ge a\): válida pela comutatividade do AND.
   - Atualizações in-place: explicam as três rodadas, mas não comprometem a exatidão. Cada valor finito possui uma fórmula-testemunha; no ponto fixo, indução sobre uma fórmula mínima mostra que nenhum custo menor foi omitido.
   - O conjunto é finito e os custos são inteiros não negativos, garantindo terminação.

4. **[ALTA] A equivalência AIG-fórmula ↔ fórmula De Morgan preserva o número de portas binárias.**

   Uma fórmula AIG pode ter todas as inversões empurradas até as folhas por De Morgan. Cada AND continua sendo exatamente uma porta AND ou OR, sem criação de nova porta binária. Reciprocamente, cada OR vira um AND com inversões nas arestas e na saída.

   Portanto, o número de ANDs na fórmula AIG é igual ao número de portas binárias na fórmula De Morgan. Para uma árvore binária, portas \(=\) folhas \(-1\).

   Para \(\oplus_3\), tomando \(A=f^{-1}(0)\), \(B=f^{-1}(1)\) e as arestas do cubo entre eles:

   \[
   |A|=|B|=4,\qquad |E|=12.
   \]

   Khrapchenko fornece

   \[
   L(f)\ge \frac{|E|^2}{|A||B|}
   =\frac{144}{16}=9
   \]

   folhas, logo pelo menos 8 portas. A construção explícita tem 10 folhas/9 portas; o DP exclui 8 e prova 9.

5. **[ALTA] \(\operatorname{opt}(\oplus_3)=6\) está solidamente sustentado.**

   Há uma construção de seis portas por dois XORs AIG de três portas encadeados. Reexecutei a instância SAT para cinco portas e obtive `UNSAT`.

   O encoder também parece completo para circuitos mínimos não constantes:

   - exigir operandos distintos não elimina solução mínima: \(u\land u=u\) e \(u\land\bar u=0\);
   - omitir a constante como entrada de portas não elimina circuito mínimo não constante;
   - exigir que toda porta anterior seja usada é válido em um circuito mínimo;
   - proibir portas duplicadas é válido, pois uma duplicata pode ser substituída pela outra;
   - a saída pode ser colocada na última porta por ordenação topológica.

   A construção SAT de seis portas foi simulada em todas as oito entradas. A única ressalva de reprodutibilidade é que o arquivo DRAT original foi apagado; o output preserva apenas o resultado, hash e verificação registrada. Isso não põe o número em dúvida, mas arquivar CNF e DRAT fortaleceria o certificado permanente.

6. **[CRÍTICA] O Corolário 6 é diretamente falso: pode haver \(s=3\).**

   No circuito ótimo:

   \[
   a=x_1\oplus x_2,
   \quad h_0=a\land\bar x_3,
   \quad h_1=\bar a\land x_3,
   \quad f=h_0\lor h_1,
   \]

   o sub-DAG de \(a\) possui três portas e está contido integralmente nos dois sub-DAGs filhos da saída. Portanto:

   \[
   s=|D_{h_0}\cap D_{h_1}|=3.
   \]

   Os dois filhos têm complexidade ótima 4; reexecutei também `UNSAT` em três portas para \(h_0\). Assim:

   \[
   1+\operatorname{opt}(h_0)+\operatorname{opt}(h_1)-s
   =1+4+4-3=6.
   \]

   Isso contradiz diretamente \(s\in\{0,1\}\). Além disso, o “optimal substructure” usado pelo paper não é válido em geral quando o sub-DAG possui portas compartilhadas com outras regiões: substituir apenas um filho não permite necessariamente remover todas as portas antigas.

7. **[ALTA] Há uma ressalva lógica importante sobre o Teorema 7.**

   Sob a definição padrão, \(\oplus_3\) tem gap 3. Logo seu \(s=3\) **não é, sozinho, contraexemplo ao enunciado formal condicional** do Teorema 7, que começa com “gap\((f)=1\)”.

   O que se pode concluir rigorosamente é:

   - a prova do Teorema 7 cai, pois depende do Corolário 6 falso;
   - a afirmação posterior de que o teorema classifica todo compartilhamento em qualquer AIG ótima é falsa;
   - sob a grandeza não padrão efetivamente usada na Tabela 1, a paridade é classificada como “gap 1”; nessa leitura, o mesmo circuito com \(s=3\) contradiz diretamente o Teorema 7.

   Portanto, a alegação de que o Teorema 7 foi **independentemente refutado sob a definição padrão** é forte demais. Ele fica sem prova; já sob o “gap” computado pelo autor, fica diretamente contradito.

8. **[MÉDIA] Os Teoremas 3 e 4 sobrevivem, embora a prova publicada do Teorema 3 tenha uma contagem defeituosa.**

   No Teorema 3, o paper afirma que as portas estritamente abaixo de \(g\), excluindo \(g\), exigem \(k-1\) portas. Isso é falso: se \(g=x_1\land x_2\), há zero portas estritamente abaixo, não uma. Também pode haver interfaces laterais entre o cone de \(g\) e o restante do circuito.

   Contudo, o resultado tem uma prova simples. Seja \(m\) o número de portas de uma AIG ótima útil e \(n\) o número de entradas essenciais. Há \(2m\) incidências de entrada em portas. Cada uma das \(n\) entradas essenciais possui fan-out pelo menos 1; cada uma das \(m-1\) portas não finais possui fan-out pelo menos 1. Se alguma porta é compartilhada, há pelo menos uma incidência adicional:

   \[
   2m\ge n+(m-1)+1=n+m,
   \]

   logo \(m\ge n\). Na verdade isso vale sempre que gap \(>0\), não apenas gap \(=1\).

   O Teorema 4 também sobrevive. Uma AIG reconvergente útil de três portas tem necessariamente

   \[
   g_1\to g_2\to g_3,\qquad g_1\to g_3.
   \]

   Escrevendo \(u\) para uma polaridade de \(g_1\), a saída reduz, conforme as polaridades, a \(0\), \(u\), \(c\land u\) ou \(\bar c\land u\), todos computáveis com no máximo duas portas. Portanto nenhuma função com \(\operatorname{opt}=3\) precisa de compartilhamento.

9. **[CRÍTICA] Nenhuma leitura honesta salva simultaneamente o paper.**

   Pode-se definir uma nova grandeza

   \[
   d(f)=\min\bigl(1+\operatorname{opt}(a)+\operatorname{opt}(b)\bigr).
   \]

   Então \(\operatorname{opt}(f)\le d(f)\le\operatorname{opt}(f)+1\), e o “Unit Gap” vira essencialmente tautológico. Mas \(d\) não é tamanho de fórmula, seus filhos podem ser DAGs, seu ponto fixo não é o Bellman descrito nas seções 3 e 7, e a comparação com a complexidade clássica \(\Theta(n^2)\) da paridade deixa de ser pertinente.

   Resultado final:

   - Teorema 2: **falso** sob a definição publicada de fórmula.
   - Valor exato: \(\operatorname{opt}(\oplus_3)=6\), \(\operatorname{tree}(\oplus_3)=9\), gap \(=3\).
   - Corolário 6: **falso**, com \(s=3\).
   - Teorema 7: prova inválida; diretamente contradito sob o “gap” computado pelo paper, mas não refutado apenas pela paridade sob o gap padrão.
   - Teoremas 3 e 4: **verdadeiros**, embora o Teorema 3 necessite de uma prova corrigida.