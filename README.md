# Pruebas de Integración - Módulo de Gestión Académica

Las pruebas de integración del Panel de Profesor verifican la comunicación entre backend y frontend mediante:

### Backend (usando unittest y requests):

- **Autenticación**: Verifica la obtención de tokens JWT mediante solicitudes POST.
- **Consulta de datos**: Prueba endpoints GET para sedes, cursos y asignaturas, validando respuestas con esquemas JSON.
- **Pruebas negativas**: Verifica el comportamiento con credenciales incorrectas y tokens inválidos.
- **Flujo completo**: Comprueba relaciones entre entidades (sedes-cursos-asignaturas).

### Frontend (usando Selenium WebDriver):

- **Login**: Automatiza la entrada de credenciales y verifica redirección correcta.
- **Navegación**: Simula clics en sidebar, sedes, cursos y asignaturas.
- **Verificación visual**: Captura pantallas en cada paso para documentar el comportamiento.
- **Validación de datos**: Comprueba que la información mostrada coincida con la esperada.

Ambos componentes generan reportes PDF detallados con los resultados de cada prueba.

## Funcionalidades Adicionales (Planificadas)

### Gestión de Asistencia:
- **Backend**: Pruebas para registrar y consultar asistencia mediante API.
- **Frontend**: Automatización de marcado de asistencia y verificación de contadores actualizados.

### Gestión de Calificaciones:
- **Backend**: Pruebas para crear, actualizar y calcular notas mediante API.
- **Frontend**: Automatización de entrada de calificaciones y verificación de promedios.

### Observaciones Disciplinarias:
- **Backend**: Pruebas para crear y consultar observaciones mediante API.
- **Frontend**: Automatización del registro de incidentes y verificación en historial.

Estas nuevas pruebas seguirán el mismo patrón de validación y documentación que las existentes, asegurando la integridad del sistema completo.

# Pruebas de Integración - Sistema de Gestión Académica IE JSMMC

Este repositorio contiene pruebas automatizadas que verifican la integración entre los microservicios de backend y las aplicaciones frontend del Sistema de Gestión Académica de la Institución Educativa Departamental Josué Manrique.

## Requisitos Generales

- Python 3.8+
- Chrome WebDriver
- Microservicios backend (puertos 8000-8012)
- Frontend (puerto 3000)
- Servicio de generación de PDF (puerto 8051)

## Configuración Inicial

### Iniciar servicio de PDF:
```bash
uvicorn PDF.main:app --reload --port 8051
```

Este servicio es necesario para la generación de reportes y la base de datos SQLite.

### Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Configurar entorno:
- Copie `.env.example` a `.env` y ajuste las URLs de los servicios
- Actualice los archivos de credenciales según el módulo a probar

## Módulos de Pruebas

### 1. Panel de Profesor (Test/Test_panel_profesor/)
Pruebas para el módulo de gestión docente:

- **Backend**: Verifica autenticación JWT, consulta de sedes asignadas, cursos por sede y asignaturas por curso. Incluye validación de esquemas JSON y pruebas con credenciales inválidas.
- **Frontend**: Automatiza login, navegación por sidebar, selección de sedes/cursos/asignaturas, y captura pantallas para documentación visual.
- **Ejecución**: `python Test/Test_panel_profesor/run_tests.py`

### 2. Autenticación (Test/Test_autenticacion/)
Pruebas del sistema de login para diferentes roles:

- **Backend**: Verifica endpoints de autenticación para administradores, profesores y acudientes. Valida tokens JWT y manejo de errores.
- **Frontend**: Prueba formulario de login, validaciones de campos, mensajes de error y redirecciones según rol de usuario.
- **Ejecución**: `python Test/Test_autenticacion/run_tests.py`

### 3. Panel de Administrador (Test/Test_panel_admin/)
Pruebas para la gestión administrativa:

- **Backend**: Verifica operaciones CRUD para usuarios, sedes, cursos y asignaturas. Prueba validaciones de datos y permisos.
- **Frontend**: Automatiza interfaces de administración, formularios de creación/edición y verificación de listados.
- **Ejecución**: `python Test/Test_panel_admin/run_tests.py`

### 4. Panel de Acudiente (Test/Test_panel_acudiente/)
Pruebas para el acceso de padres/acudientes:

- **Backend**: Verifica consulta de estudiantes asociados, notas por periodo, asistencia y comunicaciones del colegio.
- **Frontend**: Prueba visualización de información académica, reportes de asistencia y acceso a comunicaciones institucionales.
- **Ejecución**: `python Test/Test_panel_acudiente/run_tests.py`

