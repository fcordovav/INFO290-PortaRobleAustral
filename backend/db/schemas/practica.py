def practica_inicial_schema(practica) -> dict:
    return {
        "id": str(practica["_id"]),
        "nombre": practica["nombre"],
        "resumen": practica["resumen"],
        "fechaIni": practica["fechaIni"],
        "fechaFin": practica["fechaFin"],
        "estado": practica["estado"],
        "pdf": practica.get("pdf"),
        "galeria": practica["galeria"],
        "participantes": practica["participantes"],
        "instituciones": practica["instituciones"],
        "nivel": practica["nivel"],
        "tipo": practica.get(("tipo","")),
        "etiquetas": practica["etiquetas"]
    }

def practicas_iniciales_schema(practicas) -> list:
    return [practica_inicial_schema(practica) for practica in practicas]

def practica_profesional_schema(practica) -> dict:
    return practica_inicial_schema(practica)  
