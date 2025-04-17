import streamlit as st

from openai import OpenAI  
from langchain_openai import ChatOpenAI

class AIClient:
    def __init__(self, api_key, base_url, model="gpt-4o"):
        """
        OpenAI, LocalAI, Ollama등 클라이언트를 초기화합니다.

        :param api_key: OpenAI API 키
        :param model: 사용할 모델 이름 (기본값: gpt-3.5-turbo)
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        OpenAI.api_key = api_key  # OpenAI API 키 설정

    def create_client(self):
        self.ai_client = OpenAI(base_url=self.base_url,
                                api_key=self.api_key)

    def create_chatclient(self):
        self.ai_chat = ChatOpenAI(api_key=self.api_key, 
                                  base_url=self.base_url, 
                                  model=self.model)
                
    def get_client(self) -> OpenAI:
        return self.ai_client
    
    def get_chatclient(self) -> ChatOpenAI:
        return self.ai_chat
    
    def get_model_list(self) -> str:
        response = ""
        try:
            response = self.ai_client.models.list()
            st.session_state.logger.info(f"get_model_list : {response}")
        except ConnectionError as conerror:
            st.session_state.logger.error(f"API Connection Error: {conerror.strerror}")  
        except Exception as error:
            st.session_state.logger.error(f"Get Mode List Error: {error.strerror}")  
        finally:
            return response

    def generate_prompt_response(self, prompt: str, max_tokens: int=100) -> str:
        """
        주어진 프롬프트를 기반으로 OpenAI API에서 응답 생성.

        :param prompt: 사용자가 입력한 프롬프트
        :param max_tokens: 생성할 최대 토큰 수 (기본값: 100)
        :return: 생성된 텍스트 응답
        """
        try:
            response = self.ai_client.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
            
    def generate_response(self, input_text: str, max_tokens: int=100) -> str:
        try:
            response = self.ai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI chatbot having a conversation with a human."},
                    {
                        "role": "user",
                        "content": f"Answer the meaning doesn't change with question : '{input_text}'",
                    },
                ],
                max_tokens=max_tokens,
                temperature=0,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
        
    def generate_translate_response(self, source_language: str, target_language: str, input_text: str, max_tokens: int=100) -> str:
        """
        주어진 프롬프트를 기반으로 OpenAI API에서 응답 생성.

        :param input_text: 사용자가 입력한 프롬프트
        :param max_tokens: 생성할 최대 토큰 수 (기본값: 100)
        :return: 생성된 텍스트 응답
        """
        try:
            response = self.ai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI chatbot having a conversation with human also your are multi-language translator."},
                    {
                        "role": "user",
                        "content": f"Translate following {source_language} text to {target_language} with the meaning doesn't change : '{input_text}'",
                    },
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
