#############################################################
# modulos
#############################################################

from fastapi import FastAPI,UploadFile
from implementacion import pdf_to_text_01,tfm_download_one_file_from_s3,tfm_download_all_files_from_s3
from rag import tfm_rag_llama
from models import Question,Response


#############################################################
# instanciacion de FASTAPI
#############################################################

app = FastAPI()

#############################################################
# Welcome route
#############################################################

@app.get("/")
def welcome():
    return {"Message": "Welcome to OBS CHATBOT  (OCB) v1.0.0"}

#############################################################
# Q/A Route (RAG)
#############################################################

@app.post("/tfm4/question/{question}")
def send_question(question):
    result=tfm_rag_llama(question)
    return {"Response": result}

#############################################################
# Pdf to text route
#############################################################

@app.post("/tfm4/pdf_to_text")
async def call_pdf_to_text(my_file: UploadFile):
    recup=pdf_to_text_01(my_file.file)
    return {"data": recup}

#############################################################
# Load one file from S3 
#############################################################

@app.post("/tfm4/load_one_file_from_s3/")
async def load_one_file_from_s3(my_file:str):
    try:
        tfm_download_one_file_from_s3(my_file)
        result=f"file {my_file} loaded successfully!!!"
        return {"data":result}
    except:
        result: f"file {my_file} not loaded!!!"
        return {"data": result}
    
#############################################################
# Load all files from S3 
#############################################################

@app.post("/tfm4/load_all_files_from_s3")
async def load_all_files_from_s3():
    try:
        result=tfm_download_all_files_from_s3()
        return {"data": result}
    except:
        return {"data": f"files not loaded!!!"}