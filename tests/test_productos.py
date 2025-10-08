import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import Usuario, Categoria, Producto

# Configurar base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestProductosAPI:
    """Pruebas unitarias para los endpoints de productos"""
    
    @classmethod
    def setup_class(cls):
        """Configuración inicial para todas las pruebas"""
        # Crear tablas
        Base.metadata.create_all(bind=engine)
        
        # Crear datos de prueba
        db = TestingSessionLocal()
        
        # Crear usuario admin
        admin = Usuario(
            id=1,
            nombre="Admin Test",
            correo="admin@test.com",
            contraseña="hashed_password",
            rol="admin",
            estado="activo"
        )
        db.add(admin)
        
        # Crear categoría
        categoria = Categoria(
            id=1,
            nombre="Electrónicos",
            descripcion="Productos electrónicos",
            activo=True
        )
        db.add(categoria)
        
        # Crear producto de prueba
        producto = Producto(
            id=1,
            nombre="iPhone 15",
            descripcion="Teléfono inteligente",
            precio=999.99,
            stock=10,
            categoria_id=1,
            imagen="/static/imagenes/test.jpg"
        )
        db.add(producto)
        
        db.commit()
        db.close()
    
    @classmethod
    def teardown_class(cls):
        """Limpieza después de todas las pruebas"""
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test.db"):
            os.remove("test.db")
    
    def test_listar_productos(self):
        """Prueba el endpoint GET /productos/"""
        response = client.get("/productos/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "nombre" in data[0]
        assert "precio" in data[0]
    
    def test_obtener_producto_existente(self):
        """Prueba el endpoint GET /productos/{id} con producto existente"""
        response = client.get("/productos/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["nombre"] == "iPhone 15"  # El producto creado en setup_class
        assert data["precio"] == 999.99
    
    def test_obtener_producto_no_existente(self):
        """Prueba el endpoint GET /productos/{id} con producto inexistente"""
        response = client.get("/productos/999")
        assert response.status_code == 404
        assert "Producto no encontrado" in response.json()["detail"]
    
    @patch('app.routers.productos.get_current_user')
    def test_crear_producto_admin(self, mock_get_current_user):
        """Prueba el endpoint POST /productos/ con usuario admin"""
        # Mock del usuario autenticado
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        # Crear archivo temporal para la imagen
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"fake image content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as f:
                files = {"imagen": ("test.jpg", f, "image/jpeg")}
                data = {
                    "admin_id": 1,
                    "nombre": "Samsung Galaxy",
                    "descripcion": "Teléfono Android",
                    "precio": 799.99,
                    "stock": 5,
                    "categoria_id": 1
                }
                
                response = client.post("/productos/", data=data, files=files)
                assert response.status_code == 200
                result = response.json()
                assert "Producto creado exitosamente" in result["mensaje"]
                assert "producto" in result
        finally:
            os.unlink(tmp_file_path)
    
    @patch('app.routers.productos.get_current_user')
    def test_crear_producto_sin_permisos(self, mock_get_current_user):
        """Prueba el endpoint POST /productos/ sin permisos de admin"""
        # Mock del usuario no admin
        mock_user = Mock()
        mock_user.id = 2
        mock_get_current_user.return_value = mock_user
        
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"fake image content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as f:
                files = {"imagen": ("test.jpg", f, "image/jpeg")}
                data = {
                    "admin_id": 2,  # Usuario no admin
                    "nombre": "Samsung Galaxy",
                    "descripcion": "Teléfono Android",
                    "precio": 799.99,
                    "stock": 5,
                    "categoria_id": 1
                }
                
                response = client.post("/productos/", data=data, files=files)
                assert response.status_code == 403
                assert "No tiene permisos" in response.json()["detail"]
        finally:
            os.unlink(tmp_file_path)
    
    @patch('app.routers.productos.get_current_user')
    def test_crear_producto_categoria_inexistente(self, mock_get_current_user):
        """Prueba el endpoint POST /productos/ con categoría inexistente"""
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"fake image content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as f:
                files = {"imagen": ("test.jpg", f, "image/jpeg")}
                data = {
                    "admin_id": 1,
                    "nombre": "Samsung Galaxy",
                    "descripcion": "Teléfono Android",
                    "precio": 799.99,
                    "stock": 5,
                    "categoria_id": 999  # Categoría inexistente
                }
                
                response = client.post("/productos/", data=data, files=files)
                assert response.status_code == 404
                assert "Categoría no encontrada" in response.json()["detail"]
        finally:
            os.unlink(tmp_file_path)
    
    @patch('app.routers.productos.get_current_user')
    def test_actualizar_producto_admin(self, mock_get_current_user):
        """Prueba el endpoint PUT /productos/{id} con usuario admin"""
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        data = {
            "admin_id": 1,
            "nombre": "iPhone 15 Pro",
            "descripcion": "Teléfono inteligente actualizado",
            "precio": 1099.99,
            "stock": 15,
            "categoria_id": 1,
            "imagen": "/static/imagenes/iphone15pro.jpg"
        }
        
        response = client.put("/productos/1", params=data)
        assert response.status_code == 200
        result = response.json()
        assert "Producto actualizado" in result["mensaje"]
    
    @patch('app.routers.productos.get_current_user')
    def test_actualizar_producto_inexistente(self, mock_get_current_user):
        """Prueba el endpoint PUT /productos/{id} con producto inexistente"""
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        data = {
            "admin_id": 1,
            "nombre": "Producto Test",
            "descripcion": "Descripción test",
            "precio": 100.00,
            "stock": 5,
            "categoria_id": 1,
            "imagen": "/static/imagenes/test.jpg"
        }
        
        response = client.put("/productos/999", params=data)
        assert response.status_code == 404
        assert "Producto no encontrado" in response.json()["detail"]
    
    @patch('app.routers.productos.get_current_user')
    def test_eliminar_producto_admin(self, mock_get_current_user):
        """Prueba el endpoint DELETE /productos/{id} con usuario admin"""
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        # Crear un producto temporal para eliminar
        db = TestingSessionLocal()
        producto_temp = Producto(
            nombre="Producto Temporal",
            descripcion="Para eliminar",
            precio=50.00,
            stock=1,
            categoria_id=1,
            imagen="/static/imagenes/temp.jpg"
        )
        db.add(producto_temp)
        db.commit()
        producto_id = producto_temp.id
        db.close()
        
        response = client.delete(f"/productos/{producto_id}?admin_id=1")
        assert response.status_code == 200
        result = response.json()
        assert "Producto eliminado" in result["mensaje"]
    
    @patch('app.routers.productos.get_current_user')
    def test_eliminar_producto_inexistente(self, mock_get_current_user):
        """Prueba el endpoint DELETE /productos/{id} con producto inexistente"""
        mock_user = Mock()
        mock_user.id = 1
        mock_get_current_user.return_value = mock_user
        
        response = client.delete("/productos/999?admin_id=1")
        assert response.status_code == 404
        assert "Producto no encontrado" in response.json()["detail"]
    
    def test_crear_producto_formato_imagen_invalido(self):
        """Prueba el endpoint POST /productos/ con formato de imagen inválido"""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_file.write(b"not an image")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as f:
                files = {"imagen": ("test.txt", f, "text/plain")}
                data = {
                    "admin_id": 1,
                    "nombre": "Producto Test",
                    "descripcion": "Descripción test",
                    "precio": 100.00,
                    "stock": 5,
                    "categoria_id": 1
                }
                
                response = client.post("/productos/", data=data, files=files)
                assert response.status_code == 400
                assert "Formato de imagen no permitido" in response.json()["detail"]
        finally:
            os.unlink(tmp_file_path)
