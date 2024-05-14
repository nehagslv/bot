import streamlit as st
from PyPDF import PdfFileReader

# Define your chatbot function
def chatbot(input_text):
    # Your chatbot logic here
    response = "Hello! How can I assist you today?"
    return response

# Streamlit UI
st.title("Chatbot with File Upload")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"])

if uploaded_file is not None:
    # Display file contents
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfFileReader(uploaded_file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    else:
        text = uploaded_file.getvalue().decode("utf-8")
    
    st.write("### Uploaded File Content:")
    st.write(text)

    # Chatbot interface
    user_input = st.text_input("You:", "")
    if user_input:
        bot_response = chatbot(user_input)
        st.text_area("Bot:", bot_response, height=1000)
