# import the libraries
from pypdf import PdfReader
# from langchain_community.document_loaders import PyPDFLoader

# instanciation of the APP
app = FastAPI()


def pdf_to_text_01(my_pdf_file:File)->str:
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



