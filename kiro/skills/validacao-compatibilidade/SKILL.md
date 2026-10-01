---
name: validacao-compatibilidade
description: Guia para avaliar IMPACTO E COMPATIBILIDADE de mudanças — quebras de contrato (breaking changes) e riscos de atualização de dependências externas. Use ao alterar APIs (REST/GraphQL/gRPC), schemas de banco ou mensagens, contratos de eventos/filas, interfaces/tipos públicos, formatos de arquivo ou configuração, e ao adicionar, atualizar, remover ou trocar bibliotecas/pacotes/versões (package.json, requirements, go.mod, pom.xml, Cargo.toml, etc.). Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Compatibilidade e Impacto de Mudanças

Aplique quando a alteração puder afetar consumidores existentes ou trazer risco via dependências.

## Parte A — Quebra de contrato (breaking changes)

### 1. Identifique a superfície de contrato afetada
- **APIs**: REST (rotas, métodos, status, formato de request/response), GraphQL (schema),
  gRPC/protobuf (mensagens, campos, numeração).
- **Dados**: schema de banco (colunas, tipos, constraints, migrações), formatos de serialização.
- **Eventos/mensageria**: payloads de tópicos/filas, chaves, versionamento de eventos.
- **Código**: assinaturas de funções/métodos públicos, tipos exportados, SDKs/bibliotecas internas.
- **Config/arquivos**: variáveis de ambiente, formato de arquivos de configuração.

### 2. Classifique a mudança
- **Breaking (incompatível)**: remover/renomear campo ou endpoint; mudar tipo; tornar campo
  opcional em obrigatório; mudar semântica/valor default; endurecer validação; mudar código de
  status/erro; alterar ordem em contrato posicional; remover coluna ainda lida.
- **Não-breaking (compatível)**: adicionar campo opcional; novo endpoint; ampliar aceitação de
  entrada; deprecar sem remover.

### 3. Avalie consumidores e blast radius
- Quem consome esse contrato? (front-ends, outros serviços, jobs, integrações externas, mobile
  com versões antigas em produção). Sinalize consumidores que não conseguem atualizar em conjunto.
- Prefira mudanças aditivas + deprecação faseada a remoção direta.

### 4. Estratégia de compatibilidade
- **Versionamento**: SemVer; breaking = major. Versione APIs (ex.: `/v2`) quando necessário.
- **Expand/contract (migração em fases)**: adicione o novo, migre consumidores, só então remova o antigo.
- **Banco**: migrações backward-compatible; para colunas, siga add → backfill → dual-write/read →
  remover. Evite migração destrutiva sem janela de compatibilidade.
- **Deprecação**: marque como deprecated, comunique, defina prazo, só remova depois.

### 5. Detecção
- Ferramentas quando disponíveis: diff de OpenAPI/Swagger, `buf breaking` (protobuf),
  testes de contrato (Pact), `cargo-semver-checks`, checagem de API pública da linguagem.
- Rode a suíte de testes dos consumidores/integrados quando possível.

## Parte B — Impacto de atualização de dependências

### 1. Natureza da atualização
- Major / minor / patch (SemVer). Major merece atenção especial (breaking esperado).
- Leia CHANGELOG / release notes buscando: breaking changes, mudanças de comportamento default,
  requisitos de runtime (versão de linguagem/SO), remoção de APIs.

### 2. Segurança e cadeia de suprimentos
- A atualização corrige CVE? Introduz dependência transitiva nova/arriscada?
- Pacote é mantido e confiável? Nome correto (sem typosquatting)? Fixe a versão (pin/lockfile).
- **Rode o auditor de dependências** e reporte o resultado sempre que adicionar ou atualizar
  pacotes. Use a ferramenta correspondente ao ecossistema, quando disponível:
  - Node/npm: `npm audit` (ou `pnpm audit` / `yarn audit`)
  - Python: `pip-audit`
  - Rust: `cargo audit`
  - Go: `govulncheck`
  - Multi-ecossistema/containers: `trivy`
  Rodar o auditor é somente leitura (baixo risco) — execute e reporte vulnerabilidades por
  severidade. **Não** rode correção automática que altere versões (ex.: `npm audit fix`,
  sobretudo `--force`) sem avaliar como breaking change (Parte A) e obter decisão do usuário.
  Se nenhum auditor estiver instalado, sinalize isso em vez de omitir a checagem.

### 3. Impacto funcional e de build
- Rode build + testes após atualizar. Verifique deprecações e warnings novos.
- Cheque conflitos de versão / dependências transitivas incompatíveis (dependency hell).
- Avalie efeito em tamanho de bundle, tempo de build e performance quando relevante.

### 4. Reversibilidade
- Garanta que dá para reverter (lockfile versionado). Prefira atualizar de forma incremental,
  não várias majors de uma vez.

## Saída esperada
Reporte: contratos afetados e classificação (breaking/não-breaking); consumidores impactados e
blast radius; estratégia de compatibilidade/migração recomendada; para dependências — tipo de
atualização, breaking changes conhecidas, riscos de segurança e resultado de build/testes.
Sinalize qualquer breaking change ou atualização major que exija decisão explícita do usuário.
