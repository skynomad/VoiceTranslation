import streamlit as st

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# env.config.py
base_url="http://127.0.0.1:8080/v1"
api_key="localai"

LOCALAI_BASE_URL="http://127.0.0.1:8080/v1"
LOCALAI_API_KEY="localai"

OLLAMA_BASE_URL="http://127.0.0.1:11433"
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
