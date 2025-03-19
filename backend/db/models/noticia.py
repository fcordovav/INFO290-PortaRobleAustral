from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Noticia(BaseModel):
    id: Optional[str] = Field(default=None)
    titulo: str
    imagenes: List[str] = Field(default_factory=list)
    resumen: str
    cuerpo: str
    autor: str
    fecha: date | str = ""

    class Config:
        from_attributes = True  # Permite trabajar con objetos ORM como dicts