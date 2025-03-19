def articulo_schema(articulo) -> dict:
    return {
        "id": str(articulo["_id"]),
        "titulo": articulo["titulo"],
        "estado": articulo["estado"],
        "fechaIni": articulo["fechaIni"],
        "fechaFin": articulo["fechaFin"] if articulo["fechaFin"] != "Actualidad" else None,
        "resumen": articulo["resumen"],
        "cuerpo": articulo["cuerpo"],
        "autor": articulo["autor"],
        "participantes": articulo["participantes"],
        "galeria": articulo["galeria"],
        "link": articulo["link"],
        "instituciones": articulo["instituciones"],
        "pdf": articulo["pdf"],
        "carta_de_apoyo": articulo.get("carta_de_apoyo", ""),
        "url_github": articulo.get("url_github", ""),
        "etiquetas": articulo["etiquetas"]
    }



def articulos_schema(articulos) -> list:
    return [articulo_schema(articulo) for articulo in articulos]

