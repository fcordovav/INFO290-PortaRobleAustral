from fastapi import APIRouter, Query, HTTPException,Depends
from db.client import db_client
from db.schemas.instituciones import institucion_schema, instituciones_schema
from db.models.instituciones import Institucion
from bson import ObjectId
from middleware import auth

router = APIRouter(
    prefix="/instituciones",
    tags=["instituciones"],
    responses={404 : {"description" : "No Encontrado"}}
)

@router.get("")
async def read_titulos():
    lista_titulos = list(db_client.roble_db.instituciones.find())
    return instituciones_schema(lista_titulos)

@router.get("/paginated")
async def read_titulos(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit  
    instituciones_cursor = db_client.roble_db.instituciones.find().sort("fecha", -1).skip(skip).limit(limit)
    
    instituciones_lista = list(instituciones_cursor)
    total_instituciones = db_client.roble_db.instituciones.count_documents({})

    return {
        "noticias": instituciones_schema(instituciones_lista),
        "total": total_instituciones
    }

@router.post("",dependencies=[Depends(auth.validate_password)])
async def create_institucion(institucion: Institucion):
    institucion_dict = dict(institucion)

    db_client.roble_db.instituciones.insert_one(institucion_dict).inserted_id
    return (0)

@router.delete("/{id}",dependencies=[Depends(auth.validate_password)])
async def delete_institucion(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    result = db_client.roble_db.instituciones.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    
    return {"message": "Institución eliminada correctamente"}

@router.put("/{id}",dependencies=[Depends(auth.validate_password)])
async def update_institucion(id: str, institucion: Institucion):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    institucion_dict = dict(institucion)
    institucion_dict.pop("id", None)

    try:
        result = db_client.roble_db.instituciones.update_one(
            {"_id": ObjectId(id)},          # Filtro para encontrar el documento por ID
            {"$set": institucion_dict}       # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Institución no encontrada")
        return {"message": "Institución actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la institución: {str(e)}")