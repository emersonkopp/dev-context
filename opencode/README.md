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
| Skills variantes (2) | `opencode/skills/*/SKILL.md` | copiadas para `~/.config/opencode/skills/` via `dctx install` |
| MCP `ai-router` | `tools/kiro-ai-router/` | `mcp.servers` no config global |

**Variantes sobrepõem originais**: a array `skills` lista `kiro/skills` antes e
`opencode/skills` depois — em ID igual, a fonte posterior vence. Assim
`dev-context-manager` e `router-usage` carregam a versão OpenCode; as 14 agnósticas
seguem de `kiro/skills/` sem duplicação.

## Setup

Recomendado: `dctx install` (aplica skills e mescla config) e `dctx status`.

Manual: mesclar `config/opencode.reference.jsonc` em `~/.config/opencode/opencode.json(c)`
e copiar `skills/` para `~/.config/opencode/skills/`. Detalhes no cabeçalho do
arquivo de config. Não edite artefatos instalados diretamente — altere o monorepo
e reaplique.

## Convenções

- Skill: `skills/<id-kebab-case>/SKILL.md` com frontmatter `name` (label) e
  `description` com gatilhos reais — a `description` decide a carga sob demanda
  (OpenCode ignora `triggers` do Kiro). Defina a saída esperada no corpo.
- Variante OpenCode só muda destinos/terminologia próprios; a regra agnóstica vive
  em `kiro/` ou `shared/` — não duplique.
- Idioma PT. `kiro/steering/90-principios-artefatos.md` se aplica a todo artefato novo.
- Atualize a tabela de skills acima ao criar skill nova.
