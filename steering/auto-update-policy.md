# Requisitos de Sistema: Mecanismo de Atualização Automática (Auto-Update)

O sistema deve possuir um módulo centralizado de gerenciamento de atualizações (Auto-Update) unificado para as plataformas Desktop e Mobile, respeitando as restrições nativas de cada sistema operacional.

## 1. Controle e Ativação da Feature
* **Interruptor Geral (Feature Toggle):** O usuário deve ter a opção de ativar ou desativar o recurso de atualizações automáticas através da tela de configurações do aplicativo.
* **Persistência de Preferência:** A escolha do usuário (ativado/desativado) deve ser salva localmente de forma segura e respeitada em cada ciclo de inicialização do app.

## 2. Canais de Distribuição (Release Channels)
O sistema deve suportar múltiplos canais de distribuição para permitir testes graduais de novas versões. O usuário ou o administrador do sistema deve poder selecionar entre os seguintes canais:
* **Canal Estável (Stable):** Versões homologadas e prontas para produção (padrão do sistema).
* **Canal Beta:** Versões em estágio avançado de teste com novos recursos para validação de estabilidade.
* **Canal Alpha / Canary:** Versões de desenvolvimento (Bleeding Edge) para testes internos e feedback rápido.

## 3. Especificidades por Plataforma

### 3.1. Clientes Desktop (Windows, macOS, Linux)
* **Verificação em Segundo Plano:** O app deve checar periodicamente (ex: na inicialização e a cada X horas) a existência de novas tags de versão no servidor correspondentes ao canal selecionado.
* **Download Assíncrono:** O download da nova versão deve ocorrer de forma silenciosa e em segundo plano, sem travar a interface do usuário.
* **Aplicação da Atualização:** Assim que o download terminar, o app deve notificar o usuário discretamente, oferecendo a opção de "Reiniciar para Atualizar" ou aplicar a mudança automaticamente no próximo fechamento do software.

### 3.2. Clientes Mobile (iOS e Android)
* **Delegação para as Lojas Nativas:** Em plataformas mobile, o controle de auto-update físico do binário deve respeitar as diretrizes da Apple App Store (iOS) e Google Play Store (Android).
* **Mapeamento de Canais Mobile:** Para canais Beta/Alpha, o app deve instruir o usuário ou fornecer links direcionados para os programas oficiais de teste das lojas (TestFlight no iOS / Google Play Beta Testing no Android).
* **Atualizações In-App (OTA - Over-The-Air) se aplicável:** Caso o app utilize frameworks híbridos (como React Native, Flutter ou Expo), correções críticas de código (JS/Assets) que não alterem APIs nativas podem ser baixadas via OTA em segundo plano, respeitando as mesmas regras de Canais e Ativação selecionadas pelo usuário.
