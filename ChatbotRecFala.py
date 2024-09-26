import os
from dotenv import load_dotenv, find_dotenv
import openai
from pathlib import Path

from io import BytesIO
import speech_recognition as sr

from playsound import playsound



# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Obtém a chave da API do OpenAI do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")

# Configura a chave da API do OpenAI
openai.api_key = api_key

# Agora você pode usar o cliente OpenAI para fazer solicitações à API
client = openai.Client()

ARQUIVO_AUDIO = 'fala_assistant.mp3'

recognizer = sr.Recognizer()

def grava_audio():
    with sr.Microphone() as source:
        print('Ouvindo...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

def transcricao_audio():
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name= 'audio.wav'
    transcricao = client.audio.transcriptions.create(
        model='whisper-1',
        file=wav_data,
    )
    return transcricao.text


def completa_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model='gpt-3.5-turbo-0125',
        max_tokens=1000,
        temperature=0
    )
    return resposta


def cria_audio(texto):
    if Path(ARQUIVO_AUDIO).exists():
        Path(ARQUIVO_AUDIO).unlink()
    arquivo = 'fala_assistant.mp3'
    resposta = client.audio.speech.create(
        model='tts-1',
        voice='onyx',
        input=texto
    )
    resposta.write_to_file(arquivo)
    
def roda_audio():
    playsound(ARQUIVO_AUDIO)    
    
    
if __name__ == '__main__':
    
    mensagens= []
    while True:
        audio = grava_audio()
        transcricao = transcricao_audio(audio)
        mensagens.append({'role': 'user', 'content': transcricao})
        print(f'User: {transcricao}' )
        resposta = completa_texto(mensagens)
        mensagens.append({'role': 'assistant', 'content': resposta.choices[0].message.content})
        print(f'Assistant: {mensagens[-1]['content']}')   
        cria_audio(mensagens[-1]['content'])
        roda_audio()