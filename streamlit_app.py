import os
import logging
import streamlit as st
import streamlit.components.v1 as components

from dotenv import load_dotenv
from logging import getLogger
from speech_to_text import voice_translate, detect_source_language, translate
from translation_languages import supported_languages
#from translator import detect_source_language, translate

# 환경 변수
load_dotenv()

if "msg" not in st.session_state:
    st.session_state["msg"] = ""
    
if "source_lang" not in st.session_state:
    st.session_state["source_lang"] = "English"
            
if "target_lang" not in st.session_state:
    st.session_state["target_lang"] = "Korean"   

app_logger = getLogger()
app_logger.addHandler(logging.StreamHandler())
app_logger.setLevel(logging.INFO)
            
def main():
    """Main Function"""
    #st.title('Transcription with OCI')

    #
    # tranlsate container
    #
    voice_container = st.container()
    _,voice_column,_  = st.columns([0.5,9,0.5])
    
    with st.container():
        ## VOICE
        voice_column.title('Automatic Speech Recognition')
    
        voice_column.audio_file = voice_column.file_uploader("음성 파일을 업로드해 주세요.", 
                                                            type=["m4a", "mp3", "webm", "mp4", "mpga", "wav"])
    
        # 오디오파일이 존재하는 경우,
        if voice_column.audio_file is None:
            st.session_state.vdisabled = True
            voice_column.warning("오디오 파일은 선택하여 주세요.")
        else:
            st.session_state.vdisabled = False

        #if voice_column.audio_file:
        if voice_column.button("Audio to Text", 
                                key="audiototext", 
                                type="primary",
                                disabled=st.session_state.get("vdisabled", True), 
                                use_container_width=True):
            with st.spinner("음성파일을 분석하는 중..."):
                # Translate voice to text 
                st.session_state["msg"] = voice_translate(voice_column.audio_file)
            
        #voice_column.write(st.session_state["msg"])
        voice_column.voice_text = voice_column.text_area(
            "Text",
            placeholder="Voice to Text Here...",
            max_chars=None,
            height=250,
            value=st.session_state["msg"],
            key="source_text",
            label_visibility="hidden"
        ) 
    
    st.divider()
        
    #
    # tranlsate container
    #
    translate_container = st.container()
    _,trans_column,_  = st.columns([0.5,9,0.5])

    with st.container():
        ## TRANSLATE
        trans_column.title("Translation")

        # textarea를 체크해서 lang체크 가능할까?
        if st.session_state["msg"] != "":
            with st.spinner("음성파일 언어 확인 중..."):
                st.session_state["source_lang"] = detect_source_language(st.session_state["msg"])
                #st.write(st.session_state["source_lang"])
                        
        trans_column.write(f"**Detected source language**: {st.session_state["source_lang"]} :thumbsup:")
        
        st.session_state["target_lang"] = trans_column.selectbox(
                                                "Select Language",
                                                sorted(list(supported_languages.keys())[1:]),
                                                key="target",
                                                label_visibility="hidden",
                                            )
        
        # 번역문장 체크
        if st.session_state["target_lang"] != "" and st.session_state["msg"] != "":
            st.session_state.tdisabled = False
        #     trans_column.warning("번역하실 언어를 선택하여 주세요.")
        # else:
        #     # 오디오파일, 번역문장 체크 --> 확인필요.
        #     if st.session_state["msg"] == "":
        #         st.session_state.tdisabled = True
        #         #trans_column.warning("오디오 파일은 선택 또는 번역하실 문장을 입력하여 주세요.")
        #     else:
        #         st.session_state.tdisabled = False
                        
        if trans_column.button("Translate", 
                            type="primary",
                            disabled=st.session_state.get("tdisabled", True), 
                            use_container_width=True):
            with st.spinner("번역 중..."):
                translate_text = translate(st.session_state["msg"], 
                                    st.session_state["source_lang"],
                                    st.session_state["target_lang"])
                trans_column.write(translate_text)


if __name__ == "__main__":
    
    app_logger = getLogger()
    app_logger.addHandler(logging.StreamHandler())
    app_logger.setLevel(logging.INFO)
#    app_logger.info("---------------------------")
#    app_logger.info("Voice Translation Demo")
#    app_logger.info("---------------------------")
    
    main()
