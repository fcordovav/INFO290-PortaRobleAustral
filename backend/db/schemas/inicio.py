def inicio_schema(inicio) -> dict:
    return {"id": str(inicio["_id"]),
            "descripcion":inicio["descripcion"],
            "imagen": inicio["imagen"]
            }

def inicios_schema(inicios) -> list:
    return [inicio_schema(inicio) for inicio in inicios]

