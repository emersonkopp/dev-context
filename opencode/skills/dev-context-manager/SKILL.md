---
name: dev-context-manager
description: Gerencia o monorepo dev-context e os artefatos de IA OpenCode instalados nesta máquina. Use quando o usuário quiser instalar, atualizar ou sincronizar steerings, skills, config ou MCP do OpenCode; criar um novo steering, skill ou prompt; verificar o que está instalado e desatualizado; sincronizar mudanças com o GitHub; ou atualizar o próprio dctx CLI.
---

# dev-context-manager (OpenCode)

Gerenciador do monorepo `dev-context` para OpenCode. Opera por meio do CLI
[dctx](https://github.com/emersonkopp/dev-context-cli) e do filesystem do monorepo;
é a variante OpenCode de `kiro/skills/dev-context-manager`. Sintaxe, flags e
comportamento do `dctx` ficam na documentação do próprio projeto — não duplique aqui.

## Contexto de destinos (OpenCode)

- **Monorepo**: repo Git em `~/git/dev-context` (ou o caminho em
  `~/.dev-context/config.json`).
- **Mapeamentos**:
  ```
  kiro/steering/*.md   → instructions globais do OpenCode (glob no config global;
                          fonte única no monorepo — NADA é copiado)
  kiro/skills/*/       → array `skills` aponta o diretório do monorepo (reuso)
  opencode/skills/*/   → ~/.config/opencode/skills/*/    (instaladas pelo dctx)
  opencode/config/opencode.reference.jsonc → mesclado no config global do OpenCode
  (MCP ai-router)      → mcp.servers no config global do OpenCode
  ```
- **`dctx` não instalado** (`command -v dctx` falhou): oriente o usuário a instalar
  seguindo a documentação do [projeto](https://github.com/emersonkopp/dev-context-cli).

## Operações

### 1. Instalar, status, sync e update do ambiente
Mapeie a intenção do usuário ao comando correspondente do `dctx` (`dctx install`,
`dctx status`, `dctx sync`, `dctx update`) e execute. Interprete a saída (`✓/⚠️/✗`)
em português e ofereça a ação seguinte natural (ex.: `⚠ outdated` → reinstalar).
Depois de qualquer sync que traga mudanças, ofereça aplicar (`dctx install`).

### 2. Criar um novo steering
Fonte única para Kiro e OpenCode (o OpenCode lê via `instructions`, sem cópia).
1. Aplique `kiro/steering/90-principios-artefatos.md` antes de salvar; liste
   steerings existentes (evita duplicação).
2. Crie `kiro/steering/NN-nome.md` (`NN` de ordem livre — verifique os existentes).
3. Atualize a tabela de steerings no `README.md` do monorepo.
   O `dctx` sincroniza e registra a entrada `instructions` conforme a doc do projeto.

### 3. Criar uma nova skill
Escolha o namespace: **agnóstica** em `kiro/skills/` (Kiro e OpenCode a consomem);
**específica de OpenCode** (destinos/terminologia alheios a Kiro) em
`opencode/skills/<id>/SKILL.md` (instalada em `~/.config/opencode/skills/` pelo dctx).
1. Aplique `kiro/steering/90-principios-artefatos.md`; liste skills existentes
   (evita duplicação e colisão de ID).
2. Frontmatter obrigatório: `name` (label) e `description` com gatilhos reais —
   o OpenCode ignora `triggers`; coloque os verbos do usuário na `description`.
   Defina a saída esperada no corpo.
3. Atualize as tabelas no `README.md` do monorepo e no `opencode/README.md`.

### 4. Criar um prompt compartilhado
1. Crie `shared/prompts/<categoria>-<nome>.md` com o cabeçalho de `shared/README.md`.
2. Comando OpenCode (`/comando` = `opencode/commands/<nome>.md` com `$ARGUMENTS`)
   só quando houver demanda; documente no `opencode/README.md`.

## Regras de comportamento

- **Estado antes de agir**: rode `dctx status` quando o usuário perguntar o que
  está instalado/desatualizado, antes de decidir a ação.
- **Fonte única**: não edite `~/.config/opencode/` nem artefatos instalados
  diretamente — altere o monorepo; o `dctx` aplica as mudanças.
- **Caminhos do monorepo** ao referenciar artefatos (ex.:
  `kiro/steering/00-pilares-arquitetura.md`), não os destinos globais.
- **Antes de criar conteúdo novo**: liste o que já existe na categoria.
- **Config OpenCode**: mudanças de processo (mescla, órfãos, MCP) são do dctx —
  consulte a doc do projeto; aqui vale apenas o destino final documentado no
  `opencode/config/opencode.reference.jsonc`.

## Quando não usar este skill

- Para **executar validações** (segurança, revisão etc.): use as skills específicas.
- Para git fora do monorepo: use git diretamente.
