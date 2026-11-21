
import pymupdf

def extract_text_from_pdf(pdf_file):

    # Open PDF file
    document = pymupdf.open(
        stream=pdf_file.getvalue(),
        filetype="pdf"
    )

    extracted_text = ""

    # Extract text from every page
    for page_number, page in enumerate(document):

        text = page.get_text()

        extracted_text += (
            f"\n--- Page {page_number + 1} ---\n"
            + text
        )

    document.close()

    return extracted_text
