import streamlit as st
def chatbot(input_text):
    # Your chatbot logic here
    response = "Hello! How can I assist you today?"
    return response
    st.title("Streamlit Chatbot")
st.write("Enter your message below:")
user_input = st.text_input("You:", "")
if user_input:
    bot_response = chatbot(user_input)
    st.text_area("Bot:", bot_response, height=100)
