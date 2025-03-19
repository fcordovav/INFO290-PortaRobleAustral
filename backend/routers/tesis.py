from fastapi import APIRouter,Query, HTTPException, Depends
from bson import ObjectId 
from db.client import db_client
from db.schemas.tesis import tesises_schema, tesis_schema
from db.models.tesis import  TesisBase
from utils.date_utils import stringDate_to_dateDate
from middleware import auth
import httpx

import os
from dotenv import load_dotenv
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

router = APIRouter(prefix="/tesis", tags=["tesis"])

@router.get("/get_all")
async def get_all_tesis(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit  
    tesis_cursor = db_client.roble_db.trabajosTitulo.find().sort("fecha_inicio", -1).skip(skip).limit(limit)
    tesis_lista = list(tesis_cursor)

    total_tesis = db_client.roble_db.trabajosTitulo.count_documents({})

    return {
        "tesis": tesises_schema(tesis_lista),
        "total": total_tesis
    }

@router.get("/pregrado")
async def get_tesis(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit  # Calcula el número de artículos a omitir

    articulos_cursor = db_client.roble_db.trabajosTitulo.find(
        {"nivel": "Pregrado"}
    ).sort("fecha_inicio", -1).skip(skip).limit(limit)

    articulos_lista = list(articulos_cursor)

    total_articulos = db_client.roble_db.trabajosTitulo.count_documents({"nivel": "Pregrado"})
    
    return {
        "articulos": tesises_schema(articulos_lista),
        "total": total_articulos
    }

@router.get("/postgrado",)
async def get_tesis(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit  # Calcula el número de artículos a omitir

    articulos_cursor = db_client.roble_db.trabajosTitulo.find(
        {"nivel": "Postgrado"}
    ).sort("fecha_inicio", -1).skip(skip).limit(limit)
    
    articulos_lista = list(articulos_cursor)
    
    total_articulos = db_client.roble_db.trabajosTitulo.count_documents({"nivel": "Postgrado"})

    return {
        "articulos": tesises_schema(articulos_lista),
        "total": total_articulos
    }

@router.get("/{id}", response_model=TesisBase)
def obtener_articulo_por_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    articulo = db_client.roble_db.trabajosTitulo.find_one({"_id": ObjectId(id)})
    if articulo:
        return tesis_schema(articulo)
    else:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

@router.post("",dependencies=[Depends(auth.validate_password)])
async def create_tesis(tesis: TesisBase):
    tesis_dict = dict(tesis)
    tesis_dict.pop("id", None)


    if tesis_dict["fecha_inicio"] != "":
        tesis_dict["fecha_inicio"] = stringDate_to_dateDate(tesis_dict["fecha_inicio"])
    tesis_dict["fecha_fin"] = stringDate_to_dateDate(tesis_dict["fecha_fin"]) 

    tesis_dict["instituciones"] = [institucion.model_dump() for institucion in tesis.instituciones]

    try:
        result = db_client.roble_db.trabajosTitulo.insert_one(tesis_dict)

        tipo = tesis_dict["tipo"]  
        nivel = tesis_dict["nivel"]

        titulo = {
            "id_elem": str(result.inserted_id),
            "etiquetas": tesis_dict["etiquetas"],
            "titulo": tesis_dict["titulo"],
            "url_path": "tesis/",
            "tipo": f"{tipo} {nivel}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}/titulos", json=titulo)
            response.raise_for_status()

        return {"message": "Tesis creada exitosamente", "id": str(result.inserted_id)}, 201
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error de red al comunicarse con /titulos: {str(e)}")
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error en /titulos: {e.response.text}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la tesis: {str(e)}")

@router.delete("/{id}",dependencies=[Depends(auth.validate_password)])
async def delete_tesis(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    try:
        result = db_client.roble_db.trabajosTitulo.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Tesis no encontrada")
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{API_BASE_URL}/titulos/{id}")
            response.raise_for_status()

        return {"message": "Tesis eliminada correctamente", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la tesis: {str(e)}")

@router.put("/{id}",dependencies=[Depends(auth.validate_password)])
async def update_articulo(id: str, tesis: TesisBase):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    tesis_dict = dict(tesis)
    tesis_dict.pop("id", None) 

    if tesis_dict["fecha_inicio"] != "":
        tesis_dict["fecha_inicio"] = stringDate_to_dateDate(tesis_dict["fecha_inicio"])
    tesis_dict["fecha_fin"] = stringDate_to_dateDate(tesis_dict["fecha_fin"]) 

    tesis_dict["instituciones"] = [institucion.model_dump() for institucion in tesis.instituciones]

    try:
        result = db_client.roble_db.trabajosTitulo.update_one(
            {"_id": ObjectId(id)},          # Filtro para encontrar el documento por ID
            {"$set": tesis_dict}            # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Tesis no encontrado")
        
        tipo = tesis_dict["tipo"]  
        nivel = tesis_dict["nivel"]

        titulo = {
            "id_elem": str(id),
            "etiquetas": tesis_dict["etiquetas"],
            "titulo": tesis_dict["titulo"],
            "url_path": "tesis/",
            "tipo": f"{tipo} {nivel}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(f"{API_BASE_URL}/titulos/{id}", json=titulo)
            response.raise_for_status()

        return {"message": "Tesis actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la tesis: {str(e)}")