from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Institucion(BaseModel):
    nombre: str
    imagen: str

class PracticaBase(BaseModel):
    id: Optional[str] = Field(default=None)
    nombre: str
    resumen: str
    fechaIni: date | str = ""
    fechaFin: date | str = ""
    estado: str
    nivel: str
    tipo: Optional[str] = None
    pdf: Optional[str] = None
    galeria: List[str]
    participantes: List[str]
    instituciones: List[Institucion]
    etiquetas: List[str]

class PracticaInicial(PracticaBase):
    pass

class PracticaProfesional(PracticaBase):
    pass
