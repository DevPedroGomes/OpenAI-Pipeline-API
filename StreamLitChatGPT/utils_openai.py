import openai

# API OPENAI --------------------------

def response_generator(messages,
                            openai_key,
                            model='gpt-3.5-turbo',
                            temperature=0,
                            stream=False):
    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=stream
    )
    return response  