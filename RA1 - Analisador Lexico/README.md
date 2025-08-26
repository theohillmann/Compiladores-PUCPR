# RA1 - Analisador Léxico

## Descrição
Este projeto implementa um analisador léxico e avaliador de expressões matemáticas em notação polonesa reversa. O sistema é capaz de processar expressões aritméticas, gerenciar memória de variáveis e manter histórico de resultados.

## Funcionalidades

### Operações Aritméticas Suportadas
- **Adição** (`+`)
- **Subtração** (`-`)
- **Multiplicação** (`*`)
- **Divisão** (`/`)
- **Módulo** (`%`)
- **Exponenciação** (`^`)

### Funcionalidades Especiais
- **RES**: Acessa resultados anteriores (ex: `2 RES` acessa o penúltimo resultado)
- **Variáveis de Memória**: Armazena valores em variáveis (devem ser em maiúsculas)
- **Validação de Parênteses**: Verifica balanceamento automático
- **Tratamento de Erros**: Detecção e relatório de erros de sintaxe

## Estrutura do Projeto

```
RA1 - Analisador Lexico/
├── main.py              # Ponto de entrada principal
├── ler_arquivo.py       # Módulo para leitura de arquivos
├── parse_expressao.py   # Analisador léxico e tokenizador
├── executar_expressao.py # Avaliador de expressões
├── gerar_assembly.py    # Gerador de código assembly
└── tests/               # Arquivos de teste
    ├── test1.txt
    ├── test2.txt
    └── test3.txt
```

## Como Usar

Dentro dessa pasta:

### Execução Básica
```bash
python main.py <arquivo_expressoes> <arquivo_assembly>
```

### Exemplo
```bash
python main.py tests/test1.txt output.s
```

## Formato das Expressões

O sistema utiliza **notação pós-fixa** (polonesa reversa). As expressões devem estar entre parênteses.

### Exemplos de Entrada

#### Operações Básicas
```
( 12 5 + )        # 12 + 5 = 17
( 20 7 - )        # 20 - 7 = 13
( 6 8 * )         # 6 * 8 = 48
( 20 4 / )        # 20 / 4 = 5
( 9 4 % )         # 9 % 4 = 1
( 2 10 ^ )        # 2^10 = 1024
```

#### Uso de RES (Resultados Anteriores)
```
( 12 5 + )        # Resultado 1: 17
( 20 7 - )        # Resultado 2: 13
( ( 2 RES ) 3 + ) # Usa o 2º resultado anterior (13) + 3 = 16
```

#### Variáveis de Memória
```
( 42 X )          # Armazena 42 na variável X
( X 8 + )         # Usa X (42) + 8 = 50
```

## Tratamento de Erros

### Erros Léxicos
- Caracteres inválidos
- Múltiplos pontos decimais em números
- Parênteses desbalanceados

### Erros de Execução
- Divisão por zero
- Operadores com operandos insuficientes
- Referências RES fora do alcance
- Variáveis não inicializadas

## Exemplo de Saída

```
( 12 5 + ) = 17.0
( 20 7 - ) = 13.0
( 6 8 * ) = 48.0
( 42 X )
( X 8 + ) = 50.0

Assembly Code saved to output.s
```

## Arquivos de Teste

O projeto inclui arquivos de teste na pasta `tests/`:
- `test1.txt`: Operações básicas e uso de RES/memória
- `test2.txt`: Casos adicionais de teste
- `test3.txt`: Testes específicos


## Requisitos

- Python 3.6+
- Não há dependências externas

## Autores
Theo Hillmann Luiz Coelho

Projeto desenvolvido para a disciplina de Compiladores - PUCPR

---

**Nota**: Este é um projeto acadêmico focado no aprendizado de conceitos de compiladores, especificamente análise léxica e avaliação de expressões.
