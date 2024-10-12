import os
import ofxparse
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv

# Função para carregar extratos de arquivos OFX
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
        df = pd.concat([df, df_temp], ignore_index=True)

    return df

# Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Define o template para o prompt de categorização
template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados,
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Todos são transações financeiras.

Escolha uma dentre as seguintes categorias:

- Alimentação
- Receita
- Saúde
- Educação
- Compras
- Transporte
- Investimento
- Transferência para terceiros
- Telefone
- Moradia

Escolha a categoria deste item:
{text}

responda apenas a categoria.
"""

# Cria o prompt template e o modelo de chat
prompt = PromptTemplate.from_template(template=template)
chat = ChatGroq(model="llama-3.1-70b-versatile")
chain = prompt | chat

# Carrega os extratos
pasta_extratos = "extratos"
df_extratos = carregar_extratos(pasta_extratos)

# Lista para armazenar as categorias
categories = []

# Itera sobre a coluna "Descrição" do DataFrame e classifica cada transação
for transaction in df_extratos["Descrição"].values:
    # Obtenha a resposta do modelo para cada transação
    resposta = chain.invoke({"text": transaction}).content
    # Adiciona a resposta (categoria) à lista
    categories.append(resposta)

# Exibe as categorias para todas as transações
print(categories)
