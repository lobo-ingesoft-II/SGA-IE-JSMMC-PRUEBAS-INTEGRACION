from PDF.backend.config import settings # Traer el valor de configuración de la URI de MongoDB
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError



# Configuración de la conexión remota
# config = {
#     'host': settings.host_mysql,
#     'user': settings.user_mysql,
#     'password': settings.password_mysql,
#     'database': settings.database_mysql,
#     'port': settings.port_mysql
# }

print(settings)  # Imprimir la URI de conexión para verificar
# Construir la URL de conexión



# Crear engine
# engine = create_engine(settings.sqlalchemy_database_uri) # Gestiona las conexion en la app
DATABASE_URL = "sqlite:///./pdf.db"  # Usa ./ para ruta relativa

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite requiere este arg

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base declarativa para modelos
Base = declarative_base()  # Es la clase base de la que SE DEBEN HEREDAR todos los modelos o tablas 


