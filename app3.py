import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def display_chat_history(chain):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about your Documents", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            with st.spinner('Generating response...'):
                output = conversation_chat(user_input, chain, st.session_state['history'])

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

def create_conversational_chain(vector_store):
    tokenizer = AutoTokenizer.from_pretrained(
        "Snowflake/snowflake-arctic-instruct", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        "Snowflake/snowflake-arctic-instruct", trust_remote_code=True)

    chain = ConversationalRetrievalChain(
        vector_store=vector_store, tokenizer=tokenizer, model=model)
    return chain

def main():
    initialize_session_state()
    st.title("Multi-Docs ChatBot using llama2 :books:")
    st.sidebar.title("Document Processing")
    uploaded_files = st.sidebar.file_uploader(
        "Upload files", accept_multiple_files=True)

    if uploaded_files:
        text = []
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[1]
            if file_extension == '.txt':
                text.append(file.read().decode("utf-8"))  # Assuming text files are encoded in UTF-8
            elif file_extension == '.pdf':
                # Code for extracting text from PDF files
                pass
            elif file_extension == '.docx':
                # Code for extracting text from DOCX files
                pass
            # Add handling for other file types if necessary

        if not text:
            st.error("No text found in uploaded files. Aborting.")
            st.stop()

        # Split text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
        text_chunks = text_splitter.split_documents(text)

        # Debug output to check text chunks
        st.write("Number of text chunks:", len(text_chunks))
        st.write("Example text chunk:", text_chunks[0] if text_chunks else "No text chunks")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

        vector_store = None
        if text_chunks:
            try:
                vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
            except Exception as e:
                st.error(f"Error creating FAISS vector store: {e}")
                st.stop()

        if vector_store is None:
            st.error("Failed to create FAISS vector store. Aborting.")
            st.stop()

        chain = create_conversational_chain(vector_store)
        display_chat_history(chain)

if __name__ == "__main__":
    main()
