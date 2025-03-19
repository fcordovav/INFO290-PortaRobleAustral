from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Institucion(BaseModel):
    id: Optional[str] = Field(default=None)
    nombre: str
    imagen: str