import streamlit as st
import PyPDF4

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF4.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

# Streamlit UI
st.title("Document Parser App")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"])

if uploaded_file is not None:
    # Display file contents
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.getvalue().decode("utf-8")
    
    st.write("### Uploaded File Content:")
    st.write(text)

    # Query input
    query = st.text_input("Enter your query:", "")

    # Perform search
    if st.button("Search"):
        if query:
            if query.lower() in text.lower():
                st.success("Query found in the document.")
            else:
                st.error("Query not found in the document.")
        else:
            st.warning("Please enter a query.")
