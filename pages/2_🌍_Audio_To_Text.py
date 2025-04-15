import os
import streamlit as st
import streamlit.components.v1 as components

import env_config as env
from env_config import init_logger, init_config
from appai_client import AIClient
from audio_recorder_streamlit import audio_recorder

from transcribe_speech_text import speech_to_text
from transcript_text_speech import text_to_speech, autoplay_audio, detect_source_language, translate_language
from langchain_llm_chatbot import get_llm_response
from translation_languages import supported_languages

# Set Page & Title
st.set_page_config(page_title="Automatic Speech Recognition", page_icon="🎙️", layout="wide")
st.subheader("🎙️ Automatic Speech Recognition")

# Setting Logger
if 'logger' not in st.session_state:
    st.session_state.logger = init_logger()
    
#######################################################################
#
def translation_selector():
    with st.sidebar:
        return st.selectbox("Select Translation Language",
                            sorted(list(supported_languages.keys())[1:]),
                            index=8,
                            label_visibility="visible")
def llm_selector():
    llm_models = ["gpt-4o", "meta-llama-3.1-8b-instruct"] 
    with st.sidebar:
        if 'llm_model_option' not in st.session_state:
            st.session_state.llm_model_option = 0
        
        llm_model = st.selectbox("Model", llm_models, index=st.session_state.llm_model_option)
        st.session_state.logger.info(f"Selected LLM Model : {llm_model}")
        st.session_state.llm_model_option = llm_models.index(llm_model)
        
        return llm_model

def llm_server_selector():
    llm_servers=["LocalAI", "Ollama","OpenAI"]
    with st.sidebar:
        with st.sidebar:
            if 'llm_server_option' not in st.session_state:
                st.session_state.llm_server_option = 0
                
        llm_server = st.selectbox("LLM Server", llm_servers, index=st.session_state.llm_server_option)
        st.session_state.logger.info(f"Selected LLM Server : {llm_server}")
        st.session_state.llm_model_option = llm_servers.index(llm_server)
        
        return llm_server

with st.sidebar:
    st.title("🎙️ Audio To Text")  
        
    # Translation Option
    translate_option = st.checkbox("Enable Translation")
    if translate_option:
        target_language = translation_selector()
        st.session_state.logger.info(f"Select Lanauge : {target_language}")

    # Generate Audio Option
    #genaudio_option = st.checkbox("Enable Generate Audio")          

#
#######################################################################

#######################################################################
#  Audio To Text
#
audio_text = None

# Check AI Client
if 'ai_client' not in st.session_state:
    # Get an OpenAI/LocalAI/Ollama Client
    ai_client = AIClient(api_key=env.api_key, 
                         base_url=env.base_url,
                         model=llm_selector())
else:
    ai_client = st.session_state.ai_client

ai_client.create_client()
client = ai_client.get_client()

st.subheader('Audio Recognition')                
audio_file = st.file_uploader("Please, Upload Audio Files.", 
                              type=["m4a", "mp3", "webm", "mp4", "mpga", "wav"])

if 'vdisabled' not in st.session_state:
    st.session_state.vdisabled = True
if 'tdisabled' not in st.session_state:
    st.session_state.tdisabled = True
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

if audio_file is None:
    st.session_state.vdisabled = True
    st.warning("Select Audio File.")
else:
    st.session_state.vdisabled = False

#if voice_column.audio_file:
if st.button(
    "Audio to Text", 
    key="audiototext", 
    type="primary",
    disabled=st.session_state.get("vdisabled", True), 
    use_container_width=True
):
    with st.spinner("Analyzing Audio..."):
        # Transcribe Audio To Text 
        transcript = speech_to_text(client, audio_file)
        st.session_state.transcript = transcript
        
audio_text = st.text_area(
    "Text",
    placeholder="Audio to Text Here...",
    max_chars=None,
    height=250,
    value=st.session_state.transcript,
    key="source_text",
    label_visibility="hidden"
)
   
st.divider()
#st.subheader('Translation')
     
# Translation == TRUE 
if translate_option:
    if target_language != "" and audio_text != "":
        st.session_state.tdisabled = False
        
if st.button(
    "Translate", 
    type="primary",
    disabled=st.session_state.get("tdisabled", True), 
    use_container_width=True
):
    # Check Transcribe Audio To Text
    if audio_text != "":
        try:
            with st.spinner("Detecting language..."):
                source_language = detect_source_language(client, audio_text, )
                st.write(f"**Detected voice language**: {source_language} :thumbsup:")    
        except Exception as error:
            st.session_state.logger.error(f"Detecting languagee Failed : {error}")
            pass
        
        try:
            with st.spinner("Translating..."):
                response_text= translate_language(client, audio_text, source_language, target_language)
                st.write(response_text)
        except Exception as error:
            st.session_state.logger.error(f"Translate Response Failed : {error}")
            pass