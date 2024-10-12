from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
from llm_IA import carregar_extratos

pasta_extratos = "extratos"
df_extratos = carregar_extratos(pasta_extratos)

_ = load_dotenv(find_dotenv())

template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados,
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Todos são transações financeiras.

Escolha uma dentre as seguintes categorias:

Alimentação

- Credito
- Débito
- Receita
- Compras
- Transporte
- Investimento
- tranferência para terceiros
- Telefone

Escolha a categoria deste item:
{text}

responda apenas a categoria.
"""

prompt = PromptTemplate.from_template(template=template)
chat = ChatGroq(model="llama-3.1-70b-versatile")
chain = prompt | chat

category = []
for transaction in list(carregar_extratos["Descrição"].values):
    category += chain.invoke(transaction).content

print(category)
