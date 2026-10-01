# Kiro Steering: Governança de Requisitos Não Funcionais (RNFs) e IA

Este arquivo atua como um Guia de Contexto Persistente e Guardrail para o Kiro. Sempre que você, Kiro, estiver gerando ou refinando um arquivo `requirements.md` ou `design.md` para uma nova Feature Spec, você DEVE avaliar e aplicar as restrições abaixo.

## 🚨 Guardrails e Regras de Negócio de RNF
1. **Validação de Exageros (Trade-off de Custos):** Se o prompt inicial pedir "máxima segurança", "disponibilidade contínua" ou "infraestrutura infalível", você DEVE interromper o fluxo automático e questionar explicitamente o desenvolvedor/PO no chat sobre o impacto financeiro (ex: custo duplo de computação para RTO próximo a zero).
2. **Formato das Histórias:** Os requisitos de infraestrutura, performance e IA devem ser traduzidos para a notação EARS (Easy Approach to Requirements Syntax) dentro de `requirements.md` (Ex: "WHEN [condição] THE SYSTEM SHALL [ação]").
3. **Isolamento Técnico:** Nenhuma feature de backend ou componente de IA pode ser aceito em `design.md` sem que haja uma estratégia clara de mocks de dados e isolamento técnico que garanta testes automatizados individuais do componente.

## 📋 Questionário de Ativação Dinâmica (Discovery)
Antes de gerar o código da feature e fechar o `requirements.md`, use o chat para garantir que as seguintes premissas de arquitetura e engenharia foram respondidas pelo time:

### 1. Fronteiras de Plataforma
* Se houver canal Mobile/Desktop: Como será tratada a retrocompatibilidade da API para versões antigas instaladas nos aparelhos?
* Se houver Frontend Web: A página exige renderização no servidor (SSR) para SEO ou regras de acessibilidade estritas (WCAG)?

### 2. Volumetria, Desempenho e Resiliência
* Qual é o P95 de tempo de resposta esperado para o fluxo principal desta funcionalidade?
* Toda a infraestrutura necessária para suportar esta feature (novas tabelas, mensageria, buckets) DEVE ser descrita em scripts de Infraestrutura como Código (IaC - ex: Terraform). Configurações manuais de console são proibidas.

### 3. Continuidade e Backup
* Esta funcionalidade armazena ou manipula novos estados/dados críticos de negócio? Se sim, adicione ao `tasks.md` uma tarefa explícita para configurar rotinas automáticas de backup incremental e um plano documentado de restore.
* Caso uma dependência externa falhe, a funcionalidade deve decair graciosamente (Graceful Degradation) sem derrubar o sistema inteiro.

### 4. Inteligência Artificial e Modelos de Linguagem (LLMs)
* **Oportunidades de IA:** Existem pontos específicos nesta funcionalidade/software onde o uso de IA ou LLMs trará valor claro (ex: automação de tarefas, classificação de dados, resumos, chat)?
* **Estratégia do Modelo (Treinamento Especializado):** Esta funcionalidade exige o treinamento/Fine-Tuning de uma LLM especializada com dados proprietários da empresa, ou o uso de técnicas de RAG (Retrieval-Augmented Generation) com APIs de modelos de mercado (OpenAI, Anthropic, Bedrock) é suficiente?
* **Arquitetura de Execução (IA Offline):** É necessário que o recurso de IA funcione de forma 100% offline (ex: rodando modelos menores e otimizados como Llama/Gemma localmente no dispositivo mobile/desktop do usuário)? Se sim, descreva o impacto esperado na memória do dispositivo.

### 5. Métricas e Testabilidade
* Quais tags ou interceptores de Analytics (ex: eventos de funil) devem ser embutidos nesta feature para medir o uso pelo usuário?
* Qual é o plano de Feature Toggles para que possamos testar essa funcionalidade em produção de forma isolada e segura apenas para usuários selecionados?
