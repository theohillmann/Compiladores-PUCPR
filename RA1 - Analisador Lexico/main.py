import argparse
from ler_arquivo import lerArquivo
from parse_expressao import parseExpressao
from executar_expressao import executar_expressao
from gerar_assembly import gerarAssembly


def main(expressions_file, assembly_file):
    """
    Função principal que processa as expressões de um arquivo, executa cada uma,
    imprime os resultados e gera o código assembly.

    Args:
        expressions_file (str): Caminho para o arquivo contendo as expressões.
        assembly_file (str): Caminho para o arquivo de saída em assembly.
    """
    memory = {}
    results = []
    operations = lerArquivo(expressions_file)
    all_tokens = []

    for operation in operations:
        expression = parseExpressao(operation)

        all_tokens.append(expression)
        result = executar_expressao(expression, results, memory)
        results.append(result)
        if result != "":
            print(f"{operation} = {result}")
        else:
            print(operation)

    print(f"\nGerando Assembly para {len(all_tokens)} expressões...")
    print(all_tokens)
    assembly_code = gerarAssembly(all_tokens)

    with open(assembly_file, "w") as file:
        file.write(assembly_code)

    with open("tokens.txt", "w") as file:
        for tokens in all_tokens:
            file.write(" ".join(tokens) + "\n")

    print("Assembly Code salvo em:", assembly_file)
    print("Tokens salvos em: tokens.txt")


if __name__ == "__main__":
    """
    Ponto de entrada do programa. Analisa argumentos da linha de comando e chama a função principal.
    """
    parser = argparse.ArgumentParser(
        description="Processa expressões e gera código assembly."
    )
    parser.add_argument("expressions_file", help="Arquivo contendo as expressões")
    parser.add_argument("assembly_file", help="Arquivo de saída assembly (.s)")
    args = parser.parse_args()
    main(args.expressions_file, args.assembly_file)
