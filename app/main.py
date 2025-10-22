# app/main.py

from fastapi import FastAPI, Request
from .database import Base, engine
from .routers import usuarios
from .routers import productos
from .routers import carrito
from .routers import ventas
from .routers import categorias
from .routers import pagos
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

load_dotenv()

app = FastAPI()

# Crear carpeta de imágenes si no existe
os.makedirs("static/imagenes", exist_ok=True)

# Montar carpeta para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
        "http://192.168.1.3:5173",
        "http://192.168.1.3:3000",
        "http://192.168.1.3:8080",
        "http://192.168.1.3:8000",
        "http://0.0.0.0:5173",
        "http://0.0.0.0:3000",
        "http://0.0.0.0:8080",
        "http://0.0.0.0:8000",
        "*"  # Permitir todos los orígenes en desarrollo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(carrito.router)
app.include_router(ventas.router)
app.include_router(categorias.router)
app.include_router(pagos.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensaje": "¡Bienvenido a la tienda en línea!"}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": exc.status_code,
            "type": "HTTPException"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "code": 422,
            "type": "ValidationError"
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "code": 500,
            "type": "InternalServerError"
        }
    )
