from fastapi import APIRouter, Query, HTTPException, Depends
from bson import ObjectId
import httpx
from db.client import db_client
from db.schemas.proyecto import proyecto_schema, proyectos_schema
from db.models.proyecto import Proyecto
from utils.date_utils import stringDate_to_dateDate
from middleware import auth
import os
from dotenv import load_dotenv
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

router = APIRouter(
    prefix="/proyectos",
    tags=["proyectos"],
    responses={404: {"message": "No encontrado"}}
)

# Get con paginación
@router.get("/")
async def get_proyectos(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=100)):
    skip = (page - 1) * limit
    proyectos_cursor = db_client.roble_db.proyectos.find().sort("fecha_inicio", -1).skip(skip).limit(limit)
    proyectos_lista = list(proyectos_cursor)
    total_proyectos = db_client.roble_db.proyectos.count_documents({})
    return {
        "proyectos": proyectos_schema(proyectos_lista),
        "total": total_proyectos
    }

# Get por ID
@router.get("/{id}", response_model=Proyecto)
async def obtener_proyecto_por_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    proyecto = db_client.roble_db.proyectos.find_one({"_id": ObjectId(id)})
    if proyecto:
        return proyecto_schema(proyecto)
    else:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

@router.post("",response_model=Proyecto,dependencies=[Depends(auth.validate_password)])
async def post_noticia(noticia: Proyecto):
    proyecto_dict = noticia.model_dump(exclude={"id"})
    id = db_client.roble_db.proyectos.insert_one(proyecto_dict).inserted_id

    titulo = {
        "id_elem": str(id),
        "etiquetas": proyecto_dict["etiquetas"],
        "titulo": proyecto_dict["titulo"],
        "url_path": "proyectos/",
        "tipo": "proyecto"
    }

    async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}/titulos", json=titulo)
            response.raise_for_status()

    return proyecto_schema(db_client.roble_db.proyectos.find_one({"_id": id}))

# Put (actualización) por ID
@router.put("/{id}", response_model=dict,dependencies=[Depends(auth.validate_password)])
async def update_proyecto(id: str, proyecto: Proyecto):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    proyecto_dict = proyecto.model_dump(exclude={"id"})

    # Convertir fechas
    try:
        proyecto_dict["fecha_inicio"] = stringDate_to_dateDate(proyecto_dict["fecha_inicio"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fecha de inicio inválida: {e}")

    try:
        proyecto_dict["fecha_fin"] = stringDate_to_dateDate(proyecto_dict["fecha_fin"]) if proyecto_dict.get("fecha_fin") else None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fecha de fin inválida: {e}")

    result = db_client.roble_db.proyectos.update_one(
        {"_id": ObjectId(id)},
        {"$set": proyecto_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    titulo = {
        "id_elem": str(id),
        "etiquetas": proyecto_dict["etiquetas"],
        "titulo": proyecto_dict["titulo"],
        "url_path": "proyectos/",
        "tipo": "proyecto"
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(f"{API_BASE_URL}/titulos/{id}", json=titulo)
        response.raise_for_status()

    
    return {"message": "Proyecto actualizado correctamente"}

# Delete por ID
@router.delete("/{id}", response_model=dict, dependencies=[Depends(auth.validate_password)])
async def delete_proyecto(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    result = db_client.roble_db.proyectos.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{API_BASE_URL}/titulos/{id}")
        response.raise_for_status()
    
    return {"message": "Proyecto eliminado correctamente"}
