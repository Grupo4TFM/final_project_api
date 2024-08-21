#############################################################
# modulos
#############################################################
import os
import time
from fastapi import FastAPI,UploadFile,File
from api.implementacion import pdf_to_text_01,tfm_download_one_file_from_s3,tfm_download_all_files_from_s3, text_to_speech, speech_to_text
from api.rag import tfm_load_data,tfm_rag_llama
from fastapi.staticfiles import StaticFiles 

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
# LOAD DATA
#############################################################

@app.post("/tfm4/load_data")
def load_data():
# try:
    tfm_load_data()
    return {"data":"files loaded successfully!!!"}
# except:
    return {"data": "files not loaded!!!"}
    
#############################################################
# Q/A LLAMA RAG
#############################################################

@app.post("/tfm4/llama_rag/{question}")
def llama_rag(question):
    try:
        result=tfm_rag_llama(question)
        return {"data":result}
    except:
         result: f"files not loaded!!!"
         return {"data": result}
    
#############################################################
# Q/A Route (RAG)
#############################################################

# @app.post("/tfm4/question/{question}")
# def send_question(question):
#     result=tfm_rag_llama(question)
#     return {"Response": result}

################################################################
# Montar carpeta que guarda audios generados por la función TTS
################################################################

# Montar la carpeta de archivos estáticos donde se guardarán los MP3
app.mount("/audio", StaticFiles(directory="audio"), name="audio")
# Asegurarse de que la carpeta 'audio' existe
if not os.path.exists("audio"):
    os.makedirs("audio")

#############################################################
# Ruta_Audio (TTS)
#############################################################
@app.post("/tfm4/question_audio/{question}")
def llama_rag_audio(question: str):
    try:
        # Obtener la respuesta de la pregunta
        result = tfm_rag_llama(question)

        # Generar un nombre de archivo único con timestamp
        timestamp = int(time.time())
        audio_filename = f"response_{timestamp}.mp3"
        audio_path = f"audio/{audio_filename}"

        # Convertir la respuesta a voz y guardarla en un archivo MP3
        text_to_speech(result, audio_path)

        # Devolver la respuesta en texto y la URL del archivo de audio
        audio_url = f"/audio/{audio_filename}"
        return {"Response": result, "Audio file URL": audio_url}
    except Exception as e:
        result = "files not loaded!!!"
        return {"data": result, "error": str(e)}
    

#############################################################
# Ruta para STT
#############################################################

@app.post("/tfm4/audio_to_text/")
async def audio_to_text(audio_file: UploadFile = File(...)):
    try:
        # Guardar temporalmente el archivo en el servidor
        audio_path = f"audio/{audio_file.filename}"
        with open(audio_path, "wb") as f:
            f.write(await audio_file.read())

        # Convertir el audio a texto
        result = speech_to_text(audio_path)

        # Borrar el archivo temporal después de convertir
        os.remove(audio_path)

        return {"Transcription": result}
    except Exception as e:
        return {"error": str(e)}
    

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
    
