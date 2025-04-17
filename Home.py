import os
import sys
import logging
import streamlit as st

from dotenv import load_dotenv
from logging import getLogger

import env_config as env
from env_config import init_logger, init_config, llm_selector, translate_option, translation_language_selector
from appai_client import AIClient
    
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Setting Logger
if 'logger' not in st.session_state:
    st.session_state.logger = init_logger()


#######################################################################
#
# Get an OpenAI/LocalAI/Ollama API Key before continuing
if not env.api_key or not env.base_url:
    st.error("Enter an API Key / Base Url to continue")
    st.stop()
        
# Sidebar
with st.sidebar:
    # Adjust image path if using locally
    # st.image("oracle-cloud-icon.png", 
    #          use_column_width=False,
    #          width=100)
    
    st.title("🏠 Home")
#    st.success("Select a demo above.")
        
#     # Support
#     st.subheader("Support")
#     st.info(
#         """
#         If you want to reward my work, I'd love a cup of coffee from you. Thanks!
#         [buymeacoffee.com/giswqs](http://buymeacoffee.com/giswqs)
#         """
#     )

    st.subheader("Translation")
    translate_option = translate_option()
        #translation_language_selector()

    
# Get an OpenAI/LocalAI/Ollama Client
# AI Client 
#   OpenAI, LocalAI, Ollama 
ai_client = AIClient(api_key=env.api_key, base_url=env.base_url, model=llm_selector())
ai_client.create_client()
st.session_state.ai_client = ai_client
#
#######################################################################

#######################################################################
#

st.subheader("AI Applications Demo")

st.markdown(
    """
    This app demonstrates various interactive AI Application created using [streamlit](https://streamlit.io)
    """
)

st.subheader("Simple Question")

input_text = st.text_input(label="Question", value="What is the Galaxy?", )
if translate_option:
    source_language = translation_language_selector(label="Select Source Language", key="Source Language", index=1)
    target_lanaguge = translation_language_selector(label="Select Target Language", key="Target Language", index=8)

if st.button('Get Response'):
    if translate_option:
        response = ai_client.generate_translate_response(source_language=source_language, target_language=target_lanaguge, input_text=input_text)
    else:
        response = ai_client.generate_response(input_text=input_text)
    
    st.write(response)    

#    response = ai_client.get_model_list()
#    st.session_state.logger.info(f"Get Mode List : {response}")
#    if response is not None:
#        st.info("API Connection Success.")
#
#    else:
#        st.info("API Connection Failed.")
    

# row1_col1, row1_col2 = st.columns(2)
# with row1_col1:
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/spain.gif")
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/las_vegas.gif")
# 
# with row1_col2:
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/goes.gif")
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/fire.gif")

#
#######################################################################
