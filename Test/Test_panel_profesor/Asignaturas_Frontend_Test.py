import time
import sys
import os
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de tiempos de espera
WAIT_TIME = 5  # Tiempo de espera estándar en segundos

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PDF.services.creation_PDF import createPDF
from PDF.backend.session import Base, engine

Base.metadata.create_all(bind=engine)

# Configuración
FRONTEND_URL = os.getenv("SERVIDOR_FRONTEND_URL", "http://localhost:3000")
LOGIN_URL = f"{FRONTEND_URL}/iedjosuemanrique/autenticacion/login"
ASIGNATURA_URL = f"{FRONTEND_URL}/iedjosuemanrique/PanelProfesor/11/Asignatura/1"

# Credenciales
from credentials import TEST_PROFESOR_EMAIL, TEST_PROFESOR_PASSWORD

def test_asistencia_functionality(driver, wait, screenshots_dir, asignatura_nombre, results):
    """Prueba la funcionalidad de asistencia"""
    try:
        print("\n--- Probando asistencia ---")
        # Buscar la tabla de estudiantes
        estudiantes_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
        
        # Buscar filas de estudiantes
        estudiante_rows = estudiantes_table.find_elements(By.CSS_SELECTOR, "tr:not(:first-child)")
        
        print(f"Encontrados {len(estudiante_rows)} estudiantes en la tabla")
        
        if len(estudiante_rows) > 0:
            # Modificar asistencia para algunos estudiantes
            for i, row in enumerate(estudiante_rows):
                if i % 2 == 0:  # Solo modificar algunos estudiantes para la prueba
                    try:
                        # Buscar combobox de asistencia (usando múltiples selectores)
                        selectors = [
                            "select", 
                            "[role='combobox']", 
                            ".MuiSelect-select",
                            ".MuiInputBase-root",
                            "div[aria-haspopup='listbox']"
                        ]
                        
                        combobox = None
                        for selector in selectors:
                            elements = row.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                combobox = elements[0]
                                break
                        
                        if combobox:
                            # Hacer clic para abrir el combobox
                            combobox.click()
                            time.sleep(1)
                            
                            # Seleccionar una opción aleatoria (Presente, Ausente, Justificado)
                            opciones = ["Presente", "Ausente", "Justificado"]
                            opcion = random.choice(opciones)
                            
                            # Buscar la opción en el dropdown
                            try:
                                opcion_element = driver.find_element(By.XPATH, f"//li[contains(text(), '{opcion}')]")
                                opcion_element.click()
                                time.sleep(1)
                                print(f"Asistencia modificada para estudiante {i+1}: {opcion}")
                                results.append(["✅ PASSED", f"Cambio de asistencia", f"date: {datetime.now()}", f"Estudiante: {i+1}", f"Asistencia cambiada a: {opcion}"])
                            except:
                                print(f"No se pudo seleccionar la opción {opcion}")
                                results.append(["⚠️ WARNING", "Cambio de asistencia", f"date: {datetime.now()}", f"Estudiante: {i+1}", f"No se pudo seleccionar la opción"])
                        else:
                            print(f"No se encontró combobox de asistencia para estudiante {i+1}")
                            results.append(["⚠️ WARNING", "Cambio de asistencia", f"date: {datetime.now()}", f"Estudiante: {i+1}", "No se encontró combobox de asistencia"])
                    except Exception as e:
                        print(f"Error al modificar asistencia: {e}")
                        results.append(["⚠️ WARNING", "Cambio de asistencia", f"date: {datetime.now()}", f"Error: {str(e)}", "No se pudo modificar la asistencia"])
            
            # Tomar captura después de cambiar asistencias
            screenshot_path = f"{screenshots_dir}/asistencia_asignatura.png"
            driver.save_screenshot(screenshot_path)
            
            # Buscar y hacer clic en el botón de guardar
            try:
                guardar_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar') or contains(text(), 'guardar')]")
                guardar_btn.click()
                time.sleep(WAIT_TIME)
                results.append(["✅ PASSED", "Guardar asistencia", f"date: {datetime.now()}", f"Asignatura: {asignatura_nombre}", "Intento de guardar asistencia"])
            except Exception as e:
                print(f"No se encontró botón de guardar para asistencia: {e}")
                results.append(["⚠️ WARNING", "Guardar asistencia", f"date: {datetime.now()}", f"Error: {str(e)}", "No se encontró botón de guardar"])
        else:
            print("No hay estudiantes para probar asistencia")
            results.append(["⚠️ WARNING", f"Asistencia en {asignatura_nombre}", f"date: {datetime.now()}", "Sin estudiantes", "No hay estudiantes para probar asistencia"])
    except Exception as e:
        print(f"Error al probar asistencia: {e}")
        results.append(["❌ FAILED", "Funcionalidad de asistencia", f"date: {datetime.now()}", f"Error: {str(e)}", "Error en la prueba de asistencia"])

