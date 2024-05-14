import streamlit as st
import requests
def query_documents(query):
    # Make HTTP request to Snowflake Arctic API
    response = requests.post("https://snowflake-arctic-api-url/query", json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        return None
st.title("Document Parser App")

# Add file uploader
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded_file is not None:
    # Process the document
    document_text = uploaded_file.read()

    # Display the document content
    st.write("### Document Content:")
    st.write(document_text)

    # Perform a query using Snowflake Arctic model
    query = f"SELECT * FROM your_table WHERE document_text LIKE '%{search_term}%'"
    results = query_documents(query)

    # Display query results
    st.write("### Query Results:")
    for result in results:
        st.write(result)
