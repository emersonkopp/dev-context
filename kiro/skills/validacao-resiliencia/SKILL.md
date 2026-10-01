---
name: validacao-resiliencia
description: Guia para validar RESILIÊNCIA e tolerância a falhas em qualquer alteração. Use ao lidar com chamadas a serviços externos/dependências, timeouts, retries, circuit breaker, rate limiting, filas, concorrência, estado compartilhado, degradação graciosa, graceful shutdown ou comportamento sob falha. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Resiliência e Tolerância a Falhas

Aplique quando a alteração envolver dependências externas, concorrência ou caminhos que podem falhar.

## 1. Falhas de dependências
- Toda chamada externa (rede, DB, API, fila) precisa de **timeout** explícito.
- **Retry** com backoff exponencial + jitter, apenas para erros transitórios e operações idempotentes.
- **Circuit breaker** para dependências instáveis; evite retry-storm que amplifica a falha.

## 2. Degradação graciosa
- O que acontece quando uma dependência não-crítica cai? Prefira degradar (fallback, cache, valor
  padrão) a derrubar o sistema todo. Isole falhas (bulkhead) para não propagar.

## 3. Limites e proteção
- Rate limiting / throttling para proteger recursos. Backpressure quando o consumo excede a capacidade.
- Defina limites de tamanho (payloads, filas, buffers) para evitar exaustão de recursos.

## 4. Concorrência e estado compartilhado
- Identifique race conditions, deadlocks e acessos não sincronizados a estado compartilhado.
- Garanta atomicidade onde necessário; prefira imutabilidade e isolamento de estado.

## 5. Idempotência e consistência
- Operações que podem ser repetidas (retry, redelivery de fila) devem ser idempotentes.
- Considere entrega at-least-once e efeitos de duplicação em mensageria.

## 6. Ciclo de vida
- Graceful shutdown: drene requisições/mensagens em andamento antes de encerrar.
- Health checks (liveness/readiness) refletindo o estado real do serviço.

## Saída esperada
Reporte: caminhos de falha cobertos (timeout/retry/breaker/fallback), riscos de concorrência,
e pontos onde a falha de uma dependência ainda derruba o sistema (com recomendação).
