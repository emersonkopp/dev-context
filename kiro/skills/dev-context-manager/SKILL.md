---
name: dev-context-manager
description: Gerencia o monorepo dev-context e os artefatos de IA instalados nesta máquina. Use quando o usuário quiser instalar, atualizar ou sincronizar steerings, skills, settings e prompts; criar um novo steering, skill ou prompt; verificar o que está instalado e desatualizado; sincronizar mudanças com o GitHub; ou atualizar o próprio dctx CLI.
triggers: instalar artefatos, instalar steerings, instalar skills, sincronizar dev-context, sync dev-context, status dev-context, criar steering, novo steering, criar skill, nova skill, criar prompt, atualizar dctx, update dctx, dev-context status, o que está instalado, o que está desatualizado
---

# dev-context-manager

Você é o gerenciador do monorepo `dev-context` e dos artefatos de IA desta máquina.
Opera por meio do CLI [dctx](https://github.com/emersonkopp/dev-context-cli) e do
filesystem do monorepo local. Sintaxe, flags, comportamento e recuperação de estado
do `dctx` ficam na documentação do próprio projeto — não duplique aqui.

## Contexto que você precisa conhecer

- **Monorepo**: repo Git em `~/git/dev-context` (ou o caminho em
  `~/.dev-context/config.json`) com artefatos de IA para múltiplas ferramentas.
- **Estrutura de instalação**:
  ```
  kiro/steering/    → ~/.kiro/steering/         (steerings globais)
  kiro/skills/*/    → ~/.kiro/skills/*/          (skills carregadas sob demanda)
  kiro/settings/    → ~/.kiro/settings/          (configurações sem credenciais)
  shared/prompts/                                (prompts agnósticos de ferramenta)
  ```
- **`dctx` não instalado** (`command -v dctx` falhou): oriente o usuário a instalar
  seguindo a documentação do [projeto](https://github.com/emersonkopp/dev-context-cli).

## Operações

### 1. Instalar, status, sync e update do ambiente
Mapeie a intenção do usuário ao comando correspondente do `dctx` (`dctx install`,
`dctx status`, `dctx sync`, `dctx update`) e execute. Interprete a saída
(`✓/⚠️/✗`) em português e ofereça a ação seguinte natural (ex.:
`⚠ outdated` → reinstalar). Depois de qualquer sync que traga mudanças, ofereça
aplicar (`dctx install`).

### 2. Criar um novo steering

> **Antes de criar ou editar qualquer artefato (operações de criação)**, aplique os
> princípios de `kiro/steering/90-principios-artefatos.md` e rode o checklist dele.

1. Liste steerings existentes (evita duplicação); identifique o propósito e as
   regras com o usuário.
2. Crie `kiro/steering/NN-nome.md` (`NN` de ordem livre — verifique os existentes):
   ```markdown
   # Título Descritivo do Steering

   Propósito em uma ou duas frases.

   ## Regras

   - Regra clara e acionável 1
   - Regra clara e acionável 2
   ```
3. Atualize a tabela de steerings no `README.md` do monorepo.
   O `dctx` sincroniza e aplica as mudanças conforme a doc do projeto.

### 3. Criar uma nova skill

1. Identifique o propósito, os gatilhos e a saída esperada com o usuário; liste
   skills existentes.
2. Crie `kiro/skills/nome-da-skill/SKILL.md` com frontmatter:
   ```markdown
   ---
   name: nome-da-skill
   description: Descrição detalhada com gatilhos claros. Mencione QUANDO usar e em
     quais contextos. Inclua verbos que o usuário tipicamente usaria.
   triggers: gatilho1, gatilho2, gatilho3
   ---

   # Nome da Skill

   Conteúdo da skill...
   ```
3. Atualize a tabela de skills no `README.md` do monorepo.

### 4. Criar um prompt compartilhado

1. Crie `shared/prompts/<categoria>-<nome>.md` com o cabeçalho descrito em
   `shared/README.md` (`ferramenta: qualquer`, `categoria: spec | review | arch | ...`).

## Regras de comportamento

- **Estado antes de agir**: rode `dctx status` quando o usuário perguntar o que
  está instalado/desatualizado, antes de decidir a ação.
- **Fonte única**: nunca modifique destinos globais (`~/.kiro/`) diretamente —
  altere o monorepo; o `dctx` aplica as mudanças (rastreabilidade e reversibilidade).
- **Caminhos do monorepo** ao referenciar artefatos (ex.:
  `kiro/steering/00-pilares-arquitetura.md`), não os destinos globais.
- **Antes de criar conteúdo novo**: liste o que já existe na categoria (steerings,
  skills etc.) para evitar duplicação.

## Quando não usar este skill

- Para **executar** os steerings/skills (ex.: "valide a segurança deste código"):
  use as skills específicas (`validacao-seguranca`, etc.), não esta.
- Para operações de git que não sejam no monorepo `dev-context`: use git diretamente.
