from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Institucion(BaseModel):
    nombre: str
    imagen: str

class TesisBase(BaseModel):
    id: Optional[str] = Field(default=None)
    titulo: str
    autor: str
    fecha_inicio: date | str = ""
    fecha_fin: Optional[date] | str = ""
    estado: str
    resumen: str
    pdf: bool
    carta_de_apoyo: Optional[str] = None
    url_github: Optional[str] = None
    galeria_imagenes: List[str]
    participantes: List[str]
    patrocinantes: List[str]
    copatrocinantes: List[str]
    instituciones: List[Institucion]
    nivel: str
    tipo: str
    carrera: str
    etiquetas: List[str]