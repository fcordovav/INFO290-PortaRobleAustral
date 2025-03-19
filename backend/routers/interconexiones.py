import re
import httpx
import unicodedata
from fastapi import APIRouter
from collections import Counter
from db.client import db_client

import os
from dotenv import load_dotenv
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

router = APIRouter(
    prefix="/interconexiones",
    tags=["interconexiones"],
    responses={404: {"message": "No encontrado"}},
)


STOP_WORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "y", "o", "de", "del", "en", "por", "con", "para", "a", "que", "se", "es", 
    "no", "al", "su", "lo", "como", "si", "pero", "más", "sin", "of", "for",
    "the", "and", "is", "in", "to", "that", "it", "with", "as", "was", "at", 
    "by", "on", "an", "be", "this", "which", "or", "from", "but", "not", 
    "are", "have", "we", "has", "you", "their", "all", "can", "there", 
    "will", "up", "if", "about", "who", "how", "some", "into", "your", "hasn't",
    "they", "i", "me", "my", "our", "ours", "its", "yours", "ourselves", "we're",
    "these", "those", "so", "just", "her", "hers", "she", "he", "him", "his",
    "them", "us", "i'm", "you're", "he's", "she's", "it's", "we've", "they've", 
    "we'll", "they'll", "i'll", "you'll", "i've", "you've", "don't", "doesn't", 
    "didn't", "can't", "couldn't", "shouldn't", "won't", "wouldn't"
}

def normalizar_texto(texto):
    texto_normalizado = ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower()) if unicodedata.category(c) != 'Mn'
    )
    return texto_normalizado

def limpiar_texto(texto: str) -> list:
    palabras = re.sub(r"[^\w\s]", "", texto.lower()).split()
    return [palabra for palabra in palabras if palabra not in STOP_WORDS]

@router.get("/word_cloud_endpoint")
async def get_frec_palabras():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/titulos/")
            response.raise_for_status()
            titulos = response.json()

        palabras_totales = []
        for titulo in titulos:
            palabras_totales.extend(limpiar_texto(titulo.get("titulo", "")))

        frecuencias = Counter(palabras_totales)
        words = [{"text": palabra, "value": frecuencia} for palabra, frecuencia in frecuencias.items()]
        return words

    except httpx.HTTPError as error:
        return {"error": f"No se pudo obtener los datos: {str(error)}"}

@router.get("/color_bubble_endpoint")
async def get_frec_palabras():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/titulos/")
            response.raise_for_status()
            titulos = response.json()

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/sys_data/etiquetas_etiqueta_color")
            response.raise_for_status()
            COLORES_ETIQUETAS = response.json()["COLORES_ETIQUETAS"]

        etiquetas_counter = Counter()
        etiquetas_originales = {}

        for titulo in titulos:
            etiquetas = titulo.get("etiquetas", [])
            for etiqueta in etiquetas:
                etiqueta_normalizada = normalizar_texto(etiqueta)
                etiquetas_counter[etiqueta_normalizada] += 1
                if etiqueta_normalizada not in etiquetas_originales:
                    etiquetas_originales[etiqueta_normalizada] = etiqueta.capitalize()

        formatted_data = [
            {
                "id": etiquetas_originales[etiqueta],
                "value": frecuencia,
                "color": COLORES_ETIQUETAS.get(etiquetas_originales[etiqueta], "#000000") 
            }
            for etiqueta, frecuencia in etiquetas_counter.items()
        ]
        return formatted_data

    except httpx.HTTPError as error:
        return {"error": f"No se pudo obtener los datos: {str(error)}"}
    
