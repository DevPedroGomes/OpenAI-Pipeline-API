import os
from dotenv import load_dotenv, find_dotenv
import openai
import json
import yfinance as yf

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Obtém a chave da API do OpenAI do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")

# Configura a chave da API do OpenAI
openai.api_key = api_key

# Agora você pode usar o cliente OpenAI para fazer solicitações à API
client = openai.Client()

def retorna_cotacao_historica(
    ticker,
    periodo='1mo'
):
    ticker = ticker.replace('.SA', '')
    print('retorna_cotacao_historica',ticker)
    ticker_obj = yf.Ticker(f'{ticker}.SA')
    hist = ticker_obj.history(period=periodo)['Close']
    hist.index = hist.index.strftime('%Y-%m-%d')
    hist = round(hist, 2)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    return hist.to_json()

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'retorna_cotacao_historica',
            'description': 'Retorna a cotacao diaria historica para uma acao da bovespa',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'O ticker da acao. Exemplo: "ABEV3" para ambev, "PETR4" para petrobras, etc'
                    },
                    'periodo': {
                        'type': 'string',
                        'description': 'O periodo que sera retornado os dados historicos, sendo "1mo" equivalente a 1 mes de dados, "1d" equivalente a 1 dia, e "1y" equivalente a 1 ano',
                        'enum': ["1d", "5d", "1mo", "6mo", "1y", "5y", "10y", "ytd", "max"]
                    }
                }
            }
        }
    }
]

funcoes_disponiveis = {'retorna_cotacao_acao_historica': retorna_cotacao_historica}


def gera_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model='gpt-3.5-turbo-0125',
        tools=tools,
        tool_choice='auto'
    )


    tool_calls = resposta.choices[0].message.tool_calls

    if tool_calls:
        mensagens.append(resposta.choices[0].message)
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            function_to_call = funcoes_disponiveis[func_name]
            func_args = json.loads(tool_call.function.arguments)
            func_return = function_to_call(**func_args)
            mensagens.append({
                'tool_call_id': tool_call.id,
                'role': 'tool',
                'name': func_name,
                'content': func_return
            })
        segunda_resposta = client.chat.completions.create(
            messages=mensagens,
            model='gpt-3.5-turbo-0125',
        )
        mensagens.append(segunda_resposta.choices[0].message)
    
    print(f'Assistant: {mensagens[-1].content}')

    return mensagens


if __name__ == '__main__':
    print("Bem-vindo ao ChatBot Financeiro.")
    input_usuario = input('User: ')
    
    while True:
        mensagens = [{'role': 'user', 'content': input_usuario}]
        mensagens = gera_texto(mensagens)


