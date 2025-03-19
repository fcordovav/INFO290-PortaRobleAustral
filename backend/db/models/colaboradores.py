from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date

class Colaboracion(BaseModel):
    id: Optional[str] = Field(default=None)
    nombre: str
    links: List[Dict[str, str]]  
    fecha_ini: date
    fecha_fin: date | str = ""
    imagen: Optional[str] = None

