token_list = []
from typing import Optional


def parseExpressao(input_line: str) -> list:
    global token_list
    current_position = 0

    error_message = None

    while current_position < len(input_line) and error_message is None:
        last_position = current_position
        current_position, error_message = initial_state(current_position, input_line)

    print(token_list)


def initial_state(position: int, input_line: str) -> tuple[int, Optional[str]]:
    if position >= len(input_line):
        return position, None

    current_char = input_line[position]

    if current_char.isspace():
        return position + 1, None

    elif current_char in ["(", ")"]:
        token_list.append(current_char)
        return position + 1, None

    elif current_char.isdigit() or current_char == ".":
        return position + 1, None

    elif current_char in ["+", "-", "*", "/"]:
        token_list.append(current_char)
        return position + 1, None

    elif current_char.isalpha():
        return position + 1, None

    return position, f"Error: Invalid character '{current_char}' at position {position}"


parseExpressao("(3.14 2.0 +)")
