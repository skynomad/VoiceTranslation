import os
import streamlit as st

import env_config as env
from env_config import init_logger, init_config
from appai_client import AIClient
from audio_recorder_streamlit import audio_recorder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from transcribe_speech_text import speech_to_text
from transcript_text_speech import text_to_speech, autoplay_audio, detect_source_language, translate_language
from langchain_llm_chatbot import get_llm_response
from translation_languages import supported_languages

# Set Page & Title
st.set_page_config(page_title="Voice & Chat Bot With LLMs", page_icon="🎙️", layout="wide")
st.title("🎙️ Voice & Chat Bot")

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
    st.title("🎙️ Voice & Chat Bot")
    
    # Translation
    #st.subheader("Translation")       
    
    # Translation Option
    translate_option = st.checkbox("Enable Translation")
    if translate_option:
        target_language = translation_selector()
        st.session_state.logger.info(f"Select Lanauge : {target_language}")

    # Generate Audio Option
    genaudio_option = st.checkbox("Enable Generate Audio")
                
    audio_bytes = audio_recorder("🎤 Click and Speak",
                                 icon_size= "2x",
                                 pause_threshold=1.0, 
                                 sample_rate=16_000)
#
#######################################################################

#######################################################################
#  Voice ChatBot
#
#audio_bytes = None

# Check AI Client
if 'ai_client' not in st.session_state:
    # Get an OpenAI/LocalAI/Ollama Client
    ai_client = AIClient(api_key=env.api_key, 
                         base_url=env.base_url,
                         model=llm_selector())
else:
    ai_client = st.session_state.ai_client

ai_client.create_client()
ai_client.create_chatclient()
    
# Manage chat message history
#   Stores messages in the Streamlit session state
#   Eliminating the need for manual management.
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Set up the LangChain, passing in Message History
#   To interact with the LLM
#   Responsible for both reading and updating the chat message history.
prompt = ChatPromptTemplate.from_messages(env.CHATBOT_PROMPT)


client = ai_client.get_client()
chatclient = ai_client.get_chatclient()
chain = prompt | chatclient
chain_with_history = RunnableWithMessageHistory(chain,
                                                lambda session_id: msgs,
                                                input_messages_key="question",
                                                history_messages_key="history")

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)


# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
   st.chat_message("human").write(prompt)
   msgs.add_user_message(prompt)
   audio_bytes = None

# If audio bytes are available, transcribe and add to chat history
if audio_bytes is not None:
    try:
        # Write the audio bytes to a file
        with st.spinner("Transcribing..."):
            file_path = f"temp_audio.mp3"
            with open(file_path, "wb") as f:
                f.write(audio_bytes)

            # STT
            transcript = speech_to_text(client, file_path)
            if transcript:
                st.chat_message("human").write(transcript)
                msgs.add_user_message(transcript)
            
            # Transcription (?)
                                                  
    except Exception as error:
        st.session_state.logger.error(f"Speech Translation  Response Error : {error}")
    finally:
        audio_bytes = None      
        try:
            # audio file cleanup
            os.remove(file_path)
        except Exception as error:
            st.session_state.logger.error(f"Speech Translation Temp Audio File Remove Failed : {error}")
            pass
            
     
# If last message is not from the AI, generate a new response
if st.session_state.langchain_messages[-1].type != "ai":
    try:
        with st.chat_message("ai"):
            with st.spinner("Thinking 🤔 ..."):
                response = get_llm_response(chain_with_history,
                                                      st.session_state.langchain_messages[-1].content)
                response_text = response.content

            try:
                # Translation == TRUE 
                if translate_option:
                    with st.spinner("Detecting language..."):
                        source_language = detect_source_language(client, response_text, )
                        st.write(f"**Detected voice language**: {source_language} :thumbsup:")
                    
                    with st.spinner("Translating..."):    
                        response_text= translate_language(client, response_text, source_language, target_language)
            except Exception as error:
                st.session_state.logger.error(f"Translate Response ailed : {error}")
                pass
                        
            st.write(response_text)
            
            if genaudio_option:
                with st.spinner("Generating audio response..."):
                    audio_file = text_to_speech(client, response_text)
                    autoplay_audio(audio_file)
                
                os.remove(audio_file)
                
    except Exception as error:
        st.session_state.logger.error(f"Generate New Response with LLM Failed : {error}")
        #st.session_state.logger.error(error, stack_info=False, exc_info=True)
        st.error("AI Generate Response Failed.")
        pass