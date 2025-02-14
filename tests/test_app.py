import sys
import os
import json
import pytest

# Asegura que la raíz del proyecto esté en el PYTHONPATH para poder importar 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos los módulos para parchear las credenciales
from google.oauth2.service_account import Credentials
import gspread

# Definimos una clase dummy para simular las credenciales
class DummyCredentials:
    pass

# Función dummy para reemplazar from_service_account_info
def dummy_from_service_account_info(info, scopes):
    return DummyCredentials()

# Función dummy para simular gspread.authorize
def dummy_authorize(creds):
    class DummySheet:
        def get_all_values(self):
            return [["Reporte dummy 1"], ["Reporte dummy 2"]]
        def append_row(self, row):
            print("Dummy append_row llamada con:", row)
        def delete_rows(self, row):
            print("Dummy delete_rows llamada con:", row)
    class DummyClient:
        def open_by_key(self, key):
            # Retorna un objeto dummy con el atributo 'sheet1'
            return type("DummySpreadsheet", (), {"sheet1": DummySheet()})()
    return DummyClient()

# Fixture para parchear las funciones relacionadas con credenciales y gspread.
# Se usa la fixture sin especificar scope, de modo que sea function-scoped (valor por defecto)
@pytest.fixture(autouse=True)
def patch_credentials(monkeypatch):
    monkeypatch.setattr(Credentials, "from_service_account_info", dummy_from_service_account_info)
    monkeypatch.setattr(gspread, "authorize", dummy_authorize)
    dummy_credentials = {
        "type": "service_account",
        "project_id": "dummy",
        "private_key_id": "dummy",
        "private_key": "-----BEGIN PRIVATE KEY-----\n-----END PRIVATE KEY-----\n",
        "client_email": "dummy@example.com",
        "client_id": "dummy",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dummy@example.com",
        "universe_domain": "googleapis.com"
    }
    monkeypatch.setenv("GOOGLE_CREDENTIALS", json.dumps(dummy_credentials))

# Ahora importamos la aplicación
from app import app

# Fixture para crear un cliente de pruebas
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Función auxiliar para iniciar sesión en las pruebas
def login_client(client, username, password):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "¡Hola, Flask está funcionando!" in data

def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "Iniciar Sesi" in data

def test_valid_login(client):
    response = login_client(client, "admin", "admin123")
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    # Se espera redirigir a la página de inicio
    assert "¡Hola, Flask está funcionando!" in data

def test_invalid_login(client):
    response = client.post("/login", data={"username": "admin", "password": "wrongpassword"}, follow_redirects=True)
    assert response.status_code == 401
    data = response.get_data(as_text=True)
    assert "Credenciales incorrectas" in data

def test_reportar(client):
    login_client(client, "admin", "admin123")
    response = client.post("/reportar", data={"reporte": "Reporte de prueba"}, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "Reporte recibido: Reporte de prueba" in data

def test_listareportes(client):
    login_client(client, "admin", "admin123")
    response = client.get("/listareportes")
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "Reporte dummy" in data

def test_admin_dashboard(client):
    login_client(client, "admin", "admin123")
    response = client.get("/admin")
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    # Ajusta el texto esperado según tu plantilla
    assert "Panel" in data or "Dashboard" in data

def test_eliminar_reporte(client):
    login_client(client, "admin", "admin123")
    response = client.get("/eliminar_reporte/1", follow_redirects=True)
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    # Como usamos dummy, no se eliminará realmente, pero verificamos la redirección a /listareportes
    assert "Reporte dummy" in data or "No hay reportes" in data
