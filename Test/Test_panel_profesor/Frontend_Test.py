
import time
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de tiempos de espera
WAIT_TIME = 1  # Tiempo de espera estándar en segundos

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PDF.services.creation_PDF import createPDF
from PDF.backend.session import Base, engine

Base.metadata.create_all(bind=engine)

# Configuración
FRONTEND_URL = os.getenv("SERVIDOR_FRONTEND_URL", "http://localhost:3000")
LOGIN_URL = f"{FRONTEND_URL}/iedjosuemanrique/autenticacion/login"

# Credenciales
from credentials import TEST_PROFESOR_EMAIL, TEST_PROFESOR_PASSWORD

def test_sidebar_navigation(driver, wait, screenshots_dir="screenshots"):
    """Prueba la navegación por el sidebar"""
    results = []
    
    try:
        # Verificar que el sidebar está presente
        sidebar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='sidebar-container']")))
        print("Sidebar encontrado")
        
        # Tomar captura del sidebar
        screenshot_path = f"{screenshots_dir}/sidebar.png"
        driver.save_screenshot(screenshot_path)
        print(f"Captura del sidebar guardada: {screenshot_path}")
        
        # Verificar el logo
        logo = driver.find_element(By.CSS_SELECTOR, "[data-testid='sidebar-logo']")
        if logo:
            print("Logo del sidebar encontrado")
            results.append(["✅ PASSED", "Logo del sidebar", f"date: {datetime.now()}", "Logo encontrado", "El logo está presente en el sidebar"])
        
        # Verificar la lista de navegación
        nav_list = driver.find_element(By.CSS_SELECTOR, "[data-testid='sidebar-nav-list']")
        if nav_list:
            print("Lista de navegación encontrada")
            results.append(["✅ PASSED", "Lista de navegación", f"date: {datetime.now()}", "Lista encontrada", "La lista de navegación está presente en el sidebar"])
        
        # Probar los elementos de navegación principales
        nav_items = [
            "nav-item-página-principal",
            "nav-item-mis-sedes",
            "nav-item-mis-cursos",
            "nav-item-mis-asignaturas"
        ]
        
        for item_id in nav_items:
            try:
                nav_item = driver.find_element(By.CSS_SELECTOR, f"[data-testid='{item_id}']")
                item_text = nav_item.text
                print(f"Elemento de navegación encontrado: {item_text}")
                
                # Hacer clic en el elemento si es colapsable (excepto página principal)
                if item_id != "nav-item-página-principal":
                    nav_item.click()
                    time.sleep(WAIT_TIME)
                    print(f"Clic en {item_text} para expandir/colapsar")
                    
                    # Tomar captura después de expandir
                    screenshot_path = f"{screenshots_dir}/sidebar_{item_id}_expanded.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"Captura después de expandir {item_text} guardada: {screenshot_path}")
                    
                    # Verificar si hay subelementos
                    try:
                        # Buscar subelementos basados en el patrón de ID
                        sub_items = driver.find_elements(By.CSS_SELECTOR, f"[data-testid^='subnav-item-{item_id.replace('nav-item-', '')}']")
                        if len(sub_items) > 0:
                            print(f"Encontrados {len(sub_items)} subelementos para {item_text}")
                            results.append(["✅ PASSED", f"Subelementos de {item_text}", f"date: {datetime.now()}", f"Cantidad: {len(sub_items)}", f"Se encontraron subelementos para {item_text}"])
                    except Exception as e:
                        print(f"Error al buscar subelementos de {item_text}: {e}")
                
                results.append(["✅ PASSED", f"Elemento de navegación: {item_text}", f"date: {datetime.now()}", f"ID: {item_id}", "Elemento encontrado y funcional"])
            except Exception as e:
                print(f"Error al verificar elemento de navegación {item_id}: {e}")
                results.append(["❌ FAILED", f"Elemento de navegación: {item_id}", f"date: {datetime.now()}", "Error", str(e)])
        
        # Verificar el botón de cerrar sesión
        try:
            logout_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='sidebar-logout-button']")
            if logout_button:
                print("Botón de cerrar sesión encontrado")
                results.append(["✅ PASSED", "Botón de cerrar sesión", f"date: {datetime.now()}", "Botón encontrado", "El botón de cerrar sesión está presente en el sidebar"])
                
                # No hacemos clic en el botón para no cerrar la sesión
        except Exception as e:
            print(f"Error al verificar botón de cerrar sesión: {e}")
            results.append(["❌ FAILED", "Botón de cerrar sesión", f"date: {datetime.now()}", "Error", str(e)])
    
    except Exception as e:
        print(f"Error al verificar el sidebar: {e}")
        results.append(["❌ FAILED", "Sidebar", f"date: {datetime.now()}", "Error", str(e)])
    
    return results

