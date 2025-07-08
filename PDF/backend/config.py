from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Database
    name_db_sqLite : str = Field(..., alias="NAME_DATABASE_SQLITE")
    # Request 
    url_api_sga_autenticacion : str = Field(..., alias="SERVIDOR_API_AUTENTICACION_URL")
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()