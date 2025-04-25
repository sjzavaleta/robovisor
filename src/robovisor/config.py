import os

class Config:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 

class DevelopmentConfig(Config):
    DEBUG = True
    DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Prices.sqlite3'))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"