---
name: router-usage
description: Mostra as métricas do ai-router (uso, taxa de sucesso, tokens estimados economizados). Use quando o usuário quiser consultar o desempenho do router, estatísticas de delegação, economia de tokens ou cotas por provedor.
triggers: router-usage, métricas do router, ai-router, uso do router, taxa de sucesso, tokens economizados, cota por provedor, router_insights, router_usage, desempenho do router
---

# Métricas do ai-router

Chame as tools `router_insights` e `router_usage` e apresente o resultado em português. NÃO escreva preâmbulo (nada de "vou chamar as tools"); comece direto pelo relatório. NÃO rode shell nem escreva código.

Formato de saída (conciso):

1. **Linha de resumo** (uma linha): total de chamadas, taxa de sucesso (`success_rate`) com ✅ se ≥ 0,9 ou ⚠️ se menor, e `estimated_tokens_offloaded`.

2. **Tabela única por provedor**, consolidando métricas (`by_provider`) e cota do dia (`router_usage`), uma linha por provedor com as colunas:
   `Provedor | Sucessos | Erros | Latência média (s) | Tokens est. | Uso hoje / Limite`
   Combine o `success`/`error` de `by_provider` com os `counts` e `limits` de `router_usage`. Sinalize com ⚠️ qualquer provedor cujo uso do dia esteja ≥ 80% do limite.

3. **Uma linha final de contexto**: lembre que `estimated_tokens_offloaded` é estimativa (~4 chars/token) de trabalho servido por provedores locais/gratuitos em vez da cota paga do Kiro, e que a economia real deve ser confirmada rodando o comando nativo `/usage` do Kiro (a skill não consegue ler o billing do Kiro; execute `/usage` separadamente para comparar).

Mantenha tudo enxuto: no máximo a linha de resumo + a tabela + a linha final. Sem seções extras, sem repetição. Se o usuário passar um foco em $ARGUMENTS (ex.: "só groq"), filtre a tabela. Se as tools não estiverem disponíveis, informe que o servidor MCP `ai-router` precisa estar ativo (reinicie o Kiro CLI a partir do terminal onde as variáveis de ambiente estão visíveis).
