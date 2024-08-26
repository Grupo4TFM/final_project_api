#############################################################
# modulos
#############################################################

from fastapi import FastAPI,UploadFile
from api.implementacion import pdf_to_text_01,tfm_download_one_file_from_s3,tfm_download_all_files_from_s3,tfm_delete_folder,tfm_create_folder
from api.rag import tfm_load_data,tfm_rag_llama,tfm_load_data_with_parameters
from api.models import DeleteFolderRequest,CreateFolderRequest

#############################################################
# instanciacion de FASTAPI
#############################################################

app = FastAPI()

#############################################################
# Welcome route
#############################################################

@app.get("/",tags=["INFO"])
def welcome():
    return {"Message": "Welcome to OBS CHATBOT  (OCB) v1.0.0"}

#############################################################
# CREATE FOLDER IN S3
#############################################################

@app.post("/tfm4/s3/tfm_create_folder",tags=["S3"])
async def tfm_route_create_folder(request:CreateFolderRequest):
    try:    
        bucket = request.bucket
        folder_name = request.folder_name
        result=tfm_create_folder(folder_name,bucket)
        if result==True:
            return {"data":"Folder created!!!"}
        else : 
            return {"data":"Folder not created!!!"}
    except:
        return {"data": "Folder not created!!!"}

#############################################################
# DELETE FOLDER IN S3
#############################################################

@app.delete("/tfm4/s3/tfm_delete_folder",tags=["S3"])
async def tfm_route_delete_folder(request: DeleteFolderRequest):
    try:    
        bucket = request.bucket
        folder_name = request.folder_name
        tfm_delete_folder(bucket,folder_name)
        return {"data":"Folder deleted!!!"}
    except:
        return {"data": "Folder not deleted!!!"}

#############################################################
# Load one file from S3 
#############################################################

@app.post("/tfm4/s3/load_one_file_from_s3/",tags=["S3"])
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

@app.post("/tfm4/s3/load_all_files_from_s3",tags=["S3"])
async def load_all_files_from_s3():
    try:
        result=tfm_download_all_files_from_s3()
        return {"data": result}
    except:
        return {"data": f"files not loaded!!!"}

#############################################################
# LOAD DATA SIMPLE
#############################################################

@app.post("/tfm4/load_data",tags=["RAG"])
def load_data():
# try:
    tfm_load_data()
    return {"data":"files loaded successfully!!!"}
# except:
    return {"data": "files not loaded!!!"}

#############################################################
# LOAD DATA SIMPLE WITH PARAMETERS
#############################################################

@app.post("/tfm4/load_data_with_parameters",tags=["RAG"])
def load_data_with_parameters(llm_model,embedding_model,embed_batch_size,chunk_size,chunk_overlap):
    try:
        tfm_load_data_with_parameters(llm_model,embedding_model,int(embed_batch_size),int(chunk_size),int(chunk_overlap))
        return {"data":"files loaded successfully!!!"}
    except:
        return {"data": "files not loaded!!!"}

#############################################################
# Q/A LLAMA RAG
#############################################################

@app.post("/tfm4/llama_rag/{question}",tags=["RAG"])
def llama_rag(question):
    try:
        result=tfm_rag_llama(question)
        return {"data":result}
    except:
         result: f"files not loaded!!!"
         return {"data": result}

#############################################################
# Pdf to text route
#############################################################

@app.get("/tfm4/pdf_to_text",tags=["ROUTINES"])
async def call_pdf_to_text(my_file: UploadFile):
    recup=pdf_to_text_01(my_file.file)
    return {"data": recup}

