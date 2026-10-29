# Tasks — Port Kiro → OpenCode

> Checklist operacional do plano `docs/plan-port-opencode.md`.
> Regra: **1 fase = 1 commit** (mensagens conventional commits, PT).
> Nenhuma fase inicia sem a anterior estar marcada como concluída
> (exceto F3, dependente só de T0 dentro da F2).

## Tarefa 0 — Remoção Copilot ✅ nenhuma

- [ ] `git rm -r copilot/` (README.md, instructions/.gitkeep, prompts/.gitkeep)
- [ ] `README.md` raiz: remover 6 trechos (tabela de ferramentas; árvore; seção
      `## copilot/`; "Copilot" na frase de `shared/`; "Copilot (VS Code)" no setup;
      linha `GitHub Copilot` em credenciais; "Adicionar instruções do Copilot")
- [ ] `kiro/skills/dev-context-manager/SKILL.md`: description sem "instrução do
      Copilot"; trigger "criar instrução copilot" removido; 2 linhas de `copilot/`
      no mapa; Operação 7 removida; 8→7; "(operações 5 a 8)"→"(operações 5 a 7)"
- [ ] `shared/README.md`: "Copilot" fora da enumeração (linha 3)
- [ ] Checklist externo anotado no commit: verificar `settings.json` do VS Code
      local (referência manual a `copilot/instructions`)
- [ ] Verificação: `git grep -i copilot` = zero resultado

**Commit:** `chore: remove copilot (nunca usado; apenas exemplo)`

## Fase 0 — Spike de validação (sem repo) ✅ nenhuma

- [ ] Backup de `~/.config/opencode/opencode.json`
- [ ] 0.1 glob `~` em `instructions` → modelo cita TDD + EARS
- [ ] 0.2 `skills`: `~/git/dev-context/kiro/skills` → `validacao-seguranca` carrega
- [ ] 0.3 IDs/precedência dos 16 skills sem conflito
- [ ] 0.4 se falhou 0.1: teste path absoluto; persistindo falha → estratégia C
- [ ] Restaurar/limpar config temporária; registrar estratégia eleita

**Commit (docs):** `docs: registra decisão do spike (estratégia steerings)` — só
se houver mudança no plano; spike em si não toca no repo.

## Fase 1 — Namespace `opencode/` ✅ nenhuma

- [ ] `opencode/README.md`: convenções, tabela de artefatos, reuso (skills 14
      agnósticas lidas de `kiro/skills/` via config), setup manual
- [ ] `opencode/skills/dev-context-manager/SKILL.md` (variante; original intacto)
- [ ] `opencode/skills/router-usage/SKILL.md` (variante; original intacto)
- [ ] `opencode/instructions/.gitkeep` (ou conteúdo real se estratégia C)
- [ ] `opencode/agents/.gitkeep`, `opencode/commands/.gitkeep` (vazios por ora)
- [ ] Originais `kiro/` intocados: `git status` confere

**Commit:** `feat(opencode): cria namespace com variantes de skills`

## Fase 2 — Config de referência + MCP ✅ nenhuma

- [ ] `opencode/config/opencode.reference.jsonc` (skills × ordem; instructions
      conforme estratégia eleita; `mcp.servers.ai-router`)
- [ ] Setup manual documentado no `opencode/README.md` (incl.
      `opencode mcp add ai-router --global -- …`)
- [ ] Registro de follow-up: `configure_opencode.py` em `tools/kiro-ai-router/`
      (separado; não executa agora)

**Commit:** `feat(opencode): config de referência e MCP ai-router`

## Fase 3 — dctx (repo separado `dev-context-cli`, PR próprio) ✅ nenhuma

- [ ] Mapping `opencode/skills/*` → `~/.config/opencode/skills/*` + órfãos
- [ ] Estratégia steerings (A: `instructions`; C: concatenação `AGENTS.md`)
- [ ] Merge idempotente nas arrays de `~/.config/opencode/opencode.json`
- [ ] `dctx status` com segmento `opencode/` (`✓/⚠️/✗`)
- [ ] Entrada MCP `ai-router` quando instalador do router detectar OpenCode
- [ ] Confirmar ausência de segmento copilot no CLI

**Aceite:** `dctx install` em máquina fresca reproduz a Fase 2 sem edição manual.

## Fase 4 — Verificação + docs finais ✅ nenhuma

- [ ] Matriz de teste: 16 skills listáveis; TDD/EARS/FinOps citados em sessão
      nova; variantes disparam por gatilho; `dctx status` exibe `opencode`;
      `ai-router` conectado e `router-usage` funcional
- [ ] `README.md` raiz: adicionar apenas linha/árvore/bloco de `opencode/`
- [ ] Nota de decisão (estratégia eleita) em `docs/`
- [ ] `docs/plan-port-opencode.md`: preencher decisões pendentes da seção 6

**Commit:** `docs: port opencode concluído (suprime pendências)`
