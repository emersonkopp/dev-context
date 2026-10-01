# Pilares de Arquitetura — Regras Obrigatórias (Global)

> Este documento é carregado em **todos os projetos** e vale para **qualquer alteração de código,
> configuração ou infraestrutura**. As regras abaixo são requisitos de aceitação, não sugestões.
> Antes de concluir qualquer tarefa que crie ou modifique código, você DEVE validar TODOS os
> pilares e reportar o resultado (checklist ao final).

## Princípio geral

Toda alteração deve ser avaliada contra os pilares de arquitetura: **Segurança**, **Privacidade**,
**Eficiência de Infraestrutura**, **Observabilidade/Confiabilidade**, **Compatibilidade**,
**Testabilidade**, **Manutenibilidade**, **Resiliência**, **Dados e Migrações**, **Operabilidade/
Deploy**, **Documentação/Decisões** e **Acessibilidade/i18n**. Se uma alteração violar um requisito
obrigatório ("DEVE"), você não deve apresentá-la como pronta: corrija antes, ou — se não for
possível — sinalize explicitamente a violação, o risco e peça decisão do usuário.

O foco é **lembrar de todos os pilares em todo trabalho**. Passe por cada um; quando um pilar não
se aplicar à mudança, marque-o como N/A com uma breve justificativa — mas não o ignore.

Ao encontrar a skill correspondente a um pilar (via `skill://`), carregue-a e siga o checklist
detalhado dela. As skills aprofundam cada regra resumida aqui.

## Quando aplicar

Estas regras valem tanto ao **criar/modificar** código quanto ao **revisar** código. Isso inclui:

- Revisão de código de um branch, `git diff`, pull request / merge request, ou trecho colado.
- Auditoria/análise de código existente, mesmo que você não vá alterá-lo.
- Pedidos como "revise", "analise", "faça code review", "o que você acha deste código",
  "avalie este PR/branch".

Em revisões, você DEVE avaliar o código sob todos os pilares, carregar as skills relevantes
(`validacao-seguranca`, `validacao-privacidade`, `validacao-eficiencia-infra`,
`validacao-compatibilidade`, `validacao-testabilidade`, `validacao-manutenibilidade`,
`validacao-resiliencia`, `validacao-dados-migracoes`, `validacao-operabilidade-deploy`,
`validacao-documentacao-decisoes`, `validacao-acessibilidade-i18n`) e reportar achados
organizados por pilar/tema, com arquivo/linha quando possível e severidade. Ao final da revisão,
preencha o mesmo checklist obrigatório — marcando cada item como OK, ⚠️ (achado que precisa de
decisão/correção) ou N/A. Não conclua uma revisão sem passar por todos os itens.

---

## Pilar 1 — Segurança (DEVE)

- Nunca hardcode segredos (senhas, tokens, chaves, connection strings). Use variáveis de
  ambiente, secret managers ou cofres. Sinalize qualquer segredo encontrado no código.
- Toda entrada externa (usuário, rede, arquivo, fila) é não confiável: validar, sanitizar e
  tipar antes de usar.
- Acesso a banco de dados SEMPRE via queries parametrizadas / prepared statements. Nunca
  concatenar strings de entrada em SQL, comandos de shell ou paths.
- Autenticação e autorização devem ser verificadas em cada endpoint/operação sensível. Negar
  por padrão (deny-by-default).
- Dependências: preferir versões fixadas/pinadas e pacotes mantidos. Sinalizar pacotes com
  nome suspeito (typosquatting) ou vulnerabilidades conhecidas.
- Criptografia: usar algoritmos padrão da indústria; nunca implementar criptografia própria.
  Dados sensíveis em trânsito (TLS) e em repouso quando aplicável.
- Erros não devem vazar stack traces, segredos ou detalhes internos para o cliente.

## Pilar 2 — Privacidade (DEVE)

- Minimização: coletar e armazenar apenas o dado pessoal estritamente necessário à função.
- PII (nome, e-mail, CPF/documentos, telefone, geolocalização, dados de saúde/financeiros)
  deve ser identificada, e seu armazenamento/tráfego justificado e protegido.
- Nunca logar PII ou segredos. Mascarar/anonimizar em logs, métricas e mensagens de erro.
- Definir e respeitar retenção de dados; prever mecanismo de exclusão/anonimização.
- Compartilhamento com terceiros exige justificativa explícita; não enviar dados pessoais
  para endpoints externos sem necessidade e consentimento.
