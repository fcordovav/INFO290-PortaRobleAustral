def noticia_schema(noticia) -> dict:
    return{
        "id": str(noticia["_id"]),
        "titulo": noticia["titulo"],
        "imagenes": noticia.get("imagenes", []),
        "resumen": noticia["resumen"],
        "cuerpo": noticia["cuerpo"],
        "autor": noticia["autor"],
        "fecha": noticia["fecha"]
    }

def noticias_schema(noticias) -> list:
    return [noticia_schema(noticia) for noticia in noticias]
