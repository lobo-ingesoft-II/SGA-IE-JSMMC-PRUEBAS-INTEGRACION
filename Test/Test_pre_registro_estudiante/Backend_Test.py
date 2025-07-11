import requests

import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PDF.services.creation_PDF import createPDF, input_data
from Test.config import settings
from datetime import datetime


def create_pre_registration():
    print(settings.url_api_sga_pre_registro)
    url = f"{settings.url_api_sga_pre_registro}/pre_registration"
    response = requests.post(url, json={
    "apellidos": "Pérez Gómez",
    "nombres": "Juan Carlos",
    "tipoDocumento": "Tarjeta de Identidad",
    "numeroDocumento": "1234567890",
    "fechaNacimiento": "2010-05-15",
    "paisNacimiento": "COLOMBIA",
    "departamentoNacimiento": "CUNDINAMARCA",
    "municipioNacimiento": "Yopal",
    "categoriaSisben": "A",
    "subcategoriaSisben": "A2",
    "direccionResidencia": "Calle 10 #5-20",
    "telefono": "3201234567",
    "rutaEscolar": "Ruta 1",
    "seguroMedico": "Nueva EPS",
    "discapacidad": "NO",
    "detalleDiscapacidad": "",
    "poblacionDesplazada": "NO",
    "fechaDesplazamiento": "",
    "paisResidencia": "COLOMBIA",
    "departamentoResidencia": "CUNDINAMARCA",
    "municipioResidencia": "Yopal",
    "gradoIngreso": "6",
    "institucionAnterior": "Colegio ABC",
    "municipioAnterior": "Yopal",
    "sede": "INSTITUCIÓN EDUCATIVA DEPARTAMENTAL JOSUÉ MANRIQUE",
    "acudiente1Parentesco": "Padre",
    "acudiente1Apellidos": "Pérez Rodríguez",
    "acudiente1Nombres": "Carlos Alberto",
    "acudiente1CC": "987654321",
    "acudiente1Celular": "3109876543",
    "acudiente1Ocupacion": "Ingeniero",
    "acudiente2Parentesco": "Madre",
    "acudiente2Apellidos": "Gómez Ruiz",
    "acudiente2Nombres": "María Fernanda",
    "acudiente2CC": "1122334455",
    "acudiente2Celular": "3112233445",
    "acudiente2Ocupacion": "Docente"
    })
    response.raise_for_status()
    pre_registration_data = response.json()

    message = pre_registration_data
    id = pre_registration_data["_id"]
    status_code = response.status_code

    print(message)
    return id, message, status_code 

def delete_pre_registration(id):
    url = f"{settings.url_api_sga_pre_registro}/pre_registration/{id}"
    response = requests.delete(url, json={})
    response.raise_for_status()
    data_response = response.json()

    status_code = response.status_code

    print(data_response)
    return data_response, status_code

def create_pdf_pre_registration(id):
    url =  f"{settings.url_api_sga_pdf}/pdf_pre_registro/{id}"
    print("PDFFFFF:", url)
    response = requests.post(url, json={})
    response.raise_for_status()
    data_response = response.json()

    status_code = response.status_code

    return data_response , status_code




def integration_test():
    array_data_pdf = []
    id_Pre_registration = ""
    try:
        # Paso 1: Crear pre-registro
        id, msg_creation, status_code = create_pre_registration()
        id_Pre_registration = id

            # Agregar arreglo para pdf 
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if status_code == 200:
            arrayProvisional = ["Backend", "Create pre_registration", ["PASSED", "Fill the form", f"date: {date_now}", f"{status_code}",f"{msg_creation}"]]
            print("(GOOD) Pre-registro creado:", msg_creation)
        else:
            arrayProvisional = ["Backend", "Create pre_registration", ["DID NOT PASS", "Fill the form", f"date: {date_now}", f"{status_code}",f"{msg_creation}"]]
            print("(BAD) PDF generado para el pre-registro")

        array_data_pdf.append(arrayProvisional)
        

        try: 
            # Paso 2: Crear PDF asociado al pre-registro

            msg_pdf , status_code = create_pdf_pre_registration(id_Pre_registration)
            print("\n\n ", id_Pre_registration)

                # Agregar arreglo para pdf 
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if status_code == 200:
                arrayProvisional = ["Backend", "Create PDF pre_registration", ["PASSED", "Create PDF", f"date: {date_now}", f"{status_code}",f"{msg_pdf}"]]
                print("(GOOD) PDF generado para el pre-registro")
            else:
                arrayProvisional = ["Backend", "Create PDF pre_registration", ["DID NOT PASS", "Create PDF", f"date: {date_now}", f"{status_code}",f"{msg_pdf}"]]
                print("(BAD) PDF generado para el pre-registro")

            array_data_pdf.append(arrayProvisional)

            

        except Exception as e:
            print("(BAD) Error crear PDF:", e)
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arrayProvisional = ["Backend", "Create pre_registration", ["DID NOT PASS- ERROR", "Fill the form", f"date: {date_now}", f"{e}"]]
            array_data_pdf.append(arrayProvisional)

            
    except Exception as e:
            print("(BAD) Error Creacion Pre-registro:", e)
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arrayProvisional = ["Backend", "Create pre_registration", ["DID NOT PASS- ERROR", "Fill the form", f"date: {date_now}", f"{e}"]]
            array_data_pdf.append(arrayProvisional)
    finally:
        # Paso 3: Eliminar el pre-registro (limpiar datos de prueba)
        if id_Pre_registration != "":
            try:
                msg_delte, status_code = delete_pre_registration(id)

                if status_code == 200:
                    arrayProvisional = ["Backend", "DELETE register pre_registration", ["PASSED", "delete pre-registration", f"date: {date_now}", f"{status_code}",f"{msg_creation}"]]
                    print("(GOOD) DELETE register  pre_registration")
                else:
                    arrayProvisional = ["Backend", "DELETE register  pre_registration", ["DID NOT PASS", "delete pre-registration", f"date: {date_now}", f"{status_code}",f"{msg_creation}"]]
                    print("(BAD) DELETE register  pre_registration")

                array_data_pdf.append(arrayProvisional)

            except Exception as e:
                print("⚠️ No se pudo eliminar el pre-registro:", e)
                date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                arrayProvisional = ["Backend", "DELETE register  pre_registration", ["DID NOT PASS- ERROR", "delete pre-registration", f"date: {date_now}", f"{status_code}",f"{msg_creation}"]]
                array_data_pdf.append(arrayProvisional)

    # imprimir el pdf     
    createPDF("Juan", array_data_pdf)

if __name__ == "__main__":
    # integration_test()
    integration_test()
    