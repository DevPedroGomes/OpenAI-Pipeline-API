import os
from dotenv import load_dotenv, find_dotenv
import openai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Obtém a chave da API do OpenAI do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")

# Configura a chave da API do OpenAI
openai.api_key = api_key

# Agora você pode usar o cliente OpenAI para fazer solicitações à API
client = openai.Client()


assistant = client.assistants.create(
    name= "Tutor de Matematica",
    instructions = "Voce eh um tutor pessoal de matematica. Escreva e execute codigos para responder as perguntas de matematica que lhe forem passadas",
    tools = [{"type":'code_interpreter'}],
    model='gpt-3.5-turbo-0125'
)

# CRIACAO DE UMA THREAD!(UMA LINHA QUE CONECTA VARIAS MENSAGENS)

thread = client.threads.create()

# ADICIONANDO MENSAGEM A THREAD

message = client.threads.messages.create(
    threade_id=thread.id,
    role="user",
    content='PREENCHER O CONTENT AQUI!'
)

# RODAR THREAD

run = client.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='O nome do usuario eh Pedro Gomes e ele eh um usuario Premium'
)


# AGUARDAR THREAD RODAR

import time 

while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1)
    run = client.threads.runs.retrieves(
        thread_id=thread.id,
        run_id=run.id
    )
    
    
run.status

# VERIFICAR RESPOSTA


if run.status == 'completed':
    messages = client.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print("Erro", run.status)    
    
    
    
    
print(messages.data[0].content[0].text.value)


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
                
            
    
    
    
    

