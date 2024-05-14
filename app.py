import streamlit as st

def main():
    st.title("Document Parser App")
    st.write("Upload a document and let the magic happen!")

    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        st.write("### Uploaded Document:")
        st.write(file_contents)

if __name__ == "__main__":
    main()
