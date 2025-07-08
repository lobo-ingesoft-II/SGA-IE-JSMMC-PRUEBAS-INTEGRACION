from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from PDF.backend.session import SessionLocal
from PDF.backend.database import get_db


router = APIRouter()


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from PDF.backend.database import get_db  # Asegúrate de tener esta dependencia bien definida
from PDF.models.Log import LogPdf  # Asegúrate que el modelo herede de Base y tenga __tablename__

router = APIRouter()

# ✅ Esquema Pydantic para la entrada
class LogCreate(BaseModel):
    title: str

# 
@router.post("/logs", status_code=201)
def create_log(log_data: LogCreate, db: Session = Depends(get_db)):
    if not log_data.title:
        raise HTTPException(status_code=400, detail="Título inválido")

    log = LogPdf(title=log_data.title)
    db.add(log)
    db.commit()
    db.refresh(log)

    return {"id": log.id, "title": log.title}

# @service_d.route('/pdf/logs', methods=['GET'])
# def get_logs():
#     logs = Log_PDF.query.all()
#     return jsonify([{'id': l.id, 'title': l.title} for l in logs]), 200

# @service_d.route('/pdf/logs/getId', methods=['GET'])
# def get_next_id():
#     last_log = Log_PDF.query.order_by(Log_PDF.id.desc()).first()
#     if last_log:
#         result =  last_log.id + 1
#     else:
#         result = 1
#     return jsonify({'id': result}), 200


# Crear las tablas antes de arrancar el servidor