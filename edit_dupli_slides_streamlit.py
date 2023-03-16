import PyPDF2
import streamlit as st

input_file = st.file_uploader("Upload a PDF file", type="pdf")

# Open the PDF file in read binary mode
pdf_file = open(input_file, "rb")

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Create a PDF writer object
pdf_writer = PyPDF2.PdfWriter()

# Initialize a list to store the page numbers
page_nums = [0]

# Loop through each page of the PDF
for i, page in enumerate(pdf_reader.pages):
    # Extract the text from the page
    text = page.extract_text()

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
for i, page in enumerate(pdf_reader.pages):
    # If the current page is not in del_list, add it to the new PDF
    if i not in del_list:
        pdf_writer.add_page(page)

# Save the new PDF file in write binary mode
output_file = open("lecture_1_print.pdf", "wb")
pdf_writer.write(output_file)

st.download_button("Download the output file", output_file.read(), file_name="output_file.pdf", mime="application/pdf")

# Close the PDF files
pdf_file.close()
output_file.close()