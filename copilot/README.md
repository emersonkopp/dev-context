# copilot/

Artefatos para o GitHub Copilot.

## Estrutura

```
copilot/
├── instructions/   # Arquivos de instruções personalizadas do Copilot
└── prompts/        # Prompt files reutilizáveis (.prompt.md)
```

## instructions/

O Copilot suporta instruções customizadas que orientam o comportamento do modelo no repositório ou globalmente.

- **Instruções de repositório:** crie `.github/copilot-instructions.md` no projeto alvo e referencie ou copie o conteúdo de `instructions/`.
- **Instruções globais (VS Code):** configure `github.copilot.chat.codeGeneration.instructions` nas settings do VS Code apontando para os arquivos aqui.

Formato esperado: Markdown com regras diretas e acionáveis, sem cabeçalhos redundantes.

## prompts/

Arquivos `.prompt.md` para uso com Copilot Chat no VS Code (Copilot Edits / `/file`).

### Como usar

```bash
# Copiar instruções para um repositório específico
cp ~/git/dev-context/copilot/instructions/nome.md <repo>/.github/copilot-instructions.md
```

## Setup em uma nova máquina

Instruções globais via VS Code settings (`settings.json`):

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": "~/git/dev-context/copilot/instructions/nome.md" }
  ]
}
```

> **Não versione** tokens de autenticação do Copilot. A autenticação é feita via `gh auth login` e armazenada pelo gerenciador de credenciais do sistema.
