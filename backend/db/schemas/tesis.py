
def tesis_schema(tesis) -> dict:
    return {
        "id": str(tesis["_id"]),
        "titulo": tesis["titulo"],
        "autor": tesis["autor"],
        "fecha_inicio": tesis["fecha_inicio"],  
        "fecha_fin": tesis.get("fecha_fin", None),
        "estado": tesis["estado"],
        "resumen": tesis["resumen"],
        "pdf": tesis["pdf"],
        "carta_de_apoyo": tesis.get("carta_de_apoyo"),
        "url_github": tesis.get("url_github"),
        "galeria_imagenes": tesis.get("galeria_imagenes"),
        "participantes": tesis.get("participantes"),
        "patrocinantes": tesis.get("patrocinantes"),
        "copatrocinantes": tesis.get("copatrocinantes"),
        "instituciones": tesis.get("instituciones"),
        "nivel": tesis["nivel"],
        "tipo": tesis["tipo"],
        "carrera": tesis["carrera"],
        "etiquetas": tesis["etiquetas"]
    }

def tesises_schema(tesis_list) -> list:
    return [tesis_schema(tesis) for tesis in tesis_list]

def tesise_schema(tesis_list) -> list:
    return [tesis_schema(tesis_list)]
