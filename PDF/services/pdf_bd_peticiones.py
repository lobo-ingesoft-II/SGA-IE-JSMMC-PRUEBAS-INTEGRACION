from sqlalchemy.orm import Session
from PDF.models.Log import LogPdf

def create_log_pdf(db:Session, name):
    # Crear un log a partir del model
    db_curso = LogPdf()
    db_curso.title = name

    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def get_curso(db:Session, id:int):
    db_curso = db.query(LogPdf).filter(LogPdf.id == id).first()
    return db_curso


def get_next_id(db: Session) -> int:
    last_log = db.query(LogPdf).order_by(LogPdf.id.desc()).first()
    if last_log:
        return last_log.id + 1
    else:
        return 1

def get_all_logs(db: Session):
    logs = db.query(LogPdf).all()
    return logs
