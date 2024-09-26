import os
from dotenv import load_dotenv, find_dotenv
import openai
import streamlit as st

from utils_file import *
_ = load_dotenv(find_dotenv())

openai_key = os.getenv("OPENAI_API_KEY")

openai.api_key = openai_key

from utils_openai import response_generator

# INITIALIZATION----------

def initialization():
    if not 'messages' in st.session_state:
        st.session_state['messages'] = []
    if not 'current_chat' in st.session_state:
        st.session_state['current_chat'] = ''  
    if not 'model' in st.session_state:
        st.session_state['model'] = 'gpt-3.5-turbo' 
    if not 'api_key' in st.session_state:
        st.session_state['api_key'] = read_key()         

# MAIN PAGE -----------
def main_page():  
    
    messages = read_messages(st.session_state['messages'])
        
    st.header("PG's ChatBot", divider=True)
    
    for message in messages:
        chat = st.chat_message(message['role'])
        chat.markdown(message['content'])
        
    prompt = st.chat_input('Talk to Chat')
    if prompt:
        if st.session_state['api_key'] == '':
            st.error("Add an API Key on Config tab")
        else:
                
            new_message = {'role': 'user', 'content': prompt}
            
            chat = st.chat_message(new_message['role'])
            chat.markdown(new_message['content'])
            messages.append(new_message)
            
            chat = st.chat_message('assistant')
            
            placeholder = chat.empty()
            placeholder.markdown('')
    
            response_complete = ''
            
            responses = response_generator(messages,
                                           st.session_state['api_key'],
                                           model = st.session_state['model'],
                                           stream=True)
            
            for response in responses:
                response_complete += response.choices[0].delta.get('content', '')
                placeholder.markdown(response_complete + '')
                placeholder.markdown(response_complete)    
            new_message = {'role': 'assistant', 'content': response_complete}
            
            messages.append(new_message)
            
            st.session_state['messages'] = messages
            save_messages(messages)


# TABS -----------------


def tab_chat(tab):
    tab.button('+ New Chat',
           on_click=select_chat,
           args=('', ),
           use_container_width=True)
    tab.markdown('')
    chats = list_chats()
    for file_name in chats:
        message_name = deconvert_message_name(file_name).capitalize()
        if len(message_name) == 30:
            message_name += '...'
        tab.button(message_name,
               on_click=select_chat,
               args=(file_name, ),
               disabled=file_name==st.session_state['current_chat'],
               use_container_width=True)
    
def select_chat(file_name):  
    if file_name == '':
        st.session_state['messages'] = []
    else:
        message = read_message_byFileName(file_name)  
        st.session_state['messages'] = message 
    st.session_state['current_chat'] = file_name


def tab_configuration(tab):
    model_chosen = tab.selectbox('Select Model',
                  ['gpt-3.5-turbo', 'gpt-4'])
    st.session_state['model'] = model_chosen
    
    key = tab.text_input('Add your API Key', value= st.session_state['api_key'])
    if key != st.session_state['api_key']:
        st.session_state['api_key'] = key
        save_key(key)
        tab.success('Key saved successfully')

# SET ----------------


def main():
    initialization()
    main_page()
    tab1, tab2 = st.sidebar.tabs(['Chats', 'Configuration'])
    tab_chat(tab1)
    tab_configuration(tab2)
    
    
if __name__ == '__main__':
    main()    


        