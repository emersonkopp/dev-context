# Pilares de Arquitetura — Regras Obrigatórias

Antes de concluir qualquer criação, alteração ou revisão de código/infra, valide todos os pilares abaixo. Violação de regra obrigatória bloqueia a entrega: corrija, ou sinalize o risco e peça decisão do usuário. Pilar não aplicável → marque N/A com justificativa breve.

Cada pilar tem uma skill de validação detalhada (`validacao-*`). Carregue-a quando precisar do checklist completo.

## Aplica-se a

Criação/alteração de código, revisão de código, code review, PR/MR, git diff, auditoria ou análise de código existente. Em revisões, reporte achados por pilar com arquivo/linha e severidade.

## 1 — Segurança

- Sem segredos hardcoded; usar env/secret manager.
- Toda entrada externa: validar, sanitizar, tipar.
- DB via prepared statements; nunca concatenar entrada em SQL/shell/paths.
- AuthN+AuthZ em cada operação sensível; deny-by-default.
- Dependências: versões fixadas, pacotes mantidos, sinalizar typosquatting/CVEs.
- Criptografia padrão da indústria; nunca implementar própria. TLS em trânsito.
- Erros não vazam stack traces, segredos ou internos para o cliente.

## 2 — Privacidade

- Coletar/armazenar apenas PII estritamente necessária; justificar e proteger.
- Nunca logar PII ou segredos; mascarar em logs/métricas/erros.
- Definir retenção; prever exclusão/anonimização.
- Compartilhamento com terceiros exige justificativa e consentimento.
- Considerar base legal (LGPD/GDPR) para novo tratamento de dado pessoal.

## 3 — Eficiência de Infraestrutura

- **CPU**: evitar O(n²) em hot path; preferir async/streaming para grandes volumes.
- **Memória**: paginação/streaming em vez de carregar tudo; cuidar vazamentos.
- **Banco**: queries com índice; sem N+1; paginar resultados; connection pooling; sem `SELECT *` em produção.
- **Rede**: minimizar round-trips; cache; comprimir payloads grandes; timeouts com backoff.
- **Custo cloud**: dimensionar ao uso real; autoescala; sinalizar operações caras.

## 4 — Observabilidade

- Logs estruturados sem PII/segredos nos pontos relevantes.
- Erros tratados explicitamente; nunca engolir exceções.
- Operações críticas idempotentes quando aplicável.
- Falhas externas com timeout, tratamento e degradação graciosa.

## 5 — Compatibilidade

- Identificar se mudança em APIs/schemas/contratos/tipos públicos é breaking; avaliar blast radius.
- Preferir mudanças aditivas + deprecação faseada; breaking → versão major.
- Ao mexer em dependências: checar tipo de update, CHANGELOG, CVEs; fixar versão; rodar build+testes.
- Rodar auditor de dependências (`npm audit`, `pip-audit`, etc.); sinalizar ausência.
- Breaking change ou update major → sinalizar impacto e pedir decisão do usuário.

## 6 — Testabilidade

- Caminhos críticos e regras de negócio com testes; bug corrigido → teste de regressão.
- Pirâmide: unidade > integração > e2e. Testes determinísticos.
- Testar comportamento observável, não implementação. Contratos em integrações.
- Rodar suíte relevante e reportar resultado.

## 7 — Manutenibilidade

- Nomes que revelam intenção; funções pequenas e coesas; complexidade controlada.
- Baixo acoplamento, alta coesão; abstrações nas fronteiras.
- DRY sem abstração prematura. Seguir convenções e libs do projeto.
- Sinalizar dívida técnica; não ampliar escopo sem necessidade.

## 8 — Resiliência

- Chamadas externas com timeout; retry+backoff+jitter só para erros transitórios e ops idempotentes.
- Circuit breaker para dependências instáveis. Degradação graciosa com fallback/cache.
- Rate limiting/backpressure; limites de tamanho.
- Concorrência: atomicidade, idempotência, sem race conditions/deadlocks.
- Graceful shutdown e health checks coerentes.

## 9 — Dados e Migrações

- Constraints no banco (NOT NULL/UNIQUE/FK/CHECK); tipos corretos (decimal p/ dinheiro; timestamp c/ timezone).
- Migrações versionadas, reversíveis, com rollback. Mudanças grandes em fases.
- Consistência forte vs eventual: escolha consciente e documentada.
- Operação destrutiva em produção → exigir backup testado + decisão do usuário.

## 10 — Operabilidade/Deploy

- Config separada do código (12-factor); env/secret manager; sem secrets no código.
- Deploy reversível com rollback; rollout gradual (canary/blue-green); feature flags.
- Health checks; graceful startup/shutdown. CI/CD com build+testes+lint+audit; falha bloqueia.
- Mudança em produção → sinalizar e pedir decisão.

## 11 — Documentação/Decisões

- README/API atualizados quando setup/execução/contrato mudam.
- Decisões arquiteturais relevantes registradas como ADR (contexto, opções, decisão, porquê).
- Runbooks para componentes críticos.

## 12 — Acessibilidade/i18n (quando há UI)

- **a11y**: HTML semântico, navegação por teclado, alt/labels, contraste WCAG AA, não depender só de cor.
- **i18n**: strings externalizadas; datas/números/moeda sensíveis a locale; UTC convertido na borda; UTF-8 fim a fim.
- Sem UI → N/A com justificativa.

---

## Checklist de fechamento

Inclua ao concluir qualquer alteração. Marque ✓, N/A (com motivo) ou ⚠️ (com risco + pedido de decisão):

| # | Pilar | Verificação-chave |
|---|---|---|
| 1 | Segurança | Sem segredos; entradas validadas; DB parametrizado; authz default-deny |
| 2 | Privacidade | PII protegida; sem PII em logs; retenção definida |
| 3 | Infra | Complexidade/memória ok; queries indexadas/sem N+1; custo revisado |
| 4 | Observabilidade | Logs ok; erros tratados; falhas com timeout |
| 5 | Compatibilidade | Breaking changes identificadas; auditor executado; impacto reportado |
| 6 | Testabilidade | Críticos testados; regressão para bugs; suíte executada |
| 7 | Manutenibilidade | Legível; complexidade ok; padrão do projeto seguido |
| 8 | Resiliência | Timeout/retry/breaker; degradação graciosa; concorrência ok |
| 9 | Dados | Constraints ok; migração reversível; backup considerado |
| 10 | Operabilidade | Config por ambiente; rollback; health checks; produção sinalizada |
| 11 | Documentação | Docs atualizados; ADR se relevante |
| 12 | a11y/i18n | WCAG + i18n avaliados (ou N/A) |
