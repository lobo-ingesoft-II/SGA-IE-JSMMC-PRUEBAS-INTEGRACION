import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PDF.services.creation_PDF import createPDF, input_data
from Test.config import settings
from datetime import datetime

def open_frontend(driver):
    # Opens the frontend application in the browser
    url_page = f"{settings.url_api_frontend}/iedjosuemanrique/autenticacion/prematricula"
    driver.get(url_page)
    time.sleep(2)  # Give the page time to load



from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def fill_form(driver, wait):
    # Apellidos
    last_name_input = wait.until(EC.presence_of_element_located((By.NAME, "apellidos")))
    last_name_input.send_keys("Franco Ruiz")

    # Nombres
    names_input = wait.until(EC.presence_of_element_located((By.NAME, "nombres")))
    names_input.send_keys("Jhoan Sebastian")

    # Lista combox
        # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r5:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'Registro Civil de Nacimiento')]")
    ))
    option.click()

    # Numero Documento
    numeroDocumento_input = wait.until(EC.presence_of_element_located((By.NAME, "numeroDocumento")))
    numeroDocumento_input.send_keys("111852872")

    # Poner Fecha
    fecha_input = wait.until(EC.presence_of_element_located((By.NAME, "fechaNacimiento")))
    fecha_input.send_keys("05-11-2010")

    # Poner Pais ComBox ya esta
        # colombia
    
    # Poner Departamento
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":rf:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'TOLIMA')]")
    ))
    option.click()

    # Poner Municipio Nacimiento
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r2v:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'ARMERO')]")
    ))
    option.click()

    # Categoria Sisben 
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":rj:")))
    select_box.click()

                # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'A')]")
    ))
    option.click()

    # Sub Categoria Sisben 
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":rn:")))
    select_box.click()

                # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'A3')]")
    ))
    option.click()

    # Direccion de Residencia
    address_input = wait.until(EC.presence_of_element_located((By.NAME, "direccionResidencia")))
    address_input.send_keys("cll 56a sur # 27 -75")

    # Telefono
    tel_input = wait.until(EC.presence_of_element_located((By.NAME, "telefono")))
    tel_input.send_keys("cll 56a sur # 27 -75")

    # Ruta Escolar 
    ruta_input = wait.until(EC.presence_of_element_located((By.NAME, "rutaEscolar")))
    ruta_input.send_keys("Ruta-pepito S.A")

    # Seguro Eps
    seguroMedico_input = wait.until(EC.presence_of_element_located((By.NAME, "seguroMedico")))
    seguroMedico_input.send_keys("Compensar")

    
    # Discapacidad
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r13:")))
    select_box.click()

                # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'NO')]")
    ))
    option.click()

    # Poblacion desplazada 
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r17:")))
    select_box.click()

                # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'NO')]")
    ))
    option.click()
    
    # Poner Pais RESIDENCIA ComBox ya esta
        # colombia
    
    # Poner Departamento RESIDENCIA
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r1f:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'TOLIMA')]")
    ))
    option.click()

    # Poner Municipio Nacimiento RESIDENCIA
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r33:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'ARMERO')]")
    ))
    option.click()


    # -------------------------------------- INFORMACION ACADEMICA 
    # Grado al que ingresa 
        #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r1j:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'Sexto')]")
    ))
    option.click()

    # Institucion de donde viene
    ruta_input = wait.until(EC.presence_of_element_located((By.NAME, "institucionAnterior")))
    ruta_input.send_keys("Colegio el cerrito I.E")

    # Municipio
    municipio_input = wait.until(EC.presence_of_element_located((By.NAME, "municipioAnterior")))
    municipio_input.send_keys("Villavicencio")

    # Sede
            #Lista combox
                # Paso 1: Hacer clic en el combobox para abrir la lista
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r1r:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'ESCUELA RURAL BOTELLAS')]")
    ))
    option.click()

    #-------------------------------Acudiente 
    # Parentesco
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r1v:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'Padre')]")
    ))
    option.click()

    # Apellidos 
    apellido_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente1Apellidos")))
    apellido_input.send_keys("Franco Herrera")

    # Nombres 
    nombres_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente1Nombres")))
    nombres_input.send_keys("Juan Esteban")

    # Numero cedula 
    numeroCedula_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente1CC")))
    numeroCedula_input.send_keys("80072168")

    # Numero celular 
    numeroCedula_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente1Celular")))
    numeroCedula_input.send_keys("3054741424")

    # Ocupacion
    ocupacion =  wait.until(EC.presence_of_element_located((By.NAME, "acudiente1Ocupacion")))
    ocupacion.send_keys("Bombero")


        #-------------------------------Acudiente 2 
    # Parentesco
    select_box = wait.until(EC.element_to_be_clickable((By.ID, ":r2d:")))
    select_box.click()

        # Paso 2: Esperar a que se despliegue la lista y seleccionar la opción
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(), 'Madre')]")
    ))
    option.click()

    # Apellidos 
    apellido_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente2Apellidos")))
    apellido_input.send_keys("Ruiz Carrillo")

    # Nombres 
    nombres_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente2Nombres")))
    nombres_input.send_keys("Paola")

    # Numero celular 
    numeroCedula_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente2Celular")))
    numeroCedula_input.send_keys("3054741424")


    # Numero cedula 
    numeroCedula_input = wait.until(EC.presence_of_element_located((By.NAME, "acudiente2CC")))
    numeroCedula_input.send_keys("12156456")

    # Ocupacion
    ocupacion =  wait.until(EC.presence_of_element_located((By.NAME, "acudiente2Ocupacion")))
    ocupacion.send_keys("Administradora")
    #--------------------------------- llamar BOTON 
    boton = driver.find_element(By.XPATH, "//button[contains(text(), 'Registrar Estudiante')]")
    print("Voy a hacer clic...")
    boton.click()

    time.sleep(0.5)
    try:
        print("Esperando alerta JS...")
        WebDriverWait(driver, 30).until(EC.alert_is_present())
        alerta = driver.switch_to.alert
        print("Texto de la alerta:", alerta.text)
        time.sleep(0.5)
        alerta.accept()
        print("Alerta aceptada correctamente.")
    except Exception as e:
        print("No se pudo capturar la alerta:", e)





def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        open_frontend(driver)
        # Step 1: Create user
        fill_form(driver, wait)

        time.sleep(15)  # Final delay to observe results if not running headless

    finally:
        driver.quit()  # Always close the browser at the end


if __name__ == "__main__":
    main()
