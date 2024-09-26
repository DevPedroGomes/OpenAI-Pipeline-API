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


audio = open('arquivos/audio/audio_asimov.mp3', 'rb')
transcription = client.audio.transcriptions.create(
    model='whisper-1',
    file=audio,
    prompt='SEU PROMPT AQUI PARA O MODELO SER ESPECIFICO SOBRE O ARQUIVO DE AUDIO A SER TRANSCRITO'
)

print(transcription.text)