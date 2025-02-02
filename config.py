import os

class Config:
    SECRET_KEY = 'super_secret_key'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://usuario:clave*@localhost:3366/egresados_mysql'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://eduard:yet13593642za@localhost/egresados_mysql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
