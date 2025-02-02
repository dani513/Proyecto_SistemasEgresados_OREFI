from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.models import Usuario
    @login.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from app import routes, models
    app.register_blueprint(routes.bp)

    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Cambiar a 'None' si necesitas solicitudes cross-origin con HTTPS
    app.config['SESSION_COOKIE_SECURE'] = True 

    return app
