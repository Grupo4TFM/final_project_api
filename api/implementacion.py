# import the libraries
import os
from pypdf import PdfReader

def pdf_to_text_01(my_pdf_file)->str:
    """
    function accepting a pdf file as input and returning a text as output
    """
    text = ""
    try:
        reader = PdfReader(my_pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except:
        pass
    finally:
        return text



