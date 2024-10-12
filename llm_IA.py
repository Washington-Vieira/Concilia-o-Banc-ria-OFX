import os
import ofxparse
import pandas as pd

def carregar_extratos(pasta_extratos):
    df = pd.DataFrame()

    # Itera sobre os arquivos na pasta
    for extrato in os.listdir(pasta_extratos):
        # Abre e faz o parsing do arquivo OFX
        with open(f'{pasta_extratos}/{extrato}', encoding='utf8') as ofx_file:
            ofx = ofxparse.OfxParser.parse(ofx_file)

        # Extrai os dados de transações
        transactions_data = []
        for account in ofx.accounts:
            for transaction in account.statement.transactions:
                transactions_data.append({
                    "Data": transaction.date,
                    "Valor": transaction.amount,
                    "Descrição": transaction.memo,
                    "ID": transaction.id,
                })

        # Cria um DataFrame temporário e ajusta o formato dos dados
        df_temp = pd.DataFrame(transactions_data)
        df_temp["Valor"] = df_temp["Valor"].astype(float)
        df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())

        # Concatena o DataFrame temporário ao DataFrame principal
        df = pd.concat([df, df_temp])

    return df

# Exemplo de uso:
# pasta_extratos = "extratos"
# df_extratos = carregar_extratos(pasta_extratos)

