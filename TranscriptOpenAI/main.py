import os
from dotenv import load_dotenv, find_dotenv
import openai
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from pathlib import Path
from moviepy.editor import VideoFileClip
import time
import pydub
import queue
load_dotenv(find_dotenv())

api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

pydub.AudioSegment.converter = 'ffmpeg'

FOLDER_TEMP = Path(__file__).parent / 'temp'
FOLDER_TEMP.mkdir(exist_ok=True)

FILE_AUDIO_TEMP = FOLDER_TEMP / 'audio.mp3'
FILE_VIDEO_TEMP = FOLDER_TEMP / 'video.mp4'
FILE_MIC_TEMP = FOLDER_TEMP / 'mic.mp3'

if not 'transcription_mic' in st.session_state:
    st.session_state['transcription_mic'] = ''

@st.cache_data
def get_ice_servers():
    return [{'urls': ['stun:stun.1.google.com:19302']}]


def transcribe_audio(audio_path, prompt):
    with open(audio_path, 'rb') as audio_file:
        transcription = openai.audio.transcriptions.create(
            model='whisper-1',
            language='en',
            file=audio_file,
            prompt=prompt,
        )
        return transcription


# AUDIO TRANSCRIPT
def add_audio_chunks(audio_frames, chunk_audio):
    for frame in audio_frames:
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels)
        )
        chunk_audio += sound
    return chunk_audio

def transcribe_tab_mic():
    prompt_mic = st.text_input('(Optional) Type your prompt', key='input_mic')
    webrtx_ctx = webrtc_streamer(
        key='receive_audio',
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={'iceServers': get_ice_servers()},
        media_stream_constraints={'video':False, 'audio':True}
    )
    if not webrtx_ctx.state.playing:
        st.write(st.session_state['transcription_mic'])
        return
    
    container = st.empty()
    container.markdown("Start talking...")
    chunk_audio = pydub.AudioSegment.empty()
    last_transcription_time = time.time()
    st.session_state['transcription_mic'] = ''
    while True:
        if webrtx_ctx.audio_receiver:
            try:
                audio_frame = webrtx_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue
            
            chunk_audio = add_audio_chunks(audio_frame, chunk_audio)
            now = time.time()
            if len(chunk_audio) > 0 and now - last_transcription_time > 10:
                last_transcription_time = now
                chunk_audio.export(FILE_MIC_TEMP)
                # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # unique_file_name = FOLDER_TEMP / f'mic_{timestamp}.mp3'

                # # Salvar o áudio com o nome de arquivo único
                # chunk_audio.export(unique_file_name)                
                transcription = transcribe_audio( FILE_MIC_TEMP, prompt_mic)
                st.session_state['transcription_mic'] += transcription
                container.write(st.session_state['transcription_mic'])
                chunk_audio = pydub.AudioSegment.empty()

        else:
            break    

# def transcribe_tab_mic():
#     prompt_mic = st.text_input('(Optional) Type your prompt', key='input_mic')
#     webrtc_ctx = webrtc_streamer(
#         key='receive_audio',
#         mode=WebRtcMode.SENDONLY,
#         audio_receiver_size=1024,
#         rtc_configuration={'iceServers': get_ice_servers()},
#         media_stream_constraints={'video': False, 'audio': True}
#     )
#     if not webrtc_ctx.state.playing:
#         return

#     container = st.empty()
#     container.markdown("Start talking...")
#     chunk_audio = pydub.AudioSegment.empty()
#     last_transcription_time = time.time()

#     while True:
#         if webrtc_ctx.audio_receiver:
#             try:
#                 audio_frame = webrtc_ctx.audio_receiver.get_frames(timeout=1)
#             except queue.Empty:
#                 time.sleep(0.1)
#                 continue

#             for frame in audio_frame:
#                 sound = pydub.AudioSegment(
#                     data=frame.to_ndarray().tobytes(),
#                     sample_width=frame.format.bytes,
#                     frame_rate=frame.sample_rate,
#                     channels=len(frame.layout.channels)
#                 )
#                 chunk_audio += sound

#             now = time.time()
#             if len(chunk_audio) > 0 and now - last_transcription_time > 5:
#                 container.markdown("Saving audio")

#                 # Gerar um nome de arquivo único usando a data e hora atuais
#                 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                 unique_file_name = FOLDER_TEMP / f'mic_{timestamp}.mp3'

#                 # Salvar o áudio com o nome de arquivo único
#                 chunk_audio.export(unique_file_name, format='mp3')
#                 container.markdown(f"Audio saved as {unique_file_name}")

#                 with open(unique_file_name, 'rb') as audio_file:
#                     transcription = openai.audio.transcriptions.create(
#                         model='whisper-1',
#                         language='en',
#                         file=audio_file,
#                         prompt=prompt_mic,
#                     )
#                 st.write(transcription)

#                 # Resetar chunk_audio e atualizar last_transcription_time
#                 chunk_audio = pydub.AudioSegment.empty()
#                 last_transcription_time = now

#             container.markdown(f'Frames received {len(audio_frame)}')
#         else:
#             break    


# TRANSCRIBE VIDEO FILE -----------

def save_audio_video(video_bytes):
    with open(FILE_VIDEO_TEMP, mode='wb') as video_f:
            video_f.write(video_bytes.read())
    moviepy_video = VideoFileClip(str(FILE_VIDEO_TEMP))
    moviepy_video.write_audiofile(str(FILE_AUDIO_TEMP))
    
def transcribe_tab_video():
    prompt_video = st.text_input('(Optional) Type your prompt', key='input_video')
    video_file = st.file_uploader('Add .mp4 video file', type=['mp4'])
    if not video_file is None:
        save_audio_video(video_file)
        transcription = transcribe_audio( FILE_AUDIO_TEMP, prompt_video)
        st.write(transcription)
        
        
# TRANSCRIBE AUDIO FILE ----------
def transcribe_tab_audio():
    prompt_input = st.text_input('(Optional) Type your prompt', key='input_audio')
    audio_file = st.file_uploader('Add .mp3 audio file', type=['mp3'])
    if not audio_file is None:
        transcription = openai.audio.transcription.create(
            model='whisper-1',
            language='en',
            response_format='text',
            file=audio_file,
            prompt=prompt_input
        )
        st.write(transcription)
    

# MAIN -------------
def main():
    st.header("Welcome to Audio-Transcript!", divider=True)
    st.markdown("### Transcribe audio from microphone, video or audio file")
    
    tab_mic, tab_video, tab_audio = st.tabs([' Microphone', 'Video', 'Audio'])
    with tab_mic:
        transcribe_tab_mic()
    
    with tab_video:
        transcribe_tab_video()
    
    with tab_audio:
        transcribe_tab_audio()

if __name__ == '__main__':
    main()