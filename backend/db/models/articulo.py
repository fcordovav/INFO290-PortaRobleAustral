from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from bson import ObjectId

class Institucion(BaseModel):
    nombre: str
    imagen: str

class Articulo(BaseModel):
    id: Optional[str] = Field(default=None)  
    titulo: str
    estado: str
    fechaIni: date
    fechaFin: Optional[date] | str = "" 
    autor: str
    galeria: List[str]
    resumen: str
    cuerpo: str
    link: Optional[str] = None
    instituciones: List[Institucion]        # Aca se debe de verificar esto en el endpoint
    participantes: List[str]       # ""
    pdf: bool  
    carta_de_apoyo: Optional[str] = None
    url_github: Optional[str] = None
    etiquetas: List[str]

    class Config:
        orm_mode = True  