- Considerar base legal e finalidade (LGPD/GDPR) ao introduzir novo tratamento de dado pessoal.

## Pilar 3 — Eficiência de Infraestrutura (DEVE)

- **CPU/Processamento**: evitar complexidade desnecessária (ex.: laços aninhados O(n²) em
  caminho quente). Justificar algoritmos caros. Preferir processamento assíncrono/streaming
  para grandes volumes.
- **Memória**: evitar carregar coleções/arquivos inteiros em memória quando paginação ou
  streaming for viável. Cuidado com vazamentos (listeners, buffers, caches sem limite).
- **Banco de dados**: toda query em campo de filtro/junção deve poder usar índice; sinalizar
  full scans. Proibido padrão N+1 — usar batch/join/eager loading. Paginar resultados grandes.
  Usar connection pooling. Evitar `SELECT *` em caminho de produção.
- **Rede/I/O**: minimizar round-trips; usar cache quando o dado permitir; comprimir payloads
  grandes; definir timeouts e retries com backoff.
- **Custo em nuvem**: dimensionar recursos ao uso real; preferir autoescala; evitar recursos
  ociosos. Sinalizar operações potencialmente caras (ex.: varreduras completas, egress alto).

## Pilar 4 — Observabilidade e Confiabilidade (DEVE)

- Logs estruturados e sem PII/segredos nos pontos relevantes (entrada, erro, decisão).
- Erros tratados de forma explícita; nada de "engolir" exceções silenciosamente.
- Operações críticas devem ser idempotentes ou seguras a repetição quando aplicável.
- Falhas externas (rede, DB, dependências) devem ter timeout, tratamento e degradação graciosa.

## Pilar 5 — Compatibilidade e Impacto de Mudanças (DEVE)

- **Contratos**: ao alterar APIs (REST/GraphQL/gRPC), schemas de banco/mensagens, contratos de
  eventos/filas, interfaces/tipos públicos ou formatos de config/arquivo, identifique se a
  mudança é *breaking* (incompatível) e quais consumidores são afetados (blast radius).
- Prefira mudanças aditivas + deprecação faseada (expand/contract) a remoção/renome direto.
  Breaking change = versão major / API versionada; migrações de banco backward-compatible.
- **Dependências externas**: ao adicionar/atualizar/remover pacotes, avalie o tipo de atualização
  (major/minor/patch), leia CHANGELOG buscando breaking changes, verifique CVEs/manutenção do
  pacote, fixe versão (lockfile) e rode build + testes. Sinalize atualizações major.
- **Rode o auditor de dependências** (ex.: `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`,
  `trivy`) ao mexer em dependências e reporte vulnerabilidades por severidade. Rodar o auditor é
  leitura/baixo risco; correção automática que altera versões (ex.: `npm audit fix --force`) deve
  ser tratada como possível breaking change e submetida a decisão do usuário. Se não houver auditor
  instalado, sinalize em vez de pular a checagem.
- Qualquer breaking change ou atualização major DEVE ser sinalizada com o impacto e submetida a
  decisão explícita do usuário — não conclua silenciosamente.

## Pilar 6 — Testabilidade e Qualidade Automatizada (DEVE)

- Caminhos críticos e regras de negócio DEVEM ter testes; todo bug corrigido ganha teste de regressão.
- Respeite a pirâmide (unidade > integração > e2e). Testes determinísticos: sem flakiness.
- Teste comportamento observável, não detalhes de implementação. Use testes de contrato em integrações.
- Rode a suíte relevante e reporte o resultado. Sem framework, adote o padrão do ecossistema.

## Pilar 7 — Manutenibilidade e Qualidade de Design (DEVE)

- Nomes que revelam intenção; funções pequenas e coesas; complexidade sob controle (early-return,
  extração). Baixo acoplamento, alta coesão; dependa de abstrações nas fronteiras.
- Elimine duplicação real (DRY) sem abstração prematura. Siga convenções e libs já usadas no projeto.
- Sinalize dívida técnica introduzida ou encontrada. Não amplie o escopo "limpando" sem necessidade.

## Pilar 8 — Resiliência e Tolerância a Falhas (DEVE)

- Toda chamada externa com timeout; retry com backoff+jitter apenas para erros transitórios e
  operações idempotentes; circuit breaker para dependências instáveis (evite retry-storm).
- Degradação graciosa (fallback/cache) quando dependência não-crítica falha; isole falhas (bulkhead).
- Rate limiting/backpressure e limites de tamanho para evitar exaustão de recursos.
- Concorrência: identifique race conditions/deadlocks; garanta atomicidade e idempotência.
- Graceful shutdown e health checks (liveness/readiness) coerentes com o estado real.

