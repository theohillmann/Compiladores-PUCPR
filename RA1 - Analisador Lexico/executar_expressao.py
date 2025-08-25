def executar_expressao(tokens: list, resultados: list, memorias: dict):
    built_in_functions = ["RES"]
    stack_calculation = []
    token_index = 0

    while token_index < len(tokens):
        current_token = tokens[token_index]
        # print(current_token)

        if current_token in ["(", ")"]:
            token_index += 1
            continue

        elif current_token in ["+", "-", "*", "/", "%", "^"]:
            result = process_operation(stack_calculation, current_token)
            if isinstance(result, str):
                return result
            stack_calculation.append(result)

        elif current_token == "RES":
            try:
                tokens[token_index - 1]
            except IndexError:
                return "Error: RES requires a preceding token"
            result = res(stack_calculation, tokens[token_index - 1], resultados)
            if isinstance(result, str) and result.startswith("Erro"):
                return result

        elif current_token.isalpha():
            if current_token in built_in_functions:
                return f"Error: '{current_token}' is a reserved keyword"
            result = mem(stack_calculation, current_token, memorias)
            if isinstance(result, str) and result.startswith("Erro"):
                return result

        else:
            try:
                numeric_value = float(current_token)
                stack_calculation.append(numeric_value)
            except ValueError:
                return f"Error: Invalid token '{current_token}'"

        token_index += 1

    if len(stack_calculation) == 1:
        return stack_calculation[0]
    elif not stack_calculation:
        return "Error: Nenhum resultado produzido"
    else:
        return f"Error: Expressão mal formada"


def process_operation(stack_calculation, operator):
    if len(stack_calculation) < 2:
        return f"Error: {operator} requires two operands"

    right_operator = stack_calculation.pop()
    left_perator = stack_calculation.pop()

    return execute_operation(right_operator, operator, left_perator)


def execute_operation(
    right_operator: float, operator: str, left_operator: float
) -> float:
    try:
        if operator == "^":
            return left_operator**right_operator
        return eval(f"{left_operator} {operator} {right_operator}")
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return "Error: operation failed"


def res(stack_calculation, token, resultados):
    if len(stack_calculation) < 1:
        return "Error: RES requires one operand"
    try:
        index = stack_calculation.pop()
        if index != int(index) or index <= 0:
            return "Error: RES requires a positive integer operand"
        result = resultados[-int(index)]
    except IndexError:
        return f"Error: RES {token} out of range"

    stack_calculation.append(result)
    return result


def mem(stack_calculation: list, token: str, memorias: dict):
    if token not in memorias.keys():
        if len(stack_calculation) < 1:
            return f"Error: '{token}' is not in memory"
        memorias[token] = stack_calculation.pop()

    stack_calculation.append(memorias[token])


cenarios = [
    # (descrição, tokens, historico, memorias, esperado)
    ("Soma básica", ["(", "3", "4", "+", ")"], [], {}, 7.0),
    ("Subtração básica", ["(", "10", "5", "-", ")"], [], {}, 5.0),
    ("Multiplicação básica", ["(", "2", "3", "*", ")"], [], {}, 6.0),
    ("Divisão básica", ["(", "20", "4", "/", ")"], [], {}, 5.0),
    ("Resto da divisão", ["(", "7", "3", "%", ")"], [], {}, 1),
    ("Potenciação", ["(", "2", "5", "^", ")"], [], {}, 32.0),
    # Erros aritméticos
    (
        "Divisão por zero",
        ["(", "5", "0", "/", ")"],
        [],
        {},
        "Error: Division by zero",
    ),
    (
        "Operador inválido",
        ["(", "2", "$", "3", "+", ")"],
        [],
        {},
        "Error: Invalid token '$'",
    ),
    # Expressão mal formada
    (
        "Valor sobrando na pilha",
        ["(", "2", "3", "+", "4", ")"],
        [],
        {},
        "Error: Expressão mal formada",
    ),
    ("Nenhum resultado", ["(", "RES", ")"], [], {}, "Error: RES requires one operand"),
    # Comando RES
    ("RES válido", ["(", "2", "RES", ")"], [10.0, 20.0, 30.0], {}, 20.0),
    (
        "RES fora do intervalo",
        ["(", "5", "RES", ")"],
        [1.0, 2.0],
        {},
        "Error: RES 5 out of range",
    ),
    # Comando MEM
    ("Armazenar em X", ["(", "42", "MEM", "X", ")"], [], {}, 42.0),
    ("Recuperar X e somar", ["(", "X", "8", "+", ")"], [], {"X": 42.0}, 50.0),
    # Aninhamento com RES
    (
        "Aninhado RES e soma",
        ["(", "(", "2", "RES", ")", "10", "+", ")"],
        [5.0, 15.0, 25.0],
        {},
        25.0,
    ),
    # MEM não inicializada
    ("MEM não inicializada", ["(", "Y", ")"], [], {}, "Error: 'Y' is not in memory"),
    ("MEM sem valor", ["(", "MEM", ")"], [], {}, "Error: 'MEM' is not in memory"),
]

print("Iniciando testes manuais de executar_expressao...\n")
for descricao, tokens, historico, memorias, esperado in cenarios:
    resultado = executar_expressao(tokens, historico.copy(), memorias.copy())
    passou = False
    if isinstance(esperado, str):
        passou = esperado in str(resultado)
    else:
        passou = resultado == esperado

    status = "PASS" if passou else "FAIL"
    print(f"[{status}] {descricao}")
    print(f"    Tokens:    {tokens}")
    print(f"    Histórico: {historico}")
    print(f"    Memórias:  {memorias}")
    print(f"    Esperado:  {esperado!r}")
    print(f"    Obtido:    {resultado!r}\n")
