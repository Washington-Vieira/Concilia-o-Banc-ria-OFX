import ofxparse
import pandas as pd
import os
from datetime import datetime

df = pd.DataFrame()
for extrato in os.listdir("extratos"):
    with open(f'extratos/{extrato}', encoding='ISO-8859-1') as ofx_file:
        ofx = ofxparse.OfxParser.parse(ofx_file)

    transactions_data = []
    for account in ofx.accounts:
        for transaction in account.statement.transactions:
            transactions_data.append({
                "Data": transaction.date,
                "Valor": transaction.amount,
                "Descrição": transaction.memo,
                "ID": transaction.id,
            })

df_temp = pd.DataFrame(transactions_data)
df_temp["Valor"] = df_temp["Valor"].astype(float)
df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())
df = pd.concat([df, df_temp])
print(df)