### 5. Registro de Asistencia (Test/Test_asistencia/)
Pruebas para el control de asistencia:

- **Backend**: Verifica registro de asistencia por estudiante, consulta de reportes por fecha/curso y cálculo de estadísticas.
- **Frontend**: Automatiza interfaz de marcado de asistencia, filtros de búsqueda y generación de reportes.
- **Ejecución**: `python Test/Test_asistencia/run_tests.py`

### 6. Gestión de Calificaciones (Test/Test_calificaciones/)
Pruebas para el sistema de notas:

- **Backend**: Verifica creación y actualización de calificaciones, cálculo de promedios y validación de rangos de notas.
- **Frontend**: Prueba interfaces de registro de notas, boletines de calificaciones y reportes académicos.
- **Ejecución**: `python Test/Test_calificaciones/run_tests.py`

### 7. Observaciones Disciplinarias (Test/Test_observaciones/)
Pruebas para el registro de comportamiento:

- **Backend**: Verifica creación de observaciones disciplinarias, consulta por estudiante/fecha y seguimiento de incidentes.
- **Frontend**: Automatiza interfaz de registro de incidentes, historial disciplinario y notificaciones a acudientes.
- **Ejecución**: `python Test/Test_observaciones/run_tests.py`

## Arquitectura de Pruebas

### Backend Testing
- **Framework**: unittest con requests para llamadas HTTP
- **Validaciones**: Códigos de estado, esquemas JSON, integridad de datos
- **Autenticación**: Verificación de tokens JWT y manejo de sesiones
- **Pruebas negativas**: Comportamiento con datos inválidos y errores

### Frontend Testing
- **Framework**: Selenium WebDriver para automatización de UI
- **Validaciones**: Elementos de interfaz, flujos de navegación, datos mostrados
- **Documentación**: Capturas de pantalla en puntos clave
- **Interacciones**: Clics, formularios, validaciones de cliente

## Reportes y Artefactos

- **Capturas**: Almacenadas en `screenshots/` para documentación visual
- **Reportes PDF**: Generados en `PDF_TEST/` con resultados detallados
- **Base de datos**: Registros de pruebas en `pdf.db` (SQLite)
- **Logs**: Información detallada de ejecución y errores

## Estructura del Proyecto

```
├── PDF/                      # Servicio de generación de reportes
├── Test/                     # Módulos de pruebas
│   ├── Test_panel_profesor/  # Pruebas del panel docente
│   ├── Test_autenticacion/   # Pruebas de login
│   ├── Test_panel_admin/     # Pruebas de administración
│   ├── Test_panel_acudiente/ # Pruebas de portal para padres
│   ├── Test_asistencia/      # Pruebas de control de asistencia
│   ├── Test_calificaciones/  # Pruebas de gestión de notas
│   └── Test_observaciones/   # Pruebas de registro disciplinario
├── config.py                 # Configuración global
├── requirements.txt          # Dependencias
└── .env                      # Variables de entorno
```

## Buenas Prácticas Implementadas

- **Aislamiento**: Cada prueba es independiente y puede ejecutarse por separado
- **Validación completa**: Se verifican códigos de estado y estructura de datos
- **Manejo de errores**: Captura y documenta fallos con información detallada
- **Pruebas negativas**: Verifica comportamiento con entradas inválidas
- **Documentación visual**: Capturas de pantalla en puntos clave del flujo
- **Reportes detallados**: Documentación PDF con resultados y evidencias

## Ejecución de Pruebas

### Ejecutar todas las pruebas:
```bash
# Desde la raíz del proyecto
python -m pytest Test/ -v
```

### Ejecutar módulo específico:
```bash
# Ejemplo: solo pruebas de autenticación
python Test/Test_autenticacion/run_tests.py
```

### Ejecutar con reportes:
```bash
# Generar reportes detallados
python Test/Test_panel_profesor/run_tests.py --verbose
```

## Contribución

1. Clone el repositorio
2. Cree una rama para su funcionalidad (`git checkout -b feature/nueva-prueba`)
3. Implemente sus pruebas siguiendo el patrón existente
4. Asegúrese de que las pruebas pasen localmente
5. Envíe un pull request con descripción detallada

Para más detalles sobre la implementación de cada módulo, consulte los archivos README específicos en cada directorio de pruebas.