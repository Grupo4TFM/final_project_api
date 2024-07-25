# modulos
from typing import Union
from fastapi import FastAPI

# instanciacion de FASTAPI
app = FastAPI()

# primera ruta
@app.get("/")
def root():
    return {"Hello": "Nuestra primera route con FASTAPI"}

# segunda ruta (prueba)
@app.get("/prueba")
def root():
    return {"prueba": "segunda ruta"}