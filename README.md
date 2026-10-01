# dev-context

Monorepo de artefatos de IA do Kiro: steerings, settings, prompts e agentes customizados. Serve como fonte da verdade para configurações globais reutilizáveis entre máquinas e projetos.

## Estrutura

```
dev-context/
├── steering/          # Arquivos de steering global (guardrails e políticas)
├── settings/          # Configurações do Kiro CLI sem credenciais
├── prompts/           # Prompts reutilizáveis e templates
├── agents/
│   └── custom/        # Definições de agentes customizados
└── docs/              # Documentação e guias
```

## Artefatos incluídos

### steering/

Arquivos Markdown que o Kiro lê automaticamente como contexto persistente em todas as sessões. Cada arquivo define um conjunto de regras, guardrails ou políticas para guiar o comportamento da IA.

| Arquivo | Propósito |
|---|---|
| `non-functional-requirements.md` | Governança de RNFs e IA: guardrails de custo, formato EARS, isolamento técnico e questionário de discovery para arquitetura |
| `testing-policy.md` | Diretrizes de TDD: ciclo Red/Green/Refactor, cobertura de edge cases e entrega do artefato de testes antes do código |
| `auto-update-policy.md` | Requisitos do mecanismo de auto-update: feature toggle, canais de distribuição (stable/beta/alpha), comportamento por plataforma (Desktop e Mobile) |

### settings/

Configurações do Kiro CLI que podem ser compartilhadas entre máquinas. **Não contém credenciais** — veja a seção de setup abaixo para configurações que dependem do ambiente local.

| Arquivo | Conteúdo |
|---|---|
| `settings/cli.json` | `chat.enableAutoAgentUpgrade: true` — habilita atualização automática de agentes no chat |

### prompts/

Diretório para templates de prompts reutilizáveis. Adicione aqui prompts de sistema, templates de feature spec, prompts de code review, etc.

### agents/custom/

Definições de agentes customizados do Kiro. Cada subdiretório representa um agente com sua configuração e instruções específicas.

## Setup em uma nova máquina

### 1. Clonar o repositório

```bash
git clone <url-do-repositório> ~/git/dev-context
```

### 2. Instalar os steerings globalmente

Copie os arquivos de steering para o diretório global do Kiro:

```bash
cp ~/git/dev-context/steering/*.md ~/.kiro/steering/
```

### 3. Aplicar as settings do CLI

```bash
cp ~/git/dev-context/settings/cli.json ~/.kiro/settings/cli.json
```

> **Atenção:** Se o seu `~/.kiro/settings/cli.json` já tiver configurações adicionais (ex: credenciais ou tokens), faça um merge manual em vez de sobrescrever.

### 4. Configurações que NÃO estão neste repositório

As seguintes configurações contêm credenciais ou são específicas de cada ambiente e **devem ser configuradas manualmente** em cada máquina:

- **Autenticação do Kiro:** feita via `kiro login` — o token é armazenado em `~/.kiro/crew/` e nunca deve ser versionado.
- **Integrações com AWS:** configure via `aws configure` ou variáveis de ambiente (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`).
- **Chaves de API de terceiros** (OpenAI, Anthropic, etc.): configure via variáveis de ambiente ou no gerenciador de segredos do seu SO.

## Como contribuir

### Adicionar um novo steering

1. Crie o arquivo em `steering/nome-do-steering.md`
2. Use o formato Markdown com cabeçalho `#` descrevendo o propósito
3. Inclua regras claras e acionáveis
4. Atualize a tabela neste README
5. Copie para `~/.kiro/steering/` na sua máquina

### Adicionar um prompt

1. Crie o arquivo em `prompts/` com extensão `.md` ou `.txt`
2. Documente o contexto de uso no cabeçalho do arquivo

### Adicionar um agente customizado

1. Crie um subdiretório em `agents/custom/nome-do-agente/`
2. Inclua um `README.md` descrevendo o propósito e comportamento do agente

## Princípios

- **Sem credenciais no repositório.** Qualquer configuração que precise de chave, token ou senha deve ser gerenciada fora deste repo.
- **Reutilizável entre projetos.** Os artefatos aqui são globais — evite configurações específicas de um projeto.
- **Documentado.** Todo artefato novo deve ter seu propósito documentado aqui ou no próprio arquivo.
