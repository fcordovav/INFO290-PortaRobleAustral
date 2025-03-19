from pydantic import BaseModel, Field
from typing import List
from typing import List, Optional

class Titulo(BaseModel):
    id: Optional[str] = Field(default=None)
    id_elem: str
    etiquetas: List[str]
    titulo: str
    url_path: str
    tipo: str
