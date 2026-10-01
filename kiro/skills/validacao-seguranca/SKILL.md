---
name: validacao-seguranca
description: Checklist e guia detalhado para validar requisitos de SEGURANÇA em qualquer alteração de código, API, banco de dados ou infraestrutura. Use ao escrever, revisar ou modificar código que envolva autenticação, autorização, entrada de usuário, queries SQL, segredos/credenciais, criptografia, dependências, upload de arquivos, chamadas de rede ou endpoints. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request, e antes de concluir qualquer tarefa de desenvolvimento.
---

# Validação de Segurança

Aplique este guia sempre que criar ou alterar código. Cada item é um requisito verificável.

## 1. Segredos e credenciais
- Procure por segredos hardcoded (senhas, API keys, tokens, connection strings, chaves privadas).
- Devem vir de variáveis de ambiente, secret manager (AWS Secrets Manager, Vault) ou cofre.
- Nunca commitar `.env` com valores reais. Sinalize qualquer segredo encontrado.

## 2. Validação de entrada
- Trate toda entrada externa como não confiável (usuário, API, arquivo, fila, header).
- Valide tipo, tamanho, formato e faixa. Rejeite por padrão o que não casa (allowlist > denylist).
- Sanitize antes de renderizar (prevenção XSS) e antes de usar em comandos.

## 3. Injeção
- **SQL**: apenas prepared statements / queries parametrizadas / ORM seguro. Nunca concatenar entrada.
- **Comando/OS**: evite shell com interpolação de entrada; use APIs com arrays de argumentos.
- **Path traversal**: normalize e valide caminhos; nunca use entrada direta para montar paths.
- **Desserialização**: não desserialize dados não confiáveis sem validação.

## 4. AuthN / AuthZ
- Autentique antes de operações sensíveis. Verifique autorização em CADA recurso (deny-by-default).
- Não confie em controles apenas no cliente. Valide no servidor.
- Verifique IDOR: usuário só acessa recursos que lhe pertencem.

## 5. Criptografia e dados sensíveis
- Use algoritmos padrão (AES-GCM, TLS 1.2+, bcrypt/argon2 para senhas). Nunca "criptografia própria".
- TLS em trânsito; criptografia em repouso para dados sensíveis quando aplicável.

## 6. Dependências
- Fixe versões. Prefira pacotes mantidos. Rode auditoria (`npm audit`, `pip-audit`, etc.) quando disponível.
- Sinalize nomes suspeitos (possível typosquatting).

## 7. Tratamento de erros
- Sem stack trace / detalhes internos / segredos para o cliente. Log interno detalhado, resposta genérica.

## 8. Ferramentas úteis (quando instaladas)
- SAST: `semgrep`, `bandit` (Python), `gosec` (Go), `eslint-plugin-security` (JS/TS).
- Segredos: `gitleaks`, `trufflehog`. Dependências: `npm audit`, `pip-audit`, `trivy`.

## Saída esperada
Reporte: itens conformes, violações encontradas (com arquivo/linha), correção aplicada, e riscos
residuais. Se uma violação obrigatória não puder ser corrigida, sinalize e peça decisão do usuário.
