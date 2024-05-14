import streamlit as st
import replicate
import os
from transformers import AutoTokenizer
from dotenv import load_dotenv

load_dotenv()

# App title
st.set_page_config(page_title="Snowflake Arctic")
replicate_api = None

# Replicate Credentials
with st.sidebar:
    st.title('Snowflake Arctic')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API token loaded_if!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        st.success('API token loaded_else!', icon='✅')

    if replicate_api is not None:  # Check if replicate_api is not None
        os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader("Adjust model parameters")
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.3, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)

# Store LLM-generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."}]

# Display or clear chat messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f"**Assistant:** {message['content']}")
    else:
        st.markdown(f"**User:** {message['content']}")

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."}]
st.sidebar.button('Clear chat history', on_click=clear_chat_history)

st.sidebar.caption('Built by [Snowflake](https://snowflake.com/) to demonstrate [Snowflake Arctic](https://www.snowflake.com/blog/arctic-open-and-efficient-foundation-language-models-snowflake). App hosted on [Streamlit Community Cloud](https://streamlit.io/cloud). Model hosted by [Replicate](https://replicate.com/snowflake/snowflake-arctic-instruct).')

@st.cache_resource(show_spinner=False)
def get_tokenizer():
    """Get a tokenizer to make sure we're not sending too much text
    text to the Model. Eventually we will replace this with ArcticTokenizer
    """
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")

def get_num_tokens(prompt):
    """Get the number of tokens in a given prompt"""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)

# Function for generating Snowflake Arctic response
def generate_arctic_response():
    try:
        prompt = []
        for dict_message in st.session_state.messages:
            if dict_message["role"] == "user":
                prompt.append("user\n" + dict_message["content"] + "")
            else:
                prompt.append("assistant\n" + dict_message["content"] + "")

        prompt.append("assistant")
        prompt.append("")
        prompt_str = "\n".join(prompt)

        if get_num_tokens(prompt_str) >= 3072:
            st.error("Conversation length too long. Please keep it under 3072 tokens.")
            st.button('Clear chat history', on_click=clear_chat_history, key="clear_chat_history")
            st.stop()

        for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                                      input={"prompt": prompt_str,
                                             "prompt_template": r"{prompt}",
                                             "temperature": temperature,
                                             "top_p": top_p,
                                             }):
            yield str(event)
    except replicate.exceptions.ReplicateError as e:
        st.error("An error occurred while generating the response. Please try again later.")
        st.error(f"Error details: {str(e)}")

# User-provided prompt
if prompt := st.text_input("Enter your message", key="user_input", disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    # Code snippet to generate Arctic response
    response = generate_arctic_response()
    full_response = "\n".join(response)  # Join the lines of response
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
