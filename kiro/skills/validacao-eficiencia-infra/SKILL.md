---
name: validacao-eficiencia-infra
description: Guia para validar EFICIÊNCIA DE INFRAESTRUTURA e desempenho (uso de CPU/processador, memória, banco de dados, rede, I/O e custo em nuvem) em qualquer alteração. Use ao escrever ou revisar queries SQL, laços/algoritmos, processamento de grandes volumes, uso de cache, chamadas de rede/API, consumo de memória, dimensionamento de recursos cloud ou quando houver preocupação com performance, escalabilidade ou custo. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Eficiência de Infraestrutura

Aplique quando a alteração afetar desempenho, consumo de recursos ou custo.

## 1. CPU / Processamento
- Analise complexidade algorítmica em caminhos quentes. Sinalize O(n²)+ evitável.
- Prefira estruturas de dados adequadas (hash map vs busca linear).
- Para grandes volumes: processamento assíncrono, em lote (batch) ou streaming.

## 2. Memória
- Evite carregar arquivos/coleções inteiros quando streaming/paginação é possível.
- Cuidado com vazamentos: listeners não removidos, caches sem limite/TTL, buffers grandes.
- Libere recursos (conexões, arquivos, streams) — use padrões `with`/`defer`/`try-with-resources`.

## 3. Banco de dados (atenção especial)
- **Índices**: toda coluna usada em WHERE/JOIN/ORDER BY em caminho quente deve poder usar índice.
  Sinalize full table scans.
- **N+1**: proibido. Use JOIN, `IN`, batch ou eager loading em vez de query por item.
- **Paginação**: nunca retorne conjuntos ilimitados. Use LIMIT/OFFSET ou keyset pagination.
- **`SELECT *`**: evite em produção; selecione apenas colunas necessárias.
- **Pooling**: reuse conexões via pool; não abra/feche conexão por operação.
- **Transações**: mantenha curtas; evite lock longo.

## 4. Rede / I/O
- Minimize round-trips (agrupe chamadas). Use cache quando o dado tolerar.
- Defina timeouts e retries com backoff exponencial. Comprima payloads grandes.

## 5. Custo em nuvem
- Dimensione ao uso real; prefira autoescala; elimine recursos ociosos.
- Sinalize operações caras: varreduras completas, egress alto, funções com memória superdimensionada.
- Para estimativas de preço, direcione o usuário às calculadoras oficiais do provedor.

## 6. Ferramentas úteis (quando disponíveis)
- Banco: `EXPLAIN`/`EXPLAIN ANALYZE` para checar plano de execução e uso de índice.
- Perfilagem: profilers da linguagem; testes de carga (k6, Locust) quando aplicável.

## Saída esperada
Reporte: gargalos identificados (CPU/memória/DB/rede), otimizações aplicadas, e trade-offs.
Sinalize riscos de escala/custo que exijam decisão do usuário.
