---
name: validacao-testabilidade
description: Guia para validar TESTABILIDADE e qualidade automatizada em qualquer alteração. Use ao escrever ou revisar testes, adicionar features, corrigir bugs, avaliar cobertura, testes de unidade/integração/e2e, testes de contrato, mocks/stubs, testes flaky ou pipeline de CI. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Testabilidade e Qualidade Automatizada

Aplique ao adicionar features, corrigir bugs ou revisar código.

## 1. Cobertura significativa
- Caminhos críticos e regras de negócio devem ter testes. Cobertura é meio, não fim: foque em
  comportamento, casos de borda e caminhos de erro — não apenas o caminho feliz.
- Todo bug corrigido ganha um teste de regressão que falha antes e passa depois do fix.

## 2. Pirâmide de testes
- Muitos testes de unidade (rápidos, isolados), menos de integração, poucos e2e.
- Não confie só em e2e: lentos e frágeis. Não teste só unidade: perde integração real.

## 3. Qualidade dos testes
- Determinísticos: sem dependência de relógio real, ordem, rede instável ou dados compartilhados.
  Elimine flakiness (fonte de erosão de confiança).
- Independentes e isoláveis; setup/teardown limpos. Nomes descritivos (o que + condição + esperado).
- Teste comportamento observável, não detalhes de implementação (evita testes quebradiços).

## 4. Testes de contrato (conecta ao Pilar de Compatibilidade)
- Para integrações entre serviços/consumidores, use testes de contrato (ex.: Pact) para detectar
  quebras antes de produção.

## 5. Testabilidade do design
- Código difícil de testar sinaliza acoplamento alto. Prefira injeção de dependência, funções
  puras e efeitos colaterais isolados nas bordas.

## 6. Execução
- Rode a suíte relevante após a alteração e reporte o resultado. Se não houver framework de teste,
  proponha/adote o padrão do ecossistema. Se não for possível rodar, declare o motivo.

## Saída esperada
Reporte: testes adicionados/alterados, o que cobrem, resultado da execução, e lacunas de cobertura
em caminhos críticos que exijam atenção.
