---
name: validacao-manutenibilidade
description: Guia para validar MANUTENIBILIDADE e qualidade de design de código em qualquer alteração. Use ao avaliar legibilidade, complexidade, acoplamento, coesão, duplicação, nomes, tamanho de funções/módulos, dívida técnica, aderência a padrões do projeto e princípios SOLID. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request.
---

# Validação de Manutenibilidade e Qualidade de Design

Aplique ao escrever ou revisar código que precisará ser mantido/evoluído.

## 1. Legibilidade e clareza
- Nomes revelam intenção (variáveis, funções, tipos). Evite abreviações obscuras.
- Funções pequenas e com responsabilidade única; evite funções longas e com muitos parâmetros.
- Prefira código explícito a "esperto". Comentários explicam o *porquê*, não o *o quê*.

## 2. Complexidade
- Vigie complexidade ciclomática (muitos if/loop aninhados). Extraia, use early-return, simplifique.
- Sinalize funções/classes que fazem coisas demais (violação de responsabilidade única).

## 3. Acoplamento e coesão
- Baixo acoplamento entre módulos; alta coesão dentro deles. Dependa de abstrações nas fronteiras.
- Evite dependências circulares e vazamento de detalhes de implementação entre camadas.

## 4. Duplicação
- Elimine duplicação real (DRY), mas evite abstração prematura (não force reuso de código que
  apenas parece igual). Regra prática: duplicou 3x, considere extrair.

## 5. Consistência com o projeto
- Siga convenções, estilo, estrutura de pastas e bibliotecas já usadas. Não introduza um novo
  padrão/lib sem justificativa quando já existe um equivalente no projeto.

## 6. Dívida técnica
- Sinalize dívida introduzida ou encontrada (TODOs, workarounds, código morto). Ao corrigir um
  bug, resista a "limpar" tudo em volta sem necessidade — mantenha o escopo, mas registre o débito.

## 7. Ferramentas (quando disponíveis)
- Linters/formatadores do ecossistema; análise estática. SonarQube para métricas de complexidade,
  duplicação, code smells e dívida técnica.

## Saída esperada
Reporte: pontos de complexidade/acoplamento/duplicação, aderência ao padrão do projeto, e
recomendações objetivas (com arquivo/linha em revisões).
