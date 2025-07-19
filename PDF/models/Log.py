from sqlalchemy import Column, Integer, String
from PDF.backend.session import Base  # Asegúrate de que este sea el declarative_base()

class LogPdf(Base):  # Se recomienda usar PascalCase
    __tablename__ = "log_pdf"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)