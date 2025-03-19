from pydantic import BaseModel, Field
from typing import Optional, List

class Admin(BaseModel):
    id: Optional[str] = Field(default=None)  
    username: str
    password: str
    correo: str
    nickname: str

    class Config:
        orm_mode = True  