from fastapi import APIRouter, HTTPException,Depends
from db.client import db_client
from bson.objectid import ObjectId
from middleware import auth
from db.schemas.admin import admin_schema, admins_schema
from db.models.admin import Admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("")
async def read_admin():
    try:
        admin_lista = list(db_client.roble_db.admin.find())
        return admins_schema(admin_lista)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener a los administradores: {str(e)}")

@router.post("", dependencies=[Depends(auth.validate_password)])
async def create_admin(admin: Admin):
    admin_dict = dict(admin)      
    admin_dict.pop("id", None)        

    try:
        result = db_client.roble_db.admin.insert_one(admin_dict)
        return {"message": "Admin creado exitosamente", "id": str(result.inserted_id)}, 201
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear a el Admin: {str(e)}")

@router.delete("/{id}", dependencies=[Depends(auth.validate_password)])
async def delete_admin(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    try:
        result = db_client.roble_db.admin.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Admin no encontrado")
        return {"message": "Admin eliminado correctamente", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar a el Admin: {str(e)}")

@router.put("/{id}", dependencies=[Depends(auth.validate_password)])
async def update_admin(id: str, admin: Admin):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    admin_dict = dict(admin)
    admin_dict.pop("id", None) 

    try:
        result = db_client.roble_db.admin.update_one(
            {"_id": ObjectId(id)},          # Filtro para encontrar el documento por ID
            {"$set": admin_dict}     # Actualizar con los datos proporcionados
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Admin no encontrado")
        return {"message": "Admin actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar a el Admin: {str(e)}")