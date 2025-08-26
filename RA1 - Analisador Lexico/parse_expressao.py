from typing import Optional

token_list = []
input_line = ""


def parseExpressao(line: str) -> list:
    """
    Analisa uma expressão matemática recebida como string e retorna uma lista de tokens ou uma mensagem de erro.

    Args:
        line (str): Expressão a ser analisada.

    Returns:
        list: Lista de tokens extraídos da expressão ou mensagem de erro em caso de falha.
    """
    global token_list, input_line
    token_list.clear()
    input_line = line
    current_position = 0

    error_message = None
    if not is_parentheses_valid():
        error_message = "Error: Unmatched parentheses"

    while current_position < len(input_line) and error_message is None:
        current_position, error_message = initial_state(current_position)

    return error_message if error_message else token_list


def is_parentheses_valid():
    """
    Verifica se os parênteses na expressão estão balanceados.

    Returns:
        bool: True se os parênteses estão corretos, False caso contrário.
    """
    count = 0
    for char in input_line:
        if char in ["(", ")"]:
            count += 1 if char == "(" else -1
            if count < 0:
                return False

    return count == 0


def initial_state(position: int) -> tuple[int, Optional[str]]:
    """
    Estado inicial do analisador léxico. Identifica o tipo do próximo token na expressão.

    Args:
        position (int): Posição atual na string de entrada.

    Returns:
        tuple: Próxima posição a ser analisada e mensagem de erro (caso exista).
    """
    if position >= len(input_line):
        return position, None

    current_char = input_line[position]

    if current_char.isspace():
        return position + 1, None

    elif current_char in ["(", ")"]:
        token_list.append(current_char)
        return position + 1, None

    elif current_char.isdigit() or current_char == ".":
        return numeric_state(position)

    elif current_char in ["+", "-", "*", "/", "%", "^"]:
        token_list.append(current_char)
        return position + 1, None

    elif current_char.isalpha():
        return spacial_commands(position)

    return position, f"Error: Invalid character '{current_char}' at position {position}"


def numeric_state(position: int) -> tuple[int, Optional[str]]:
    """
    Analisa e extrai um número (inteiro ou decimal) da expressão a partir da posição atual.

    Args:
        position (int): Posição inicial do número na string de entrada.

    Returns:
        tuple: Próxima posição após o número e mensagem de erro (caso exista).
    """
    complete_number = ""
    decimal_points_count = 0

    while position < len(input_line):
        current_char = input_line[position]

        if current_char.isdigit():
            position += 1
            complete_number += current_char

        elif current_char == "." and decimal_points_count == 0:
            complete_number += current_char
            position += 1
            decimal_points_count += 1

        elif current_char == "." and decimal_points_count >= 1:
            return (
                position,
                f"Error: Multiple decimal points in number at position {position}",
            )
        else:
            break

    token_list.append(complete_number)
    return position, None


def spacial_commands(position: int) -> tuple[int, Optional[str]]:
    """
    Analisa e extrai comandos especiais (palavras ou identificadores) da expressão.

    Args:
        position (int): Posição inicial do comando na string de entrada.

    Returns:
        tuple: Próxima posição após o comando e mensagem de erro (caso exista).
    """
    complete_command = ""

    while position < len(input_line) and (
        input_line[position].isdigit() or input_line[position].isalpha()
    ):
        complete_command += input_line[position]
        position += 1

    token_list.append(complete_command)
    return position, None
