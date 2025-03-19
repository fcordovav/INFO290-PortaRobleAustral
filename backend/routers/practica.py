from fastapi import APIRouter, Query, HTTPException, Depends
from bson import ObjectId  # Para manejar ObjectId en MongoDB
from db.client import db_client
from db.schemas.practica import practica_inicial_schema, practicas_iniciales_schema, practica_profesional_schema
from db.models.practica import PracticaInicial, PracticaProfesional, PracticaBase
from utils.date_utils import stringDate_to_dateDate
from middleware import auth
import httpx
import os
from dotenv import load_dotenv
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

router = APIRouter(prefix="/practicas", tags=["practicas"], responses={404: {"description": "No encontrado"}})


@router.get("/get_all")
async def get_all_practicas(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit  # Calcula el número de artículos a omitir
    tesis_cursor = db_client.roble_db.practicas.find().sort("fechaIni", -1).skip(skip).limit(limit)
    tesis_lista = list(tesis_cursor)

    total_tesis = db_client.roble_db.practicas.count_documents({})

    return {
        "practicas": practicas_iniciales_schema(tesis_lista),
        "total": total_tesis
    }

@router.get("/iniciales", response_model=list)
async def get_iniciales():
    practica = list(db_client.roble_db.practicas.find({"nivel": "Inicial"}).sort("fechaIni", -1))
    return practicas_iniciales_schema(practica)

@router.get("/profesionales", response_model=list)
async def get_profesionales():
    practica = list(db_client.roble_db.practicas.find({"nivel": "Profesional"}))
    return practicas_iniciales_schema(practica)

@router.get("/{id}", response_model=dict)
async def get_practica_by_id(id: str):
    practica = db_client.roble_db.practicas.find_one({"_id": ObjectId(id)})
    return practica_inicial_schema(practica)

@router.post("",dependencies=[Depends(auth.validate_password)])
async def create_practica(practica: PracticaBase):
    practica_dict = dict(practica)      
    practica_dict.pop("id", None) 

    if practica_dict["fechaIni"] != "" :
        practica_dict["fechaIni"] = stringDate_to_dateDate(practica_dict["fechaIni"]) 
    practica_dict["fechaFin"] = stringDate_to_dateDate(practica_dict["fechaFin"]) 

    practica_dict["instituciones"] = [institucion.model_dump() for institucion in practica.instituciones]

    try:
        result = db_client.roble_db.practicas.insert_one(practica_dict)

        tipo = "inicial"
        if practica_dict["nivel"] == "pro": tipo = "profesional"

        titulo = {
            "id_elem": str(result.inserted_id),
            "etiquetas": practica_dict["etiquetas"],
            "titulo": practica_dict["nombre"],
            "url_path": "practicas/",
            "tipo": f"practica {tipo}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}/titulos", json=titulo)
            response.raise_for_status()

        return {"message": "Practica creada exitosamente", "id": str(result.inserted_id)}, 201
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la practica: {str(e)}")

@router.put("/{id}",dependencies=[Depends(auth.validate_password)])
async def update_practica(id:str, practica: PracticaBase):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    practica_dict = dict(practica)      
    practica_dict.pop("id", None) 

    if practica_dict["fechaIni"] != "" :
        practica_dict["fechaIni"] = stringDate_to_dateDate(practica_dict["fechaIni"]) 
    practica_dict["fechaFin"] = stringDate_to_dateDate(practica_dict["fechaFin"]) 

    practica_dict["instituciones"] = [institucion.model_dump() for institucion in practica.instituciones]

    try:
        result = db_client.roble_db.practicas.update_one(
            {"_id": ObjectId(id)},          # Filtro para encontrar el documento por ID
            {"$set": practica_dict}         # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Practica no encontrada")
        
        tipo = "inicial"
        if practica_dict["nivel"] == "pro": tipo = "profesional"

        titulo = {
            "id_elem": str(id),
            "etiquetas": practica_dict["etiquetas"],
            "titulo": practica_dict["nombre"],
            "url_path": "practicas/",
            "tipo": f"practica {tipo}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(f"{API_BASE_URL}/titulos/{id}", json=titulo)
            response.raise_for_status()

        return {"message": "Practica actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la practica: {str(e)}")
    
@router.delete("/{id}",dependencies=[Depends(auth.validate_password)])
async def delete_practica(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    try:
        result = db_client.roble_db.practicas.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Practica no encontrada")
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{API_BASE_URL}/titulos/{id}")
            response.raise_for_status()

        return {"message": "Practica eliminada correctamente", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la practica: {str(e)}")