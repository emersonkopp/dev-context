# kiro/agents/custom/

Definições de agentes customizados do Kiro. Cada subdiretório representa um agente com sua configuração e instruções específicas.

## Como adicionar um agente

1. Crie um subdiretório com o nome do agente: `agents/custom/nome-do-agente/`
2. Inclua um `README.md` descrevendo propósito, comportamento e gatilhos do agente
3. Adicione os arquivos de configuração do agente (conforme o formato do Kiro)

## Como instalar um agente

```bash
cp -r ~/git/dev-context/kiro/agents/custom/nome-do-agente/ ~/.kiro/agents/
```
