import streamlit as st
import PyPDF2
import io

# Create a file uploader in Streamlit
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# If the user has uploaded a file
if uploaded_file is not None:
    # Open the PDF file in read binary mode using PyPDF2
    pdf_file = io.BytesIO(uploaded_file.getvalue())
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Process the PDF file and create a new PDF writer object
    pdf_writer = PyPDF2.PdfFileWriter()
    page_nums = [0]

    for i, page in enumerate(pdf_reader.pages):
        text = page.extractText()

        try:
            gregory_loc = text.index("Gregory")
            page_num_1 = text[gregory_loc + 17]
            page_nums.append(int(page_num_1))

            try:
                page_num_2 = text[gregory_loc + 18]
                del page_nums[-1]
                page_nums.append(int(page_num_1 + page_num_2))

            except IndexError:
                continue

        except ValueError:
            page_nums.append(page_nums[-1] + 1)

    del_list = []
    i = 1

    while i < len(page_nums):
        if page_nums[i - 1] == page_nums[i]:
            del_list.append(i - 2)

        i += 1

    for i, page in enumerate(pdf_reader.pages):
        if i not in del_list:
            pdf_writer.addPage(page)

    # Create a download link for the new PDF file
    stream = io.BytesIO()
    pdf_writer.write(stream)
    stream.seek(0)
    st.download_button(
        label="Download updated PDF",
        data=stream,
        file_name="updated.pdf",
        mime="application/pdf"
    )