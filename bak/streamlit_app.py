import streamlit as st

st.set_page_config(
    page_title="Voice & Chat Bot",
    page_icon="🎙️",
)

st.write("# Voice & Chat Bot With LLMs 🎙️")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Voice & Chat Bot With LLMs 👋
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more about GenAI?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
)