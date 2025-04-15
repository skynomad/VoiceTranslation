import streamlit as st
import json

from openai import OpenAI

# Speech to text
def speech_to_text(client: OpenAI, audio_path: str, model_name="whisper-1") -> str:
    try:
        transcript_text = ""
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=model_name,
                response_format="text",
                file=audio_file
            )
            
            transcript_text = transcript.text
            st.session_state.logger.info(f"Speech_to_text transcript : {transcript}") 
            
            # If transcript type is json, --> Need Check
            #transcript_text = json.loads(transcript)["text"]
            #transcript_text = transcript["text"]
           
    except Exception as error:
        st.session_state.logger.error(f"Speech_to_text Error : {error}")
        pass
    
    return transcript_text

def speech_to_text(client: OpenAI, audio_file: bytes, model_name="whisper-1") -> str:
    try:
        transcript_text = ""    
        transcript = client.audio.transcriptions.create(
            model=model_name,
            response_format="text",
            file=audio_file
        )
        
        transcript_text = transcript.text
        st.session_state.logger.info(f"Speech_to_text transcript : {transcript}") 
            
        # If transcript type is json, --> Need Check
        #transcript_text = json.loads(transcript)["text"]
        #transcript_text = transcript["text"]
           
    except Exception as error:
        st.session_state.logger.error(f"Speech_to_text Error : {error}")
        pass
    
    return transcript_text