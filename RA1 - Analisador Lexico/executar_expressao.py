def executar_expressao(tokens: list, resultados: list, memorias: dict):
    built_in_functions = ["RES"]
    stack_calculation = []
    token_index = 0

    while token_index < len(tokens):
        current_token = tokens[token_index]

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

            if isinstance(result, str) and result.startswith("Error"):
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
        if not token.isupper():
            return f"Error: '{token}' not valid for memory. It must be upper case."
        if len(stack_calculation) < 1:
            return f"Error: '{token}' is not in memory"
        memorias[token] = stack_calculation.pop()
        stack_calculation.append("")

    else:
        stack_calculation.append(memorias[token])
