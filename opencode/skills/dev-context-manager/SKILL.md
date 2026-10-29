---
name: dev-context-manager
description: Gerencia o monorepo dev-context e os artefatos de IA OpenCode instalados nesta máquina. Use quando o usuário quiser instalar, atualizar ou sincronizar steerings, skills, config ou MCP do OpenCode; criar um novo steering, skill ou prompt; verificar o que está instalado e desatualizado; sincronizar mudanças com o GitHub; ou atualizar o próprio dctx CLI.
---

# dev-context-manager (OpenCode)

Você é o gerenciador do monorepo `dev-context` para OpenCode. Opera via CLI `dctx` e
filesystem do monorepo. Este skill é a variante OpenCode de `kiro/skills/dev-context-manager`
— mesma mecânica do dctx, destinos diferentes.

## Contexto de destinos (OpenCode)

- **Monorepo**: repo Git em `~/git/dev-context` (ou caminho de `~/.dev-context/config.json`).
- **CLI `dctx`**: confere com `command -v dctx` e `dctx config show`.
- **Mapeamentos**:
  ```
  kiro/steering/*.md   → instructions globais (glob no config global do OpenCode;
                          fonte única no monorepo — NADA é copiado)
  kiro/skills/*/       → array `skills` aponta o diretório do monorepo (NADA é copiado)
  opencode/skills/*/   → ~/.config/opencode/skills/*/    (cópia, via dctx)
  opencode/config/opencode.reference.jsonc → mesclado em ~/.config/opencode/opencode.json
  (MCP ai-router)      → mcp.servers no config global do OpenCode
  ```

## Pré-condições: verifique antes de agir

1. `dctx` instalado: `command -v dctx` — senão, instruza:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/emersonkopp/dev-context-cli/main/install.sh | bash
   ```
2. Config existe: `dctx config show`
3. Caminho do monorepo existe e é repo Git.

## Operações

### 1. Instalar / reinstalar artefatos
```bash
dctx install
```
Copia `opencode/skills/` e mescla a config de referência no config global.
Idempotente; remove órfãos (renomeados/removidos do monorepo).

### 2. Status
```bash
dctx status
```
Interprete: `✓ up-to-date` / `⚠ outdated` (rode `dctx install`) / `✗ not installed`.

### 3. Sincronizar com o GitHub
```bash
dctx sync
```
Sem divergência: pull/push automático. Com divergência: menu — oriente o usuário
(**merge** recomendado; `prefer-remote` = reset para o remoto; `prefer-local` =
force-push; `abort`). Após sync com mudanças do remoto, sempre ofereça `dctx install`.

### 4. Atualizar o dctx
```bash
dctx update
```

### 5. Criar um novo steering
Fonte única para Kiro e OpenCode (o OpenCode lê via `instructions`, sem cópia).
1. Aplique `kiro/steering/90-principios-artefatos.md` antes de salvar.
2. Crie `kiro/steering/NN-nome.md` (verifique `NN` existentes antes de escolher).
3. Rode `dctx install` (grava a entrada `instructions`) e `dctx sync`.
4. Atualize as tabelas de steerings no `README.md` do monorepo.

### 6. Criar uma nova skill
Escolha o namespace: **agnóstica** em `kiro/skills/` (Kiro e OpenCode a consomem);
**específica de OpenCode** (destinos/terminologia excluidos de Kiro) em
`opencode/skills/<id>/SKILL.md`.
1. Aplique `kiro/steering/90-principios-artefatos.md`; liste skills existentes
   primeiro (evita duplicação e colisão de ID).
2. Frontmatter obrigatório: `name` (label) e `description` com gatilhos reais —
   o OpenCode ignora `triggers`; coloque os verbos do usuário na `description`.
   Defina a saída esperada no corpo.
3. Rode `dctx install` (copia para `~/.config/opencode/skills/`) e `dctx sync`.
4. Atualize as tabelas de skills no `README.md` do monorepo e do `opencode/README.md`.

### 7. Criar um prompt compartilhado
1. Crie `shared/prompts/<categoria>-<nome>.md` com o cabeçalho de `shared/README.md`.
2. Rode `dctx sync`.
3. Se precisar de comando OpenCode (`/comando`), crie também
   `opencode/commands/<nome>.md` com `$ARGUMENTS` e documente em `opencode/README.md`.

## Regras de comportamento

- **Estado antes de agir**: rode `dctx status` quando o usuário perguntar o que
  está instalado/desatualizado.
- **Sync ≠ install**: sync atualiza o Git; install aplica. Depois de sync com
  mudanças do remoto, ofereça `dctx install`.
- **Não edite `~/.config/opencode/` diretamente**: altere o monorepo e rode
  `dctx install` (rastreabilidade e reversibilidade).
- **Caminhos relativos ao monorepo** ao referenciar artefatos (ex:
  `kiro/steering/00-pilares-arquitetura.md`), não os destinos globais.
- **Conflitos no sync**: explique o que divergiu antes de pedir a escolha;
  mostre `git log --oneline` dos dois lados se útil.

## Quando não usar este skill

- Para **executar validações** (segurança, revisão etc.): use as skills específicas.
- Para git fora do monorepo: use git diretamente.
