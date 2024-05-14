import streamlit as st
import PyPDF4

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF4.PdfFileReader(uploaded_file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extractText()
    return text

# Function to parse text and answer queries
def parse_and_answer(text, query):
    # Your document parsing and query answering logic here
    # For simplicity, let's assume the document contains FAQ-style questions and answers
    # You can replace this with your own logic or NLP model
    faqs = text.split("\n\n")  # Assuming each FAQ is separated by double newline
    for faq in faqs:
        question,answer = faq.split("\n", 1)# Assuming question and answer are separated by single newline
        if query.lower() in question.lower():
            return answer
    return "Sorry, I couldn't find an answer to your query."

# Streamlit UI
st.title("Document Parser and Query App")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"])

if uploaded_file is not None:
    # Display file contents
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.getvalue().decode("utf-8")
    
    st.write("### Uploaded File Content:")
    # Query input
    query = st.text_input("Enter your query:", "")

    # Answer query
    if st.button("Ask"):
        answer = parse_and_answer(text, query)
        st.write("### Answer:")
        st.write(answer)
