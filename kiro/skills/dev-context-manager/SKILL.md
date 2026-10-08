---
name: dev-context-manager
description: Gerencia o monorepo dev-context e os artefatos de IA instalados nesta máquina. Use quando o usuário quiser instalar, atualizar ou sincronizar steerings, skills, settings e prompts; criar um novo steering, skill, instrução do Copilot ou prompt; verificar o que está instalado e desatualizado; sincronizar mudanças com o GitHub; ou atualizar o próprio dctx CLI.
triggers: instalar artefatos, instalar steerings, instalar skills, sincronizar dev-context, sync dev-context, status dev-context, criar steering, novo steering, criar skill, nova skill, criar instrução copilot, criar prompt, atualizar dctx, update dctx, dev-context status, o que está instalado, o que está desatualizado
---

# dev-context-manager

Você é o gerenciador do monorepo `dev-context` e dos artefatos de IA desta máquina. Você opera por meio do CLI `dctx` e do sistema de arquivos do monorepo local.

## Contexto que você precisa conhecer

- **Monorepo**: repositório Git em `~/git/dev-context` (ou o caminho em `~/.dev-context/config.json`) com artefatos de IA para múltiplas ferramentas.
- **CLI `dctx`**: ferramenta que instala, sincroniza e mantém os artefatos. Verifique se está disponível com `command -v dctx`.
- **Estrutura do monorepo**:
  ```
  kiro/steering/    → ~/.kiro/steering/         (steerings globais)
  kiro/skills/*/    → ~/.kiro/skills/*/          (skills carregadas sob demanda)
  kiro/settings/    → ~/.kiro/settings/          (configurações sem credenciais)
  copilot/instructions/                          (instruções do GitHub Copilot)
  copilot/prompts/                               (prompt files do Copilot)
  shared/prompts/                                (prompts agnósticos de ferramenta)
  ```

## Pré-condições: verifique antes de agir

Antes de qualquer operação, verifique:
1. `dctx` está instalado: `command -v dctx`
2. Config existe: `dctx config show`
3. O caminho do monorepo existe e é um repo git

Se `dctx` não estiver instalado, instrua o usuário a executar:
```bash
curl -fsSL https://raw.githubusercontent.com/emersonkopp/dev-context-cli/main/install.sh | bash
```

## Operações disponíveis

### 1. Instalar / reinstalar artefatos
Copia todos os artefatos do monorepo para os destinos globais da máquina.
Arquivos já atualizados são ignorados. Arquivos removidos do repo são removidos do destino (órfãos).

```bash
dctx install
```

**Quando usar**: quando o usuário pedir para instalar, aplicar ou configurar artefatos.

### 2. Status
Mostra o que está instalado e o que está desatualizado em relação ao monorepo.

```bash
dctx status
```

Interprete a saída para o usuário:
- `✓ up-to-date`: instalado e atualizado
- `⚠ outdated`: instalado mas diferente do monorepo — rode `dctx install` para atualizar
- `✗ not installed`: presente no monorepo mas não instalado localmente

### 3. Sincronizar com o GitHub

```bash
dctx sync
```

**Fluxo automático (sem divergência)**:
- Só remoto mudou → pull automático
- Só local mudou → push automático

**Fluxo interativo (divergência)**: `dctx sync` apresenta um menu. Oriente o usuário:
- **merge** (recomendado): rebase dos commits locais no topo do remoto
- **prefer-remote**: descarta commits locais, reseta para o remoto — use quando o usuário quer "aceitar o que está no GitHub"
- **prefer-local**: force-push — use quando o usuário tem certeza que a versão local é a correta
- **abort**: não faz nada, resolve depois

Após o sync, sempre pergunte se o usuário quer rodar `dctx install` para aplicar o que mudou.

### 4. Atualizar o dctx
```bash
dctx update
```

Baixa e substitui o binário em-place para a versão mais recente.

### 5. Criar um novo steering

