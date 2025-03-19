from pydantic import BaseModel, Field
from typing import Optional


class Inicio(BaseModel):
    id : str | None = Field(default = None)
    descripcion: str
    imagen: str