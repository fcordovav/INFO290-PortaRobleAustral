from fastapi import APIRouter,Depends, HTTPException
from db.client import db_client
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from fastapi import status
from dotenv import load_dotenv

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"message": "No encontrado"}}
)

#oauth2 = OAuth2PasswordBearer(tokenUrl="admin")
load_dotenv()

USER_ADM = os.getenv("USER_ADM")
PASS_ADM = os.getenv("PASS_ADM")
SESSION_TOKEN = os.getenv("SESSION_TOKEN")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/")
async def login( login_request: LoginRequest):
    if login_request.username == USER_ADM and login_request.password == PASS_ADM:
        return {"token": SESSION_TOKEN}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuario o contraseña incorrectos",
        headers={"WWW-Authenticate": "Bearer"},
    )