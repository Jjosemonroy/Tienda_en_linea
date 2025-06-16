# app/main.py

from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import usuarios
from .routers import productos
from .routers import carrito
from .routers import ventas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Crear carpeta de imágenes si no existe
os.makedirs("static/imagenes", exist_ok=True)

# Montar carpeta para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(carrito.router)
app.include_router(ventas.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensaje": "¡Bienvenido a la tienda en línea!"}
