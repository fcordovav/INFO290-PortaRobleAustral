## Instalar Git

Instalar Git para poder gestionar el código fuente del proyecto y establecer una vinculación con el repositorio remoto.

- Git: https://git-scm.com/downloads

## Clonar este repositorio

Una vez que Git esté instalado, se debe clonar el repositorio en el directorio local. Esto permitirá obtener una copia del código en tu computadora para visualizarlo y ejecutar la página.

- Comando: git clone https://github.com/robleaustral/202402_INFO282_portalrobleaustral.git

## Instalar Tecnologías Backend

- Nodejs: https://nodejs.org/en/
- Python desde 3.12.x: https://www.python.org/downloads/

### Instalar librerías para el Backend

- Escribir el comando: pip install -r requirements.txt

## Instalar Tecnologías Frontend

Ya una vez instalado node, se instala el lenguaje principal de la página: TypeScript

- npm install -g typescript

### Instalar librerías para el Frontend

- Escribir el comando: npm install

## Ejecutar la aplicación con Docker

Se Incluyen Dockerfiles para ejecutar la aplicación usando Docker

- Descargar e instalar Docker siguiendo las instrucciones encontradas en: https://www.docker.com/
- En la carpeta del repositorio ejecutar el comando:  docker compose up --build
- La aplicación estará accesible desde https://localhost:3008/inicio

Eso es todo 👍
