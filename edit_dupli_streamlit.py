import PyPDF2
import streamlit as st

def delete_duplicate_pages(input_file_path, output_file_path):
    # Open the input PDF file in read binary mode
    with open(input_file_path, "rb") as input_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(input_file)

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

        # Initialize a set to store the page numbers of duplicate pages
        duplicate_page_nums = set()

        # Loop through the page numbers and identify duplicate pages
        for i in range(len(page_nums) - 1):
            if page_nums[i] == page_nums[i + 1]:
                duplicate_page_nums.add(i)
                duplicate_page_nums.add(i + 1)

        # Loop through each page of the PDF again
        for i in range(pdf_reader.getNumPages()):
            # If the current page is not a duplicate, add it to the new PDF
            if i not in duplicate_page_nums:
                pdf_writer.addPage(pdf_reader.getPage(i))

        # Save the new PDF file in write binary mode
        with open(output_file_path, "wb") as output_file:
            pdf_writer.write(output_file)

    st.success("Duplicate pages have been removed from the PDF.")

# Create the Streamlit app
st.title("Remove Duplicate Pages from PDF")
input_file = st.file_uploader("Upload a PDF file", type="pdf")

if input_file is not None:
    # Save the uploaded file to a temporary location
    with open("input_file.pdf", "wb") as f:
        f.write(input_file.getbuffer())

    # Call the delete_duplicate_pages function
    delete_duplicate_pages("input_file.pdf", "output_file.pdf")

    # Download the output file
    with open("output_file.pdf", "rb") as f:
        st.download_button("Download the output file", f.read(), file_name="output_file.pdf", mime="application/pdf")