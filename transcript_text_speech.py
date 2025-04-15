import streamlit as st

from openai import OpenAI
from translation_languages import supported_languages

def detect_source_language(client: OpenAI, input_text: str, model_name="gpt-4o") -> str:
    """
    Detect Source Languagej , Check Model : gpt-4o , meta-llama-3.1-8b-instruct
    Args:
        client (_type_): _description_
        input_text (str): _description_
        model (str, optional): _description_. Defaults to "gpt-4o".

    Returns:
        str: _description_
    """
    source_language = ""
    
    try: 
               
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a multi-language translator."},
                {
                    "role": "user",
                    "content": f"Which language is '{input_text}' written in? Explain in 1 word without punctuation.",
                },
            ],
            temperature=0,
        )
        
        source_language = response.choices[0].message.content.strip()
        st.session_state.logger.info(f"detect_source_language response : {source_language}")

        # Check Supported Languages
        # if source_language.capitalize() not in list(supported_languages.keys())[1:]:
        #     st.error(f"Detected source language '{source_language}' is not supported!")
        #     st.stop()
        
    except Exception as error:
        st.session_state.logger.error(f"detect_source_language Error : {error}")
        pass
    
    return source_language


def translate_language(client: OpenAI, input_text: str, source_language: str, target_language: str, model_name="gpt-4o") -> str:
    """
    Translate Sentence, Check Model : gpt-4o , meta-llama-3.1-8b-instruct
    Args:
        text (str): _description_
        source_language (str): _description_
        target_language (str): _description_

    Returns:
        str: _description_
    """
    translate_text = ""
    
    try:
        # Translate text and return result
        #client.timeout = 600    
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a multi-language translator.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following {source_language} text to {target_language} without summarizing and quotes: '{input_text}'",
                    #"content": f"Translate the following {source_language} text to {target_language} without quotes: '{text}'",
                },
            ],
            temperature=0
        )
        translate_text = response.choices[0].message.content.strip().replace("'", "").replace('"', "")
        st.session_state.logger.info(f"translate_language response : {translate_text}")
        
    except Exception as error:
        st.session_state.logger.error(f"translate_language Error : {error}")
        pass
            
    return translate_text

def text_to_speech(client, input_text: str) -> str:
    """
    Text to speech
    Args:
        client (_type_): AI Client
        input_text (_type_): source text for speech

    Returns:
        _type_: speech file path
    """
    try:
        
        speech_file_path = f"temp_audio_play.mp3"
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=input_text,
        ) as response:
            
            response.stream_to_file(speech_file_path)
            st.session_state.logger.info(f"text_to_speech speech_file_path : {speech_file_path}")
                
    except Exception as error:
        st.session_state.logger.error(f"text_to_speechError : {error}")
        pass
    
    return speech_file_path

def autoplay_audio(file_path: str):
    """
    Play audio
    Args:
        file_path (str): audio file path
    """
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mpeg", autoplay=True)
        
    except Exception as error:
        st.session_state.logger.error(f"Auto Play Audio Error : {error}")
        pass