import time
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Importar función PDF y configuración de BD
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PDF.services.creation_PDF import createPDF
from PDF.backend.session import Base, engine

Base.metadata.create_all(bind=engine)

URL_LOGIN = "http://localhost:3000/iedjosuemanrique/autenticacion/login"
USUARIO_ADMIN = "carlos.admin@ejemplo.com"
CLAVE_ADMIN = "clave12345"

def generar_resultado(nombre_prueba, exito=True, error=None):
    estado = "✅ PASSED" if exito else "❌ FAILED"
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    detalles = [estado, nombre_prueba, fecha]
    if error:
        detalles.append(f"Error: {error}")
    return detalles

def test_crear_editar_cambiar_estado_y_eliminar_usuario():
    opciones = Options()
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--disable-notifications")
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=opciones)
    wait = WebDriverWait(driver, 20)
    resultados = []

    datos_usados = {
        "Nombres": "Diego Felip",
        "Apellidos": "Uribe",
        "Documento": "1043424424",
        "Teléfono": "1234567890",
        "Correo": "diegoadmin12@gmail.com",
        "Contraseña": "clave12345",
        "Especialidad inicial": "Matemáticas",
        "Especialidad editada": "Español",
        "Teléfono editado": "111111111",
        "Apellidos editado": "Uribe Uribe"
    }

    try:
        # ========== [1] LOGIN ==========
        driver.get(URL_LOGIN)
        wait.until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(USUARIO_ADMIN)
        driver.find_element(By.ID, "password").send_keys(CLAVE_ADMIN)
        driver.find_element(By.XPATH, "//button[contains(., 'Log in')]").click()
        wait.until(EC.url_contains("/PanelAdministrador"))
        resultados.append(["Frontend", "Login administrador", generar_resultado("Login administrador")])
        
        # ========== [2] GESTIÓN USUARIOS ==========
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Gestión de usuarios']"))).click()
        time.sleep(1)

        # ========== [3] CREAR USUARIO ==========
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='btn-nuevo-usuario']"))).click()
        time.sleep(2)

        datos = {
            "input-nombres": datos_usados["Nombres"],
            "input-apellidos": datos_usados["Apellidos"],
            "input-documento": datos_usados["Documento"],
            "input-telefono": datos_usados["Teléfono"],
            "input-email": datos_usados["Correo"],
            "input-contrasena": datos_usados["Contraseña"],
            "input-confirmar-contrasena": datos_usados["Contraseña"]
        }

        for testid, valor in datos.items():
            campo = driver.find_element(By.CSS_SELECTOR, f"[data-testid='{testid}'] input")
            campo.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            campo.send_keys(valor)

        esp = driver.find_element(By.CSS_SELECTOR, "input[name='datos_adicionales.especialidad']")
        esp.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        esp.send_keys(datos_usados["Especialidad inicial"])

        driver.find_element(By.CSS_SELECTOR, "[data-testid='btn-guardar']").click()
        resultados.append(["Frontend", "Usuario creado", generar_resultado("Usuario creado")])

        # ========== [4] VERIFICAR NOTIFICACIÓN ==========
        notificacion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='notificacion']")))
        if "creado" in notificacion.text.lower():
            resultados.append(["Frontend", "Notificación creación", generar_resultado("Notificación creación")])
        else:
            resultados.append(["Frontend", "Notificación creación", generar_resultado("Notificación creación", False, "Texto incorrecto")])

        # ========== [5] NAVEGAR A ÚLTIMA PÁGINA ==========
        while True:
            try:
                btn = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
                if "disabled" in btn.get_attribute("class"):
                    break
                btn.click()
                time.sleep(1)
            except:
                break

        # ========== [6] EDITAR USUARIO ==========
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid^='btn-editar']")))[-1].click()
        time.sleep(1)

        def actualizar(testid, valor):
            campo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='{testid}'] input")))
            campo.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            campo.send_keys(valor)

        actualizar("input-apellidos", datos_usados["Apellidos editado"])
        actualizar("input-telefono", datos_usados["Teléfono editado"])
        esp = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='datos_adicionales.especialidad']")))
        esp.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        esp.send_keys(datos_usados["Especialidad editada"])
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='btn-guardar']"))).click()
        resultados.append(["Frontend", "Usuario editado", generar_resultado("Usuario editado")])

        # ========== [7] VERIFICAR EDICIÓN ==========
        notificacion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='notificacion']")))
        if "actualizado" in notificacion.text.lower():
            resultados.append(["Frontend", "Notificación edición", generar_resultado("Notificación edición")])
        else:
            resultados.append(["Frontend", "Notificación edición", generar_resultado("Notificación edición", False, "Texto incorrecto")])

        # ========== [8] CAMBIAR ESTADO ==========
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid^='btn-estado-']")))[-1].click()
        resultados.append(["Frontend", "Estado cambiado", generar_resultado("Estado cambiado")])
        
        # ========== [9] VERIFICAR ESTADO ==========
        time.sleep(3)
        texto_estado = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='notificacion']"))).text.lower()
        if "activado" in texto_estado or "desactivado" in texto_estado:
            resultados.append(["Frontend", "Notificación estado", generar_resultado(f"Notificación estado: {texto_estado}")])
        else:
            resultados.append(["Frontend", "Notificación estado", generar_resultado("Notificación estado", False, "Texto incorrecto")])

        # ========== [10] ELIMINAR USUARIO ==========
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid^='btn-eliminar']")))[-1].click()
        WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()
        resultados.append(["Frontend", "Usuario eliminado", generar_resultado("Usuario eliminado")])

        # ========== [11] VERIFICAR ELIMINACIÓN ==========
        notificacion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='notificacion']")))
        if "eliminado" in notificacion.text.lower():
            resultados.append(["Frontend", "Notificación eliminación", generar_resultado("Notificación eliminación")])
        else:
            resultados.append(["Frontend", "Notificación eliminación", generar_resultado("Notificación eliminación", False, "Texto incorrecto")])

        time.sleep(2)

    except Exception as e:
        exc_type, _, tb = sys.exc_info()
        resultados.append(["Frontend", "Error en prueba", generar_resultado("Error en prueba", False, f"Línea {tb.tb_lineno}: {str(e)}")])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(f"error_{timestamp}.png")

    finally:
        driver.quit()
        createPDF("CRUD_Usuarios_Frontend", resultados)
        print("✅ Prueba completada. Revisa el PDF en la carpeta PDF_TEST.")

if __name__ == "__main__":
    test_crear_editar_cambiar_estado_y_eliminar_usuario()




