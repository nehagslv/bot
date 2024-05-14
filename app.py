import streamlit as st
import PyPDF4
def extract_text(file):
    if file.name.endswith('.pdf'):
        pdf_reader = PyPDF4.PdfFileReader(file)
        text = ''
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
        return text
    elif file.name.endswith('.txt'):
        return file.getvalue().decode('utf-8')
    else:
        return None
def chatbot(input_text):
    # Your chatbot logic here
    response = "Hello! How can I assist you today?"
    return response
st.title("Document Parser")
uploaded_file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"])
if uploaded_file is not None:
    document_text = extract_text(uploaded_file)
    if document_text:
        st.write("### Uploaded Document Content:")
    else:
        st.write("Invalid file format. Please upload a PDF or text file.")
        user_input = st.text_input("You:")
user_input = st.text_input("You:")

if user_input is not None:
    # Check if user_input is not empty and not just whitespace
    if user_input.strip() != "":
        bot_response = chatbot(user_input)
        st.text_area("Bot:", bot_response, height=100)
        st.write(bot_response)




