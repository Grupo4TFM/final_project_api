# modulos
from typing import Union
from fastapi import FastAPI

# instanciacion de FASTAPI
app = FastAPI()

# primera ruta
@app.get("/")
def root():
    return {"Hola": "Nuestra primera route con FASTAPI"}

