---
name: validacao-operabilidade-deploy
description: Guia para validar OPERABILIDADE, DEPLOY, RELEASE e CONFIGURAÇÃO em qualquer alteração. Use ao lidar com CI/CD, pipelines, feature flags, rollout gradual (canary/blue-green), rollback, health checks, configuração por ambiente, variáveis de ambiente, secrets por ambiente, containers, infraestrutura como código ou qualquer mudança que afete como o sistema vai para produção. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Operabilidade, Deploy e Configuração

Aplique ao mudar como o sistema é construído, configurado ou implantado.

## 1. Configuração (12-factor)
- Separe código de configuração. Config por ambiente vem de variáveis de ambiente / secret manager,
  não hardcoded. Nunca commitar secrets (conecta ao Pilar de Segurança).
- Paridade dev/staging/prod tão próxima quanto possível. Defaults seguros.

## 2. Deploy e release
- Deploy deve ser reversível: tenha plano de **rollback** claro e rápido.
- Prefira rollout gradual (canary / blue-green) para mudanças de risco.
- Desacople deploy de release quando útil: **feature flags** para ativar/desativar sem redeploy.
- Migração de banco desacoplada do deploy de código (permite rollback independente — ver Dados/Migrações).

## 3. Saúde e prontidão
- Health checks (liveness/readiness) que refletem estado real. Startup/shutdown graciosos.
- Configuração de recursos (CPU/memória/replicas) coerente com a carga (conecta a Eficiência de Infra).

## 4. Pipeline CI/CD
- Build, testes, lint e auditoria de dependências rodando no pipeline. Falha do pipeline bloqueia release.
- Artefatos versionados e reproduzíveis. Pin de versões de base (imagens, runtimes).

## 5. Infra como código
- Mudanças de infra revisáveis e versionadas. Sinalize alterações que afetam recursos vivos/produção
  como alto risco, exigindo revisão e decisão explícita.

## Saída esperada
Reporte: impacto no deploy, existência de rollback/flags, mudanças de config/ambiente, e riscos
operacionais. Sinalize mudanças que afetam produção diretamente para decisão do usuário.