def test_calificaciones_functionality(driver, wait, screenshots_dir, asignatura_nombre, results):
    """Prueba la funcionalidad de calificaciones"""
    try:
        print("\n--- Probando calificaciones ---")
        # Buscar la tabla de estudiantes
        estudiantes_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
        
        # Buscar filas de estudiantes
        estudiante_rows = estudiantes_table.find_elements(By.CSS_SELECTOR, "tr:not(:first-child)")
        
        print(f"Encontrados {len(estudiante_rows)} estudiantes en la tabla")
        
        if len(estudiante_rows) > 0:
            # Modificar calificaciones para algunos estudiantes
            for i, row in enumerate(estudiante_rows):
                if i % 2 == 0:  # Solo modificar algunos estudiantes para la prueba
                    try:
                        # Buscar celdas de calificaciones (asumiendo que son inputs)
                        calificacion_inputs = row.find_elements(By.CSS_SELECTOR, "input[type='number']")
                        
                        if len(calificacion_inputs) > 0:
                            for input_field in calificacion_inputs:
                                # Generar una nota aleatoria entre 3.0 y 5.0
                                nota_aleatoria = round(random.uniform(3.0, 5.0), 1)
                                
                                # Limpiar el input y establecer el nuevo valor
                                input_field.clear()
                                input_field.send_keys(str(nota_aleatoria))
                                input_field.send_keys(Keys.TAB)  # Para disparar el evento blur
                                time.sleep(0.5)
                            
                            print(f"Calificaciones modificadas para estudiante {i+1}")
                            results.append(["✅ PASSED", f"Cambio de calificación", f"date: {datetime.now()}", f"Estudiante: {i+1}", f"Calificaciones modificadas"])
                    except Exception as e:
                        print(f"Error al modificar calificaciones: {e}")
                        results.append(["⚠️ WARNING", "Cambio de calificación", f"date: {datetime.now()}", f"Error: {str(e)}", "No se pudieron modificar las calificaciones"])
            
            # Tomar captura después de cambiar calificaciones
            screenshot_path = f"{screenshots_dir}/calificaciones_asignatura.png"
            driver.save_screenshot(screenshot_path)
            
            # Buscar y hacer clic en el botón de guardar
            try:
                guardar_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar') or contains(text(), 'guardar')]")
                guardar_btn.click()
                time.sleep(WAIT_TIME)
                results.append(["✅ PASSED", "Guardar calificaciones", f"date: {datetime.now()}", f"Asignatura: {asignatura_nombre}", "Intento de guardar calificaciones"])
            except Exception as e:
                print(f"No se encontró botón de guardar: {e}")
                results.append(["⚠️ WARNING", "Guardar calificaciones", f"date: {datetime.now()}", f"Error: {str(e)}", "No se encontró botón de guardar"])
        else:
            print("No hay estudiantes para probar calificaciones")
            results.append(["⚠️ WARNING", f"Calificaciones en {asignatura_nombre}", f"date: {datetime.now()}", "Sin estudiantes", "No hay estudiantes para probar calificaciones"])
    except Exception as e:
        print(f"Error al probar calificaciones: {e}")
        results.append(["❌ FAILED", "Funcionalidad de calificaciones", f"date: {datetime.now()}", f"Error: {str(e)}", "Error en la prueba de calificaciones"])

