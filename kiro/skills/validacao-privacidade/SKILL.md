---
name: validacao-privacidade
description: Guia para validar requisitos de PRIVACIDADE e proteção de dados pessoais (LGPD/GDPR) em qualquer alteração. Use ao lidar com dados pessoais (PII) como nome, e-mail, CPF, documentos, telefone, endereço, geolocalização, dados de saúde ou financeiros; ao criar schemas de banco, logs, telemetria, exportações, integrações com terceiros ou qualquer coleta/armazenamento/compartilhamento de dados de usuários. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request que toquem em dados pessoais ou logs.
---

# Validação de Privacidade

Aplique quando a alteração tocar em dados pessoais, logs, telemetria ou integrações externas.

## 1. Identificação de PII
Localize dados pessoais no fluxo: nome, e-mail, CPF/CNPJ, RG, telefone, endereço, IP,
geolocalização, biometria, dados de saúde, dados financeiros/cartão. Marque onde entram,
onde são armazenados e para onde vão.

## 2. Minimização
- Colete e armazene apenas o necessário para a finalidade. Questione campos "por precaução".
- Prefira agregação/anonimização quando o dado individual não for necessário.

## 3. Logs e telemetria
- **Nunca** logar PII ou segredos. Mascare (ex.: `email=j***@***`) ou omita.
- Verifique logs de erro, request/response dumps, métricas e traces — pontos comuns de vazamento.

## 4. Armazenamento e retenção
- Defina por quanto tempo o dado fica e como será excluído/anonimizado.
- Criptografia em repouso para dados sensíveis. Controle de acesso mínimo.

## 5. Compartilhamento com terceiros
- Justifique qualquer envio de dado pessoal para fora do sistema.
- Não transmita PII a endpoints externos/analytics sem necessidade e base legal.

## 6. Base legal e direitos do titular (LGPD/GDPR)
- Novo tratamento de dado pessoal deve ter finalidade e base legal claras.
- Preveja suporte a direitos: acesso, correção, exclusão, portabilidade.

## Nota
Isto é orientação técnica de engenharia de privacidade, não aconselhamento jurídico. Para
decisões de conformidade legal, recomende validação com a área jurídica/DPO.

## Saída esperada
Reporte: PII identificada, medidas aplicadas (mascaramento, minimização, retenção), pontos de
risco e recomendações. Sinalize claramente qualquer novo tratamento de dado pessoal introduzido.
