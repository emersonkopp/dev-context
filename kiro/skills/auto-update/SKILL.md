---
name: auto-update
description: Requisitos de referência para implementar um mecanismo de atualização automática (auto-update) em aplicações Desktop e Mobile. Use ao projetar ou implementar auto-update, release channels (stable/beta/alpha), verificação de versão em background, download e aplicação de updates, ou atualizações OTA em apps híbridos (React Native, Flutter, Expo).
triggers: auto-update, atualização automática, release channel, canal de distribuição, stable beta alpha, update em background, OTA, over-the-air, TestFlight, Google Play Beta, verificar nova versão
---

# Auto-Update: requisitos de referência

Guia para implementar um módulo de atualização automática unificado para Desktop e Mobile, respeitando as restrições de cada plataforma.

## 1. Controle e ativação

- **Feature toggle**: o usuário pode ativar/desativar auto-update nas configurações.
- **Persistência**: a preferência é salva localmente de forma segura e respeitada a cada inicialização.

## 2. Canais de distribuição

- **Stable**: versões homologadas para produção (padrão).
- **Beta**: estágio avançado de teste, novos recursos para validação.
- **Alpha/Canary**: versões de desenvolvimento (bleeding edge) para testes internos.

O usuário ou administrador seleciona o canal.

## 3. Desktop (Windows, macOS, Linux)

- **Verificação em background**: checar novas versões periodicamente (na inicialização e a cada X horas), conforme o canal.
- **Download assíncrono**: baixar em segundo plano, sem travar a UI.
- **Aplicação**: ao terminar, notificar discretamente e oferecer "Reiniciar para Atualizar" ou aplicar no próximo fechamento.

## 4. Mobile (iOS e Android)

- **Lojas nativas**: o auto-update do binário respeita as diretrizes da App Store e Google Play.
- **Canais beta/alpha**: direcionar o usuário aos programas oficiais (TestFlight / Google Play Beta Testing).
- **OTA (apps híbridos — RN/Flutter/Expo)**: correções de JS/assets que não alteram APIs nativas podem ser baixadas via OTA em background, respeitando as regras de canal e ativação.
