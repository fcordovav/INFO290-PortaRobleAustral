def persona_schema(persona) -> dict:
    return {
        "id": str(persona["_id"]),
        "nombre": persona["nombre"],
        "correo": persona["correo"], 
        "fecha": persona["fecha"],
        "imagen": persona["imagen"],
        "linkedin": persona["linkedin"], 
        "profesion": persona["profesion"],
        "orden": persona.get("orden", None)
    }

def personas_schema(personas) -> list:
    return [persona_schema(persona) for persona in personas]


def ordenar_personas(personas: list) -> list:
    return sorted(personas, key=lambda p: p.get("orden", float('inf')))
