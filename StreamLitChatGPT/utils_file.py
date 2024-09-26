import re
from pathlib import Path
import pickle
from unidecode import unidecode

CONFIG_FOLDER = Path(__file__).parent / 'config'
CONFIG_FOLDER.mkdir(exist_ok = True)
MESSAGES_FOLDER = Path(__file__).parent / 'messages'
MESSAGES_FOLDER.mkdir(exist_ok = True)
CACHE_DENCOVERT = {}
   

def convert_message_name(message_name):
    file_name = unidecode(message_name)
    file_name = re.sub('\w+', '', file_name.lower())
    return file_name

def read_message_byFileName(file_name, key='message'):
    message_name = retrieve_message_name(messages)
    file_name = convert_message_name(message_name)
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def deconvert_message_name(file_name):
    if not file_name in CACHE_DENCOVERT:
        message_name = read_message_byFileName(file_name, key='message_name')
        CACHE_DENCOVERT[file_name] = message_name
        return CACHE_DENCOVERT[file_name]

def retrieve_message_name(messages):
    message_name = ''
    for message in messages:
        if message['role'] == 'user':
            message_name = message['content'][:30]
            break
    return message_name

def save_messages(messages):
    if len(messages) == 0:  
        return False
    message_name = retrieve_message_name(messages)
    file_name = convert_message_name(message_name)
    file_save = {'message_name': message_name,
                 'file_name': file_name,
                 'message': messages}
    with open(MESSAGES_FOLDER / file_name, 'wb') as f:
        pickle.dump(file_save, f)

def read_message_byFileName(file_name, key='messages'):  # Adicionado argumento `messages`
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def read_messages(messages, key='messages'):
    if len(messages) == 0:
        return []
    message_name = retrieve_message_name(messages)
    file_name = convert_message_name(message_name)
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]    

def list_chats():
    chats = list(MESSAGES_FOLDER.glob('*'))
    chats = sorted(chats, key=lambda item: item.stat().st.mtime.ns, reverse=True)
    return [c.stem for c in chats]

# SAVE AND READ APIKEY

def save_key(key):
    with open(CONFIG_FOLDER / 'key', 'wb') as f:
        pickle.dump(key, f)


def read_key():
    if (CONFIG_FOLDER / 'key').exists():
        with open(CONFIG_FOLDER / 'key', 'rb') as f:
            return pickle.load(f)
    else:
        return ''
