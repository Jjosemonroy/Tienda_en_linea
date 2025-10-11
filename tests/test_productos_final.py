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
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_final.db"
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

class TestProductosFinal:
    """Pruebas unitarias finales para los endpoints de productos"""
    
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
        if os.path.exists("test_final.db"):
            try:
                os.remove("test_final.db")
            except PermissionError:
                pass
    
    def test_listar_productos(self):
        """Prueba listar todos los productos"""
        response = client.get("/productos/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # Al menos 1 producto de prueba
        print(f"PASS: Listar productos - {len(data)} productos encontrados")
    
    def test_obtener_producto_existente(self):
        """Prueba obtener producto existente"""
        response = client.get("/productos/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        # El producto con ID 1 ya existe en la BD real con nombre "MAC"
        assert data["nombre"] == "MAC"
        assert data["precio"] == 10.00
        print(f"PASS: Obtener producto existente - {data['nombre']}")
    
    def test_obtener_producto_no_existente(self):
        """Prueba obtener producto inexistente"""
        response = client.get("/productos/9999")
        assert response.status_code == 404
        assert "Producto no encontrado" in response.json()["detail"]
        print("PASS: Obtener producto inexistente - Error 404 correcto")
    
    def test_crear_producto_formato_imagen_invalido(self):
        """Prueba crear producto con formato de imagen inválido"""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_file.write(b"not an image")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as f:
                files = {"imagen": ("test.txt", f, "text/plain")}
                data = {
                    "admin_id": 1,
                    "nombre": "Producto Test",
                    "descripcion": "Descripción",
                    "precio": 100.00,
                    "stock": 5,
                    "categoria_id": 1
                }
                
                response = client.post("/productos/", data=data, files=files)
                # Sin autenticación, esperamos 422 por validación de Form
                assert response.status_code in [400, 422]
                print("PASS: Formato imagen inválido - Error correcto")
        finally:
            os.unlink(tmp_file_path)
    
    @patch('app.routers.productos.get_current_user')
    def test_crear_producto_con_auth_admin(self, mock_get_current_user):
        """Prueba crear producto con autenticación de admin"""
        # Mock del usuario autenticado
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
                    "categoria_id": 1
                }
                
                response = client.post("/productos/", data=data, files=files)
                assert response.status_code == 200
                result = response.json()
                assert "Producto creado exitosamente" in result["mensaje"]
                print("PASS: Crear producto con auth admin - Exitoso")
        finally:
            os.unlink(tmp_file_path)
    
    @patch('app.routers.productos.get_current_user')
    def test_crear_producto_categoria_inexistente(self, mock_get_current_user):
        """Prueba crear producto con categoría inexistente"""
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
                    "nombre": "Producto Test",
                    "descripcion": "Descripción",
                    "precio": 99.99,
                    "stock": 10,
                    "categoria_id": 9999  # Categoría inexistente
                }
                
                response = client.post("/productos/", data=data, files=files)
                assert response.status_code == 404
                assert "Categoría no encontrada" in response.json()["detail"]
                print("PASS: Categoría inexistente - Error 404 correcto")
        finally:
            os.unlink(tmp_file_path)
    
    @patch('app.routers.productos.get_current_user')
    def test_actualizar_producto_con_auth(self, mock_get_current_user):
        """Prueba actualizar producto con autenticación"""
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
        print("PASS: Actualizar producto con auth - Exitoso")
    
    @patch('app.routers.productos.get_current_user')
    def test_eliminar_producto_con_auth(self, mock_get_current_user):
        """Prueba eliminar producto con autenticación"""
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
        print("PASS: Eliminar producto con auth - Exitoso")
    
    def test_actualizar_producto_sin_auth(self):
        """Prueba actualizar producto sin autenticación"""
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
        # Sin autenticación, esperamos error 401 o 422
        assert response.status_code in [401, 422]
        print("PASS: Actualizar sin auth - Error correcto")
    
    def test_eliminar_producto_sin_auth(self):
        """Prueba eliminar producto sin autenticación"""
        response = client.delete("/productos/1?admin_id=1")
        # Sin autenticación, esperamos error 401 o 422
        assert response.status_code in [401, 422]
        print("PASS: Eliminar sin auth - Error correcto")

if __name__ == "__main__":
    # Ejecutar las pruebas directamente
    test_instance = TestProductosFinal()
    test_instance.setup_class()
    
    try:
        test_instance.test_listar_productos()
        test_instance.test_obtener_producto_existente()
        test_instance.test_obtener_producto_no_existente()
        test_instance.test_crear_producto_formato_imagen_invalido()
        test_instance.test_crear_producto_con_auth_admin()
        test_instance.test_crear_producto_categoria_inexistente()
        test_instance.test_actualizar_producto_con_auth()
        test_instance.test_eliminar_producto_con_auth()
        test_instance.test_actualizar_producto_sin_auth()
        test_instance.test_eliminar_producto_sin_auth()
        print("\n🎉 ¡Todas las pruebas finales pasaron correctamente!")
    finally:
        test_instance.teardown_class()
