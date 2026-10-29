---
name: router-usage
description: Mostra as métricas do ai-router (uso, taxa de sucesso, tokens estimados economizados, cotas por provedor). Use quando o usuário quiser consultar o desempenho do router, estatísticas de delegação, economia de tokens ou cotas por provedor.
---

# Métricas do ai-router

Chame as tools `router_insights` e `router_usage` e apresente o resultado em português.
NÃO escreva preâmbulo (nada de "vou chamar as tools"); comece direto pelo relatório.
NÃO rode shell nem escreva código.

Formato de saída (conciso):

1. **Linha de resumo** (uma linha): total de chamadas, taxa de sucesso (`success_rate`)
   com ✅ se ≥ 0,9 ou ⚠️ se menor, e `estimated_tokens_offloaded`.

2. **Tabela única por provedor**, consolidando métricas (`by_provider`) e cota do dia
   (`router_usage`), uma linha por provedor:
   `Provedor | Sucessos | Erros | Latência média (s) | Tokens est. | Uso hoje / Limite`
   Sinalize com ⚠️ qualquer provedor cujo uso do dia esteja ≥ 80% do limite.

3. **Uma linha final de contexto**: `estimated_tokens_offloaded` é estimativa
   (~4 chars/token) de trabalho servido por provedores locais/gratuitos em vez da
   cota paga da ferramenta principal; a economia real deve ser confirmada nos
   dados de custo/tokens das sessões do OpenCode.

Mantenha enxuto: linha de resumo + tabela + linha final. Sem seções extras. Se o
usuário passar um foco ($ARGUMENTS, ex.: "só groq"), filtre a tabela. Se as tools não
estiverem disponíveis, informe que o server MCP `ai-router` precisa estar ativo:
verifique a conexão em `/mcps` do OpenCode (mudanças de config aplicam sem restart);
se as variáveis de ambiente dos provedores faltarem, rode a partir do terminal onde
eles estão visíveis.
