# Proyecto Flask y Vue.js para Gestión de Egresados

Este proyecto es una aplicación web desarrollada con Flask y Vue.js para la gestión de egresados. Permite agregar, consultar, editar y eliminar egresados, así como generar cartas y gestionar información del director y decano.

## Requisitos Previos

- Python 3.6+
- Node.js 12+
- npm 6+

## Instalación

### Backend (Flask)

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configura la base de datos (utilizando Flask-Migrate):
    ```sh
    flask db init  # Solo si es la primera vez que configuras migraciones
    flask db migrate -m "Inicializar la base de datos"
    flask db upgrade
    ```

5. Ejecuta el servidor Flask:
    ```sh
    flask run
    ```

### Frontend (Vue.js)

1. Ve a la carpeta `frontend`:
    ```sh
    cd frontend
    ```

2. Instala las dependencias:
    ```sh
    npm install
    ```

3. Ejecuta el servidor de desarrollo de Vue.js:
    ```sh
    npm run serve
    ```

## Estructura del Proyecto

