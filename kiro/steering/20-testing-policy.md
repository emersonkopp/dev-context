# Política de Testes (TDD)

Adote TDD em toda implementação ou alteração de código.

## Ciclo obrigatório

1. **Red**: escreva testes baseados nos requisitos. Veja-os falhar.
2. **Green**: implemente o mínimo para os testes passarem.
3. **Refactor**: melhore o código mantendo testes verdes.

## Cobertura exigida

Não limite ao happy path. Cubra:

- **Regras de negócio**: validação direta de cada requisito.
- **Edge cases**: inputs nulos, vazios, negativos, limites, overflow.
- **Erros**: exceções corretas lançadas, códigos de erro adequados, sem falhas silenciosas.

## Ordem de entrega

Apresente os testes primeiro (com os cenários mapeados), depois o código de produção.
