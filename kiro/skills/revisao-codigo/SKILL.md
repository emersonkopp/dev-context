---
name: revisao-codigo
description: Revisa alterações de código comparando um branch de origem (onde está a mudança) com um branch de destino. Use para code review, revisão de PR/MR, revisar branch antes de merge, auditar um diff, ou quando o usuário pedir para revisar/avaliar mudanças de código. Verifica se os requisitos foram atendidos e valida os pilares de arquitetura (00-pilares-arquitetura.md), produzindo um relatório de pontos de melhoria com links para o código relacionado.
triggers: revisar código, code review, revisar branch, revisar PR, revisar MR, revisar pull request, revisar merge request, revisar alterações, revisar diff, auditar diff, comparar branches, revisão antes de merge, avaliar mudanças de código
---

# Revisão de Código (branch origem vs destino)

Revisa as alterações entre um **branch de origem** (contém a mudança) e um **branch de destino**
(onde será mergeado), verifica atendimento aos **requisitos** e aos **pilares de arquitetura**, e
gera um **relatório de pontos de melhoria** com links para o código relacionado.

**Somente revisão.** Esta skill nunca altera código, nunca aplica correções e nunca sugere trechos
de código ou mudanças a serem feitas. Não execute edições, commits, nem proponha patches. A **única**
saída permitida é o relatório descrito no passo 5 — identificando problemas e seu impacto, sem
prescrever a solução. Se o usuário pedir para corrigir, isso é outra tarefa fora desta skill.

## 1. Determinar o escopo da revisão

1. Confirme os branches. Se o usuário não disse, pergunte ou infira:
   - **Origem** (feature/fix) e **destino** (ex: `main`, `develop`).
2. Identifique a base de comparação (merge-base) para revisar só o que mudou no branch de origem:
   ```bash
   git fetch --all --quiet
   BASE=$(git merge-base <destino> <origem>)
   git diff --stat $BASE..<origem>        # panorama dos arquivos
   git diff $BASE..<origem>               # diff completo a revisar
   git log --oneline $BASE..<origem>      # commits da mudança
   ```
   Use `$BASE..<origem>` (não `<destino>..<origem>`) para não incluir commits que o destino ganhou
   em paralelo.
3. Capture o SHA do commit de topo da origem para montar links estáveis:
   ```bash
   git rev-parse <origem>
   git remote get-url origin   # para montar permalinks do forge
   ```

## 2. Levantar os requisitos

Antes de julgar, saiba o que a mudança deveria fazer. Nesta ordem:
1. Requisitos fornecidos pelo usuário no pedido.
2. Specs do repo: `requirements.md`, `design.md`, `tasks.md`, descrição do PR/MR, issues ligadas.
3. Se não houver requisito explícito, infira a intenção pelos commits/diff e **declare essa suposição**
   no relatório (não invente requisitos).

Para cada requisito, classifique: **Atendido**, **Parcial**, **Não atendido** ou **Não verificável**
(com motivo). Aponte o código que o atende ou a lacuna.

## 3. Validar os pilares de arquitetura

Avalie o diff contra `00-pilares-arquitetura.md` (os 12 pilares) e o pilar de custo
`30-custo-finops.md`. Para o checklist aprofundado de cada tema, carregue a skill `validacao-*`
correspondente (ex: `validacao-seguranca`, `validacao-eficiencia-infra`, `validacao-testabilidade`).
Marque cada pilar: ✓ ok, ⚠️ risco (com pedido de decisão), ✗ violação, ou N/A (com motivo).

Priorize achados que o diff realmente introduz; não audite código fora do escopo da mudança.

## 4. Montar os links para o código

Cada ponto de melhoria relacionado a código DEVE ter um link. Use referência relativa à raiz do
repo e, quando houver remote, o permalink com SHA:

- Referência local: `caminho/do/arquivo.ext:LINHA` (ou `:INICIO-FIM` para faixa).
- Permalink (GitHub): `https://github.com/<org>/<repo>/blob/<SHA>/<arquivo>#L<inicio>-L<fim>`
  (GitLab: `/-/blob/<SHA>/<arquivo>#L<inicio>-<fim>`). Derive `<org>/<repo>` do `git remote`.
- Use o SHA do commit revisado (passo 1.3), não o nome do branch, para o link não "escorregar".
- Achado sem local específico (ex: requisito ausente) → marque "sem código relacionado".

## 5. Gerar o relatório

Produza em Markdown, nesta estrutura:

```markdown
# Relatório de Revisão — <origem> → <destino>

Base: <SHA-base>  ·  Topo: <SHA-origem>  ·  Arquivos alterados: N

## Resumo
<2-4 linhas: o que a mudança faz e veredito geral (aprovar / aprovar com ressalvas / bloquear).>

## Requisitos
| Requisito | Status | Evidência / lacuna |
|---|---|---|
| ... | Atendido/Parcial/Não atendido/Não verificável | arquivo:linha ou motivo |

## Pontos de melhoria
Ordenados por severidade (Crítico > Alto > Médio > Baixo).

### [Severidade] Título curto do ponto
- **Pilar**: <pilar/requisito afetado>
- **Local**: [`arquivo.ext:120-128`](<permalink>)
- **Problema**: <o que está errado e qual o impacto>

## Pilares — resumo
| Pilar | Status | Nota |
|---|---|---|
| 1 Segurança | ✓/⚠️/✗/N/A | ... |
| ... | ... | ... |
| Custo (FinOps) | ✓/⚠️/✗/N/A | ... |
```

## Regras de comportamento

- **Severidade honesta.** Crítico = segurança/perda de dados/quebra em produção. Não infle nem minimize.
- **Somente leitura.** Nunca altere, corrija ou proponha código/patches. Descreva o problema e o
  impacto; não prescreva a solução. A entrega é exclusivamente o relatório.
- **Específico.** Cada ponto identifica claramente o problema e seu impacto, com local no código.
- **Baseado em evidência.** Toda afirmação sobre o código vem do diff/arquivos que você leu; não
  presuma comportamento que não verificou — diga o que não deu para verificar.
- **Respeite o escopo.** Revise a mudança, não reescreva o projeto. Dívida pré-existente fora do
  diff entra só como nota de contexto, não como bloqueio.
- **Decisão do usuário.** Riscos ⚠️ e violações que dependem de contexto de negócio → sinalize e peça
  decisão em vez de bloquear unilateralmente.
