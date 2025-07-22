import time
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Agregar el path raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PDF.services.creation_PDF import createPDF
from PDF.backend.session import Base, engine

# Crear tablas necesarias si no existen
Base.metadata.create_all(bind=engine)

# URL del login del frontend
LOGIN_URL = "http://localhost:3000/iedjosuemanrique/autenticacion/login"

# Lista de pruebas con correo, contraseña y el rol esperado
CREDENCIALES = [
    {"email": "carlos.admin@ejemplo.com", "password": "clave12345", "rol": "administrador"},
    {"email": "paula.forero@ejemplo.com", "password": "clave12345", "rol": "profesor"},
     {"email": "juan.perez@email.com", "password": "clave12345", "rol": "acudiente"},
    {"email": "paula.forero@ejemplo.com", "password": "incorrecta", "rol": "error"},
    {"email": "noexiste@correo.com", "password": "loquesea", "rol": "error"},
]

def test_login_frontend(driver, wait, email, password, expected_rol=None):
    driver.get(LOGIN_URL)
    time.sleep(1)

    try:
        wait.until(EC.presence_of_element_located((By.ID, "email")))
    except Exception as e:
        return ["FALLÓ", f"Login {email}", f"Fecha: {datetime.now()}", "No cargó formulario", str(e)]

    # Llenar formulario
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    time.sleep(1)

    # Clic en botón
    driver.find_element(By.XPATH, "//button[contains(., 'Log in')]").click()
    time.sleep(2)

    if expected_rol == "error":
        try:
            alerta = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiAlert-message")))
            return ["PASÓ", f"Login incorrecto esperado para {email}", f"Fecha: {datetime.now()}", "Alerta visible", alerta.text]
        except Exception as e:
            return ["FALLÓ", f"Login incorrecto esperado para {email}", f"Fecha: {datetime.now()}", "No se mostró alerta", str(e)]
    else:
        try:
            # Verifica redirección por rol
            ruta = f"/Panel{expected_rol.capitalize()}/"
            wait.until(EC.url_contains(ruta))
            return ["PASÓ", f"Login correcto de {expected_rol} para {email}", f"Fecha: {datetime.now()}", f"Redirigido a: {driver.current_url}", "Redirección exitosa"]
        except Exception as e:
            return ["FALLÓ", f"Login correcto esperado para {email}", f"Fecha: {datetime.now()}", "No se redirigió correctamente", str(e)]

def integration_test_frontend():
    resultados_pdf = []

    for cred in CREDENCIALES:
        options = Options()
        # options.add_argument('--headless')  # Activa si no quieres que se abra el navegador
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        try:
            resultado = test_login_frontend(driver, wait, cred["email"], cred["password"], cred["rol"])
            resultados_pdf.append(["Frontend", f"Login: {cred['email']}", resultado])
            time.sleep(2)  # Espera visual entre usuarios
        finally:
            driver.quit()

    createPDF("Login_Auth_Test_Frontend", resultados_pdf)
    print("✅ Pruebas completadas. Revisa el PDF generado en la carpeta PDF_TEST.")

if __name__ == "__main__":
    integration_test_frontend()


