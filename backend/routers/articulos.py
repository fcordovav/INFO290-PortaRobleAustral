from fastapi import APIRouter, Query, HTTPException,Depends
from bson import ObjectId
from db.client import db_client
from db.schemas.articulo import articulo_schema, articulos_schema
from db.models.articulo import Articulo
from utils.date_utils import stringDate_to_dateDate
from middleware import auth
import httpx
import os 
from dotenv import load_dotenv

router = APIRouter(prefix="/articulos", 
                    tags=["articulos"],
                    responses={404: {"message":"no encontrado"} })

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

# Get todos los articulos
@router.get("/")
async def read_articulos(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit 

    articulos_cursor = db_client.roble_db.articulos.find().sort("fechaIni", -1).skip(skip).limit(limit)
    articulos_lista = list(articulos_cursor)
    total_articulos = db_client.roble_db.articulos.count_documents({})

    return {
        "articulos": articulos_schema(articulos_lista),
        "total": total_articulos
    }

# Get de un articulo (singular)
@router.get("/{id}", response_model=Articulo)
def read_articulo_singular(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    articulo = db_client.roble_db.articulos.find_one({"_id": ObjectId(id)})
    if articulo:
        return articulo_schema(articulo)
    else:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

@router.post("/post", dependencies=[Depends(auth.validate_password)])
async def create_articulo(articulo: Articulo):
    articulo_dict = dict(articulo)
    articulo_dict.pop("id", None)

    if articulo_dict["fechaIni"] != "":
        articulo_dict["fechaIni"] = stringDate_to_dateDate(articulo_dict["fechaIni"])
    articulo_dict["fechaFin"] = stringDate_to_dateDate(articulo_dict["fechaFin"]) 

    articulo_dict["instituciones"] = [institucion.model_dump() for institucion in articulo.instituciones]

    try:
        result = db_client.roble_db.articulos.insert_one(articulo_dict)

        titulo = {
            "id_elem": str(result.inserted_id),
            "etiquetas": articulo_dict["etiquetas"],
            "titulo": articulo_dict["titulo"],
            "url_path": "articulos/",
            "tipo": "articulo"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}/titulos", json=titulo)
            response.raise_for_status()

        return {"message": "Articulo creado exitosamente", "id": str(result.inserted_id)}, 201
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error de red al comunicarse con /titulos: {str(e)}")
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error en /titulos: {e.response.text}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el articulo: {str(e)}")

@router.delete("/delete/{id}", dependencies=[Depends(auth.validate_password)])
async def delete_articulo(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    try:
        result = db_client.roble_db.articulos.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Articulo no encontrado")
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{API_BASE_URL}/titulos/{id}")
            response.raise_for_status()

        return {"message": "Articulo eliminado correctamente", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el articulo: {str(e)}")

@router.put("/put/{id}", dependencies=[Depends(auth.validate_password)])
async def update_articulo(id: str, articulo: Articulo):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    articulo_dict = dict(articulo)
    articulo_dict.pop("id", None) 

    if articulo_dict["fechaIni"] != "":
        articulo_dict["fechaIni"] = stringDate_to_dateDate(articulo_dict["fechaIni"])
    articulo_dict["fechaFin"] = stringDate_to_dateDate(articulo_dict["fechaFin"]) 

    articulo_dict["instituciones"] = [institucion.model_dump() for institucion in articulo.instituciones]
    
    try:
        result = db_client.roble_db.articulos.update_one(
            {"_id": ObjectId(id)},          # Filtro para encontrar el documento por ID
            {"$set": articulo_dict}         # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Articulo no encontrado")
        
        titulo = {
            "id_elem": str(id),
            "etiquetas": articulo_dict["etiquetas"],
            "titulo": articulo_dict["titulo"],
            "url_path": "articulos/",
            "tipo": "articulo"
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(f"{API_BASE_URL}/titulos/{id}", json=titulo)
            response.raise_for_status()

        return {"message": "Articulo actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el articulo: {str(e)}")