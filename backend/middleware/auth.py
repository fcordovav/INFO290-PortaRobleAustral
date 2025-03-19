from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()
SESSION_TOKEN = os.getenv("SESSION_TOKEN")

#app = FastAPI()

async def validate_password(request: Request):

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Contraseña no proporcionada o formato incorrecto")

    password = auth_header.split(" ")[1]  # Obtener la contraseña después de "Bearer"
    if password != SESSION_TOKEN:
        raise HTTPException(status_code=403, detail="Contraseña incorrecta")

    return True
