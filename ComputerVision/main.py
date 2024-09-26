import os
from dotenv import load_dotenv, find_dotenv
import openai
import streamlit as st
import base64


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Obtém a chave da API do OpenAI do arquivo .env
api_key = os.getenv("OPENAI_API_KEY")

# Configura a chave da API do OpenAI
openai.api_key = api_key

@st.cache_data
def get_ice_servers():
    return [{'urls': ['stun:stun.1.google.com:19302']}]

# ENCODE AND ANALYZE FUNCTIONS

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(prompt, file):
    base_64_img = encode_image(file)
    response = openai.ChatCompletion.create(
        model='gpt-4-turbo',
        messages=[
            {
                'role': 'user',
                'content': f"{prompt}\n![image](data:image/jpeg;base64,{base_64_img})"
            }
        ],
        max_tokens=1000,
    )
    text = response['choices'][0]['message']['content']
    return st.write(text)

# MAIN ------------------

def main():
    st.markdown("""
        <style>
        .centered-header {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="centered-header">This is the Analyzer</h1>', unsafe_allow_html=True)
    
    st.markdown('### Type your instructions about what you want to check from your image provided')
    st.divider()
    
    prompt_input = st.text_area('Type your prompt', height=200, key='input_image')
    image_file = st.file_uploader('Add image file', type=['jpeg', 'png'])
    
    if prompt_input and image_file:
        analyze_button = st.button('Analyze')
        if analyze_button:
            analyze_image(prompt_input, image_file)
    else:
        st.button('Analyze', disabled=True)
    
if __name__ == '__main__':
    main()
