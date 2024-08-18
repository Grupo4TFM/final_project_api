# modulos
from fastapi import FastAPI,UploadFile
from implementacion import pdf_to_text_01
from rag import query_engine

# instanciacion de FASTAPI
app = FastAPI()

# pdf to text route
@app.post("/pdf_to_text")
async def call_pdf_to_text(my_file: UploadFile):
    recup=pdf_to_text_01(my_file.file)
    return {"data": recup}

# Basic route
@app.get("/")
def welcome():
    return {"Message": "Welcome to OBS CHATBOT  (OCB) v1.0.0"}

# Sending back the answer
@app.post("/question/{question}")
def send_question(question):
    return {"Response": query_engine.query(question)}