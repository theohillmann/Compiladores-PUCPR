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

        elif current_token in ["+", "-", "*", "/", "%", "^", "^"]:
            result = process_operation(stack_calculation, current_token)
            stack_calculation.append(result)

        elif current_token == "RES":
            try:
                tokens[token_index - 1]
            except IndexError:
                return "Erro: RES requires a preceding token"
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
                return f"Erro: Invalid token '{current_token}'"

        token_index += 1

    return stack_calculation
    # if len(stack_calculation) != 0:
    #     return "Erro: Wrong expression"
    #
    # return result


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


def res(stack_calculation, token, resultados):
    if len(stack_calculation) < 1:
        return "Erro: RES requires one operand"
    try:
        index = stack_calculation.pop()
        if index != int(index) or index <= 0:
            return "Erro: RES requires a positive integer operand"
        result = resultados[-int(index)]
    except IndexError:
        return f"Erro: RES {token} out of range"

    stack_calculation.append(result)
    return result


def mem(stack_calculation: list, token: str, memorias: dict):
    if token not in memorias.keys():
        if len(stack_calculation) < 1:
            return f"Error: '{token}' is not in memory"
        memorias[token] = stack_calculation.pop()

    stack_calculation.append(memorias[token])


# print(executar_expressao(["(", "2", "2.0", "+", ")"], "", ""))
# print(executar_expressao(["(", "3", "2.0", "*", ")"], "", ""))
# print(executar_expressao(["(", "10", "5", "/", ")"], "", ""))
# print(executar_expressao(["(", "2", "2", "-", ")"], "", ""))
# print(executar_expressao(["(", "11", "2", "%", ")"], "", ""))
# print(executar_expressao(["(", "2", "2", "^", ")"], "", ""))
# print(executar_expressao(["(", "2", "0", "%", ")"], "", ""))
# print(executar_expressao(["(", "2", "0", "/", ")"], "", ""))
# print(executar_expressao(["(", "2", "0", "$", ")"], "", ""))
# print(executar_expressao(["(", "2", "+", "0", ")"], "", ""))
# print(executar_expressao(["(", "2", "1", "+", "21", ")"], "", ""))
# print(
#     executar_expressao(
#         ["(", "(", "5", "RES", ")", "4", "+", ")"], [10, 20, 30, 40, 50], ""
#     )
# )
# print(executar_expressao(["(", "1", "RES", ")"], [1, 2, 3], ""))

# print(executar_expressao(["(", "test", "1", "+", ")"], [], {"test": 42}))
# print(executar_expressao(["(", "21", "test", ")"], [], {}))
print(executar_expressao(["(", "teste", "4", "+", ")"], [], {"teste": 10}))
