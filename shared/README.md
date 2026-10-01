# shared/

Artefatos agnósticos de ferramenta — reutilizáveis com Kiro, Copilot, Cursor, Claude ou qualquer outra IA.

## Estrutura

```
shared/
└── prompts/   # Templates de prompts independentes de ferramenta
```

## prompts/

Prompts e templates que funcionam com qualquer modelo ou assistente de IA:

- Templates de feature spec
- Prompts de code review
- Checklists de arquitetura
- Templates de ADR (Architecture Decision Record)
- Roteiros de entrevista técnica

### Convenção de nomenclatura

```
<categoria>-<nome>.md

Exemplos:
  spec-feature-template.md
  review-pull-request.md
  arch-adr-template.md
```

### Cabeçalho recomendado para cada prompt

```markdown
---
ferramenta: qualquer
categoria: spec | review | arch | onboarding | ...
---

# Título do Prompt

**Quando usar:** <contexto de uso>
**Input esperado:** <o que passar como contexto>

---
<corpo do prompt>
```
