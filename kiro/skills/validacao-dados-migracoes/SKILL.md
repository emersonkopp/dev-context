---
name: validacao-dados-migracoes
description: Guia para validar INTEGRIDADE DE DADOS e MIGRAÇÕES em qualquer alteração. Use ao criar/alterar schema de banco, escrever migrações, lidar com transações, consistência (forte vs eventual), integridade referencial, backup/restore, backfill de dados ou qualquer mudança que possa corromper ou perder dados. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Dados e Migrações

Aplique quando a alteração tocar em schema, persistência ou migração de dados.
(Complementa o Pilar de Compatibilidade, que trata da quebra de *contrato* do schema.)

## 1. Integridade dos dados
- Constraints no banco (NOT NULL, UNIQUE, FK, CHECK) como rede de segurança, não só validação na app.
- Integridade referencial: o que acontece com registros dependentes ao deletar/atualizar (cascade?).
- Tipos e precisão adequados (ex.: dinheiro com decimal, não float; timezone em timestamps).

## 2. Transações e consistência
- Agrupe operações que devem ser atômicas em transação. Mantenha transações curtas.
- Escolha consciente entre consistência forte e eventual; documente onde há consistência eventual
  e seus efeitos (ex.: leitura logo após escrita).
- Idempotência de escrita para operações que podem repetir.

## 3. Migrações seguras
- Migrações versionadas, revisáveis e **reversíveis** (com plano de rollback). Evite passos
  destrutivos irreversíveis sem backup e janela de compatibilidade.
- Padrão seguro para mudanças grandes: **add → backfill → dual write/read → cutover → remover antigo**.
- Backfill de grandes volumes: em lotes, fora de horário de pico, sem lock longo de tabela.
- Migração de schema desacoplada do deploy de código (para permitir rollback independente).

## 4. Backup e recuperação
- Antes de mudança destrutiva/irreversível em dados de produção: confirme backup recente e
  **testado** (restore que funciona). Sinalize se não houver.

## 5. Volume e performance
- Avalie impacto de migração/backfill em tabelas grandes (bloqueios, tempo, replicação). Conecta
  ao Pilar de Eficiência de Infra.

## Saída esperada
Reporte: mudanças de schema/dados, se a migração é reversível e tem rollback, riscos de perda/
corrupção, e necessidade de backup. Sinalize operação destrutiva em dados para decisão do usuário.
