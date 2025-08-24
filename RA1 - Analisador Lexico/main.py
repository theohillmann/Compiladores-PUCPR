from typing import Optional

token_list = []
input_line = ""


def parseExpressao(line: str) -> list:
    global token_list, input_line
    input_line = line
    current_position = 0

    error_message = None

    while current_position < len(input_line) and error_message is None:
        last_position = current_position
        current_position, error_message = initial_state(current_position)

    print(token_list, error_message)


def initial_state(position: int) -> tuple[int, Optional[str]]:
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

    elif current_char in ["+", "-", "*", "/"]:
        token_list.append(current_char)
        return position + 1, None

    elif current_char.isalpha():
        return spacial_commands(position)

    return position, f"Error: Invalid character '{current_char}' at position {position}"


def numeric_state(position: int) -> tuple[int, Optional[str]]:
    complete_number = ""
    decimal_points_count = 0

    while position < len(input_line):
        current_char = input_line[position]
        print(current_char)

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
    complete_command = ""

    while position < len(input_line) and (
        input_line[position].isdigit() or input_line[position].isalpha()
    ):
        complete_command += input_line[position]
        position += 1

    token_list.append(complete_command)
    return position, None


# parseExpressao("(3.14 2.0 +)")
parseExpressao("12 MEM")
