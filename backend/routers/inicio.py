from fastapi import APIRouter
from db.client import db_client
from db.schemas.inicio import inicio_schema
from db.models.inicio import Inicio

router = APIRouter(prefix="/inicio", 
                    tags=["inicio"],
                    responses={404: {"message":"no encontrado"} })

@router.get("/")
async def get_inicio():
    inicio = db_client.roble_db.inicio.find_one()

    return inicio_schema(inicio)

@router.post("/")
async def post_inicio(inicio : Inicio):
    
    inicio_dict = dict(inicio)
    del inicio_dict["id"]

    id = db_client.roble_db.inicio.insert_one(inicio_dict).inserted_id    

    return inicio_schema(** db_client.roble_db.inicio.find_one({"_id":id}))