@router.get("/relationship_graph_endpoint")
async def get_frec_palabras():
    relaciones = [
        {"type": "Practica Inicial", "data": []},
        {"type": "Practica Profesional", "data": []},
        {"type": "TT: Tesis Pregrado", "data": []},
        {"type": "TT: Tesis Postgrado", "data": []},
        {"type": "TT: Articulo Pregrado", "data": []},
        {"type": "TT: Articulo Postgrado", "data": []},
        {"type": "Articulo", "data": []},
        {"type": "Proyectos", "data": []}
    ]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/practicas/iniciales")
        response.raise_for_status()
        data = response.json()  
        for elem in data:
            participantes = elem.get("participantes", []) 
            for participante in participantes:  
                for relacion in relaciones:
                    if relacion["type"] == "Practica Inicial":
                        if participante not in relacion["data"]:
                            relacion["data"].append(participante)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/practicas/profesionales")
        response.raise_for_status()
        data = response.json()  
        for elem in data:
            participantes = elem.get("participantes", []) 
            for participante in participantes:  
                for relacion in relaciones:
                    if relacion["type"] == "Practica Profesional":
                        if participante not in relacion["data"]:
                            relacion["data"].append(participante)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/articulos/")
        response.raise_for_status()
        data = response.json()  

        for elem in data.get("articulos", []):
            participantes = elem.get("participantes", []) 
            for participante in participantes:  
                for relacion in relaciones:
                    if relacion["type"] == "Articulo":
                        if participante not in relacion["data"]:
                            relacion["data"].append(participante)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/tesis/pregrado")
        response.raise_for_status()
        data = response.json()  
        for elem in data["articulos"]:
            if elem.get("tipo") == "Tesis":
                participantes = elem.get("participantes", []) 
                for participante in participantes:  
                    for relacion in relaciones:
                        if relacion["type"] == "TT: Tesis Pregrado":
                            if participante not in relacion["data"]:
                                relacion["data"].append(participante)
            elif elem.get("tipo") == "Artículo":
                participantes = elem.get("participantes", []) 
                for participante in participantes:  
                    for relacion in relaciones:
                        if relacion["type"] == "TT: Articulo Pregrado":
                            if participante not in relacion["data"]:
                                relacion["data"].append(participante)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/tesis/postgrado")
        response.raise_for_status()
        data = response.json()  
        for elem in data["articulos"]:
            if elem.get("tipo") == "Tesis":
                participantes = elem.get("participantes", []) 
                for participante in participantes:  
                    for relacion in relaciones:
                        if relacion["type"] == "TT: Tesis Postgrado":
                            if participante not in relacion["data"]:
                                relacion["data"].append(participante)

            elif elem.get("tipo") == "Artículo":
                participantes = elem.get("participantes", []) 
                for participante in participantes:  
                    for relacion in relaciones:
                        if relacion["type"] == "TT: Articulo Postgrado":
                            if participante not in relacion["data"]:
                                relacion["data"].append(participante)
    return relaciones
    
