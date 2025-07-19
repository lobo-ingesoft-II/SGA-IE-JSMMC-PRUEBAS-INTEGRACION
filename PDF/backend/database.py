from PDF.backend.session import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text


def get_db():
    db = SessionLocal()

    # Utilizacion de Yield: Cuando FastAPI dectecta que se esta usando Yield entonces sabe que al finalizar el request debe cerrar la sesión automaticamente
    try:
        yield db
    finally:
        db.close()  # Se ejecuta siempre al final y libera el recurso Y EL RECURSO DEBE DE SER LIBERADO 
