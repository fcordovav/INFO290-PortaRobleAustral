from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import admin, instituciones, inicio, articulos, colaboradores, noticia, tesis, practica, persona,proyecto, titulos, interconexiones, sys_data, login

app = FastAPI()

#para que no salga el error del CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#incluir get y post de cada página
app.include_router(inicio.router)
app.include_router(articulos.router)
app.include_router(colaboradores.router)
app.include_router(noticia.router)
app.include_router(tesis.router)
app.include_router(practica.router)
app.include_router(persona.router)
app.include_router(proyecto.router)
app.include_router(titulos.router)
app.include_router(interconexiones.router)
app.include_router(login.router)
app.include_router(sys_data.router)
app.include_router(instituciones.router)
app.include_router(admin.router)

@app.get("/inicio/")
async def read_root():
    return {"message": "Hola desde FastAPI!"}