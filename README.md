# dev-context

Monorepo de artefatos de IA: steerings, settings, prompts, instruções e agentes customizados para múltiplas ferramentas. Serve como fonte da verdade para configurações globais reutilizáveis entre máquinas e projetos.

## Ferramentas suportadas

| Diretório | Ferramenta |
|---|---|
| `kiro/` | [Kiro](https://kiro.dev) — CLI de IA para desenvolvimento |
| `copilot/` | [GitHub Copilot](https://github.com/features/copilot) |
| `shared/` | Agnóstico — funciona com qualquer ferramenta |

## Estrutura

```
dev-context/
├── kiro/
│   ├── steering/       # Steerings globais (contexto persistente em todas as sessões)
│   ├── settings/       # Configurações do CLI sem credenciais
│   ├── agents/
│   │   └── custom/     # Definições de agentes customizados
│   └── prompts/        # Templates de prompts específicos do Kiro
├── copilot/
│   ├── instructions/   # Arquivos de instruções personalizadas
│   └── prompts/        # Prompt files (.prompt.md) para Copilot Chat
├── shared/
│   └── prompts/        # Templates agnósticos de ferramenta
└── docs/               # Documentação e guias gerais
```

---

## kiro/

### kiro/steering/

Arquivos Markdown lidos automaticamente pelo Kiro como contexto persistente em todas as sessões. Definem guardrails, políticas e comportamentos esperados.

| Arquivo | Propósito |
|---|---|
| `non-functional-requirements.md` | Governança de RNFs e IA: guardrails de custo, formato EARS, isolamento técnico e questionário de discovery |
| `testing-policy.md` | Diretrizes de TDD: ciclo Red/Green/Refactor, cobertura de edge cases, entrega de testes antes do código |
| `auto-update-policy.md` | Requisitos de auto-update: feature toggle, canais stable/beta/alpha, comportamento por plataforma |

### kiro/settings/

Configurações do Kiro CLI compartilháveis entre máquinas. **Sem credenciais.**

| Arquivo | Conteúdo |
|---|---|
| `cli.json` | `chat.enableAutoAgentUpgrade: true` |

### kiro/agents/custom/

Definições de agentes customizados. Cada subdiretório é um agente com configuração e instruções próprias.

---

## copilot/

Veja `copilot/README.md` para detalhes de uso e convenções.

- **`instructions/`** — instruções personalizadas para referenciar em `.github/copilot-instructions.md` ou via VS Code settings.
- **`prompts/`** — arquivos `.prompt.md` para Copilot Chat.

---

## shared/

Prompts e templates independentes de ferramenta — reutilizáveis com Kiro, Copilot, Cursor, Claude, etc.

Veja `shared/README.md` para convenções de nomenclatura e estrutura de cabeçalho.

---

## Setup em uma nova máquina

### Kiro

```bash
# Clonar
git clone <url-do-repositório> ~/git/dev-context

# Instalar steerings
cp ~/git/dev-context/kiro/steering/*.md ~/.kiro/steering/

# Aplicar settings (merge manual se já houver configurações locais)
cp ~/git/dev-context/kiro/settings/cli.json ~/.kiro/settings/cli.json
```

### Copilot (VS Code)

```bash
# Instruções globais via settings.json do VS Code
# Adicione em ~/.config/Code/User/settings.json (Linux) ou
# ~/Library/Application Support/Code/User/settings.json (macOS):
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": "~/git/dev-context/copilot/instructions/nome.md" }
  ]
}
```

### Configurações que NÃO estão neste repositório

As seguintes configurações contêm credenciais ou são específicas de cada ambiente:

| Ferramenta | Como configurar |
|---|---|
| Kiro | `kiro login` — token armazenado em `~/.kiro/crew/` |
| GitHub Copilot | `gh auth login` — token gerenciado pelo keychain do SO |
| AWS | `aws configure` ou variáveis `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| APIs de terceiros | Variáveis de ambiente ou gerenciador de segredos do SO |

---

## Como contribuir

### Adicionar um steering do Kiro

1. Crie `kiro/steering/nome.md`
2. Inclua regras claras e acionáveis com cabeçalho `#` descrevendo o propósito
3. Atualize a tabela acima neste README
4. Sincronize: `cp kiro/steering/nome.md ~/.kiro/steering/`

### Adicionar instruções do Copilot

1. Crie `copilot/instructions/nome.md`
2. Documente o contexto de uso no cabeçalho
3. Referencie nos projetos via `.github/copilot-instructions.md` ou VS Code settings

### Adicionar um prompt compartilhado

1. Crie `shared/prompts/<categoria>-<nome>.md`
2. Use o cabeçalho YAML descrito em `shared/README.md`

### Adicionar um agente customizado do Kiro

1. Crie `kiro/agents/custom/nome-do-agente/`
2. Inclua `README.md` com propósito e comportamento

### Adicionar suporte a nova ferramenta

1. Crie um diretório raiz com o nome da ferramenta (ex: `cursor/`, `claude/`)
2. Adicione um `README.md` explicando os tipos de artefatos suportados
3. Atualize a tabela "Ferramentas suportadas" neste README

---

## Princípios

- **Sem credenciais no repositório.** Chaves, tokens e senhas são gerenciados fora deste repo.
- **Organizado por ferramenta.** Cada IA tem seu próprio namespace, evitando conflitos de convenção.
- **Reutilizável entre projetos.** Os artefatos são globais — configurações específicas de projeto ficam no próprio projeto.
- **Documentado.** Todo artefato novo deve ter propósito documentado aqui ou no próprio arquivo.