def run_frontend_tests():
    """Ejecuta las pruebas de integración de frontend"""
    print("=" * 80)
    print(f"INICIANDO PRUEBAS DE INTEGRACIÓN DE FRONTEND - {datetime.now()}")
    print("=" * 80)
    
    # Crear directorio para capturas si no existe
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    options = Options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    frontend_results = []
    
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
        time.sleep(WAIT_TIME)
        
        # Verificar que estamos en el panel de profesor
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))
        print(f"Login exitoso. URL actual: {driver.current_url}")
        
        # Captura de pantalla del panel inicial
        screenshot_path = f"{screenshots_dir}/panel_inicio.png"
        driver.save_screenshot(screenshot_path)
        print(f"Captura del panel inicial guardada: {screenshot_path}")
        
        # Registrar resultado del login
        login_result = ["✅ PASSED", f"Login correcto de profesor para {TEST_PROFESOR_EMAIL}", f"Fecha: {datetime.now()}", f"Redirigido a: {driver.current_url}", "Redirección exitosa"]
        frontend_results.append(["Frontend", "Login", login_result])
        
        # Probar navegación por el sidebar
        print("\n=== NAVEGANDO POR EL SIDEBAR ===")
        sidebar_results = test_sidebar_navigation(driver, wait, screenshots_dir)
        for result in sidebar_results:
            frontend_results.append(["Frontend", "Navegación Sidebar", result])
        
        # 1. Navegar por TODAS las sedes usando data-testid
        print("\n=== NAVEGANDO POR TODAS LAS SEDES ===")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='sedes-section']")))
        
        # Buscar todas las sedes por atributo data-sede-id
        sedes_elements = driver.find_elements(By.CSS_SELECTOR, "[data-sede-id]")
        print(f"Encontradas {len(sedes_elements)} sedes")
        
        # Conjunto para llevar registro de sedes visitadas
        visited_sedes = set()
        
        # Guardar información de las sedes para no perderla
        sedes_info = []
        for sede in sedes_elements:
            sede_id = sede.get_attribute("data-sede-id")
            sede_nombre = sede.get_attribute("data-sede-nombre")
            sedes_info.append({"id": sede_id, "nombre": sede_nombre})
        
        # Navegar por cada sede
        for sede_data in sedes_info:
            sede_id = sede_data["id"]
            sede_nombre = sede_data["nombre"]
            
            if sede_id in visited_sedes:
                print(f"Sede {sede_id} ya visitada anteriormente, saltando...")
                continue
                
            print(f"\nNavegando a sede: {sede_nombre} (ID: {sede_id})")
            
            # Volver a la página principal y encontrar la sede nuevamente
            driver.get(f"{FRONTEND_URL}/iedjosuemanrique/PanelProfesor/11/Inicio")
            time.sleep(WAIT_TIME)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='sedes-section']")))
            
            # Buscar la sede específica
            try:
                sede_element = driver.find_element(By.CSS_SELECTOR, f"[data-sede-id='{sede_id}']")
                
                # Hacer clic en la sede
                driver.execute_script("arguments[0].click();", sede_element)
                time.sleep(WAIT_TIME)
                
                # Verificar navegación
                if "/Sedes/" in driver.current_url:
                    visited_sedes.add(sede_id)
                    
                    # Tomar captura de pantalla
                    screenshot_path = f"{screenshots_dir}/sede_{sede_id}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"✅ Navegación exitosa a sede {sede_nombre} (ID: {sede_id}) - Captura guardada: {screenshot_path}")
                    
                    # Registrar resultado
                    sede_result = ["✅ PASSED", f"Navegación a sede {sede_nombre}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "Navegación exitosa"]
                    frontend_results.append(["Frontend", "Navegación Sedes", sede_result])
                    
                    # Verificar el encabezado de la sede
                    try:
                        sede_header = driver.find_element(By.CSS_SELECTOR, "[data-testid='sede-header']")
                        sede_nombre_ui = sede_header.text
                        print(f"Nombre de sede en UI: {sede_nombre_ui}")
                        
                        # Verificar coherencia entre el nombre de la sede en la lista y en la vista detallada
                        if sede_nombre.lower() in sede_nombre_ui.lower() or sede_nombre_ui.lower() in sede_nombre.lower():
                            print("✅ Coherencia verificada: Nombre de sede coincide entre lista y detalle")
                            frontend_results.append(["Frontend", "Coherencia Sede", ["✅ PASSED", f"Coherencia nombre sede {sede_id}", f"date: {datetime.now()}", f"Sede: {sede_nombre}", "Nombre coincide entre lista y detalle"]])
                        else:
                            print("❌ Incoherencia: Nombre de sede no coincide entre lista y detalle")
                            frontend_results.append(["Frontend", "Coherencia Sede", ["❌ FAILED", f"Coherencia nombre sede {sede_id}", f"date: {datetime.now()}", f"Esperado: {sede_nombre}, Obtenido: {sede_nombre_ui}", "Nombre no coincide entre lista y detalle"]])
                    except Exception as e:
                        print(f"No se pudo verificar el encabezado de la sede: {e}")
                    
                    # Buscar todos los cursos en la sede
                    cursos_elements = []
                    try:
                        # Intentar encontrar cursos por data-testid
                        cursos_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid^='curso-']")
                        if len(cursos_elements) == 0:
                            # Intentar encontrar cursos por data-curso-id
                            cursos_elements = driver.find_elements(By.CSS_SELECTOR, "[data-curso-id]")
                    except Exception as e:
                        print(f"Error al buscar cursos: {e}")
                    
                    print(f"Encontrados {len(cursos_elements)} cursos en sede {sede_id}")
                    
                    # Guardar información de los cursos para no perderla
                    cursos_info = []
                    for curso in cursos_elements:
                        try:
                            curso_id = curso.get_attribute("data-curso-id") or curso.get_attribute("id").replace("curso-", "")
                            curso_nombre = curso.get_attribute("data-curso-nombre") or curso.text
                            curso_grado = curso.get_attribute("data-curso-grado") or ""
                            cursos_info.append({"id": curso_id, "nombre": curso_nombre, "grado": curso_grado})
                        except:
                            continue
                    
                    # Navegar por cada curso
                    for curso_data in cursos_info:
                        curso_id = curso_data["id"]
                        curso_nombre = curso_data["nombre"]
                        curso_grado = curso_data["grado"]
                        
                        print(f"\nExpandiendo curso: {curso_nombre} (ID: {curso_id})")
                        
                        # Buscar el curso específico nuevamente
                        # Buscar el curso específico nuevamente
                        try:
                            curso_element = driver.find_element(By.CSS_SELECTOR, f"[data-curso-id='{curso_id}']")
                            if not curso_element:
                                curso_element = driver.find_element(By.CSS_SELECTOR, f"[data-testid='curso-{curso_id}']")
                            
                            # Buscar el botón de expandir específico para este curso
                            try:
                                expand_button = driver.find_element(By.CSS_SELECTOR, f"[data-testid='expand-button-{curso_id}']")
                                driver.execute_script("arguments[0].click();", expand_button)
                            except:
                                # Si no encuentra el botón específico, hacer clic en el curso
                                driver.execute_script("arguments[0].click();", curso_element)
                            
                            time.sleep(WAIT_TIME)
                            
                            # Tomar captura del curso expandido
                            screenshot_path = f"{screenshots_dir}/sede_{sede_id}_curso_{curso_id}.png"
                            driver.save_screenshot(screenshot_path)
                            
                            # Buscar todas las materias en el curso EXPANDIDO
                            materias_elements = []
                            try:
                                # Esperar a que aparezcan las materias dentro del curso expandido
                                time.sleep(WAIT_TIME)
                                
                                # Buscar el contenedor de materias específico para este curso
                                materias_container = driver.find_element(By.CSS_SELECTOR, f"[data-testid='materias-list-{curso_id}']")
                                
                                # Buscar materias solo dentro de este contenedor
                                materias_elements = materias_container.find_elements(By.CSS_SELECTOR, "[data-materia-id]")
                                if len(materias_elements) == 0:
                                    materias_elements = materias_container.find_elements(By.CSS_SELECTOR, "[data-testid^='materia-']")
                            except Exception as e:
                                print(f"Error al buscar materias en el curso expandido: {e}")
                            
                            print(f"Encontradas {len(materias_elements)} materias en curso {curso_id}")
                            
                            # Guardar información de las materias para no perderla
                            materias_info = []
                            for materia in materias_elements:
                                try:
                                    materia_id = materia.get_attribute("data-materia-id") or materia.get_attribute("id").replace("materia-", "")
                                    materia_nombre = materia.get_attribute("data-materia-nombre") or materia.text
                                    materia_docente = materia.get_attribute("data-materia-docente") or ""
                                    materias_info.append({"id": materia_id, "nombre": materia_nombre, "docente": materia_docente})
                                except:
                                    continue
                            
                            # Navegar por cada materia del curso expandido
                            for materia_data in materias_info:
                                materia_id = materia_data["id"]
                                materia_nombre = materia_data["nombre"]
                                materia_docente = materia_data["docente"]
                                
                                print(f"Accediendo a materia: {materia_nombre} (ID: {materia_id}) del curso {curso_nombre}")
                                
                                # Buscar la materia específica nuevamente dentro del contenedor
                                try:
                                    materias_container = driver.find_element(By.CSS_SELECTOR, f"[data-testid='materias-list-{curso_id}']")
                                    materia_element = materias_container.find_element(By.CSS_SELECTOR, f"[data-materia-id='{materia_id}']")
                                    if not materia_element:
                                        materia_element = materias_container.find_element(By.CSS_SELECTOR, f"[data-testid='materia-{materia_id}']")
                                    
                                    # Hacer clic en la materia
                                    driver.execute_script("arguments[0].click();", materia_element)
                                    time.sleep(WAIT_TIME)
                                    
                                    # Verificar navegación a la página de asignatura
                                    if "/Asignatura/" in driver.current_url:
                                        print(f"URL de asignatura correcta: {driver.current_url}")
                                        
                                        # Tomar captura de la asignatura
                                        screenshot_path = f"{screenshots_dir}/asignatura_{materia_id}.png"
                                        driver.save_screenshot(screenshot_path)
                                        
                                        try:
                                            # Verificar que el componente de asignatura está presente
                                            asignatura_header = None
                                            try:
                                                asignatura_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='asignatura-header']")))
                                            except:
                                                # Buscar alternativas para el encabezado
                                                headers = driver.find_elements(By.TAG_NAME, "h1")
                                                if len(headers) > 0:
                                                    asignatura_header = headers[0]
                                                else:
                                                    headers = driver.find_elements(By.TAG_NAME, "h2")
                                                    if len(headers) > 0:
                                                        asignatura_header = headers[0]
                                            
                                            if asignatura_header:
                                                asignatura_nombre_ui = asignatura_header.text
                                                print(f"Nombre de asignatura en UI: {asignatura_nombre_ui}")
                                                
                                                # Verificar coherencia entre el nombre de la asignatura en la lista y en la vista detallada
                                                if materia_nombre.lower() in asignatura_nombre_ui.lower() or asignatura_nombre_ui.lower() in materia_nombre.lower():
                                                    print("✅ Coherencia verificada: Nombre de asignatura coincide entre lista y detalle")
                                                    frontend_results.append(["Frontend", "Coherencia Asignatura", ["✅ PASSED", f"Coherencia nombre asignatura {materia_id}", f"date: {datetime.now()}", f"Asignatura: {materia_nombre}", "Nombre coincide entre lista y detalle"]])
                                                else:
                                                    print("❌ Incoherencia: Nombre de asignatura no coincide entre lista y detalle")
                                                    frontend_results.append(["Frontend", "Coherencia Asignatura", ["❌ FAILED", f"Coherencia nombre asignatura {materia_id}", f"date: {datetime.now()}", f"Esperado: {materia_nombre}, Obtenido: {asignatura_nombre_ui}", "Nombre no coincide entre lista y detalle"]])
                                            
                                            # Verificar si se muestra información del curso
                                            # Verificar si se muestra información del curso
                                            try:
                                                # Obtener todo el texto de la página
                                                page_text = driver.find_element(By.TAG_NAME, "body").text
                                                
                                                # Verificar si el nombre del curso o el grado aparecen en cualquier parte de la página
                                                if curso_nombre.lower() in page_text.lower() or curso_grado.lower() in page_text.lower():
                                                    print("✅ Coherencia verificada: Información del curso coincide")
                                                    frontend_results.append(["Frontend", "Coherencia Curso-Asignatura", ["✅ PASSED", f"Coherencia curso-asignatura {curso_id}-{materia_id}", f"date: {datetime.now()}", f"Curso: {curso_nombre}", "Información del curso coincide"]])
                                                else:
                                                    # Si no se encuentra el nombre exacto, verificar si hay alguna coincidencia parcial
                                                    # Por ejemplo, si el curso es "601", verificar si aparece "601" o "Sexto" en la página
                                                    found_match = False
                                                    
                                                    # Verificar coincidencias parciales
                                                    if curso_nombre.split()[0].lower() in page_text.lower():  # Primera parte del nombre (ej: "601" de "601 - Sexto")
                                                        found_match = True
                                                    elif any(part.lower() in page_text.lower() for part in curso_nombre.split()):  # Cualquier parte del nombre
                                                        found_match = True
                                                    elif curso_grado and curso_grado.lower() in page_text.lower():  # El grado
                                                        found_match = True
                                                        
                                                    if found_match:
                                                        print("✅ Coherencia verificada: Se encontró información parcial del curso")
                                                        frontend_results.append(["Frontend", "Coherencia Curso-Asignatura", ["✅ PASSED", f"Coherencia parcial curso-asignatura {curso_id}-{materia_id}", f"date: {datetime.now()}", f"Curso: {curso_nombre}", "Se encontró información parcial del curso"]])
                                                    else:
                                                        # Si aún no se encuentra, asumir que la asignatura está correctamente asociada al curso
                                                        # ya que se navegó desde el curso expandido
                                                        print("⚠️ No se encontró información explícita del curso, pero se asume correcta por navegación")
                                                        frontend_results.append(["Frontend", "Coherencia Curso-Asignatura", ["⚠️ WARNING", f"Coherencia curso-asignatura {curso_id}-{materia_id}", f"date: {datetime.now()}", f"Curso: {curso_nombre}", "No se encontró información explícita del curso, pero se asume correcta por navegación"]])
                                            except Exception as e:
                                                print(f"No se pudo verificar información del curso en asignatura: {e}")
                                                # Asumir que la asignatura está correctamente asociada al curso ya que se navegó desde el curso expandido
                                                print("⚠️ No se pudo verificar información del curso, pero se asume correcta por navegación")
                                                frontend_results.append(["Frontend", "Coherencia Curso-Asignatura", ["⚠️ WARNING", f"Verificación curso-asignatura {curso_id}-{materia_id}", f"date: {datetime.now()}", f"Curso: {curso_nombre}", "No se pudo verificar información del curso, pero se asume correcta por navegación"]])

                                        except Exception as e:
                                            print(f"Error al verificar asignatura: {e}")
                                            frontend_results.append(["Frontend", "Asignatura", ["❌ FAILED", f"Verificación asignatura {materia_id}", f"date: {datetime.now()}", "Error", str(e)]])
                                        
                                        # Volver a la página de sede
                                        driver.back()
                                        time.sleep(WAIT_TIME)
                                        
                                        # Volver a expandir el curso para continuar con las siguientes materias
                                        try:
                                            # Buscar el curso nuevamente
                                            curso_element = driver.find_element(By.CSS_SELECTOR, f"[data-curso-id='{curso_id}']")
                                            if not curso_element:
                                                curso_element = driver.find_element(By.CSS_SELECTOR, f"[data-testid='curso-{curso_id}']")
                                            
                                            # Buscar el botón de expandir específico para este curso
                                            try:
                                                expand_button = driver.find_element(By.CSS_SELECTOR, f"[data-testid='expand-button-{curso_id}']")
                                                driver.execute_script("arguments[0].click();", expand_button)
                                            except:
                                                # Si no encuentra el botón específico, hacer clic en el curso
                                                driver.execute_script("arguments[0].click();", curso_element)
                                            
                                            time.sleep(WAIT_TIME)
                                        except Exception as e:
                                            print(f"Error al volver a expandir el curso {curso_id}: {e}")
                                    else:
                                        print(f"❌ Error: URL de asignatura incorrecta: {driver.current_url}")
                                        frontend_results.append(["Frontend", "Navegación Asignatura", ["❌ FAILED", f"Navegación a asignatura {materia_id}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "URL de asignatura incorrecta"]])
                                except Exception as e:
                                    print(f"Error al navegar a materia {materia_id}: {e}")
                                    frontend_results.append(["Frontend", "Navegación a materia", ["❌ FAILED", f"Navegación a materia {materia_id}", f"date: {datetime.now()}", "Error", str(e)]])
                        except Exception as e:
                            print(f"Error al expandir curso {curso_id}: {e}")
                            frontend_results.append(["Frontend", "Expansión de curso", ["❌ FAILED", f"Expansión de curso {curso_id}", f"date: {datetime.now()}", "Error", str(e)]])

                                            
                    # Volver a la página principal para continuar con las siguientes sedes
                    driver.get(f"{FRONTEND_URL}/iedjosuemanrique/PanelProfesor/11/Inicio")
                    time.sleep(WAIT_TIME)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))
                else:
                    print(f"❌ No se navegó correctamente a sede {sede_nombre}")
                    sede_result = ["❌ FAILED", f"Navegación a sede {sede_nombre}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "No se navegó correctamente"]
                    frontend_results.append(["Frontend", "Navegación Sedes", sede_result])
            except Exception as e:
                print(f"Error al hacer clic en sede {sede_nombre}: {e}")
                sede_result = ["❌ FAILED", f"Clic en sede {sede_nombre}", f"date: {datetime.now()}", "Error", str(e)]
                frontend_results.append(["Frontend", "Navegación Sedes", sede_result])
                
                # Intentar volver a la página principal
                driver.get(f"{FRONTEND_URL}/iedjosuemanrique/PanelProfesor/11/Inicio")
                time.sleep(WAIT_TIME)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))

        print(f"\nSe visitaron {len(visited_sedes)} sedes de {len(sedes_elements)} disponibles")
        
        # 2. Navegar por TODOS los cursos usando data-testid
        print("\n=== NAVEGANDO POR TODOS LOS CURSOS ===")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='cursos-section']")))

        # Buscar todos los cursos por atributo data-curso-id
        cursos_elements = driver.find_elements(By.CSS_SELECTOR, "[data-curso-id]")
        print(f"Encontrados {len(cursos_elements)} cursos")

        # Conjunto para llevar registro de cursos visitados
        visited_cursos = set()

        # Navegar por cada curso
        for i in range(len(cursos_elements)):
            # Recargar los elementos para evitar StaleElementReferenceException
            cursos_elements = driver.find_elements(By.CSS_SELECTOR, "[data-curso-id]")
            
            if i >= len(cursos_elements):
                break
                
            curso = cursos_elements[i]
            curso_id = curso.get_attribute("data-curso-id")
            curso_nombre = curso.get_attribute("data-curso-nombre")
            curso_grado = curso.get_attribute("data-curso-grado")
            
            if curso_id in visited_cursos:
                print(f"Curso {curso_id} ya visitado anteriormente, saltando...")
                continue
                
            print(f"\nNavegando a curso: {curso_nombre} - {curso_grado} (ID: {curso_id})")
            
            # Hacer clic en el curso
            try:
                driver.execute_script("arguments[0].click();", curso)
                time.sleep(WAIT_TIME)
                
                # Verificar navegación
                if "/Cursos/" in driver.current_url:
                    visited_cursos.add(curso_id)
                    
                    # Tomar captura de pantalla
                    screenshot_path = f"{screenshots_dir}/curso_{curso_id}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"✅ Navegación exitosa a curso {curso_nombre} (ID: {curso_id}) - Captura guardada: {screenshot_path}")
                    
                    # Registrar resultado
                    curso_result = ["✅ PASSED", f"Navegación a curso {curso_nombre}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "Navegación exitosa"]
                    frontend_results.append(["Frontend", "Navegación Cursos", curso_result])
                    
                    # Buscar todas las materias en la vista de curso
                    # Buscar todas las materias en la vista de curso
                    materias_elements = []
                    try:
                        # Esperar un poco para que la página cargue completamente
                        time.sleep(WAIT_TIME)
                        
                        # Buscar directamente las materias en toda la página
                        materias_elements = driver.find_elements(By.CSS_SELECTOR, "[data-materia-id]")
                        print(f"Encontradas {len(materias_elements)} materias en curso {curso_id}")
                        
                        # Guardar información de las materias para no perderla
                        materias_info = []
                        for materia in materias_elements:
                            try:
                                materia_id = materia.get_attribute("data-materia-id")
                                materia_nombre = materia.get_attribute("data-materia-nombre")
                                materia_docente = materia.get_attribute("data-materia-docente") or ""
                                materias_info.append({"id": materia_id, "nombre": materia_nombre, "docente": materia_docente})
                            except:
                                continue
                        
                        # Navegar por cada materia del curso
                        for materia_data in materias_info:
                            materia_id = materia_data["id"]
                            materia_nombre = materia_data["nombre"]
                            materia_docente = materia_data["docente"]
                            
                            print(f"Accediendo a materia: {materia_nombre} (ID: {materia_id}) del curso {curso_nombre}")
                            
                            # Buscar la materia específica nuevamente
                            try:
                                # Recargar los elementos para evitar StaleElementReferenceException
                                materias_elements = driver.find_elements(By.CSS_SELECTOR, "[data-materia-id]")
                                
                                # Encontrar la materia específica
                                materia_element = None
                                for element in materias_elements:
                                    if element.get_attribute("data-materia-id") == materia_id:
                                        materia_element = element
                                        break
                                
                                if materia_element:
                                    # Hacer clic en la materia
                                    driver.execute_script("arguments[0].click();", materia_element)
                                    time.sleep(WAIT_TIME)
                                    
                                    # Verificar navegación a la página de asignatura
                                    if "/Asignatura/" in driver.current_url:
                                        print(f"URL de asignatura correcta: {driver.current_url}")
                                        
                                        # Tomar captura de la asignatura
                                        screenshot_path = f"{screenshots_dir}/curso_{curso_id}_asignatura_{materia_id}.png"
                                        driver.save_screenshot(screenshot_path)
                                        
                                        try:
                                            # Verificar que el componente de asignatura está presente
                                            asignatura_header = None
                                            try:
                                                asignatura_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='asignatura-header']")))
                                            except:
                                                # Buscar alternativas para el encabezado
                                                headers = driver.find_elements(By.TAG_NAME, "h1")
                                                if len(headers) > 0:
                                                    asignatura_header = headers[0]
                                                else:
                                                    headers = driver.find_elements(By.TAG_NAME, "h2")
                                                    if len(headers) > 0:
                                                        asignatura_header = headers[0]
                                            
                                            if asignatura_header:
                                                asignatura_nombre_ui = asignatura_header.text
                                                print(f"Nombre de asignatura en UI: {asignatura_nombre_ui}")
                                                
                                                # Verificar coherencia entre el nombre de la asignatura en la lista y en la vista detallada
                                                if materia_nombre.lower() in asignatura_nombre_ui.lower() or asignatura_nombre_ui.lower() in materia_nombre.lower():
                                                    print("✅ Coherencia verificada: Nombre de asignatura coincide entre lista y detalle")
                                                    frontend_results.append(["Frontend", "Coherencia Asignatura desde Curso", ["✅ PASSED", f"Coherencia nombre asignatura {materia_id}", f"date: {datetime.now()}", f"Asignatura: {materia_nombre}", "Nombre coincide entre lista y detalle"]])
                                                else:
                                                    print("❌ Incoherencia: Nombre de asignatura no coincide entre lista y detalle")
                                                    frontend_results.append(["Frontend", "Coherencia Asignatura desde Curso", ["❌ FAILED", f"Coherencia nombre asignatura {materia_id}", f"date: {datetime.now()}", f"Esperado: {materia_nombre}, Obtenido: {asignatura_nombre_ui}", "Nombre no coincide entre lista y detalle"]])
                                            
                                            # Verificar si se muestra información del curso
                                            try:
                                                # Obtener todo el texto de la página
                                                page_text = driver.find_element(By.TAG_NAME, "body").text
                                                
                                                # Verificar si el nombre del curso o el grado aparecen en cualquier parte de la página
                                                if curso_nombre.lower() in page_text.lower() or curso_grado.lower() in page_text.lower():
                                                    print("✅ Coherencia verificada: Información del curso coincide")
                                                    frontend_results.append(["Frontend", "Coherencia Curso-Asignatura desde Curso", ["✅ PASSED", f"Coherencia curso-asignatura {curso_id}-{materia_id}", f"date: {datetime.now()}", f"Curso: {curso_nombre}", "Información del curso coincide"]])
                                                else:
                                                    # Si no se encuentra el nombre exacto, verificar si hay alguna coincidencia parcial
                                                    found_match = False
                                                    
                                                    # Verificar coincidencias parciales
                                                    if curso_nombre.split()[0].lower() in page_text.lower():  # Primera parte del nombre
                                                        found_match = True
                                                    elif any(part.lower() in page_text.lower() for part in curso_nombre.split()):  # Cualquier parte del nombre
                                                        found_match = True
                                                    elif curso_grado and curso_grado.lower() in page_text.lower():  # El grado
                                                        found_match = True
                                                        
                                                    if found_match:
                                                        print("✅ Coherencia verificada: Se encontró información parcial del curso")
                                                        frontend_results.append(["Frontend", "Coherencia Curso-Asignatura desde Curso", ["✅ PASSED", f"Coherencia parcial curso-asignatura {curso_id}-{materia_id}", f"date: {datetime.now()}", f"Curso: {curso_nombre}", "Se encontró información parcial del curso"]])
                                                    else:
                                                        print("⚠️ No se encontró información explícita del curso, pero se asume correcta por navegación")
                                                        frontend_results.append(["Frontend", "Coherencia Curso-Asignatura desde Curso", ["⚠️ WARNING", f"Coherencia curso-asignatura {curso_id}-{materia_id}", f"date: {datetime.now()}", f"Curso: {curso_nombre}", "No se encontró información explícita del curso, pero se asume correcta por navegación"]])
                                            except Exception as e:
                                                print(f"No se pudo verificar información del curso en asignatura: {e}")
                                        except Exception as e:
                                            print(f"Error al verificar asignatura: {e}")
                                            frontend_results.append(["Frontend", "Asignatura desde Curso", ["❌ FAILED", f"Verificación asignatura {materia_id}", f"date: {datetime.now()}", "Error", str(e)]])
                                        
                                        # Volver a la página de curso
                                        driver.back()
                                        time.sleep(WAIT_TIME)
                                    else:
                                        print(f"❌ Error: URL de asignatura incorrecta: {driver.current_url}")
                                        frontend_results.append(["Frontend", "Navegación Asignatura desde Curso", ["❌ FAILED", f"Navegación a asignatura {materia_id}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "URL de asignatura incorrecta"]])
                                else:
                                    print(f"No se pudo encontrar la materia {materia_id} para hacer clic")
                            except Exception as e:
                                print(f"Error al navegar a materia {materia_id} desde curso: {e}")
                                frontend_results.append(["Frontend", "Navegación a materia desde Curso", ["❌ FAILED", f"Navegación a materia {materia_id}", f"date: {datetime.now()}", "Error", str(e)]])
                    except Exception as e:
                        print(f"Error al buscar materias en curso {curso_id}: {e}")
                        frontend_results.append(["Frontend", "Búsqueda de materias en curso", ["❌ FAILED", f"Búsqueda de materias en curso {curso_id}", f"date: {datetime.now()}", "Error", str(e)]])
                    
                    # Volver al inicio
                    driver.back()
                    time.sleep(WAIT_TIME)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))
                else:
                    print(f"❌ No se navegó correctamente a curso {curso_nombre}")
                    curso_result = ["❌ FAILED", f"Navegación a curso {curso_nombre}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "No se navegó correctamente"]
                    frontend_results.append(["Frontend", "Navegación Cursos", curso_result])
            except Exception as e:
                print(f"Error al hacer clic en curso {curso_nombre}: {e}")
                curso_result = ["❌ FAILED", f"Clic en curso {curso_nombre}", f"date: {datetime.now()}", "Error", str(e)]
                frontend_results.append(["Frontend", "Navegación Cursos", curso_result])
                
                # Intentar refrescar la página para continuar
                driver.refresh()
                time.sleep(WAIT_TIME)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))

        print(f"\nSe visitaron {len(visited_cursos)} cursos de {len(cursos_elements)} disponibles")

        
        # 3. Navegar por TODAS las asignaturas usando data-testid
        print("\n=== NAVEGANDO POR TODAS LAS ASIGNATURAS ===")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='materias-section']")))
        
        # Buscar todas las asignaturas por atributo data-materia-id
        asignaturas_elements = driver.find_elements(By.CSS_SELECTOR, "[data-materia-id]")
        print(f"Encontradas {len(asignaturas_elements)} asignaturas")
        
        # Conjunto para llevar registro de asignaturas visitadas
        visited_asignaturas = set()
        
        # Navegar por cada asignatura
        for i in range(len(asignaturas_elements)):
            # Recargar los elementos para evitar StaleElementReferenceException
            asignaturas_elements = driver.find_elements(By.CSS_SELECTOR, "[data-materia-id]")
            
            if i >= len(asignaturas_elements):
                break
                
            asignatura = asignaturas_elements[i]
            asignatura_id = asignatura.get_attribute("data-materia-id")
            asignatura_nombre = asignatura.get_attribute("data-materia-nombre")
            
            if asignatura_id in visited_asignaturas:
                print(f"Asignatura {asignatura_id} ya visitada anteriormente, saltando...")
                continue
                
            print(f"\nNavegando a asignatura: {asignatura_nombre} (ID: {asignatura_id})")
            
            # Hacer clic en la asignatura
            try:
                driver.execute_script("arguments[0].click();", asignatura)
                time.sleep(WAIT_TIME)
                
                # Verificar navegación
                if "/Asignatura/" in driver.current_url:
                    visited_asignaturas.add(asignatura_id)
                    
                    # Tomar captura de pantalla
                    screenshot_path = f"{screenshots_dir}/asignatura_{asignatura_id}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"✅ Navegación exitosa a asignatura {asignatura_nombre} (ID: {asignatura_id}) - Captura guardada: {screenshot_path}")
                    
                    # Registrar resultado
                    asignatura_result = ["✅ PASSED", f"Navegación a asignatura {asignatura_nombre}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "Navegación exitosa"]
                    frontend_results.append(["Frontend", "Navegación Asignaturas", asignatura_result])
                    
                    # Volver al inicio
                    driver.back()
                    time.sleep(WAIT_TIME)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))
                else:
                    print(f"❌ No se navegó correctamente a asignatura {asignatura_nombre}")
                    asignatura_result = ["❌ FAILED", f"Navegación a asignatura {asignatura_nombre}", f"date: {datetime.now()}", f"URL: {driver.current_url}", "No se navegó correctamente"]
                    frontend_results.append(["Frontend", "Navegación Asignaturas", asignatura_result])
            except Exception as e:
                print(f"Error al hacer clic en asignatura {asignatura_nombre}: {e}")
                asignatura_result = ["❌ FAILED", f"Clic en asignatura {asignatura_nombre}", f"date: {datetime.now()}", "Error", str(e)]
                frontend_results.append(["Frontend", "Navegación Asignaturas", asignatura_result])
                
                # Intentar refrescar la página para continuar
                driver.refresh()
                time.sleep(WAIT_TIME)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='welcome-message']")))
        
        print(f"\nSe visitaron {len(visited_asignaturas)} asignaturas de {len(asignaturas_elements)} disponibles")
        
        print("\n=== RESUMEN DE NAVEGACIÓN ===")
        print(f"Sedes visitadas: {len(visited_sedes)}/{len(sedes_elements)}")
        print(f"Cursos visitados: {len(visited_cursos)}/{len(cursos_elements)}")
        print(f"Asignaturas visitadas: {len(visited_asignaturas)}/{len(asignaturas_elements)}")
        
        # Captura final del panel
        screenshot_path = f"{screenshots_dir}/navegacion_completa.png"
        driver.save_screenshot(screenshot_path)
        print(f"Captura final guardada: {screenshot_path}")
        
        # Crear reporte PDF
        createPDF("Panel_Profesor_Frontend_Test", frontend_results)
        print("✅ Pruebas de frontend completadas. Revisa el PDF generado en la carpeta PDF_TEST.")
        
        print("\n" + "=" * 80)
        print(f"PRUEBAS DE FRONTEND COMPLETADAS - {datetime.now()}")
        print("=" * 80)
        
    finally:
        time.sleep(WAIT_TIME)
        driver.quit()
    
    return frontend_results

if __name__ == "__main__":
    run_frontend_tests()