@router.get("/zoomable_bubble_endpoint")
async def get_frec_palabras():
    practicas_iniciales = []
    practicas_profesionales = []
    articulos = []
    TT_articulos_pred = []
    TT_articulos_post = []
    TT_tesis_pred = []
    TT_tesis_post = []
    proyectos = []

    async with httpx.AsyncClient() as client:
        people = {} 
        response = await client.get(f"{API_BASE_URL}/practicas/iniciales")
        response.raise_for_status()
        data = response.json()  

        for elem in data:
            nombre_practica = elem.get("nombre", "") 
            participantes = elem.get("participantes", []) 

            for participante in participantes:  
                if participante not in people:
                    people[participante] = {"works": []}
                
                people[participante]["works"].append(nombre_practica)

        practicas_iniciales = [{"name": name, "wname": person_data["works"]} for name, person_data in people.items()]

    async with httpx.AsyncClient() as client:
        people = {} 
        response = await client.get(f"{API_BASE_URL}/practicas/profesionales")
        response.raise_for_status()
        data = response.json()  

        for elem in data:
            nombre_practica = elem.get("nombre", "") 
            participantes = elem.get("participantes", []) 

            for participante in participantes:  
                if participante not in people:
                    people[participante] = {"works": []}
                
                people[participante]["works"].append(nombre_practica)

        practicas_profesionales = [{"name": name, "wname": person_data["works"]} for name, person_data in people.items()]

    async with httpx.AsyncClient() as client:
        people = {} 
        response = await client.get(f"{API_BASE_URL}/articulos/")
        response.raise_for_status()
        data = response.json()  

        for elem in data["articulos"]:
            nombre_articulo = elem.get("titulo", "") 
            participantes = elem.get("participantes", []) 

            for participante in participantes:  
                if participante not in people:
                    people[participante] = {"works": []}
                
                people[participante]["works"].append(nombre_articulo)

        articulos = [{"name": name, "wname": person_data["works"]} for name, person_data in people.items()]

    async with httpx.AsyncClient() as client:
        people_articulo = {}
        people_tesis = {} 
        response = await client.get(f"{API_BASE_URL}/tesis/pregrado")
        response.raise_for_status()
        data = response.json()  

        for elem in data["articulos"]:
            if elem.get("tipo") == "Tesis":
                nombre_articulo = elem.get("titulo", "") 
                participantes = elem.get("participantes", []) 

                for participante in participantes:  
                    if participante not in people_tesis:
                        people_tesis[participante] = {"works": []}
                    
                    people_tesis[participante]["works"].append(nombre_articulo)

                TT_tesis_pred = [{"name": name, "wname": person_data["works"]} for name, person_data in people_tesis.items()]

            elif elem.get("tipo") == "Artículo":
                nombre_articulo = elem.get("titulo", "") 
                participantes = elem.get("participantes", []) 

                for participante in participantes:  
                    if participante not in people_articulo:
                        people_articulo[participante] = {"works": []}
                    
                    people_articulo[participante]["works"].append(nombre_articulo)

                TT_articulos_pred = [{"name": name, "wname": person_data["works"]} for name, person_data in people_articulo.items()]

    async with httpx.AsyncClient() as client:
        people_articulo = {}
        people_tesis = {} 
        response = await client.get(f"{API_BASE_URL}/tesis/postgrado")
        response.raise_for_status()
        data = response.json()  

        for elem in data["articulos"]:
            if elem.get("tipo") == "Tesis":
                nombre_articulo = elem.get("titulo", "") 
                participantes = elem.get("participantes", []) 

                for participante in participantes:  
                    if participante not in people_tesis:
                        people_tesis[participante] = {"works": []}
                    
                    people_tesis[participante]["works"].append(nombre_articulo)

                TT_tesis_post = [{"name": name, "wname": person_data["works"]} for name, person_data in people_tesis.items()]

            elif elem.get("tipo") == "Artículo":
                nombre_articulo = elem.get("titulo", "") 
                participantes = elem.get("participantes", []) 

                for participante in participantes:  
                    if participante not in people_articulo:
                        people_articulo[participante] = {"works": []}
                    
                    people_articulo[participante]["works"].append(nombre_articulo)

                TT_articulos_post = [{"name": name, "wname": person_data["works"]} for name, person_data in people_articulo.items()]

    async with httpx.AsyncClient() as client:
        people = {} 
        response = await client.get(f"{API_BASE_URL}/proyectos/")
        response.raise_for_status()
        data = response.json()  

        for elem in data["proyectos"]:
            nombre_proyecto = elem.get("titulo", "") 
            participantes = elem.get("participantes", []) 

            for participante in participantes:  
                if participante not in people:
                    people[participante] = {"works": []}
                
                people[participante]["works"].append(nombre_proyecto)

        proyectos = [{"name": name, "wname": person_data["works"]} for name, person_data in people.items()]


    data = {
        "name": "root",
        "children": [
            {
                "name": "Practicas",
                "children": 
                [
                    {
                        "name": "Practicas Iniciales",
                        "children": practicas_iniciales
                    },
                    {
                        "name": "Practicas Profesionales",
                        "children": practicas_profesionales
                    }
                ]
            },
            {
                "name": "Trabajos de titulo",
                "children": [
                    {
                        "name": "Articulos",
                        "children": [
                            {
                                "name": "Articulos Pregrado",
                                "children": TT_articulos_pred
                            },
                            {
                                "name": "Articulos Postgrado",
                                "children": TT_articulos_post
                            }
                        ]
                    },
                    {
                        "name": "Tesis",
                        "children": [
                            {
                                "name": "Tesis Pregrado",
                                "children": TT_tesis_pred
                            },
                            {
                                "name": "Tesis Postgrado",
                                "children": TT_tesis_post
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Articulos",
                "children": articulos
            },
            {
                "name": "Proyectos",
                "children": proyectos
            }
        ]
    }

    return data