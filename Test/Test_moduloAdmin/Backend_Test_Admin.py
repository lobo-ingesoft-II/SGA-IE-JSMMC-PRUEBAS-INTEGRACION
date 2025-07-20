import requests
from datetime import datetime
import sys, os

# Añadir ruta raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Test.config import settings
from PDF.services.creation_PDF import createPDF
from PDF.backend.session import Base, engine

Base.metadata.create_all(bind=engine)

BASE_URL = f"{settings.url_api_sga_portal_admin}/portal_admin"

def generar_resultado(nombre_prueba, response, esperado=True):
    status = response.status_code
    texto = response.text
    estado = "✅ PASSED" if (status in [200, 201] and esperado) or (status >= 400 and not esperado) else "❌ FAILED"
    return [estado, nombre_prueba, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Status: {status}", f"Respuesta: {texto}"]

def integration_test_portal_admin():
    resultados = []
    usuarios_creados = []

    # Usuarios de prueba
    usuarios_test = [
        {
            "nombre_prueba": "Crear Profesor",
            "rol": "profesor",
            "email": "test.profesor2@ejemplo.com",
            "documento": "111121111",
            "datos_adicionales": {
                "especialidad": "Matemáticas",
                "es_director": True
            }
        },
        {
            "nombre_prueba": "Crear Administrador",
            "rol": "administrador",
            "email": "test.admin2@ejemplo.com",
            "documento": "222212222",
            "datos_adicionales": {}
        },
        {
            "nombre_prueba": "Crear Acudiente",
            "rol": "acudiente",
            "email": "test.acudiente2@ejemplo.com",
            "documento": "333323333",
            "datos_adicionales": {
                "parentesco": "Madre",
                "celular": "3119876543",
                "direccion": "Calle Falsa 123"
            }
        }
    ]

    for usuario in usuarios_test:
        data = {
            "nombres": "Test",
            "apellidos": usuario["rol"].capitalize(),
            "tipo_documento": "CC",
            "documento_identidad": usuario["documento"],
            "telefono": "3001234567",
            "email": usuario["email"],
            "contrasena": "clave12345",
            "rol": usuario["rol"],
            "datos_adicionales": usuario["datos_adicionales"]
        }

        r = requests.post(f"{BASE_URL}/usuarios", json=data)
        resultados.append(["Backend", usuario["nombre_prueba"], generar_resultado(usuario["nombre_prueba"], r)])

        json_resp = {}
        try:
            json_resp = r.json()
        except Exception:
            pass

        if r.status_code in [200, 201] and "id_usuario" in json_resp:
            user_id = json_resp["id_usuario"]
            usuarios_creados.append(user_id)

            # Editar
            r2 = requests.patch(f"{BASE_URL}/usuarios/{user_id}", json={"telefono": "3010000000"})
            resultados.append(["Backend", "Editar " + usuario["rol"], generar_resultado("Editar " + usuario["rol"], r2)])

            # Cambiar estado
            r3 = requests.patch(f"{BASE_URL}/usuarios/{user_id}/estado?estado=inactivo")
            resultados.append(["Backend", "Desactivar " + usuario["rol"], generar_resultado("Desactivar " + usuario["rol"], r3)])
        else:
            resultados.append(["Backend", "Falló creación → pruebas dependientes no ejecutadas", generar_resultado(f"No se pudo crear {usuario['rol']}", r, esperado=False)])

    # Consultas
    for ep in ["profesores", "acudientes", "administradores"]:
        r = requests.get(f"{BASE_URL}/{ep}")
        resultados.append(["Backend", f"GET {ep.capitalize()}", generar_resultado(f"GET {ep}", r)])

    # Casos con errores esperados
    r8 = requests.patch(f"{BASE_URL}/usuarios/999999", json={"telefono": "123"})
    resultados.append(["Backend", "Editar usuario inexistente", generar_resultado("Editar usuario que no existe", r8, esperado=False)])

    r9 = requests.delete(f"{BASE_URL}/usuarios/999999")
    resultados.append(["Backend", "Eliminar usuario inexistente", generar_resultado("Eliminar usuario que no existe", r9, esperado=False)])

    # 🔴 ELIMINAR usuarios creados
    for uid in usuarios_creados:
        r_del = requests.delete(f"{BASE_URL}/usuarios/{uid}")
        resultados.append(["Backend", f"Eliminar usuario {uid}", generar_resultado(f"Eliminar usuario {uid}", r_del)])

    # Crear PDF
    createPDF("CRUD_Usuarios_Backend", resultados)

if __name__ == "__main__":
    integration_test_portal_admin()
