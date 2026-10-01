# Diretrizes de Qualidade: Desenvolvimento Orientado a Testes (TDD)

Você deve obrigatoriamente adotar a metodologia TDD (Test-Driven Development) para qualquer implementação ou alteração de código solicitada.

## 1. Fluxo de Desenvolvimento (Ciclo TDD)
Antes de escrever qualquer linha de código produtivo, você deve:
1. **Red**: Escrever os testes unitários baseados nos requisitos técnicos e vê-los falhar.
2. **Green**: Escrever a quantidade mínima de código produtivo necessária para fazer os testes passarem.
3. **Refactor**: Refatorar o código mantendo os testes verdes, garantindo boas práticas, legibilidade e padrões de arquitetura.

## 2. Cobertura Abrangente de Cenários
Os testes unitários gerados não devem se limitar ao "caminho feliz" (happy path). Eles devem cobrir:
* **Funcionalidades dos Requisitos:** Validação direta de cada regra de negócio descrita nos requisitos do projeto.
* **Cenários Não Cobertos (Casos de Borda/Edge Cases):** Identificar proativamente lacunas nas especificações (ex: inputs nulos, strings vazias, números negativos onde não deveriam existir, estolamento de memória ou violações de limites).
* **Tratamento de Erros e Exceções:** Verificar se o sistema falha graciosamente. Os testes devem explicitamente garantir que exceções corretas sejam lançadas, códigos de erro adequados sejam retornados e falhas silenciosas não ocorram em situações inesperadas.

## 3. Entrega do Artefato
Sempre que for solicitado o desenvolvimento de uma funcionalidade, apresente primeiro a estrutura e o código dos testes unitários correspondentes, explicando quais cenários de falha e exceção foram mapeados, antes de exibir o código da funcionalidade em si.
