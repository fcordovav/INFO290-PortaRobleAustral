def proyecto_schema(proyecto) -> dict:
    return {
        "id": str(proyecto["_id"]),
        "titulo": proyecto["titulo"],
        "estado": proyecto["estado"],
        "fecha_inicio": proyecto["fecha_inicio"],
        "fecha_fin": proyecto.get("fecha_fin",None),
        "resumen": proyecto["resumen"],
        "autor": proyecto["autor"],
        "cuerpo": proyecto["cuerpo"],
        "imagen": proyecto["imagen"],
        "galeria_imagenes": proyecto["galeria_imagenes"],
        "instituciones": proyecto["instituciones"],
        "participantes": proyecto["participantes"],
        "url_proyecto": proyecto.get("url_proyecto", ""),
        "url_github": proyecto.get("url_github", ""),
        "pdf": proyecto["pdf"],
        "etiquetas": proyecto["etiquetas"]
    }

def proyectos_schema(proyectos) -> list:
    return [proyecto_schema(proyecto) for proyecto in proyectos]
