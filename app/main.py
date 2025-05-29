# app/main.py

from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import usuarios
from.routers import productos


app = FastAPI()

app.include_router(usuarios.router)
app.include_router(productos.router)

# Crear tablas solo si no existen (no afecta las existentes)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensaje": "¡Bienvenido a la tienda en línea!"}
