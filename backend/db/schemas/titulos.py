def titulo_schema(titulo: dict) -> dict:
    return {
        "id": str(titulo["_id"]),
        "id_elem": str(titulo["id_elem"]),
        "titulo": titulo["titulo"],
        "id_elem": titulo["id_elem"],
        "etiquetas": titulo["etiquetas"],
        "url_path": titulo["url_path"],
        "tipo": titulo["tipo"]
    }

# Función para transformar una lista de documentos en una lista de esquemas
def titulos_schema(titulos: list) -> list:
    return [titulo_schema(titulo) for titulo in titulos]