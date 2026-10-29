# dev-context

Monorepo de artefatos de IA: steerings, settings, prompts, instruções e agentes customizados para múltiplas ferramentas. Serve como fonte da verdade para configurações globais reutilizáveis entre máquinas e projetos.

> O [dctx](https://github.com/emersonkopp/dev-context-cli) instala, sincroniza e mantém
> estes artefatos em cada máquina — documentação e processo no próprio projeto.

## Ferramentas suportadas

| Diretório | Ferramenta |
|---|---|
| `kiro/` | [Kiro](https://kiro.dev) — CLI de IA para desenvolvimento |
| `opencode/` | [OpenCode](https://opencode.ai) — V2 |
| `shared/` | Agnóstico — funciona com qualquer ferramenta |

## Estrutura

```
dev-context/
├── kiro/
│   ├── steering/       # Steerings globais (contexto persistente em todas as sessões)
│   ├── skills/         # Skills globais (carregadas sob demanda por tema)
│   ├── settings/       # Configurações do CLI sem credenciais
│   ├── agents/
│   │   └── custom/     # Definições de agentes customizados
│   └── prompts/        # Templates de prompts específicos do Kiro
├── opencode/
│   ├── skills/         # Skills variantes OpenCode (sobrepõem IDs de kiro/skills)
│   ├── instructions/   # reservado — steerings são reusados de kiro/steering/
│   ├── agents/         # reservado — agentes (*.md + frontmatter) no futuro
│   ├── commands/       # reservado — comandos (prompt templates) no futuro
│   └── config/         # opencode.reference.jsonc — mesclado no config global
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
| `00-pilares-arquitetura.md` | 12 pilares obrigatórios de arquitetura com checklist de fechamento (tabela compacta); cada pilar tem uma skill `validacao-*` de aprofundamento |
| `10-non-functional-requirements.md` | Governança de RNFs: guardrails de custo, formato EARS, isolamento para testes e questionário de discovery |
| `20-testing-policy.md` | TDD: ciclo Red/Green/Refactor, cobertura de edge cases, testes antes do código |
| `30-custo-finops.md` | Pilar de custo (FinOps): estimativa prévia, teto/alertas de orçamento, custo de terceiros/LLM e por transação, tagging de alocação, trade-offs |
| `90-principios-artefatos.md` | Princípios de efetividade e concisão para criar/editar os artefatos deste monorepo (steerings, skills, prompts), com checklist |

### kiro/skills/

Skills do Kiro — guias carregados sob demanda (quando o tema é relevante, via a `description` do
frontmatter). Cada skill é um diretório com um `SKILL.md`. As skills `validacao-*` aprofundam os
pilares de arquitetura; as demais cobrem fluxos específicos (discovery, auto-update, gestão do monorepo).

| Skill | Propósito |
|---|---|
| `discovery` | Elicitação de requisitos (product discovery): perguntas estruturadas que geram um resumo para o `/speckit.specify` |
| `auto-update` | Requisitos de referência para implementar auto-update (Desktop/Mobile): feature toggle, canais stable/beta/alpha, OTA |
| `validacao-seguranca` | Segredos, validação de entrada, injeção, authn/authz, criptografia, dependências |
| `validacao-privacidade` | PII, LGPD/GDPR, minimização, logs sem dado pessoal, retenção |
| `validacao-eficiencia-infra` | CPU, memória, banco (N+1/índices), rede/I/O, custo em nuvem |
| `validacao-compatibilidade` | Breaking changes de contrato + impacto/auditoria de dependências |
| `validacao-testabilidade` | Cobertura, pirâmide de testes, regressão, testes de contrato |
| `validacao-manutenibilidade` | Legibilidade, complexidade, acoplamento, duplicação, dívida técnica |
| `validacao-resiliencia` | Timeout/retry/circuit breaker, concorrência, graceful shutdown |
| `validacao-dados-migracoes` | Integridade, transações, migrações reversíveis, backup/restore |
| `validacao-operabilidade-deploy` | CI/CD, rollback, feature flags, config por ambiente (12-factor) |
| `validacao-documentacao-decisoes` | README, ADRs, runbooks |
| `validacao-acessibilidade-i18n` | Acessibilidade (WCAG) e internacionalização (quando há UI) |
| `revisao-codigo` | Revisão de código comparando branch de origem vs destino: valida requisitos e os pilares de arquitetura, gera relatório de pontos de melhoria com links para o código |
| `dev-context-manager` | Gerencia este monorepo pelo chat: instalar, sincronizar, status e criação de novos artefatos via `dctx` |
| `router-usage` | Mostra as métricas do `ai-router` (uso, taxa de sucesso, tokens estimados economizados, cotas por provedor) via tools MCP |

### kiro/settings/

Configurações do Kiro CLI compartilháveis entre máquinas. **Sem credenciais.**

| Arquivo | Conteúdo |
|---|---|
| `cli.json` | `chat.enableAutoAgentUpgrade: true` |

### kiro/agents/custom/

Definições de agentes customizados. Cada subdiretório é um agente com configuração e instruções próprias.

---

## shared/

Prompts e templates independentes de ferramenta — reutilizáveis com Kiro, Cursor, Claude, etc.

Veja `shared/README.md` para convenções de nomenclatura e estrutura de cabeçalho.

---

## tools/

Projetos de software versionados junto com os artefatos, mas **fora do fluxo de
instalação do dctx**. Ferramentas aqui têm o próprio instalador.

| Ferramenta | Descrição | Instalação |
|---|---|---|
| `kiro-ai-router/` | MCP server local-first que delega tarefas de análise (read-only) a provedores de IA locais/gratuitos (Ollama, Groq, OpenRouter, Gemini API), com roteamento só para provedores configurados, scanner de secrets, salvaguardas de custo e métricas locais. Expõe as tools `delegate_task`, `router_usage`, `router_insights` (ver skill `router-usage`). | `bash tools/kiro-ai-router/scripts/install.sh` |

---

## Setup em uma nova máquina

### Kiro

Instalação e sincronização automáticas: [dctx](https://github.com/emersonkopp/dev-context-cli)
(documentação e processo no próprio projeto).

### Kiro (manual)

```bash
# Clonar
git clone <url-do-repositório> ~/git/dev-context

# Instalar steerings
cp ~/git/dev-context/kiro/steering/*.md ~/.kiro/steering/

# Instalar skills
mkdir -p ~/.kiro/skills
cp -r ~/git/dev-context/kiro/skills/* ~/.kiro/skills/

# Aplicar settings (merge manual se já houver configurações locais)
cp ~/git/dev-context/kiro/settings/cli.json ~/.kiro/settings/cli.json
```

> A via manual não remove artefatos órfãos (renomeados/removidos).

### OpenCode

Instalação e sincronização automáticas: [dctx](https://github.com/emersonkopp/dev-context-cli)
(documentação e processo no próprio projeto).

### OpenCode (manual)

```bash
# Copiar skills variantes
mkdir -p ~/.config/opencode/skills
cp -r ~/git/dev-context/opencode/skills/* ~/.config/opencode/skills/

# Steerings + reuso das skills agnósticas + MCP ai-router:
# mesclar opencode/config/opencode.reference.jsonc em ~/.config/opencode/opencode.json(c)
```

Detalhes de reuso/convenções: `opencode/README.md`.

### Configurações que NÃO estão neste repositório

As seguintes configurações contêm credenciais ou são específicas de cada ambiente:

| Ferramenta | Como configurar |
|---|---|
| Kiro | `kiro login` — token armazenado em `~/.kiro/crew/` |
| AWS | `aws configure` ou variáveis `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| APIs de terceiros | Variáveis de ambiente ou gerenciador de segredos do SO |

---

## Como contribuir

### Adicionar um steering do Kiro

1. Crie `kiro/steering/nome.md`
2. Inclua regras claras e acionáveis com cabeçalho `#` descrevendo o propósito
3. Atualize a tabela acima neste README

### Adicionar uma skill do Kiro

1. Crie `kiro/skills/nome-da-skill/SKILL.md`
2. Inicie o arquivo com frontmatter YAML (`name` e `description`); a `description` deve conter
   gatilhos claros, pois determina quando a skill é carregada sob demanda
3. Atualize a tabela de skills acima neste README

> **Nota:** skills específicas de uma organização/cliente (ex.: contratos internos) **não** devem
> ir para este repositório — mantenha-as apenas localmente em `~/.kiro/skills/`.

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
