# modulos
from typing import Union
from fastapi import FastAPI
from implementacion import addition

# instanciacion de FASTAPI
app = FastAPI()

# primera ruta
@app.get("/")
def root():
    return {"Hola": "Nuestra primera route con FASTAPI"}

# secunda ruta
@app.get("/addicion")
def add():
    return {"Resultado 25 + 35 ": addition()}

