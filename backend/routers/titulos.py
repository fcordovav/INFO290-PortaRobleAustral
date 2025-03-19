from fastapi import APIRouter, Query, HTTPException
from db.client import db_client
from db.models.titulos import Titulo
from db.schemas.titulos import titulo_schema, titulos_schema
from bson import ObjectId

router = APIRouter(
    prefix="/titulos",
    tags=["titulos"],
    responses={404 : {"description" : "No Encontrado"}}
)

@router.get("/")
async def get_titulos():
    lista_titulos = list(db_client.roble_db.titulos.find())
    return titulos_schema(lista_titulos)

@router.post("")
async def create_titulo(titulo: Titulo):
    titulo_dict = dict(titulo)

    try:
        result = db_client.roble_db.titulos.insert_one(titulo_dict)
        return {"message": "Titulo creado exitosamente", "id": str(result.inserted_id)}, 201
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el titulo: {str(e)}")
    
@router.delete("/{id}")
async def delete_titulo(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    try:
        result = db_client.roble_db.titulos.delete_one({"id_elem": id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Titulo no encontrado")
        return {"message": "Titulo eliminado correctamente", "id_elem": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el titulo: {str(e)}")

@router.put("/{id}")
async def update_titulo(id: str, titulo: Titulo):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    titulo_dict = dict(titulo)

    try:
        result = db_client.roble_db.titulos.update_one(
            {"id_elem": id}, 
            {"$set": titulo_dict}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Titulo no encontrado")
        return {"message": "Titulo actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el titulo: {str(e)}")