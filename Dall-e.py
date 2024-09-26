import os
from dotenv import load_dotenv, find_dotenv
import openai
from PIL import Image
import requests

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Obtém a chave da API do OpenAI do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")

# Configura a chave da API do OpenAI
openai.api_key = api_key

# Agora você pode usar o cliente OpenAI para fazer solicitações à API
client = openai.Client()

# CRIACAO DE IMAGEM

resposta = client.image.generate(
    model='dall-e-3',
    promtp='Crie uma imagem de duas senhoras conversando num bosque',
    size='1024x1024',
    quality='hd',
    style='natural',
    n=1
)

print(resposta.data[0].revised_prompt)


print(resposta.data[0].url)


# SALVAR IMAGEM

nome_arquivo= f'arquivos/imagens/{nome}_{modelo}_{qualidade}_{style}.jpg'

image_url=resposta.data[0].url

img_data=requests.get(image_url).content

with open(nome_arquivo, 'wb') as f:
    f.write(img_data)
    
    
    
    
# MOSTRA IMAGEM

image= Image.open(nome_arquivo)
image.show() 



# EDICAO DE IMAGEM

resposta = client.images.edit(
    model='dall-e-2',
    image=open('arquivos/imagens/original.png', 'rb'),
    mask=open('arquivos/imagens/mask.png', 'rb'),
    prompt="POR AQUI A SUA EXIGENCIA DE EDICAO NA IMAGEM",
    n=1,
    size='1024x1024'
    
)

nome_arquivo='editada.png'

image_url = resposta.data[0].url
img_data= requests.get(image_url).content
with open(nome_arquivo, 'rb') as f:
    f.write(img_data)
    
    
# CRIACAO DE VARIACOES


respota = client.images.create_variation(
    image=open('arquivos/imagens/senhoras_bosque_dall-e-2_hd_natural.jpg', 'rb'),
    n=1,
    size='1024x1024'
) 

nome_arquivo='variacao.png'

image_url = resposta.data[0].url
img_data= requests.get(image_url).content
with open(nome_arquivo, 'rb') as f:
    f.write(img_data)
    
# MOSTRA IMAGEM

image= Image.open(nome_arquivo)
image.show()     

