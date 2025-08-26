def lerArquivo(nomeArquivo):

    expressions_list = []

    with open(nomeArquivo, "r", encoding="utf-8") as file:
        for line in file:
            line_cleaned = line.strip()

            if not line_cleaned:
                continue
            expressions_list.append(line_cleaned)
    return expressions_list
