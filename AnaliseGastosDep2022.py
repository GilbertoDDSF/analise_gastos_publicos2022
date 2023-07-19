from lxml import etree
import locale


def carregar_dados():
    dicionario_deputado = {}
    dados = etree.parse("data/Ano-2022.xml")
    lista_despesas = dados.findall('dados')
    for despesa in lista_despesas:
        for informacao in despesa:
            propriedades = informacao.getchildren()
            if propriedades[19].tag == 'valorLiquido':
                nome = propriedades[0].text
                categoria = propriedades[9].text
                valor_despesa = propriedades[19].text.replace('.', '').replace(',', '.')

                dicionario = dicionario_deputado.get(nome, {})
                dicionario[categoria] = dicionario.get(categoria, 0) + float(valor_despesa)
                dicionario_deputado[nome] = dicionario

    return dicionario_deputado


def formatar_valor(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor_formatado = locale.currency(valor, grouping=True, symbol=None)
    locale.setlocale(locale.LC_ALL, '')
    return valor_formatado


if __name__ == "__main__":
    dicionario = carregar_dados()

    while True:
        total_despesas = 0
        deputado = input("Informe o nome do deputado ou digite 0 para sair: ")
        if deputado == "0":
            break
        elif deputado in dicionario:
            for categoria, valor in dicionario[deputado].items():
                total_despesas += valor
                valor_formatado = formatar_valor(valor)
                print(f"{categoria}: {valor_formatado}")
        else:
            print("Deputado não localizado!")
            opcao = input("Deseja ver a lista de deputados? (S/N): ")
            if opcao.upper() == "S":
                for nome in dicionario.keys():
                    print(nome)

        total_despesas_formatado = formatar_valor(total_despesas)
        print(f"Total de despesas: {total_despesas_formatado}")

    print("--- Obrigado por utilizar o sistema ---")
