import logging
import streamlit as st

from dotenv import load_dotenv
from logging import getLogger
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from translation_languages import supported_languages

# env.config.py
base_url="http://127.0.0.1:8080/v1"
api_key="localai"

LOCALAI_BASE_URL="http://127.0.0.1:8080/v1"
LOCALAI_API_KEY="localai"

OLLAMA_BASE_URL="http://127.0.0.1:11434/v1"
OLLAMA_API_KEY="ollama"

OPENAI_BASE_URL="http://127.0.0.1:8080"
OPENAI_API_KEY="openai"

PROMPT = [
    ("system", "You are an AI chatbot having a conversation with a human."), 
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
]

CHATBOT_PROMPT = [
    ("system", "You are an AI chatbot having a conversation with a human."), 
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
]


def get_chatbot_promt() -> str:
    return CHATBOT_PROMPT

def init_config(llm_server:str = "LocalAI"):
    st.session_state.llm_server = llm_server
    if base_url:
        st.session_state.base_url = base_url
    else:
        st.session_state.base_url = st.sidebar.text_input("Base Url")

    if api_key:
        st.session_state.api_key = api_key
    else:
        st.session_state.api_key = st.sidebar.text_input("API Key", type="password")


def init_logger() -> logging:
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s>>>%(message)s', "%H:%M:%S")
    logger = logging.getLogger("streamlist.app")
    logger.propagate = False
    #logger.setLevel = logging.INFO
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel = logging.INFO
    logger.addHandler(stream_handler)
    
    return logger

def llm_selector_onchange():
    print("llm_selector_onchange")
    
def llm_selector(disabled: bool = False):
    #llm_models = ["llama3.2", "gpt-4o", "meta-llama-3.1-8b-instruct"] 
    llm_models = ["gpt-4o", "meta-llama-3.1-8b-instruct"] 
    with st.sidebar:
        if 'llm_model_option' not in st.session_state:
            st.session_state.llm_model_option = 0
            
        llm_model = st.selectbox("Model", 
                                 llm_models,
                                 disabled=disabled, 
                                 index=st.session_state.llm_model_option, 
                                 on_change=llm_selector_onchange())
        st.session_state.logger.info(f"Selected LLM Model : {llm_model}")
        st.session_state.llm_model_option = llm_models.index(llm_model)
        
        return llm_model

def translation_selector():
    with st.sidebar:
        return st.selectbox("Select Translation Language",
                            sorted(list(supported_languages.keys())[1:]),
                            index=8,
                            label_visibility="visible")

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