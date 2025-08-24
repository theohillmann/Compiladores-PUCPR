def parseExpressao(linha: str) -> list:
    token_list = []
    current_position = 0

    error_message = None

    while current_position < len(linha) and error_message is None:
        print(current_position)



parseExpressao("(3.14 2.0 +)")