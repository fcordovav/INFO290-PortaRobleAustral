from fastapi import APIRouter, Query, HTTPException, Depends
from bson import ObjectId
from db.client import db_client
from db.schemas.noticia import noticia_schema, noticias_schema
from db.models.noticia import Noticia
from utils.date_utils import stringDate_to_dateDate
from middleware import auth
import httpx

import os
from dotenv import load_dotenv
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

router = APIRouter(prefix="/noticias", 
                    tags=["noticias"],
                    responses={404: {"message": "No encontrado"}})

@router.get("/")
async def read_noticias(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit  
    noticias_cursor = db_client.roble_db.noticias.find().sort("fecha", -1).skip(skip).limit(limit)
    
    noticias_lista = list(noticias_cursor)
    # print(noticias_lista)
    total_noticias = db_client.roble_db.noticias.count_documents({})

    return {
        "noticias": noticias_schema(noticias_lista),
        "total": total_noticias
    }

@router.get("/{id}")
def read_articulo_singular(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    noticia = db_client.roble_db.noticias.find_one({"_id": ObjectId(id)})
    if noticia:
        return noticia_schema(noticia)
    else:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

##PROTEGIDO
@router.post("/post", dependencies=[Depends(auth.validate_password)])
async def post_noticia(noticia: Noticia):
    noticia_dict = dict(noticia)
    noticia_dict.pop("id", None)

    if noticia_dict["fecha"] != "":
        noticia_dict["fecha"] = stringDate_to_dateDate(noticia_dict["fecha"])

    try:
        result = db_client.roble_db.noticias.insert_one(noticia_dict)

        titulo = {
            "id_elem": str(result.inserted_id),
            "etiquetas": [],
            "titulo": noticia_dict["titulo"],
            "url_path": "noticias/",
            "tipo": "noticia"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}/titulos", json=titulo)
            response.raise_for_status()

        return {"message": "Noticia creado exitosamente", "id": str(result.inserted_id)}, 201
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error de red al comunicarse con /titulos: {str(e)}")
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error en /titulos: {e.response.text}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la noticia: {str(e)}")


##PROTEGIDO
@router.delete("/delete/{id}", dependencies=[Depends(auth.validate_password)])
async def delete_noticia(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    try:
        result = db_client.roble_db.noticias.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Noticia no encontrada")
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{API_BASE_URL}/titulos/{id}")
            response.raise_for_status()

        return {"message": "Noticia eliminada correctamente", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la noticia: {str(e)}")
    
## PROTEGIDO
@router.put("/put/{id}",dependencies=[Depends(auth.validate_password)])
async def update_noticia(id: str, noticia: Noticia):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    noticia_dict = dict(noticia)
    noticia_dict.pop("id", None) 

    if noticia_dict["fecha"] != "":
        noticia_dict["fecha"] = stringDate_to_dateDate(noticia_dict["fecha"])

    try:
        result = db_client.roble_db.noticias.update_one(
            {"_id": ObjectId(id)},          # Filtro para encontrar el documento por ID
            {"$set": noticia_dict}     # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Noticia no encontrada")
        
        titulo = {
            "id_elem": str(id),
            "etiquetas": [],
            "titulo": noticia_dict["titulo"],
            "url_path": "noticias/",
            "tipo": "noticia"
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(f"{API_BASE_URL}/titulos/{id}", json=titulo)
            response.raise_for_status()

        return {"message": "Noticia actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la noticia: {str(e)}")