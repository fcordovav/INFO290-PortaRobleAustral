def institucion_schema(institucion) -> dict:
    return {
        "id": str(institucion["_id"]),
        "nombre": institucion["nombre"],
        "imagen": institucion["imagen"], 
    }

def instituciones_schema(instituciones) -> list:
    return [institucion_schema(institucion) for institucion in instituciones]
