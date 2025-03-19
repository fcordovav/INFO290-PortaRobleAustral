from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Persona(BaseModel):
    id: Optional[str] = Field(default=None)
    nombre: str
    correo: str 
    fecha: date | str = ""
    imagen: str
    linkedin: str 
    profesion: str
    orden: Optional[int] = Field(default=None)