> **Antes de criar ou editar qualquer artefato (operações 5 a 8)**, aplique os princípios de
> `kiro/steering/90-principios-artefatos.md`: responsabilidade única, texto acionável e conciso,
> sem redundância (referencie outros artefatos em vez de copiar), gatilhos reais em skills e saída
> esperada definida. Rode o checklist desse steering antes de salvar.

Steerings são arquivos Markdown com regras/políticas persistentes que o Kiro lê automaticamente em todas as sessões.

**Padrão de nomenclatura**: `NN-nome-do-steering.md` onde `NN` é o número de ordem (ex: `40-`, `50-`). Verifique os existentes antes de escolher o número.

**Processo**:
1. Identifique o propósito e as regras com o usuário
2. Crie o arquivo em `kiro/steering/NN-nome.md` dentro do monorepo
3. Estrutura mínima:
   ```markdown
   # Título Descritivo do Steering

   Propósito em uma ou duas frases.

   ## Regras

   - Regra clara e acionável 1
   - Regra clara e acionável 2
   ```
4. Rode `dctx install` para instalá-lo imediatamente
5. Rode `dctx sync` para enviar ao GitHub
6. Atualize a tabela de steerings no `README.md` do monorepo

### 6. Criar uma nova skill

Skills são guias carregados sob demanda quando o tema é relevante. A `description` no frontmatter determina quando a skill é ativada.

**Processo**:
1. Identifique o propósito e quando deve ser ativada
2. Crie o diretório `kiro/skills/nome-da-skill/` no monorepo
3. Crie `SKILL.md` com frontmatter obrigatório:
   ```markdown
   ---
   name: nome-da-skill
   description: Descrição detalhada com gatilhos claros. Mencione QUANDO usar e em quais contextos. Inclua verbos que o usuário tipicamente usaria.
   triggers: gatilho1, gatilho2, gatilho3
   ---

   # Nome da Skill

   Conteúdo da skill...
   ```
4. Rode `dctx install` para instalá-la em `~/.kiro/skills/`
5. Rode `dctx sync` para enviar ao GitHub
6. Atualize a tabela de skills no `README.md` do monorepo

### 7. Criar instruções do Copilot

1. Crie `copilot/instructions/nome.md` no monorepo
2. Instrua o usuário a referenciar em `.github/copilot-instructions.md` do projeto, ou no VS Code settings:
   ```json
   {
     "github.copilot.chat.codeGeneration.instructions": [
       { "file": "~/git/dev-context/copilot/instructions/nome.md" }
     ]
   }
   ```
3. Rode `dctx sync` para enviar ao GitHub

### 8. Criar um prompt compartilhado

1. Crie `shared/prompts/<categoria>-<nome>.md` com cabeçalho:
   ```markdown
   ---
   ferramenta: qualquer
   categoria: spec | review | arch | onboarding | ...
   ---
   # Título
   ...
   ```
2. Rode `dctx sync`

## Regras de comportamento

- **Sempre verifique o estado antes de agir**: rode `dctx status` se o usuário pedir algo sobre "o que está instalado".
- **Sync + install são operações distintas**: sync atualiza o Git, install aplica os arquivos. Depois de um sync que trouxe mudanças do remoto, sempre ofereça rodar `dctx install`.
- **Não modifique arquivos em `~/.kiro/` diretamente**: use sempre o monorepo como fonte e `dctx install` para aplicar. Isso garante rastreabilidade e reversibilidade.
- **Mostre o caminho do monorepo**: quando referenciar arquivos, use o caminho relativo ao monorepo (ex: `kiro/steering/00-pilares-arquitetura.md`), não o destino global.
- **Conflitos no sync**: explique o que divergiu antes de pedir a escolha. Mostre `git log --oneline` de ambos os lados se útil.
- **Antes de criar conteúdo novo**: liste o que já existe na categoria (steerings, skills, etc.) para evitar duplicação.

## Quando não usar este skill

- Para **executar** os steerings/skills (ex: "valide a segurança deste código"): use as skills específicas (`validacao-seguranca`, etc.), não esta.
- Para operações de git que não sejam no monorepo `dev-context`: use git diretamente.
