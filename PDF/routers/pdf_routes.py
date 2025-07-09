from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from PDF.backend.database import get_db  # Asegúrate de tener esta dependencia bien definida
from PDF.models.Log import LogPdf  # Asegúrate que el modelo herede de Base y tenga __tablename__
from PDF.services.pdf_bd_peticiones import create_log_pdf, get_next_id, get_all_logs

router = APIRouter()

# ✅ Esquema Pydantic para la entrada
class LogCreate(BaseModel):
    title: str

@router.post("/log", status_code=201)
def create_log(logData: LogCreate, db: Session = Depends(get_db)):
    log = create_log_pdf(db, name=logData.title)
    if not log:
        raise HTTPException(status_code=400, detail="Error creating log")
    
    return {"id": log.id, "title": log.title}

@router.get('/logs', methods=['GET'])
def get_logs(db: Session = Depends(get_db)):
    logs = get_all_logs(db)
    return logs, 200

@router.get('/logs/getId', methods=['GET'])
def get_next_id(db: Session = Depends(get_db)):
    next_id = get_next_id(db)
    if next_id is None:
        raise HTTPException(status_code=404, detail="No logs found")
    return ({'id': next_id}), 200

