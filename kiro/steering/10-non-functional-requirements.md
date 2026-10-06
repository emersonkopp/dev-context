# Governança de Requisitos Não Funcionais (RNFs)

Ao gerar ou refinar `requirements.md` ou `design.md` em Feature Specs, aplique estas regras.

## Guardrails

1. **Trade-off de custo**: se o prompt pedir "máxima segurança", "disponibilidade contínua" ou similar, interrompa e questione o impacto financeiro antes de prosseguir.
2. **Formato EARS**: requisitos de infra, performance e IA em `requirements.md` devem usar notação EARS: `WHEN [condição] THE SYSTEM SHALL [ação]`.
3. **Isolamento para testes**: nenhuma feature de backend ou componente de IA aceito em `design.md` sem estratégia de mocks e isolamento que garanta testes automatizados individuais.

## Questionário de discovery

Antes de gerar código e fechar o `requirements.md`, garanta respostas para as questões aplicáveis:

### Plataforma
- Mobile/Desktop: como tratar retrocompatibilidade da API para versões antigas?
- Web: SSR necessário para SEO ou a11y?

### Performance e Infra
- P95 de tempo de resposta esperado para o fluxo principal?
- Toda infra nova (tabelas, filas, buckets) DEVE ser IaC (ex: Terraform). Configuração manual de console é proibida.

### Continuidade
- Dados críticos de negócio? → tarefa explícita para backup incremental + plano de restore.
- Degradação graciosa obrigatória: falha de dependência externa não derruba o sistema.

### IA/LLMs (quando aplicável)
- Onde IA/LLM agrega valor claro nesta feature?
- RAG com APIs de mercado é suficiente ou precisa de fine-tuning com dados proprietários?
- Execução offline necessária (modelo local no dispositivo)? → documentar impacto de memória.

### Métricas e rollout
- Quais eventos de analytics embutir para medir uso?
- Plano de feature toggles para teste isolado em produção?
