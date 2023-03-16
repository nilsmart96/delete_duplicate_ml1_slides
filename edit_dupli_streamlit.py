import streamlit as st
import PyPDF2

st.title("PDF Reader")

# Allow the user to upload a PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a PdfFileReader object
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)

    # Extract text from the first page
    page = pdf_reader.getPage(0)
    text = page.extractText()

    # Display the extracted text
    st.write(text)