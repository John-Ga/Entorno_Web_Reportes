import os
import json
import gspread
from flask import Flask, render_template, request, redirect, url_for
from google.oauth2.service_account import Credentials
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
)

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = "91185032"  # Reemplaza por una clave segura

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirige a login seguro

# Modelo de usuario sencillo
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Usuarios de ejemplo (almacenados en un diccionario)
users = {
    "admin": User(id=1, username="admin", password="admin123"),
    "usuario": User(id=2, username="usuario", password="usuario123"),
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == str(user_id):
            return user
    return None

# Configuración de Google Sheets usando variables de entorno
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Cargar las credenciales desde la variable de entorno "GOOGLE_CREDENTIALS"
credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
if not credentials_json:
    raise Exception("La variable de entorno 'GOOGLE_CREDENTIALS' no está definida.")

# Convertir el JSON en un diccionario
credentials_info = json.loads(credentials_json)

# Intentar crear las credenciales reales; si falla, usar dummy para desarrollo
try:
    CREDS = Credentials.from_service_account_info(credentials_info, scopes=SCOPE)
    client = gspread.authorize(CREDS)
except Exception as e:
    print("Advertencia: Error al cargar credenciales reales, se usarán credenciales dummy para desarrollo.")
    print("Error:", e)
    # Definir credenciales dummy
    class DummyCredentials:
        pass
    CREDS = DummyCredentials()
    # Definir un cliente dummy que simula una hoja de cálculo
    class DummySheet:
        def get_all_values(self):
            return [["Reporte dummy 1"], ["Reporte dummy 2"]]
        def append_row(self, row):
            print("Dummy append_row llamada con:", row)
        def delete_rows(self, row):
            print("Dummy delete_rows llamada con:", row)
    class DummyClient:
        def open_by_key(self, key):
            return type("DummySpreadsheet", (), {"sheet1": DummySheet()})()
    client = DummyClient()

# Reemplaza "tu_sheet_id_aquí" con el ID real de la hoja de cálculo
SPREADSHEET_ID = "1ev_ziJEksMDOqPDklDQuU4777HTjIvBFGWnnBpFLI2k"
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Rutas de la aplicación
@app.route("/")
def home():
    return "¡Hola, Flask está funcionando!"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("home"))
        else:
            return "Credenciales incorrectas", 401
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/reportar", methods=["GET", "POST"])
@login_required
def reportar():
    if request.method == "POST":
        # Aquí se guardan los datos del reporte
        reporte = request.form.get("reporte", "")
        sheet.append_row([reporte])
        return f"Reporte recibido: {reporte}"
    return render_template("reportar.html")

@app.route("/listareportes")
@login_required
def listareportes():
    # Obtenemos todos los datos de la hoja de cálculo
    reports = sheet.get_all_values()
    # Renderiza la plantilla 'listareportes.html' pasando la variable 'reports'
    return render_template("listareportes.html", reports=reports)

@app.route("/eliminar_reporte/<int:row>")
@login_required
def eliminar_reporte(row):
    try:
        # Elimina la fila correspondiente en la hoja de cálculo.
        # Ajusta el índice si es necesario (por ejemplo, si hay encabezado, usar row+1).
        sheet.delete_rows(row)
        return redirect(url_for("listareportes"))
    except Exception as e:
        return f"Error al eliminar el reporte: {str(e)}", 500

@app.route("/admin")
@login_required
def admin_dashboard():
    # Obtener todos los reportes desde la hoja de cálculo
    reports = sheet.get_all_values()
    total_reports = len(reports)
    return render_template("admin_dashboard.html", total_reports=total_reports)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
