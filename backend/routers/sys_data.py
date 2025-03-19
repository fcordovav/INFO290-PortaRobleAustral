from fastapi import APIRouter
from db.client import db_client

router = APIRouter(
    prefix="/sys_data",
    tags=["/sys_data"],
    responses={404: {"message": "No encontrado"}},
)

@router.get("/etiquetas_{opcion}")
async def read_etiquetas(opcion: str):
    etiquetas_cursor = db_client.roble_db.sys_data.find({"key": "etiquetas"})
    etiquetas_list = list(etiquetas_cursor)[0]

    match opcion:
        case "only_etiquetas":
            data_out = []
            for obj in etiquetas_list["valores"]:
                if "etiquetas_arr" in obj:  
                    data_out.extend(obj["etiquetas_arr"]) 
            return {"etiquetas": data_out}
        
        case "etiqueta_color":
            data_out = {}
            for obj in etiquetas_list["valores"]:
                if "etiquetas_arr" in obj and "color" in obj:
                    for etiqueta in obj["etiquetas_arr"]:
                        data_out[etiqueta] = obj["color"]  
            return {"COLORES_ETIQUETAS": data_out}
