import streamlit as st

def get_llm_response(chain_with_history, input: str) -> str:
    """
    Get LLM response w/ Langchaing
    Args:
        chain_with_history (_type_): _description_
        input (str): _description_

    Returns:
        str: _description_
    """
    response = ""
    try:
        # Note: new messages are saved to history automatically by Langchain during run
        config = {"configurable": {"session_id": "any"}}
        response = chain_with_history.invoke({"question": input}, config)
    except ConnectionError as conerror:
        st.session_state.logger.exception(f"LLM Connection Error : {error}")
        pass
    except Exception as error:
        st.session_state.logger.error(f"get_llm_response Error : {error}")
        pass
    
    return response