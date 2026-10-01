---
name: validacao-documentacao-decisoes
description: Guia para validar DOCUMENTAÇÃO e registro de DECISÕES DE ARQUITETURA em qualquer alteração. Use ao introduzir decisões arquiteturais relevantes, mudar APIs públicas, adicionar features complexas, criar/atualizar README, documentação de API, ADRs (Architecture Decision Records) ou runbooks operacionais. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Documentação e Decisões de Arquitetura

Aplique quando a mudança for arquiteturalmente relevante ou alterar como outros usam/operam o sistema.

## 1. Documentação de uso
- README/onboarding atualizado quando o setup, execução ou dependências mudam.
- Documentação de API (OpenAPI/GraphQL schema/exemplos) sincronizada com o contrato real.
- Mudanças de comportamento público refletidas na doc (evita doc que mente).

## 2. Decisões de arquitetura (ADR)
- Decisões relevantes e difíceis de reverter devem ser registradas (ADR): contexto, opções
  consideradas, decisão e consequências/trade-offs.
- Prefira registrar o *porquê*. Código mostra o "como"; a decisão precisa do "por quê".

## 3. Runbooks e operação
- Para componentes críticos: como operar, alarmes, o que fazer em incidente comum, como reverter.
  Conecta a Observabilidade e Operabilidade.

## 4. Clareza no próprio código e no PR
- Comentários explicam intenção/decisão, não o óbvio. Descrição de PR resume o quê, por quê e como
  foi testado.

## 5. Proporcionalidade
- Documente na medida do impacto: mudança pequena e local não precisa de ADR; decisão estrutural sim.
  Evite tanto a ausência de doc quanto documentação cerimonial que ninguém mantém.

## Saída esperada
Reporte: o que precisa ser documentado/atualizado, se a decisão merece um ADR, e lacunas de
documentação que dificultariam manutenção ou operação futura.
