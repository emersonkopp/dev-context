# Plano de Port: Kiro → OpenCode

> Status do plano: **aprovado para execução**. Registro criado em
> `feat/port-opencode` antes da execução de qualquer tarefa.
> Checklist operacional em `docs/tasks-port-opencode.md`.

## 1. Objetivo

Adicionar o [OpenCode](https://opencode.ai) (V2) como ferramenta suportada por este
monorepo, portando os artefatos criados para o Kiro **sem modificar os originais**
(exceto o que está explicitamente listado na Tarefa 0), seguindo:

- **(a) Reuso antes de cópia** — OpenCode consome direto do monorepo os artefatos
  agnósticos; cópias/variantes só onde o conteúdo diverge.
- **(b) Validação antes da decisão** — a estratégia de steerings só é fixada após o
  spike (Fase 0).
- **(c) dctx como pré-requisito** — o port só está completo quando
  `dctx install/status` conhecer o namespace `opencode/`.

## 2. Escopo e restrições

- Nada em `shared/` ou `tools/` é modificado.
- `kiro/` e `README.md` raiz só são alterados **nos itens da Tarefa 0** (remoção Copilot).
- Todo artefato novo nasce em `opencode/`.
- Trabalho no repo externo `dev-context-cli` (dctx) é Fase 3, PR próprio.
- Sem credenciais; idioma PT; princípios de `kiro/steering/90-principios-artefatos.md`
  aplicam-se aos novos artefatos.

## 3. Resumo do levantamento (portabilidade)

### 3.1 Mapeamento de conceitos Kiro → OpenCode V2

| Artefato Kiro | Destino OpenCode | Paridade |
|---|---|---|
| Steering (sempre ativo) | `~/.config/opencode/AGENTS.md` ou array `instructions` em `~/.config/opencode/opencode.json` | Alta |
| Skills sob demanda (`SKILL.md` + `description`) | `~/.config/opencode/skills/<id>/SKILL.md` (carrega via tool `skill` pela `description`) | Muito alta |
| Frontmatter `triggers` | Ignorado pelo OpenCode (info já vive na `description`) | N/A |
| Agents customizados | `~/.config/opencode/agents/*.md` (frontmatter + corpo = system prompt) | Formato diferente |
| Prompt templates (`kiro/prompts/`) | Commands: `~/.config/opencode/commands/*.md` (`$ARGUMENTS`) | Formato diferente |
| Settings `kiro/settings/cli.json` | Sem equivalente | Nenhuma |
| MCP (`~/.kiro/settings/mcp.json`) | `mcp.servers` no `opencode.json` / `opencode mcp add <nome> --global` | Protocolo agnóstico |

### 3.2 O que pode ser portado

- **14 de 16 skills quase verbatim**: 11× `validacao-*` + `discovery` + `revisao-codigo`
  + `auto-update` — frontmatter `name`/`description` no formato que o OpenCode consome,
  IDs kebab-case válidos, carregamento sob demanda pela mesma mecânica.
  - Adaptação opcional: mesclar `triggers` na `description` (OpenCode ignora a chave).
- **2 skills exigem variante de conteúdo** (não portáveis verbatim):
  `dev-context-manager` (destinos `~/.kiro/` → `~/.config/opencode/…`) e
  `router-usage` (frases sobre Kiro CLI/`/usage`/billing do Kiro → ambiente OpenCode).
- **5 steerings** → instruções globais sempre ativas; ordenação `NN-` preservada.
  Estratégias: **A** global `instructions` com glob apontando o monorepo; **B** path
  absoluto com glob; **C** concatenar em `~/.config/opencode/AGENTS.md` via dctx.
- **MCP `kiro-ai-router`** — verificado no código: server independente do Kiro CLI
  (HTTP puro: Ollama/Gemini/OpenRouter/Groq). Registrável via
  `opencode mcp add ai-router --global -- <venv>/bin/python -m kiro_ai_router.server`.
  Automação por script (`configure_opencode.py` em `tools/kiro-ai-router/`) fica como
  follow-up (alteraria projeto original).

### 3.3 O que NÃO pode / não se aplica

| Item | Motivo |
|---|---|
| `kiro/settings/cli.json` (`chat.enableAutoAgentUpgrade`) | Específico do Kiro CLI; `~/.config/opencode/cli.json` tem schema distinto (preferência de TUI) |
| Steering com `inclusion: fileMatch`/`on-demand` | OpenCode não tem instruções condicionais por glob; hoje nenhum steering usa esse modo |
| Comparativo de billing do Kiro na skill `router-usage` | Irrecuperável no OpenCode; texto adapta |
| `kiro/agents/custom/` | Vazio; formato (subdir + README) não é nem Kiro nem OpenCode; redefinir quando o 1º agente nascer |
| `kiro/prompts/` | Vazio; futuro destino = commands (cada prompt exigirá wrapper `$ARGUMENTS`) |
| ~~`copilot/`~~ | Removido na Tarefa 0 (nunca usado efetivamente; apenas exemplo) |

## 4. Backlog de fases (ordem de execução)

| # | Fase | Alvo | Esforço |
|---|---|---|---|
| T0 | Remoção Copilot | `copilot/`, `README.md`, `kiro/skills/dev-context-manager/` | S |
| F0 | Spike de validação | config local da máquina (sem repo) | S |
| F1 | Namespace `opencode/` | `opencode/README.md` + 2 skills variantes | M |
| F2 | Config de referência + MCP | `opencode/config/opencode.reference.jsonc` | S |
| F3 | dctx (repo externo) | `dev-context-cli` mappings `opencode/*` | M |
| F4 | Verificação + docs | README raiz (linhas `opencode/`), nota de decisão `docs/` | S |

## 5. Fases detalhadas

### Tarefa 0 — Remoção Copilot

Commit: `chore: remove copilot (nunca usado; apenas exemplo)`

| Alvo | Ação |
|---|---|
| `copilot/` (README.md + 2 .gitkeep) | `git rm -r` |
| `README.md` raiz (6 trechos) | ① linha `copilot/` na tabela "Ferramentas suportadas"; ② entrada na árvore "Estrutura"; ③ seção `## copilot/`; ④ "Copilot" da frase de `shared/`; ⑤ seção "### Copilot (VS Code)" do setup; ⑥ linha `GitHub Copilot | gh auth login` de configurações-credenciais; ⑦ subseção "### Adicionar instruções do Copilot" de "Como contribuir" |
| `kiro/skills/dev-context-manager/SKILL.md` | ① "instrução do Copilot" fora da `description`; ② trigger "criar instrução copilot"; ③ 2 linhas de `copilot/` no mapa de estrutura; ④ Operação 7 inteira ("Criar instruções do Copilot") e renumerar 8→7; ⑤ "(operações 5 a 8)" → "(operações 5 a 7)" |
| `shared/README.md` (decisão) | Remover "Copilot" da enumeração de exemplos (linha 3) |

Atenção: (1) nas máquinas locais, remover referências manuais VS Code
`settings.json` → `{ "file": "~/git/dev-context/copilot/instructions/…" }`
(dctx não instala copilot; não há órfão global gerenciado); (2) confirmar no PR da
F3 que `dctx` nunca teve segmento copilot; (3) histórico preserva `copilot/`.

Aceite: `git grep -i copilot` = zero; `dctx status`/`install` sem órfãos inesperados;
skill dev-context-manager válida (op. renumeradas).

### Fase 0 — Spike de validação (sem tocar no repo)

Objetivo: fixar a estratégia de steerings e provar o reuso de skills.

| # | Teste | Como | Critério |
|---|---|---|---|
| 0.1 | Glob `~` em `instructions` | Config temporária em `~/.config/opencode/opencode.json`: `"instructions": ["~/git/dev-context/kiro/steering/*.md"]`; sessão nova pedindo "cite o ciclo TDD e o formato EARS" | Modelo cita Red/Green/Refactor e `WHEN…THE SYSTEM SHALL…` |
| 0.2 | Reuso de skills | No mesmo arquivo: `"skills": ["~/git/dev-context/kiro/skills"]`; pedir validação de segurança de um trecho | `validacao-seguranca` anunciada e carrega |
| 0.3 | IDs e precedência | Confirmar registro dos 16 IDs, sem quebra | Nenhum conflito |
| 0.4 | Fallbacks | 0.1 falhou → testar path absoluto com glob; ainda falhou → eleger estratégia C (concatenar `NN-*.md` → `~/.config/opencode/AGENTS.md` via dctx) | Estratégia eleita por evidência |

100% reversível (backup do `opencode.json`). Resultado registrado na F4 e neste
plano (seção 6).

### Fase 1 — Namespace `opencode/`

```
opencode/
├── README.md                          # convenções, setup manual, reuso, tabela de artefatos
├── skills/
│   ├── dev-context-manager/SKILL.md   # VARIANTE (destinos/operações OpenCode)
│   └── router-usage/SKILL.md          # VARIANTE (textos Kiro → OpenCode)
├── instructions/                      # só se eleger a estratégia C; senão .gitkeep
├── agents/                            # vazio por ora (*.md c/ frontmatter no futuro)
├── commands/                          # vazio por ora (futuro: kiro/prompts e shared/prompts)
└── config/opencode.reference.jsonc    # Fase 2
```

Variantes:
- `dev-context-manager`: mesma estrutura de operações do dctx (agnóstico); mapa
  `opencode/skills/*/ → ~/.config/opencode/skills/`; steerings via `instructions`/
  `AGENTS.md`; regra "não edite `~/.config/opencode/*` diretamente — use `dctx install`";
  referências de rastreio continuam apontando os caminhos do monorepo.
- `router-usage`: formato de relatório mantido; "reinicie o Kiro CLI" → conferir server
  em `/mcps` (config aplica sem restart); nota de billing do Kiro removida/adaptada.

### Fase 2 — Config de referência + MCP

`opencode/config/opencode.reference.jsonc` (snippet canônico que o dctx mescla em
`~/.config/opencode/opencode.json`; caminho do monorepo resolvido/expandido pelo dctx):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Ordem importa: fontes posteriores ganham em ID igual → variantes OpenCode sobrescrevem
  "skills": [
    "~/git/dev-context/kiro/skills",      // reuso das 14 agnósticas
    "~/git/dev-context/opencode/skills",  // variantes dev-context-manager, router-usage
  ],
  // Estratégia A (se 0.1 aprovado); C = dctx concatena em ~/.config/opencode/AGENTS.md
  "instructions": ["~/git/dev-context/kiro/steering/*.md"],
  "mcp": {
    "servers": {
      "ai-router": {
        "type": "local",
        "command": ["~/.local/share/kiro-ai-router/app/.venv/bin/python", "-m", "kiro_ai_router.server"],
      },
    },
  },
}
```

Setup manual documentado no `opencode/README.md` (incl. `opencode mcp add ai-router
--global -- …`). Política do router (não sobrescrever entrada existente) preservada
quando o registro for por dctx/script. Scripts (`configure_opencode.py`) em
`tools/kiro-ai-router/` = follow-up separado.

### Fase 3 — dctx (repo separado `dev-context-cli`, PR próprio)

| Item | Detalhe |
|---|---|
| Mapping `opencode/skills/<id>/` | Copia por arquivo → `~/.config/opencode/skills/<id>/` + remoção de órfãos (modelo existente) |
| Estratégia steerings | A: garantir entradas `instructions`; C: gerar/atualizar `AGENTS.md` (concatenação `NN-`) e remover conteúdo fora da lista |
| Merge de config JSON | `install` faz merge idempotente nas arrays (`skills`, `instructions`) sem sobrescrever chaves de terceiros |
| `status` | Novo segmento `opencode/` no relatório (`✓/⚠️/✗`) |
| MCP | Entrada `ai-router` quando o instalador do router detectar destino OpenCode |
| Verificação extra | Confirmar que nunca existiu segmento copilot |

Aceite: `dctx install` em máquina fresca reproduz a Fase 2 sem edição manual.

### Fase 4 — Verificação + docs

1. Matriz de teste: 16 skills listáveis (14 reuso + 2 variantes); citação de TDD/
   EARS/FinOps em sessão nova; `dctx status` mostrando segmento `opencode`; variantes
   disparadas pelos gatilhos; `ai-router` conectado e `router-usage` funcional.
2. README raiz: **apenas adicionar** `opencode/` (linha na tabela "Ferramentas
   suportadas", árvore de "Estrutura", bloco "Setup → OpenCode (via dctx)"); remoção
   Copilot já isolada no commit da T0.
3. Nota curta de decisão em `docs/` (estratégia A/B/C eleita) — insumo mínimo rastreável.

## 6. Registro de decisões

| Data | Decisão | Origem |
|---|---|---|
| 2026-10-29 | Port aprovado; artefatos originais intactos, exceto T0 | usuário |
| 2026-10-29 | Copilot removido antes de tudo (nunca usado; exemplo) | usuário |
| 2026-10-29 | Branch de trabalho `feat/port-opencode`; plano/tasks commitados antes da execução | usuário |
| **pendente** | Estratégia steerings A/B/C | F0 |
| **pendente** | Mesclar `triggers` na `description` das variantes | F1 |

## 7. Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Glob `~` em `instructions` diferente do documentado | Re-trabalho F1 | F0 antes de artefatos; fallback C |
| Colisão de ID (variantes vs. originais Kiro via reuso) | Skill errada carrega | Ordem do array `skills` dá vitória às variantes; testes 0.3/F4 |
| Duplicação `kiro/`↔`opencode/` ao evoluir | Divergência de fonte | `90-principios`: variante só muda o próprio de OpenCode; links de rastreio |
| dctx demorar | Setup manual no meio-tempo | F1–F2 entregam uso manual; F3 formaliza |
| Caminho do monorepo variável | Config quebrada por máquina | dctx resolve o caminho real e grava expandido |

## 8. Critérios de conclusão (Definition of Done)

- 16 skills disponíveis no OpenCode (14 reuso + 2 variantes), IDs corretos.
- 5 steerings ativos em sessão nova (estratégia eleita por evidência).
- `ai-router` registrável como MCP; `router-usage` operacional.
- `dctx install/status/sync` cobrindo `opencode/` (ou nota explícita de setup manual).
- `git grep -i copilot` = zero.
- `kiro/`, `shared/`, `tools/` intocados exceto T0; `git status` limpo fora de
  `opencode/`, `docs/`, `README.md`.
