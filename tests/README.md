# Entorno Web Reportes

**Entorno Web Reportes** es una aplicación web desarrollada con Flask que permite a los usuarios reportar incidentes y a los administradores gestionar dichos reportes. La aplicación se integra con Google Sheets para almacenar los reportes y utiliza Bootstrap para ofrecer una interfaz de usuario moderna y responsiva.

## Características

- **Autenticación de Usuarios:**  
  La aplicación utiliza Flask-Login para gestionar el inicio de sesión.  
  - Ejemplos de credenciales:  
    - Usuario: `admin` | Contraseña: `admin123`  
    - Usuario: `usuario` | Contraseña: `usuario123`

- **Reportes de Incidentes:**  
  Los usuarios autenticados pueden enviar reportes mediante un formulario, los cuales se almacenan en una hoja de cálculo de Google Sheets.

- **Listado de Reportes:**  
  Se muestra un listado de los reportes guardados, con la opción de eliminar reportes a través del panel de administración.

- **Panel de Administración:**  
  Permite al administrador visualizar métricas, como el total de reportes, y gestionar las acciones sobre los reportes.

- **Interfaz de Usuario Mejorada:**  
  Se utiliza Bootstrap para garantizar un diseño limpio y responsivo.

## Estructura del Proyecto

La estructura del repositorio es la siguiente:

Entorno_Web_Reportes/ ├── README.md # Este archivo, con la documentación del proyecto ├── .gitignore # Archivos y carpetas a ignorar (e.g., venv, pycache, credentials/) ├── Procfile # Instrucciones para iniciar la aplicación con Gunicorn ├── app.py # Archivo principal de la aplicación Flask ├── requirements.txt # Lista de dependencias └── templates/ # Plantillas HTML de la aplicación ├── login.html ├── reportar.html ├── listareportes.html └── admin_dashboard.html

markdown
Copiar
Editar

> **Nota:**  
> Los archivos o datos sensibles (por ejemplo, credenciales de Google) se gestionan a través de variables de entorno y se excluyen del repositorio utilizando `.gitignore`.

## Instalación y Configuración

### Requisitos Previos

- **Python 3.x** (se recomienda la versión 3.11 o superior)
- **Git** para clonar el repositorio
- Un entorno virtual (recomendado)

### Pasos para ejecutar la aplicación localmente

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/Entorno_Web_Reportes.git
   cd Entorno_Web_Reportes
Crear y activar un entorno virtual:

En Windows (PowerShell):
powershell
Copiar
Editar
python -m venv venv
.\venv\Scripts\Activate
En Linux/Mac:
bash
Copiar
Editar
python3 -m venv venv
source venv/bin/activate
Instalar las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Configurar las variables de entorno:

La aplicación utiliza la variable GOOGLE_CREDENTIALS para cargar las credenciales de Google Sheets. Define esta variable en tu entorno local (para desarrollo, se pueden usar credenciales dummy):

En Windows (PowerShell):

powershell
Copiar
Editar
$env:GOOGLE_CREDENTIALS = '{"type": "service_account", "project_id": "dummy", "private_key_id": "dummy", "private_key": "-----BEGIN PRIVATE KEY-----\n-----END PRIVATE KEY-----\n", "client_email": "dummy@example.com", "client_id": "dummy", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dummy@example.com", "universe_domain": "googleapis.com"}'
Ejecutar la aplicación localmente:

bash
Copiar
Editar
flask run
La aplicación estará disponible en http://127.0.0.1:5000/.

Uso de la Aplicación
Página de Inicio:
http://127.0.0.1:5000/
Muestra el mensaje "¡Hola, Flask está funcionando!".

Página de Login:
http://127.0.0.1:5000/login
Inicia sesión con las credenciales de ejemplo.

Reportar Incidente:
http://127.0.0.1:5000/reportar
Envía un reporte mediante un formulario (requiere autenticación).

Listado de Reportes:
http://127.0.0.1:5000/listareportes
Visualiza los reportes almacenados en Google Sheets.

Panel de Administración:
http://127.0.0.1:5000/admin
Visualiza métricas y opciones administrativas.

Despliegue en Producción
La aplicación está configurada para desplegarse en servicios como Render o Heroku.

Procfile:
El archivo Procfile contiene la instrucción para iniciar la aplicación con Gunicorn:

bash
Copiar
Editar
web: gunicorn app:app --bind 0.0.0.0:$PORT
Variables de Entorno:
En producción, asegúrate de configurar la variable GOOGLE_CREDENTIALS con las credenciales reales en la plataforma de despliegue.

Pruebas
Se han implementado pruebas automatizadas usando pytest. Para ejecutar las pruebas:

bash
Copiar
Editar
python -m pytest
Estas pruebas cubren las rutas principales y la funcionalidad de la aplicación.

Contribución
Si deseas contribuir a este proyecto, por favor:

Realiza un fork del repositorio.
Crea una rama para tus cambios.
Envía un pull request con una descripción clara de los cambios.
Licencia
Este proyecto se distribuye bajo la MIT License.

Contacto
Para dudas o sugerencias, por favor contacta a: [tu_email@dominio.com]