import os
from dotenv import load_dotenv, find_dotenv
import openai
import pandas as pd

dataset = pd.read_csv('arquivos/supermarket_sales.csv')
dataset.head()
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Obtém a chave da API do OpenAI do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")

# Configura a chave da API do OpenAI
openai.api_key = api_key

# Agora você pode usar o cliente OpenAI para fazer solicitações à API
client = openai.Client()


file = client.files.create(
    file=open('arquivos/supermarket_sales.csv', 'rb'),
    purpose='assistants'
)

assistant = client.assistants.create(
    name='Analista Financeiro Supermercados',
    instructions="Voce eh um analista financeiro de um supermercado. Voce utiliza os dados .csv relativo as vendas dos supermercado para realizar as suas analises",
    tools=[{'type':'code_interpreter'}],
    file_ids=[file.id],
    model='gtp-4-turbo-preview'
)


# CRIA UMA THREAD

thread = client.threads.create()

# ALTERNAR ENTRE AS PERGUNTAS NO PROMPT
pergunta = 'Qual o rating medio das vendas do nosso supermercado?'
pergunta2 = 'Gere um grafico pizza com o percentual de vendas por meio de pagamento'

messages = client.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=pergunta
)

# RODAR A THREAD

run = client.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='O nome do usuario eh Pedro.'
)

# AGUARDAR THREAD RODAR

import time

while run.status in ['queued', 'in_progress', "cancelling"]:
    time.sleep(1)
    run = client.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    
print(run.status)


# VERIFICAR RESPOSTA

if run.status == 'completed':
    messages = client.threads.message.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print("Error:", run.status)
    
    
    # PARA A PERGUNTA2 REMOVER O TEXT E VALUE
messages.data[0].content[0].text.value 

       
       
# ANALISANDO OS PASSOS DO MODELO


run_steps = client.threads.runs.steps.list(
    thread_id=thread.id,
    run_id=run.id
) 

for step in run_steps.data:
    print("Step:", step.step_details.type)
    if step.step_details.type == 'tool_calls':
        for tool_call in step.step_details.tool_calls:
            print('--------')
            print(tool_call.code_interpreter.input)
            print('--------')
            print('Result')
            print(tool_call.code_interpreter.outputs[0].logs)
    if step.step_details.type == 'message_creation':
        message = client.threads.messages.retrieve(
            thread_id=thread.id,
            message_id=step.step_details.message_creation.message_id
        )
        print(message.content[0].text.value)



# FAZENDO DOWNLOAD DO GRAFICO
file_id = message.content[0].image_file.file.id

image_data = client.files.content(file_id)

with open('arquivos/{file_id}.png', "w") as f:
    file.write(image_data.read())    