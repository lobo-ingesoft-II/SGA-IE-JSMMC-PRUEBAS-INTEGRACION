from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PDF.routers import  pdf_routes

import uvicorn
from PDF.backend.session import engine, Base


# Crear instancia de FastAPI
app = FastAPI(title="PDF-test API")


# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir dominios si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Registrar rutas
app.include_router(pdf_routes.router, prefix="/pdf", tags=["pdf"])


def create_tables():
    Base.metadata.create_all(bind=engine)
    

@app.on_event("startup")
def on_startup():
    print("Creando tablas en la base de datos (evento startup)...")
    create_tables()


# if __name__ == "__main__":
#     print("Creando tablas en la base de datos...")
#     create_tables()
#     uvicorn.run("main:app", host="0.0.0.0", port=5004, reload=True)


