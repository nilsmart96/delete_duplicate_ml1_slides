import streamlit as st
import PyPDF2
from io import BytesIO

st.set_page_config(page_title="PDF Pages Deleter", page_icon=":books:", layout="wide")

# Define the function to delete duplicate pages
def delete_duplicate_pages(input_file):
    # Open the PDF file in read binary mode
    pdf_file = open(input_file, "rb")

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfFileWriter()

    # Initialize a list to store the page numbers
    page_nums = [0]

    # Loop through each page of the PDF
    for i in range(pdf_reader.getNumPages()):
        # Get the page object
        page = pdf_reader.getPage(i)

        # Extract the text from the page
        text = page.extractText()

        try:
            # Find the index of the text "Gregory"
            gregory_loc = text.index("Gregory")

            # Get the page number at the bottom right
            page_num_1 = text[gregory_loc + 17]
            page_nums.append(int(page_num_1))

            try:
                # If the page number has two digits
                page_num_2 = text[gregory_loc + 18]
                # Replace the last element in page_nums with the two-digit page number
                del page_nums[-1]
                page_nums.append(int(page_num_1 + page_num_2))

            except IndexError:
                # If the page number has one digit, do nothing
                continue

        except ValueError:
            # If "Gregory" is not found, increment the previous page number by 1
            page_nums.append(page_nums[-1] + 1)

    # Initialize a list to store the indices of pages to delete
    del_list = []
    i = 1
    while i < len(page_nums):
        # If two consecutive pages have the same page number
        if page_nums[i - 1] == page_nums[i]:
            # Add the index of the previous page to del_list
            del_list.append(i - 2)

        i += 1

    # Loop through each page of the PDF again
    for i in range(pdf_reader.getNumPages()):
        # If the current page is not in del_list, add it to the new PDF
        if i not in del_list:
            pdf_writer.addPage(pdf_reader.getPage(i))

    # Save the new PDF file in write binary mode
    output_file = BytesIO()
    pdf_writer.write(output_file)

    # Close the PDF files
    pdf_file.close()

    return output_file


# Define the main function
def main():
    st.title("Delete Duplicate Pages in PDF")

    # Upload the PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Delete duplicate pages
        output_file = delete_duplicate_pages(uploaded_file)

        # Download the new PDF file
        st.download_button("Download the new PDF file", output_file.getvalue(), file_name="new_pdf_file.pdf")


if __name__ == "__main__":
    main()