import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://usuario:clave*@localhost/egresados_mysql'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:D669820a*@localhost/egresados_mysql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
