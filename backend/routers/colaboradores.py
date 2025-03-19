from fastapi import APIRouter, HTTPException,Depends
from db.client import db_client
from db.schemas.colaboradores import colaboraciones_schema, colaboracion_schema 
from db.models.colaboradores import Colaboracion
from bson.objectid import ObjectId
from utils.date_utils import stringDate_to_dateDate
from middleware import auth

router = APIRouter(
    prefix="/colaboraciones",
    tags=["colaboraciones"],
    responses={404: {"description": "No encontrado"}}
)

# Get de todos los colaboradores
@router.get("/")
async def read_colaboraciones():
    try:
        colaboraciones_lista = list(db_client.roble_db.colaboraciones.find().sort("fecha_ini", -1))
        return colaboraciones_schema(colaboraciones_lista)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener colaboraciones: {str(e)}")

# Las fechas deben ser YYYY-mm-dd
@router.post("/post", dependencies=[Depends(auth.validate_password)])
async def create_colaboracion(colaboracion: Colaboracion):
    colaboracion_dict = dict(colaboracion)      
    colaboracion_dict.pop("id", None)           # Eliminar el campo 'id' si existe (Se agregara automatico)

    if colaboracion_dict["fecha_ini"] != "" :
        colaboracion_dict["fecha_ini"] = stringDate_to_dateDate(colaboracion_dict["fecha_ini"]) 
    colaboracion_dict["fecha_fin"] = stringDate_to_dateDate(colaboracion_dict["fecha_fin"]) 

    try:
        result = db_client.roble_db.colaboraciones.insert_one(colaboracion_dict)
        return {"message": "Colaboración creada exitosamente", "id": str(result.inserted_id)}, 201
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la colaboración: {str(e)}")

@router.delete("/delete/{id}", dependencies=[Depends(auth.validate_password)])
async def delete_colaboracion(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    try:
        result = db_client.roble_db.colaboraciones.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Colaboración no encontrada")
        return {"message": "Colaboración eliminada correctamente", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la colaboración: {str(e)}")

@router.put("/put/{id}", dependencies=[Depends(auth.validate_password)])
async def update_colaboracion(id: str, colaboracion: Colaboracion):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    colaboracion_dict = dict(colaboracion)
    colaboracion_dict.pop("id", None) 

    colaboracion_dict["fecha_ini"] = stringDate_to_dateDate(colaboracion_dict["fecha_ini"]) 
    colaboracion_dict["fecha_fin"] = stringDate_to_dateDate(colaboracion_dict["fecha_fin"]) 
    
    try:
        result = db_client.roble_db.colaboraciones.update_one(
            {"_id": ObjectId(id)},          # Filtro para encontrar el documento por ID
            {"$set": colaboracion_dict}     # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Colaboración no encontrada")
        return {"message": "Colaboración actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la colaboración: {str(e)}")