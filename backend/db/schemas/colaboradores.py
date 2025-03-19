def colaboracion_schema(colaboracion) -> dict:
    return {
        "id": str(colaboracion["_id"]),
        "nombre": colaboracion["nombre"],
        "links": colaboracion["links"], 
        "fecha_ini": colaboracion["fecha_ini"],
        "fecha_fin": colaboracion["fecha_fin"],
        "imagen": colaboracion["imagen"]
    }

def colaboraciones_schema(colaboraciones) -> list:
    return [colaboracion_schema(colaboracion) for colaboracion in colaboraciones]