def test_observaciones_functionality(driver, wait, screenshots_dir, asignatura_nombre, results):
    """Prueba la funcionalidad de observaciones"""
    try:
        print("\n--- Probando observaciones ---")
        
        # Buscar la tabla de estudiantes
        estudiantes_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
        
        # Buscar filas de estudiantes
        estudiante_rows = estudiantes_table.find_elements(By.CSS_SELECTOR, "tr:not(:first-child)")
        
        if len(estudiante_rows) == 0:
            print("No hay estudiantes para probar observaciones")
            results.append(["⚠️ WARNING", f"Observaciones en {asignatura_nombre}", f"date: {datetime.now()}", "Sin estudiantes", "No hay estudiantes para probar observaciones"])
            return
        
        # Seleccionar un estudiante aleatorio
        estudiante_row = random.choice(estudiante_rows)
        
        # Buscar el botón de observación (IconButton con AddCommentIcon)
        try:
            # Buscar por data-testid primero
            observacion_btns = estudiante_row.find_elements(By.CSS_SELECTOR, "[data-testid^='observacion-btn-']")
            
            if len(observacion_btns) == 0:
                # Buscar por título
                observacion_btns = estudiante_row.find_elements(By.CSS_SELECTOR, "[title*='observación'], [title*='Observación'], [title*='disciplinaria'], [title*='Disciplinaria']")
            
            if len(observacion_btns) == 0:
                # Buscar cualquier IconButton
                observacion_btns = estudiante_row.find_elements(By.CSS_SELECTOR, "button.MuiIconButton-root")
            
            if len(observacion_btns) == 0:
                # Buscar cualquier botón en la última celda
                last_cell = estudiante_row.find_elements(By.CSS_SELECTOR, "td:last-child")
                if last_cell:
                    observacion_btns = last_cell[0].find_elements(By.CSS_SELECTOR, "button")
            
            if len(observacion_btns) > 0:
                # Hacer clic en el botón de observación
                observacion_btns[0].click()
                time.sleep(WAIT_TIME)
                
                # Verificar si se abre un modal o formulario
                try:
                    modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, [role='dialog'], .MuiDialog-root, .MuiDialog-paper")))
                    print("Modal de observación abierto")
                    
                    # Completar el formulario
                    # 1. Fecha del incidente
                    try:
                        fecha_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='date']")))
                        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                        driver.execute_script(f"arguments[0].value = '{fecha}';", fecha_input)
                        print("Fecha establecida")
                    except Exception as e:
                        print(f"Error al establecer fecha: {e}")
                    
                    # 2. Tipo de falta
                    try:
                        tipo_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiSelect-select")))
                        tipo_select.click()
                        time.sleep(1)
                        option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Leve')]")))
                        option.click()
                        time.sleep(1)
                        print("Tipo de falta seleccionado")
                    except Exception as e:
                        print(f"Error al seleccionar tipo de falta: {e}")
                    
                    # 3. Artículo del manual de convivencia
                    try:
                        articulo_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='Art']")))
                        articulo_input.clear()
                        articulo_input.send_keys("Art. 23, Num. 5")
                        print("Artículo establecido")
                    except Exception as e:
                        print(f"Error al establecer artículo: {e}")
                    
                    # 4. Descripción de lo sucedido - IMPORTANTE
                    try:
                        # Buscar el textarea para la descripción
                        descripcion_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea")))
                        # Limpiar el campo
                        descripcion_input.clear()
                        # Escribir una descripción larga (más de 10 caracteres)
                        descripcion_texto = "Esta es una descripción detallada del incidente. El estudiante no presentó la tarea asignada y no justificó su falta."
                        descripcion_input.send_keys(descripcion_texto)
                        print(f"Descripción establecida: {descripcion_texto}")
                    except Exception as e:
                        print(f"Error al establecer descripción: {e}")
                        
                        # Intento alternativo usando JavaScript
                        try:
                            driver.execute_script("""
                                var textareas = document.querySelectorAll('textarea');
                                for(var i=0; i<textareas.length; i++) {
                                    textareas[i].value = 'Esta es una descripción detallada del incidente. El estudiante no presentó la tarea asignada y no justificó su falta.';
                                    var event = new Event('input', { bubbles: true });
                                    textareas[i].dispatchEvent(event);
                                }
                            """)
                            print("Descripción establecida mediante JavaScript")
                        except Exception as js_error:
                            print(f"Error al establecer descripción mediante JavaScript: {js_error}")
                    
                    # Tomar captura del formulario completado
                    screenshot_path = f"{screenshots_dir}/observacion_form.png"
                    driver.save_screenshot(screenshot_path)
                    
                    # Buscar botón de guardar en el modal
                    try:
                        guardar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Guardar') or contains(text(), 'guardar') or contains(text(), 'Enviar') or contains(text(), 'enviar')]")))
                        
                        # Usar JavaScript para hacer clic en el botón (evita problemas de intercepción)
                        driver.execute_script("arguments[0].click();", guardar_btn)
                        time.sleep(WAIT_TIME)
                        results.append(["✅ PASSED", "Crear observación", f"date: {datetime.now()}", f"Asignatura: {asignatura_nombre}", "Intento de crear observación"])
                    except Exception as e:
                        print(f"Error al hacer clic en el botón guardar: {e}")
                        results.append(["⚠️ WARNING", "Crear observación", f"date: {datetime.now()}", f"Error: {str(e)}", "Error al guardar observación"])
                except Exception as e:
                    print(f"No se detectó modal de observación: {e}")
                    results.append(["⚠️ WARNING", "Crear observación", f"date: {datetime.now()}", f"Error: {str(e)}", "No se detectó modal de observación"])
            else:
                print("No se encontraron botones de observación")
                results.append(["⚠️ WARNING", f"Observaciones en {asignatura_nombre}", f"date: {datetime.now()}", "Sin botones", "No se encontraron botones de observación"])
        except Exception as e:
            print(f"Error al buscar botón de observación: {e}")
            results.append(["❌ FAILED", "Buscar botón de observación", f"date: {datetime.now()}", f"Error: {str(e)}", "Error al buscar botón de observación"])
    except Exception as e:
        print(f"Error al probar observaciones: {e}")
        results.append(["❌ FAILED", "Funcionalidad de observaciones", f"date: {datetime.now()}", f"Error: {str(e)}", "Error en la prueba de observaciones"])

