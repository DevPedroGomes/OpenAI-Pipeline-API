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



arquivo = 'arquivos/audios/fala.mp3'

text = 'TEXTO A SE TRANSFERIR AQUI'

resposta = client.audio.speech.create(
    model='tts-1',
    voice='echo',
    input=text
)

resposta.write_to_file(arquivo)