# modulos
from typing import Union
from fastapi import FastAPI,UploadFile
from implementacion import pdf_to_text_01

# instanciacion de FASTAPI
app = FastAPI()

# root
@app.get("/")
def welcome():
    return {"data": "welcome"}

# pdf to text route
@app.post("/pdf_to_text")
async def call_pdf_to_text(my_file: UploadFile):
    recup=pdf_to_text_01(my_file.file)
    return {"data": recup}

