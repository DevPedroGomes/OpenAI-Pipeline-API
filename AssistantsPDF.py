import os
from dotenv import load_dotenv, find_dotenv
import openai
import pandas as pd

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Obtém a chave da API do OpenAI do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")

# Configura a chave da API do OpenAI
openai.api_key = api_key

# Agora você pode usar o cliente OpenAI para fazer solicitações à API
client = openai.Client()

file = client.files.create(
    file= open("arquivos/divulgacao_resultado_ambev_4T23.pdf", 'rb'),
    purpose='assistants'
)

assistant = client.threads.create(
    name="Analista de Demonstracoes Financeiras",
    instructions='Voce eh um analista de demonstracoes financeiras da AMBEV. Voce tem acesso a demonstracao de resultado do 4 trimestre de 2023. Baseado apenas no documento que voce tem acesso, responda as perguntas do usuario',
    tools=[{'type':'retrieval'}],
    file_ids=[file.id],
    model='gpt-4-turbo-preview'
)


# CRIAR A THREAD

thread = client.threads.create()


# ADICIONAR MENSAGEM A THREAD

pergunta= "Como foi o desempenho operacional da AMBEV? Lembre-se que os numeros do resultado financeiro estao no padrao brasileiro, com decimais sendo separados por virgulas e milhares por ponto"

messages = client.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=pergunta
)

# RODAR A THREAD

run = client.threads.runs.create(
    thread_id = thread.id,
    assistant_id=assistant.id,
    instructions="O nome do usuario eh Pedro"
)


# AGUARDAR THREAD RODAR


import time 

while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1)
    run - client.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
print(run.status)



# VERIFICA RESPOSTA


if run.status == 'completed':
    messages = client.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print("Error:", run.status)    
    

# CHECANDO RESPOSTA
print(messages.data[0].content[0].text.value)
    