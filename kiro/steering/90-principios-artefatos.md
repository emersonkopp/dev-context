# Princípios de Artefatos de IA (efetividade e concisão)

Regras para criar e editar artefatos deste monorepo (steerings, skills, prompts, instruções).
O objetivo é que cada artefato seja o mais curto possível sem perder efetividade: contexto é
finito e caro, e texto supérfluo degrada a atenção do modelo. Aplique a todo artefato novo ou
alterado.

## Efetividade

- **Uma responsabilidade por artefato.** Se cobre dois temas independentes, divida.
- **Acionável, não expositivo.** Prefira regras verificáveis ("não concatene entrada em SQL") a
  explicações teóricas ("SQL injection é um problema sério porque...").
- **Imperativo e direto.** Comece regras com verbo. Evite voz passiva e hedging ("talvez", "em geral").
- **Gatilhos claros em skills.** A `description`/`triggers` do frontmatter decide quando a skill
  carrega — liste contextos e verbos reais do usuário, não sinônimos redundantes.
- **Defina a saída esperada.** Diga o que o artefato deve produzir (relatório, checklist, decisão).

## Concisão

- **Sem redundância.** Não repita o que outro artefato já diz; referencie-o pelo caminho relativo.
- **Sem preâmbulo nem floreio.** Corte "este documento tem como objetivo", "é importante notar que".
- **Listas sobre parágrafos** para regras. Uma regra por item; uma linha quando possível.
- **Sem exemplos redundantes.** Inclua um exemplo só quando a regra for ambígua sem ele.
- **Limite de tamanho.** Steering ou skill passando de ~150 linhas é sinal de que deve ser dividido
  ou enxugado. Justifique exceções.

## Consistência

- Siga o padrão dos artefatos existentes (nomenclatura, estrutura de seções, frontmatter).
- Idioma: português, salvo motivo explícito.
- Não duplique regra entre steering e skill: o steering traz a regra obrigatória curta; a skill
  aprofunda o checklist.

## Checklist antes de salvar um artefato

- [ ] Responsabilidade única e propósito claro na primeira ou segunda linha.
- [ ] Toda regra é acionável e verificável.
- [ ] Nada repete outro artefato (referenciei em vez de copiar).
- [ ] Sem preâmbulo, floreio ou exemplos desnecessários.
- [ ] Skill: `description`/`triggers` com gatilhos reais e saída esperada definida.
- [ ] Tamanho justificado (enxuto; dividi se passou de ~150 linhas sem razão).
