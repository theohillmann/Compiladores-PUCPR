def executar_expressao(tokens: list, resultados: list, memorias: dict):
    stack_calculation = []
    token_index = 0

    while token_index < len(tokens):
        current_token = tokens[token_index]
        print(current_token)

        if current_token in ["(", ")"]:
            token_index += 1
            continue

        elif current_token in ["+", "-", "*", "/", "%", "^"]:
            if len(stack_calculation) < 2:
                return f"Erro: {current_token} requires two operands"

            right_operator = stack_calculation.pop()
            left_perator = stack_calculation.pop()

            result = f"{right_operator} {current_token} {left_perator}"

        else:
            try:
                numeric_value = float(current_token)
                stack_calculation.append(numeric_value)
            except ValueError:
                return f"Erro: Invalid token '{current_token}'"

        token_index += 1
    print(result)


print(executar_expressao(["(", "3.14", "2.0", "+", ")"], "", ""))
