import argparse
from ler_arquivo import lerArquivo
from parse_expressao import parseExpressao
from executar_expressao import executar_expressao


def main(expressions_file, assembly_file):
    memory = {}
    results = []
    operations = lerArquivo(expressions_file)
    for operation in operations:
        expression = parseExpressao(operation)
        result = executar_expressao(expression, results, memory)
        results.append(result)
        if result != "":
            print(f"{operation} = {result}")
        else:
            print(operation)

    print("\n Assembly Code saved to", assembly_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process expressions and generate assembly."
    )
    parser.add_argument("expressions_file", help="File containing expressions")
    parser.add_argument("assembly_file", help="Output assembly (.s) file")
    args = parser.parse_args()
    main(args.expressions_file, args.assembly_file)
