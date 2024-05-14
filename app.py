import streamlit as st
import snowflake.connector
import PyPDF4

# Connect to Snowflake
conn = snowflake.connector.connect(
    user='your_username',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='your_database',
    schema='your_schema'
)

# Function to query documents from Snowflake Arctic model
def query_documents(query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# Streamlit UI
st.title("Document Parser App")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"])

# Query input
query_input = st.text_input("Enter your query:", "")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF4.PdfFileReader(uploaded_file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extractText()
    return text

# Function to extract text from text file
def extract_text_from_text_file(uploaded_file):
    text = uploaded_file.getvalue().decode("utf-8")
    return text

# Parse and query documents
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        document_text = extract_text_from_text_file(uploaded_file)
    
    st.write("### Uploaded Document Content:")
    st.write(document_text)

    if st.button("Search"):
        query = f"SELECT * FROM your_table WHERE document_text LIKE '%{query_input}%'"
        results = query_documents(query)
        st.write("### Query Results:")
        for result in results:
            st.write(result)
