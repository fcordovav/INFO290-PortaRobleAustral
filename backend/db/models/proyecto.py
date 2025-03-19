from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from bson import ObjectId

class Institucion(BaseModel):
    nombre: str
    imagen: str

class Proyecto(BaseModel):
    id: Optional[str] = Field(default=None)  # Cambiado a Optional[str] para ser más explícito
    titulo: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] | str = ""  # Optional para la fecha de fin
    autor: str
    imagen: str
    cuerpo: str
    galeria_imagenes: List[str]
    resumen: str
    instituciones: List[Institucion]
    participantes: List[str]
    url_proyecto: Optional[str] = None
    url_github: Optional[str] = None
    pdf: bool
    etiquetas: List[str]

    class Config:
        orm_mode = True  # Esto permite que Pydantic trabaje con objetos ORM como si fueran dicts

