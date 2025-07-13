import requests
from datetime import datetime
#from PDF.services.creation_PDF import createPDF
import sys, os

# Añade el path raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Test.config import settings
from PDF.services.creation_PDF import createPDF
from PDF.backend.session import Base, engine

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

def test_login(email, password, expected_rol=None):
    url = f"{settings.url_api_sga_autenticacion}/auth/login"
    response = requests.post(url, json={
        "email": email,
        "contrasena": password
    })

    print(f"\nLogin attempt for: {email}")
    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("Success:", data)
        assert "access_token" in data
        if expected_rol:
            assert data["rol"] == expected_rol
        return ["PASSED", f"Login {email}", f"date: {datetime.now()}", f"{response.status_code}", f"{data}"]
    else:
        print("Error:", response.text)
        return ["DID NOT PASS", f"Login {email}", f"date: {datetime.now()}", f"{response.status_code}", f"{response.text}"]

def integration_test_auth():
    array_data_pdf = []

    # 1. Login correcto - Admin
    array_data_pdf.append(["Backend", "Login Admin", test_login("carlos.admin@ejemplo.com", "clave12345", expected_rol="administrador")])

    # 2. Login correcto - Profesor
    array_data_pdf.append(["Backend", "Login Profesor", test_login("paula.forero@ejemplo.com", "clave12345", expected_rol="profesor")])

    # 3. Login correcto - Acudiente
    array_data_pdf.append(["Backend", "Login Acudiente", test_login("juan.perez@email.com", "clave12345", expected_rol="acudiente")])


    # 4. Clave incorrecta
    array_data_pdf.append(["Backend", "Clave incorrecta", test_login("paula.forero@ejemplo.com", "clave_mal")])

    # 5. Correo no registrado
    array_data_pdf.append(["Backend", "Correo no registrado", test_login("noexiste@correo.com", "clave123")])

    # Crear reporte PDF
    createPDF("Login_Auth_Test", array_data_pdf)


if __name__ == "__main__":
    integration_test_auth()
