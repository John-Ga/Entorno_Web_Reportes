from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask (__name__)
app.secret_key = "tu_clave_secreta_aqui"

# configuración de Falsk-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Modelo de usuario sencillo
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
# Usuarios de ejemplo (almacenados en un diccionario)
users = {
    "admin": User(id=1, username="admin", password="admin123"),
    "usuario": User(id=2, username="usuario", password="usuario123")
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == str(user_id):
            return user
        
    return None         

#Configuración de la API de Google Sheets
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file(r"C:\Users\Sevicol\OneDrive\Escritorio\Entorno_Wed_Reportes\credentials\credenciales.json", scopes=SCOPE)

client = gspread.authorize(CREDS)

#Reemplaza "tu_sheet_id_aquí" con  el ID real de hoja de cálculo
SPREADSHEET_ID = "1ev_ziJEksMDOqPDklDQuU4777HTjIvBFGWnnBpFLI2k"
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

#Página de inicio
@app.route('/')
def home():
    return "¡Hola, Flask está funcionando!"

# Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return f"Bienvenido, {username}!"
        else:
            return "Credenciales incorrectas", 401
    return render_template("login.html")

# Página de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Has cerrado sesión."    
   
# Página para realizar reportes (acceso restringido)
@app.route('/reportar', methods=['GET', 'POST'])
@login_required
def reportar():
    if request.method == 'POST':
        #Aquí guardarias los datos del reporte
        reporte = request.form.get('reporte', '')
        #Guardar el reporte en google sheets (añade una nueva fila)
        sheet.append_row([reporte])      
        return f"Reporte recibido: {reporte}"
    return render_template ('reportar.html')

# Página para listar reportes (acceso restringido)
@app.route('/listareportes')
@login_required
def listareportes():
    #Obtenemos todos los datos de la hoja de cálculo
    reports = sheet.get_all_values()
    #Renderizamos la plantilla 'listareportes.html' pasando la variable 'reports'
    return render_template('listareportes.html', reports=reports)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)