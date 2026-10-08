# Pilar de Custo (FinOps) — Regras Obrigatórias

Pilar dedicado a custo financeiro de criar, operar e escalar o software. Complementa o Pilar 3
(Eficiência de Infra, em `00-pilares-arquitetura.md`), que trata de desempenho/recursos; aqui o
foco é o gasto em dinheiro. Valide antes de concluir qualquer criação/alteração que introduza ou
aumente custo. Violação de regra obrigatória bloqueia a entrega: corrija, ou sinalize o risco e
peça decisão do usuário. Não aplicável → N/A com justificativa.

## Aplica-se a

Novos recursos cloud, filas, buckets, bancos; chamadas a APIs pagas (incluindo LLMs/tokens);
licenças e SaaS; jobs agendados e processamento em lote; qualquer mudança que altere o custo por
transação ou o custo fixo mensal. Também em code review, PR/MR e git diff.

## Regras

- **Estimativa prévia.** Toda infra/serviço pago novo exige estimativa de custo (ordem de grandeza)
  antes de aprovar. Direcione o usuário às calculadoras oficiais do provedor para números finais.
- **Custo por transação/unidade.** Para fluxos de alto volume, estime o custo marginal por
  requisição/registro. Sinalize operações cujo custo cresce linearmente sem teto.
- **Teto e alertas de orçamento.** Recurso que escala com uso deve ter budget/billing alerts e, quando
  possível, limites rígidos (cotas, max tokens, concurrency caps) para evitar surpresa de fatura.
- **APIs de terceiros e LLMs.** Avalie custo por token/chamada; prefira caching, batching e o menor
  modelo que atenda. Sinalize chamadas de LLM em loop ou sem limite de tokens.
- **Elimine ocioso.** Nada de recursos superdimensionados ou ligados sem uso (ambientes efêmeros,
  autoescala para zero, TTL em dados temporários). Sinalize over-provisioning.
- **Tagging/alocação.** Recursos novos devem ter tags de alocação de custo (projeto/ambiente/owner)
  quando o provedor suportar, para rastreabilidade de gasto.
- **Trade-off explícito.** Pedido de "máxima disponibilidade/segurança/performance" tem custo:
  explicite o impacto financeiro e peça decisão (reforça o guardrail de RNFs em
  `10-non-functional-requirements.md`).
- **Dado destrutivo barato ≠ seguro.** Não reduza custo às custas de backup/retenção exigidos; custo
  cede a segurança, privacidade e dados.

## Saída esperada

Em criação/alteração: estimativa de custo (quando aplicável), teto/alerta definido ou proposto, e
riscos de custo sinalizados para decisão. Em revisão: achados de custo por arquivo/linha com
severidade e sugestão de mitigação.
