def lerArquivo(nomeArquivo):
    """
    Lê um arquivo texto linha por linha e retorna uma lista contendo cada linha não vazia.

    Parâmetros:
        nomeArquivo (str): O caminho para o arquivo a ser lido.

    Retorna:
        list: Uma lista de strings, cada uma representando uma linha não vazia do arquivo.
    """

    expressions_list = []

    with open(nomeArquivo, "r", encoding="utf-8") as file:
        for line in file:
            line_cleaned = line.strip()

            if not line_cleaned:
                continue
            expressions_list.append(line_cleaned)
    return expressions_list
