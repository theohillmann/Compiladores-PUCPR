def executar_expressao(tokens: list, resultados: list, memorias: dict):
    stack_calculation = []
    token_index = 0

    while token_index < len(tokens):
        current_token = tokens[token_index]
        # print(current_token)

        if current_token in ["(", ")"]:
            token_index += 1
            continue

        elif current_token in ["+", "-", "*", "/", "%", "^", "^"]:
            result = process_operation(stack_calculation, current_token)

        else:
            try:
                numeric_value = float(current_token)
                stack_calculation.append(numeric_value)
            except ValueError:
                return f"Erro: Invalid token '{current_token}'"

        token_index += 1

    return result


def process_operation(stack_calculation, operator):
    if len(stack_calculation) < 2:
        return f"Erro: {operator} requires two operands"

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
        return "Erro: Division by zero"
    except Exception as e:
        return "Error: operation failed"


print(executar_expressao(["(", "2", "2.0", "+", ")"], "", ""))
print(executar_expressao(["(", "3", "2.0", "*", ")"], "", ""))
print(executar_expressao(["(", "10", "5", "/", ")"], "", ""))
print(executar_expressao(["(", "2", "2", "-", ")"], "", ""))
print(executar_expressao(["(", "11", "2", "%", ")"], "", ""))
print(executar_expressao(["(", "2", "2", "^", ")"], "", ""))
print(executar_expressao(["(", "2", "0", "%", ")"], "", ""))
print(executar_expressao(["(", "2", "0", "/", ")"], "", ""))
print(executar_expressao(["(", "2", "0", "$", ")"], "", ""))
print(executar_expressao(["(", "2", "+", "0", ")"], "", ""))
