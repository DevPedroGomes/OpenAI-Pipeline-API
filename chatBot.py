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

def geracao_texto(messages):
    resposta = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=1000,
        stream=True,
    )
    
    print('Assistant:', end='')
    texto_completo = ''
    for resposta_stream in resposta:
        text = resposta_stream.choices[0].delta.content
        if text:
            print(text, end="")
            texto_completo += text
    print()
            
    messages.append({'role' : 'assistant', 'content' : texto_completo})
    return messages


if __name__ == '__main__':
    print('Bem-vindo ao ChatBot')
    messages = []
    while True:
        input_usuario = input('User: ')
        messages.append({'role':'user', 'content': input_usuario})
        messages = geracao_texto(messages)
        
        