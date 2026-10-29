# Tasks — Port Kiro → OpenCode

> Checklist operacional do plano `docs/plan-port-opencode.md`.
> Regra: **1 fase = 1 commit** (mensagens conventional commits, PT).
> Estado em 2026-10-29: **T0, F0, F1, F2 e F4 concluídas**; **F3 (dctx) pendente**
> (repo externo `dev-context-cli`, PR próprio).

## Tarefa 0 — Remoção Copilot ✅ (commit `4b9d104`)

- [x] `git rm -r copilot/` (README.md, instructions/.gitkeep, prompts/.gitkeep)
- [x] `README.md` raiz: 7 trechos removidos (tabela, árvore, seção `## copilot/`,
      "Copilot" na frase de `shared/`, "Copilot (VS Code)", linha `GitHub Copilot`
      em credenciais, "Adicionar instruções do Copilot")
- [x] `kiro/skills/dev-context-manager/SKILL.md`: description/triggers limpos; mapa
      sem `copilot/`; Operação 7 removida; 8→7; "(operações 5 a 7)"
- [x] `shared/README.md`: "Copilot" fora da enumeração
- [x] Checklist externo anotado no PR: verificar `settings.json` do VS Code local
      (referência manual a `copilot/instructions`)
- [x] Verificação refinada: `git grep -i copilot` = **zero fora de
      `docs/plan-*`/`docs/tasks-*`** (registros históricos do plano)

> Nota de execução: o 1º commit da T0 pegou só os `git rm` (edições de texto
> unstaged); corrigido via `fixup` + rebase — tudo consolidado no `4b9d104`.

## Fase 0 — Spike de validação ✅ (sem mudanças no repo; config local revertida)

- [x] Backup de `~/.config/opencode/opencode.jsonc` (restaurado após testes)
- [x] 0.1 glob `~` em `instructions` → **aprovado**: ao salvar a config, a sessão
      viva injetou os 5 steerings (`~/git/dev-context/kiro/steering/*.md`)
- [x] 0.2 reuso de skills → **aprovado**: skill `validacao-seguranca` carregada via
      tool `skill` com base directory no monorepo
- [x] 0.3 IDs/precedência → **aprovado**: 16 IDs anunciados no `<available_skills>`
- [x] 0.4 fallbacks — **desnecessário** (0.1 ok de primeira)
- [x] Config global restaurada (a sessão corrente reverteu os artefatos ao vivo —
      reversibilidade provada); backup `.spike-backup` removido

**Decisão registrada: estratégia A.** Evidência obtida na própria sessão (recarga de
config), sem necessidade de `opencode run` dedicado.

## Fase 1 — Namespace `opencode/` ✅ (commit `2663ba5`)

- [x] `opencode/README.md`: convenções, tabela de artefatos, reuso, setup, MCP
- [x] `opencode/skills/dev-context-manager/SKILL.md` (variante; original intacto)
- [x] `opencode/skills/router-usage/SKILL.md` (variante; original intacto)
- [x] `opencode/instructions/.gitkeep` (estratégia A → diretório fica reservado)
- [x] `opencode/agents/.gitkeep`, `opencode/commands/.gitkeep`
- [x] Originais `kiro/` intocados (exceto itens da T0)

## Fase 2 — Config de referência + MCP ✅ (commit `7ce4afd`)

- [x] `opencode/config/opencode.reference.jsonc` (`skills` na ordem de
      precedência; `instructions` com glob `~`; `mcp.servers.ai-router` com
      `{env:HOME}` — `~` não é expandido em `command` do OpenCode)
- [x] Setup manual + `opencode mcp add ai-router --global -- …` documentados
      no `opencode/README.md`
- [x] Follow-up registrado: script `configure_opencode.py` em `tools/kiro-ai-router/`
      (separado; não executado neste port)

## Fase 3 — dctx (repo separado `dev-context-cli`, PR próprio) ⏳ pendente

- [ ] Mapping `opencode/skills/*` → `~/.config/opencode/skills/*` + órfãos
- [ ] Estratégia A: manter entradas `instructions` no config global (merge idempotente)
- [ ] Merge das arrays `skills`/`instructions` sem sobrescrever chaves de terceiros
- [ ] `dctx status` com segmento `opencode/` (`✓/⚠️/✗`)
- [ ] Entrada MCP `ai-router` quando o dctx mesclar a config
- [ ] Confirmar ausência de segmento copilot no CLI

**Aceite:** `dctx install` em máquina fresca reproduz a Fase 2 sem edição manual.

## Fase 4 — Verificação + docs finais ✅ (este commit)

- [x] README raiz: `opencode/` na tabela, árvore e seção Setup (via dctx + manual)
- [x] `docs/plan-port-opencode.md`: decisões pendentes preenchidas + log de execução
- [x] Linha de commit da F4 redefinida no próprio doc (mensagem definitiva abaixo)
- [x] Verificação estática concluída (ver matriz parcial abaixo)

**Commit:** `docs: conclui port opencode no monorepo (dctx pendente)`

### Matriz de verificação executável nesta sessão

| Item | Resultado |
|---|---|
| Glob `~` em `instructions` carrega 5 steerings | ✅ F0 (recarga viva da sessão) |
| 16 skills anunciados a partir do monorepo | ✅ F0 |
| Skill agnóstica carrega conteúdo do monorepo | ✅ F0 (`validacao-seguranca`) |
| `git grep -i copilot` zero fora de docs | ✅ |
| Skills variantes listadas em `~/.config/opencode/` | ⏳ pós-F3 (dctx) — hoje manual |
| MCP `ai-router` conectado no OpenCode | ⏳ pós-instalação do router nesta máquina |
| `dctx status` exibe segmento `opencode/` | ⏳ F3 |
