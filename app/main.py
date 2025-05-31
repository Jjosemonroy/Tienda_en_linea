# app/main.py

from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import usuarios
from.routers import productos
from.routers import carrito
from.routers import ventas
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # tu frontend
    allow_credentials=True,
    allow_methods=["*"],                      # permite GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],                      # permite headers como Authorization, Content-Type, etc.
)

app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(carrito.router)
app.include_router(ventas.router)

# Crear tablas solo si no existen (no afecta las existentes)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensaje": "¡Bienvenido a la tienda en línea!"}
