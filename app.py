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
    faqs = text.split("\n\n")  # Split text into FAQs assuming each FAQ is separated by double newline
    for faq in faqs:
        parts = faq.split("\n", 1)  # Split FAQ into question and answer assuming they are separated by a newline
        if len(parts) == 2:  # Ensure both question and answer are present
            question, answer = parts
            if query.lower() in question.lower():
                return answer.strip()  # Strip leading/trailing whitespaces from answer
        elif len(parts) == 1:  # Handle cases where question and answer are not separated by a newline
            if query.lower() in faq.lower():
                return "FAQ found but answer format is not recognized. Please ensure each FAQ is formatted as 'Question\\nAnswer'."
        # Else: Skip FAQ if it doesn't have both question and answer or doesn't match query

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
