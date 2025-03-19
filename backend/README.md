# Backend Roble Austral

Este documento contiene toda la información relevante sobre la instalación, ejecución y configuración del backend de Roble Austral.

## Instalación

El backend utiliza **Poetry**, una herramienta para gestionar dependencias y empaquetar proyectos en Python. Para instalar los paquetes necesarios, sigue estos pasos:

1. Instalar Poetry:

   ```bash
   pip install poetry
   ```

2. Instalar dependencias del proyecto:

   ```bash
   python -m poetry install
   ```

## Configuración

Se utiliza un archivo `.env` para configurar variables de entorno. Este archivo debe estar ubicado en la carpeta `backend` y debe contener las siguientes claves:

```.env
USER_ADM = <Nombre Admin>
PASS_ADM = <Password>
SESSION_TOKEN = <TOKEN>
API_BASE_URL = <API URL>
```

## Ejecución

Para ejecutar el servidor utiliza el siguiente comando:

```bash
python -m poetry run uvicorn main:app --port 4008 --reload
```
