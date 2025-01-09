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
    git clone https://github.com/dani513/Proyecto_SistemasEgresados_OREFI.git
    cd Proyecto_SistemasEgresados_OREFI
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

4. Configura la base de datos :
    ```python
    mysql -u root -p
    CREATE DATABASE egresados_mysql
    USE egresados_mysql
    mysql -u root -p egresados_mysql < corrected_database_script.sql
    # Configuración en config.py 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Puedes cambiar a PostgreSQL u otro sistema
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```    

5. Configura la base de datos (utilizando Flask-Migrate):

```sh
    flask db init  # Solo si es la primera vez que configuras migraciones
    flask db migrate -m "Inicializar la base de datos"
    flask db upgrade
    ```
6. Ejecuta el servidor Flask:
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
