# opencode/

Artefatos para o [OpenCode V2](https://opencode.ai). Fonte da verdade dos artefatos
OpenCode desta máquina, instalados em `~/.config/opencode/`.

## Estrutura

```
opencode/
├── README.md
├── skills/
│   ├── dev-context-manager/SKILL.md   # variante do skill Kiro (destinos OpenCode)
│   └── router-usage/SKILL.md          # variante do skill Kiro (terminologia OpenCode)
├── instructions/                      # reservado — steerings NÃO são copiados (reuso)
├── agents/                            # reservado — agentes (*.md + frontmatter) no futuro
├── commands/                          # reservado — comandos (prompt templates) no futuro
└── config/
    └── opencode.reference.jsonc       # snippet canônico mesclado no config global
```

## Reuso em vez de cópia

| Artefato | Fonte no monorepo | Consumo pelo OpenCode |
|---|---|---|
| Steerings (5) | `kiro/steering/*.md` | `instructions` com glob no config global — nada é copiado |
| Skills agnósticas (14) | `kiro/skills/*/SKILL.md` | array `skills` apontando `~/git/dev-context/kiro/skills` |
| Skills variantes (2) | `opencode/skills/*/SKILL.md` | instaladas em `~/.config/opencode/skills/` (pelo dctx) |
| MCP `ai-router` | `tools/kiro-ai-router/` | `mcp.servers` no config global |

**Variantes sobrepõem originais**: a array `skills` lista `kiro/skills` antes e
`opencode/skills` depois — em ID igual, a fonte posterior vence. Assim
`dev-context-manager` e `router-usage` carregam a versão OpenCode; as 14 agnósticas
seguem de `kiro/skills/` sem duplicação.

## Setup

Automático: [dctx](https://github.com/emersonkopp/dev-context-cli) instala as skills
e mescla a config — documentação e processo no próprio projeto.

Manual: mesclar `config/opencode.reference.jsonc` em `~/.config/opencode/opencode.json(c)`
e copiar `skills/` para `~/.config/opencode/skills/`. Detalhes no cabeçalho do
arquivo de config. Não edite artefatos instalados diretamente — altere o monorepo
e reaplique.

### MCP ai-router

Instale o router (`bash tools/kiro-ai-router/scripts/install.sh`) e registre:

```bash
opencode mcp add ai-router --global -- \
  "$HOME/.local/share/kiro-ai-router/app/.venv/bin/python" -m kiro_ai_router.server
opencode mcp list   # deve exibir "✓ ai-router  connected"
```

No chat, gerencie a conexão em `/mcps`. O `opencode.reference.jsonc` traz o mesmo
server em `mcp.servers` (merge idempotente, sem sobrescrever entradas de terceiros).

## Convenções

- Skill: `skills/<id-kebab-case>/SKILL.md` com frontmatter `name` (label) e
  `description` com gatilhos reais — a `description` decide a carga sob demanda
  (OpenCode ignora `triggers` do Kiro). Defina a saída esperada no corpo.
- Variante OpenCode só muda destinos/terminologia próprios; a regra agnóstica vive
  em `kiro/` ou `shared/` — não duplique.
- Idioma PT. `kiro/steering/90-principios-artefatos.md` se aplica a todo artefato novo.
- Atualize a tabela de skills acima ao criar skill nova.
