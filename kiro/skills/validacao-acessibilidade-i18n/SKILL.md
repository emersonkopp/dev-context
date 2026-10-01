---
name: validacao-acessibilidade-i18n
description: Guia para validar ACESSIBILIDADE (a11y) e INTERNACIONALIZAÇÃO/LOCALIZAÇÃO (i18n/l10n) em qualquer alteração. Use ao criar ou revisar interfaces de usuário (web, mobile, desktop), componentes visuais, formulários, conteúdo textual voltado ao usuário, ou ao lidar com múltiplos idiomas, fusos horários, moedas, formatos regionais e encoding. Use também em revisões de código (code review), análise de branch, git diff, pull request ou merge request que toquem em UI ou texto de usuário.
---

# Validação de Acessibilidade e Internacionalização

Aplique quando a alteração envolver UI ou conteúdo voltado ao usuário. Se não houver UI nem texto
de usuário, marque como N/A.

## Parte A — Acessibilidade (a11y)
- Semântica: use elementos/roles corretos (HTML semântico, roles ARIA quando necessário).
- Teclado: toda funcionalidade acessível via teclado; foco visível e ordem lógica.
- Leitores de tela: textos alternativos em imagens, labels em campos de formulário, mensagens de
  erro associadas ao campo.
- Contraste e tamanho: contraste suficiente (WCAG AA), não depender só de cor para transmitir informação.
- Componentes dinâmicos: anunciar mudanças relevantes (live regions) sem armadilhas de foco.

## Parte B — Internacionalização (i18n/l10n)
- Externalize strings de UI (nada de texto fixo no código quando há suporte a idiomas).
- Datas, horas, números, moeda e ordenação sensíveis a locale. Armazene tempo em UTC; converta na borda.
- Suporte a Unicode/UTF-8 fim a fim; cuidado com normalização e comparação de strings.
- Layouts que acomodam textos de tamanhos diferentes e, se aplicável, RTL (direita-para-esquerda).
- Evite concatenar frases (dificulta tradução); use interpolação com placeholders e pluralização adequada.

## Saída esperada
Reporte: problemas de a11y (com critério WCAG quando possível) e de i18n encontrados, com
recomendação. Se a alteração não tiver UI/texto de usuário, declare N/A e o motivo.