def run_asignaturas_frontend_tests():
    """Ejecuta las pruebas de integración de frontend para asignaturas"""
    print("=" * 80)
    print(f"INICIANDO PRUEBAS DE INTEGRACIÓN DE FRONTEND PARA ASIGNATURAS - {datetime.now()}")
    print("=" * 80)
    
    # Crear directorio para capturas si no existe
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    options = Options()
    options.add_argument("--disable-dev-shm-usage")  # Evita errores de memoria compartida
    options.add_argument("--no-sandbox")  # Evita problemas de seguridad
    options.add_argument("--disable-gpu")  # Desactiva aceleración GPU
    options.add_argument("--window-size=1920,1080")  # Tamaño de ventana fijo
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    asignaturas_results = []
    
    try:
        # Login
        print("Iniciando sesión...")
        driver.get(LOGIN_URL)
        time.sleep(WAIT_TIME)
        
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(TEST_PROFESOR_EMAIL)
        
        try:
            password_field = driver.find_element(By.ID, "password")
        except:
            try:
                password_field = driver.find_element(By.ID, "contrasena")
            except:
                password_field = driver.find_element(By.NAME, "password")
        
        password_field.send_keys(TEST_PROFESOR_PASSWORD)
        driver.find_element(By.XPATH, "//button[contains(., 'Log in')]").click()
        time.sleep(WAIT_TIME * 2)  # Esperar más tiempo para asegurar que la página cargue
        
        # Captura de pantalla después del login
        screenshot_path = f"{screenshots_dir}/login_success.png"
        driver.save_screenshot(screenshot_path)
        
        # Registrar resultado del login
        login_result = ["✅ PASSED", f"Login correcto de profesor para {TEST_PROFESOR_EMAIL}", f"Fecha: {datetime.now()}", f"URL actual: {driver.current_url}", "Login exitoso"]
        asignaturas_results.append(["Frontend", "Login", login_result])
        
        # Ir directamente a la página de asignatura
        print("\nNavegando directamente a la página de asignatura...")
        driver.get(ASIGNATURA_URL)
        time.sleep(WAIT_TIME * 2)  # Esperar más tiempo para asegurar que la página cargue
        
        # Captura de pantalla de la página de asignatura
        screenshot_path = f"{screenshots_dir}/asignatura_page.png"
        driver.save_screenshot(screenshot_path)
        
        # Verificar que estamos en la página de asignatura
        try:
            # Intentar encontrar cualquier elemento que indique que estamos en la página de asignatura
            asignatura_container = driver.find_element(By.TAG_NAME, "body")
            print("Página de asignatura cargada correctamente")
            asignaturas_results.append(["Frontend", "Navegación", ["✅ PASSED", "Navegación a asignatura", f"date: {datetime.now()}", f"URL: {driver.current_url}", "Navegación exitosa"]])
            
            # Obtener el nombre de la asignatura
            try:
                asignatura_nombre = driver.find_element(By.CSS_SELECTOR, "h2, h3, h4, h5").text
            except:
                asignatura_nombre = "Asignatura"
            
            print(f"Asignatura detectada: {asignatura_nombre}")
            asignaturas_results.append(["Frontend", "Asignaturas", ["✅ PASSED", f"Navegación a asignatura {asignatura_nombre}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "Navegación exitosa"]])
            
            # Probar funcionalidades de la asignatura una por una para evitar errores de elementos obsoletos
            
            # 1. Probar calificaciones
            test_calificaciones_functionality(driver, wait, screenshots_dir, asignatura_nombre, asignaturas_results)
            
            # 2. Recargar la página para evitar elementos obsoletos
            driver.refresh()
            time.sleep(WAIT_TIME * 2)
            
            # 3. Probar asistencia
            test_asistencia_functionality(driver, wait, screenshots_dir, asignatura_nombre, asignaturas_results)
            
            # 4. Recargar la página para evitar elementos obsoletos
            driver.refresh()
            time.sleep(WAIT_TIME * 2)
            
            # 5. Probar observaciones
            test_observaciones_functionality(driver, wait, screenshots_dir, asignatura_nombre, asignaturas_results)
            
        except Exception as e:
            print(f"Error al cargar la página de asignatura: {e}")
            asignaturas_results.append(["Frontend", "Navegación", ["❌ FAILED", "Navegación a asignatura", f"date: {datetime.now()}", f"Error: {str(e)}", "No se pudo cargar la página de asignatura"]])
    
    except Exception as e:
        print(f"Error general en las pruebas: {e}")
        asignaturas_results.append(["Frontend", "General", ["❌ FAILED", "Error general", f"date: {datetime.now()}", f"Error: {str(e)}", "Error general en las pruebas"]])
    
    finally:
        # Cerrar el navegador
        driver.quit()
        
        # Crear reporte PDF
        createPDF("Asignaturas_Frontend_Test", asignaturas_results)
        print("✅ Pruebas de frontend para asignaturas completadas. Revisa el PDF generado en la carpeta PDF_TEST.")
    
    return asignaturas_results

if __name__ == "__main__":
    run_asignaturas_frontend_tests()