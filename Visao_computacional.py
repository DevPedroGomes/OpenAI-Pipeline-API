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


import base64


# CONTANDO CELULAS DE UMA IMAGEM DE ENDOSCOPIA
def encode_image(caminho_imagem):
    with open(caminho_imagem, 'rb') as img:
        return base64.b64encode(img.read()).decode('utf-8')


caminho = 'arquivos/vision/celulas.jpg'
base_64_img = encode_image(caminho)
        
def generate_image(prompt):
    resposta = client.chat.completions.create(
        model='gpt-4-vision-preview',
        messages=[{
            'role': 'user',
            'content': [
                {'type' : 'text' , 'text': prompt},
                {'type': 'image_url', "image_url" :
                    {'url':f'data:image/jpg;{base_64_img}'}}
            ]
        }],
        max_tokens=1000,
    )

    image =  resposta.choices[0].message.content
    return image





# VERIFICANDO PLACA DE CARRO

caminho = 'arquivos/vision/placa_carro.jpg'
base_64_img = encode_image(caminho)    
        

resposta = client.chat.completions.create(
    model='gpt-4-vision-preview',
    messages=[{
        'role': 'user',
        'content': [
            {'type' : 'text' , 'text': 'Qual eh a placa do carro'},
            {'type': 'image_url', "image_url" :
                {'url':f'data:image/jpg;{base_64_img}'}}
        ]
    }],
    max_tokens=1000,
)

print(resposta.choices[0].message.content)


# DECIFRANDO ESCRITAS

caminho = 'arquivos/vision/escrito_mao_facil.jpg'
base_64_img = encode_image(caminho)    

text = 'O que esta escrito na imagem'
        

resposta = client.chat.completions.create(
    model='gpt-4-vision-preview',
    messages=[{
        'role': 'user',
        'content': [
            {'type' : 'text' , 'text': text},
            {'type': 'image_url', "image_url" :
                {'url':f'data:image/jpg;{base_64_img}'}}
        ]
    }],
    max_tokens=1000,
)

print(resposta.choices[0].message.content)

# MUDAR LAYOUT DE PAGINA WEB


caminho = 'arquivos/vision/layout.jpg'
base_64_img = encode_image(caminho)    
        
text= 'Crie um novo layout para esta pagina, quero um layout que gere uma melhor experiencia de usuario. Retorne os codigos html e css da pagina nova'
resposta = client.chat.completions.create(
    model='gpt-4-vision-preview',
    messages=[{
        'role': 'user',
        'content': [
            {'type' : 'text' , 'text': text},
            {'type': 'image_url', "image_url" :
                {'url':f'data:image/jpg;{base_64_img}'}}
        ]
    }],
    max_tokens=4000,
)

print(resposta.choices[0].message.content)