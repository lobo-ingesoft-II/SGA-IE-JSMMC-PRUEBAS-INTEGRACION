import requests
from datetime import datetime
#from PDF.services.creation_PDF import createPDF
import sys, os

# Añadir ruta raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Test.config import settings
from PDF.services.creation_PDF import createPDF
from PDF.backend.session import Base, engine

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

def test_login(email, password, expected_rol=None, esperado=True):
    url = f"{settings.url_api_sga_autenticacion}/auth/login"
    response = requests.post(url, json={
        "email": email,
        "contrasena": password
    })

    print(f"\nLogin attempt for: {email}")
    print("Status Code:", response.status_code)

    try:
        data = response.json()
    except:
        data = response.text

    if esperado:
        if response.status_code == 200 and "access_token" in data:
            if expected_rol:
                if data.get("rol") != expected_rol:
                    return ["❌ FAILED", f"Login {email}", f"date: {datetime.now()}", f"{response.status_code}", f"{data}"]
            return ["✅ PASSED", f"Login {email}", f"date: {datetime.now()}", f"{response.status_code}", f"{data}"]
        else:
            return ["❌ FAILED", f"Login {email}", f"date: {datetime.now()}", f"{response.status_code}", f"{data}"]
    else:
        if response.status_code != 200:
            return ["✅ PASSED", f"Login con error esperado {email}", f"date: {datetime.now()}", f"{response.status_code}", f"{data}"]
        else:
            return ["❌ FAILED", f"Login {email} debió fallar", f"date: {datetime.now()}", f"{response.status_code}", f"{data}"]

def integration_test_auth():
    array_data_pdf = []

    # 1. Login correcto - Admin
    array_data_pdf.append(["Backend", "Login Admin", test_login("carlos.admin@ejemplo.com", "clave12345", expected_rol="administrador", esperado=True)])

    # 2. Login correcto - Profesor
    array_data_pdf.append(["Backend", "Login Profesor", test_login("paula.forero@ejemplo.com", "clave12345", expected_rol="profesor", esperado=True)])

    # 3. Login correcto - Acudiente
    array_data_pdf.append(["Backend", "Login Acudiente", test_login("juan.perez@email.com", "clave12345", expected_rol="acudiente", esperado=True)])

    # 4. Clave incorrecta (esperamos error)
    array_data_pdf.append(["Backend", "Clave incorrecta", test_login("paula.forero@ejemplo.com", "clave_mal", esperado=False)])

    # 5. Correo no registrado (esperamos error)
    array_data_pdf.append(["Backend", "Correo no registrado", test_login("noexiste@correo.com", "clave123", esperado=False)])

    # Crear reporte PDF
    createPDF("Login_Auth_Test_Backend", array_data_pdf)

if __name__ == "__main__":
    integration_test_auth()