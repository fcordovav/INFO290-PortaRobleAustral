from fastapi import APIRouter, HTTPException, Depends
from db.client import db_client
from db.schemas.persona import persona_schema, personas_schema
from db.models.persona import Persona
from bson.objectid import ObjectId
from utils.date_utils import stringDate_to_dateDate
from middleware import auth

router = APIRouter(
    prefix="/integrantes",
    tags=["integrantes"],
    responses={404 : {"description" : "No Encontrado"}}
)

@router.get("/")
async def read_personas():
    lista_personas = list(db_client.roble_db.personas.find().sort("fecha", -1))
    return personas_schema(lista_personas)

@router.post("/post",dependencies=[Depends(auth.validate_password)])
async def create_personas(persona : Persona):
    presona_dict = dict(persona)    # Se define que sera un diccionario
    presona_dict.pop("id", None)        # Eliminar el campo 'id' si existe (Se agrega automatico)

    if presona_dict["fecha"] != "":
        presona_dict["fecha"] = stringDate_to_dateDate(presona_dict["fecha"]) 

    db_client.roble_db.personas.insert_one(presona_dict).inserted_id
    return (0)

@router.delete("/delete/{id}",dependencies=[Depends(auth.validate_password)])
async def delete_personas(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    result = db_client.roble_db.personas.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    return {"message": "Persona eliminada correctamente"}

@router.put("/put/{id}",dependencies=[Depends(auth.validate_password)])
async def update_personas(id: str, persona : Persona):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    persona_dict = dict(persona)
    persona_dict.pop("id", None)

    if persona_dict["fecha"] != "":
        persona_dict["fecha"] = stringDate_to_dateDate(persona_dict["fecha"]) 

    try:
        result = db_client.roble_db.personas.update_one(
            {"_id": ObjectId(id)},       # Filtro para encontrar el documento por ID
            {"$set": persona_dict}       # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return {"message": "Persona actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar a la Persona: {str(e)}")