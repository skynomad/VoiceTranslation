"""
    Sppech to Text
    Reference https://github.com/coskundeniz/howcanisay
"""
import json
import logging
import os
import streamlit as st


from logging import getLogger
from dotenv import load_dotenv
from openai import OpenAI
from translation_languages import supported_languages

# 환경 변수
load_dotenv()

app_logger = getLogger()
app_logger.addHandler(logging.StreamHandler())
app_logger.setLevel(logging.INFO)

"""
# OpenAPI를 사용하는 경우, Sidebar에서 Key값 입력
api_key = st.sidebar.text_input("OpenAI API Key", 
                                type="password", 
                                value=os.getenv("OPENAI_API_KEY") or "")
if not api_key:
    st.error("OpenAPI Key를 입력해주세요.")
    st.stop()
else:
    api_key = os.getenv('OPENAI_API_KEY')
"""

# OpenAI(LocalAI) Client
api_base = os.getenv('LOCALAI_API_BASE')
api_key = os.getenv('LOCALAI_API_KEY')
if not api_key:
    st.error("LocalAI Key를 설정해주세요.")
    st.stop()
else:
    api_key = os.getenv('LOCALAI_API_KEY')
    
LocalAI_client = OpenAI(
   base_url="http://127.0.0.1:8080/v1",
   api_key=api_key
)

"""
_summary_
"""
def voice_translate(audiofile) -> str:
    #
    transcript_text = LocalAI_client.audio.transcriptions.create(
                                                        model="whisper-1",
                                                        file=audiofile,
                                                        response_format="text")
    
    #st.write(transcript_text.text)
    
    #transcript=json.loads(transcript_text)
        
    # 변환 결과
    return transcript_text.text

"""
_summary_
gpt-4o , meta-llama-3.1-8b-instruct
"""
def detect_source_language(text: str) -> str:
    #
    response = LocalAI_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a multi-language translator."},
                        {
                            "role": "user",
                            "content": f"Which language is '{text}' written in? Explain in 1 word without punctuation.",
                        },
                    ],
                    temperature=0.7,
                )

    translation_language = response.choices[0].message.content.strip()

    if translation_language.capitalize() not in list(supported_languages.keys())[1:]:
        st.error(f"Detected source language '{translation_language}' is not supported!")
        st.stop()

    app_logger.info("Translation Languate :" + translation_language)
    
    return translation_language

"""
_summary_
gpt-4o , meta-llama-3.1-8b-instruct
"""
def translate(text: str, source_language: str, target_language: str) -> str:
    
    # Translate text and return result
    LocalAI_client.timeout = 600000    
    response = LocalAI_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a multi-language translator.",
                        },
                        {
                            "role": "user",
                            "content": f"Translate the following {source_language} text to {target_language} without summarizing and quotes: '{text}'",
                            #"content": f"Translate the following {source_language} text to {target_language} without quotes: '{text}'",
                        },
                    ],
                    temperature=0.7,
                )

    app_logger.info("Translation Languate :" + response)
    
    return response.choices[0].message.content.strip().replace("'", "").replace('"', "");
