# ADR 0001 — Provedores, segurança e observabilidade do router

Data: 2026-10-09
Status: Aceito

## Contexto

O kiro-ai-router delega tarefas de análise (code/tests/review/docs/general) a provedores
de IA, priorizando execução local. Durante auditoria de segurança e configuração das
integrações, foram tomadas decisões sobre quais provedores habilitar, como reduzir a
superfície de ataque e como medir o uso sem introduzir custo.

## Decisões

### 1. Gemini CLI desabilitado das rotas
O Gemini CLI é um **agente autônomo** executado como subprocesso local com acesso a
filesystem/rede; `cwd=tempdir` não é sandbox. Risco de severidade média (prompt-injection
no `context` podendo induzir ações locais). O adaptador foi mantido no código, mas com
`env` reduzido a allowlist e **removido de todas as rotas**. Reabilitar só atrás de
isolamento real (container / `sandbox-exec`). Para usar Gemini com segurança, preferir a
*API* do Google AI Studio (HTTP puro), não o CLI.

### 2. Groq adicionado como provedor de nuvem (free tier)
API HTTP OpenAI-compatível, **sem execução local** — superfície muito menor que o Gemini CLI.
Mesmo padrão seguro do adaptador OpenRouter: `trust_env=False`, timeout, `max_tokens=768`,
acesso defensivo à resposta, credencial via env (`GROQ_API_KEY`), modelo via `GROQ_MODEL`.
Salvaguarda de custo opcional `GROQ_ALLOWED_MODELS` (fail-closed antes de qualquer rede).
Ordem de rota: `ollama → groq → openrouter`.

### 3. Observabilidade local sem custo (`router_insights`)
Nova tool MCP que agrega **apenas o SQLite local** (sem rede, sem serviço pago, sem tokenizer).
Schema estendido de forma retrocompatível com `prompt_chars`/`response_chars` (migração
idempotente). Reporta total de chamadas, taxa de sucesso, latência média por provedor e
`estimated_tokens_offloaded` (~4 chars/token) — estimativa de trabalho servido por
provedores locais/gratuitos em vez da cota paga do Kiro. É estimativa, não fonte de
faturamento; comparar com Kiro `/usage` para economia real.

### 4. Hardening de segurança transversal (resumo)
Env mínimo em allowlist no subprocesso Gemini; scanner de secrets ampliado + heurística de
entropia; validação de tipos/limites na config (`cloud_enabled` booleano, URL Ollama
loopback, inteiros com teto); validação de tipos de entrada em `delegate()`; permissões
`600`/`700` nos artefatos escritos; delimitador sentinela anti prompt-injection no prompt.

## Consequências

- **Positivas**: menor superfície de ataque (sem agente local nas rotas); fallback de nuvem
  gratuito e resiliente; visibilidade de uso sem custo; config e credenciais validadas.
- **Negativas / dívidas**: defesa anti prompt-injection é textual (não elimina o risco);
  Groq não valida pricing (depende do free tier da conta + allowlist opcional); métricas de
  token são estimativas grosseiras.
- **Testes**: suíte via TDD cobrindo happy path, edge cases e erros; `conftest.py` isola a
  config real e remove credenciais do ambiente para evitar chamadas de rede acidentais na
  suíte.

## Alternativas consideradas

- Manter o Gemini CLI com env completo: rejeitado (vazamento de segredos ao subprocesso).
- Provedor de nuvem direto adicional (Cerebras, Mistral, Together): adiável — OpenRouter já
  agrega vários modelos free; Groq escolhido por latência e free tier generoso.
- Métrica via tokenizer real ou API de billing: rejeitado por custo monetário/processamento.

---

## Atualização (2026-10-09) — Gemini migrado de CLI para API HTTP

A decisão 1 (Gemini CLI desabilitado) é **substituída**: o Gemini foi reintroduzido como
adaptador de **API HTTP pura** (`generativelanguage.googleapis.com`, header `x-goog-api-key`),
sem subprocesso nem agente local — eliminando a brecha que motivou a desativação do CLI.
Imports `subprocess`/`shutil`/`tempfile` removidos do adaptador.

Salvaguardas de custo (o router não valida pricing do Gemini): default no modelo mais barato
`gemini-flash-lite-latest`; allowlist opcional `GEMINI_ALLOWED_MODELS` (fail-closed antes da rede);
`maxOutputTokens` em 768. Recomendação operacional: usar API key de projeto **sem billing
habilitado** para custo zero garantido. Gemini reintroduzido nas rotas como **último fallback**
(`ollama → groq → openrouter → gemini`). Sandbox do CLI (sandbox-exec/container) foi avaliado e
rejeitado: frágil/deprecado no caso nativo e pesado para 8 GB no caso de container, com
custo-benefício inferior à API pura.