## Pilar 9 — Dados e Migrações (DEVE)

- Integridade via constraints no banco (NOT NULL/UNIQUE/FK/CHECK); tipos/precisão corretos
  (dinheiro em decimal; timestamps com timezone). Transações atômicas e curtas.
- Migrações versionadas, revisáveis e **reversíveis** (com rollback). Mudanças grandes por fases
  (add → backfill → dual write/read → cutover → remover). Backfill em lotes, sem lock longo.
- Consistência forte vs eventual: escolha consciente e documentada. Idempotência de escrita.
- Antes de operação destrutiva/irreversível em dados de produção: exigir backup recente e testado.
  Operação destrutiva em dados DEVE ir a decisão explícita do usuário.

## Pilar 10 — Operabilidade, Deploy e Configuração (DEVE)

- Config separada do código (12-factor): por ambiente, via env/secret manager; nunca secrets no código.
- Deploy reversível com plano de **rollback**; prefira rollout gradual (canary/blue-green) e
  **feature flags**. Migração de banco desacoplada do deploy de código.
- Health checks e startup/shutdown graciosos. Pipeline CI/CD com build, testes, lint e auditoria;
  falha bloqueia release. Pin de versões (imagens/runtimes).
- Mudança que afeta recursos vivos/produção é alto risco: sinalizar e pedir decisão explícita.

## Pilar 11 — Documentação e Decisões de Arquitetura (DEVE)

- Atualize README/doc de API quando setup, execução ou contrato mudam (doc não pode "mentir").
- Decisões arquiteturais relevantes/difíceis de reverter DEVEM ser registradas (ADR): contexto,
  opções, decisão e consequências. Registre o *porquê*.
- Runbooks para componentes críticos. Documente na medida do impacto (evite doc cerimonial).

## Pilar 12 — Acessibilidade e Internacionalização (DEVE, quando há UI/texto de usuário)

- **a11y**: HTML semântico/roles, navegação por teclado com foco visível, textos alternativos e
  labels, contraste (WCAG AA), não depender só de cor. Aplica-se a interfaces de usuário.
- **i18n/l10n**: externalize strings; datas/números/moeda/ordenção sensíveis a locale; tempo em
  UTC convertido na borda; Unicode/UTF-8 fim a fim; layouts que acomodam tamanhos e RTL.
- Se a alteração não tiver UI nem texto de usuário, marque este pilar como N/A com justificativa.

---

## Checklist obrigatório de fechamento

Ao concluir qualquer alteração de código/infra, inclua no resumo um checklist marcando cada item:

- [ ] **Segurança**: sem segredos hardcoded; entradas validadas; DB parametrizado; authz por padrão.
- [ ] **Privacidade**: PII identificada e protegida; sem PII em logs; retenção considerada.
- [ ] **Infra**: complexidade e memória avaliadas; queries indexadas/sem N+1; I/O e custo revisados.
- [ ] **Observabilidade**: logs adequados; erros tratados; falhas externas com timeout/retry.
- [ ] **Compatibilidade**: breaking changes de contrato identificadas; consumidores/blast radius avaliados; ao mexer em dependências, auditor executado (ou ausência sinalizada) e impacto (major/CVE) reportado.
- [ ] **Testabilidade**: caminhos críticos testados; teste de regressão para bugs; suíte executada e reportada.
- [ ] **Manutenibilidade**: legibilidade, complexidade, acoplamento e duplicação avaliados; padrão do projeto seguido; dívida sinalizada.
- [ ] **Resiliência**: chamadas externas com timeout/retry/breaker; degradação graciosa; concorrência e idempotência revisadas.
- [ ] **Dados e Migrações**: integridade/constraints; migração reversível com rollback; risco de perda/corrupção e backup considerados.
- [ ] **Operabilidade/Deploy**: config por ambiente (sem secrets no código); rollback/flags; health checks; impacto em produção sinalizado.
- [ ] **Documentação/Decisões**: README/API atualizados; ADR para decisões relevantes; runbook quando crítico.
- [ ] **Acessibilidade/i18n**: a11y (WCAG) e i18n/l10n avaliados quando há UI/texto de usuário (senão N/A).

Se algum item **não se aplica**, escreva "N/A" e o motivo. Se algum item **falha e não foi
corrigido**, marque como ⚠️, descreva o risco e peça decisão explícita do usuário — não conclua
silenciosamente.
